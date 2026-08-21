// Exact search for small unions of relabelled Cycle-3 RR_n families.
//
// This program counts literal subsets and checks the full induced
// inclusion-by-one DAG.  It never substitutes seed-path coverage for union
// coverage.  The only shortcut is exact: a coloring accepted by any one
// copy is already accepted by the union, so the union DAG need only be run
// on colorings rejected by every individual copy.

#include <algorithm>
#include <bit>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <utility>
#include <vector>

using Mask = std::uint64_t;

namespace {

Mask low_mask(int bits) {
    if (bits == 64) return ~Mask{0};
    return (Mask{1} << bits) - 1;
}

Mask rotate_down(Mask value, int amount, int width) {
    assert(width > 0 && width < 64);
    amount %= width;
    value &= low_mask(width);
    if (amount == 0) return value;
    return ((value >> amount) | (value << (width - amount))) & low_mask(width);
}

bool rr_accepts_normalized_word(Mask word, int q) {
    // Forward form of the exact Cycle-3 cyclic-interval recurrence.
    Mask current = word;
    const Mask boundary = word ^ rotate_down(word, 1, q);
    for (int length = 1; length < q; length += 2) {
        const Mask add_left_left = rotate_down(current, 2, q) & boundary;
        const Mask add_split = rotate_down(current, 1, q)
                             & (word ^ rotate_down(word, length + 1, q));
        const Mask add_right_right = current & rotate_down(boundary, length, q);
        current = add_left_left | add_split | add_right_right;
        if (current == 0) return false;
    }
    return current != 0;
}

std::uint64_t choose_u64(int n, int k) {
    if (k < 0 || k > n) return 0;
    k = std::min(k, n - k);
    unsigned __int128 answer = 1;
    for (int i = 1; i <= k; ++i) {
        answer = answer * static_cast<unsigned>(n - k + i) / static_cast<unsigned>(i);
    }
    if (answer > std::numeric_limits<std::uint64_t>::max()) {
        throw std::overflow_error("binomial coefficient does not fit uint64");
    }
    return static_cast<std::uint64_t>(answer);
}

struct FailureData {
    int n{};
    int q{};
    int weight{};
    std::uint64_t necklace_count{};
    std::vector<Mask> failing_necklace_representatives;
    std::vector<Mask> normalized_failure_masks;
};

FailureData enumerate_rr_failures(int n) {
    if (n < 2 || n % 2 != 0 || n >= 64) {
        throw std::invalid_argument("n must be positive, even, and below 64");
    }
    const int q = n - 1;
    const int weight = n / 2;
    std::vector<int> a(q + 1, 0);
    FailureData out;
    out.n = n;
    out.q = q;
    out.weight = weight;

    std::function<void(int, int, int)> generate = [&](int t, int period, int ones) {
        const int unassigned = q - t + 1;
        if (ones > weight || ones + unassigned < weight) return;
        if (t > q) {
            if (q % period != 0 || ones != weight) return;
            ++out.necklace_count;
            Mask word = 0;
            for (int i = 1; i <= q; ++i) {
                if (a[i]) word |= Mask{1} << (i - 1);
            }
            if (!rr_accepts_normalized_word(word, q)) {
                out.failing_necklace_representatives.push_back(word);
            }
            return;
        }

        a[t] = a[t - period];
        generate(t + 1, period, ones + a[t]);
        if (a[t - period] == 0) {
            a[t] = 1;
            generate(t + 1, t, ones + 1);
        }
    };
    generate(1, 1, 0);

    const std::uint64_t expected_necklaces = choose_u64(q, weight) / static_cast<unsigned>(q);
    if (out.necklace_count != expected_necklaces) {
        throw std::runtime_error("fixed-weight necklace count mismatch");
    }

    out.normalized_failure_masks.reserve(out.failing_necklace_representatives.size()
                                         * static_cast<std::size_t>(q));
    for (Mask representative : out.failing_necklace_representatives) {
        for (int shift = 0; shift < q; ++shift) {
            out.normalized_failure_masks.push_back(rotate_down(representative, shift, q));
        }
    }
    std::sort(out.normalized_failure_masks.begin(), out.normalized_failure_masks.end());
    out.normalized_failure_masks.erase(
        std::unique(out.normalized_failure_masks.begin(), out.normalized_failure_masks.end()),
        out.normalized_failure_masks.end());
    if (out.normalized_failure_masks.size()
        != out.failing_necklace_representatives.size() * static_cast<std::size_t>(q)) {
        throw std::runtime_error("unexpected periodic fixed-weight word");
    }
    return out;
}

using Permutation = std::vector<int>;

Permutation identity_permutation(int n) {
    Permutation p(n);
    std::iota(p.begin(), p.end(), 0);
    return p;
}

Permutation inverse_permutation(const Permutation& p) {
    Permutation inverse(p.size());
    for (int i = 0; i < static_cast<int>(p.size()); ++i) inverse[p[i]] = i;
    return inverse;
}

Mask permute_mask(Mask mask, const Permutation& p) {
    Mask result = 0;
    while (mask) {
        const int point = std::countr_zero(mask);
        result |= Mask{1} << p[point];
        mask &= mask - 1;
    }
    return result;
}

Mask sign_normalize(Mask plus, int n) {
    if (plus & (Mask{1} << (n - 1))) plus ^= low_mask(n);
    return plus;
}

bool base_rejects(Mask normalized_plus, const FailureData& failures) {
    return std::binary_search(failures.normalized_failure_masks.begin(),
                              failures.normalized_failure_masks.end(),
                              normalized_plus);
}

bool copy_rejects(Mask physical_normalized_plus,
                  const Permutation& inverse,
                  const FailureData& failures) {
    Mask pulled_back = permute_mask(physical_normalized_plus, inverse);
    pulled_back = sign_normalize(pulled_back, failures.n);
    return base_rejects(pulled_back, failures);
}

std::vector<Mask> common_individual_rejections(const FailureData& failures,
                                               const std::vector<Permutation>& copies) {
    assert(!copies.empty());
    std::vector<Permutation> inverses;
    inverses.reserve(copies.size());
    for (const auto& p : copies) inverses.push_back(inverse_permutation(p));

    std::vector<Mask> survivors;
    survivors.reserve(failures.normalized_failure_masks.size());
    for (Mask plus : failures.normalized_failure_masks) {
        bool rejected_by_all = true;
        for (std::size_t i = 1; i < copies.size(); ++i) {
            if (!copy_rejects(plus, inverses[i], failures)) {
                rejected_by_all = false;
                break;
            }
        }
        if (rejected_by_all) survivors.push_back(plus);
    }
    return survivors;
}

Mask cyclic_interval_mask(int q, int start, int length) {
    Mask result = 0;
    for (int offset = 0; offset < length; ++offset) {
        result |= Mask{1} << ((start + offset) % q);
    }
    return result;
}

std::vector<std::vector<Mask>> base_rr_ranks(int n) {
    const int q = n - 1;
    std::vector<std::vector<Mask>> ranks(n + 1);
    ranks[0].push_back(0);
    for (int point = 0; point < q; ++point) ranks[1].push_back(Mask{1} << point);
    const Mask infinity = Mask{1} << q;
    for (int rank = 2; rank < n; ++rank) {
        for (int start = 0; start < q; ++start) {
            ranks[rank].push_back(infinity | cyclic_interval_mask(q, start, rank - 1));
        }
    }
    ranks[n].push_back(low_mask(n));
    return ranks;
}

struct LiteralUnionDag {
    int n{};
    std::vector<std::vector<Mask>> ranks;
    std::vector<std::vector<std::vector<int>>> parents;
    std::size_t literal_subset_count{};

    bool accepts(Mask plus) const {
        std::vector<unsigned char> previous(1, 1);
        for (int rank = 1; rank <= n; ++rank) {
            std::vector<unsigned char> current(ranks[rank].size(), 0);
            for (std::size_t j = 0; j < ranks[rank].size(); ++j) {
                const Mask state = ranks[rank][j];
                const int plus_count = std::popcount(state & plus);
                if (std::abs(2 * plus_count - rank) > 1) continue;
                for (int parent : parents[rank][j]) {
                    if (previous[parent]) {
                        current[j] = 1;
                        break;
                    }
                }
            }
            previous.swap(current);
            if (std::none_of(previous.begin(), previous.end(), [](unsigned char x) { return x; })) {
                return false;
            }
        }
        return previous.size() == 1 && previous[0] != 0;
    }
};

LiteralUnionDag build_literal_union(int n, const std::vector<Permutation>& copies) {
    LiteralUnionDag dag;
    dag.n = n;
    dag.ranks.resize(n + 1);
    dag.parents.resize(n + 1);
    const auto base = base_rr_ranks(n);
    for (int rank = 0; rank <= n; ++rank) {
        for (const auto& p : copies) {
            for (Mask state : base[rank]) dag.ranks[rank].push_back(permute_mask(state, p));
        }
        auto& row = dag.ranks[rank];
        std::sort(row.begin(), row.end());
        row.erase(std::unique(row.begin(), row.end()), row.end());
        dag.literal_subset_count += row.size();
    }

    for (int rank = 1; rank <= n; ++rank) {
        dag.parents[rank].resize(dag.ranks[rank].size());
        const auto& prior = dag.ranks[rank - 1];
        for (std::size_t j = 0; j < dag.ranks[rank].size(); ++j) {
            Mask bits = dag.ranks[rank][j];
            while (bits) {
                const int point = std::countr_zero(bits);
                const Mask parent = dag.ranks[rank][j] ^ (Mask{1} << point);
                auto it = std::lower_bound(prior.begin(), prior.end(), parent);
                if (it != prior.end() && *it == parent) {
                    dag.parents[rank][j].push_back(static_cast<int>(it - prior.begin()));
                }
                bits &= bits - 1;
            }
        }
    }
    return dag;
}

struct UnionCheck {
    std::size_t common_individual_rejections{};
    std::size_t full_union_rejections{};
    std::size_t hybrid_only_acceptances{};
    LiteralUnionDag dag;
};

bool lex_word_less(Mask left, Mask right, int q) {
    for (int position = 0; position < q; ++position) {
        const bool a = (left >> position) & 1;
        const bool b = (right >> position) & 1;
        if (a != b) return a < b;
    }
    return false;
}

Mask least_rotation_mask(Mask word, int q) {
    Mask least = word;
    for (int shift = 1; shift < q; ++shift) {
        const Mask rotated = rotate_down(word, shift, q);
        if (lex_word_less(rotated, least, q)) least = rotated;
    }
    return least;
}

UnionCheck check_union(const FailureData& failures,
                       const std::vector<Permutation>& copies) {
    UnionCheck result;
    auto common = common_individual_rejections(failures, copies);
    result.common_individual_rejections = common.size();
    result.dag = build_literal_union(failures.n, copies);
    for (Mask plus : common) {
        if (!result.dag.accepts(plus)) ++result.full_union_rejections;
    }
    result.hybrid_only_acceptances = result.common_individual_rejections
                                   - result.full_union_rejections;
    return result;
}

UnionCheck check_rotation_equivariant_pair(const FailureData& failures,
                                           const Permutation& candidate) {
    // Used for finite-cycle multipliers fixing infinity.  Both copies and
    // their union are invariant under finite cyclic translations, so one
    // representative per common failure orbit is sufficient.  Every orbit
    // has size q because gcd(q,(q+1)/2)=1.
    const auto inverse = inverse_permutation(candidate);
    std::unordered_set<Mask> bad_orbits(
        failures.failing_necklace_representatives.begin(),
        failures.failing_necklace_representatives.end());
    std::vector<Mask> common_orbits;
    for (Mask representative : failures.failing_necklace_representatives) {
        const Mask pulled = permute_mask(representative, inverse);
        const Mask canonical = least_rotation_mask(pulled, failures.q);
        if (bad_orbits.contains(canonical)) common_orbits.push_back(representative);
    }

    UnionCheck result;
    result.common_individual_rejections = common_orbits.size()
                                        * static_cast<std::size_t>(failures.q);
    result.dag = build_literal_union(
        failures.n, {identity_permutation(failures.n), candidate});
    std::size_t rejected_orbits = 0;
    for (Mask plus : common_orbits) {
        if (!result.dag.accepts(plus)) ++rejected_orbits;
    }
    result.full_union_rejections = rejected_orbits * static_cast<std::size_t>(failures.q);
    result.hybrid_only_acceptances = result.common_individual_rejections
                                   - result.full_union_rejections;
    return result;
}

std::string permutation_json(const Permutation& p) {
    std::ostringstream out;
    out << '[';
    for (std::size_t i = 0; i < p.size(); ++i) {
        if (i) out << ',';
        out << p[i];
    }
    out << ']';
    return out.str();
}

std::string rank_profile_json(const LiteralUnionDag& dag) {
    std::ostringstream out;
    out << '[';
    for (int rank = 0; rank <= dag.n; ++rank) {
        if (rank) out << ',';
        out << dag.ranks[rank].size();
    }
    out << ']';
    return out.str();
}

std::uint64_t fnv1a_masks(const std::vector<Mask>& masks) {
    std::uint64_t hash = 1469598103934665603ULL;
    for (Mask mask : masks) {
        for (int byte = 0; byte < 8; ++byte) {
            hash ^= static_cast<unsigned char>((mask >> (8 * byte)) & 0xff);
            hash *= 1099511628211ULL;
        }
    }
    return hash;
}

struct CandidateSpec {
    std::string kind;
    Permutation permutation;
    bool rotation_equivariant{};
};

std::vector<CandidateSpec> algebraic_candidates(int n) {
    std::vector<CandidateSpec> candidates;
    const int q = n - 1;

    // Multipliers of the finite cycle, with infinity fixed.  Translation is
    // an automorphism of RR_n and would not create a new copy.
    for (int a = 2; a < q; ++a) {
        if (std::gcd(a, q) != 1 || a == q - 1) continue;
        Permutation p(n);
        for (int x = 0; x < q; ++x) p[x] = (a * x) % q;
        p[q] = q;
        candidates.push_back({"finite_multiplier_" + std::to_string(a), std::move(p), true});
    }

    // Affine permutations of all n labels.  These generally move the
    // distinguished infinity point and are not RR automorphisms.
    for (int a = 1; a < n; ++a) {
        if (std::gcd(a, n) != 1) continue;
        for (int b = 0; b < n; ++b) {
            if (a == 1 && b == 0) continue;
            Permutation p(n);
            for (int x = 0; x < n; ++x) p[x] = (a * x + b) % n;
            candidates.push_back({"full_affine_" + std::to_string(a) + "_" + std::to_string(b),
                                  std::move(p), false});
        }
    }
    return candidates;
}

void write_representatives(const FailureData& failures, const std::filesystem::path& path) {
    std::ofstream out(path, std::ios::binary);
    if (!out) throw std::runtime_error("cannot open representative output");
    out << "# q=" << failures.q << " weight=" << failures.weight
        << " failing_necklaces=" << failures.failing_necklace_representatives.size() << "\n";
    out << std::hex << std::setfill('0');
    const int digits = (failures.q + 3) / 4;
    for (Mask mask : failures.failing_necklace_representatives) {
        out << std::setw(digits) << mask << '\n';
    }
}

void write_certificate(const FailureData& failures,
                       const std::vector<Permutation>& copies,
                       const std::vector<std::string>& kinds,
                       const UnionCheck& checked,
                       std::uint64_t seed,
                       std::size_t candidate_number,
                       const std::filesystem::path& output_dir) {
    const int n = failures.n;
    const auto reps_name = "cycle04_multi_rr_failure_necklaces_n" + std::to_string(n) + ".txt";
    write_representatives(failures, output_dir / reps_name);

    const auto cert_name = "cycle04_multi_rr_n" + std::to_string(n) + ".json";
    std::ofstream out(output_dir / cert_name, std::ios::binary);
    if (!out) throw std::runtime_error("cannot open certificate output");
    out << "{\n";
    out << "  \"schema\": \"cycle04-multi-rr-v1\",\n";
    out << "  \"epistemic_status\": \"EXHAUSTIVE_FINITE_COMPUTATION\",\n";
    out << "  \"n\": " << n << ",\n";
    out << "  \"q\": " << failures.q << ",\n";
    out << "  \"normalized_balanced_colorings\": " << choose_u64(n - 1, n / 2) << ",\n";
    out << "  \"fixed_weight_necklaces\": " << failures.necklace_count << ",\n";
    out << "  \"one_copy_normalized_rejections\": "
        << failures.normalized_failure_masks.size() << ",\n";
    out << "  \"one_copy_failing_necklaces\": "
        << failures.failing_necklace_representatives.size() << ",\n";
    out << "  \"one_copy_failure_masks_fnv1a64_le\": \""
        << std::hex << std::setw(16) << std::setfill('0')
        << fnv1a_masks(failures.normalized_failure_masks) << std::dec << "\",\n";
    out << "  \"failure_necklace_file\": \"" << reps_name << "\",\n";
    out << "  \"copy_count\": " << copies.size() << ",\n";
    out << "  \"minimum_t_exact\": "
        << ((checked.full_union_rejections == 0 && !failures.normalized_failure_masks.empty()
             && copies.size() == 2) ? "2" : "null") << ",\n";
    out << "  \"search_seed\": " << seed << ",\n";
    out << "  \"successful_candidate_number\": " << candidate_number << ",\n";
    out << "  \"permutation_kinds\": [";
    for (std::size_t i = 0; i < kinds.size(); ++i) {
        if (i) out << ',';
        out << '\"' << kinds[i] << '\"';
    }
    out << "],\n";
    out << "  \"permutations_old_to_new\": [\n";
    for (std::size_t i = 0; i < copies.size(); ++i) {
        out << "    " << permutation_json(copies[i]) << (i + 1 == copies.size() ? "\n" : ",\n");
    }
    out << "  ],\n";
    out << "  \"common_individual_rejections\": "
        << checked.common_individual_rejections << ",\n";
    out << "  \"hybrid_only_acceptances\": " << checked.hybrid_only_acceptances << ",\n";
    out << "  \"full_literal_union_rejections\": " << checked.full_union_rejections << ",\n";
    out << "  \"literal_distinct_subset_count\": " << checked.dag.literal_subset_count << ",\n";
    out << "  \"literal_rank_profile\": " << rank_profile_json(checked.dag) << ",\n";
    out << "  \"proof_scope\": \"All sign-orbits: exact necklace exhaustion for individual failures, followed by full induced literal-subset-DAG search on their exact intersection.\"\n";
    out << "}\n";
}

struct CandidateResult {
    bool found{};
    Permutation permutation;
    std::string kind;
    UnionCheck checked;
    std::size_t candidate_number{};
};

CandidateResult search_two_copies(const FailureData& failures,
                                  std::uint64_t seed,
                                  int random_trials) {
    const int n = failures.n;
    const auto identity = identity_permutation(n);
    auto candidates = algebraic_candidates(n);
    std::mt19937_64 rng(seed);
    for (int trial = 0; trial < random_trials; ++trial) {
        auto p = identity;
        std::shuffle(p.begin(), p.end(), rng);
        candidates.push_back({"random_" + std::to_string(trial), std::move(p), false});
    }

    std::size_t number = 0;
    std::size_t best_union_reject = std::numeric_limits<std::size_t>::max();
    for (auto& spec : candidates) {
        ++number;
        const auto& kind = spec.kind;
        const auto& candidate = spec.permutation;
        std::vector<Permutation> copies{identity, candidate};
        UnionCheck checked = spec.rotation_equivariant
                           ? check_rotation_equivariant_pair(failures, candidate)
                           : check_union(failures, copies);
        if (checked.full_union_rejections < best_union_reject) {
            best_union_reject = checked.full_union_rejections;
            std::cerr << "n=" << n << " candidate=" << number << " kind=" << kind
                      << " common=" << checked.common_individual_rejections
                      << " union_reject=" << checked.full_union_rejections
                      << " literals=" << checked.dag.literal_subset_count << '\n';
        }
        if (checked.full_union_rejections == 0) {
            return {true, candidate, kind, std::move(checked), number};
        }
    }
    return {};
}

} // namespace

int main(int argc, char** argv) {
    try {
        if (argc != 6) {
            std::cerr << "usage: cycle04_multi_rr_search MIN_EVEN_N MAX_EVEN_N OUTPUT_DIR SEED RANDOM_TRIALS\n";
            return 2;
        }
        const int min_n = std::stoi(argv[1]);
        const int max_n = std::stoi(argv[2]);
        const std::filesystem::path output_dir = argv[3];
        const std::uint64_t master_seed = std::stoull(argv[4]);
        const int random_trials = std::stoi(argv[5]);
        std::filesystem::create_directories(output_dir);

        for (int n = min_n; n <= max_n; n += 2) {
            const auto began = std::chrono::steady_clock::now();
            FailureData failures = enumerate_rr_failures(n);
            std::cerr << "n=" << n << " necklaces=" << failures.necklace_count
                      << " bad_necklaces=" << failures.failing_necklace_representatives.size()
                      << " bad_words=" << failures.normalized_failure_masks.size() << '\n';
            if (failures.normalized_failure_masks.empty()) {
                std::cerr << "n=" << n << " one copy is already valid; no two-copy search needed\n";
                continue;
            }

            const std::uint64_t seed = master_seed ^ (0x9e3779b97f4a7c15ULL * static_cast<unsigned>(n));
            CandidateResult result = search_two_copies(failures, seed, random_trials);
            if (result.found) {
                std::vector<Permutation> copies{identity_permutation(n), result.permutation};
                std::vector<std::string> kinds{"identity", result.kind};
                write_certificate(failures, copies, kinds, result.checked, seed,
                                  result.candidate_number, output_dir);
                std::cerr << "EXACT n=" << n << " minimum_t=2 kind=" << result.kind
                          << " common=" << result.checked.common_individual_rejections
                          << " hybrid=" << result.checked.hybrid_only_acceptances
                          << " literals=" << result.checked.dag.literal_subset_count << '\n';
            } else {
                std::cerr << "n=" << n << " no successful two-copy candidate in tested list\n";
            }
            const auto ended = std::chrono::steady_clock::now();
            std::cerr << "n=" << n << " elapsed_seconds="
                      << std::chrono::duration<double>(ended - began).count() << '\n';
        }
        return 0;
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
}

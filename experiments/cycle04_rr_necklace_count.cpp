#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

// Exact Cycle-4 counter for the corrected round-robin family RR_n.
//
// The program does not enumerate all binomial(q,(q+1)/2) normalized words.
// Because q=2m-1 is coprime to m, every such word has a full rotation orbit
// of size q.  The fixed-density FKM recursion below generates exactly one
// lexicographically least necklace representative per orbit.  Acceptance is
// then decided for all possible singleton starts simultaneously by a
// q-bit implementation of the exact cyclic-interval reachability recurrence.

namespace fs = std::filesystem;
using u64 = std::uint64_t;

static u64 choose_u64(int n, int k) {
    if (k < 0 || k > n) return 0;
    k = std::min(k, n - k);
    unsigned __int128 value = 1;
    for (int i = 1; i <= k; ++i) {
        value = value * static_cast<unsigned>(n - k + i) / static_cast<unsigned>(i);
    }
    if (value > static_cast<unsigned __int128>(~u64{0})) {
        throw std::overflow_error("binomial coefficient does not fit uint64_t");
    }
    return static_cast<u64>(value);
}

static u64 rotate_down(u64 value, int shift, int q, u64 mask) {
    shift %= q;
    if (shift == 0) return value & mask;
    return ((value >> shift) | (value << (q - shift))) & mask;
}

static bool rr_accepts(u64 word, int q) {
    const u64 mask = (u64{1} << q) - 1;
    u64 reachable = word;
    const u64 adjacent_difference = word ^ rotate_down(word, 1, q, mask);
    for (int length = 1; length < q; length += 2) {
        const u64 left_left =
            rotate_down(reachable, 2, q, mask) & adjacent_difference;
        const u64 left_right =
            rotate_down(reachable, 1, q, mask) &
            (word ^ rotate_down(word, length + 1, q, mask));
        const u64 right_right =
            reachable & rotate_down(adjacent_difference, length, q, mask);
        reachable = left_left | left_right | right_right;
        if (reachable == 0) return false;
    }
    return reachable != 0;
}

static std::string word_string(u64 word, int q) {
    std::string result;
    result.reserve(q);
    for (int i = 0; i < q; ++i) result.push_back((word >> i) & 1 ? '1' : '0');
    return result;
}

// Booth's algorithm, used only to decide whether reversal preserves a
// rotation orbit.  The FKM representative itself is already least rotation.
static std::string least_rotation(const std::string& input) {
    const int n = static_cast<int>(input.size());
    const std::string doubled = input + input;
    int i = 0;
    int j = 1;
    int k = 0;
    while (i < n && j < n && k < n) {
        const char a = doubled[i + k];
        const char b = doubled[j + k];
        if (a == b) {
            ++k;
            continue;
        }
        if (a > b) {
            i += k + 1;
            if (i <= j) i = j + 1;
        } else {
            j += k + 1;
            if (j <= i) j = i + 1;
        }
        k = 0;
    }
    const int start = std::min(i, j);
    return doubled.substr(start, n);
}

struct RunData {
    int cyclic_runs = 0;
    int max_zero_run = 0;
    int max_one_run = 0;
};

static RunData run_data(u64 word, int q) {
    RunData result;
    int boundary = -1;
    for (int i = 0; i < q; ++i) {
        const int previous = (i + q - 1) % q;
        if (((word >> i) & 1) != ((word >> previous) & 1)) {
            boundary = i;
            break;
        }
    }
    if (boundary < 0) {
        result.cyclic_runs = 1;
        if (word & 1) result.max_one_run = q;
        else result.max_zero_run = q;
        return result;
    }
    int current_bit = static_cast<int>((word >> boundary) & 1);
    int current_length = 0;
    for (int offset = 0; offset < q; ++offset) {
        const int position = (boundary + offset) % q;
        const int bit = static_cast<int>((word >> position) & 1);
        if (bit == current_bit) {
            ++current_length;
        } else {
            ++result.cyclic_runs;
            if (current_bit) result.max_one_run = std::max(result.max_one_run, current_length);
            else result.max_zero_run = std::max(result.max_zero_run, current_length);
            current_bit = bit;
            current_length = 1;
        }
    }
    ++result.cyclic_runs;
    if (current_bit) result.max_one_run = std::max(result.max_one_run, current_length);
    else result.max_zero_run = std::max(result.max_zero_run, current_length);
    return result;
}

static std::string json_map(const std::map<int, u64>& values, int indent) {
    std::ostringstream out;
    out << "{";
    bool first = true;
    for (const auto& [key, value] : values) {
        if (!first) out << ",";
        out << "\n" << std::string(indent + 2, ' ') << '"' << key << "\": " << value;
        first = false;
    }
    if (!values.empty()) out << "\n" << std::string(indent, ' ');
    out << "}";
    return out.str();
}

static std::string json_map(const std::map<std::string, u64>& values, int indent) {
    std::ostringstream out;
    out << "{";
    bool first = true;
    for (const auto& [key, value] : values) {
        if (!first) out << ",";
        out << "\n" << std::string(indent + 2, ' ') << '"' << key << "\": " << value;
        first = false;
    }
    if (!values.empty()) out << "\n" << std::string(indent, ' ');
    out << "}";
    return out.str();
}

struct Summary {
    int n = 0;
    int q = 0;
    int weight = 0;
    u64 normalized_words = 0;
    u64 necklace_orbits = 0;
    u64 rejected_orbits = 0;
    u64 reflection_symmetric_rejected_orbits = 0;
    u64 rejected_word_xor = 0;
    u64 rejected_word_sum_mod_2_64 = 0;
    std::map<int, u64> cyclic_run_orbits;
    std::map<int, u64> maximum_run_orbits;
    std::map<int, u64> maximum_zero_run_orbits;
    std::map<int, u64> maximum_one_run_orbits;
    std::map<std::string, u64> joint_run_profile_orbits;
};

class NecklaceCounter {
  public:
    NecklaceCounter(int n, const fs::path& output_directory)
        : output_directory_(output_directory) {
        summary_.n = n;
        summary_.q = n - 1;
        summary_.weight = n / 2;
        if (n < 2 || n % 2 || summary_.q > 63) {
            throw std::invalid_argument("n must be positive even with n-1 <= 63");
        }
        if (std::gcd(summary_.q, summary_.weight) != 1) {
            throw std::logic_error("expected gcd(2m-1,m)=1");
        }
        summary_.normalized_words = choose_u64(summary_.q, summary_.weight);
        digits_.assign(summary_.q + 1, 0);
        const std::string stem = "cycle04_rr_failures_n" + std::to_string(n) + ".txt";
        failure_relative_path_ = "certificates/cycle04_rr_acceptance/" + stem;
        failure_stream_.open(output_directory_ / stem, std::ios::binary);
        if (!failure_stream_) throw std::runtime_error("could not open failure output");
    }

    Summary run() {
        generate(1, 1, 0, 0);
        failure_stream_.close();
        if (summary_.necklace_orbits * static_cast<u64>(summary_.q) !=
            summary_.normalized_words) {
            throw std::logic_error("necklace orbit total does not equal binomial count");
        }
        return summary_;
    }

    const std::string& failure_relative_path() const { return failure_relative_path_; }

  private:
    Summary summary_;
    fs::path output_directory_;
    std::vector<unsigned char> digits_;
    std::ofstream failure_stream_;
    std::string failure_relative_path_;

    void generate(int position, int period, int ones, u64 word) {
        const int q = summary_.q;
        const int remaining = q - position + 1;
        if (ones > summary_.weight || ones + remaining < summary_.weight) return;
        if (position > q) {
            if (ones == summary_.weight && q % period == 0) {
                // Coprimality forces every fixed-weight orbit to be aperiodic.
                if (period != q) throw std::logic_error("unexpected short period");
                process(word);
            }
            return;
        }

        const unsigned char copied = digits_[position - period];
        digits_[position] = copied;
        generate(position + 1, period, ones + copied,
                 word | (static_cast<u64>(copied) << (position - 1)));
        if (copied == 0) {
            digits_[position] = 1;
            generate(position + 1, position, ones + 1,
                     word | (u64{1} << (position - 1)));
        }
    }

    void process(u64 word) {
        ++summary_.necklace_orbits;
        if (rr_accepts(word, summary_.q)) return;

        ++summary_.rejected_orbits;
        summary_.rejected_word_xor ^= word;
        summary_.rejected_word_sum_mod_2_64 += word;
        const std::string text = word_string(word, summary_.q);
        failure_stream_ << text << '\n';

        std::string reversed = text;
        std::reverse(reversed.begin(), reversed.end());
        if (least_rotation(reversed) == text) {
            ++summary_.reflection_symmetric_rejected_orbits;
        }

        const RunData runs = run_data(word, summary_.q);
        const int maximum_run = std::max(runs.max_zero_run, runs.max_one_run);
        ++summary_.cyclic_run_orbits[runs.cyclic_runs];
        ++summary_.maximum_run_orbits[maximum_run];
        ++summary_.maximum_zero_run_orbits[runs.max_zero_run];
        ++summary_.maximum_one_run_orbits[runs.max_one_run];
        const std::string key =
            std::to_string(runs.cyclic_runs) + "|" +
            std::to_string(runs.max_zero_run) + "|" +
            std::to_string(runs.max_one_run);
        ++summary_.joint_run_profile_orbits[key];
    }
};

static void write_summary(const Summary& s, const fs::path& output_directory,
                          const std::string& failure_relative_path,
                          double seconds) {
    const u64 rejected_words = s.rejected_orbits * static_cast<u64>(s.q);
    const u64 accepted_words = s.normalized_words - rejected_words;
    const u64 accepted_orbits = s.necklace_orbits - s.rejected_orbits;
    const u64 reflected = s.reflection_symmetric_rejected_orbits;
    if ((s.rejected_orbits - reflected) % 2 != 0) {
        throw std::logic_error("non-reflection rotation orbits do not pair under reversal");
    }
    const u64 rejected_dihedral_orbits =
        reflected + (s.rejected_orbits - reflected) / 2;

    const fs::path path = output_directory /
        ("cycle04_rr_acceptance_n" + std::to_string(s.n) + ".json");
    std::ofstream out(path, std::ios::binary);
    if (!out) throw std::runtime_error("could not open JSON output");
    out << "{\n";
    out << "  \"schema\": \"cycle04-rr-acceptance-v1\",\n";
    out << "  \"epistemic_status\": \"EXHAUSTIVE_NECKLACE_ENUMERATION\",\n";
    out << "  \"n\": " << s.n << ",\n";
    out << "  \"q\": " << s.q << ",\n";
    out << "  \"normalized_finite_weight\": " << s.weight << ",\n";
    out << "  \"normalized_balanced_words\": " << s.normalized_words << ",\n";
    out << "  \"accepted_normalized_words\": " << accepted_words << ",\n";
    out << "  \"rejected_normalized_words\": " << rejected_words << ",\n";
    out << "  \"acceptance_fraction_exact\": \"" << accepted_words << "/"
        << s.normalized_words << "\",\n";
    out << "  \"rejection_fraction_exact\": \"" << rejected_words << "/"
        << s.normalized_words << "\",\n";
    out << std::setprecision(17);
    out << "  \"acceptance_fraction_decimal\": "
        << static_cast<double>(accepted_words) / static_cast<double>(s.normalized_words)
        << ",\n";
    out << "  \"rejection_fraction_decimal\": "
        << static_cast<double>(rejected_words) / static_cast<double>(s.normalized_words)
        << ",\n";
    out << "  \"rotation_orbits_total\": " << s.necklace_orbits << ",\n";
    out << "  \"accepted_rotation_orbits\": " << accepted_orbits << ",\n";
    out << "  \"rejected_rotation_orbits\": " << s.rejected_orbits << ",\n";
    out << "  \"rotation_orbit_size\": " << s.q << ",\n";
    out << "  \"reflection_symmetric_rejected_rotation_orbits\": " << reflected << ",\n";
    out << "  \"rejected_dihedral_orbits\": " << rejected_dihedral_orbits << ",\n";
    out << "  \"failure_representatives_file\": \"" << failure_relative_path << "\",\n";
    out << "  \"failure_representative_xor_uint64\": " << s.rejected_word_xor << ",\n";
    out << "  \"failure_representative_sum_mod_2_64\": "
        << s.rejected_word_sum_mod_2_64 << ",\n";
    out << "  \"cyclic_run_count_rejected_rotation_orbits\": "
        << json_map(s.cyclic_run_orbits, 2) << ",\n";
    out << "  \"maximum_cyclic_run_rejected_rotation_orbits\": "
        << json_map(s.maximum_run_orbits, 2) << ",\n";
    out << "  \"maximum_zero_run_rejected_rotation_orbits\": "
        << json_map(s.maximum_zero_run_orbits, 2) << ",\n";
    out << "  \"maximum_one_run_rejected_rotation_orbits\": "
        << json_map(s.maximum_one_run_orbits, 2) << ",\n";
    out << "  \"joint_run_profile_rejected_rotation_orbits\": "
        << json_map(s.joint_run_profile_orbits, 2) << ",\n";
    out << "  \"runtime_seconds_informational\": " << seconds << "\n";
    out << "}\n";
}

int main(int argc, char** argv) {
    try {
        if (argc != 4) {
            std::cerr << "usage: cycle04_rr_necklace_count MIN_EVEN_N MAX_EVEN_N OUTPUT_DIR\n";
            return 2;
        }
        const int minimum_n = std::stoi(argv[1]);
        const int maximum_n = std::stoi(argv[2]);
        const fs::path output_directory = argv[3];
        if (minimum_n < 2 || minimum_n % 2 || maximum_n < minimum_n || maximum_n % 2) {
            throw std::invalid_argument("bounds must be positive even integers in increasing order");
        }
        fs::create_directories(output_directory);
        for (int n = minimum_n; n <= maximum_n; n += 2) {
            const auto start = std::chrono::steady_clock::now();
            NecklaceCounter counter(n, output_directory);
            const Summary summary = counter.run();
            const double seconds = std::chrono::duration<double>(
                std::chrono::steady_clock::now() - start).count();
            write_summary(summary, output_directory, counter.failure_relative_path(), seconds);
            std::cout << "n=" << n
                      << " normalized=" << summary.normalized_words
                      << " necklaces=" << summary.necklace_orbits
                      << " rejected_orbits=" << summary.rejected_orbits
                      << " rejected_words=" << summary.rejected_orbits * static_cast<u64>(summary.q)
                      << " seconds=" << std::fixed << std::setprecision(3) << seconds
                      << '\n';
        }
    } catch (const std::exception& error) {
        std::cerr << "ERROR: " << error.what() << '\n';
        return 1;
    }
    return 0;
}

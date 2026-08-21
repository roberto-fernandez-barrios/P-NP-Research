#include <algorithm>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <tuple>
#include <vector>

// Independent finite scanner for the corrected RR cyclic-interval recurrence.
// A q=2m-1 bit word has m ones and m-1 zeroes (the distinguished point is
// fixed negative).  The scanner counts literal interval-DAG acceptance, not
// acceptance by the listed round-robin seed paths.

namespace {

using u64 = std::uint64_t;

u64 low_mask(int q) {
  return q == 64 ? ~u64{0} : ((u64{1} << q) - 1);
}

u64 rotate_left(u64 x, int shift, int q) {
  const u64 mask = low_mask(q);
  shift %= q;
  if (shift < 0) shift += q;
  if (shift == 0) return x & mask;
  return ((x << shift) | (x >> (q - shift))) & mask;
}

bool rr_accepts_from(u64 word, int q, u64 allowed_roots) {
  const u64 mask = low_mask(q);
  // diff[j] says that positions j and j+1 (cyclically) are opposite.
  const u64 diff = (word ^ rotate_left(word, -1, q)) & mask;
  u64 reachable = word & allowed_roots & mask;
  if (reachable == 0) return false;
  for (int length = 1; length < q; length += 2) {
    // From start i, extend twice left, once on each side, or twice right.
    const u64 twice_left = rotate_left(reachable, -2, q) & diff;

    // New start j=i-1; compare old boundary positions i-1 and i+length.
    // These are j and j+length+1.
    const u64 separated_diff =
        (word ^ rotate_left(word, -(length + 1), q)) & mask;
    const u64 split = rotate_left(reachable, -1, q) & separated_diff;

    // Keep start i, requiring the pair at i+length,i+length+1 to cross.
    const u64 twice_right = reachable & rotate_left(diff, -length, q);
    reachable = twice_left | split | twice_right;
    if (reachable == 0) return false;
  }
  return reachable != 0;
}

bool rr_accepts(u64 word, int q) {
  return rr_accepts_from(word, q, low_mask(q));
}

bool root_zero_left_split_accepts(u64 word, int q) {
  if ((word & 1) == 0) return false;
  std::set<int> starts{0};
  auto sign = [&](int position) { return (word >> ((position % q + q) % q)) & 1; };
  for (int length = 1; length < q; length += 2) {
    std::set<int> following;
    for (int start : starts) {
      if (sign(start - 2) != sign(start - 1)) following.insert((start - 2 + q) % q);
      if (sign(start - 1) != sign(start + length)) following.insert((start - 1 + q) % q);
    }
    starts.swap(following);
    if (starts.empty()) return false;
  }
  return true;
}

bool greedy_accepts_from_root(u64 word, int q, int root) {
  if (((word >> root) & 1) == 0) return false;
  int start = root;
  auto sign = [&](int position) { return (word >> ((position % q + q) % q)) & 1; };
  for (int length = 1; length < q; length += 2) {
    // Fixed priority L, then X, then R.  This uses only information at the
    // actual current interval boundaries.
    if (sign(start - 2) != sign(start - 1)) {
      start = (start - 2 + q) % q;
    } else if (sign(start - 1) != sign(start + length)) {
      start = (start - 1 + q) % q;
    } else if (sign(start + length) != sign(start + length + 1)) {
      // start unchanged
    } else {
      return false;
    }
  }
  return true;
}

int capped_rooted_path_count(u64 word, int q, int root) {
  if (((word >> root) & 1) == 0) return 0;
  std::vector<unsigned char> current(q, 0), following(q, 0);
  current[root] = 1;
  auto add = [&](int target, int amount) {
    following[target] = static_cast<unsigned char>(
        std::min(2, static_cast<int>(following[target]) + amount));
  };
  auto sign = [&](int position) { return (word >> ((position % q + q) % q)) & 1; };
  for (int length = 1; length < q; length += 2) {
    std::fill(following.begin(), following.end(), 0);
    for (int start = 0; start < q; ++start) {
      if (!current[start]) continue;
      if (sign(start - 2) != sign(start - 1)) add((start - 2 + q) % q, current[start]);
      if (sign(start - 1) != sign(start + length)) add((start - 1 + q) % q, current[start]);
      if (sign(start + length) != sign(start + length + 1)) add(start, current[start]);
    }
    current.swap(following);
  }
  int result = 0;
  for (int count : current) result = std::min(2, result + count);
  return result;
}

int cyclic_runs(u64 word, int q) {
  int changes = 0;
  for (int i = 0; i < q; ++i) {
    changes += ((word >> i) & 1) != ((word >> ((i + 1) % q)) & 1);
  }
  return changes;
}

int max_cyclic_run(u64 word, int q) {
  if (word == 0 || word == low_mask(q)) return q;
  int first_change = 0;
  while (((word >> first_change) & 1) ==
         ((word >> ((first_change + 1) % q)) & 1)) {
    ++first_change;
  }
  int best = 1;
  int current = 1;
  for (int step = 1; step < q; ++step) {
    const int prev = (first_change + step) % q;
    const int next = (first_change + step + 1) % q;
    if (((word >> prev) & 1) == ((word >> next) & 1)) {
      ++current;
      best = std::max(best, current);
    } else {
      current = 1;
    }
  }
  return best;
}

u64 reverse_word(u64 word, int q) {
  u64 result = 0;
  for (int i = 0; i < q; ++i) {
    if ((word >> i) & 1) result |= u64{1} << (q - 1 - i);
  }
  return result;
}

u64 dihedral_canonical(u64 word, int q) {
  u64 best = word;
  const u64 reversed = reverse_word(word, q);
  for (int shift = 0; shift < q; ++shift) {
    best = std::min(best, rotate_left(word, shift, q));
    best = std::min(best, rotate_left(reversed, shift, q));
  }
  return best;
}

std::string bits(u64 word, int q) {
  std::string result;
  result.reserve(q);
  for (int i = 0; i < q; ++i) result.push_back((word >> i) & 1 ? '1' : '0');
  return result;
}

std::vector<int> cyclic_run_lengths(u64 word, int q) {
  int cut = 0;
  while (((word >> cut) & 1) == ((word >> ((cut + q - 1) % q)) & 1)) {
    ++cut;
  }
  std::vector<int> lengths;
  int length = 1;
  for (int step = 1; step < q; ++step) {
    const int prev = (cut + step - 1) % q;
    const int here = (cut + step) % q;
    if (((word >> prev) & 1) == ((word >> here) & 1)) {
      ++length;
    } else {
      lengths.push_back(length);
      length = 1;
    }
  }
  lengths.push_back(length);
  return lengths;
}

void scan(int q, std::size_t orbit_print_limit) {
  if (q < 1 || q > 63 || q % 2 == 0) {
    std::cerr << "q must be odd and lie in [1,63]\n";
    std::exit(2);
  }
  const int weight = (q + 1) / 2;
  u64 word = (u64{1} << weight) - 1;
  const u64 limit = u64{1} << q;
  std::uint64_t total = 0;
  std::uint64_t rejected = 0;
  std::uint64_t root_zero_accepted = 0;
  std::uint64_t root_zero_unique_path = 0;
  std::uint64_t root_zero_left_split = 0;
  std::uint64_t root_zero_greedy = 0;
  std::uint64_t some_root_greedy = 0;
  std::map<int, std::uint64_t> rejected_by_runs;
  std::map<int, std::uint64_t> rejected_by_max_run;
  std::set<u64> rejected_orbits;
  int largest_failure_run_count = -1;
  u64 largest_failure_run_example = 0;
  int smallest_failure_max_run = q + 1;
  u64 smallest_failure_max_run_example = 0;

  while (word < limit) {
    ++total;
    root_zero_accepted += rr_accepts_from(word, q, 1);
    root_zero_unique_path += capped_rooted_path_count(word, q, 0) == 1;
    root_zero_left_split += root_zero_left_split_accepts(word, q);
    root_zero_greedy += greedy_accepts_from_root(word, q, 0);
    bool any_greedy = false;
    for (int root = 0; root < q && !any_greedy; ++root) {
      any_greedy = greedy_accepts_from_root(word, q, root);
    }
    some_root_greedy += any_greedy;
    if (!rr_accepts(word, q)) {
      ++rejected;
      ++rejected_by_runs[cyclic_runs(word, q)];
      ++rejected_by_max_run[max_cyclic_run(word, q)];
      rejected_orbits.insert(dihedral_canonical(word, q));
      if (cyclic_runs(word, q) > largest_failure_run_count) {
        largest_failure_run_count = cyclic_runs(word, q);
        largest_failure_run_example = word;
      }
      if (max_cyclic_run(word, q) < smallest_failure_max_run) {
        smallest_failure_max_run = max_cyclic_run(word, q);
        smallest_failure_max_run_example = word;
      }
    }
    const u64 c = word & (~word + 1);
    const u64 r = word + c;
    if (r == 0) break;
    word = (((r ^ word) >> 2) / c) | r;  // Gosper's fixed-weight successor
  }

  std::cout << "q=" << q << " n=" << (q + 1) << " total=" << total
            << " accepted=" << (total - rejected) << " rejected=" << rejected
            << " root_zero_accepted=" << root_zero_accepted
            << " root_zero_unique_path=" << root_zero_unique_path
            << " root_zero_left_split=" << root_zero_left_split
            << " root_zero_greedy=" << root_zero_greedy
            << " some_root_greedy=" << some_root_greedy
            << " rejection_fraction=" << std::setprecision(17)
            << (static_cast<long double>(rejected) / total)
            << " dihedral_failure_orbits=" << rejected_orbits.size() << "\n";
  std::cout << "rejected_by_cyclic_runs";
  for (const auto& [key, value] : rejected_by_runs) {
    std::cout << ' ' << key << ':' << value;
  }
  std::cout << "\nrejected_by_max_cyclic_run";
  for (const auto& [key, value] : rejected_by_max_run) {
    std::cout << ' ' << key << ':' << value;
  }
  std::cout << '\n';
  if (rejected) {
    std::cout << "largest_failure_run_count=" << largest_failure_run_count
              << " example=" << bits(dihedral_canonical(largest_failure_run_example, q), q)
              << "\nsmallest_failure_max_run=" << smallest_failure_max_run
              << " example=" << bits(dihedral_canonical(smallest_failure_max_run_example, q), q)
              << '\n';
  }

  std::size_t shown = 0;
  for (u64 representative : rejected_orbits) {
    if (shown++ >= orbit_print_limit) break;
    std::cout << "orbit " << bits(representative, q) << " runs";
    for (int length : cyclic_run_lengths(representative, q)) {
      std::cout << ' ' << length;
    }
    std::cout << '\n';
  }
}

}  // namespace

int main(int argc, char** argv) {
  const int q = argc >= 2 ? std::atoi(argv[1]) : 21;
  const std::size_t print_limit = argc >= 3 ? std::strtoull(argv[2], nullptr, 10) : 20;
  scan(q, print_limit);
}

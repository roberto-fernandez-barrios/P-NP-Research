#include <algorithm>
#include <bit>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

using u64 = std::uint64_t;

bool balanced_state(u64 word, u64 state, int size) {
    const int plus = std::popcount(word & state);
    const int sum = 2 * plus - size;
    return (size & 1) ? sum == 1 : (sum == 0 || sum == 2);
}

std::vector<std::vector<u64>> standard_intervals(int q) {
    std::vector<std::vector<u64>> levels(q);
    for (int len = 1; len < q; ++len) {
        levels[len].resize(q);
        for (int start = 0; start < q; ++start) {
            u64 mask = 0;
            for (int offset = 0; offset < len; ++offset) {
                mask |= u64{1} << ((start + offset) % q);
            }
            levels[len][start] = mask;
        }
    }
    return levels;
}

bool rr_accepts(u64 word, int q, const std::vector<std::vector<u64>>& levels) {
    if (q == 1) {
        return word == 1;
    }

    std::vector<unsigned char> previous(q, 0), current(q, 0);
    for (int start = 0; start < q; ++start) {
        previous[start] = balanced_state(word, levels[1][start], 1);
    }

    for (int len = 2; len < q; ++len) {
        bool any = false;
        for (int start = 0; start < q; ++start) {
            const bool parent = previous[start] || previous[(start + 1) % q];
            current[start] = parent && balanced_state(word, levels[len][start], len);
            any = any || current[start];
        }
        if (!any) {
            return false;
        }
        previous.swap(current);
        std::fill(current.begin(), current.end(), 0);
    }

    for (unsigned char value : previous) {
        if (value) {
            return true;
        }
    }
    return false;
}

u64 next_same_popcount(u64 value) {
    const u64 low = value & (~value + 1);
    const u64 ripple = value + low;
    return ripple | (((value ^ ripple) >> 2) / low);
}

}  // namespace

int main(int argc, char** argv) {
    try {
        int n = 0;
        std::string dump_path;
        for (int i = 1; i < argc; ++i) {
            const std::string arg = argv[i];
            if (arg == "--n" && i + 1 < argc) {
                n = std::stoi(argv[++i]);
            } else if (arg == "--dump" && i + 1 < argc) {
                dump_path = argv[++i];
            } else {
                throw std::runtime_error("usage: enumerate_rr_failures --n EVEN [--dump PATH]");
            }
        }
        if (n < 2 || (n & 1) || n > 62) {
            throw std::runtime_error("n must be even and satisfy 2 <= n <= 62");
        }

        const int q = n - 1;
        const int weight = n / 2;
        const auto levels = standard_intervals(q);
        std::ofstream dump;
        if (!dump_path.empty()) {
            dump.open(dump_path, std::ios::binary);
            if (!dump) {
                throw std::runtime_error("cannot open dump path");
            }
        }

        const u64 limit = u64{1} << q;
        u64 word = (u64{1} << weight) - 1;
        std::uint64_t tested = 0;
        std::uint64_t rejected = 0;
        while (word < limit) {
            ++tested;
            if (!rr_accepts(word, q, levels)) {
                ++rejected;
                if (dump) {
                    dump << std::hex << word << '\n';
                }
            }
            const u64 next = next_same_popcount(word);
            if (next <= word) {
                break;
            }
            word = next;
        }

        std::cout << "n=" << n << " q=" << q << " tested=" << tested
                  << " rejected=" << rejected;
        if (!dump_path.empty()) {
            std::cout << " dump=" << dump_path;
        }
        std::cout << '\n';
        return 0;
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 2;
    }
}

// Cycle 5 Phase 5D: exhaustive / sampled scans of two-copy RR unions.
//
// Ground set: Z_q ∪ {∞}, q = n-1 odd.  Copy 1 = identity order; copy 2 given
// by an ∞-fixing permutation p of Z_q (copy 2 order C2[i] = p[i]).
// Normalized coloring = q-bit word w (bit x = 1 iff finite point x is plus),
// popcount = m = n/2.
//
// Per word:
//   rej1: single-copy recurrence on w.
//   rej2: single-copy recurrence on pullback word w∘p (pull[x] = w[p[x]]).
//   if both reject: run the two-order union DP (with cross arrows and
//   common-interval sync) and count rescued vs union-rejected.
//
// Union DP semantics (proved in research_cycle_05/hybrid_definitions.md,
// Lemma 5A.1, cross-checked against literal induced-DAG reference):
//   nested I_1 ⊂ … ⊂ I_{q-1}, |I_j|=j, each interval of ≥1 order,
//   plus-count p_j = (j+1)/2 at odd j, p_j ∈ {j/2, j/2+1} at even j.
//
// Modes:
//   --n N --transpose u,v | --swap a,b,len | --mult a | --randperm seed |
//   --perm csv           (explicit permutation of Z_q)
//   --sample R --seed s  (random words instead of exhaustive scan)
//   --list-cross         (print cross-arrow counts by length and exit)
//
// Build: g++ -O2 -std=c++17 -o cycle05_union_scan cycle05_union_scan.cpp

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <random>
#include <string>
#include <unordered_map>
#include <vector>

typedef uint64_t u64;
typedef unsigned __int128 u128;

static int Q, M;             // q = n-1, m = n/2
static u64 FULLQ;

static inline u64 rotr1(u64 x) { return ((x >> 1) | (x << (Q - 1))) & FULLQ; }

// ---------------------------------------------------------------- single copy
// Odd-interval growth recurrence: R over starts; returns true iff REJECTED.
static bool single_rejects(u64 w) {
    // neq[i] = 1 iff w_i != w_{i+1}
    u64 wrot = ((w >> 1) | (w << (Q - 1))) & FULLQ;   // bit i = w_{i+1}
    u64 neq = (w ^ wrot) & FULLQ;                     // bit i = [w_i != w_{i+1}]
    u64 R = w;
    for (int L = 1; L + 2 <= Q; L += 2) {
        if (!R) return true;
        u64 nxt = 0;
        // left-left: start i-2, need w_{i-2} != w_{i-1}: neq bit (i-2)
        u64 s = R;
        // shift start masks: bit i -> bit (i-2): rotate right by 2
        u64 Rm2 = ((R >> 2) | (R << (Q - 2))) & FULLQ;
        nxt |= Rm2 & (((neq)) ); // at position i-2 need neq_{i-2}
        // split: start i-1, need w_{i-1} != w_{i+L}
        u64 Rm1 = rotr1(R);
        // cond at new start j=i-1: w_j != w_{j+L+1}: build mask neqL: bit j = [w_j != w_{j+L+1}]
        u64 wrotL1 = ((w >> ((L + 1) % Q)) | (w << (Q - (L + 1) % Q))) & FULLQ;
        u64 neqL1 = (w ^ wrotL1) & FULLQ;
        nxt |= Rm1 & neqL1;
        // right-right: start i, need w_{i+L} != w_{i+L+1}: bit i of neq rotated: [w_{i+L} != w_{i+L+1}] = neq bit (i+L)
        u64 neqShift = ((neq >> (L % Q)) | (neq << (Q - L % Q))) & FULLQ;
        nxt |= R & neqShift;
        R = nxt;
    }
    return R == 0;
}

// ------------------------------------------------------------------ two-copy
struct UnionDP {
    std::vector<int> p;       // permutation of Z_q: copy-2 order C2[i] = p[i]
    std::vector<int> pinv;
    // cross/eq arrows per length: from (order o, start s) at length L to
    // (order o', start s') at length L+1  [cross], or same length [eq].
    // encoded: arrays of pairs (s, s2), one vector per (L, o->o').
    std::vector<std::vector<std::pair<int, int>>> cross01, cross10, eq;
    // interval mask helpers
    std::vector<u64> pref2;   // prefix masks of order 2

    void init(const std::vector<int>& perm) {
        p = perm;
        pinv.assign(Q, 0);
        for (int i = 0; i < Q; i++) pinv[p[i]] = i;
        pref2.assign(Q + 1, 0);
        for (int i = 0; i < Q; i++) pref2[i + 1] = pref2[i] | (1ULL << p[i]);
        cross01.assign(Q, {});
        cross10.assign(Q, {});
        eq.assign(Q, {});
        // interval mask of order o, start s, length L
        auto imask1 = [&](int s, int L) -> u64 {
            u64 m = 0;
            if (s + L <= Q) {
                m = ((L == 64 ? ~0ULL : ((1ULL << L) - 1)) << s);
            } else {
                int a = Q - s;
                m = (((1ULL << a) - 1) << s) | ((1ULL << (L - a)) - 1);
            }
            return m & FULLQ;
        };
        auto imask2 = [&](int s, int L) -> u64 {
            int e = s + L;
            if (e <= Q) return pref2[e] ^ pref2[s];
            return (pref2[Q] ^ pref2[s]) | pref2[e - Q];
        };
        // hash maps per length: mask -> start, for each order
        for (int L = 1; L + 1 <= Q - 1; L++) {
            std::unordered_map<u64, int> m1, m2;
            m1.reserve(Q * 2);
            m2.reserve(Q * 2);
            for (int s = 0; s < Q; s++) {
                m1[imask1(s, L)] = s;
                m2[imask2(s, L)] = s;
            }
            // eq at length L: same set in both orders
            for (auto& kv : m1) {
                auto it = m2.find(kv.first);
                if (it != m2.end()) eq[L].push_back({kv.second, it->second});
            }
            // cross into length L+1
            for (int s2 = 0; s2 < Q; s2++) {
                u64 big = imask2(s2, L + 1);
                u64 mm = big;
                while (mm) {
                    u64 b = mm & (mm - 1);
                    u64 bit = mm ^ b;
                    mm = b;
                    auto it = m1.find(big ^ bit);
                    if (it != m1.end()) cross01[L].push_back({it->second, s2});
                }
            }
            for (int s2 = 0; s2 < Q; s2++) {
                u64 big = imask1(s2, L + 1);
                u64 mm = big;
                while (mm) {
                    u64 b = mm & (mm - 1);
                    u64 bit = mm ^ b;
                    mm = b;
                    auto it = m2.find(big ^ bit);
                    if (it != m2.end()) cross10[L].push_back({it->second, s2});
                }
            }
        }
        // eq at the last length (Q-1): all co-singletons common — the DP
        // terminates at length Q-1 anyway; also eq at length Q-1 unused.
        // remove same-order duplicates from cross01/cross10: cross01 maps
        // order-1 states to order-2 states, never same-order, fine.
    }

    // returns true iff the union ACCEPTS word w
    bool accepts(u64 w) const {
        // per-order coloring in position space
        // order 1: pos = point; order 2: w2[i] = w[p[i]]
        u64 w2 = 0;
        for (int i = 0; i < Q; i++)
            if ((w >> p[i]) & 1) w2 |= 1ULL << i;
        // plus-count per start per length, computed incrementally
        static thread_local std::vector<int> pc1, pc2;
        pc1.assign(Q, 0);
        pc2.assign(Q, 0);
        u64 R1 = w, R2 = w2;   // length-1 reachable: plus singletons
        for (int s = 0; s < Q; s++) {
            pc1[s] = (w >> s) & 1;
            pc2[s] = (w2 >> s) & 1;
        }
        if (!(R1 | R2)) return false;
        for (int L = 1; L <= Q - 2; L++) {
            // sync at length L (common intervals)
            for (auto& pr : eq[L]) {
                bool a = (R1 >> pr.first) & 1, b = (R2 >> pr.second) & 1;
                if (a && !b) R2 |= 1ULL << pr.second;
                else if (b && !a) R1 |= 1ULL << pr.first;
            }
            // grow to length L+1
            u64 N1 = R1 | rotr1(R1);
            u64 N2 = R2 | rotr1(R2);
            for (auto& pr : cross01[L])
                if ((R1 >> pr.first) & 1) N2 |= 1ULL << pr.second;
            for (auto& pr : cross10[L])
                if ((R2 >> pr.first) & 1) N1 |= 1ULL << pr.second;
            // update plus counts to length L+1 and filter
            int Lp1 = L + 1;
            int lo = Lp1 / 2, target = (Lp1 + 1) / 2;
            u64 K1 = 0, K2 = 0;
            for (int s = 0; s < Q; s++) {
                int e1 = s + L;
                pc1[s] += (w >> (e1 >= Q ? e1 - Q : e1)) & 1;
                pc2[s] += (w2 >> (e1 >= Q ? e1 - Q : e1)) & 1;
                if (Lp1 & 1) {
                    if (pc1[s] == target) K1 |= 1ULL << s;
                    if (pc2[s] == target) K2 |= 1ULL << s;
                } else {
                    if (pc1[s] == lo || pc1[s] == lo + 1) K1 |= 1ULL << s;
                    if (pc2[s] == lo || pc2[s] == lo + 1) K2 |= 1ULL << s;
                }
            }
            R1 = N1 & K1;
            R2 = N2 & K2;
            if (!(R1 | R2)) return false;
        }
        return true;
    }
};

// ------------------------------------------------------------------- driver
int main(int argc, char** argv) {
    int n = 22;
    std::vector<int> perm;
    long long sample = 0;
    unsigned long long seed = 20260821ULL;
    bool listCross = false;
    std::string permdesc = "";
    for (int i = 1; i < argc; i++) {
        std::string a = argv[i];
        auto next = [&]() { return std::string(argv[++i]); };
        if (a == "--n") n = atoi(next().c_str());
        else if (a == "--sample") sample = atoll(next().c_str());
        else if (a == "--seed") seed = strtoull(next().c_str(), nullptr, 10);
        else if (a == "--list-cross") listCross = true;
        else if (a == "--transpose") permdesc = "T" + next();
        else if (a == "--swap") permdesc = "S" + next();
        else if (a == "--mult") permdesc = "M" + next();
        else if (a == "--randperm") permdesc = "R" + next();
        else if (a == "--perm") permdesc = "P" + next();
        else { fprintf(stderr, "unknown arg %s\n", a.c_str()); return 2; }
    }
    Q = n - 1;
    M = n / 2;
    FULLQ = (Q == 64) ? ~0ULL : ((1ULL << Q) - 1);
    perm.resize(Q);
    for (int i = 0; i < Q; i++) perm[i] = i;
    if (permdesc.empty()) { fprintf(stderr, "need a permutation\n"); return 2; }
    char kind = permdesc[0];
    std::string rest = permdesc.substr(1);
    if (kind == 'T') {
        int u, v;
        sscanf(rest.c_str(), "%d,%d", &u, &v);
        std::swap(perm[u], perm[v]);
    } else if (kind == 'S') {
        int a, b, len;
        sscanf(rest.c_str(), "%d,%d,%d", &a, &b, &len);
        for (int i = 0; i < len; i++)
            std::swap(perm[(a + i) % Q], perm[(b + i) % Q]);
    } else if (kind == 'M') {
        int a = atoi(rest.c_str());
        for (int i = 0; i < Q; i++) perm[i] = (int)((long long)a * i % Q);
        std::vector<char> seen(Q, 0);
        for (int i = 0; i < Q; i++) seen[perm[i]] = 1;
        for (int i = 0; i < Q; i++)
            if (!seen[i]) {
                fprintf(stderr, "multiplier %d not invertible mod %d\n", a, Q);
                return 2;
            }
    } else if (kind == 'R') {
        std::mt19937_64 rg(strtoull(rest.c_str(), nullptr, 10));
        for (int i = Q - 1; i > 0; i--) {
            int j = (int)(rg() % (i + 1));
            std::swap(perm[i], perm[j]);
        }
    } else if (kind == 'P') {
        int pos = 0;
        for (int i = 0; i < Q; i++) {
            perm[i] = atoi(rest.c_str() + pos);
            while (pos < (int)rest.size() && rest[pos] != ',') pos++;
            pos++;
        }
    }

    UnionDP dp;
    dp.init(perm);

    if (listCross) {
        printf("{\"n\": %d, \"perm\": \"%s\", \"cross\": [", n, permdesc.c_str());
        for (int L = 1; L <= Q - 2; L++)
            printf("%s[%d,%zu,%zu,%zu]", L > 1 ? "," : "", L,
                   dp.cross01[L].size(), dp.cross10[L].size(), dp.eq[L].size());
        printf("]}\n");
        return 0;
    }

    bool dumpCommon = getenv("CYCLE05_DUMP_COMMON") != nullptr;
    long long total = 0, rej1 = 0, rej2 = 0, commonrej = 0, rescued = 0,
              unionrej = 0;
    auto handle = [&](u64 w) {
        total++;
        bool r1 = single_rejects(w);
        if (r1) rej1++;
        u64 pull = 0;
        for (int x = 0; x < Q; x++)
            if ((w >> perm[x]) & 1) pull |= 1ULL << x;
        bool r2 = single_rejects(pull);
        if (r2) rej2++;
        if (r1 && r2) {
            commonrej++;
            bool acc = dp.accepts(w);
            if (acc) rescued++;
            else unionrej++;
            if (dumpCommon)
                fprintf(stderr, "COMMON %llx %d\n", (unsigned long long)w,
                        acc ? 1 : 0);
        }
    };

    if (sample > 0) {
        std::mt19937_64 rg(seed);
        for (long long i = 0; i < sample; i++) {
            // random q-bit word with m ones (Fisher-Yates on positions)
            int posn[64];
            for (int j = 0; j < Q; j++) posn[j] = j;
            u64 w = 0;
            for (int j = 0; j < M; j++) {
                int k = j + (int)(rg() % (Q - j));
                std::swap(posn[j], posn[k]);
                w |= 1ULL << posn[j];
            }
            handle(w);
        }
    } else {
        // exhaustive: Gosper over q-bit words of weight m
        u64 w = (1ULL << M) - 1;
        while (w <= FULLQ) {
            handle(w);
            u64 c = w & (~w + 1), r = w + c;
            w = (((r ^ w) >> 2) / c) | r;
        }
    }

    printf("{\"n\": %d, \"perm\": \"%s\", \"mode\": \"%s\", \"total\": %lld, "
           "\"rej1\": %lld, \"rej2\": %lld, \"commonrej\": %lld, "
           "\"rescued\": %lld, \"unionrej\": %lld}\n",
           n, permdesc.c_str(), sample > 0 ? "sample" : "exhaustive", total,
           rej1, rej2, commonrej, rescued, unionrej);
    return 0;
}

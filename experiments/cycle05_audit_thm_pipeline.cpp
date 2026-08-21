// Cycle 5 adversarial audit (SKEPTIC): independent implementation of the
// LITERAL union semantics (induced inclusion-by-one DAG over literal subset
// masks, built directly from the corrected RR_n definition), plus:
//   --scan  : exhaustive scan of a two-copy union at given n; counts
//             rej1/rej2/common/rescued with MY OWN literal DP; dumps
//             "COMMON <hex> <flag>" lines for differential comparison with
//             the proposer's engine; runs the Theorem-E minimax check
//             (min over plus roots of the minimax over maximal rooted
//             cyclic-interval chains of max |f|) on every rescued word.
//   --conj  : falsification search for Theorem A AS LITERALLY STATED:
//             samples pairs P = (pi, psi o pi) with psi affine (x -> a x),
//             which satisfy the stated hypothesis pi_2 o pi_1^{-1} = psi
//             affine, and looks for hybrid-only colorings (G(P) > 0).
//   --selftest : internal consistency + minimax reference check.
//
// Shares no code with the proposer's tools.  Build:
//   g++ -O2 -std=c++17 -o experiments/cycle05_audit_thm_pipeline.exe experiments/cycle05_audit_thm_pipeline.cpp
#include <cassert>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include <map>
#include <random>
#include <set>
#include <string>
#include <vector>

using namespace std;
typedef uint64_t u64;

// ------------------------------------------------------------ literal family
static vector<vector<u64>> rr_base(int n) {
    int q = n - 1;
    u64 inf = 1ULL << q;
    vector<vector<u64>> R(n + 1);
    R[0] = {0};
    for (int x = 0; x < q; x++) R[1].push_back(1ULL << x);
    for (int k = 2; k <= n - 1; k++) {
        int L = k - 1;
        for (int s = 0; s < q; s++) {
            u64 m = 0;
            for (int j = 0; j < L; j++) m |= 1ULL << ((s + j) % q);
            R[k].push_back(m | inf);
        }
    }
    R[n] = {(n == 64) ? ~0ULL : ((1ULL << n) - 1)};
    return R;
}

static u64 apply_perm(u64 mask, const vector<int>& pfin, int n) {
    int q = n - 1;
    u64 out = 0;
    for (int x = 0; x < q; x++)
        if ((mask >> x) & 1) out |= 1ULL << pfin[x];
    if ((mask >> q) & 1) out |= 1ULL << q;  // infinity fixed
    return out;
}

struct Family {
    int n, q;
    vector<vector<u64>> ranks;     // literal masks per rank (deduped, sorted)
    vector<vector<u64>> predmask;  // per rank k>=1, per cand: bitmask of rank-(k-1) subsets
};

static Family build_family(int n, const vector<vector<int>>& perms) {
    Family F;
    F.n = n;
    F.q = n - 1;
    auto base = rr_base(n);
    F.ranks.assign(n + 1, {});
    for (int k = 0; k <= n; k++) {
        set<u64> s;
        for (auto& p : perms)
            for (u64 m : base[k]) s.insert(apply_perm(m, p, n));
        F.ranks[k] = vector<u64>(s.begin(), s.end());
        assert((int)F.ranks[k].size() <= 63);
    }
    F.predmask.assign(n + 1, {});
    for (int k = 1; k <= n; k++) {
        F.predmask[k].assign(F.ranks[k].size(), 0);
        for (size_t i = 0; i < F.ranks[k].size(); i++) {
            u64 big = F.ranks[k][i];
            for (size_t j = 0; j < F.ranks[k - 1].size(); j++)
                if ((F.ranks[k - 1][j] & ~big) == 0)
                    F.predmask[k][i] |= 1ULL << j;
        }
    }
    return F;
}

// literal acceptance: chain empty=C_0 c C_1 c ... c C_n=U, |C_k|=k, every
// C_k in family, every |f(C_k)| <= 1.  w = plus mask over finite bits.
static bool accept(const Family& F, u64 w) {
    u64 reach = 1;  // rank 0: {empty}, f = 0
    for (int k = 1; k <= F.n; k++) {
        u64 nxt = 0;
        const auto& row = F.ranks[k];
        const auto& pm = F.predmask[k];
        for (size_t i = 0; i < row.size(); i++) {
            int f = 2 * __builtin_popcountll(row[i] & w) - k;
            if (f < -1 || f > 1) continue;
            if (reach & pm[i]) nxt |= 1ULL << i;
        }
        if (!nxt) return false;
        reach = nxt;
    }
    return true;
}

// ------------------------------------------------- Theorem E minimax check
// min over maximal chains of cyclic O*-intervals {r}=G_1 c ... c G_q=Z_q of
// max_i |f(G_i)|, then min over plus roots r.
static int chain_minimax_root(u64 w, int q, int r) {
    const int INF = 1 << 28;
    vector<int> pl(q), best(q, INF), nb(q), npl(q);
    for (int s = 0; s < q; s++) pl[s] = (w >> s) & 1;
    for (int s = 0; s < q; s++) best[s] = (s == r) ? 1 : INF;
    for (int L = 2; L <= q; L++) {
        for (int s = 0; s < q; s++) {
            int e = (s + L - 1) % q;
            npl[s] = pl[s] + ((w >> e) & 1);
            int inr = ((r - s + q) % q) < L;
            if (!inr) { nb[s] = INF; continue; }
            int pred = INF;
            if (((r - s + q) % q) < L - 1) pred = min(pred, best[s]);
            if (((r - (s + 1) + 2 * q) % q) < L - 1) pred = min(pred, best[(s + 1) % q]);
            int val = abs(2 * npl[s] - L);
            nb[s] = (pred >= INF) ? INF : max(val, pred);
        }
        best = nb;
        pl = npl;
    }
    int ans = INF;
    for (int s = 0; s < q; s++) ans = min(ans, best[s]);
    return ans;
}

static int minimax_word(u64 w, int q) {
    const int INF = 1 << 28;
    int ans = INF;
    for (int r = 0; r < q; r++)
        if ((w >> r) & 1) ans = min(ans, chain_minimax_root(w, q, r));
    return ans;
}

// reference (independent recursion with memo) for the minimax, small q only
static map<pair<int, int>, int> mm_memo;
static u64 mm_w;
static int mm_q, mm_r;
static int mm_val(int s, int L) {
    int v = 0;
    for (int k = 0; k < L; k++) v += (mm_w >> ((s + k) % mm_q)) & 1;
    return abs(2 * v - L);
}
static int mm_rec(int s, int L) {  // interval [s, s+L-1] containing r
    if (L == 1) return (s == mm_r) ? 1 : (1 << 28);
    auto it = mm_memo.find({s, L});
    if (it != mm_memo.end()) return it->second;
    int pred = 1 << 28;
    if (((mm_r - s + mm_q) % mm_q) < L - 1) pred = min(pred, mm_rec(s, L - 1));
    if (((mm_r - (s + 1) + 2 * mm_q) % mm_q) < L - 1)
        pred = min(pred, mm_rec((s + 1) % mm_q, L - 1));
    int res = (pred >= (1 << 28)) ? (1 << 28) : max(mm_val(s, L), pred);
    mm_memo[{s, L}] = res;
    return res;
}

// ------------------------------------------------------------------ helpers
static u64 next_gosper(u64 w) {
    u64 c = w & (~w + 1), r = w + c;
    return (((r ^ w) >> 2) / c) | r;
}

static vector<int> pairswap_perm(int q) {
    vector<int> p(q);
    for (int i = 0; i < q; i++) p[i] = i;
    for (int i = 0; i + 1 < q; i += 2) swap(p[i], p[i + 1]);
    return p;
}

static vector<int> mult_perm(int q, long long a, long long b) {
    vector<int> p(q);
    for (int i = 0; i < q; i++) p[i] = (int)((a * i + b) % q);
    vector<char> seen(q, 0);
    for (int i = 0; i < q; i++) seen[p[i]] = 1;
    for (int i = 0; i < q; i++)
        if (!seen[i]) { fprintf(stderr, "mult not invertible\n"); exit(2); }
    return p;
}

static u64 pull_word(u64 w, const vector<int>& tau, int q) {
    // (w o tau)(x) = w(tau(x))
    u64 out = 0;
    for (int x = 0; x < q; x++)
        if ((w >> tau[x]) & 1) out |= 1ULL << x;
    return out;
}

static u64 push_word(u64 w, const vector<int>& pi, int q) {
    // f = w o pi^{-1}: bit pi[x] of out = bit x of w
    u64 out = 0;
    for (int x = 0; x < q; x++)
        if ((w >> x) & 1) out |= 1ULL << pi[x];
    return out;
}

// ------------------------------------------------------------------- selftest
static void selftest() {
    // 1. single-copy family counts: total = q^2 + 2
    for (int n : {8, 10, 12}) {
        vector<vector<int>> perms;
        vector<int> ident(n - 1);
        for (int i = 0; i < n - 1; i++) ident[i] = i;
        perms.push_back(ident);
        Family F = build_family(n, perms);
        int tot = 0;
        for (auto& r : F.ranks) tot += (int)r.size();
        assert(tot == (n - 1) * (n - 1) + 2);
    }
    // 2. acceptance sanity at n=8: every word accepted by identity copy iff
    //    an explicit chain exists via naive DFS on masks (independent code path)
    {
        int n = 8, q = 7, m = 4;
        vector<int> ident(q);
        for (int i = 0; i < q; i++) ident[i] = i;
        Family F = build_family(n, {ident});
        u64 w = (1ULL << m) - 1;
        int cnt = 0;
        while (w < (1ULL << q)) {
            // DFS over subset masks
            vector<vector<u64>> reach(n + 1);
            reach[0].push_back(0);
            for (int k = 1; k <= n; k++) {
                for (u64 cand : F.ranks[k]) {
                    int f = 2 * __builtin_popcountll(cand & w) - k;
                    if (f < -1 || f > 1) continue;
                    bool ok = false;
                    for (u64 pv : reach[k - 1])
                        if ((pv & ~cand) == 0) { ok = true; break; }
                    if (ok) reach[k].push_back(cand);
                }
            }
            bool dfs = !reach[n].empty();
            bool fast = accept(F, w);
            assert(dfs == fast);
            cnt += fast;
            w = next_gosper(w);
        }
        printf("selftest n=8 identity accept count = %d of 35\n", cnt);
    }
    // 3. minimax DP vs memo recursion at q=9, random words
    {
        mt19937_64 rg(12345);
        int q = 9;
        for (int t = 0; t < 300; t++) {
            u64 w = 0;
            vector<int> pos(q);
            for (int i = 0; i < q; i++) pos[i] = i;
            for (int i = 0; i < 5; i++) {
                int j = i + rg() % (q - i);
                swap(pos[i], pos[j]);
                w |= 1ULL << pos[i];
            }
            for (int r = 0; r < q; r++) {
                if (!((w >> r) & 1)) continue;
                mm_memo.clear();
                mm_w = w; mm_q = q; mm_r = r;
                int a = mm_rec((r + 1) % q, q);  // any start at L=q gives Z_q...
                // reference answer: min over all starts at L = q
                int ref = 1 << 28;
                for (int s = 0; s < q; s++) ref = min(ref, mm_rec(s, q));
                int dp = chain_minimax_root(w, q, r);
                (void)a;
                assert(dp == ref);
            }
        }
        printf("selftest minimax DP == reference recursion (q=9, 300 words)\n");
    }
    printf("selftest PASS\n");
}

// ---------------------------------------------------------------------- scan
static void run_scan(int n, const string& spec, const string& dumpfile,
                     bool skip_minimax, const string& dumpall = "") {
    int q = n - 1, m = n / 2;
    vector<int> ident(q);
    for (int i = 0; i < q; i++) ident[i] = i;
    vector<int> p2;
    if (spec == "pairswap") p2 = pairswap_perm(q);
    else if (spec.rfind("mult:", 0) == 0) {
        long long a = 0, b = 0;
        sscanf(spec.c_str(), "mult:%lld:%lld", &a, &b);
        p2 = mult_perm(q, a, b);
        if (b != 0) {
            // verify the b-irrelevance claim: union family (id, mult a b)
            // literally equals union family (id, mult a 0)
            Family Ub = build_family(n, {ident, mult_perm(q, a, b)});
            Family U0 = build_family(n, {ident, mult_perm(q, a, 0)});
            bool same = true;
            for (int k = 0; k <= n; k++)
                if (Ub.ranks[k] != U0.ranks[k]) same = false;
            printf("b-irrelevance: union family (id,x->%lldx+%lld) == (id,x->%lldx): %s\n",
                   a, b, a, same ? "IDENTICAL" : "DIFFERENT");
        }
    } else { fprintf(stderr, "bad spec\n"); exit(2); }

    Family F1 = build_family(n, {ident});
    Family F2 = build_family(n, {p2});
    Family FU = build_family(n, {ident, p2});

    FILE* dump = nullptr;
    if (!dumpfile.empty()) dump = fopen(dumpfile.c_str(), "w");
    FILE* dall = nullptr;
    if (!dumpall.empty()) dall = fopen(dumpall.c_str(), "w");

    long long total = 0, rej1 = 0, rej2 = 0, common = 0, rescued = 0;
    vector<u64> rej1set, rescued_words;
    u64 w = (1ULL << m) - 1;
    u64 lim = (q == 64) ? ~0ULL : ((1ULL << q) - 1);
    while (w <= lim) {
        total++;
        bool a1 = accept(F1, w);
        bool a2 = accept(F2, w);
        if (!a1) { rej1++; if ((int)rej1set.size() < 100000) rej1set.push_back(w); }
        if (!a2) rej2++;
        if (!a1 && !a2) {
            common++;
            bool au = accept(FU, w);
            if (au) { rescued++; rescued_words.push_back(w); }
            if (dump) fprintf(dump, "COMMON %llx %d\n", (unsigned long long)w, au ? 1 : 0);
        }
        if (dall) {
            bool au2 = accept(FU, w);
            fprintf(dall, "W %llx %d %d %d\n", (unsigned long long)w,
                    a1 ? 1 : 0, a2 ? 1 : 0, au2 ? 1 : 0);
        }
        w = next_gosper(w);
    }
    if (dump) fclose(dump);
    if (dall) fclose(dall);
    printf("{\"audit_scan\": {\"n\": %d, \"copy2\": \"%s\", \"total\": %lld, "
           "\"rej1\": %lld, \"rej2\": %lld, \"common\": %lld, \"rescued\": %lld}}\n",
           n, spec.c_str(), total, rej1, rej2, common, rescued);

    if (n == 22) {
        // independent check: identity reject set == 21 rotations of 1^8 0^5 1^3 0^5
        u64 base = 0xFFULL | (0x7ULL << 13);
        set<u64> rots;
        u64 r = base;
        for (int i = 0; i < q; i++) {
            rots.insert(r);
            r = ((r << 1) | (r >> (q - 1))) & lim;
        }
        set<u64> mine(rej1set.begin(), rej1set.end());
        printf("n=22 identity reject set == 21 rotations of 1^8 0^5 1^3 0^5: %s "
               "(|mine| = %zu)\n", (mine == rots) ? "CONFIRMED" : "MISMATCH",
               mine.size());
    }

    if (!skip_minimax && !rescued_words.empty()) {
        int worst = -1;
        u64 worstw = 0;
        for (u64 rw : rescued_words) {
            int k = minimax_word(rw, q);
            if (k > worst) { worst = k; worstw = rw; }
        }
        printf("theoremE minimax over %zu rescued words: max over words of "
               "min over plus roots of chain-minimax = %d (bound 3d+4 = 10 for "
               "d = 2): %s  [worst word %llx]\n",
               rescued_words.size(), worst, worst <= 10 ? "WITHIN BOUND" : "VIOLATION",
               (unsigned long long)worstw);
        // per-word detail
        for (u64 rw : rescued_words) {
            printf("  rescued %llx  min-k = %d\n", (unsigned long long)rw,
                   minimax_word(rw, q));
        }
    }
}

// ---------------------------------------------------------------------- conj
static void run_conj(int n, long long a, unsigned long long seed, long long iters,
                     int maxfinds) {
    int q = n - 1, m = n / 2;
    vector<int> ident(q);
    for (int i = 0; i < q; i++) ident[i] = i;
    Family F1 = build_family(n, {ident});
    // identity reject set
    vector<u64> R;
    u64 w = (1ULL << m) - 1;
    u64 lim = (1ULL << q) - 1;
    while (w <= lim) {
        if (!accept(F1, w)) R.push_back(w);
        w = next_gosper(w);
    }
    set<u64> Rset(R.begin(), R.end());
    printf("conj mode n=%d a=%lld: identity reject set size %zu\n", n, a, R.size());

    mt19937_64 rg(seed);
    long long tried = 0, with_common = 0, common_words = 0;
    int finds = 0;
    for (long long it = 0; it < iters && finds < maxfinds; it++) {
        tried++;
        // random infinity-fixing pi
        vector<int> pi(q);
        for (int i = 0; i < q; i++) pi[i] = i;
        for (int i = q - 1; i > 0; i--) {
            int j = (int)(rg() % (u64)(i + 1));
            swap(pi[i], pi[j]);
        }
        vector<int> piinv(q);
        for (int i = 0; i < q; i++) piinv[pi[i]] = i;
        // tau = pi^{-1} o psi o pi, psi(x) = a x
        vector<int> tau(q);
        for (int x = 0; x < q; x++) tau[x] = piinv[(int)((a * pi[x]) % q)];
        // candidates: w in R with (w o tau) in R
        vector<u64> commons;
        for (u64 rw : R)
            if (Rset.count(pull_word(rw, tau, q))) commons.push_back(rw);
        if (commons.empty()) continue;
        with_common++;
        common_words += (long long)commons.size();
        Family FU = build_family(n, {ident, tau});
        for (u64 cw : commons) {
            if (!accept(FU, cw)) continue;
            // FOUND: hybrid-only coloring for the pair (id, tau).
            finds++;
            printf("\n=== THEOREM A LITERAL-HYPOTHESIS COUNTEREXAMPLE (find %d) ===\n", finds);
            printf("n = %d, q = %d, psi(x) = %lld x mod %d\n", n, q, a, q);
            printf("pi (copy 1 finite perm) = [");
            for (int i = 0; i < q; i++) printf("%d%s", pi[i], i + 1 < q ? "," : "");
            printf("]\n");
            printf("tau = pi^{-1} o psi o pi = [");
            for (int i = 0; i < q; i++) printf("%d%s", tau[i], i + 1 < q ? "," : "");
            printf("]\n");
            printf("word (for pair (id, tau)) w = %llx\n", (unsigned long long)cw);
            // Full independent verification on P = (pi, psi o pi):
            vector<int> p1 = pi, p2(q);
            for (int x = 0; x < q; x++) p2[x] = (int)((a * pi[x]) % q);
            // hypothesis check: p2 o p1^{-1} = psi
            bool hyp = true;
            for (int y = 0; y < q; y++)
                if (p2[piinv[y]] != (int)((a * y) % q)) hyp = false;
            printf("hypothesis pi_2 o pi_1^{-1} = psi affine: %s\n", hyp ? "HOLDS" : "BROKEN");
            u64 fword = push_word(cw, pi, q);  // f = w o pi^{-1}
            Family G1 = build_family(n, {p1});
            Family G2 = build_family(n, {p2});
            Family GU = build_family(n, {p1, p2});
            bool a1 = accept(G1, fword), a2 = accept(G2, fword), au = accept(GU, fword);
            printf("literal DP on P = (pi, psi.pi), coloring f = %llx:\n",
                   (unsigned long long)fword);
            printf("  copy pi(RR) accepts: %s\n", a1 ? "YES" : "no");
            printf("  copy psi.pi(RR) accepts: %s\n", a2 ? "YES" : "no");
            printf("  union accepts: %s\n", au ? "YES" : "no");
            printf("  => G(P) > 0 with stated hypothesis: %s\n",
                   (!a1 && !a2 && au) ? "CONFIRMED FALSIFICATION" : "verification FAILED");
        }
        if ((it + 1) % 5000 == 0)
            printf("  ... %lld iters, %lld with common rejects (%lld common words), %d finds\n",
                   it + 1, with_common, common_words, finds);
    }
    printf("conj done: tried %lld, with_common %lld, finds %d\n", tried, with_common, finds);
}

// ---------------------------------------------------------------------- main
int main(int argc, char** argv) {
    string mode, spec, dumpfile, dumpall;
    int n = 22;
    long long a = 2, iters = 20000;
    unsigned long long seed = 1;
    int maxfinds = 3;
    bool skip_minimax = false;
    for (int i = 1; i < argc; i++) {
        string s = argv[i];
        auto next = [&]() { return string(argv[++i]); };
        if (s == "--selftest") mode = "selftest";
        else if (s == "--scan") mode = "scan";
        else if (s == "--conj") mode = "conj";
        else if (s == "--n") n = atoi(next().c_str());
        else if (s == "--copy2") spec = next();
        else if (s == "--dump") dumpfile = next();
        else if (s == "--dump-all") dumpall = next();
        else if (s == "--a") a = atoll(next().c_str());
        else if (s == "--seed") seed = strtoull(next().c_str(), nullptr, 10);
        else if (s == "--iters") iters = atoll(next().c_str());
        else if (s == "--max-finds") maxfinds = atoi(next().c_str());
        else if (s == "--no-minimax") skip_minimax = true;
        else { fprintf(stderr, "unknown arg %s\n", s.c_str()); return 2; }
    }
    if (mode == "selftest") selftest();
    else if (mode == "scan") run_scan(n, spec, dumpfile, skip_minimax, dumpall);
    else if (mode == "conj") run_conj(n, a, seed, iters, maxfinds);
    else { fprintf(stderr, "need --selftest | --scan | --conj\n"); return 2; }
    return 0;
}

// Independent auditor engine (written from definitions only; no Cycle-5 code reuse).
// Semantics: research_cycle_05/hybrid_definitions.md sections 1-4, re-derived and
// cross-validated against the auditor's Python literal-DAG reference.
#include <cstdio>
#include <cstdint>
#include <array>
#include <cstring>
#include <cstdlib>
#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>
#include <algorithm>
#include <numeric>
using namespace std;
typedef unsigned long long u64;

static int Q, M; // q = n-1, m = n/2

// ---------- single-copy (identity circle) fast DP ----------
static bool single_accepts(u64 w) {
    // std cyclic intervals [s, s+L); reach bitmask over starts
    u64 full = (Q >= 64) ? ~0ULL : ((1ULL << Q) - 1);
    u64 reach = 0;
    static int cnt[64];
    for (int s = 0; s < Q; s++) { cnt[s] = (int)((w >> s) & 1); if (cnt[s] == 1) reach |= 1ULL << s; }
    if (!reach) return false;
    for (int L = 2; L < Q; L++) {
        u64 okm = 0;
        for (int s = 0; s < Q; s++) {
            int e = s + L - 1; if (e >= Q) e -= Q;
            cnt[s] += (int)((w >> e) & 1);
            int d = 2 * cnt[s] - L;
            bool ok = (L & 1) ? (d == 1) : (d == 0 || d == 2);
            if (ok) okm |= 1ULL << s;
        }
        u64 ext = reach | ((reach >> 1) | (reach << (Q - 1))) ;
        ext &= full;
        reach = ext & okm;
        if (!reach) return false;
    }
    return true;
}

// ---------- circles ----------
struct Circle {
    vector<int> pf;                       // position i holds pf[i]
    vector<vector<u64>> ints;             // ints[L]: q masks (L = 1..Q-1)
    vector<unordered_set<u64>> memb;      // memb[L]: set membership
    void build(const vector<int>& p) {
        pf = p;
        ints.assign(Q, {});
        memb.assign(Q, {});
        for (int s = 0; s < Q; s++) {
            u64 msk = 0;
            for (int L = 1; L < Q; L++) {
                msk |= 1ULL << pf[(s + L - 1) % Q];
                ints[L].push_back(msk);
                memb[L].insert(msk);
            }
        }
    }
};

static inline bool sum_ok(u64 mask, u64 w, int L) {
    int p = __builtin_popcountll(mask & w);
    int d = 2 * p - L;
    return (L & 1) ? (d == 1) : (d == 0 || d == 2);
}

// ---------- union walk DP (any t circles), set-level ----------
static bool union_accepts(u64 w, const vector<Circle*>& cs) {
    unordered_set<u64> cur, nxt, cand;
    for (auto c : cs) for (u64 msk : c->ints[1]) if (sum_ok(msk, w, 1)) cur.insert(msk);
    if (cur.empty()) return false;
    for (int L = 1; L < Q - 1; L++) {
        cand.clear();
        for (auto c : cs) for (u64 msk : c->ints[L + 1]) cand.insert(msk);
        nxt.clear();
        for (u64 T : cand) {
            if (!sum_ok(T, w, L + 1)) continue;
            u64 mm = T;
            while (mm) {
                u64 b = mm & (~mm + 1);
                if (cur.count(T ^ b)) { nxt.insert(T); break; }
                mm ^= b;
            }
        }
        swap(cur, nxt);
        if (cur.empty()) return false;
    }
    return true;
}

// ---------- exact min switches over accepting chains, t = 2 ----------
static int min_switches2(u64 w, Circle& c1, Circle& c2) {
    // dp[mask] = pair (cost with label 1, cost with label 2); INF = 1e9
    const int INF = 1000000000;
    unordered_map<u64, pair<int,int>> cur, nxt;
    for (auto c : {&c1, &c2}) {
        for (u64 msk : c->ints[1]) if (sum_ok(msk, w, 1)) cur[msk] = {0, 0}; // singletons in both
    }
    if (cur.empty()) return -1;
    for (int L = 1; L < Q - 1; L++) {
        nxt.clear();
        unordered_set<u64> cand;
        cand.insert(c1.ints[L + 1].begin(), c1.ints[L + 1].end());
        cand.insert(c2.ints[L + 1].begin(), c2.ints[L + 1].end());
        for (u64 T : cand) {
            if (!sum_ok(T, w, L + 1)) continue;
            bool in1 = c1.memb[L + 1].count(T) > 0, in2 = c2.memb[L + 1].count(T) > 0;
            int best1 = INF, best2 = INF;
            u64 mm = T;
            while (mm) {
                u64 b = mm & (~mm + 1); mm ^= b;
                auto it = cur.find(T ^ b);
                if (it == cur.end()) continue;
                int p1 = it->second.first, p2 = it->second.second;
                if (in1) best1 = min(best1, min(p1, p2 == INF ? INF : p2 + 1));
                if (in2) best2 = min(best2, min(p2, p1 == INF ? INF : p1 + 1));
            }
            if (best1 < INF || best2 < INF) nxt[T] = {best1, best2};
        }
        swap(cur, nxt);
        if (cur.empty()) return -1;
    }
    int best = INF;
    for (auto& kv : cur) best = min(best, min(kv.second.first, kv.second.second));
    return best >= INF ? -1 : best;
}

// ---------- helpers ----------
static u64 compose_word(u64 w, const vector<int>& perm) {
    // (w o perm)(x) = w(perm[x])
    u64 r = 0;
    for (int x = 0; x < Q; x++) if ((w >> perm[x]) & 1) r |= 1ULL << x;
    return r;
}
static vector<int> inverse(const vector<int>& p) {
    vector<int> inv(Q);
    for (int i = 0; i < Q; i++) inv[p[i]] = i;
    return inv;
}
static vector<u64> load_words(const char* path) {
    vector<u64> R;
    FILE* f = fopen(path, "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", path); exit(1); }
    char buf[128];
    while (fgets(buf, sizeof buf, f)) { if (buf[0] == '\n') continue; R.push_back(strtoull(buf, nullptr, 10)); }
    fclose(f);
    return R;
}
static vector<int> parse_perm_spec(const string& spec) {
    vector<int> p(Q); iota(p.begin(), p.end(), 0);
    if (spec[0] == 'T') { int i, j; sscanf(spec.c_str(), "T%d,%d", &i, &j); swap(p[i], p[j]); }
    else if (spec == "pairswap")  { for (int i = 0; i + 1 < Q; i += 2) swap(p[i], p[i + 1]); }
    else if (spec == "pairswap1") { for (int i = 1; i + 1 < Q; i += 2) swap(p[i], p[i + 1]); }
    else if (spec[0] == 'A') { int a, b; sscanf(spec.c_str(), "A%d,%d", &a, &b);
        for (int x = 0; x < Q; x++) p[x] = (a * x + b) % Q; }
    else if (spec[0] == 'p' && spec[1] == ':') {
        const char* s = spec.c_str() + 2;
        for (int i = 0; i < Q; i++) { p[i] = atoi(s); while (*s && *s != ',') s++; if (*s) s++; }
    } else { fprintf(stderr, "bad perm spec\n"); exit(1); }
    return p;
}

int main(int argc, char** argv) {
    if (argc < 3) { fprintf(stderr, "usage: audit_engine <mode> <n> ...\n"); return 1; }
    string mode = argv[1];
    int n = atoi(argv[2]);
    Q = n - 1; M = n / 2;

    if (mode == "rejects") {
        // enumerate all C(Q,M) words via Gosper, output rejected ones
        const char* out = argv[3];
        FILE* f = fopen(out, "w");
        u64 w = (1ULL << M) - 1, last = w << (Q - M);
        u64 total = 0, rej = 0;
        for (;;) {
            total++;
            if (!single_accepts(w)) { rej++; fprintf(f, "%llu\n", w); }
            if (w == last) break;
            u64 c = w & (~w + 1), r = w + c;
            w = (((r ^ w) >> 2) / c) | r;
        }
        fclose(f);
        printf("n=%d total=%llu rejects=%llu\n", n, total, rej);
    }
    else if (mode == "affine") {
        // exhaustive attack on repaired Theorem A: all (a,b), a unit not +-1
        vector<u64> R = load_words(argv[3]);
        unordered_set<u64> RS(R.begin(), R.end());
        Circle cid; { vector<int> id(Q); iota(id.begin(), id.end(), 0); cid.build(id); }
        long long maps = 0, cands = 0, ces = 0;
        for (int a = 2; a <= Q - 2; a++) {
            if (__gcd(a, Q) != 1) continue;
            for (int b = 0; b < Q; b++) {
                vector<int> p(Q);
                for (int x = 0; x < Q; x++) p[x] = (a * x + b) % Q;
                maps++;
                vector<int> pinv = inverse(p);
                Circle c2; bool built = false;
                for (u64 r : R) {
                    u64 wcand = compose_word(r, pinv);  // words w with w o p = r in R
                    if (!RS.count(wcand)) continue;     // need w itself rejected by copy 1
                    cands++;
                    if (!built) { c2.build(p); built = true; }
                    vector<Circle*> cs = {&cid, &c2};
                    if (union_accepts(wcand, cs)) {
                        ces++;
                        printf("COUNTEREXAMPLE n=%d a=%d b=%d w=%llu\n", n, a, b, wcand);
                    }
                }
            }
        }
        printf("n=%d affine maps=%lld common-reject candidates=%lld counterexamples=%lld\n",
               n, maps, cands, ces);
    }
    else if (mode == "scan") {
        // exhaustive union scan row for one copy-2 perm: needs reject file
        vector<u64> R = load_words(argv[3]);
        unordered_set<u64> RS(R.begin(), R.end());
        vector<int> p = parse_perm_spec(argv[4]);
        vector<int> pinv = inverse(p);
        Circle cid; { vector<int> id(Q); iota(id.begin(), id.end(), 0); cid.build(id); }
        Circle c2; c2.build(p);
        long long common = 0, unionrej = 0, rescued = 0;
        vector<u64> resc;
        for (u64 r : R) {
            u64 w = compose_word(r, pinv);
            if (!RS.count(w)) continue;
            common++;
            vector<Circle*> cs = {&cid, &c2};
            if (union_accepts(w, cs)) { rescued++; resc.push_back(w); }
            else unionrej++;
        }
        printf("n=%d perm=%s rej1=%zu rej2=%zu commonrej=%lld rescued=%lld unionrej=%lld\n",
               n, argv[4], R.size(), R.size(), common, rescued, unionrej);
        if ((long long)resc.size() <= 40) { for (u64 w : resc) printf("rescued %llu\n", w); }
    }
    else if (mode == "certs") {
        // verify certificate lines: "<q perm ints comma-sep> <word-decimal> <minsw>"
        vector<u64> R = load_words(argv[3]);
        unordered_set<u64> RS(R.begin(), R.end());
        Circle cid; { vector<int> id(Q); iota(id.begin(), id.end(), 0); cid.build(id); }
        FILE* f = fopen(argv[4], "r");
        if (!f) { fprintf(stderr, "no certfile\n"); return 1; }
        char line[4096];
        long long nl = 0, ok = 0, bad = 0;
        unordered_map<string, Circle> cache;
        while (fgets(line, sizeof line, f)) {
            if (line[0] == '\n') continue;
            nl++;
            char permcsv[2048]; u64 w; int msw;
            if (sscanf(line, "%s %llu %d", permcsv, &w, &msw) != 3) { fprintf(stderr, "parse err line %lld\n", nl); return 1; }
            string key(permcsv);
            auto it = cache.find(key);
            if (it == cache.end()) {
                vector<int> p(Q); const char* s = permcsv;
                for (int i = 0; i < Q; i++) { p[i] = atoi(s); while (*s && *s != ',') s++; if (*s) s++; }
                it = cache.emplace(key, Circle()).first;
                it->second.build(p);
            }
            Circle& c2 = it->second;
            bool r1 = !RS.count(w) ? false : true;                 // copy1 rejects w?
            u64 w2 = compose_word(w, c2.pf);
            bool r2 = RS.count(w2) ? true : false;                 // copy2 rejects w?
            vector<Circle*> cs = {&cid, &c2};
            bool ua = union_accepts(w, cs);
            int ms = min_switches2(w, cid, c2);
            bool good = r1 && r2 && ua && (ms == msw);
            if (good) ok++;
            else { bad++; printf("BADCERT line=%lld w=%llu r1=%d r2=%d ua=%d ms=%d claimed=%d\n", nl, w, r1, r2, ua, ms, msw); }
        }
        fclose(f);
        printf("certs n=%d lines=%lld ok=%lld bad=%lld\n", n, nl, ok, bad);
    }
    else if (mode == "triple") {
        // reproduce triple probe: copies id, pairswap, pairswap1; count over common rejects
        vector<u64> R = load_words(argv[3]);
        unordered_set<u64> RS(R.begin(), R.end());
        Circle cid; { vector<int> id(Q); iota(id.begin(), id.end(), 0); cid.build(id); }
        vector<int> p2 = parse_perm_spec("pairswap"), p3 = parse_perm_spec("pairswap1");
        Circle c2; c2.build(p2); Circle c3; c3.build(p3);
        vector<int> p2i = inverse(p2), p3i = inverse(p3);
        unordered_set<u64> R2, R3;
        for (u64 r : R) { R2.insert(compose_word(r, p2i)); R3.insert(compose_word(r, p3i)); }
        long long pc = 0, prsc = 0, tc = 0, trsc = 0, turj = 0, prsc_on_tc = 0;
        for (u64 w : R) {
            bool c2r = R2.count(w) > 0, c3r = R3.count(w) > 0;
            vector<Circle*> pair = {&cid, &c2};
            if (c2r) {
                pc++;
                bool pr = union_accepts(w, pair);
                if (pr) prsc++;
                if (c3r) {
                    tc++;
                    if (pr) prsc_on_tc++;
                    vector<Circle*> tri = {&cid, &c2, &c3};
                    if (union_accepts(w, tri)) trsc++;
                    else { turj++; printf("triple-union-reject w=%llu\n", w); }
                }
            }
        }
        printf("triple n=%d pair_common=%lld pair_rescued=%lld triple_common=%lld pair_rescued_on_tc=%lld triple_rescued=%lld triple_unionrej=%lld\n",
               n, pc, prsc, tc, prsc_on_tc, trsc, turj);
    }
    else if (mode == "dmid") {
        // coloring-free exact middle switch depth for pair (id, spec)
        vector<int> p = parse_perm_spec(argv[3]);
        Circle c1; { vector<int> id(Q); iota(id.begin(), id.end(), 0); c1.build(id); }
        Circle c2; c2.build(p);
        // dp[mask] -> best[3]: last-single-label 0(none),1,2
        unordered_map<u64, array<int,3>> cur, nxt;
        for (u64 msk : c1.ints[1]) cur[msk] = {0, -1, -1};
        for (int L = 1; L < Q - 1; L++) {
            nxt.clear();
            unordered_set<u64> cand;
            cand.insert(c1.ints[L + 1].begin(), c1.ints[L + 1].end());
            cand.insert(c2.ints[L + 1].begin(), c2.ints[L + 1].end());
            for (u64 T : cand) {
                bool in1 = c1.memb[L + 1].count(T) > 0, in2 = c2.memb[L + 1].count(T) > 0;
                int lab = (in1 && in2) ? 0 : (in1 ? 1 : 2);      // 0 = common
                bool mid = (L + 1 >= 3 && L + 1 <= Q - 3);
                array<int,3> best = {-1, -1, -1};
                u64 mm = T;
                while (mm) {
                    u64 b = mm & (~mm + 1); mm ^= b;
                    auto it = cur.find(T ^ b);
                    if (it == cur.end()) continue;
                    for (int last = 0; last < 3; last++) {
                        int v = it->second[last];
                        if (v < 0) continue;
                        int nl = last, add = 0;
                        if (mid && lab != 0) {
                            if (last != 0 && last != lab) add = 1;
                            nl = lab;
                        }
                        if (v + add > best[nl]) best[nl] = v + add;
                    }
                }
                if (best[0] >= 0 || best[1] >= 0 || best[2] >= 0) nxt[T] = best;
            }
            swap(cur, nxt);
        }
        int ans = -1;
        for (auto& kv : cur) for (int l = 0; l < 3; l++) ans = max(ans, kv.second[l]);
        printf("dmid q=%d perm=%s D_mid=%d\n", Q, argv[3], ans);
    }
    else if (mode == "kmin") {
        // for each rescued word of pair (id, spec): min over plus-rooted std-interval
        // maximal walks of max |f(G_i)|  (Theorem E pipeline check, k0 bound 3d+4)
        vector<u64> R = load_words(argv[3]);
        unordered_set<u64> RS(R.begin(), R.end());
        vector<int> p = parse_perm_spec(argv[4]);
        vector<int> pinv = inverse(p);
        Circle cid; { vector<int> id(Q); iota(id.begin(), id.end(), 0); cid.build(id); }
        Circle c2; c2.build(p);
        unordered_map<int, long long> dist;
        long long rescued = 0;
        int worst = -1;
        for (u64 r : R) {
            u64 w = compose_word(r, pinv);
            if (!RS.count(w)) continue;
            vector<Circle*> cs = {&cid, &c2};
            if (!union_accepts(w, cs)) continue;
            rescued++;
            // DP over std cyclic intervals [s, s+L): val = min over walks of max |f|
            const int INF = 1000000000;
            vector<int> dp(Q, INF), nd(Q);
            for (int s = 0; s < Q; s++) dp[s] = ((w >> s) & 1) ? 1 : INF;  // plus root
            vector<int> cnt(Q);
            for (int s = 0; s < Q; s++) cnt[s] = (int)((w >> s) & 1);
            for (int L = 2; L <= Q; L++) {
                for (int s = 0; s < Q; s++) {
                    int e = s + L - 1; if (e >= Q) e -= Q;
                    cnt[s] += (int)((w >> e) & 1);
                    int d = abs(2 * cnt[s] - L);
                    int fromR = dp[s];                    // extend right
                    int fromL = dp[(s + 1) % Q];         // extend left
                    int bestp = min(fromR, fromL);
                    nd[s] = bestp >= INF ? INF : max(bestp, d);
                }
                dp = nd;
            }
            int v = *min_element(dp.begin(), dp.end());   // size-Q set is unique; take best route
            dist[v]++;
            worst = max(worst, v);
        }
        printf("kmin n=%d perm=%s rescued=%lld worst_k=%d\n", n, argv[4], rescued, worst);
        for (auto& kv : dist) printf("  k=%d count=%lld\n", kv.first, kv.second);
    }
    else { fprintf(stderr, "unknown mode\n"); return 1; }
    return 0;
}

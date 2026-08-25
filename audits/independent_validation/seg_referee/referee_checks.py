# Arms-length referee checks for Lemma SEG (Theorem S of
# audits/cycle05_seg_deep_independent_validation.md).
# Written 2026-08-25 from the definitions and the FLSY primary source only.
# NO code, constants, or seeds reused from any prior repository engine
# (experiments/cycle05_audit_seg_mc.py, audits/independent_validation/my_seg_mc.py,
# audits/independent_validation/seg_deep/* were not opened).
# Seed family: 250825xxx (fresh).
import numpy as np, math, itertools, json, sys, time
from math import comb, sqrt, exp, lgamma, log

T0 = time.time()
OUT = {}
def report(key, val):
    OUT[key] = val
    print(f"[{time.time()-T0:7.1f}s] {key}: {val}", flush=True)

# =====================================================================
# Check W1: first-passage law, reflection identity, constants c_lo, c_hi
# =====================================================================
def fp_law_dp(delta, ymax):
    """Exact DP for Pr[F_delta = y] (absorbing barrier at +delta), float."""
    lo = -(ymax + 2)
    size = delta - lo  # positions lo .. delta-1
    v = np.zeros(size); v[0 - lo] = 1.0
    out = np.zeros(ymax + 1)
    for y in range(1, ymax + 1):
        nv = np.zeros(size)
        nv[1:] += 0.5 * v[:-1]
        nv[:-1] += 0.5 * v[1:]
        # mass stepping from delta-1 up to delta is absorbed:
        out[y] = 0.5 * v[size - 1]
        nv[size - 1] = 0.5 * v[size - 2]  # only from delta-2
        v = nv
    return out

def fp_law_formula(delta, y):
    if (y - delta) % 2 != 0 or y < delta:
        return 0.0
    return delta / y * comb(y, (y + delta) // 2) / 2.0**y

def log_binom_prob(m, x):
    """log Pr[g(m) = x] for simple walk, float via lgamma."""
    if (m + x) % 2 != 0 or abs(x) > m:
        return -math.inf
    a = (m + x) // 2
    return lgamma(m + 1) - lgamma(a + 1) - lgamma(m - a + 1) - m * log(2.0)

def fp_tail_reflection(delta, z):
    """Pr[F_delta >= z] = Pr[-delta < g(z-1) < delta] + Pr[g(z-1) = -delta]."""
    m = z - 1
    s = 0.0
    for x in range(-delta + 1, delta):
        lp = log_binom_prob(m, x)
        if lp > -math.inf:
            s += exp(lp)
    lp = log_binom_prob(m, -delta)
    if lp > -math.inf:
        s += exp(lp)
    return s

def check_w1():
    # (a) DP law == closed formula
    worst = 0.0
    for delta in (1, 2, 3, 5):
        dp = fp_law_dp(delta, 401)
        for y in range(1, 402):
            f = fp_law_formula(delta, y)
            worst = max(worst, abs(dp[y] - f))
    report("W1.law_dp_vs_formula_maxabs", f"{worst:.2e}")
    # (b) reflection identity == direct tail sum (small z)
    worst = 0.0
    for delta in (1, 2, 3):
        dp = fp_law_dp(delta, 300)
        for z in range(1, 300):
            tail_direct = 1.0 - dp[:z].sum()
            tail_refl = fp_tail_reflection(delta, z)
            worst = max(worst, abs(tail_direct - tail_refl))
    report("W1.reflection_identity_maxabs", f"{worst:.2e}")
    # (c) constants scan on integer z >= 4 delta^2
    ratios = []
    for delta in range(1, 9):
        zs = list(range(4 * delta * delta, 4 * delta * delta + 400))
        z = 4 * delta * delta
        while z < 200000:
            z = int(z * 1.15) + 1
            zs.append(z)
        for z in zs:
            t = fp_tail_reflection(delta, z)
            ratios.append(t * sqrt(z) / delta)
    report("W1.ratio_min_max_int_z", (round(min(ratios), 4), round(max(ratios), 4)))
    report("W1.constants_ok_int", bool(min(ratios) >= 1/6 and max(ratios) <= 4))
    # (d) real-z extension used by W3's t*: Pr[F>=z] >= (1/6) delta/sqrt(z)
    # for REAL z >= 4 delta^2  <=>  tail(ceil(z)) * sqrt(z) / delta >= 1/6;
    # worst case z -> u from below: tail(u) * sqrt(u-1) / delta.
    real_ratios = []
    for delta in range(1, 9):
        zs = list(range(4 * delta * delta + 1, 4 * delta * delta + 400))
        z = 4 * delta * delta
        while z < 200000:
            z = int(z * 1.15) + 1
            zs.append(z)
        for u in zs:
            t = fp_tail_reflection(delta, u)
            real_ratios.append(t * sqrt(u - 1) / delta)
    report("W1.ratio_min_real_z", round(min(real_ratios), 4))
    report("W1.constants_ok_real", bool(min(real_ratios) >= 1/6))

# =====================================================================
# Check W2 mechanism: Pr[D_Delta > c3*Delta^3] <= 2^-Delta (exact DP)
# =====================================================================
def check_w2():
    for Delta in (4, 6):
        T = 256 * Delta**3
        # band DP: positions -(Delta-1)..(Delta-1), exit prob at |.|=Delta
        size = 2 * Delta - 1
        v = np.zeros(size); v[Delta - 1] = 1.0
        for _ in range(T):
            nv = np.zeros(size)
            nv[1:] += 0.5 * v[:-1]
            nv[:-1] += 0.5 * v[1:]
            v = nv
        surv = v.sum()
        report(f"W2.P[D>{256}*{Delta}^3]_vs_2^-{Delta}",
               f"{surv:.3e} <= {2.0**-Delta:.3e}: {bool(surv <= 2.0**-Delta)}")

# =====================================================================
# Check S2: 3*sqrt(N)*Pr[g([N])=sigma] >= 1 for |sigma|<=1, sigma=N mod 2
# =====================================================================
def check_s2():
    worst = math.inf
    for N in range(1, 401):
        sigma = N % 2  # representative; sigma=-1 symmetric
        p = comb(N, (N + sigma) // 2) / 2.0**N
        worst = min(worst, 3 * sqrt(N) * p)
    report("S2.min_3sqrtN_times_prob", round(worst, 4))
    report("S2.ok", bool(worst >= 1.0))

# =====================================================================
# Check S1: literal chain BFS (bitmask, definition-only) vs grid DP,
# linear + native cyclic + cyclic cut + B = Z_N terminal-split union.
# =====================================================================
def popcount(x): return x.bit_count()

def is_interval_mask(mask, N, cyclic):
    pc = popcount(mask)
    if pc == 0 or pc == N:
        return True
    if cyclic:
        rot = ((mask >> 1) | ((mask & 1) << (N - 1)))
        adj = popcount(mask & rot)
    else:
        adj = popcount(mask & (mask >> 1))
    return adj == pc - 1

def bfs_event(f, N, A_mask, B_mask, k, cyclic):
    """Literal nested-interval-chain existence, A -> B, one point per step,
    every set an interval (linear or cyclic) with |f(.)| <= k.
    Tries EVERY candidate point (no endpoint assumption)."""
    fA = sum(f[i] for i in range(N) if (A_mask >> i) & 1)
    if abs(fA) > k or not is_interval_mask(A_mask, N, cyclic):
        return False
    frontier = {A_mask: fA}
    L = popcount(B_mask) - popcount(A_mask)
    for _ in range(L):
        nxt = {}
        for mask, s in frontier.items():
            cand = B_mask & ~mask
            while cand:
                b = cand & (-cand)
                cand ^= b
                y = b.bit_length() - 1
                T = mask | b
                if T in nxt:
                    continue
                s2 = s + f[y]
                if abs(s2) <= k and is_interval_mask(T, N, cyclic):
                    nxt[T] = s2
        frontier = nxt
        if not frontier:
            return False
    return B_mask in frontier

def grid_event(vals, k, p, m):
    """Scalar grid DP. vals[j][i] = f(D_{j,i}); reach corner (p,m)."""
    reach_prev = None
    for j in range(p + 1):
        allowed = [abs(vals[j][i]) <= k for i in range(m + 1)]
        row = [False] * (m + 1)
        for i in range(m + 1):
            if not allowed[i]:
                continue
            if j == 0 and i == 0:
                row[i] = True
            else:
                down = reach_prev[i] if j > 0 else False
                left = row[i - 1] if i > 0 else False
                row[i] = down or left
        reach_prev = row
    return reach_prev[m]

def seg_grid_linear(f, N, a1, a2, p, m, k):
    """Linear S1 normal form: A=[a1,a2], B=[a1-p, a2+m]."""
    fA = sum(f[a1:a2 + 1])
    lam = [0] * (p + 1)
    for j in range(1, p + 1):
        lam[j] = lam[j - 1] + f[a1 - j]
    rho = [0] * (m + 1)
    for i in range(1, m + 1):
        rho[i] = rho[i - 1] + f[a2 + i]
    vals = [[fA + lam[j] + rho[i] for i in range(m + 1)] for j in range(p + 1)]
    return grid_event(vals, k, p, m)

def seg_grid_cyclic(f, N, a1, sizeA, p, m, k):
    """Cyclic S1: A = {a1..a1+sizeA-1 mod N}, left ext p, right ext m."""
    idx = lambda x: x % N
    fA = sum(f[idx(a1 + t)] for t in range(sizeA))
    lam = [0] * (p + 1)
    for j in range(1, p + 1):
        lam[j] = lam[j - 1] + f[idx(a1 - j)]
    rho = [0] * (m + 1)
    for i in range(1, m + 1):
        rho[i] = rho[i - 1] + f[idx(a1 + sizeA - 1 + i)]
    vals = [[fA + lam[j] + rho[i] for i in range(m + 1)] for j in range(p + 1)]
    return grid_event(vals, k, p, m)

def mask_of(points, N):
    msk = 0
    for x in points:
        msk |= 1 << (x % N)
    return msk

def enum_colorings(N, sigma):
    """All f: [N] -> {+-1} with f([N]) = sigma."""
    npos = (N + sigma) // 2
    for pos in itertools.combinations(range(N), npos):
        f = [-1] * N
        for i in pos:
            f[i] = 1
        yield f

def check_s1_linear():
    N, sigma = 10, 0
    mism = 0; total = 0
    configs = []
    for a1 in range(N):
        for sizeA in (1, 2, 3):
            a2 = a1 + sizeA - 1
            if a2 >= N: continue
            for p in range(0, min(4, a1) + 1):
                for m in range(0, min(4, N - 1 - a2) + 1):
                    if p + m >= 1:
                        configs.append((a1, a2, p, m))
    colorings = list(enum_colorings(N, sigma))
    for f in colorings:
        for (a1, a2, p, m) in configs:
            A = mask_of(range(a1, a2 + 1), N)
            B = mask_of(range(a1 - p, a2 + m + 1), N)
            e1 = bfs_event(f, N, A, B, 1, cyclic=False)
            e2 = seg_grid_linear(f, N, a1, a2, p, m, 1)
            total += 1
            if e1 != e2: mism += 1
    report("S1.linear_N10_checks", total)
    report("S1.linear_N10_mismatches", mism)

def check_s1_cyclic():
    results = {}
    for (N, sigma, nconf) in ((12, 0, 14), (13, 1, 14), (14, 0, 6)):
        # config list: (a1, sizeA, p, m) cyclic, B proper
        rng = np.random.default_rng(250825101 + N)
        configs = []
        base = [(0, 1, 3, 4), (0, 1, 7, 0), (0, 1, 0, 7),
                (N - 1, 3, 2, 3),          # A wraps the seam
                (5, 2, 4, 4), (2, 1, 5, 3)]
        for c in base[:nconf]:
            a1, sA, p, m = c
            if sA + p + m < N:            # B proper
                configs.append(c)
        # translated copies for exact translation invariance
        shifted = [(a1 + 3, sA, p, m) for (a1, sA, p, m) in configs]
        mism = 0; total = 0
        counts = {}; counts_sh = {}
        for f in enum_colorings(N, sigma):
            for ci, (a1, sA, p, m) in enumerate(configs):
                A = mask_of(range(a1, a1 + sA), N)
                B = mask_of(range(a1 - p, a1 + sA + m), N)
                for k in (1, 2):
                    e1 = bfs_event(f, N, A, B, k, cyclic=True)
                    e2 = seg_grid_cyclic(f, N, a1, sA, p, m, k)
                    total += 1
                    if e1 != e2: mism += 1
                    if e1: counts[(ci, k)] = counts.get((ci, k), 0) + 1
            for ci, (a1, sA, p, m) in enumerate(shifted):
                A = mask_of(range(a1, a1 + sA), N)
                B = mask_of(range(a1 - p, a1 + sA + m), N)
                for k in (1, 2):
                    if bfs_event(f, N, A, B, k, cyclic=True):
                        counts_sh[(ci, k)] = counts_sh.get((ci, k), 0) + 1
        trans_ok = counts == counts_sh
        results[f"N{N}s{sigma}"] = (total, mism, trans_ok)
        report(f"S1.cyclic_N{N}_sigma{sigma}", f"checks={total} mismatches={mism} translation_exact={trans_ok}")
    return results

def check_s1_fullB():
    """B = Z_N: literal BFS to the full set vs union over terminal splits."""
    mism = 0; total = 0
    for (N, sigma) in ((11, 1), (12, 0)):
        for (a1, sA) in ((0, 3), (4, 2), (N - 1, 2)):
            L = N - sA
            for f in enum_colorings(N, sigma):
                for k in (1, 2):
                    A = mask_of(range(a1, a1 + sA), N)
                    B = (1 << N) - 1
                    e1 = bfs_event(f, N, A, B, k, cyclic=True)
                    e2 = False
                    if abs(sigma) <= k:
                        for u in range(L):      # u + v = L - 1
                            v = L - 1 - u
                            if seg_grid_cyclic(f, N, a1, sA, u, v, k):
                                e2 = True
                                break
                    total += 1
                    if e1 != e2: mism += 1
    report("S1.fullB_checks", total)
    report("S1.fullB_mismatches", mism)

def check_s1_cutpoints():
    """Cyclic B != Z_N: two different cut points give identical events
    (and equal the native cyclic BFS) - checked implicitly by
    check_s1_cyclic since seg_grid_cyclic is cut-free; here verify
    explicit cut-relabeling at two cut points vs native BFS."""
    N, sigma = 12, 0
    a1, sA, p, m = 3, 2, 3, 4      # B = {0..8}, complement {9,10,11}
    mism = 0; total = 0
    for f in enum_colorings(N, sigma):
        A = mask_of(range(a1, a1 + sA), N)
        B = mask_of(range(a1 - p, a1 + sA + m), N)
        e_native = bfs_event(f, N, A, B, 1, cyclic=True)
        for c in (9, 11):          # two cut points in the complement
            g = [f[(c + 1 + t) % N] for t in range(N)]   # cut order
            na1 = (a1 - (c + 1)) % N
            e_cut = seg_grid_linear(g, N, na1, na1 + sA - 1, p, m, 1)
            total += 1
            if e_cut != e_native: mism += 1
    report("S1.cutpoint_checks", total)
    report("S1.cutpoint_mismatches", mism)

# =====================================================================
# Walk-level battery: vectorized grid-reachability DP (self-tested)
# =====================================================================
def dp_batch(k, p, m, off, lam, rho):
    """Vectorized reachability of corner (p,m). lam:(b,p), rho:(b,m)."""
    b = lam.shape[0]
    Lam = np.concatenate([np.zeros((b, 1), np.int64), np.cumsum(lam, axis=1)], axis=1)
    Rho = np.concatenate([np.zeros((b, 1), np.int64), np.cumsum(rho, axis=1)], axis=1)
    reach = None
    for j in range(p + 1):
        val = off + Lam[:, j][:, None] + Rho
        allowed = np.abs(val) <= k
        if j == 0:
            seed = np.zeros((b, m + 1), bool)
            seed[:, 0] = allowed[:, 0]
        else:
            seed = reach & allowed
        cnt = np.cumsum(~allowed, axis=1)
        s = np.where(seed, cnt, -1)
        mx = np.maximum.accumulate(s, axis=1)
        reach = allowed & (mx == cnt)
    return reach[:, m]

def brute_paths_event(k, p, m, off, lam, rho):
    """Enumerate all monotone paths; independent of the DP."""
    Lam = [0]
    for x in lam: Lam.append(Lam[-1] + x)
    Rho = [0]
    for x in rho: Rho.append(Rho[-1] + x)
    def ok(j, i): return abs(off + Lam[j] + Rho[i]) <= k
    if not ok(0, 0): return False
    stack = [(0, 0)]
    seen = {(0, 0)}
    while stack:
        j, i = stack.pop()
        if (j, i) == (p, m): return True
        for (nj, ni) in ((j + 1, i), (j, i + 1)):
            if nj <= p and ni <= m and (nj, ni) not in seen and ok(nj, ni):
                seen.add((nj, ni)); stack.append((nj, ni))
    return False

def selftest_dp():
    rng = np.random.default_rng(250825001)
    bad = 0; total = 0
    for p in range(0, 4):
        for m in range(0, 4):
            if p + m == 0: continue
            for _ in range(200):
                lam = rng.integers(0, 2, size=(1, p)) * 2 - 1
                rho = rng.integers(0, 2, size=(1, m)) * 2 - 1
                for k in (1, 2):
                    for off in range(-k, k + 1):
                        e1 = bool(dp_batch(k, p, m, off, lam, rho)[0])
                        e2 = brute_paths_event(k, p, m, off, list(lam[0]), list(rho[0]))
                        total += 1
                        if e1 != e2: bad += 1
    report("DP.selftest_checks", total)
    report("DP.selftest_mismatches", bad)

def rate(k, L, split, off, nsamp, seed):
    p = split; m = L - split
    rng = np.random.default_rng(seed)
    hits = 0; B = 20000
    done = 0
    while done < nsamp:
        b = min(B, nsamp - done)
        lam = rng.integers(0, 2, size=(b, p)) * 2 - 1 if p else np.zeros((b, 0), np.int64)
        rho = rng.integers(0, 2, size=(b, m)) * 2 - 1 if m else np.zeros((b, 0), np.int64)
        hits += int(dp_batch(k, p, m, off, lam, rho).sum())
        done += b
    return hits, nsamp

def check_rates():
    # decay in L, k = 1 and 2, balanced split, offset 0 (and parity-offset 1)
    for k, Ls, ns in ((1, (16, 32, 64, 128, 256), (200000, 200000, 200000, 100000, 60000)),
                      (2, (32, 64, 128, 256), (200000, 200000, 100000, 60000))):
        rows = []
        for L, n in zip(Ls, ns):
            h, n0 = rate(k, L, L // 2, 0, n, 250825200 + 7 * L + k)
            rows.append((L, h, n0, h / n0))
        report(f"RATE.k{k}_offset0_balanced", [(L, f"{r:.3e}", f"{h}/{n}") for (L, h, n, r) in rows])
        dec = all(rows[i][3] > rows[i + 1][3] for i in range(len(rows) - 1)
                  if rows[i + 1][1] > 0 or rows[i][1] > 0)
        report(f"RATE.k{k}_monotone_decay", dec)
    # offset effect, k = 2: offsets 0,1,2 at L = 64, 256
    for L, n in ((64, 200000), (256, 60000)):
        row = {}
        for off in (0, 1, 2):
            h, n0 = rate(2, L, L // 2, off, n, 250825300 + 11 * L + off)
            row[off] = (h, n0, h / n0)
        r20 = row[2][2] / row[0][2] if row[0][2] > 0 else None
        report(f"OFFSET.k2_L{L}", {o: f"{v[2]:.3e}" for o, v in row.items()} | {"ratio_off2/off0": None if r20 is None else round(r20, 3)})
    # parity effect, k = 1: offsets 0 vs 1 at L = 32, 128
    for L, n in ((32, 200000), (128, 100000)):
        h0, _ = rate(1, L, L // 2, 0, n, 250825400 + L)
        h1, _ = rate(1, L, L // 2, 1, n, 250825450 + L)
        report(f"PARITY.k1_L{L}_off1/off0", round(h1 / h0, 3) if h0 else None)
    # split effect, k = 1, L = 128: balanced vs skewed vs one-sided
    row = {}
    for sp in (64, 32, 16, 0):
        h, n0 = rate(1, 128, sp, 0, 100000, 250825500 + sp)
        row[sp] = h / n0
    report("SPLIT.k1_L128", {sp: f"{v:.3e}" for sp, v in row.items()})
    report("SPLIT.balanced_is_max", bool(row[64] == max(row.values())))

# =====================================================================
# Exact unconditioning check (S2 in action): conditional <= 3 sqrt(N) * uniform
# =====================================================================
def check_uncond():
    N, sigma, k = 13, 1, 1
    a1, sA, p, m = 4, 2, 4, 4
    cnt = 0; tot = 0
    for f in enum_colorings(N, sigma):
        tot += 1
        if seg_grid_cyclic(f, N, a1, sA, p, m, k):
            cnt += 1
    cond = cnt / tot
    # uniform: only f on B matters (|B| = sA + p + m = 10)
    ucnt = 0; utot = 0
    for bits in itertools.product((-1, 1), repeat=sA + p + m):
        # order: A points (sA), left arc (p), right arc (m)
        f = [0] * N
        for t in range(sA): f[(a1 + t) % N] = bits[t]
        for j in range(1, p + 1): f[(a1 - j) % N] = bits[sA + j - 1]
        for i in range(1, m + 1): f[(a1 + sA - 1 + i) % N] = bits[sA + p + i - 1]
        utot += 1
        if seg_grid_cyclic(f, N, a1, sA, p, m, k):
            ucnt += 1
    unif = ucnt / utot
    report("UNCOND.cond_prob", f"{cond:.5f} ({cnt}/{tot})")
    report("UNCOND.unif_prob", f"{unif:.5f} ({ucnt}/{utot})")
    report("UNCOND.ratio_vs_3sqrtN", f"{cond/unif:.3f} <= {3*sqrt(N):.3f}: {bool(cond <= 3*sqrt(N)*unif)}")

if __name__ == "__main__":
    check_w1()
    check_w2()
    check_s2()
    selftest_dp()
    check_s1_linear()
    check_s1_cyclic()
    check_s1_fullB()
    check_s1_cutpoints()
    check_uncond()
    check_rates()
    with open(__file__.replace("referee_checks.py", "referee_results.json"), "w") as fh:
        json.dump(OUT, fh, indent=1, default=str)
    print("DONE", flush=True)

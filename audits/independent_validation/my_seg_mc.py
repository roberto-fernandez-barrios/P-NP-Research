"""Auditor's own independent SEG Monte Carlo (fresh code, different design).

N = 600, A = [200, 349] (|A| = 150, off-center: 200 left slots, 250 right).
Uniform balanced colorings; event: exists interval chain A = D_0 c ... c D_L
(any B), all |f(D_i)| <= k.  Survival depth T via reachable-frontier DP over
u at each level.  Checks: monotone decay, offset effect at k = 2.
"""
import numpy as np

N, A0, ASZ = 600, 200, 150
UMAX, VMAX = A0, N - (A0 + ASZ)
rng = np.random.default_rng(77777)

def survival_depth(f, k):
    a0 = int(f[A0:A0 + ASZ].sum())
    if abs(a0) > k:
        return -1
    U = np.concatenate(([0], np.cumsum(f[A0 - 1::-1])))       # U[u] = f([A0-u, A0-1])
    V = np.concatenate(([0], np.cumsum(f[A0 + ASZ:])))        # V[v] = f([b+1, b+v])
    # frontier: set of feasible u at level t (v = t - u)
    feas = {0}
    T = 0
    for t in range(1, UMAX + VMAX + 1):
        nxt = set()
        for u in feas:
            # extend left: u+1, v = t-u-1
            if u + 1 <= UMAX and t - u - 1 <= VMAX and t - u - 1 >= 0:
                if abs(a0 + U[u + 1] + V[t - u - 1]) <= k:
                    nxt.add(u + 1)
            # extend right: u, v = t-u
            if t - u <= VMAX and t - u >= 0:
                if abs(a0 + U[u] + V[t - u]) <= k:
                    nxt.add(u)
        if not nxt:
            return T
        feas = nxt
        T = t
    return T

M = 3000
grid = [10, 20, 50, 100, 150, 200, 300, 400]
for k in (1, 2):
    depths = []
    off_depths = {0: [], 2: []}
    tries = 0
    while len(depths) < M and tries < 300000:
        tries += 1
        f = np.ones(N, dtype=np.int8); f[N // 2:] = -1
        rng.shuffle(f)
        T = survival_depth(f, k)
        if T >= 0:
            depths.append(T)
            if k == 2:
                a0 = abs(int(f[A0:A0 + ASZ].sum()))
                if a0 in off_depths: off_depths[a0].append(T)
    depths = np.array(depths)
    print(f"k={k}: accepted {len(depths)} of {tries} sampled")
    row = "  surv:"
    prev = None
    mono_ok = True
    for L in grid:
        p = float((depths >= L).mean())
        row += f" L{L}:{p:.4f}"
        if prev is not None and p > prev + 1e-12: mono_ok = False
        prev = p
    print(row)
    print(f"  monotone decay: {mono_ok}")
    if k == 2:
        for a0v, arr in off_depths.items():
            arr = np.array(arr)
            if len(arr):
                ps = [float((arr >= L).mean()) for L in (20, 50, 100, 200)]
                print(f"  |a0|={a0v} (M={len(arr)}): surv@20/50/100/200 = "
                      + "/".join(f"{p:.4f}" for p in ps))

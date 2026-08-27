"""
cycle05_audit_seg_selftest.py -- cross-check the batched DP of
cycle05_audit_seg_mc.py against an independent recursive brute force on
small instances (small N, exhaustive-ish random colorings).
"""

import sys

import numpy as np

sys.path.insert(0, "experiments")
import cycle05_audit_seg_mc as mc


def brute_depth(f, a_start, a_size, k, umax, vmax):
    """Independent implementation: DFS over (u, v) states."""
    a0 = int(f[a_start:a_start + a_size].sum())
    if abs(a0) > k:
        return -1
    left = f[:a_start][::-1]
    right = f[a_start + a_size:]
    U = [0]
    for x in left:
        U.append(U[-1] + int(x))
    V = [0]
    for x in right:
        V.append(V[-1] + int(x))
    seen = set()
    stack = [(0, 0)]
    best = 0
    while stack:
        u, v = stack.pop()
        if (u, v) in seen:
            continue
        seen.add((u, v))
        best = max(best, u + v)
        for nu, nv in ((u + 1, v), (u, v + 1)):
            if nu <= umax and nv <= vmax and (nu, nv) not in seen:
                if abs(a0 + U[nu] + V[nv]) <= k:
                    stack.append((nu, nv))
    return best


def main():
    rng = np.random.default_rng(7)
    # patch module geometry to a small instance
    for (N, a_start, a_size) in ((16, 6, 4), (20, 5, 6), (14, 2, 5)):
        mc.N = N
        mc.A_START = a_start
        mc.A_SIZE = a_size
        mc.UMAX = a_start
        mc.VMAX = N - (a_start + a_size)
        mc.LCAP = mc.UMAX + mc.VMAX
        for k in (1, 2):
            # random colorings, not necessarily balanced (irrelevant to DP)
            F = (rng.integers(0, 2, size=(600, N)) * 2 - 1).astype(np.int16)
            a0 = F[:, a_start:a_start + a_size].sum(axis=1).astype(np.int32)
            keep = np.abs(a0) <= k
            F = F[keep]
            if F.shape[0] == 0:
                continue
            a0, U, V = mc.prep_walks(F)
            T = mc.survival_depths(a0.copy(), U.copy(), V.copy(), k)
            for row in range(F.shape[0]):
                bt = brute_depth(F[row], a_start, a_size, k, mc.UMAX, mc.VMAX)
                assert bt == int(T[row]), (
                    f"MISMATCH N={N} k={k} row={row}: brute={bt} dp={int(T[row])} "
                    f"f={F[row].tolist()}")
            print(f"N={N}, A=[{a_start},{a_start+a_size-1}], k={k}: "
                  f"{F.shape[0]} colorings OK (DP == brute force)")
    print("SELFTEST PASSED")


if __name__ == "__main__":
    main()

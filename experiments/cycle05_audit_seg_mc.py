"""
cycle05_audit_seg_mc.py -- Adversarial audit of Lemma SEG (cycle 5): Monte Carlo
sanity check of the SHAPE of the segment interval-growth bound.

Event tested (the "any B" form used by Theorem C):
    f : uniformly random BALANCED coloring of [N], N = 2000.
    A : fixed central interval, |A| = 400 (positions 800..1199, 0-indexed).
    E_L(k) := exists an interval chain A = D_0 c D_1 c ... c D_L (each D_i an
              interval of the linear order, |D_{i+1}| = |D_i|+1, D_i between A
              and some B >= A with |B\\A| = L) with |f(D_i)| <= k for all i.
Note E_L is monotone decreasing in L, so E_L(k) = {T >= L} where
    T := max { L : E_L holds }   (survival depth; T = -1 if |f(A)| > k).

DP: reachable set over u (left-extension size) at level i = u + v.  Chain
element D = [a-u, b+v] has f(D) = a0 + U(u) + V(v), a0 = f(A),
U(u) = f([a-u, a-1]), V(v) = f([b+1, b+v]).  O(L^2) per coloring, batched.

Outputs survival curves P[T >= L | |f(A)| <= k], absolute estimates, split by
offset a0 for k = 2, prefix-only (one-sided) contrast curves, and crude
stretched-exponential shape fits.  Results -> JSON + printed table.

This is a qualitative check only: it can FALSIFY (non-decay / plateau) but a
finite-n fit can never confirm an asymptotic exponent.
"""

import json
import time

import numpy as np

# ----------------------------------------------------------------------------
N = 2000
A_SIZE = 400
A_START = 800                      # A = [800, 1199], 0-indexed
UMAX = A_START                     # left room  = 800
VMAX = N - (A_START + A_SIZE)      # right room = 800
LCAP = UMAX + VMAX                 # 1600

QUOTA_K1 = 4000                    # accepted colorings with a0 == 0
QUOTA_K2 = 6000                    # accepted colorings with |a0| <= 2
RAW_CHUNK = 4000
RAW_BUDGET = 400_000

GRID = [10, 20, 50, 100, 150, 200, 300, 400, 500, 700, 1000, 1300, 1600]
SEED = 20260821

rng = np.random.default_rng(SEED)


def sample_raw_chunk(batch):
    """batch balanced colorings of [N] as int16 rows of +-1."""
    base = np.ones((batch, N), dtype=np.int16)
    base[:, N // 2:] = -1
    idx = np.argsort(rng.random((batch, N)), axis=1)
    return np.take_along_axis(base, idx, axis=1)


def prep_walks(F):
    """F: (B, N) colorings -> a0 (B,), U (B, UMAX+1), V (B, VMAX+1) int16."""
    a0 = F[:, A_START:A_START + A_SIZE].sum(axis=1).astype(np.int32)
    left = F[:, :A_START][:, ::-1]              # f[a-1], f[a-2], ...
    right = F[:, A_START + A_SIZE:]             # f[b+1], f[b+2], ...
    U = np.zeros((F.shape[0], UMAX + 1), dtype=np.int16)
    V = np.zeros((F.shape[0], VMAX + 1), dtype=np.int16)
    np.cumsum(left, axis=1, out=U[:, 1:], dtype=np.int16)
    np.cumsum(right, axis=1, out=V[:, 1:], dtype=np.int16)
    return a0, U, V


def survival_depths(a0, U, V, k, compact_every=25, verbose_tag=""):
    """Batched DP.  Returns T (B,) int32; T = LCAP means censored (alive at cap).
    Assumes |a0| <= k for every row."""
    B = a0.shape[0]
    T = np.full(B, LCAP, dtype=np.int32)
    live_ids = np.arange(B)
    reach = np.zeros((B, UMAX + 1), dtype=bool)
    reach[:, 0] = True
    u_arr = np.arange(UMAX + 1)
    t0 = time.time()
    for i in range(1, LCAP + 1):
        vidx = i - u_arr
        valid = (vidx >= 0) & (vidx <= VMAX)
        vclip = np.clip(vidx, 0, VMAX)
        Sv = a0[:, None] + U + V[:, vclip]              # (B, UMAX+1)
        allowed = (np.abs(Sv) <= k) & valid[None, :]
        shifted = np.zeros_like(reach)
        shifted[:, 1:] = reach[:, :-1]
        reach = (reach | shifted) & allowed
        dead = ~reach.any(axis=1)
        if dead.any():
            T[live_ids[dead]] = i - 1
            keep = ~dead
            live_ids = live_ids[keep]
            reach = reach[keep]
            a0 = a0[keep]
            U = U[keep]
            V = V[keep]
            if live_ids.size == 0:
                break
        if i % compact_every == 0 and verbose_tag:
            print(f"  [{verbose_tag}] level {i}: {live_ids.size} alive "
                  f"({time.time()-t0:.1f}s)", flush=True)
    return T


def prefix_depths(a0, V, k):
    """One-sided (rightward-only) survival: max v with |a0 + V(j)| <= k for
    all j <= v.  Contrast curve (classical tube confinement)."""
    bad = np.abs(a0[:, None] + V[:, 1:]) > k            # (B, VMAX)
    any_bad = bad.any(axis=1)
    first_bad = np.where(any_bad, bad.argmax(axis=1), VMAX)
    return first_bad.astype(np.int32)                   # T_pref = first_bad


def curve(T, grid):
    M = T.shape[0]
    return {int(L): (int((T >= L).sum()), M) for L in grid}


def fit_shapes(T, grid, min_survivors=10, min_L=50):
    """ln P[T>=L] ~ -c * g(L) + b for g in candidate shapes; report R^2, c."""
    M = T.shape[0]
    pts = [(L, (T >= L).sum() / M) for L in grid
           if L >= min_L and (T >= L).sum() >= min_survivors and (T >= L).sum() < M]
    if len(pts) < 3:
        return {"points_used": len(pts), "fits": {}}
    Ls = np.array([p[0] for p in pts], dtype=float)
    lnP = np.log(np.array([p[1] for p in pts]))
    shapes = {"L^(1/5)": Ls ** 0.2, "L^(1/3)": Ls ** (1 / 3),
              "L^(1/2)": Ls ** 0.5, "L": Ls, "ln L": np.log(Ls)}
    out = {}
    for name, g in shapes.items():
        Amat = np.vstack([g, np.ones_like(g)]).T
        coef, res, *_ = np.linalg.lstsq(Amat, lnP, rcond=None)
        pred = Amat @ coef
        ss_res = float(((lnP - pred) ** 2).sum())
        ss_tot = float(((lnP - lnP.mean()) ** 2).sum())
        out[name] = {"c": -float(coef[0]), "intercept": float(coef[1]),
                     "R2": 1 - ss_res / ss_tot if ss_tot > 0 else float("nan")}
    return {"points_used": len(pts), "grid_pts": [(float(L), float(p)) for L, p in pts],
            "fits": out}


def main():
    t_start = time.time()
    n_raw = 0
    acc = {"k1": [], "k2": []}     # lists of (a0, U, V) tuples per chunk
    n_acc = {"k1": 0, "k2": 0}
    n_a0 = {}                      # histogram of a0 among raws (for P[accept])

    print(f"Sampling balanced colorings of [N={N}], A = [{A_START},"
          f"{A_START+A_SIZE-1}] (|A|={A_SIZE}), UMAX={UMAX}, VMAX={VMAX}")
    while (n_acc["k1"] < QUOTA_K1 or n_acc["k2"] < QUOTA_K2) and n_raw < RAW_BUDGET:
        F = sample_raw_chunk(RAW_CHUNK)
        n_raw += RAW_CHUNK
        a0c = F[:, A_START:A_START + A_SIZE].sum(axis=1).astype(np.int32)
        for v in (-4, -2, 0, 2, 4):
            n_a0[v] = n_a0.get(v, 0) + int((a0c == v).sum())
        m2 = np.abs(a0c) <= 2
        if m2.any() and n_acc["k2"] < QUOTA_K2:
            a0, U, V = prep_walks(F[m2])
            acc["k2"].append((a0, U, V))
            n_acc["k2"] += int(m2.sum())
        m1 = a0c == 0
        if m1.any() and n_acc["k1"] < QUOTA_K1:
            a0, U, V = prep_walks(F[m1])
            acc["k1"].append((a0, U, V))
            n_acc["k1"] += int(m1.sum())
        if n_raw % 40000 == 0:
            print(f"  raw={n_raw}  acc_k1={n_acc['k1']}  acc_k2={n_acc['k2']}",
                  flush=True)

    p_acc = {"k1": n_a0.get(0, 0) / n_raw,
             "k2": sum(n_a0.get(v, 0) for v in (-2, 0, 2)) / n_raw}
    print(f"raw={n_raw}; P[a0=0]~{p_acc['k1']:.4f}, P[|a0|<=2]~{p_acc['k2']:.4f}")

    results = {"N": N, "A_size": A_SIZE, "A_start": A_START, "LCAP": LCAP,
               "seed": SEED, "n_raw": n_raw, "p_accept": p_acc,
               "a0_hist_raw": {str(kk): vv for kk, vv in sorted(n_a0.items())},
               "grid": GRID, "runs": {}}

    for tag, k, quota in (("k1", 1, QUOTA_K1), ("k2", 2, QUOTA_K2)):
        a0 = np.concatenate([t[0] for t in acc[tag]])[:quota]
        U = np.vstack([t[1] for t in acc[tag]])[:quota]
        V = np.vstack([t[2] for t in acc[tag]])[:quota]
        M = a0.shape[0]
        print(f"\n=== k={k}: DP on {M} accepted colorings ===", flush=True)
        T = survival_depths(a0.copy(), U.copy(), V.copy(), k,
                            verbose_tag=f"k={k}")
        Tp = prefix_depths(a0, V, k)
        run = {"k": k, "M": M,
               "surv": curve(T, GRID),
               "surv_prefix": curve(Tp, GRID),
               "T_stats": {"median": float(np.median(T)), "mean": float(T.mean()),
                           "max": int(T.max()), "censored_at_cap": int((T == LCAP).sum())},
               "fits": fit_shapes(T, GRID)}
        if k == 2:
            for lab, mask in (("a0=0", a0 == 0), ("|a0|=2", np.abs(a0) == 2)):
                run[f"surv_{lab}"] = curve(T[mask], GRID)
                run[f"fits_{lab}"] = fit_shapes(T[mask], GRID)
                run[f"M_{lab}"] = int(mask.sum())
        results["runs"][tag] = run
        print(f"  k={k}: median T={np.median(T):.0f}, max T={T.max()}, "
              f"censored={int((T==LCAP).sum())}")

    out_path = "experiments/cycle05_audit_seg_mc_results.json"
    with open(out_path, "w") as fh:
        json.dump(results, fh, indent=1)
    print(f"\nWrote {out_path}  ({time.time()-t_start:.0f}s total)")

    # ---- printed table ----------------------------------------------------
    for tag in ("k1", "k2"):
        run = results["runs"][tag]
        k, M = run["k"], run["M"]
        print(f"\nSurvival table, k={k} (M={M} accepted; P[accept]~"
              f"{p_acc[tag]:.4f}):")
        print("  L    surv    P[T>=L|acc]   abs.est      prefix-only")
        for L in GRID:
            s, m = run["surv"][L]
            sp, mp = run["surv_prefix"][L]
            pc = s / m
            print(f"  {L:5d} {s:6d}   {pc:11.5f}   {pc*p_acc[tag]:.3e}   "
                  f"{sp/mp:.5f}")
        print("  shape fits (ln P vs -c*g(L)):",
              {kk: (round(vv['c'], 4), round(vv['R2'], 4))
               for kk, vv in run["fits"]["fits"].items()}
              if run["fits"]["fits"] else "insufficient tail data")


if __name__ == "__main__":
    main()

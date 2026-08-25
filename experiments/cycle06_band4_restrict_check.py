"""Cycle 6: finite check of Lemma W4-RESTRICT.

Claim (elementary; proof in results/research_cycle_06_reassessment.md):
if X is 1-balanced-chain on [n+2] and a,b are two fixed points, then
X|ab = { S \\ {a,b} : S in X } contains, for every total-+2 coloring f of
the remaining n points, a maximal chain with all prefix imbalances in
[-1,3], and for every total--2 coloring a chain with prefix imbalances
in [-3,1]; and |X|ab| <= |X|.  Hence R_[-1,3](n) <= N(n+2).

This script builds verified 1-balanced-chain families on 6 and 8 points
with the Cycle-6 search machinery, restricts them (removing the two top
points), and literally checks the band-4 routing property on 4 and 6
points respectively.  Standard library only; deterministic.

Run:  python -B experiments/cycle06_band4_restrict_check.py
"""

import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cycle06_defect_router_exact as base


def restrict(X, n_small, a, b):
    drop = ~((1 << a) | (1 << b))
    return {S & drop for S in X}


def main():
    rng = random.Random(base.SEED + 2)
    ok_all = True
    for n_big, restarts in ((6, 40), (8, 25)):
        n_small = n_big - 2
        a, b = n_big - 2, n_big - 1
        cols_bal = base.colorings_balanced(n_big)
        size, X = base.minimize_family(n_big, cols_bal, -1, 1, rng, restarts)
        assert base.is_valid_family(set(X), n_big, cols_bal, -1, 1)
        Xr = restrict(X, n_small, a, b)
        plus = base.colorings_plus2(n_small)
        minus = base.colorings_minus2(n_small)
        ok_p = base.is_valid_family(Xr, n_small, plus, -1, 3)
        ok_m = base.is_valid_family(Xr, n_small, minus, -3, 1)
        ok = ok_p and ok_m and len(Xr) <= len(X)
        ok_all &= ok
        print(f"W4-RESTRICT check: |X_{n_big}|={size} (verified balanced) -> "
              f"restricted family size {len(Xr)} on {n_small} points; "
              f"width-4 routing +2 side: {ok_p}, -2 side: {ok_m} "
              f"[{'PASS' if ok else 'FAIL'}]")
    print("W4-RESTRICT FINITE CHECKS PASS" if ok_all
          else "W4-RESTRICT FINITE CHECKS FAIL")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())

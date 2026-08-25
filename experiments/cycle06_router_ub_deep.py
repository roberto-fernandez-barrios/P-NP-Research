"""Cycle 6 supplement: deeper upper-bound search for R(8), R(10).

Reuses the definitions and checkers of cycle06_defect_router_exact.py
(imported, not reimplemented) and runs a longer seeded minimization plus
a perturbation phase (kick one witness chain, re-minimize).  Upper
bounds only; the rigorous lower bounds remain the exact sum-of-rho
values from the base experiment.  Deterministic (seeded).

Run:  python -B experiments/cycle06_router_ub_deep.py
"""

import json
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cycle06_defect_router_exact as base


def deep_minimize(n, restarts, kicks, rng):
    cols = base.colorings_plus2(n)
    best_size, best_family = base.minimize_family(n, cols, 0, 2, rng, restarts)
    # perturbation phase: restart from best family's witnesses, kick chains
    for _ in range(kicks):
        D = set(best_family)
        lv = base.family_by_level(D, n)
        witness = {}
        ok = True
        for P in cols:
            w = base.find_witness(lv, n, P, 0, 2)
            if w is None:
                ok = False
                break
            witness[P] = w
        if not ok:
            break
        # kick: replace a few random witnesses by fresh random chains
        for P in rng.sample(cols, max(2, len(cols) // 12)):
            ch = base.order_to_sets(
                base.random_band_order(n, P, 0, 2, rng))
            witness[P] = ch
            D.update(ch)
        # re-minimize by removal with witness caching
        improved = True
        while improved:
            improved = False
            order_out = list(D)
            rng.shuffle(order_out)
            for S in order_out:
                if S == 0 or S == (1 << n) - 1 or S not in D:
                    continue
                affected = [P for P in cols if S in witness[P]]
                D.discard(S)
                lv = base.family_by_level(D, n)
                new_w = {}
                ok2 = True
                for P in affected:
                    w = base.find_witness(lv, n, P, 0, 2)
                    if w is None:
                        ok2 = False
                        break
                    new_w[P] = w
                if ok2:
                    witness.update(new_w)
                    improved = True
                else:
                    D.add(S)
        if len(D) < best_size:
            best_size = len(D)
            best_family = sorted(D)
            print(f"  n={n}: improved UB -> {best_size}", flush=True)
    return best_size, best_family


def main():
    rng = random.Random(base.SEED + 1)
    out = {}
    for n, restarts, kicks in ((8, 400, 250), (10, 40, 120)):
        size, fam = deep_minimize(n, restarts, kicks, rng)
        cols_p = base.colorings_plus2(n)
        cols_m = base.colorings_minus2(n)
        vp = base.is_valid_family(set(fam), n, cols_p, 0, 2)
        vm = base.is_valid_family(set(fam), n, cols_m, -2, 0)
        assert vp and vm
        out[str(n)] = {"deep_UB": size, "witness_family": [int(x) for x in fam],
                       "verified_plus": bool(vp), "verified_minus": bool(vm)}
        print(f"R({n}) deep UB = {size} (two-sided verified)", flush=True)
    path = os.path.join(base.OUT_DIR, "cycle06_router_values_deep.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    print(f"wrote {path}")
    print("DEEP UB SEARCH DONE")


if __name__ == "__main__":
    main()

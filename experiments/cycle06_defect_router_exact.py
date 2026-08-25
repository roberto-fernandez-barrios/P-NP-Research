"""Research Cycle 6 bounded experiment: one-sided 2-defect routers.

Everything here is standard library only and deterministic (seeded).

Objects.  Ground set [n] = {0,...,n-1}, n even, m = n/2.  A "+2 coloring"
is a subset P of [n] with |P| = m+1 (the positive side); the coloring is
f(x)=+1 iff x in P.  The imbalance of S under P is

    d_P(S) = 2|S & P| - |S|.

A family D of subsets is a one-sided 2-defect router (Cycle-3 definition,
research_cycle_03/cp_s_recursion_attack.md section 5.2) iff

  (+) for every +2 coloring P there is a maximal chain
      {} = C_0 < C_1 < ... < C_n = [n], all C_i in D, with
      d_P(C_i) in [0,2] for every i; and
  (-) for every -2 coloring (|P| = m-1) a maximal chain in D with
      d_P(C_i) in [-2,0] for every i.

R(n) is the minimum size of such a D.

Checks performed:

1. LEMMA R-SYM (finite check).  Condition (-) is equivalent to
   condition (+) with the SAME chains: a chain C has d in [0,2] for the
   +2 coloring P iff C has d in [-2,0] for the -2 coloring [n]\\P.
   (Proof: d_{[n]\\P}(S) = |S| - 2|S&P| + 2|S&P| - ... = -d_P(S) after
   negating the coloring; checked literally below on all orderings.)
   Consequently R(n) is computed from the (+) side alone.

2. LEMMA R-PARITY (finite check).  For a +2 coloring, a maximal chain
   has all prefix imbalances in [0,2] iff every odd prefix has imbalance
   exactly 1 and every even prefix has imbalance 0 or 2, iff the ordered
   pair walk condition holds: reading consecutive ordered pairs
   (pi_{2i-1}, pi_{2i}), from even-state 0 the pair is (+,-) [stay 0] or
   (+,+) [go to 2], from even-state 2 the pair is (-,+) [stay 2] or
   (-,-) [go to 0]; the walk starts at 0 and ends at 2.

3. LEMMA R-DUAL (finite check).  Complementation S -> [n]\\S maps the
   band [0,2] to itself (d_P([n]\\S) = 2 - d_P(S)), so the level-cover
   minima satisfy rho(n,k) = rho(n,n-k) and reversal+complementation of
   a valid band chain is a valid band chain.

4. Exact per-level cover minima rho(n,k) (branch-and-bound set cover,
   exact) and the rigorous lower bound R(n) >= sum_k rho(n,k).

5. Upper bounds by witness-chain-union seeding plus removal
   minimization with witness caching (many seeded restarts); exact
   values whenever UB == LB.

6. The same machinery run on the balanced problem (band [-1,1], total-0
   colorings) as a self-test: it must reproduce the known values
   N(4)=6, N(6)=12 (L=N there) and reach the known N(8)=20 over L(8)=19.

7. DEFECT-LIFT finite recheck: with X_4 an optimal balanced family
   (size 6) and D_4 an optimal router (size 7), the Cycle-3 lift
   R(X,D) = X u ({a}+D) u {U+{b}, U+{a,b}} must be 1-balanced-chain on
   six points with exactly |X|+|D|+2 = 15 subsets.

Run:  python -B experiments/cycle06_defect_router_exact.py
"""

import itertools
import json
import os
import random
import sys
from math import comb

SEED = 20260825
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "certificates", "cycle06_router")


def popcount(x):
    return bin(x).count("1")


def colorings_plus2(n):
    """Positive-side masks of size n/2+1."""
    m = n // 2
    return [sum(1 << i for i in c) for c in itertools.combinations(range(n), m + 1)]


def colorings_minus2(n):
    m = n // 2
    return [sum(1 << i for i in c) for c in itertools.combinations(range(n), m - 1)]


def colorings_balanced(n):
    m = n // 2
    return [sum(1 << i for i in c) for c in itertools.combinations(range(n), m)]


def imbalance(S, P):
    return 2 * popcount(S & P) - popcount(S)


def chain_band_ok(order, P, lo, hi):
    """order: tuple of points; checks all prefix imbalances in [lo,hi]."""
    S = 0
    d = 0
    for x in order:
        S |= 1 << x
        d += 1 if (P >> x) & 1 else -1
        if d < lo or d > hi:
            return False
    return True


# ----------------------------------------------------------------------
# Lemma checks
# ----------------------------------------------------------------------

def check_r_sym(n, sample_orders=None, rng=None):
    """Chain serves +2 coloring P with band [0,2] iff it serves the -2
    coloring [n]\\P with band [-2,0]."""
    full = (1 << n) - 1
    if sample_orders is None:
        orders = list(itertools.permutations(range(n)))
    else:
        orders = [tuple(rng.sample(range(n), n)) for _ in range(sample_orders)]
    for P in colorings_plus2(n):
        Q = full & ~P  # -2 coloring
        for order in orders:
            a = chain_band_ok(order, P, 0, 2)
            b = chain_band_ok(order, Q, -2, 0)
            if a != b:
                return False, (order, P)
    return True, None


def check_r_parity(n, sample_orders=None, rng=None):
    if sample_orders is None:
        orders = list(itertools.permutations(range(n)))
    else:
        orders = [tuple(rng.sample(range(n), n)) for _ in range(sample_orders)]
    for P in colorings_plus2(n):
        for order in orders:
            a = chain_band_ok(order, P, 0, 2)
            # parity characterization
            S = 0
            d = 0
            ok = True
            for i, x in enumerate(order, start=1):
                S |= 1 << x
                d += 1 if (P >> x) & 1 else -1
                if i % 2 == 1:
                    if d != 1:
                        ok = False
                        break
                else:
                    if d not in (0, 2):
                        ok = False
                        break
            # ordered-pair state walk
            state = 0
            walk_ok = True
            for i in range(0, n, 2):
                u, v = order[i], order[i + 1]
                su = 1 if (P >> u) & 1 else -1
                sv = 1 if (P >> v) & 1 else -1
                if state == 0:
                    if (su, sv) == (1, -1):
                        pass
                    elif (su, sv) == (1, 1):
                        state = 2
                    else:
                        walk_ok = False
                        break
                else:
                    if (su, sv) == (-1, 1):
                        pass
                    elif (su, sv) == (-1, -1):
                        state = 0
                    else:
                        walk_ok = False
                        break
            walk_ok = walk_ok and state == 2
            if not (a == ok == walk_ok):
                return False, (order, P)
    return True, None


def check_r_dual(n):
    """d_P(complement S) = 2 - d_P(S) for +2 colorings; hence compatible
    level-k sets biject with compatible level-(n-k) sets."""
    full = (1 << n) - 1
    for P in colorings_plus2(n):
        for S in range(1 << n):
            if imbalance(full & ~S, P) != 2 - imbalance(S, P):
                return False, (S, P)
    return True, None


# ----------------------------------------------------------------------
# Exact per-level cover minima (branch-and-bound set cover)
# ----------------------------------------------------------------------

def allowed_at_level(k, band_lo, band_hi):
    """Allowed imbalance values at level k inside [band_lo, band_hi]
    (imbalance has the parity of k)."""
    return [d for d in range(band_lo, band_hi + 1) if (d - k) % 2 == 0]


def level_cover_min(n, k, cols, band_lo, band_hi):
    """Exact minimum number of k-subsets such that every coloring in
    cols has one with imbalance in the band.  Exact B&B set cover.

    Symmetry use (valid as in Cycle 3 section 3.1): S_n is transitive on
    k-subsets and permutes the coloring set while preserving imbalance,
    so if any size-m cover exists then one exists containing the
    canonical subset {0,...,k-1}.  For k not in {0,n} the search
    therefore fixes that first member.
    """
    allowed = set(allowed_at_level(k, band_lo, band_hi))
    subsets = [sum(1 << i for i in c) for c in itertools.combinations(range(n), k)]
    ncol = len(cols)
    covers = []
    for S in subsets:
        mask = 0
        for j, P in enumerate(cols):
            if imbalance(S, P) in allowed:
                mask |= 1 << j
        covers.append(mask)
    fullmask = (1 << ncol) - 1
    union_all = 0
    for c in covers:
        union_all |= c
    if union_all != fullmask:
        return None, None
    # greedy upper bound
    def greedy():
        unc = fullmask
        chosen = []
        while unc:
            best_i = max(range(len(covers)), key=lambda i: popcount(covers[i] & unc))
            chosen.append(best_i)
            unc &= ~covers[best_i]
        return chosen
    best = [len(greedy())]
    best_sol = [None]
    maxcov = max(popcount(c) for c in covers)
    who = [[] for _ in range(ncol)]
    for i, c in enumerate(covers):
        for j in range(ncol):
            if (c >> j) & 1:
                who[j].append(i)

    def dfs(unc, chosen):
        if unc == 0:
            if len(chosen) < best[0]:
                best[0] = len(chosen)
                best_sol[0] = list(chosen)
            return
        need = (popcount(unc) + maxcov - 1) // maxcov
        if len(chosen) + need >= best[0]:
            return
        j_pick, cands = None, None
        for j in range(ncol):
            if (unc >> j) & 1:
                c = who[j]
                if cands is None or len(c) < len(cands):
                    j_pick, cands = j, c
        for i in sorted(cands, key=lambda i: -popcount(covers[i] & unc)):
            chosen.append(i)
            dfs(unc & ~covers[i], chosen)
            chosen.pop()

    if 0 < k < n:
        canon = 0
        for i, S in enumerate(subsets):
            if S == (1 << k) - 1:
                canon = i
                break
        dfs(fullmask & ~covers[canon], [canon])
    else:
        dfs(fullmask, [])
    sol = best_sol[0]
    sol_masks = [subsets[i] for i in sol] if sol is not None else [subsets[i] for i in greedy()]
    return best[0], sol_masks


# ----------------------------------------------------------------------
# Validity checking and witness extraction (reachability DP by level)
# ----------------------------------------------------------------------

def family_by_level(D, n):
    lv = [[] for _ in range(n + 1)]
    for S in D:
        lv[popcount(S)].append(S)
    return lv


def find_witness(lv, n, P, band_lo, band_hi):
    """Return a witness chain (list of subsets level 0..n) or None.

    Reachability DP by level; the predecessor of a level-k set T is
    looked up among its k single-element deletions (dict lookups),
    rather than by scanning the whole previous layer.
    """
    allowed_cache = [set(allowed_at_level(k, band_lo, band_hi)) for k in range(n + 1)]
    if 0 not in lv[0]:
        return None
    reach = {0: None} if imbalance(0, P) in allowed_cache[0] else {}
    layers = [reach]
    for k in range(1, n + 1):
        cur = {}
        prev_layer = layers[k - 1]
        if not prev_layer:
            return None
        for T in lv[k]:
            if imbalance(T, P) not in allowed_cache[k]:
                continue
            rem = T
            while rem:
                low = rem & (-rem)
                if (T & ~low) in prev_layer:
                    cur[T] = T & ~low
                    break
                rem &= rem - 1
        layers.append(cur)
    full = (1 << n) - 1
    if full not in layers[n]:
        return None
    chain = [full]
    for k in range(n, 0, -1):
        chain.append(layers[k][chain[-1]])
    chain.reverse()
    return chain


def is_valid_family(D, n, cols, band_lo, band_hi):
    lv = family_by_level(D, n)
    for P in cols:
        if find_witness(lv, n, P, band_lo, band_hi) is None:
            return False
    return True


# ----------------------------------------------------------------------
# Upper-bound search: witness-union seeding + removal minimization
# ----------------------------------------------------------------------

def random_band_order(n, P, band_lo, band_hi, rng, tries=800):
    pts = list(range(n))
    for _ in range(tries):
        rng.shuffle(pts)
        if chain_band_ok(tuple(pts), P, band_lo, band_hi):
            return tuple(pts)
    # deterministic fallback: interleave positives and negatives
    pos = [x for x in pts if (P >> x) & 1]
    neg = [x for x in pts if not (P >> x) & 1]
    order = []
    if band_lo == 0:            # +2 router band: p n p n ... p [p]
        while neg:
            order.append(pos.pop())
            order.append(neg.pop())
        order.extend(pos)
    else:                        # balanced band [-1,1]: p n p n ...
        while pos and neg:
            order.append(pos.pop())
            order.append(neg.pop())
        order.extend(pos)
        order.extend(neg)
    order = tuple(order)
    assert chain_band_ok(order, P, band_lo, band_hi)
    return order


def order_to_sets(order):
    out = [0]
    S = 0
    for x in order:
        S |= 1 << x
        out.append(S)
    return out


def minimize_family(n, cols, band_lo, band_hi, rng, restarts, inner_passes=6):
    best_size = None
    best_family = None
    for _ in range(restarts):
        # seed: one random band chain per coloring
        witness = {}
        D = set()
        for P in cols:
            ch = order_to_sets(random_band_order(n, P, band_lo, band_hi, rng))
            witness[P] = ch
            D.update(ch)
        # removal loop with witness caching
        improved = True
        passes = 0
        while improved and passes < inner_passes:
            improved = False
            passes += 1
            order_out = list(D)
            rng.shuffle(order_out)
            for S in order_out:
                if S == 0 or S == (1 << n) - 1:
                    continue
                if S not in D:
                    continue
                affected = [P for P in cols if S in witness[P]]
                D.discard(S)
                lv = family_by_level(D, n)
                new_w = {}
                ok = True
                for P in affected:
                    w = find_witness(lv, n, P, band_lo, band_hi)
                    if w is None:
                        ok = False
                        break
                    new_w[P] = w
                if ok:
                    witness.update(new_w)
                    improved = True
                else:
                    D.add(S)
        if best_size is None or len(D) < best_size:
            best_size = len(D)
            best_family = sorted(D)
    return best_size, best_family


# ----------------------------------------------------------------------
# DEFECT-LIFT finite recheck
# ----------------------------------------------------------------------

def defect_lift(X4, D4):
    """Cycle-3 lift with new points a=4, b=5 on old ground set {0,1,2,3}."""
    a, b = 4, 5
    U = 0b1111
    lifted = set(X4)
    for S in D4:
        lifted.add(S | (1 << a))
    lifted.add(U | (1 << b))
    lifted.add(U | (1 << a) | (1 << b))
    return sorted(lifted)


# ----------------------------------------------------------------------
# Driver
# ----------------------------------------------------------------------

def main():
    rng = random.Random(SEED)
    results = {"seed": SEED, "definition":
               "R(n) = min size of one-sided 2-defect router (Cycle-3 "
               "definition); by Lemma R-SYM computed from the +2 side alone.",
               "lemma_checks": {}, "rho": {}, "R": {}, "balanced_selftest": {},
               "defect_lift": {}}
    ok_all = True

    # Lemma checks
    for n in (4, 6):
        ok1, _ = check_r_sym(n)
        ok2, _ = check_r_parity(n)
        print(f"LEMMA R-SYM   n={n} exhaustive over all {comb(n, n//2+1)} "
              f"+2 colorings x n! orderings: {'PASS' if ok1 else 'FAIL'}")
        print(f"LEMMA R-PARITY n={n} exhaustive: {'PASS' if ok2 else 'FAIL'}")
        results["lemma_checks"][f"R-SYM_n{n}"] = "PASS-EXHAUSTIVE" if ok1 else "FAIL"
        results["lemma_checks"][f"R-PARITY_n{n}"] = "PASS-EXHAUSTIVE" if ok2 else "FAIL"
        ok_all &= ok1 and ok2
    ok1, _ = check_r_sym(8, sample_orders=3000, rng=rng)
    ok2, _ = check_r_parity(8, sample_orders=3000, rng=rng)
    print(f"LEMMA R-SYM   n=8 sampled 3000 orderings x all colorings: "
          f"{'PASS' if ok1 else 'FAIL'}")
    print(f"LEMMA R-PARITY n=8 sampled: {'PASS' if ok2 else 'FAIL'}")
    results["lemma_checks"]["R-SYM_n8"] = "PASS-SAMPLED" if ok1 else "FAIL"
    results["lemma_checks"]["R-PARITY_n8"] = "PASS-SAMPLED" if ok2 else "FAIL"
    ok_all &= ok1 and ok2
    for n in (4, 6):
        okd, _ = check_r_dual(n)
        print(f"LEMMA R-DUAL  n={n} exhaustive over all subsets: "
              f"{'PASS' if okd else 'FAIL'}")
        results["lemma_checks"][f"R-DUAL_n{n}"] = "PASS-EXHAUSTIVE" if okd else "FAIL"
        ok_all &= okd

    # rho tables and R(n) brackets
    for n in (2, 4, 6, 8, 10):
        cols = colorings_plus2(n)
        rho = []
        for k in range(n + 1):
            v, _ = level_cover_min(n, k, cols, 0, 2)
            rho.append(v)
        LB = sum(rho)
        results["rho"][str(n)] = rho
        # duality sanity
        dual_ok = all(rho[k] == rho[n - k] for k in range(n + 1))
        ok_all &= dual_ok
        restarts = {2: 5, 4: 60, 6: 60, 8: 40, 10: 12}[n]
        UB, fam = minimize_family(n, cols, 0, 2, rng, restarts)
        valid = is_valid_family(set(fam), n, cols, 0, 2)
        # also confirm the two-sided condition literally (R-SYM consequence)
        valid_minus = is_valid_family(set(fam), n, colorings_minus2(n), -2, 0)
        ok_all &= valid and valid_minus
        exact = (UB == LB)
        results["R"][str(n)] = {"rho": rho, "LB_sum_rho": LB, "UB": UB,
                                "exact": exact, "dual_symmetric_rho": dual_ok,
                                "witness_family": [int(x) for x in fam],
                                "witness_verified_plus_side": bool(valid),
                                "witness_verified_minus_side": bool(valid_minus)}
        tag = "EXACT" if exact else "BRACKET"
        print(f"R({n}): rho={rho} sum={LB}  UB={UB}  [{tag}]  "
              f"two-sided verified={valid and valid_minus}")

    # balanced self-test
    known_N = {4: 6, 6: 12, 8: 20}
    for n in (4, 6, 8):
        cols = colorings_balanced(n)
        tau = []
        for k in range(n + 1):
            v, _ = level_cover_min(n, k, cols, -1, 1)
            tau.append(v)
        L = sum(tau)
        restarts = {4: 60, 6: 60, 8: 60}[n]
        UB, fam = minimize_family(n, cols, -1, 1, rng, restarts)
        valid = is_valid_family(set(fam), n, cols, -1, 1)
        ok_all &= valid
        match = (UB == known_N[n])
        results["balanced_selftest"][str(n)] = {
            "tau": tau, "L": L, "UB": UB, "known_N": known_N[n],
            "UB_matches_known_N": match, "witness_verified": bool(valid)}
        print(f"balanced self-test n={n}: tau={tau} L={L} UB={UB} "
              f"known N={known_N[n]} match={match}")
        if n in (4, 6):
            ok_all &= match  # L=N there; machinery must reproduce it

    # DEFECT-LIFT recheck with optimal X_4 and D_4
    cols4b = colorings_balanced(4)
    _, X4 = minimize_family(4, cols4b, -1, 1, rng, 60)
    cols4r = colorings_plus2(4)
    _, D4 = minimize_family(4, cols4r, 0, 2, rng, 60)
    lifted = defect_lift(X4, D4)
    cols6b = colorings_balanced(6)
    lift_valid = is_valid_family(set(lifted), 6, cols6b, -1, 1)
    count_ok = (len(lifted) == len(X4) + len(D4) + 2)
    ok_all &= lift_valid and count_ok
    results["defect_lift"] = {
        "X4_size": len(X4), "D4_size": len(D4), "lift_size": len(lifted),
        "additive_count_ok": count_ok,
        "lift_is_balanced_chain_on_6": bool(lift_valid),
        "X4": [int(x) for x in X4], "D4": [int(x) for x in D4],
        "lifted": [int(x) for x in lifted]}
    print(f"DEFECT-LIFT recheck: |X4|={len(X4)} |D4|={len(D4)} "
          f"|R(X,D)|={len(lifted)} additive={count_ok} "
          f"valid-on-6={lift_valid}")

    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "cycle06_router_values.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=1)
    print(f"wrote {out}")
    print("ALL CYCLE-6 ROUTER CHECKS PASS" if ok_all
          else "CYCLE-6 ROUTER CHECKS: FAILURES PRESENT")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())

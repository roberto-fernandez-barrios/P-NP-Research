"""Cycle 5 adversarial audit (SKEPTIC): independent lemma-level checks for
Theorem A (switch_structure_theory.md section 2) and Theorem E
(dense_circle_obstruction.md).

Written from scratch for the audit; shares no code with cycle05_hybrid_core.py.
All checks are direct set computations over the literal definitions.

Run:  python -B experiments/cycle05_audit_thm_lemmas.py
"""

from __future__ import annotations

from math import gcd

FAIL = []


def report(name: str, ok: bool, detail: str = ""):
    tag = "PASS" if ok else "FAIL"
    print(f"[{tag}] {name}" + (f" -- {detail}" if detail else ""))
    if not ok:
        FAIL.append((name, detail))


# ---------------------------------------------------------------- primitives


def is_cyclic_interval(S: frozenset[int], q: int) -> bool:
    s = len(S)
    if s == 0 or s == q:
        return True
    # S is an interval iff its complement is a single cyclic run
    # equivalently: number of x in S with x+1 not in S equals 1
    ends = sum(1 for x in S if (x + 1) % q not in S)
    return ends == 1


def ap_set(c: int, a: int, s: int, q: int) -> frozenset[int]:
    return frozenset((c + j * a) % q for j in range(s))


def adjacency_count(S: frozenset[int], q: int) -> int:
    return sum(1 for x in S if (x + 1) % q in S)


def gaps_of(S: frozenset[int], q: int) -> list[tuple[int, int]]:
    """Maximal runs of the complement, as (start, length)."""
    comp = [x for x in range(q) if x not in S]
    if not comp:
        return []
    if len(comp) == q:
        return [(0, q)]
    compset = set(comp)
    out = []
    for x in comp:
        if (x - 1) % q not in compset:  # run start
            L = 0
            y = x
            while y in compset:
                L += 1
                y = (y + 1) % q
            out.append((x, L))
    return out


def defect_and_hulls(S: frozenset[int], q: int):
    """Return (defect, list of minimal hulls as frozensets)."""
    if len(S) == q:
        return 0, [frozenset(range(q))]
    g = gaps_of(S, q)
    mx = max(L for (_, L) in g)
    hulls = []
    for (st, L) in g:
        if L == mx:
            hulls.append(frozenset((st + L + k) % q for k in range(q - L)))
    return q - mx - len(S), hulls


# ------------------------------------------------------ Lemma A.1 (formula)


def check_A1():
    ok_formula = True
    ok_statement = True
    witness = None
    for q in (7, 11, 21, 25):
        for a in range(2, q):  # a = 1 checked as control below
            if gcd(a, q) != 1:
                continue
            h = pow(a, -1, q)
            for s in range(2, q):
                for c in (0, 1, (q - 1) // 2):
                    S = ap_set(c, a, s, q)
                    assert len(S) == s
                    cnt = adjacency_count(S, q)
                    formula = max(0, s - h) + max(0, s - (q - h))
                    if cnt != formula:
                        ok_formula = False
                        witness = (q, a, s, c, cnt, formula)
                    ival = is_cyclic_interval(S, q)
                    # statement: a not in {1,q-1}, 2<=s<=q-2 -> not interval
                    if a not in (1, q - 1) and 2 <= s <= q - 2 and ival:
                        ok_statement = False
                        witness = ("interval!", q, a, s, c, sorted(S))
                    # control: s = q-1 always interval
                    if s == q - 1 and not ival:
                        ok_statement = False
                        witness = ("q-1 not interval!", q, a, s, c)
        # control a = 1 and a = q-1: APs ARE intervals
        for a in (1, q - 1):
            for s in range(2, q):
                if not is_cyclic_interval(ap_set(3, a, s, q), q):
                    ok_statement = False
                    witness = ("control", q, a, s)
    report("A.1 adjacency-count formula (q in 7,11,21,25; all invertible a, all s, 3 offsets)",
           ok_formula, str(witness) if witness else "")
    report("A.1 statement: no difference-a AP of size 2..q-2 is an interval (a != +-1)",
           ok_statement, str(witness) if witness else "")


# ------------------------------------------------------ Lemma A.2 (statement)


def check_A2():
    all_ok = True
    boundary_witnesses = []
    for q in (7, 11, 21, 25):
        intervals_by_size: dict[int, set[frozenset[int]]] = {}
        for s in range(1, q):
            intervals_by_size[s] = set()
            for st in range(q):
                intervals_by_size[s].add(frozenset((st + k) % q for k in range(s)))
        for a in range(2, q - 1):
            if gcd(a, q) != 1:
                continue
            aps_by_size: dict[int, set[frozenset[int]]] = {}
            for s in range(1, q):
                aps_by_size[s] = set(ap_set(c, a, s, q) for c in range(q))
            # direction O -> O': A interval size j, A u {y} an AP of size j+1
            for j in range(1, q - 1):
                for A in intervals_by_size[j]:
                    for y in range(q):
                        if y in A:
                            continue
                        B = A | {y}
                        if B in aps_by_size[j + 1]:
                            if not (j <= 2 or j >= q - 3):
                                all_ok = False
                                print("  A.2 VIOLATION O->O'", q, a, j, sorted(A), y)
                            elif j == q - 3:
                                boundary_witnesses.append(("O->O'", q, a, j))
            # direction O' -> O: A AP size j, A u {y} an interval of size j+1
            for j in range(1, q - 1):
                for A in aps_by_size[j]:
                    for y in range(q):
                        if y in A:
                            continue
                        B = A | {y}
                        if B in intervals_by_size[j + 1] if j + 1 < q else is_cyclic_interval(B, q):
                            if not (j <= 2 or j >= q - 3):
                                all_ok = False
                                print("  A.2 VIOLATION O'->O", q, a, j, sorted(A), y)
                            elif j == q - 3:
                                boundary_witnesses.append(("O'->O", q, a, j))
    report("A.2 statement: all cross pairs have |A| <= 2 or |A| >= q-3 (q in 7,11,21,25, all a)",
           all_ok)
    # The historical draft's claim 'matching ... forces q <= 5' would mean NO
    # interior-y cross pair O'->O exists at any size for q >= 7.  The canonical
    # repaired proof retains the |A| = q-3 boundary witnesses exhibited here.
    n_wit = len([w for w in boundary_witnesses if w[0] == "O'->O"])
    report("A.2 repaired-proof check: |A| = q-3 cross pairs O'->O EXIST for q >= 7 "
           "(the historical draft's 'forces q <= 5' was wrong; the corrected proof "
           "retains this boundary, and the statement is unaffected)",
           n_wit > 0, f"{n_wit} witnesses at sizes q-3")
    # explicit q=7 example from hand derivation: A = {0,1,4,5} = AP diff 4, B = A u {6}
    q = 7
    A = frozenset({0, 1, 4, 5})
    okex = (A in set(ap_set(c, 4, 4, q) for c in range(q))
            and is_cyclic_interval(A | {6}, q) and not is_cyclic_interval(A, q))
    report("A.2 hand example q=7: ({0,1,4,5}, +{6}) is a strict O'->O cross pair at |A| = 4 = q-3",
           okex)


# ------------------------------------------------------ Lemma A.3 (local)


def check_A3():
    # (i) every 3-sign pattern with sum +1 has a bichromatic consecutive sub-pair
    ok = True
    for p in range(8):
        signs = [1 if (p >> i) & 1 else -1 for i in range(3)]
        if sum(signs) != 1:
            continue
        bich = (signs[0] != signs[1]) or (signs[1] != signs[2])
        if not bich:
            ok = False
    report("A.3(i) local: sum-1 triples always have a bichromatic consecutive pair", ok)
    # (ii) endpoint claims
    ok = True
    for p in range(8):
        signs = [1 if (p >> i) & 1 else -1 for i in range(3)]
        if sum(signs) == 1:      # f(T') = 1: need a plus endpoint
            if not (signs[0] == 1 or signs[2] == 1):
                ok = False
        if sum(signs) == -1:     # f(T') = -1: need a minus endpoint
            if not (signs[0] == -1 or signs[2] == -1):
                ok = False
    report("A.3(ii) local: majority-sign endpoint always exists", ok)
    # end-to-end (ii) for q = 9 over all balanced-normalized colorings and all
    # standard intervals S of size q-3 with f(S) in {0, 2}
    q, m = 9, 5
    ok = True
    from itertools import combinations
    for combo in combinations(range(q), m):
        plus = set(combo)

        def fval(X):
            return sum(1 if x in plus else -1 for x in X)

        for st in range(q):
            S = [(st + k) % q for k in range(q - 3)]
            fs = fval(S)
            if fs not in (0, 2):
                continue
            Tp = [(st + q - 3 + k) % q for k in range(3)]  # complement, in order
            want = 1 if fs == 0 else -1
            cand = [y for y in (Tp[0], Tp[2]) if (1 if y in plus else -1) == want]
            if not cand:
                ok = False
                continue
            y = cand[0]
            I2 = frozenset(S) | {y}
            if not is_cyclic_interval(I2, q) or fval(I2) != 1:
                ok = False
            for z in set(Tp) - {y}:
                I1 = I2 | {z}
                if not is_cyclic_interval(I1, q) or fval(I1) not in (0, 2):
                    ok = False
    report("A.3(ii) end-to-end at q=9: construction always yields a valid completion", ok)


# ------------------------- Theorem A merging clause: which composition works


def check_merge_composition():
    """Copies with relative map in D_q: identical families iff PREcomposition."""
    q = 11
    std = set(frozenset((st + k) % q for k in range(s)) for s in range(1, q) for st in range(q))

    def apply(pi, fam):
        return set(frozenset(pi[x] for x in S) for S in fam)

    import random
    rng = random.Random(5)
    pi = list(range(q))
    rng.shuffle(pi)
    rot = [(x + 1) % q for x in range(q)]         # delta: rotation, in D_q
    fam_pi = apply(pi, std)
    # precomposition pi o delta: same family
    pre = [pi[rot[x]] for x in range(q)]
    fam_pre = apply(pre, std)
    # postcomposition delta o pi: different family in general
    post = [rot[pi[x]] for x in range(q)]
    fam_post = apply(post, std)
    report("merge clause: pi o delta (delta in D_q) gives IDENTICAL interval family",
           fam_pre == fam_pi)
    report("merge clause: delta o pi generally gives a DIFFERENT family "
           "(so 'a_ij = +-1 => identical circles' needs pi_i^{-1} o pi_j, "
           "confirming the composition-order bug)",
           fam_post != fam_pi)


# ------------------------------------------- Theorem A hypothesis-order bug


def check_composition_bug_common_interval():
    """Literal hypothesis pi_j o pi_i^{-1} affine does NOT rule out middle-size
    common intervals: construct (pi, psi o pi), psi = x->2x mod 21, with a
    common size-3 set."""
    q, a = 21, 2
    ainv = pow(a, -1, q)
    S = {1, 4, 16}
    assert all((a * x) % q not in S for x in S)  # S and aS disjoint
    T = [0, 1, 2]          # standard interval
    T2 = [3, 4, 5]         # disjoint standard interval
    Sl = sorted(S)
    target2 = [(ainv * x) % q for x in Sl]
    pi = [None] * q
    for i, x in zip(T, Sl):
        pi[i] = x
    for i, x in zip(T2, target2):
        pi[i] = x
    used = set(x for x in pi if x is not None)
    rest = [x for x in range(q) if x not in used]
    j = 0
    for i in range(q):
        if pi[i] is None:
            pi[i] = rest[j]
            j += 1
    psi_pi = [(a * pi[i]) % q for i in range(q)]
    fam1_3 = set(frozenset(pi[(st + k) % q] for k in range(3)) for st in range(q))
    fam2_3 = set(frozenset(psi_pi[(st + k) % q] for k in range(3)) for st in range(q))
    common3 = fam1_3 & fam2_3
    report("composition bug: pair (pi, psi.pi), psi = x->2x mod 21 "
           "(satisfies discarded postcomposition hypothesis "
           "pi_2 o pi_1^{-1} affine) has a "
           "COMMON size-3 interval -- contradicts applying Lemma A.1 under that discarded hypothesis",
           frozenset(S) in common3, f"common size-3 sets: {[sorted(c) for c in common3]}")


# ------------------------------------------- Theorem E Step 1 (hull lemma)


def check_E_step1():
    ok_unique = True
    ok_nested = True
    tight_unique = None
    tight_nested = None
    for q in (11, 13):
        for d in (1, 2):
            jmax = q - 2 * d - 1
            for bits in range(1, 1 << q):
                S = frozenset(x for x in range(q) if (bits >> x) & 1)
                j = len(S)
                if j == q:
                    continue
                dS, hulls = defect_and_hulls(S, q)
                if dS <= d and j <= jmax and len(hulls) > 1:
                    ok_unique = False
                    print("  E.1 uniqueness VIOLATION", q, d, sorted(S))
                if dS <= d and j == q - 2 * d and len(hulls) > 1 and tight_unique is None:
                    tight_unique = (q, d, sorted(S))
            # nestedness over all (S, S+x)
            for bits in range(1, 1 << q):
                S = frozenset(x for x in range(q) if (bits >> x) & 1)
                j = len(S)
                if j + 1 > jmax:
                    # boundary probe |T| = q-2d
                    if j + 1 == q - 2 * d and tight_nested is None:
                        dS, hS = defect_and_hulls(S, q)
                        if dS <= d and len(hS) == 1:
                            for x in range(q):
                                if x in S:
                                    continue
                                T = S | {x}
                                dT, hT = defect_and_hulls(T, q)
                                if dT <= d and hT and not (hS[0] <= hT[0]):
                                    tight_nested = (q, d, sorted(S), x)
                                    break
                    continue
                dS, hS = defect_and_hulls(S, q)
                if dS > d or len(hS) != 1:
                    continue
                for x in range(q):
                    if x in S:
                        continue
                    T = S | {x}
                    dT, hT = defect_and_hulls(T, q)
                    if dT > d:
                        continue
                    if len(hT) != 1 or not (hS[0] <= hT[0]):
                        ok_nested = False
                        print("  E.1 nestedness VIOLATION", q, d, sorted(S), x)
    report("E Step 1 uniqueness: def<=d, |S| <= q-2d-1 => unique largest gap "
           "(q in 11,13; d in 1,2; all subsets)", ok_unique)
    report("E Step 1 nestedness: hull(S) subset hull(T) for |T| <= q-2d-1 "
           "(all subset pairs)", ok_nested)
    report("E Step 1 sharpness: at |S| = q-2d the largest gap can be non-unique "
           "(bound is tight; expected)", tight_unique is not None,
           str(tight_unique))
    report("E Step 1 sharpness: at |T| = q-2d nestedness can fail (expected)",
           tight_nested is not None, str(tight_nested))


# --------------------------------------- Theorem E section 2 (pairswap defect)


def check_E_pairswap():
    ok = True
    attained = True
    for q in (13, 21, 29, 37):
        perm = list(range(q))
        for i in range(0, q - 1, 2):
            perm[i], perm[i + 1] = perm[i + 1], perm[i]
        mx = 0
        for st in range(q):
            for L in range(1, q + 1):
                S = frozenset(perm[(st + k) % q] for k in range(L))
                dS, _ = defect_and_hulls(S, q)
                mx = max(mx, dS)
                if dS > 2:
                    ok = False
                    print("  pairswap defect VIOLATION", q, st, L, sorted(S), dS)
        if mx != 2:
            attained = False
    report("E section 2: pairswap circle is 2-dense (def <= 2 for all position "
           "intervals, q in 13,21,29,37)", ok)
    report("E section 2: bound 2 attained at every tested q", attained)


if __name__ == "__main__":
    check_A1()
    check_A2()
    check_A3()
    check_merge_composition()
    check_composition_bug_common_interval()
    check_E_step1()
    check_E_pairswap()
    print()
    if FAIL:
        print(f"{len(FAIL)} CHECK(S) FAILED")
        raise SystemExit(1)
    print("all lemma-level audit checks completed")

"""Independent hostile attack on Theorem A (repaired precomposition version).

Claim under attack: P = (pi_1..pi_t), every precomposition relative map
pi_i^{-1} o pi_j (i != j) affine on Z_q with multiplier not in {+1,-1}
==> G(P) = 0 (no hybrid-only colorings).

By relabeling invariance G(P) = G(id, rho_2, ..., rho_t) with rho_j = pi_1^{-1} pi_j
affine; pairwise ratios also constrained. t=2 case: rho = (a,b), a unit, a not +-1.

Attack: for each n in {22, 24, 26}: enumerate ALL such affine rho; candidates =
words rejected by BOTH copies; union-walk check each candidate. Any acceptance
is a counterexample.
"""
import sys, json
from math import gcd
from itertools import combinations
from audit_ref import (intervals_by_len, union_accepts_walk, single_accepts_fast,
                       popcount, count_single_rejects)

def affine_perm(a, b, q):
    return [ (a*x + b) % q for x in range(q) ]

def compose_word(w, perm, q):
    """(w o perm)(x) = w(perm(x)): bit x of result = bit perm[x] of w."""
    r = 0
    for x in range(q):
        if (w >> perm[x]) & 1:
            r |= 1 << x
    return r

def attack_n(n, rejset=None, do_triples=True):
    q = n - 1
    m = n // 2
    if rejset is None:
        rej = count_single_rejects(n, verbose=True)
    else:
        rej = rejset
    R = set(rej)
    units = [a for a in range(2, q-1) if gcd(a, q) == 1]  # excludes 1 and q-1 == -1
    idc = intervals_by_len(list(range(q)), q)
    total_cand = 0
    counterexamples = []
    pair_count = 0
    for a in units:
        for b in range(q):
            perm = affine_perm(a, b, q)
            # copy 2 = perm(RR) rejects w  iff  RR rejects w o perm
            cands = [w for w in R if compose_word(w, perm, q) in R]
            pair_count += 1
            if not cands:
                continue
            circ2 = intervals_by_len(perm, q)
            for w in cands:
                total_cand += 1
                if union_accepts_walk(w, [idc, circ2], q):
                    counterexamples.append((n, a, b, w))
                    print(f"COUNTEREXAMPLE n={n} a={a} b={b} w={w}")
    print(f"n={n}: affine maps tested={pair_count}, common-reject candidates={total_cand}, "
          f"counterexamples={len(counterexamples)}")
    # sanity: verify candidate filter direction on a few cases by direct walk
    import random
    rng = random.Random(7)
    checked = 0
    for a in units[:3]:
        for b in (0, 1, 5):
            perm = affine_perm(a, b, q)
            circ2 = intervals_by_len(perm, q)
            for w in list(R)[:4]:
                direct = union_accepts_walk(w, [circ2], q)     # copy-2 only acceptance
                indirect = single_accepts_fast(compose_word(w, perm, q), q)
                assert direct == indirect, (n,a,b,w)
                checked += 1
    print(f"  candidate-direction sanity checks passed: {checked}")
    # t = 3 spot checks: all pairs of distinct affine maps (a2,b2),(a3,b3) with
    # a2,a3, a2^-1 a3 all not +-1 would be huge; sample systematically over b=0..2
    if do_triples:
        trip_cand = 0; trip_ce = 0; trips = 0
        for a2 in units:
            for a3 in units:
                r = (a3 * pow(a2, -1, q)) % q
                if r in (1, q-1):
                    continue
                for b2 in (0, 3):
                    for b3 in (0, 5):
                        p2 = affine_perm(a2, b2, q); p3 = affine_perm(a3, b3, q)
                        cands = [w for w in R
                                 if compose_word(w, p2, q) in R and compose_word(w, p3, q) in R]
                        trips += 1
                        if not cands: continue
                        c2 = intervals_by_len(p2, q); c3 = intervals_by_len(p3, q)
                        for w in cands:
                            trip_cand += 1
                            if union_accepts_walk(w, [idc, c2, c3], q):
                                trip_ce += 1
                                print(f"TRIPLE COUNTEREXAMPLE n={n} {(a2,b2,a3,b3,w)}")
        print(f"  t=3 sampled: triples={trips}, candidates={trip_cand}, counterexamples={trip_ce}")
    return counterexamples

if __name__ == "__main__":
    ns = [int(x) for x in sys.argv[1:]] or [22]
    for n in ns:
        if n == 22:
            rej = json.load(open('rej22.json'))
        else:
            rej = None
        attack_n(n, rejset=rej, do_triples=(n == 22))

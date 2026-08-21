"""Cycle 5 audit: standalone verification of the Theorem A literal-hypothesis
counterexample found by cycle05_audit_thm_pipeline.exe --conj.

P = (pi_1, pi_2) with pi_1 = pi, pi_2 = psi o pi, psi(x) = 2x mod 23.
Then pi_2 o pi_1^{-1} = psi is affine with multiplier 2 (not +-1), both copies
fix infinity, t = 2 -- ALL hypotheses of Theorem A as stated hold.  Yet the
normalized balanced coloring f below is rejected by both copies and accepted
by the literal union: G(P) > 0.

This script re-verifies the claim with the PROPOSER's own literal reference
(brute_accepts over the induced-subset DAG), i.e. the second side of a
differential test whose first side is the auditor's independent C++ DP.

Run:  python -B experiments/cycle05_audit_thm_a_counterexample.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cycle05_hybrid_core import brute_accepts, union_family_masks  # noqa: E402

CASES = [
    # (n, a, pi, hybrid-only colorings f for P = (pi, psi o pi))
    (24, 2,
     [5, 17, 9, 19, 22, 13, 8, 14, 20, 4, 7, 12, 18, 2, 10, 11, 0, 6, 15, 16, 21, 3, 1],
     [0x2793AA, 0x27D2AA]),
    (22, 2,
     [7, 13, 17, 0, 20, 2, 12, 8, 3, 9, 5, 14, 11, 18, 6, 16, 10, 4, 1, 19, 15],
     [0xAE2B3]),
]

CASE = int(sys.argv[1]) if len(sys.argv) > 1 else 0
N, A, PI, F_WORDS = CASES[CASE]
Q = N - 1

pi1 = PI + [Q]                       # infinity-fixing
pi2 = [(A * x) % Q for x in PI] + [Q]

# hypothesis check: pi_2 o pi_1^{-1} affine (multiplier A, offset 0)
inv1 = [0] * N
for i, v in enumerate(pi1):
    inv1[v] = i
rel = [pi2[inv1[y]] for y in range(Q)]
assert rel == [(A * y) % Q for y in range(Q)], "hypothesis broken"
print(f"hypothesis: pi_2 o pi_1^(-1) = x -> {A}x mod {Q} (affine, a not +-1): HOLDS")
print("both copies infinity-fixing: HOLDS")

fam1 = union_family_masks(N, [pi1])
fam2 = union_family_masks(N, [pi2])
famU = union_family_masks(N, [pi1, pi2])

ok = True
for f in F_WORDS:
    assert bin(f).count("1") == N // 2, "not balanced-normalized"
    a1 = brute_accepts(fam1, f, N)
    a2 = brute_accepts(fam2, f, N)
    au = brute_accepts(famU, f, N)
    print(f"f = {f:#x}: copy1 accepts={a1}, copy2 accepts={a2}, union accepts={au}")
    if not (a1 is False and a2 is False and au is True):
        ok = False

# the repaired hypothesis pi_1^{-1} o pi_2 affine does NOT hold for this pair
tau = [inv1[pi2[x]] for x in range(Q)]
diffs = {(tau[(x + 1) % Q] - tau[x]) % Q for x in range(Q)}
print(f"repaired-hypothesis check: pi_1^(-1) o pi_2 has step set {sorted(diffs)} "
      f"-> {'affine' if len(diffs) == 1 else 'NOT affine'} "
      "(so the repaired theorem does not cover this pair; consistent)")

print("COUNTEREXAMPLE CONFIRMED by proposer-reference brute_accepts"
      if ok else "verification FAILED")
sys.exit(0 if ok else 1)

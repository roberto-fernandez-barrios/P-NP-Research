# Research State

## Current phase

RESEARCH CYCLE 5 FINALIZED — hybrid multi-order RR routing resolved under
S5-D (with an S5-F proof candidate); RR retired as the primary O01 route

## Current objective

Preserve the completed Cycle-5 disposition.  Do not begin Research Cycle 6
without explicit authorization.

## Primary target and status

**O01 — Polynomial-size 1-balanced-chain set systems.**  For every positive
even `n`, determine whether an absolute constant `C` satisfies
`N(n) <= n^C`.

O01 remains **OPEN**.  The audited public range is
`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}` (both bounds FLSY; the
withdrawn TR26-043 polynomial claim remains withdrawn as of 2026-08-21).
No Cycle-5 result changes that status: every Cycle-5 theorem is an
obstruction to restricted multi-RR construction routes, not a bound on
`N(n)`.

## Cycle-5 stopping result

The primary question — can literal unions of relabelled `RR_n` copies
accept dramatically more than their constituents through hybrid paths that
switch copies mid-chain — was answered exactly in both directions.

**Hybridity exists (5C diagnostic, positive).**  Smallest possible case
`n = 22` (provably minimal); a single transposition of two finite points
suffices; minimum switch count is exactly 1 in every verified example.
122 distinct certificates at `n = 22`; at `n = 24`, 14,864 verified stored
records represent 8,258 distinct `(permutation, word)` examples, with 6,606
duplicate records arising exactly from `swap`/`xswap` route labels.  Every
one of the 414 single-copy failure words is rescued by some pair.  A probe
also shows the phenomenon for relabelings that move the infinity point.
Everything is double-verified (fast engine with checked witness chains;
independent reference-only checker), and every stored witness has minimum
switch count exactly 1.

**Hybridity does not scale (obstructions).**  With `q = n-1` and the
interval-walk semantics (Lemma 5A.1, machine-cross-checked):

* **Theorem A (unconditional).**  Lists that are global relabelings of
  affine families — every precomposition relative map `π_i^{-1}∘π_j`
  affine with multiplier `∉ {±1}` — have hybrid gain exactly zero:
  `G(P) = 0`.  Structurally explains Cycle 4's zero hybrid-only accepts.
  The adversarial audit FALSIFIED the original postcomposition phrasing
  (`π_j∘π_i^{-1}` affine) with verified counterexamples at `n = 22, 24`
  (a conjugation subtlety); the repaired hypothesis is the one the proof
  uses.  Verdicts: original UNSOUND AS STATED; repaired statement
  independently reconstructed and cross-model validated SOUND AS STATED
  (`audits/cycle05_sol_final_cross_model_validation.md`).
* **Theorem E (unconditional, t-independent).**  If every copy's circle is
  `D`-dense for an integer `D >= 0` (each interval within `D` hull-holes of
  one common reference circle) and `6D + 8 < (n-2)^{1/5}`, then
  `H(P) ≤ (n/2)·2^{-c(n-2)^{1/5}}` for ANY number of copies.  Proof: hull
  chains + stepwise refinement + Cycle-4 rooted complement reduction +
  published FLSY Theorem 4.4 at the integer parameter `k = 5+3D <
  (n-2)^{1/5}`.  The common reference need not itself be a listed circle.
  This kills the strongest measured family (2-dense pair-swap circles:
  85.6–87.9% hybrid rescue on the
  exhaustive range `n = 24..34`, 69.7% at `n = 62` sampled, and a `t = 3`
  list rejecting only 3 of 20M colorings at `n = 28`,
  `certificates/cycle05_hybrid/triple_probe.json`) — all provably
  transient finite-`n` phenomena.
* **Lemma SEG and Theorems C/F (adversarially reviewed proof candidates;
  unformalized).**  SEG is a repository-derived segment version of the
  FLSY interval theorem (decay `2^{-cL^{1/5}}` in added length), not a
  theorem published verbatim by FLSY.  Its complete proof now incorporates
  the deep audit, arms-length R1--R5 repairs, and the final cross-model Sol
  corrections: integer first-passage rounding, the first-leg argument, the
  two-case tail arithmetic, the length-`L` full-cycle endpoint reduction,
  and `C=6`.  The cross-model verdict is SOUND WITH REPAIRS APPLIED.
  Theorems C and F retain an explicit dependency on SEG but are no longer
  labelled conditional on an unproved lemma.  Unions with middle switch
  depth `D` satisfy
  `H ≤ t·poly(q)·exp(-c'((q-7)/(D+1))^{1/5})` (Theorem C), and EVERY
  two-copy ∞-fixing union satisfies `H ≤ poly(n)·exp(-c''n^{1/25})`
  (Theorem F, via the run-sandwich lemma: short pure runs force chain
  density, long pure runs die by SEG).
* **Structure theory.**  `D_mid` values are machine-exact for `q ≤ 21`:
  multipliers 0 and transpositions/single block swaps at most 1.  The
  all-`q` transposition bound remains a proof candidate, used
  qualitatively.  For pair-swap, the all-`q` lower bound
  `D_mid >= (q-7)/2` is proved; equality is asserted only for the finite
  exact-DP range.  Common-interval descriptions are proved; the anchored
  transposition cross/switch-depth case analysis remains a proof candidate.
* **Measurements.**  Exhaustive `n ≤ 34` and sampled `n ≤ 62` scans: the
  hybrid rescue rate of every tested family decays (best transposition
  36.4% → 0.9%; pair-swap 87.9% → 69.7%; random and multiplier pairs
  exactly 0 everywhere).  By the verified FLSY Lemma 2.3 the positive
  target is only `H ≥ 1/poly` at `poly` copies; the theorems rule this
  out for every affine, every common-reference-dense, and, through the
  validated SEG dependency, every two-copy and every low-switch-depth
  family covered by C/F.

**Open boundary, stated exactly.**  (i) `t ≥ 3` ∞-fixing lists whose
circles are simultaneously at hull-defect `≥ n^{1/5}` from every common
reference AND of switch depth `≥ q/polylog(q)` — no such family is known;
the isolated Lemma M (run-sandwich stitching for `t ≥ 3`) would close
this.  (ii) Different-anchor/general infinity-moving lists (hybrid examples
exist; a common moved anchor globally reduces to the infinity-fixing case).
SEG is a complete, cross-model-adversarially reviewed repository proof
candidate and remains unformalized; it is not a published FLSY theorem.

Novelty status is conservative and records bounded-search outcomes, not
claims.  N1 (the affine AP/cyclic-interval lemma) is UNCLEAR; exact
Theorems A and E are narrowly POTENTIALLY NOVEL and require targeted
prior-art review; the aggregate switching framework N4 is UNCLEAR, with at
most its narrow quantitative `D_mid`/run-sandwich components potentially
novel.  N5, the literal union of relabelled set systems under full-chain
semantics, is KNOWN from FLSY Lemma 2.3.  Algaba--van den Brink--Dietz,
Example 4.7 (working paper), is prior art for the broad extra-chain-under-a-
union phenomenon.  Neither source subsumes the RR-specific theorems,
minimal threshold, certificates, or quantitative obstruction results.  No
Cycle-5 item has strong novelty support.

Status labels: Theorem A (repaired) `ADVERSARIALLY REVIEWED — SOUND AS
STATED`; Theorem E `ADVERSARIALLY REVIEWED — SOUND WITH APPLIED
CONCLUSION-PRESERVING REPAIRS`; SEG/C/F `ADVERSARIALLY REVIEWED PROOF
CANDIDATE; UNFORMALIZED` with explicit dependency arrows; hybrid minimality
`INDEPENDENTLY CONFIRMED AT n=22`; certificates
`INDEPENDENTLY VALIDATED WITH CORRECTED DISTINCT-COUNT WORDING`; and all
finite computations `EXHAUSTIVE/SAMPLED; INDEPENDENTLY CHECKED`.

**Stop-rule disposition.**  Cycle 5 ends under S5-D (broad restricted
obstruction classes) with the S5-F structure-theory candidate.  As
mandated: RR-family unions are retired as the primary O01 route.  A later
cycle should reassess the all-defect-router obligation from Cycle 3, O03,
O02, O18, and O05.  What would reopen the RR route: an externally validated
counterexample to SEG, or an explicit `t ≥ 3`/different-anchor family
escaping both density and switch-depth obstructions.

## Cycle-4 stopping result

(Verified again at the start of Cycle 5: both verifier suites PASS, both
SHA-256 manifests check, and the single-copy rejection counts at
`n ∈ {22,24}` were reproduced by a from-scratch reimplementation.)

The symmetrization implication is valid but its premise is false: for the
corrected `RR_n`, fixing a positive rank-one root and
complementing/reversing the nested cyclic intervals is an exact bijection
with 1-balanced maximal chains of the ordinary interval family on `n-2`
points, so `A_n <= (n/2) p_{n-2}` and FLSY Theorem 4.4 gives
`A_n <= (n/2) 2^{-c(n-2)^{1/5}} = exp(-Omega(n^{1/5}))`.  Individual-copy
acceptance and random-cover routes need `exp(Omega(n^{1/5}))` copies.
Status: `RIGOROUS COROLLARY; INDEPENDENTLY RECONSTRUCTED AND
FINITE-CHECKED; ADVERSARIALLY REVIEWED`.  Cycle 5 verified all four FLSY
imports verbatim against both primary versions.

Exact finite necklace counts (normalized rejections) for
`n = 22,24,...,34`: `21, 414, 4700, 40392, 292407, 1885203, 11191257`.
Full literal-union certificates prove `t_RR(n) = 2` for `n = 22..30` with
multiplier second copies and disjoint individual rejection sets — now
known (Theorem A) to be the only mechanism available to affine pairs.

## Cycle-3 stopping result

`N(10) = 35` (exact, exhaustively verified, independently adversarially
reviewed; falsifies `N(2m) = m(m+1)` at `n = 10`).  Level-cover vector
`tau(10,k) = 1,1,5,3,5,3,5,3,5,1,1` (sum 33); the exact-minimum lower
profile cannot reach all 252 signed balanced colorings; complementation
supplies the dual obstruction; a stored 35-subset family passes all 252.
Exact table: `N(2)=3, N(4)=6, N(6)=12, N(8)=20, N(10)=35` with
`L(n) = 3,6,12,19,33` and `sigma(n) = 0,0,0,1,2`.  Finite evidence only.

## Hardened foundation

Cycle 3 independently rechecked the consecutive-pair characterization, the
contracted-path functionality, the raw-count vs `N(n)` distinction, Lemmas
S1/S2, the `tau/L/sigma` definitions, and the CF-LOGGAP non-transfer
boundary.  A fixed maximal chain covers `2^{n/2}` signed balanced
colorings.  Cycle 5 additionally hardened the failure-list formats: the
`cycle04_rr_acceptance` failure files are binary-encoded, the
`cycle04_multi_rr` necklace files are hex; Cycle-5 parsers validate length
and weight (an early mis-parse was caught and the affected search rerun).

## Structural-class dispositions

All counts are distinct literal subsets.  Retained from Cycle 3 (details
in `results/research_cycle_03.md` and `failure_knowledge.jsonl`):

* CP-S/CP-SQ: no valid member for `n >= 10`; terminal-fanout candidate;
  conditional lift `R(X,D)` with exact size accounting; no polynomial
  router.
* CP-P: `h(T) = 2h(A)+2h(B)-4`; complete balanced trees fail at `n = 4`;
  full two-point insertion costs `4|X|`; sparse splice loses its invariant.
* CP-G: exact-minimum gluing fails first at `n = 8`; adjacent-interface
  local rule fails at `n = 4`; prefix-defect lemma forces dual surplus.
* CP-M: canonical-support bounds `Q(n) <= N(n) <= Q(n) + min(...)`;
  hybrid-path warning (RC3-CPM-01) — realized at scale by Cycle 5's
  hybrid-only certificates.
* `RR_n`: `(n-1)^2+2` subsets, valid for even `n <= 20`, fails from
  `n = 22` on; single-copy asymptotics dead (Cycle 4); multi-copy hybrid
  routing obstructed for the affine/dense/low-depth/two-copy classes by the
  cross-model-validated Cycle-5 proof candidates.

## Formal verification

Lean 4.32.1 with pinned mathlib accepts, without `sorry`/`axiom`/`admit`
(8,663 jobs in the clean Sol validation): balanced colorings and
1-balanced-chain definitions;
insertion-order chains and prefix lemmas; the consecutive-pair
characterization (both directions); the contracted-path reformulation;
Lemmas S1 and S2; the Cycle-4 relabeling/equivariance and literal-union
layer; and the new Cycle-5 multi-copy layer (`labelSet`, `ChainPure`,
`AcceptsPure`, `HybridOnly`, `SwitchBound`,
`switchBound_zero_iff_chainPure`, `acceptsUnion_pure_or_hybridOnly`,
monotonicity and trivial-bound lemmas).  The literal `RR_n`, the
interval-walk reformulation, Theorems A/C/E/F, SEG, and all probability
statements remain UNFORMALIZED; the boundary is in `formal/coverage.md`.

## Literature status through 2026-08-26

FLSY is published at CCC 2026, LIPIcs 383, Article 22 (ECCC TR26-001 full
version).  Cycle 5 verified verbatim: Definition 1.2/1.4 (chain-balance,
`(eps,k)` systems), Definition 2.1 (`I_{n,m}`), Theorem 4.4 = 1.7
(= published 23/8, exponent `n^{1/5}`, `k < n^{1/5}`, even `n`), Lemma 2.3
= 1.5 (= published 14/6, size `O(sn/p)`).  Their upper bound
`n^{O(log n/log log n)}` is a randomized hierarchy, explicitly not a union
of interval orders (derandomization open — their stated open problem).
Their Lemma 2.3 nevertheless constructs the literal union of relabelled
copies of an arbitrary set system, so that object is known even though its
hybrid-chain structure is not analyzed there.  Algaba--van den
Brink--Dietz, working-paper Example 4.7, gives an earlier abstract example
in which a union of selected prefix chains contains an additional full
chain.  Their `Sigma_pi` lower bound never analyzes hybrid literal unions;
`I_{n,m}` for `1 < m < 2 ceil(lg n)` is untouched.  TR26-043 remains
withdrawn (no v3, no successor).  Common-interval literature: survey in
`research_cycle_05/common_interval_literature.md`.  The exact RR-specific
switch-depth and obstruction statements were not located, which supports
only the conservative statuses recorded above.

## Cycle-2 findings retained

CF-LOGGAP remains `ADVERSARIALLY REVIEWED; UNFORMALIZED; NOVELTY UNCLEAR`
for its frozen construction family only.  The TR26-043 true-filtration
failures, exact values through `n = 8`, and retry conditions remain
canonical in `results/research_cycle_02.md` and `research_cycle_02/`.
Cycle-1 barrier/dependency/counterexample records remain retained.

## Next action

Stop.  Do not begin Research Cycle 6 automatically.  A later cycle
requires fresh authorization and should NOT: retry inverse-polynomial
single-copy RR acceptance (rigorously false); retry affine multi-RR
hybridity (`G = 0`, Theorem A); retry common-reference-dense multi-RR
lists of any size (Theorem E); or re-measure two-copy or low-switch-depth
families expecting different asymptotics (Theorem F/C, with validated SEG
dependency).  The recommended reassessment order for a next cycle is the
all-defect-router
obligation from Cycle 3; O03; O02; O18; O05.  The isolated open statement
whose resolution would change the remaining infinity-fixing RR boundary is
Lemma M; an externally validated counterexample to SEG would also reopen
the two-copy/low-depth conclusions.

## Critical rule

Do not directly attempt P versus NP.  No Boolean or algebraic complexity
separation follows from any cycle so far.

## Canonical Cycle-5 artifacts

* `results/research_cycle_05.md`
* `research_cycle_05/README.md`
* `research_cycle_05/hybrid_definitions.md`
* `research_cycle_05/switch_structure_theory.md`
* `research_cycle_05/dense_circle_obstruction.md`
* `research_cycle_05/flsy_reconstruction.md`
* `research_cycle_05/common_interval_literature.md`
* `research_cycle_05/novelty_audit_theorems.md`
* `audits/cycle05_theorems_adversarial.md`
* `audits/cycle05_seg_lemma_adversarial.md`
* `audits/cycle05_seg_deep_independent_validation.md`
* `audits/cycle05_seg_arms_length_referee.md`
* `audits/cycle05_sol_final_cross_model_validation.md`
* `audits/cycle05_final_correction_integration.md`
* `audits/barriers/cycle05_hybrid_obstructions.md`
* `audits/cycle05_final_integration_adversarial.md`
* `certificates/cycle05_hybrid/`
* `experiments/cycle05_*.py`, `experiments/cycle05_union_scan.cpp`
* `formal/BalancedChain.lean`, `formal/coverage.md`
* `failure_knowledge.jsonl`

## Canonical Cycle-4 artifacts

* `results/research_cycle_04.md`
* `research_cycle_04/README.md`
* `research_cycle_04/symmetrization_independent.md`
* `research_cycle_04/rooted_interval_obstruction.md`
* `research_cycle_04/rr_probability_attack.md`
* `research_cycle_04/literature_novelty_audit.md`
* `research_cycle_04/cycle04_rr_exact_count.md`
* `research_cycle_04/cycle04_multi_rr.md`
* `research_cycle_04/lean_formalization.md`
* `audits/cycle04_rr_obstruction_adversarial.md`
* `audits/barriers/cycle04_rr_interval_obstruction.md`
* `audits/cycle04_final_integration_adversarial.md`
* `certificates/cycle04_rr_acceptance/`
* `certificates/cycle04_multi_rr/`

## Canonical Cycle-3 artifacts

* `results/research_cycle_03.md`
* `research_cycle_03/README.md`
* `research_cycle_03/foundation_independent_audit.md`
* `research_cycle_03/literature_novelty_audit.md`
* `research_cycle_03/exact_n10.md`
* `research_cycle_03/cp_s_recursion_attack.md`
* `research_cycle_03/cp_p_hierarchy_attack.md`
* `research_cycle_03/cp_g_gluing.md`
* `research_cycle_03/cp_m_matching_equivalence.md`
* `research_cycle_03/lean_formalization.md`
* `research_cycle_03/formal_adversarial_audit.md`
* `certificates/balanced_chain_n10/`
* `audits/cycle03_n10_structural_adversarial.md`
* `audits/cycle03_final_integration_adversarial.md`

## Canonical earlier-cycle artifacts

* `results/research_cycle_02.md`
* `research_cycle_02/`
* `results/research_cycle_01.md`
* `literature/known_results.md`
* `literature/barriers.md`
* `literature/dependency_graph.md`
* `literature/open_problems.md`

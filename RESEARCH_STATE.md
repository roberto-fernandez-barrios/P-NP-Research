# Research State

**BRANCH NOTE (cycle07-o18-fable).**  The Cycle-6 section below remains
**PROVISIONAL** (produced while the Cycle-5 theorems await independent
cross-model validation; depends on none of them).  Cycle 7 was
explicitly authorized on 2026-08-25, executed on this branch from base
`3918bd6`, and depends on no Cycle-5 result either.

## Current phase

RESEARCH CYCLE 7 COMPLETE — O18 attack executed under the two-gated
mandate.  **Stage V verdict: JC-SOUND-WITH-REPAIRS** (hostile
validation of Jiang–Cai arXiv:2607.10697v1; repaired frontier UNCHANGED
at randomized general 3-SAT `O(1.307031578^n)`, Unique-3-SAT
`O(1.306969598^n)`).  **Stage I outcome: stop rule S7-C** — the
recombination LP corner `(i_0, i_1, tau) = (0, 0.060043…, 0)` is
REALIZABLE by explicit uniquely satisfiable families (Theorem CR,
adversarially reviewed, repairs applied; machine-verified by two
independent implementations on 21 instances), so no valid constraint on
these three statistics can improve the certified value: the narrow
missing-inequality route is closed by construction, and the [JC26]
recombination is exactly optimal over its statistic system.  Certified
errata for the source chain (ECCC TR21-069 rev 1) were produced along
the way.  Cycle 5 remains quarantined pending independent cross-model
validation.

## Current objective

Preserve Cycle 7.  Do not begin Research Cycle 8 without explicit
authorization.  The recorded next-cycle candidate for the O18 line is
the "fourth estimate" route: verbatim import and coordinate expression
of Hertli-2014's 1C-Unique gain (arXiv:1311.2513), whose class contains
the corner family — plus the open sparse-instance (`m = O(n)`)
realizability question.  Independent cross-model validation of Cycle 5
remains outstanding.

## Cycle-7 result (2026-08-25 → 2026-08-26)

Full report: `results/research_cycle_07.md`.  Verdict document:
`audits/cycle07_jc_validation.md`.  Key facts:

* Stage V: sources frozen with SHA-256 (arXiv v1 + GitHub artifacts at
  commit `3e732e0`); authors' checker reproduces its transcript; an
  arms-length independent exact-rational checker replicates 89/90
  claims and finds F1 (Scheder's printed endgame constant `1/15218` is
  exactly false — true minimax `31273/475913718`; his rounded Theorem-6
  base survives); verbatim import ledgers: SS lifting layer CLEAN,
  Scheder layer transcription-exact with hypothesis-layer mismatches
  repaired and certified in exact rationals (R1 `ε_R` beyond the
  printed `ε ≤ 0.1` — all four Prop-C.12 claims certified at the exact
  operating point; R2 hidden `Thr ≤ 1/1150`; R3 source's `256/600`
  corrected to `64/600`; R4 TwoCC is Definition 31's closure set; R5
  fixed-strength packaging downgraded to the source-verbatim
  `w(n)` form with all `O(·)` claims surviving).  Frontier claim
  independently supported (HKZZ 1.306995 and Qin–Watanabe 1.306984 are
  Unique-only; no prior explicit general decimal below Hertli's
  1.30704).  All numeric layers above the change-of-measure identity
  exist only in the unrefereed ECCC revision (the refereed TheoretiCS
  version dropped k = 3) — now underwritten by this cycle's
  certifications.
* Stage I: Theorem CR — for `n ≥ n_0`, `m_1 ≤ n/10`, explicit uniquely
  satisfiable 3-CNFs (width-≤3 "pairs" and width-exactly-3 "triples"
  variants; the triples variant is the primary carrier, its closure
  being trivially `F̃ = F`) with statistics exactly `(0, m_1/n, 0)`,
  closure-TwoCC empty under both Definition-31 readings, forced
  canonical selection.  Realizability map: grid points
  `(0, t, 0)` for `t` up to `0.32` at the verified sizes; `(0, 0.06, 0)`
  exactly at `n ∈ {50, 100}`.  Corollary: the recombination LP value
  `γ* = 0.000068779380458836…` is exactly optimal over
  `(i_0, i_1, tau)`; improvements require new estimates or new
  statistics.  Hostile review verdict SOUND WITH REPAIRS; repairs
  R-A–R-E applied (δ-condition, δ-existence counting, girth bound
  replaced by the reviewer's certified `girth > 17` for
  `n > 96 + 51δ`, triangle-free pairs-uniqueness argument,
  reading-sensitivity caveat).
* Statuses: finite claims `MACHINE-VERIFIED BY TWO INDEPENDENT
  IMPLEMENTATIONS`; asymptotic arguments and CR-2 `ADVERSARIALLY
  REVIEWED — SOUND WITH REPAIRS (applied)`; everything `UNFORMALIZED`
  (no Lean layer this cycle); no novelty claims beyond audited search
  outcomes.
* Failure knowledge: RC7-O18-01 (missing-inequality route falsified by
  realizability), RC7-JC-01 (printed-constant trust; certified source
  errata), RC7-ENG-01 (construction/verification traps).

## Cycle-6 reassessment result (PROVISIONAL, 2026-08-25)

Mandate: compare, independently, the Cycle-3 all-defect-router
obligation, O03, O02, O18, and O05; select exactly one next target.
Full dossiers: `results/research_cycle_06_reassessment.md`; selection
audit: `audits/cycle06_target_selection.md`.

**Ranking:** 1. O18 (selected); 2. router obligation (reserve);
3. O05; 4. O03; 5. O02.

**Selected target (recommendation only; attack not begun).**  O18, two
stages: (V) independently validate the Jiang–Cai exact-rational PPSZ
certificate (arXiv:2607.10697, v1 2026-07-12; artifact repository
confirmed public); (I) add at least one new proved valid
inequality/statistic to the recombination LP and certify a randomized
general 3-SAT base strictly below `1.307031578` (or below Scheder's
`1.307031594` if validation fails).  Smallest plausible missing lemma:
one valid linear constraint on the normalized statistics
`(i_0, i_1, tau)` violated at the certified LP optimum
`(0, (A-P_reg)/(A+b_1), 0)`.  Stop rules S-A–S-D frozen in the audit.

**Router obligation clarified (all PROVISIONAL, single-implementation,
machine-checked, unformalized).**  With `R(n)` the minimum size of a
Cycle-3 one-sided 2-defect router: `R(2)=3`, `R(4)=7`, `R(6)=15`
(exact), `R(8) in [24,26]`, `R(10) in [41,50]`; exact per-level vectors
`rho` recorded.  Lemma R-SYM (the `-2` side is implied by the `+2`
side), Lemma R-PARITY (band walk characterization), Lemma R-DUAL
(complementation symmetry, `rho(n,k)=rho(n,n-k)`), Lemma W4-RESTRICT
(`R_{[-1,3]}(n) <= N(n+2)`), and Observation DR2O01 (granting Cycle-3
DEFECT-LIFT: DR-POLY implies O01, `N(n) = O(n^{c+1})` from
`R(n) <= n^c`).  Consequently the router obligation is a strengthening
of O01 — the entire gap is band narrowing from width 4 to width 2 — and
`R(n) > N(n)` at every computed size.  It is retained as the canonical
structural route to O01, to be reassessed after the Cycle-5 validation.

**O05 status update (derived observation, PROVISIONAL).**  Published
supercritical size–depth trade-offs (bracket formulas,
arXiv:2411.14268; truly supercritical trade-offs, arXiv:2411.14267;
both STOC 2025) block the canonical flatten-then-translate route to
Buss–Yolcu Question 3.2 (`BY-ROUTE-BLOCK`): strict effective simulation
must handle formulas whose small resolution refutations are necessarily
superpolynomially deep.

**Literature freshness (2026-08-25).**  TR26-043 remains flawed with no
successor; FLSY range for O01 unchanged; no independent validation or
improvement of Jiang–Cai found; no CP_2-space or quadratic-disperser
progress found; O03's operative gap is dispersion at entropy `o(n)`
versus the known `(1-c)n` (ITCS 2024).

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
122 certificates at `n = 22`, 14,864 at `n = 24` (where every one of the
414 single-copy failure words is rescued by some pair); a probe shows the
phenomenon also occurs for relabelings that move the infinity point.
Everything is double-verified (fast engine with checked witness chains;
independent reference-only checker).

**Hybridity does not scale (obstructions).**  With `q = n-1` and the
interval-walk semantics (Lemma 5A.1, machine-cross-checked):

* **Theorem A (unconditional).**  Lists that are global relabelings of
  affine families — every precomposition relative map `π_i^{-1}∘π_j`
  affine with multiplier `∉ {±1}` — have hybrid gain exactly zero:
  `G(P) = 0`.  Structurally explains Cycle 4's zero hybrid-only accepts.
  The adversarial audit FALSIFIED the original postcomposition phrasing
  (`π_j∘π_i^{-1}` affine) with verified counterexamples at `n = 22, 24`
  (a conjugation subtlety); the repaired hypothesis is the one the proof
  uses.  Verdicts: original UNSOUND AS STATED; repaired SOUND AFTER
  REPAIRS (`audits/cycle05_theorems_adversarial.md`).
* **Theorem E (unconditional, t-independent).**  If every copy's circle is
  `d`-dense (each interval within `d` hull-holes of one common reference
  circle) and `6d + 8 < (n-2)^{1/5}`, then
  `H(P) ≤ (n/2)·2^{-c(n-2)^{1/5}}` for ANY number of copies.  Proof: hull
  chains + stepwise refinement + Cycle-4 rooted complement reduction +
  published FLSY Theorem 4.4 at `k = 5+3d`.  Kills the strongest measured
  family (2-dense pair-swap circles: 85.7–87.9% hybrid rescue on the
  exhaustive range `n = 24..34`, 69.7% at `n = 62` sampled, and a `t = 3`
  list rejecting only 3 of 20M colorings at `n = 28`,
  `certificates/cycle05_hybrid/triple_probe.json`) — all provably
  transient finite-`n` phenomena.
* **Theorems C and F (conditional on Lemma SEG).**  SEG is a segment
  version of the FLSY interval theorem (decay `2^{-cL^{1/5}}` in added
  length), reconstructed from their own translation-invariant
  Fréchet-distance proof; status PROOF CANDIDATE; independent skeptic
  audit verdict SOUND WITH REPAIRS (all statement-level; endorsed form in
  `audits/cycle05_seg_lemma_adversarial.md` §7 covers exactly the use
  made here).  SEG is not a published theorem; the conditional labels
  stand.
  Granting SEG: unions with middle switch depth `D` satisfy
  `H ≤ t·poly(q)·exp(-c'((q-7)/(D+1))^{1/5})` (Theorem C), and EVERY
  two-copy ∞-fixing union satisfies `H ≤ poly(n)·exp(-c''n^{1/25})`
  (Theorem F, via the run-sandwich lemma: short pure runs force chain
  density, long pure runs die by SEG).
* **Structure theory.**  `D_mid` values, machine-exact for `q ≤ 21`:
  multipliers 0, transpositions/single block swaps ≤ 1 (the all-`q`
  transposition bound is a recorded proof candidate, used qualitatively),
  pair-swap `(q-7)/2` (matching optimal construction, all-`q` lower
  bound proved); exact common-interval and cross-pair characterizations
  for affine and transposition relative maps; cross-arrow profiles
  measured for every family.
* **Measurements.**  Exhaustive `n ≤ 34` and sampled `n ≤ 62` scans: the
  hybrid rescue rate of every tested family decays (best transposition
  36.4% → 0.9%; pair-swap 87.9% → 69.7%; random and multiplier pairs
  exactly 0 everywhere).  By the verified FLSY Lemma 2.3 the positive
  target is only `H ≥ 1/poly` at `poly` copies; the theorems rule this
  out for every affine, every common-reference-dense, and (conditionally)
  every two-copy and every low-switch-depth family.

**Open boundary, stated exactly.**  (i) `t ≥ 3` ∞-fixing lists whose
circles are simultaneously at hull-defect `≥ n^{1/5}` from every common
reference AND of switch depth `≥ q/polylog(q)` — no such family is known;
the isolated Lemma M (run-sandwich stitching for `t ≥ 3`) would close
this.  (ii) Relabelings moving the infinity point (hybrid examples exist;
no obstruction theorem covers them).  (iii) Lemma SEG itself remains a
reconstruction-level import, not a published theorem.

The switching-chain framework (label sets, cross pairs, switch depth,
hull defect) appears to be unstudied per the cited survey and the
dedicated novelty audit
(`research_cycle_05/novelty_audit_theorems.md`): theorem components
POTENTIALLY NOVEL (Lemma A.1 with an explicit folklore-risk caveat), the
multi-RR-union object of study NOVELTY STRONGLY SUPPORTED.  Recorded as
search outcomes, not claims.

Status labels: Theorem A (repaired) and Theorem E `ADVERSARIALLY
REVIEWED — SOUND AFTER REPAIRS` (`audits/cycle05_theorems_adversarial.md`;
Theorem E's repair cosmetic; its hull lemma verified exactly tight and its
pipeline conclusion checked exhaustively on every rescued coloring at
`n = 24, 26` with min-k `= 2` against the bound `10`); Theorems C/F
`CONDITIONAL (SEG — skeptic verdict SOUND WITH REPAIRS, statement-level)`;
all finite computations `EXHAUSTIVE/SAMPLED; INDEPENDENTLY CHECKED`.

**Stop-rule disposition.**  Cycle 5 ends under S5-D (broad restricted
obstruction classes) with the S5-F structure-theory candidate.  As
mandated: RR-family unions are retired as the primary O01 route.  A later
cycle should reassess the all-defect-router obligation from Cycle 3, O03,
O02, O18, and O05.  What would reopen the RR route: refuting SEG, or an
explicit `t ≥ 3`/∞-moving family escaping both density and switch-depth
obstructions.

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
  routing dead for affine/dense/low-depth/two-copy classes (Cycle 5,
  partly conditional).

## Formal verification

Lean 4.32.1 with pinned mathlib accepts, without `sorry`/`axiom`/`admit`
(8,656 jobs): balanced colorings and 1-balanced-chain definitions;
insertion-order chains and prefix lemmas; the consecutive-pair
characterization (both directions); the contracted-path reformulation;
Lemmas S1 and S2; the Cycle-4 relabeling/equivariance and literal-union
layer; and the new Cycle-5 multi-copy layer (`labelSet`, `ChainPure`,
`AcceptsPure`, `HybridOnly`, `SwitchBound`,
`switchBound_zero_iff_chainPure`, `acceptsUnion_pure_or_hybridOnly`,
monotonicity and trivial-bound lemmas).  The literal `RR_n`, the
interval-walk reformulation, Theorems A/C/E/F, SEG, and all probability
statements remain UNFORMALIZED; the boundary is in `formal/coverage.md`.

## Literature status through 2026-08-21

FLSY is published at CCC 2026, LIPIcs 383, Article 22 (ECCC TR26-001 full
version).  Cycle 5 verified verbatim: Definition 1.2/1.4 (chain-balance,
`(eps,k)` systems), Definition 2.1 (`I_{n,m}`), Theorem 4.4 = 1.7
(= published 23/8, exponent `n^{1/5}`, `k < n^{1/5}`, even `n`), Lemma 2.3
= 1.5 (= published 14/6, size `O(sn/p)`).  Their upper bound
`n^{O(log n/log log n)}` is a randomized hierarchy, explicitly not a union
of interval orders (derandomization open — their stated open problem);
their `Sigma_pi` lower bound never analyzes literal unions;
`I_{n,m}` for `1 < m < 2 ceil(lg n)` is untouched.  TR26-043 remains
withdrawn (no v3, no successor).  Common-interval literature: survey in
`research_cycle_05/common_interval_literature.md`; switching chains and
cross pairs across two orders: NOT FOUND.

## Cycle-2 findings retained

CF-LOGGAP remains `ADVERSARIALLY REVIEWED; UNFORMALIZED; NOVELTY UNCLEAR`
for its frozen construction family only.  The TR26-043 true-filtration
failures, exact values through `n = 8`, and retry conditions remain
canonical in `results/research_cycle_02.md` and `research_cycle_02/`.
Cycle-1 barrier/dependency/counterexample records remain retained.

## Next action

Stop.  Do not begin Research Cycle 8 automatically.  Recorded
candidates for a future cycle, in no committed order: (a) the O18
"fourth estimate" route — verbatim import of Hertli-2014's 1C-Unique
gain (arXiv:1311.2513) expressed in the recombination coordinates
(the corner family lies in that class; Scheder's TheoretiCS §1.4
explicitly flags combining approaches as open); (b) the sparse-instance
(`m = O(n)`) corner-realizability question; (c) the width-2
quasi-polynomial router question if O01 work resumes
(`results/research_cycle_06_reassessment.md` §2.10) — only after the
Cycle-5 cross-model validation resolves.  Do-not-retry list additions:
do not retry the O18 missing-inequality route on `(i_0, i_1, tau)`
(closed by Theorem CR); the Cycle-5 do-not-retry list remains in force
(no inverse-polynomial single-copy RR acceptance; no affine multi-RR
hybridity, common-reference-dense lists, or two-copy/low-switch-depth
asymptotics pending validation).  Isolated statements whose resolution
would change pictures: Lemma SEG and Lemma M (RR route); the D1
width-<3 critical-clause convention pin (O18 line, minor).

## Critical rule

Do not directly attempt P versus NP.  No Boolean or algebraic complexity
separation follows from any cycle so far.

## Canonical Cycle-7 artifacts

* `results/research_cycle_07.md`
* `audits/cycle07_jc_validation.md`
* `audits/cycle07_corner_theorem_review.md`
* `audits/cycle07_final_adversarial.md`
* `research_cycle_07/` (stageV_log, lp_reconstruction, import ledgers,
  novelty audit, stage1_semantics, corner_realizability, checkers/,
  frozen_sources/ with SHA-256 manifests)
* `experiments/cycle07_corner_family.py`
* `certificates/cycle07_corner/instances.json`
* `failure_knowledge.jsonl` entries RC7-O18-01, RC7-JC-01, RC7-ENG-01

## Canonical Cycle-6 artifacts (PROVISIONAL, this branch)

* `results/research_cycle_06_reassessment.md`
* `audits/cycle06_target_selection.md`
* `experiments/cycle06_defect_router_exact.py`
* `experiments/cycle06_router_ub_deep.py`
* `experiments/cycle06_band4_restrict_check.py`
* `certificates/cycle06_router/` (README plus two value certificates)
* `failure_knowledge.jsonl` entries RC6-DR-01 and RC6-O05-01

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

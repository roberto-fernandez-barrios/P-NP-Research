# Research Cycle 5: hybrid multi-order routing

**Base commit:** `745f2bdf8b6d1e472279da913245aa048b36112c`
**Branch:** finalized on `cycle05-finalized` (candidate originated on
`cycle05-fable`)
**Date:** 2026-08-21; finalized 2026-08-27
**Primary target:** O01 remains **OPEN**
**Stopping condition:** **S5-D** (rigorous obstructions for broad, precisely
defined multi-order construction classes) together with an **S5-F
candidate** (the switching-chain structure theory), and a completed
high-priority 5C diagnostic.  Per the stop rule, RR is no longer
recommended as the primary O01 route.

## 1. Outcome in one page

Cycle 5 answered its primary question in both directions.

**Hybridity is real.**  The literal union of two relabelled `RR_n` copies
can accept colorings that both constituent copies reject.  The smallest
possible case, `n = 22`, occurs (provably minimal: every relabelling of
`RR_n` accepts everything through `n = 20`); a single transposition of two
finite points suffices as relative permutation; one copy switch suffices.
There are 122 verified `n = 22` examples.  The `n = 24` artifact has 14,864
verified stored records representing 8,258 distinct `(permutation, word)`
examples; 6,606 records duplicate a find under `swap`/`xswap` labels.
Minimum switch count was independently recomputed as exactly 1 throughout,
and every one of the 414 `n = 24` single-copy failure words is rescued by
some two-copy union.  Examples with relabelings that move the infinity point
exist as well.

**Hybridity does not scale.**  Two unconditional obstruction theorems and
two SEG-dependent adversarially reviewed proof candidates, plus systematic
exact and sampled measurements:

* **Theorem A (unconditional; final repaired statement SOUND AS STATED).**
  If the list is a global relabeling of affine maps — i.e.
  every precomposition relative map `π_i^{-1}∘π_j` is affine with
  multiplier `∉ {±1}` — the hybrid gain is exactly zero: `G(P) = 0`, the
  union accepts iff some copy accepts.  This retroactively explains the
  Cycle-4 two-copy certificates (multiplier relabelings, zero hybrid-only
  accepts) as structural rather than accidental.  The audit FALSIFIED the
  cycle's original postcomposition phrasing (`π_j∘π_i^{-1}` affine) with
  verified counterexamples — a conjugation subtlety invisible to every
  scan (which all had `π_1 = id`); the repaired hypothesis is what the
  proof always used.
* **Theorem E (unconditional; adversarially reviewed SOUND WITH APPLIED
  REPAIRS).**  If all copies'
  circles are `D`-dense w.r.t. one common reference circle (every interval
  within `D` hull-holes), for an integer `D ≥ 0` with
  `6D + 8 < (n-2)^{1/5}`, then for ANY number
  of copies `t` — the bound is `t`-independent —

  `H(P) ≤ (n/2)·2^{-c(n-2)^{1/5}}`.

  This kills the empirically strongest family found (the adjacent
  pair-swap circle, which is 2-dense, rescued 85.6–87.9% of common rejects
  on the exhaustive range `n = 24..34` and still 69.7% at `n = 62`
  sampled), every bounded-displacement relabeling family, and every
  "local shuffle" derandomization candidate.
* **Lemma SEG and Theorems C and F (ADVERSARIALLY REVIEWED PROOF
  CANDIDATES; SOUND WITH APPLIED REPAIRS; UNFORMALIZED).**  SEG is a
  repository segment localization of
  the FLSY proof technique, not a theorem published verbatim by FLSY.  The
  deep reconstruction, arms-length referee, and final cross-model audit
  supplied and checked proof repairs R1–R5.  C and F retain an explicit
  dependency on SEG, but are no longer merely conditional on an allegedly
  unproved lemma.
  C: unions with middle switch depth `D`, `(q-7)/(D+1) ≥ polylog`, have
  stretched-exponentially small `H`.  F: for `t = 2` no hypothesis is
  needed at all — every two-copy ∞-fixing union has
  `H ≤ poly(n)·exp(-c n^{1/25})` — via the run-sandwich lemma (short pure
  runs force chain density; long pure runs die by SEG).

By the verified FLSY worst-to-average Lemma 2.3, resolving O01 through
multi-RR unions does not require full coverage, only
`H(P) ≥ n^{-O(1)}` at `poly(n)` copies.  The theorems and adversarially
reviewed proof candidates above rule this out for every affine, every
common-reference-dense, every two-copy, and every low-switch-depth family,
subject to the explicit SEG dependency for the last two classes.  The route
survives only for
`t ≥ 3` lists whose circles are simultaneously `≥ n^{1/5}`-far from every
common reference and of switch depth `≥ q/polylog(q)`; no structured
family with both properties was found (a precise open statement, Lemma M,
would close the gap).  Different-anchor, or otherwise non-reducible,
infinity-moving lists remain outside the obstruction proofs; a common moved
anchor globally relabels back to the ∞-fixing setting.  A caution from the
adversarial audit: conjugated-affine pairs `(π, ψ∘π)` — outside the repaired
Theorem A — do show finite-`n` hybrid-only colorings (verified at
`n = 22, 24`); like every ∞-fixing two-copy family they are addressed by
the SEG-dependent Theorem F proof candidate, but they show the finite
phenomenon is broader than the structured families scanned.

O01 itself remains open in both directions.  Nothing here bounds `N(n)`.

## 2. Phase 5A: exact hybridity definitions

`research_cycle_05/hybrid_definitions.md` fixes the provenance-invariant
framework: label sets `L(S) = {j : S ∈ π_j(RR_n)}`, copy-pure vs hybrid
chains, switch counts as the minimum number of adjacent label changes
(equivalently, one less than the minimum common-label block count),
acceptance quantities `A_j, I(P), H(P), G(P) = H - I ≥ 0`, and
the two switch mechanisms (common states; cross pairs `(A, A∪{y})`).
Lemma 5A.1 reduces union acceptance for ∞-fixing lists to a nested
interval-growth walk in `t` circles with sums pinned to 1 at odd sizes and
{0,2} at even sizes.  The reduction is proved and machine-cross-checked
against the literal induced-subset-DAG reference on every normalized
coloring for `n ∈ {8,10,12}` over randomized copy lists
(`experiments/cycle05_hybrid_core.py`, self-tests).

A consequence recorded there: since `I(P) ≤ t·A_n = t·exp(-Ω(n^{1/5}))`
(Cycle-4 obstruction, re-verified), any all-`n` polynomial multi-RR
theorem would need `H(P)` to come almost entirely from hybrid-only
colorings.

## 3. Phase 5B: two-copy intersections and literature

For ∞-fixing copies, rank-`k` members are `{∞} ∪ I` with `I` an interval
of one of the circles, so copy intersections are governed by common cyclic
intervals and cross pairs of the relative permutation.  The proved and
proof-candidate components in
`research_cycle_05/switch_structure_theory.md` are separated as follows:

* **Affine relative maps** (`x ↦ ax+b`, `a ∉ {±1}`): common intervals only
  at sizes `{0,1,q-1,q}`; cross pairs only at `|A| ≤ 2` or `|A| ≥ q-3`
  (Lemmas A.1–A.2, via adjacency counting in difference-`a` progressions).
* **Transpositions `(u,v)`**: the common-interval characterization is
  proved (intervals containing neither or both of `u, v`, plus four
  exceptional arcs).  The anchored cross structure and all-`q` bound
  `D_mid ≤ 1` remain a recorded case-analysis proof candidate; exact DP
  verifies the bound on the committed range `q ≤ 21`.
* **Pair-swap circle**: the explicit construction proves
  `D_mid ≥ (q-7)/2` for every odd `q`; exact DP proves equality for
  `q ∈ {13,17,21}`.  No all-`q` optimality theorem is claimed.

The independent literature survey
(`research_cycle_05/common_interval_literature.md`) verifies: linear
common intervals are classical (Uno–Yagiura 2000; strong interval trees /
PQ-trees, Bergeron–Chauve–de Montgolfier–Raffinot 2008; simple-permutation
density `e^{-2}`, Albert–Atkinson–Klazar 2003; Poisson(2) commons for
random pairs, Corteel–Louchard–Pemantle 2006); circular common intervals
have optimal algorithms and complement-closure (Heber–Mayr–Stoye 2011,
Lemma 8).  Broader feasible-word, arc-permutation, regular-system, and
antimatroid literature already studies alternative full chains, and an
explicit public working-paper extra-chain example shows that a union of permutation
prefix families can contain a full chain absent from the inputs.  Moreover,
FLSY Lemma 2.3 already forms literal unions of relabelled copies of an
arbitrary set system.  Those sources do not supply the exact
interval-specific `D_mid`, affine rigidity, or hull-transfer results, but
they rule out calling the broad hybrid/literal-union object new.

The original dedicated audit records 20 numbered query strings plus direct
source and catalog scans.  The expanded final cross-model search assigns:
Lemma A.1 `UNCLEAR` (high folklore risk); the repaired Theorem A and Theorem
E mechanisms narrowly `POTENTIALLY-NOVEL`; the aggregate switching
framework `UNCLEAR` (with the quantitative `D_mid` and run-sandwich pieces
at most potentially novel); the literal-union object `KNOWN` from FLSY
Lemma 2.3; and the RR-specific structural analysis at most
`POTENTIALLY-NOVEL`.  SEG localization is `UNCLEAR` as a novelty matter.
These are bounded-search classifications, not novelty claims; no strong
novelty label remains.

## 4. Phase 5C: smallest hybrid-only examples (the diagnostic)

Since `RR_n` is valid for all even `n ≤ 20` and relabeling preserves
acceptance of everything, both copies can only reject at `n ≥ 22`, making
`n = 22` the provable minimum.  There, the single rejected orbit is the
21 rotations of `1^8 0^5 1^3 0^5`.

Findings (all machine-verified twice: fast interval engine with
independently checked witness chains, then an independent checker that
rebuilds the literal families and runs reference DPs only —
`experiments/cycle05_verify_hybrid_certificates.py`):

* `n = 22`: 349 word-preserving structured moves tested; **122 hybrid-only
  examples** across 43 distinct relative permutations (66 from single
  transpositions).  Canonical minimal example: `π = (1 13)` (transposing
  one plus of the `1^8` run with one plus of the `1^3` run), coloring
  `0x1fe0e`; both copies reject; the union accepts; **minimum switches
  = 1** — as for every one of the 122 examples.
* Rescue is direction-selective: at `n = 22`, transposition distances
  `δ ≤ 8` rescue zero words and the rescuing distances are exactly
  `δ ∈ {9,10}`.  Far block swaps also rescue; arc reversals never
  produced a hybrid-only example at `n ∈ {22, 24}`.
* `n = 24`: 2,647 structured moves (now including cross-orbit moves that
  map one failure word to a different one): **14,864 verified stored
  records representing 8,258 distinct `(permutation, word)` examples**.
  Exactly 6,606 records repeat a find under `swap`/`xswap` labels.  There
  are 440 distinct permutations, independently recomputed minimum switch
  count is 1 for every record, and **all 414 failure words are rescued by
  at least one pair**.
* Infinity-moving relabelings: a 550-candidate probe at `n = 22`
  (transpose ∞ with a finite minus point, composed with a far finite
  transposition) found 32 hybrid-only examples under the literal
  reference semantics.  The phenomenon does not require fixing ∞.

Certificates: `certificates/cycle05_hybrid/hybrid_only_n22_candidates.json`
and `hybrid_only_n24_candidates.json`.  The committed search generator
reproduces raw finds, not the `n = 22` `min_switches` and `canonical`
fields; those fields were added by separately verified manual
postprocessing.  The `n = 24` artifact does not contain those annotation
fields (so it is not the same schema); its minimum-switch statement was
independently recomputed from the stored records.

## 5. Phase 5D: hybrid gain measurements

Tooling: `experiments/cycle05_union_scan.cpp` (exact bit-parallel
single-copy recurrence; two-copy union DP with precomputed cross/eq
arrows; exhaustive Gosper scans or samples), cross-validated per-word
against the Python engine and the literal reference.  All counters below
are exact for `mode=exhaustive`; `n ≥ 38` rows are 2·10^6-sample
estimates.  `common` = colorings rejected by both copies; `rescued` =
common rejects accepted by the union (the hybrid-only colorings).

**Transpositions `(0,δ)` (all δ up to conjugacy, exhaustive):**

| `n` | best δ | best rescued/common | aggregate rescue |
|---:|---:|---:|---:|
| 22 | 10 | 4/11 = 36.4% | 6.00% |
| 24 | 11 | 54/220 = 24.5% | 4.79% |
| 26 | 12 | 448/2504 = 17.9% | 3.90% |
| 28 | 13 | 2970/21394 = 13.9% | 3.24% |
| 30 | 14 | 16892/154891 = 10.9% | 2.71% |
| 32 | 15 | 87944/1000613 = 8.8% (selected δ only) | — |
| 34 | 16 | 425086/5979437 = 7.1% (selected δ only) | — |

At `n = 22`, distances `δ ≤ 8` rescue nothing and exactly
`δ ∈ {9,10}` rescue; across the full exhaustive scan, `δ ≤ 7`
rescues nothing at any tested `n`.  Sampled at `n = 38..62`, the best
transposition rescue falls 4.7% → 0.9%.

**Controls (exhaustive, n = 22..30):** all valid multiplier pairs and all
25 random-permutation pairs rescued **exactly 0** of their common rejects
(commons up to 2,179) — matching Theorem A and the empty mid-rank cross
structure of generic pairs.  Cross-arrow profiles (`--list-cross`) confirm
the structural trichotomy: multipliers and random pairs have no mid-rank
arrows at all; transpositions have Θ(1) anchored arrows per rank;
pair-swap has Θ(q).

**Pair-swap circle (2-dense, proved `D_mid ≥ (q-7)/2`; equality
finite-DP verified for `q ∈ {13,17,21}`):**

| `n` | common | rescued | rate |
|---:|---:|---:|---:|
| 24 | 14 | 12 | 85.7% |
| 26 | 360 | 316 | 87.8% |
| 28 | 4,709 | 4,138 | 87.9% |
| 30 | 44,692 | 39,044 | 87.4% |
| 32 | 350,053 | 302,988 | 86.6% |
| 34 | 2,413,835 | 2,065,656 | 85.6% |
| 38* | 9,983 | 8,317 | 83.3% |
| 42* | 19,971 | 16,185 | 81.0% |
| 46* | 34,625 | 27,177 | 78.5% |
| 50* | 54,751 | 41,597 | 76.0% |
| 54* | 79,898 | 58,768 | 73.6% |
| 58* | 111,653 | 80,301 | 71.9% |
| 62* | 148,726 | 103,716 | 69.7% |
| 64* | 169,982 | 117,043 | 68.9% |

(*sampled.)  The strongest family found; slowly decaying; unconditionally
dead asymptotically by Theorem E.

**Three copies (id, pair-swap, shifted pair-swap):** at `n = 28`
(exhaustive on the relevant sets) the triple union rejects only **3 of
20,058,300** normalized colorings: diversity shrinks the triple-common set
to 308 and hybrid routing rescues 305 of them (99.0%).  At `n = 42`
(sampled, fixed seed) the triple rescue is down to 95.0% and the diversity
advantage erodes (triple-common/pair-common rises from 6.5% to 31.8%).
Stored, scripted reproduction:
`experiments/cycle05_triple_probe.py` →
`certificates/cycle05_hybrid/triple_probe.json`.  Both
partners are 2-dense, so Theorem E covers this list too: excellent finite
performance, provably doomed scaling — the cycle's sharpest illustration
of the finite-vs-asymptotic trap.

## 6. Phase 5E: structured families

* **Affine/multiplier families:** exactly zero hybrid gain (Theorem A).
  With the multiplier's inverse `h = a^{-1}`, size-2 cross pairs exist iff
  `h ∈ {±2}`; nothing exists at sizes 3..q-4.  The Cycle-4 multipliers
  `2,2,2,4,5` succeeded purely by rejection-set disjointness.
* **Non-reproducible diagnostic — interpolating `revB` family.**  The
  uncommitted construction reversed each `B`-block, with `B = 2` giving
  pair-swap.  The recorded `q = 21` measurements were pair-swap `(7,2)`,
  `rev4` `(3,6)`, and block swaps `(1,·)` for `(D_mid, defect)`.  No
  committed generator defines/reproduces these `revB` measurements, so
  they are retained only as diagnostics and are not used as theorem
  evidence.
* **Non-reproducible diagnostics — bit-reversal / xor-block orders.**  The
  recorded `q = 21` values were `D_mid = 0` for bit reversal and `≤ 4`
  for the tested xor maps.  No committed driver reproduces these
  constructions or measurements; the qualitative comparison is not a
  canonical coverage claim.
* No tested family combines high defect with high switch depth; whether
  that combination is possible at all is exactly the Lemma-M question.

## 7. Phases 5F/5G: the positive route

No positive routing theorem was obtained, and the finite data plus
obstructions explain why every candidate tried must fail.  The
sharpened targets are recorded:

* **Relaxed H2′** (via verified FLSY Lemma 2.3): `poly(n)` copies with
  `H(P) ≥ n^{-O(1)}` would give `N(n) = poly(n)` and resolve O01 — full
  coverage is not needed.  All obstruction theorems above are stated
  against this weaker target as well.
* The remaining positive territory after the current proof candidates:
  `t ≥ 3` lists that are simultaneously non-dense and deep-switching,
  or different-anchor/general ∞-moving lists.  A common moved anchor is
  globally equivalent to the ∞-fixing setting.  Nothing in this cycle
  constructs an escaping list.

## 8. Phase 5H/5I: obstructions and the FLSY connection

`research_cycle_05/flsy_reconstruction.md` (verbatim-verified against
ECCC TR26-001 and the LIPIcs version): all four Cycle-4 imports match
exactly; the interval theorem's engine is an anti-concentration bound for
the discrete Fréchet distance of two independent walks (milestones +
first-passage lower tails; the `1/5` balances `exp(-Ω(d))` against
`exp(-Ω(n/d⁴))`); their quasi-polynomial upper bound is a
`log n / log log n`-depth randomized hierarchy explicitly *not* a union of
interval orders (derandomization open); their `Σ_π` multi-order lower
bound handles orders by rank subadditivity and never analyzes literal
unions; `𝓘_{n,m}` results exist only for `m = 1` (negative) and
`m = 2⌈lg n⌉` (positive) — the intermediate regime and the union-of-orders
question are untouched.  TR26-043 remains withdrawn; the public range
`Ω(n²) ≤ N(n) ≤ n^{O(log n/log log n)}` stands.

**Lemma SEG** (segment version, decay `2^{-cL^{1/5}}` in the added length,
`k < L^{1/5}`, `O(√N)` ambient factor): reconstructed from the FLSY proof;
status `ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED`.  The first
skeptic audit, deep independent reconstruction, arms-length referee, and
final cross-model audit returned **SOUND WITH APPLIED REPAIRS**.  The frozen
proof includes the exact quantifiers and the five proof repairs: the offset first
leg, tail arithmetic split, analytic integrality/rounding bounds, terminal
cyclic split, and final constant `C = 6`.  SEG is a repository-derived proof
from published FLSY machinery; it is not a theorem published verbatim by
FLSY, and its novelty status remains `UNCLEAR`.

Obstruction theorems: Theorem A (`switch_structure_theory.md` §2,
unconditional), Theorem E (`dense_circle_obstruction.md`, unconditional),
Theorem C (§5) and Theorem F (§5b) are `ADVERSARIALLY REVIEWED PROOF
CANDIDATES; SOUND WITH APPLIED REPAIRS; UNFORMALIZED` with explicit
dependency on SEG.  F's density
branch uses Theorem E and its long-run branch uses SEG.  The isolated open
Lemma M would extend F to every `poly(n)`-size ∞-fixing list.  The audit
chain is recorded in `audits/cycle05_theorems_adversarial.md`,
`audits/cycle05_seg_lemma_adversarial.md`,
`audits/cycle05_seg_deep_independent_validation.md`,
`audits/cycle05_seg_arms_length_referee.md`, and
`audits/cycle05_sol_final_cross_model_validation.md`.

None of this is a lower bound on `N(n)`; no claim about arbitrary
1-balanced-chain families is made.

## 9. Phase 5J: formalization

The pinned Lean 4.32.1 / mathlib development builds with no `sorry`,
`axiom`, or `admit` (8,663 jobs in the final cold build,
`formal/check.ps1` PASS).  Newly
formalized this cycle (multi-copy layer in `formal/BalancedChain.lean`):
`labelSet`, `ChainPure`, `AcceptsPure`, `HybridOnly`,
`chainContained_mono`, `acceptsPure_acceptsUnion` (pure acceptance
transfers to the union), `acceptsUnion_pure_or_hybridOnly` (the dichotomy),
`IsLabeling`, `SwitchBound`, `switchBound_zero_iff_chainPure` (zero
switches = copy-purity), and `chainContained_union_switchBound` (every
union chain admits a labeling with the trivial bound).  The literal `RR_n`
family, the interval-walk reformulation, Theorems A/E/C/F, SEG, and all
probability statements remain UNFORMALIZED; the exact boundary is in
`formal/coverage.md`.

## 10. Validation summary

* Cycle-4 dependency verification: both Cycle-4 verifier suites rerun and
  PASS (multi-RR certificates; RR acceptance certificates with recount
  through `n = 26`); both SHA-256 manifests check; single-copy rejection
  counts at `n ∈ {22, 24}` reproduced by a from-scratch Cycle-5
  implementation (21 and 414).
* New-code validation: brute-force literal reference vs fast engine on
  every normalized coloring at `n ∈ {8,10,12}` over randomized copy
  lists; witness chains re-checked element-wise; C++ scanner
  cross-validated per-word against the Python engine; all hybrid-only
  certificates verified by an independent checker using only reference
  DPs.
* A parsing hazard was found and fixed during the cycle: the
  `cycle04_rr_acceptance` failure lists are binary-encoded while the
  `cycle04_multi_rr` necklace lists are hex; the first (void) `n = 24`
  search run was discarded and rerun with strict weight/length validation.
* Adversarial audits: `audits/cycle05_theorems_adversarial.md` (Theorems
  A and E); the SEG chain
  `audits/cycle05_seg_lemma_adversarial.md`,
  `audits/cycle05_seg_deep_independent_validation.md`, and
  `audits/cycle05_seg_arms_length_referee.md`; and the repository/final
  checks `audits/cycle05_final_integration_adversarial.md` and
  `audits/cycle05_sol_final_cross_model_validation.md`.

## 11. Epistemic ledger

| Claim | Status |
|---|---|
| Hybrid-only two-copy examples exist; minimum `n = 22`; transposition relative permutation; 1 switch | EXHAUSTIVE FINITE COMPUTATION; INDEPENDENTLY CHECKED |
| Every `n = 24` failure word rescued by some pair | EXHAUSTIVE FINITE COMPUTATION; INDEPENDENTLY CHECKED |
| Interval-walk union semantics (Lemma 5A.1) | PROVED; MACHINE CROSS-CHECKED |
| Theorem A (relabelled-affine list ⟹ `G = 0`) | ADVERSARIALLY REVIEWED: original postcomposition statement FALSIFIED (counterexample stored); final repaired precomposition statement SOUND AS STATED |
| Theorem E (common-reference `D`-dense for integer `D` ⟹ stretched-exp `H`, any `t`) | ADVERSARIALLY REVIEWED: SOUND WITH APPLIED, CONCLUSION-PRESERVING REPAIRS (integer `D` used throughout; common reference normalized without assuming it is a listed circle; growing `k = 3D+5 < (n-2)^{1/5}` retained); hull lemma and finite pipeline checks pass |
| Lemma SEG | ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED; SOUND WITH APPLIED PROOF REPAIRS; not published verbatim |
| Theorems C, F | ADVERSARIALLY REVIEWED PROOF CANDIDATES; SOUND WITH APPLIED REPAIRS; UNFORMALIZED; explicit dependency on SEG retained |
| Lemma M (`t ≥ 3` stitching) | OPEN |
| Rescue-decay measurements | EXACT (`n ≤ 34`) / SAMPLED (`n ≥ 38`) |
| Novelty / prior art | N1 and aggregate N4 UNCLEAR; narrow N2/N3 POTENTIALLY-NOVEL; N5 literal-union object KNOWN via FLSY Lemma 2.3; RR-specific structural analysis at most POTENTIALLY-NOVEL; no strong novelty claim |
| O01 | OPEN |

## 12. Stop decision

Cycle 5 stops under **S5-D**.  The S5-F route, SEG, C, and F are recorded as
adversarially reviewed, unformalized proof candidates, sound with applied
repairs and with the dependency arrows retained.  Per the mandated stop
rule, the recommendation is to **retire
RR-family unions as the primary O01 route**.  What would reopen it:
refuting Lemma SEG under external review, or constructing a `t ≥ 3`
far-and-deep list (or a different-anchor/general ∞-moving list) escaping
both density and switch-depth obstructions.  A common moved anchor is already
covered by global relabeling.  Otherwise the next cycle
should reassess the all-defect-router obligation from Cycle 3, O03, O02,
O18, and O05.  Cycle 6 is not started automatically.

# Cycle-6 target selection audit: O18 — certified PPSZ improvement

**Decision date:** 2026-08-25
**Branch:** `cycle06-fable` (provisional)
**Selected target:** O18, and no other target.
**Current status of the target:** OPEN in the audited public literature
(re-verified against primary sources 2026-08-25).
**Work boundary:** reassessment and selection only.  No Stage-V/Stage-I
attack work has begun; beginning the attack cycle requires fresh
authorization.  Cycle-5 Theorems A/E/C/F and Lemma SEG remain quarantined
pending independent cross-model validation and are not used anywhere in
this selection.

## 1. Exact statement of the selected target

Two mandatory stages, in order.

**Stage V — independent validation (explicitly not novelty).**
Verify the Jiang–Cai claim [JC26]:

> The unchanged PPSZ algorithm, analyzed via Scheder's regular and
> irregular estimates expressed in common structural coordinates and
> recombined by an explicit linear-programming dual certificate checked
> in exact rational interval arithmetic, decides Unique-3-SAT in
> `O*(1.306969598^n)` and general 3-SAT in `O*(1.307031578^n)`
> randomized time.

Validation means: (a) the exact-rational certificate re-verifies under an
independently written checker; (b) the estimates imported from Scheder
are verified verbatim against the published source; (c) the LP dual
argument is re-derived independently.

**Stage I — the open increment (the actual target).**
Produce at least one *new, proved* valid inequality or structural
statistic on the recombination coordinates, and derive a certified
randomized general 3-SAT running-time base **strictly smaller** than the
Stage-V frontier (claimed `1.307031578`; Scheder's `1.307031594` if
[JC26] fails validation).  "Certified" means an exact-rational,
independently checkable certificate; floating-point optimization does
not count.  Replication alone is not novelty; the strict improvement is
the result.

## 2. What is known

Bound chain for randomized 3-SAT (bases, `O*` suppressed):

| Result | Unique-3-SAT | general 3-SAT | Status |
|---|---|---|---|
| PPSZ (Paturi–Pudlák–Saks–Zane, JACM 2005) | `1.30704` (exponent `2 ln 2 - 1`) | weaker | published |
| Hertli (arXiv:1103.2165) | — | unique bound holds in general | published |
| Scheder, *PPSZ is better than you think* (arXiv:2207.11071) | `1.306972377` | `1.307031594` | published (numbers as quoted by [JC26]; verbatim check is Stage V(b)) |
| Jiang–Cai [JC26] (arXiv:2607.10697, v1 2026-07-12) | `1.306969598` | `1.307031578` | **preprint, unvalidated** |

Deterministic 3-SAT (`O(1.32793^n)`, Liu ICALP 2018) is a separate
target (O17) and is unaffected by this selection.

Artifact chain (confirmed to exist 2026-08-25):
`github.com/jiangxioabai/A-Better-Analysis-For-PPSZ` with
`ppsz_certificate.json` (exact-rational parameters, root brackets,
version `2026-07-12-rational-v6`), `verify_ppsz_constants.py`
(Python 3 standard library, `fractions.Fraction`, series tails with
rational remainder bounds), and a verification transcript.

Attack surface (source reconnaissance this session; to be re-derived
verbatim in the attack cycle, and treated until then as
reconnaissance-level): the recombination is a linear program over three
normalized statistics `i_0 = |ID_0|/n`, `i_1 = |ID_1|/n`,
`tau = |TwoCC|/n`; the certified optimum sits at
`i_1 = (A - P_reg)/(A + b_1)`, `i_0 = tau = 0`; the dual constraints for
`i_0` and `tau` carry strictly positive slack margins (approximately
`0.00134` and `0.0139`).  A proved valid constraint violated at that
corner — for instance a lower bound forcing `i_0` or `tau` weight when
`i_1 > 0` on extremal instances — immediately moves the LP value and
strictly improves the certified base.

## 3. Why the target is genuinely unresolved

Evidence gathered 2026-08-25 (this session), extending the repository
audit of 2026-08-21:

* arXiv:2607.10697 has exactly one version (2026-07-12); no errata.
* Web searches for independent validation, replication, or improvement
  of the [JC26] bound found none; searches for any later randomized
  general 3-SAT bound below Scheder's found none.
* The Phase-0/Phase-1 record (`literature/drafts/proof_sat.md`,
  `literature/open_problems.md`) already separated
  randomized/deterministic and unique/general records to prevent
  terminology collisions; those separations were re-checked.
* Negative searches cannot prove that no one is working on this; the
  scoop risk is recorded in Section 10.

## 4. Comparison with the other four candidates

Full ten-point dossiers are in
[`../results/research_cycle_06_reassessment.md`](../results/research_cycle_06_reassessment.md).
Condensed decision matrix:

| Candidate | Verdict | Decisive facts |
|---|---|---|
| Cycle-3 all-defect-router obligation (DR-POLY) | reserve, rank 2 | Implies O01 (`DR2O01`), so not a smaller lemma; new exact values `R(4)=7 > N(4)=6`, `R(6)=15 > N(6)=12`, `R(8) >= 24 > 20`, `R(10) >= 41 > 35`; lift overhead `R(n)+2` is 1.5–2.1× the true marginal `N(n+2)-N(n)`; O01-adjacent work should wait for the Cycle-5 cross-model validation |
| O03 quadratic disperser | rank 4 | Required dispersion at entropy `o(n)` against `1.83n` quadratics vs state of the art `(1-c)n` (ITCS 2024); no engine fit; marginal numerical payoff |
| O02 `CP_2` space | rank 5 | `CT_n` has `2^n` clauses; iterated-log target invisible to any experiment; no falsification channel |
| O18 PPSZ | **selected** | Concrete smallest missing lemma (one valid inequality at an identified LP corner); public exact-rational artifact chain; perfect match to demonstrated engine capabilities; robust to the Cycle-5 validation outcome |
| O05 strict effective simulation | rank 3 | New connection found this cycle: bracket formulas (arXiv:2411.14268) block the canonical flatten-then-translate route (`BY-ROUTE-BLOCK`); positive direction needs an unknown gadget, negative direction needs lifting machinery |

## 5. Anti-continuity check (mandated)

The selection instruction forbids choosing a target merely to preserve
continuity with Cycles 1–5.  Checks:

1. O18 shares no mathematical objects, files, techniques, or
   dependencies with the O01/RR line (Cycles 1–5).  It belongs to
   Track D (SAT algorithms) of the mission, which has had no dedicated
   cycle yet.
2. The runner-up (the router obligation) is the continuity candidate;
   it was ranked second *despite* the engine's accumulated O01 capital,
   for the reasons in the decision matrix — the strongest of which
   (DR2O01: it *is* O01, strengthened) was established by this cycle's
   own analysis, not assumed.
3. The selection is also robust to the pending Cycle-5 validation: no
   outcome of that validation changes O18's statement, feasibility, or
   value; the same cannot be said of any O01-adjacent choice.
4. Capability continuity (exact-rational certificates, import
   discipline, adversarial audits) is intentional and is not target
   continuity.

## 6. Active search for reasons NOT to choose O18 (mandated)

Sought and recorded, with dispositions:

1. **Weakest lower-bound connection of all five (`C=2`).**  True.  A
   3-SAT base improvement implies no separation and feeds no barrier
   bypass.  Disposition: the mission's Phase-1 rule optimizes for the
   smallest genuinely-new, correct, checkable increment, explicitly not
   prestige; Track D is a sanctioned track; connection was scored
   honestly and O18 wins the product anyway.
2. **Microscopic magnitude.**  The [JC26] step over Scheder is
   `1.6e-8` in the general base; a Stage-I improvement may be of
   similar scale.  Disposition: accepted and stated openly; the value
   is the certified frontier plus the reusable exact-certificate
   methodology, and the mission's success ladder counts a genuinely
   improved restricted-case theorem (Level 4) regardless of magnitude.
3. **Unrefereed-preprint dependence.**  [JC26] may be wrong.
   Disposition: validation-first ordering makes this a feature: a
   documented flaw is itself a valuable validation result (the engine
   has produced exactly this kind of result before, for TR26-043), and
   the improvement target then reverts to Scheder's certified bound.
4. **Scheder-import weight.**  Verbatim verification of a long
   technical analysis may dominate the cycle.  Disposition: bounded by
   stop rule S-B; the FLSY-import discipline (twice executed) is the
   template.
5. **The LP corner may be realizable.**  If extremal instances actually
   approach `(0, i_1^*, 0)`, no valid inequality separates it and
   Stage I fails in its narrow form.  Disposition: the
   falsification-first plan tests exactly this before any proof effort;
   outcome S-C converts the cycle into a realizability map plus the
   Stage-V validation, both useful.
6. **Scoop risk.**  Fresh area, active authors.  Disposition: accepted;
   the validation component retains value regardless.
7. **"Is it even a lower-bound program's business?"**  The mission's
   operational objective is the strongest genuinely new, correct,
   independently checkable intermediate result across four tracks, of
   which SAT algorithms is one.  Disposition: in scope.

None of these, singly or jointly, overturns the comparison of Section 4.

## 7. Falsification-first plan (Phase 4 discipline)

Before proving anything:

1. Run the authors' checker on the frozen artifacts; then re-verify the
   certificate with an independently written exact-rational checker
   (independent series-tail bounds, no code reuse).  A failure here
   falsifies [JC26] (outcome S-A).
2. Enumerate critical-clause structures of small unique-3-SAT instances
   exhaustively (exact finite enumeration) and map the realizable
   region of `(i_0, i_1, tau)`.  Actively try to construct instance
   families approaching the LP corner `(0, i_1^*, 0)` — i.e. try to
   *refute* the hoped-for missing inequality before conjecturing it.
3. Any candidate inequality must survive: (a) the exhaustive small-`n`
   map; (b) randomized adversarial instance generation; (c) an
   attempted analytic counterexample family; only then does it become a
   Phase-3 candidate lemma with the full statement format.

## 8. Proof program and stop rules

Stage V: independent re-derivation of the recombination LP from
Scheder's estimates; verbatim import table (FLSY discipline); dual
certificate re-check; publish the validation verdict in
`audits/` with SOUND / SOUND WITH REPAIRS / UNSOUND labels.

Stage I: prove the surviving inequality combinatorially (expected shape:
a counting/structure lemma about critical clause trees and sibling
graphs on the extremal statistics); rerun the LP with the new constraint
in exact rationals; produce certificate v2; independent reimplementation
+ adversarial review + novelty audit + Lean check of the final rational
certificate.

Stop rules: **S-A** certificate fails validation → document the flaw,
report, stop.  **S-B** Scheder imports cannot be verbatim-verified
within the bounded budget → record the exact boundary, stop.  **S-C**
the LP corner is realizable / no valid inequality survives bounded
falsification → record the realizability map, stop.  **S-D** strict
certified improvement achieved → full validation chain, then stop.
Under every stop rule the cycle ends with a labelled, checkable
artifact.

## 9. Computational and Lean plan

* Computation: standard-library exact rational arithmetic
  (`fractions.Fraction`) as in the existing artifact chain; exhaustive
  small-instance enumeration engines in the style of
  `experiments/check_balanced_chain_n10_exact.py`; all certificates
  JSON-frozen with SHA-256 manifests as in Cycles 4–5.
* Lean: formalize the final certificate check (rational inequalities,
  series remainder bounds, LP duality verification) — a finite,
  self-contained core in the style of the existing
  `formal/BalancedChain.lean` layer; the probabilistic PPSZ semantics
  remain declared unformalized imports in `formal/coverage.md`.

## 10. Risk register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| [JC26] flawed | medium | Stage-I frontier moves to Scheder's bound | S-A produces a validation result either way |
| Scheder verbatim check exceeds budget | medium | cycle ends at S-B | bounded import table; FLSY template |
| LP corner realizable | medium | Stage I unachievable as framed | falsification-first (S-C) detects early |
| Scooped | low-medium | novelty lost, validation remains | fast bounded cycle; record dates |
| Hidden model mismatch (unique vs general, randomized vs deterministic) | low | wrong target claimed | Phase-0 separations already frozen; restate in every artifact |

## 11. Epistemic statuses and constraint compliance

* This audit and the selection are **PROVISIONAL** (branch-local) until
  the cycle is reviewed alongside the pending Cycle-5 cross-model
  validation.
* Nothing here depends on Cycle-5 Theorems A/E/C/F or Lemma SEG.
* O01 is not claimed and its status is unchanged; the router obligation
  remains OPEN with its relationship to O01 now made exact
  (`DR2O01`, `W4-RESTRICT`, finite values — all PROVISIONAL,
  single-implementation, listed in the reassessment document).
* No proof program has been started for O18; this document authorizes
  nothing by itself.
* The critical rule stands: no P-versus-NP attempt; no Boolean or
  algebraic separation follows from anything in this cycle.

# Research Cycle 7: O18 — hostile validation of Jiang–Cai and the realizability of their LP corner

**Cycle dates:** 2026-08-25 → 2026-08-26
**Branch:** `cycle07-o18-fable` (base `3918bd6`); `master`,
`cycle05-fable`, `cycle06-fable` untouched
**Authorization:** explicit (Cycle-7 mandate); Cycle 5 remains
quarantined — nothing in this cycle depends on Theorems A/E/C/F, SEG,
`RR_n`, or any other Cycle-5 result
**Stop rule reached:** **S7-C** (the LP corner is realizable; the
narrow missing-inequality route is closed by an explicit construction),
on top of a completed Stage V with verdict **JC-SOUND-WITH-REPAIRS**

## 0. Executive summary

Target O18 had two gated stages.

**Stage V (hostile validation of [JC26] = Jiang–Cai,
arXiv:2607.10697v1, "A Better Analysis For PPSZ For 3-SAT"):**
completed in full.  Verdict: **JC-SOUND-WITH-REPAIRS**, with the
repaired frontier UNCHANGED at the paper's claimed values — randomized
general 3-SAT in `O(1.307031578^n)`, Unique-3-SAT in
`O(1.306969598^n)`.  Every number of [JC26]'s NEW analysis
(recombination, dual certificate, lifting instantiation, all margins
and bases) replicates in exact rational arithmetic under two
independent checkers — 89/90 independent checks pass, the single
failure being the genuine finding F1 against a background display
inherited verbatim from Scheder (§1 item 7); every import from
Scheder's ECCC TR21-069 rev 1 and from Scheder–Steinberger's journal
version is transcription-exact; the repairs concern hypothesis ranges,
a definitional relabel, and a quantifier form — none moves a number.
Real defects were found and certified — mostly in the *source*
literature, not in [JC26]'s new mathematics (see §1, items 6–7).

**Stage I (the open increment — improve the certified base via a new
valid inequality on the recombination statistics):** the mandate's
falsification-first order was decisive.  Before conjecturing any
inequality we attempted to realize the LP corner — and succeeded:

> **Theorem CR (adversarially reviewed, repairs applied).**  For every
> `n ≥ n_0` and `0 ≤ m_1 ≤ n/10` there are uniquely satisfiable 3-CNF
> formulas (a width-≤3 and a width-exactly-3 variant) whose
> critical-clause structure has NO closure-TwoCC variables, NO
> indegree-0 variables, exactly `m_1` indegree-1 variables, and no
> canonical-selection freedom — statistics exactly
> `(i_0, i_1, tau) = (0, m_1/n, 0)`.

With `m_1 = round(i_1^* n)` this realizes the [JC26] LP optimum
`(0, 0.060043…, 0)` in the limit (exactly `i_1 = 0.06` at
`n ∈ {50, 100}`).  **Corollary: no valid constraint on
`(i_0, i_1, tau)` — linear or not, even jointly with `n` — can improve
the certified value `γ*`; the [JC26] recombination is exactly optimal
over its statistic system.**  Improving the `1.307031578` frontier
within Scheder's framework therefore requires new estimates or new
statistics, not a cleverer recombination — with a concrete next-cycle
candidate identified (a verbatim import of Hertli-2014's 1C-class
estimate, whose "1C-Unique" class contains the corner family).

No new frontier bound is claimed.  The cycle's product is (a) the
first arms-length validation on record of the current randomized
3-SAT frontier, with certified errata for its source chain, and (b) a
structural optimality/no-go theorem for its recombination.

## 1. Stage V — what was done and what it found

Full report: `audits/cycle07_jc_validation.md`; evidence log:
`research_cycle_07/stageV_log.md`.  Summary:

1. **Sources frozen** (SHA-256 manifests; GitHub artifacts pinned to
   commit `3e732e0`; arXiv v1 source + PDF + abs snapshot).  The paper
   and artifact repository are real; provenance defects recorded
   (certificate says `…-v5`, paper claims `…-v6`; `REVISION_NOTES.md`
   listed with a checksum but absent from the repo).
2. **Authors' checker**: inspected, executed — exit 0, transcript
   byte-identical to the frozen one.
3. **Independent exact-rational checker** (arms-length; the authors'
   code was never read by its author): 89/90 checks PASS with margins
   replicated to ≥17–65 significant digits; the one FAIL is a genuine
   finding (F1 below).
4. **Recombination LP re-derived from scratch**
   (`research_cycle_07/lp_reconstruction.md`): octant relaxation sound;
   dual certificate re-proved; **the optimum verified from first
   principles to be the unique corner `(0, 0.060043…, 0)` with zero
   duality gap and strictly positive dual slacks on `i_0` and `tau`**
   (subgradient optimality, not certificate trust).
5. **Verbatim import ledgers** against the frozen primary sources:
   * Scheder ECCC TR21-069 rev 1 (`scheder_import_ledger.md`, I1–I10):
     every display transcription-exact (all sixteen coefficient
     decimals, Eq. (11), Lemma 34, Definition 67, the endgame
     constants); the two estimates are unconditional and the source
     itself takes their max (simultaneity confirmed);
     hypothesis-layer mismatches → repairs R1–R4.
   * Scheder–Steinberger journal 2024 + Hertli + HKZZ
     (`ss_lifting_import_ledger.md`): **CLEAN** — Main Theorem 1.17,
     Lifting, and the finite-strength error `p_w = p0 + ε_w` verbatim
     (SS's printed 1.17 under-declares hypotheses its own proof uses;
     [JC26] add them — safe direction); [JC26]'s own lifting lemmas
     re-proved sound against SS's definitions.
6. **Repairs** (`checkers/repair_certifications.py`; adversarially
   reviewed — SOUND WITH CAVEATS; caveats C1/C2/C4 hardened into the
   script, C3 carried as an explicit dependency — see item 7 and the
   validation audit).  R1–R3, and R5's numeric slack, are certified in
   exact rationals; R4 is a definitional relabel; R5 is otherwise a
   statement-form repair:
   * **R1** [JC26]'s `ε_R = 0.10248` exceeds the source's printed
     `ε ≤ 0.1` hypothesis (Prop C.12), and the claimed range
     `[0, 0.13]` is FALSE near 0.13 (certified witness).  All four
     C.12 claims are certified TRUE at the exact operating point →
     the import is valid where used; range withdrawn.
   * **R2** hidden constraint `Thr ≤ 1/1150` (its own source margin is
     hairline, `4.0·10⁻⁷` — certified); [JC26] comply.
   * **R3** the source's `ε ≤ 256/600` rests on a false bound (true:
     `64/600`); [JC26]'s `ε_I = 0.0731` complies with the corrected
     constraint; their Lemma A.1 calculus certified.
   * **R4** [JC26]'s printed TwoCC definition omits the source's
     closure (`F̃`, Definition 31); usage is opaque/consistent — a
     relabel, but material for Stage I semantics.
   * **R5** the fixed-strength packaging of the imported estimates is
     [JC26]'s own; the source proves only the `w(n)`-slowly-growing
     form.  Repaired by re-running the chain in the source-verbatim
     packaging: all headline `O(·)` running times survive because the
     outward-rounded bases carry certified slack that absorbs
     `2^{o(n)}`; only the literal "∃ fixed w₀" quantifier is
     downgraded.
7. **Findings against the source literature** (certified errata
   candidates for ECCC TR21-069 rev 1; none overturns its Theorem 6):
   **F1** the end-of-§6 endgame constant `1/15218` is exactly false
   (true minimax `31273/475913718 ≈ 1/15218.04`; wrong-direction
   rounding; the valid clean bound is `1/15219`); the printed
   `JUNK₂ ≤ 0.000184` is false; `10r²(1−2r)² ≤ 10/256` is false;
   the `s′ ≤ 1.05 provided ε ≤ 0.13` claim is false at 0.13; several
   load-bearing constants survive by only `10⁻⁷`-scale margins (all
   now certified); one §7.7 recon discrepancy remains unreconciled and
   is covered 33.5× by a certified robustness envelope (and `γ*` does
   not depend on the affected coefficient at all).
8. **Publication-status finding:** every k = 3 numeric import lives
   ONLY in the unrefereed ECCC revision — the refereed TheoretiCS 2024
   version deliberately dropped the whole k = 3 part (its own words:
   a simple tightening "would already yield a better bound") and only
   the change-of-measure identity is refereed.  This cycle's
   certifications now independently underwrite the hairline constants.
9. **Novelty/frontier audit** (`novelty_frontier_audit.md`): [JC26]'s
   "best currently known" claim SUPPORTED — HKZZ's 1.306995 and
   Qin–Watanabe's 1.306984 are Unique-3-SAT figures; no general-3-SAT
   decimal below Hertli's 1.30704 exists anywhere before [JC26]; no
   follow-ups, no v2, zero citations, no community uptake; this cycle
   is the first arms-length check on record.

**Verdict: JC-SOUND-WITH-REPAIRS; repaired frontier = 1.307031578
(general), 1.306969598 (unique); Stage I gate: OPEN.**

## 2. Stage I — the corner is realizable (S7-C)

Full statement and proofs: `research_cycle_07/corner_realizability.md`
(with `stage1_semantics.md` for the from-first-principles semantics);
hostile review: `audits/cycle07_corner_theorem_review.md` (verdict
SOUND WITH REPAIRS; all repairs applied); engine:
`experiments/cycle07_corner_family.py`; data:
`certificates/cycle07_corner/instances.json`.

* **Construction.**  Critical clauses `(x ∨ ¬(x+1) ∨ ¬g(x))` with `g`
  a jump-window function (`jumps ∈ [⌊n/3⌋+1, ⌊(n−3)/2⌋]`) redirecting
  `m_1` spread-out specials (`g(s_i) = q_i`), plus all-positive
  "killer" clauses on CCG-non-adjacent pairs (width-≤3 variant) or
  pairwise-non-adjacent triples (width-exactly-3 variant, the primary
  carrier — its closure is trivially `F̃ = F` under every reading of
  Definition 31).
* **Why it works.**  Unique satisfiability ⟺ no nonempty "closed"
  zero-set: singletons die on their own critical clause; larger sets
  must be cliques of the (triangle-free) adjacency graph — impossible
  beyond 2-cycles, which the jump arithmetic excludes (pairs variant);
  or contain a directed cycle of length > 17 and hence an independent
  triple (triples variant).  The closure adds no critical clause: aux
  clauses have no negative literals, so all their resolvents keep ≥ 2
  positive literals, and critical×critical overlaps are excluded by
  the jump arithmetic.  Degrees are exact by construction.
* **Verification.**  21/21 instances (`n = 26…120`, both variants,
  search-mode and explicit-mode constructions) pass V1–V6: exactly one
  critical clause per variable in `F̃` under BOTH Definition-31
  readings (TwoCC = ∅, forced selection), uniqueness by complete DPLL,
  exact degree profiles.  Independently replicated by the hostile
  reviewer with different methods (own enumerator; exhaustive
  `|S| ≤ 8` sweep of 8.66M subsets at `n = 30`; differential tests of
  the engine's DPLL/resolution against brute force — zero mismatches).
* **Development honesty:** four real bugs in early versions were
  caught by the machine (all-pairs TwoCC blowup; a DPLL
  assigned-literal branching bug; repair-window 2-cycles; a
  `δ`-resonance chaining jumps into a 5-cycle), and four errors in the
  asymptotic proof TEXT were caught by the hostile review (R-A–R-D,
  plus the R-E reading-sensitivity caveat) — all repaired; the
  instances and corollaries were never affected.
* **Consequence (Corollary CR-2).**  Any constraint on
  `(i_0, i_1, tau)` valid for all uniquely satisfiable 3-CNFs admits
  the corner (the family realizes it with no selection freedom), so
  the re-optimized LP value over ANY valid constraint set equals `γ*`:
  **the narrow Stage-I route is mathematically closed**, not merely
  unexplored.  Stop rule S7-C.
* **Realizability map.**  The whole edge
  `{(0, t, 0) : t ∈ {0, 0.04, 0.05, 0.058…0.077, 0.12, 0.24, 0.32}}`
  is realized at the verified sizes; `(0, 0.06, 0)` exactly at
  `n ∈ {50, 100}`; distance to the corner `≤ 1/(2n)` in general.  No
  obstruction exists anywhere on this edge.
* **Scope.**  The corner instances are algorithmically EASY (dense
  all-positive structure); the result is about validity of
  statistics-level constraints, and says nothing about tightness of
  the full PPSZ analysis (tight instances for it are not known;
  Scheder, TR21-069 §1.2: "we do not even fully understand the true
  success probability of PPSZ").  Not ruled out, and recorded as
  future routes: improving
  the imported estimates; new statistics with new proved estimates —
  concretely, importing Hertli-2014's 1C-Unique gain (arXiv:1311.2513),
  whose class contains this family, as a fourth affine bound active
  near `tau = 0`; and the sparse-instance (`m = O(n)`) restriction of
  the realizability question, which remains OPEN.

## 3. Compliance

* Cycle-5 quarantine respected: no dependence on Theorems A/E/C/F,
  SEG, or `RR_n` anywhere in this cycle.
* `master`, `cycle05-fable`, `cycle06-fable` untouched; all work on
  `cycle07-o18-fable`.
* No promotion beyond the labels stated; no novelty claims beyond the
  audited search outcomes ("potentially new: the prescribed-profile
  constructions and the recombination-optimality no-go; not new: the
  1C-Unique class").
* The critical rule stands: no P-versus-NP attempt; nothing in this
  cycle implies any complexity separation.
* Stage-I candidate-inequality protocol: no inequality was proposed,
  because step 0 (falsification-first realizability) closed the route;
  the protocol's falsification machinery (exhaustive small-instance
  checks, adversarial construction, hostile review) was instead applied
  to the realizability theorem itself.

## 4. Artifact index

**Stage V:** `audits/cycle07_jc_validation.md`;
`research_cycle_07/stageV_log.md`, `lp_reconstruction.md`,
`scheder_import_ledger.md`, `ss_lifting_import_ledger.md`,
`novelty_frontier_audit.md`;
`research_cycle_07/frozen_sources/` (all primary sources + SHA-256
manifests); `research_cycle_07/checkers/independent_checker.py`
(+ output + report), `repair_certifications.py` (+ output + review).

**Stage I:** `research_cycle_07/stage1_semantics.md`,
`corner_realizability.md`, `corner_family_verification_output.txt`;
`experiments/cycle07_corner_family.py`;
`certificates/cycle07_corner/instances.json`;
`audits/cycle07_corner_theorem_review.md`;
`research_cycle_07/checkers/cr_review_*` (reviewer's independent
implementations and logs).

**Cycle-level:** `audits/cycle07_final_adversarial.md`;
`failure_knowledge.jsonl` entries RC7-O18-01, RC7-JC-01, RC7-ENG-01;
`RESEARCH_STATE.md` (Cycle-7 section).

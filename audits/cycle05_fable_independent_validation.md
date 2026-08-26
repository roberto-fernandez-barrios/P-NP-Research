# Independent hostile validation of Research Cycle 5

**Role:** fresh independent hostile auditor (did not produce any Cycle-5 work;
treated every Cycle-5 claim as false until independently reconstructed).
**Date:** 2026-08-22.
**Object audited:** branch `cycle05-fable`, commit
`bd12e5c` ("Complete research cycle 5 hybrid multi-order routing"), working
tree clean.
**Deliverable:** this file.  Auditor tooling (written from the definitions
only, no reuse of any Cycle-5 engine) is in `audits/independent_validation/`:
`audit_ref.py` (reference Python engine: literal induced-subset-DAG DP,
interval-walk DP, fast single-copy recurrence), `audit_engine.cpp`
(independent C++ engine: rejection enumeration, exhaustive affine attack,
scan rows, certificate verification with exact min-switch DP, coloring-free
`D_mid` DP, rooted min-max-k DP, triple probe), `attack_thm_a.py`,
`prep_and_verify_certs.py`, `my_seg_mc.py`.  These files are provided
untracked for the integrator's disposal; nothing in the repository was
modified (every generator rerun was diffed against git and restored;
`git status` clean at audit end).

**Supersession notice (2026-08-26).**  This file remains the historical
Fable audit at commit `bd12e5c`.  Its mathematical reconstructions and
reproductions are preserved, but its Theorem-E repair inventory, SEG
disposition, and §F novelty conclusion are superseded by the deep SEG proof,
arms-length referee, and final Sol cross-model validation
(`audits/cycle05_sol_final_cross_model_validation.md`).  The corrected current statuses are
recorded at the affected passages below.

**Method summary.**  I re-derived the interval-walk semantics from the
`RR_n` definition *before* reading Lemma 5A.1 (they matched), wrote both a
literal-DAG reference and a walk engine, cross-validated them against each
other on every normalized coloring at `n ∈ {8,10,12}` over random ∞-fixing
lists of `t ∈ {1,2,3}` copies plus ∞-moving unions (0 mismatches), and only
then attacked the Cycle-5 claims.  The Theorem-A counterexample search was
completed before reading the repository proof, as tasked.  The FLSY primary
source (ECCC TR26-001) was fetched and read by this auditor directly; no
FLSY statement was accepted from repository transcription alone.

---

## Verdict summary

| Task | Object | Verdict |
|---|---|---|
| A | Theorem A (repaired precomposition statement) | **SOUND AS STATED** |
| A′ | Original postcomposition statement | FALSE (both stored counterexamples independently confirmed) |
| B | Theorem E | **HISTORICAL VERDICT SUPERSEDED:** SOUND WITH APPLIED, CONCLUSION-PRESERVING REPAIRS (integer `D`, common-reference normalization, and growing strict FLSY parameter); t-independence and the conclusion remain valid |
| C | Lemma SEG / Theorems C, F | **HISTORICAL VERDICT SUPERSEDED:** SEG is `SOUND WITH REPAIRS`, an **ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED** repository proof, not published verbatim by FLSY; C/F retain the dependency but no longer depend on an unproved lemma |
| D | Finite certificates | ALL VERIFIED (one count-presentation finding, F1 below) |
| E | Formal scope | CLEAN (8,656 jobs from clean state; kernel-level axiom check passed; coverage ledger exactly matches reality) |
| F | Novelty audit | **HISTORICAL VERDICT SUPERSEDED:** final statuses are N1 `UNCLEAR`, N2/N3 narrowly `POTENTIALLY NOVEL`, aggregate N4 `UNCLEAR`, N5 object `KNOWN`, SEG localization `UNCLEAR` |
| G | Post-audit fixes | Blocker D1 verified fixed at committed-blob level; 6 of 7 dispositions fully verified; residuals listed (F6–F8) |
| — | **Final decision** | **MERGE-SAFE-WITH-MINOR-CORRECTIONS** |

No mathematical defect was found.  Every one of the >120 published numbers I
recomputed reproduced exactly.  The corrections listed at the end are
count-presentation, range-wording, and provenance items; none touches a
theorem conclusion or a certificate.  Later audits did correct the SEG and
novelty/provenance labels as noted above.

---

## A. Theorem A, reconstructed from zero

**Reconstruction.**  `RR_n`, literal union, hybrid acceptance and the
normalized-word model were rebuilt from `hybrid_definitions.md` §1 (which
matches the Cycle-4 canonical definition).  My engines independently
reproduce the canonical baseline: single-copy rejects `0` for all even
`n ≤ 20` (exhaustive, all `C(q, n/2)` words) and `21 / 414 / 4,700 /
40,392 / 292,407` at `n = 22..30` — exactly the Cycle-4 table.  The `n=22`
reject set equals the 21 rotations of `1^8 0^5 1^3 0^5` (verified as sets).

**Independent counterexample attack on the FINAL repaired statement**
(performed *before* reading the repository proof).  For every affine map
`x ↦ ax+b` with `a` a unit, `a ∉ {±1}` (all offsets `b`, not only `b=0` as
in the repository's scans):

| n | affine maps tested | common-reject candidates | union-rescued (counterexamples) |
|---:|---:|---:|---:|
| 22 | 210 | 0 | 0 |
| 24 | 460 | 0 | 0 |
| 26 | 450 | 0 | 0 |
| 28 | 432 | 5,832 | **0** |
| 30 (spot: a=2,3, b=0) | 2 | 667 + 493 | **0** |

t = 3 affine triples with all pairwise ratios `∉ {±1}` were sampled
systematically at `n = 22` (320 triples): zero common rejects.  So `G = 0`
holds vacuously at `n = 22..26` (affine pairs have *disjoint* rejection
sets there — a stronger empirical fact) and non-vacuously at `n = 28, 30`
(6,992 shared rejected words, none rescued).  **No counterexample exists in
the tested range.**

**Proof audit (after the attack).**  Line-by-line re-derivation of Lemmas
A.1, A.2, A.3 and the main proof:

* A.1 (adjacency count `max(0, s−h) + max(0, s−(q−h))`, four-way case
  split): correct, including composite `q` (`h ∉ {1, q−1}` ⟺ `a ∉ {±1}`;
  no double count since `q` odd).
* A.2: the committed text carries the repaired interior-case analysis (gap
  multiset `{1, q−j−1}`; `a = ±(q+1)/2` two-run structure with `j`-dependent
  gaps; matches at `j ∈ {2, q−3, q−2, q−1}` only — all inside the allowed
  boundary).  I verified the arithmetic independently.  The complement
  reduction is direction-swapping, and the proof is complete because
  direction `O′ → O` is proved directly at all sizes (the committed
  parenthetical states this; drafting remains slightly fragile but is
  mathematically closed).
* A.3: sign-pattern analysis correct in both parts; correctly
  circle-agnostic.
* Main proof: middle single-ownership (A.1) + no middle cross steps (A.2,
  sizes `j ∈ [3, q−4]` excluded, boundary steps `2→3` and `q−3→q−2` harmless
  because sizes `1,2,q−2,q−1` are rebuilt by A.3) + boundary conversion is
  airtight; the rebuilt pure chain certifies individual acceptance via
  Lemma 5A.1 at `t = 1`.  The dihedral merging clause is sound under the
  precomposition reading (rotations/reflections literally preserve the
  family).
* The reduction `(π_i(Std), π_j(Std)) ≅ (Std, ρ_{ij}(Std))` with
  `ρ_{ij} = π_i^{-1}π_j` is exactly why precomposition is the right
  hypothesis.

**Falsification of the original postcomposition statement.**  Both stored
counterexamples were re-verified end-to-end with my own engine (never
touching the Cycle-5 code): `n=22`, `π = [7,13,17,0,20,2,…,15]`,
`ψ = ×2`, word `0xae2b3`; `n=24`, `π = [5,17,9,…,1]`, words `0x2793aa`,
`0x27d2aa`.  In each case I confirmed: `π_2∘π_1^{-1} = ψ` affine with
`a = 2`; `ρ = π^{-1}ψπ` **not** affine (checked against all 252/506 affine
maps); both copies reject; the union accepts.  A 4,000-trial random
conjugate search of my own found no further examples (the phenomenon is
rare), which is consistent with the audit's targeted `--conj` search.

**Verdict: SOUND AS STATED** (repaired precomposition version).  Remark:
the `a ∈ {±1}` exclusion is a proof-necessity, not a truth-necessity — for
`a = ±1` the copies are literally identical and `G = 0` trivially; the
statement could absorb that case, as the merging clause implicitly does.

## B. Theorem E, reconstructed from zero

All six steps re-derived independently; every inequality checked:

* Step 1 uniqueness (`2(q−j−d) + j ≤ q ⟹ j ≥ q−2d`) and nestedness
  (`j ≥ q−2d−1` contradiction) verified; the ranges `j ≤ j* = q−2d−2` are
  exactly what the chain construction uses; the bounds are tight (the
  Cycle-5 audit's tightness computation is consistent with my derivation).
* Steps 2–3 budget: intermediates `≤ 3+2d`, top completion `≤ 3d+4 = k₀`;
  maximal chain with one set per size; every set contains the plus root.
* Step 5 (repaired indexing): complements `G_1^c ⊇ … ⊇ G_q^c` give a
  maximal linear-interval chain on `V_r` (`N = n−2` points, sizes `0..N`
  once each), sums `≤ k₀ + 1 = 3d+5`.  The committed text carries the
  repair.
* Step 6: fiber argument exact (`Pr[f(r)=+1] = m/q`; conditional
  restriction uniform balanced); union over roots gives `(n/2)·2^{−cN^{1/5}}`.

**Quantifier verification.**  (i) *t-independence is genuine*: the proof
processes one accepting chain; only the density of that chain's own states
enters; `t` never appears — confirmed at the level of each step.  (ii) *No
hidden large-n condition*: "for all sufficiently large even n" is explicit
in the statement; `q ≥ 2d+3` and FLSY's own threshold are implied by it.
(iii) The hypothesis `6d+8 < (n−2)^{1/5}` is strictly stronger than the
needed `3d+5 < N^{1/5}` — safe direction.  (iv) **The FLSY import**: I
fetched ECCC TR26-001 myself and read §4 in the original.  Theorem 4.4 is
verbatim: universal `c > 0`, every sufficiently large **even** `n`,
`𝓘_{n,1}` not `(ε,k)`-balanced-chain for `ε > 2^{−cn^{1/5}}` **and
`k < n^{1/5}`** — the *full* k-range, with a bound uniform in `k` (its
proof passes through `cbal ≤ n^{1/5}`).  This matters because Theorem E
allows `d` growing to `~n^{1/5}/6` and Theorem F uses `k ≈ (3/7)n^{1/5}`;
both sit inside the verified range.  (Doc nit F4: the header phrase
"`k = O(1)`" in `dense_circle_obstruction.md` understates this; harmless.)

**Adversarial attempt.**  A violating list must beat an asymptotic bound;
no finite computation can, and the deterministic part (Steps 1–5) leaves no
room: my own rooted min-max-k DP verified, for **every** pair-swap-rescued
coloring at `n = 24` (12) and `n = 26` (316), a rooted maximal std-interval
chain with `max |f| = 2` — versus the theorem's budget `3d+4 = 10`.  The
pair-swap 2-density derivation (§2) was re-checked (per-end substitution
structure; `def ≤ 2`).  The scan evidence the theorem "kills" was itself
reproduced exactly (see D).

**Historical verdict: SOUND AS STATED.  Final corrected status: SOUND WITH
APPLIED, CONCLUSION-PRESERVING REPAIRS.**  The later Sol audit additionally
requires integer `D` in all indices, normalizes only the common reference
(without assuming it is listed), retains the growing parameter
`k=3D+5<N^(1/5)`, and does not use the source proof display's non-strict
perfect-fifth enlargement.  None changes the conclusion or uniformity in
the number of copies.

## C. Lemma SEG, treated as hostile

**Primary-source work (this auditor's own).**  I fetched ECCC TR26-001 and
read pp. 18–25 (Definition 4.1, Lemmas 4.2/4.3/4.5/4.6/4.7, Theorem 4.4,
and the full proofs of 4.2 and 4.3).  The repository's transcriptions are
verbatim-faithful, including the paper-level slops the SEG audit flags (I
confirmed the overstated p. 25 extraction claim, the `x₀ := 0` anchor in
Lemma 4.7, and the `l, r ∈ [n]` degenerate-split slop).

**Anchor census — independently confirmed.**  The chain anchoring enters
only through: (i) Lemma 4.2 bookkeeping (choice of `(s,e)`; both walks
normalized to start at 0; `O(√n)` unconditioning) and (ii) the milestone
base case `z_0 := 0` in the proof of Lemma 4.3.  Every other ingredient
(first-passage Lemmas 4.5/4.6, milestone Lemma 4.7's increment condition,
the p. 25 domination chain with its explicit "translation invariance of
random walks") is translation-invariant and length-local.  For the segment
event with offset `|f(A)| ≤ k ≤ d`, the base case degrades exactly one of
`Θ(L/d³)` summands from `F_{Δ−2d}` to `F_{Δ−d−k} ⪰ F_{Δ−2d}` — constants
only.  The segment reduction itself is strictly simpler than the paper's
Lemma 4.2 (no `(s,e)` enumeration; disjoint coordinate sets give the needed
independence under uniform `g`; the `O(√N)` unconditioning is a pointwise
counting inequality).  The endorsed-form hypotheses (`A ≠ ∅`; cyclic case
`B ≠ Z_N` or an `(L+1)` factor; ambient normalization `f([N]) = σ`,
`|σ| ≤ 1`; `k ≥ 1`) are exactly the ones needed, and Theorem C's use sits
inside them (`|A| ≥ 3`, `|B| ≤ q−3`, `k = 2`, `σ = 1`).

**Falsification attempts.**  The event is monotone in `L`, so only the
*rate* is attackable.  The committed seeded Monte Carlo
(`cycle05_audit_seg_mc.py`, N = 2000) was rerun: **content-identical** to
the stored results JSON.  My own fresh MC (different N = 600, off-center
`A`, different seed, independently coded DP) shows the same picture: clean
monotone decay at `k = 1, 2` and an offset effect that is a constant factor
(`≈ 0.65–0.70` across two decades), not a rate change — matching the
audit's 0.68.  Nothing inconsistent with `exp(−cL^{1/5})` decay (observed
decay is much faster).

**Historical judgment, superseded as a current disposition.**  This audit
correctly observed that SEG does not appear in either version of FLSY, but
it treated the localization as routine and retained C/F as conditional on
an unproved lemma before a complete standalone proof was available.  The
later deep reconstruction, arms-length referee, and final Sol audit supplied
and checked the offset, integrality, first-leg, tail-arithmetic, cyclic-full,
and final-constant repairs R1–R5.  Current status: SEG is `SOUND WITH
REPAIRS`, **ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED**.  Its
provenance is **NEW BUT PROVED IN THIS REPOSITORY**, not a theorem published
verbatim in FLSY; its novelty status is `UNCLEAR`.  Theorems C/F retain the
dependency on SEG and inherit its reviewed-proof status, rather than being
unconditional consequences quoted from FLSY.

Statement-level checks of C and F themselves: the run-splitting arithmetic
(`≥ (q−7)/(D+1)` middle run), the union-bound accounting (`t·q³`-to-`q⁴`
slack), the `k = 2 < (L*)^{1/5}` regime, Lemma RS's sandwich bound, and
Theorem F's two-branch budget (`L = ⌊n^{1/5}/7⌋`; `6d+8 < (n−2)^{1/5}` for
`d = L+2` at large `n`; final `exp(−c″n^{1/25})`) all check out.  One
pinhole (F5): Lemma RS is stated for "middle" states while Theorem F's use
of Lemma E\* needs defect control from size 2 up; the same sandwich proof
covers those sizes, but the statement should say so.  Sketch-level,
conditional-track; no effect on labels.

## D. Finite certificates (all with my own engines)

* **Minimality.**  `RR_n` accepts every normalized coloring for all even
  `n ≤ 20` (exhaustive, my engine): since every copy of a valid family
  accepts everything, **no hybrid-only example can exist below `n = 22`**,
  for any list, ∞-moving included.  At `n = 22` exactly 21 words fail (the
  claimed orbit, verified as a set of rotations).
* **n = 22 certificates.**  All 122 verified: witness chains structurally
  valid under my semantics (nesting, sizes, interval membership in the
  correct circle, sum conditions); both copies reject; union accepts (my
  set-level DP); **exact minimum switch count 1 in all 122** (my own
  min-switch DP, not the repo's); 122 distinct `(perm, word)` pairs over 43
  distinct permutations, 66 single transpositions (dihedral δ ∈ {9, 10});
  exactly one canonical flag: `(1 13)`, word `0x1fe0e` — the transposition
  joins the `1^3` and `1^8` runs as described.  `common_rejects_of_pair`
  fields match my own counts for all 43 permutations.
* **n = 24 stored records.**  All 14,864 records verified the same way; exact
  minimum switches = 1 in every entry (computed, since the file lacks the
  field); the 414 distinct words are exactly the full single-copy failure
  set — "every failure word is rescued by some pair" CONFIRMED.  **Finding
  F1: the file contains 8,258 distinct `(perm, word)` examples; 6,606
  appear twice** (identical but for `swap[...]`/`xswap[...]` labels — two
  search routes recording the same find).  The exact formulation is
  **14,864 verified stored records = 8,258 distinct examples + 6,606
  swap/xswap duplicate records**.  Neither earlier Cycle-5 audit noticed.
* **Scan rows.**  Independently reproduced, all six counters each:
  `trans:22:1..10` (including the 2 and 4 rescued words at δ = 9, 10, by
  value), `trans:24:11` (54/220), `trans:30:14` (16,892/154,891),
  `pairswap:24/26/28/30` (12/14, 316/360, 4,138/4,709, 39,044/44,692),
  `mult:24/26/28/30` including the non-vacuous 54/0, 667/0, 493/0.  My
  rescued-word sets agree with the committed audit dumps
  (`audit_common_n24_pairswap.txt` etc.), whose pairwise diffs against the
  proposer dumps I re-verified empty.
* **Triple probe.**  Reproduced exhaustively at `n = 28` with my own
  3-circle engine: pair 4,709/4,138; triple-common 308; rescued 305; **3
  union rejects of 20,058,300** (the three words are one rotation orbit) —
  matching `triple_probe.json` exactly.  The committed seeded script also
  reruns content-identically, including the previously-unreproducible
  `n = 42` sampled row (19,971/16,185/6,342/5,232/6,026/316).
* **∞-moving probe.**  Schema-verified (32 finds / 550 tested); 5 of 32
  finds re-verified hybrid-only with my literal-DAG engine (the walk
  reformulation is correctly not asserted there); the committed script
  reruns content-identically.
* **Hashes / byte stability.**  All five SHA-256 manifest entries equal the
  **committed blob** hashes (`git cat-file | sha256sum`), the working tree
  matches, and `.gitattributes` pins `/certificates/cycle05_hybrid/**
  text eol=lf`.  Seeded generators (∞-probe, triple probe, SEG MC) rerun
  content-identically.  Caveat: on a fresh Windows rerun the scripts emit
  CRLF locally; identity holds at the committed/normalized level, which is
  what the manifest describes.
* **D_mid.**  My own coloring-free exact DP reproduces the entire claimed
  table: pair-swap `3/5/7 = (q−7)/2` at `q = 13/17/21` (Theorem D equality
  verified), transpositions `(0,2) → 0`, `(0,⌊q/2⌋) → 1`, `(0,q/4) → 0/1/1`,
  multipliers (with and without offsets) `→ 0`.

## E. Formal-scope audit

* Project build artifacts deleted (`formal/.lake/build`), then
  `formal/check.ps1` rerun: **`Build completed successfully (8656 jobs)`**,
  `PASS: BalancedChain.lean contains no sorry/axiom/admit` — the exact
  claimed job count.  Only linter warnings (unused section variables).
* Toolchain pinned: `lean-toolchain` = 4.32.1, mathlib pinned by rev in
  `lakefile.toml` + `lake-manifest.json`.
* My own token scan (`sorry|admit|axiom|native_decide|unsafe|opaque|
  implemented_by|extern|partial def|macro`): the only hits are the word
  "admits" in two doc comments; the checker's regex has proper word
  boundaries.
* **Kernel-level check (stronger than the repo's own):** `#print axioms`
  on `switchBound_zero_iff_chainPure`, `acceptsUnion_pure_or_hybridOnly`,
  `chainContained_union_switchBound`, `acceptsPure_acceptsUnion`,
  `chainGood_iff_consecutivePairsCross`,
  `iUnion_isOneBalancedChain_of_pointwise_accepts`,
  `acceptsColoring_relabel_iff` — every one depends only on
  `propext / Classical.choice / Quot.sound`.  No `sorryAx`, no custom
  axioms.
* The `MultiCopy` section was read in full: `labelSet` is genuinely
  provenance-invariant, `SwitchBound` matches the label-function definition
  of switch count, `switchBound_zero_iff_chainPure` is a real proof, and
  the trivial-bound lemma is honestly described as trivial.
* **Ledger accuracy:** `formal/coverage.md` and all prose keep the literal
  `RR_n`, Lemma 5A.1, Theorems A/C/E/F, SEG/RS/M, and every probability
  statement **UNFORMALIZED**.  I found no sentence anywhere implying Lean
  verifies any of those.  The coverage ledger exactly matches reality.

## F. Novelty audit from scratch

The searches performed for this historical audit (not reusing the original
Cycle-5 queries) covered common intervals of two circular permutations
(Uno–Yagiura-line, strong interval trees, Heber–Mayr–Stoye circular
algorithms); the exact phrases for alternating/switching chains and
"switch depth"/"alternation depth"; the AP-mod-q never-an-interval
dichotomy; and "balanced-chain set system".  The exact-term footprint for
the last phrase was FLSY plus withdrawn TR26-043.  Key citations were
spot-checked as real (FLSY at ECCC/CCC'26; CKSS24 at LIPIcs 300; NNN12;
DMPY12; AKV20; Uno–Yagiura; BCMR; Heber–Mayr–Stoye;
Albert–Atkinson–Klazar; Cooper).

**Assessment — SUPERSEDED.**  The original corroboration was too narrow
because exact-term searches missed equivalent-object vocabularies.  The
final Sol audit located arc permutations for pure cyclic growth words;
greedoid/antimatroid and learning-space feasible-path machinery; FLSY
Definition 1.2/Lemma 2.3's literal unions of relabelled set systems; and the
explicit extra full chain in Algaba–van den Brink–Dietz, TI 15-007/II
(2015), Example 4.7, printed p. 23.  The corrected classifications are:

- N1: `UNCLEAR` because the exact statement was not located but folklore
  risk is high.
- N2: narrowly `POTENTIALLY NOVEL` for the repaired affine rigidity theorem.
- N3: narrowly `POTENTIALLY NOVEL` for the exact hull/refinement/rooted-FLSY
  transfer, not for approximate intervals generally.
- N4: `UNCLEAR` as an aggregate framework; only the exact `D_mid` and
  run-sandwich quantitative forms may be potentially novel.
- N5: `KNOWN` as a literal-union balanced-chain object from FLSY; the
  RR-specific structural results remain separately classified.
- SEG localization: `UNCLEAR`; it is a repository proof using published
  FLSY machinery, not a novelty-certified or published-verbatim theorem.

No strong novelty status is justified by the bounded searches.

## G. Post-audit fix verification (against artifacts, not dispositions)

| Fix | Verified state |
|---|---|
| D1 blocker (byte stability) | **FIXED, strongest level:** `.gitattributes` rule present; all five payloads LF; manifest SHA-256 = committed blob SHA-256 for all five files (checked via `git cat-file`); `sha256sum -c` OK; attributes report `text: set, eol: lf` |
| D2 stale pair-swap-open sentence | FIXED — grep finds no "genuinely open" residue; §6 now states the A/E/C/F coverage map |
| D3 `D_mid ≤ 1` label inflation | FIXED — results §3 and STATE carry "machine-exact for q ≤ 21; all-q bound a recorded proof candidate, used qualitatively" |
| D4 "87.5%" | FIXED — the figure survives only inside the audit/disposition records; live docs use per-n figures.  Residual F2 below |
| D5(i) triple probe provenance | FIXED and verified — committed script defines "shifted pair-swap", reruns content-identically including the formerly lost n=42 sample; manifest extended to 5 entries |
| D6 artifact indexes | FIXED — README and STATE now list the novelty audit, ∞-probe script/JSON, barrier audit |
| D11 mutating repro command | FIXED — README command targets a scratch path with an explicit warning |
| D5(ii) annotation provenance | **NOT fixed** — the step that added `min_switches`/`canonical` to the n22 JSON is still uncommitted (annotations are correct; I recomputed them) |
| D5(iii) revB / bit-reversal / xor generators | **NOT fixed** — still no committed generator |
| D7 "same schema" | **NOT fixed** — README still says the n24 JSON has the n22 schema; it lacks `min_switches`/`canonical` |
| D8 "~40 searches" | **NOT fixed** — results §3 still says ~40; the novelty file documents 20 numbered queries plus listing scans/reads |
| D9, D10 | Not addressed (cosmetic; D10 files are declared audit evidence) |

The disposition's "all MINOR items addressed" is slightly overstated
(D5(ii)/(iii) remain), and its table silently omits the cosmetic findings.
None of the residue affects correctness.

---

## Findings register (this audit's own)

| ID | Severity | Finding |
|---|---|---|
| F1 | MINOR (count presentation) | The `n=24` artifact has **14,864 stored records**, not that many distinct examples: distinct `(perm, word)` examples number **8,258**, and 6,606 records duplicate finds under `swap`/`xswap` labels.  All records individually validate; the 414-word coverage, min-switch-1, and 440-permutation claims are unaffected. |
| F2 | COSMETIC (range wording) | results §1/STATE: "rescued 85.7–87.9% … n = 24..34" — the n=34 rate is 85.6% (2,065,656/2,413,835), just below the stated floor.  `switch_structure_theory.md` §4: "87.4–87.9% … at n = 24, 26, 28, 30" — the n=24 rate is 85.7% (12/14).  Same 0.1–1.7pp class as the D4 finding the cycle already fixed once |
| F3 | COSMETIC | results §4 "only far transpositions (δ ≥ 8 at n=22) … rescue": true as a necessary bound, but δ = 8 rescues nothing (observed rescuing δ ∈ {9, 10}); the sharp threshold is 9 |
| F4 | COSMETIC | `dense_circle_obstruction.md` header "FLSY Theorem 4.4 … with k = O(1) < N^{1/5}" understates the theorem's own use (k = 3d+5 with d allowed to grow); the import is valid for the full k < N^{1/5} range (primary source verified), so no mathematical effect |
| F5 | MINOR (conditional track only) | Lemma RS covers "middle" states; Theorem F's use of Lemma E* needs defect control from size 2 up.  The identical sandwich argument covers those sizes; the statement should be widened when SEG/F are ever written out in full |
| F6 | MINOR (provenance) | D5(ii): the annotation-adding step for the n22 JSON remains unrecorded (annotations independently reconfirmed correct by this audit) |
| F7 | MINOR (provenance) | D5(iii): §6's revB / bit-reversal / xor constructions still have no committed generator |
| F8 | COSMETIC | D7 ("same schema"), D8 ("~40 searches"), D9 remain as the integration audit left them |

## What this audit reproduced, in numbers

21/414/4,700/40,392/292,407 rejects (n = 22..30, exhaustive, own engine);
the n=22 orbit as a rotation set; 0 rejects for n ≤ 20 (nine exhaustive
enumerations); 1,554 affine maps attacked with 6,992 non-vacuous shared
rejects and 0 rescues; 2 postcomposition counterexamples confirmed; 122
`n=22` certificates plus 14,864 `n=24` stored records fully re-verified,
including exact min-switch (the latter are 8,258 distinct examples plus
6,606 swap/xswap duplicates); 20+ scan rows
(all six counters); the full D_mid table; the triple probe (both rows); 5
∞-probe finds; 328 rooted min-max-k values (all = 2 ≤ 10); 3 seeded
generators content-identical on rerun; 5 manifest entries vs committed
blobs; 8,656 Lean jobs from clean state + kernel axiom check on 7 theorems;
FLSY Theorem 4.4 / Lemmas 4.2–4.7 verified against the fetched primary PDF;
TR26-043 withdrawal verified at source.

## Final decision

**MERGE-SAFE-WITH-MINOR-CORRECTIONS**

The mathematics of Cycle 5 survived a hostile, from-zero, independently
tooled validation: Theorem A (repaired) is sound as stated and its original
form is genuinely falsified; Theorem E is sound with the later
conclusion-preserving integer-parameter, common-reference, and growing-`k`
repairs applied, while its `t`-independence and conclusion are unchanged.
As corrected by later audits, SEG is a `SOUND WITH REPAIRS`, adversarially
reviewed, unformalized repository proof and C/F retain that dependency;
every certificate and every checked number reproduces; the formal ledger
matches reality.  The original novelty endorsement in this audit is
superseded by the corrected N1–N5/SEG statuses in §F; the pre-commit blocker
fix is verified at the committed-byte level.  Findings F1–F8 are historical
correction requirements; their Cycle-5 final resolutions are mapped in
`audits/cycle05_final_correction_integration.md`.  None changes a theorem
conclusion or certificate validity.

Per the mandate: this audit does not merge, does not authorize a merge by
itself, and does not begin Research Cycle 6.

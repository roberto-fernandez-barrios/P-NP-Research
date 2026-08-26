# Cycle 7 — final integration adversarial audit

**Date:** 2026-08-26.  **Branch audited:** `cycle07-o18-fable`.
**Auditor stance:** hostile consistency-and-overclaim review of the
cycle's own documents.  This audit does NOT re-verify the mathematics
(done by the dedicated Stage-V checkers and the Theorem-CR hostile
review); it verifies that every claim, label, number, and status in the
cycle's summary documents is backed by the cited artifacts, internally
consistent, and not overclaimed.
**Method:** full read of `results/research_cycle_07.md`,
`audits/cycle07_jc_validation.md`, `research_cycle_07/stageV_log.md`,
`corner_realizability.md`, `audits/cycle07_corner_theorem_review.md`,
`lp_reconstruction.md`, `stage1_semantics.md`, the three RC7-*
`failure_knowledge.jsonl` entries, and the Cycle-7 sections of
`RESEARCH_STATE.md`; every shared number re-grepped against the primary
transcripts (`repair_certifications_output.txt`,
`independent_checker_output.txt` + `_report.md`,
`corner_family_verification_output.txt`, `instances.json`); ledger and
review verdict lines read in situ; SHA-256 of the Stage-I artifacts
recomputed; quarantine and no-new-bound greps run over all cycle
documents.  No file was modified except the creation of this audit; no
git commands were run.

---

## OVERALL VERDICT: **INTEGRATION SOUND AFTER LISTED FIXES**

No mathematical claim, number, verdict, or label was found to be wrong
or unsupported at the substance level: every cross-document number
reconciles exactly with the primary transcripts (A2: zero numeric
discrepancies), the Stage-V verdict is in the mandated form with the
required frontier statement and gate decision (A1), the stop rule was
honored (A4), the quarantine holds (A5), labels follow house style
(A7), and no new bound or complexity consequence is claimed anywhere
(A8).  The required fixes below are documentation-accuracy defects —
two stale SHA-256 hashes, three sentences that overclaim relative to
their own cited evidence, one wrong internal cross-reference, and one
quotation not present in any frozen source.  None invalidates the
cycle's results; all must be fixed before the final commit because they
are exactly the kind of defect this repository's discipline exists to
prevent.

---

## REQUIRED FIXES (before commit)

**RF1 [stale hashes — factual error in the current revision].**
`research_cycle_07/corner_realizability.md` §5 states:

> "Engine: `experiments/cycle07_corner_family.py` (SHA-256
> `fa51e86e372d4a47b1fffce7b23cfb475072500a60beaeba22e2dd4516ee96e9`).
> Transcript: `research_cycle_07/corner_family_verification_output.txt`
> (SHA-256 `782fc107…bf26f`)."

Recomputed today, the files on disk hash to
`c00ae7235399ce43d61a54eaaf23cd5ffa0c86778b24701aa0f45c9e6f4f8c55`
(engine) and
`eac85d35581b697f625c6454aec7eb397b56732011b1ab02c62f82d19c93017b`
(transcript) — **neither matches**.  The dataset hash DOES match
(`instances.json` = `1af8aff15117d948285bf32e82a87a8574195ea5c3266aeb4c1ccb42acac28cd`
= the doc's and the reviewer's `1af8aff1…28cd`).  Diagnosis (from file
content and mtimes; git was off-limits to this audit): after the
hostile review (which pinned `fa51e86e…`/`782fc107…`), the engine's V1
and V6 docstrings were edited exactly along the review's B7 "minor
cosmetic gaps" (they now read "their non-adjacency is by construction"
and "reported, not …"), and the engine was re-run, changing the
transcript's timing fields; the deterministic dataset was rebuilt
byte-identical.  All 21 result lines in the current transcript match
the review's independently replicated values (clause counts
299/405/740/1175/1710/3080/4850/7020/27684/70245/142806, profiles
{1: m1, 2: n−2m1, 3: m1}, girths 5–30, 21/21 PASS), so evidential
continuity holds — but the document's hash claims are false as
written.  *Fix:* update §5's engine and transcript hashes to the
current values and add one sentence: the only post-review engine change
is the docstring/comment corrections responding to review B7's minor
items; the transcript re-run differs in timing fields only; the dataset
is byte-identical to the reviewed one (hash unchanged).  (Alternative:
revert the engine to the reviewed bytes.)  The review file's own hash
lines are a correct historical record of what was reviewed and must NOT
be edited.

**RF2 [overclaim vs the checker's own 89/90].**
`results/research_cycle_07.md` §0:

> "Every displayed number replicates in exact rational arithmetic under
> two independent checkers"

This contradicts finding F1 three paragraphs later and the independent
checker's recorded result (89/90 PASS, check 09d FAIL): [JC26] eq. (2)
*displays* the terminal bound `≥ 1/15218`, which is exactly false
(refuted by the independent checker; not covered by the authors'
checker at all, per `stageV_log.md` §V1).  *Fix:* scope the sentence,
e.g. "Every displayed number of the paper's new analysis replicates in
exact rational arithmetic under two independent checkers; the one
displayed claim that fails anywhere is the inherited background
endgame of eq. (2) — finding F1, a source defect."  (The same
scoping should be echoed in `audits/cycle07_jc_validation.md` §2 item 2,
whose heading "Every displayed number." has the same universal form,
though its itemization is already scoped.)

**RF3 [wrong internal cross-reference].**  `results/research_cycle_07.md`
§0:

> "Real defects were found and certified — mostly in the *source*
> literature, not in [JC26]'s new mathematics (see §2)."

§2 of the report is "Stage I — the corner is realizable"; the defects
are in §1 (items 6–7).  *Fix:* "(see §1)" or "(see §1, items 6–7)".

**RF4 [repair-status heading overclaims two repairs].**
`results/research_cycle_07.md` §1 item 6:

> "**Repairs, all certified in exact rationals**
> (`checkers/repair_certifications.py`; adversarially reviewed — SOUND
> WITH CAVEATS, caveats hardened in):"

Two of the five listed repairs are not exact-rational certifications by
the cycle's own account: R4 is a definitional relabel (nothing to
certify) and R5 is a statement-form/quantifier repair established by
verified reasoning (`lp_reconstruction.md` §6 + the audit), with only
its numeric slack (γ*−γ_new = 8.05·10⁻¹¹, base margins 4.8·10⁻¹⁰ /
6.9·10⁻¹¹) certified.  Also "caveats hardened in" is inaccurate for
caveat C3, which is an inherited-trust boundary that *cannot* be
hardened (see RF5).  *Fix:* e.g. "**Repairs** (R1–R3 and R5's numeric
slack certified in exact rationals, `checkers/repair_certifications.py`;
R4 a definitional relabel; adversarially reviewed — SOUND WITH CAVEATS,
caveats C1/C2/C4 hardened in, C3 carried as an explicit dependency):".

**RF5 [evidence-map row overstates the repair review].**
`audits/cycle07_jc_validation.md` §1, "Repair certifications" row:

> "…every derivation independently re-derived, enclosure fuzz-tested,
> certifier mutation-tested …; all caveats hardened into the script
> afterwards (C1 sign-precondition assert; C2 upper side
> |φ_TwoCC| ≤ 5 certified; C4 Ψ-ordering certified exactly) and the run
> re-passes exit 0"

The review itself (`repair_certifications_review.md`) says: "four
integrals re-derived fully by hand; **nine more by high-resolution
Simpson quadrature**" (reproduction, not re-derivation), and its caveat
C3 states the §8.3 constants "are certified only *relative to the
printed closed forms*; B(r) and the 8.3 integrals are not re-derived …
Any Stage-V verdict should carry this dependency forward explicitly."
C1/C2/C4 are indeed hardened (verified in this audit: the assert at
`repair_certifications.py` lines 612–614 and the two new PASS lines in
the stored transcript; re-run exit 0 confirmed by the transcript's
final line), but C3 is not — and cannot be.  *Fix:* "…every exact
result independently reproduced (four integrals re-derived by hand,
nine by independent quadrature), enclosure fuzz-tested, certifier
mutation-tested …; caveats C1/C2/C4 hardened into the script … ; C3
(the three §8.3 closed forms taken as printed; B(r) not re-derived)
carried forward as an explicit dependency."

**RF6 [publication-status paragraph contradicts review caveat C3].**
`audits/cycle07_jc_validation.md`, "Publication-status finding":

> "…now mitigated by this cycle's independent certifications of the
> load-bearing hairline constants (…, **the full §8 closed-form family
> re-integrated symbolically**, and the falsity of the printed
> JUNK₂ ≤ 0.000184 certified harmless downstream)."

Per the review's C3 and the transcript itself, the §8.4-side family
(BFS, DFC, DFS, JUNK₁, JUNK₂, the three φ²-integrals) was re-derived
by exact symbolic integration, but the three §8.3 constants (Bonus2CC,
DFS2CC+DFD2CC, JUNK2CC) were certified only *from their printed closed
forms* (transcript lines show "value in […]" with no "closed form =="
re-derivation).  *Fix:* "…the §8 closed-form family re-integrated
symbolically except the three §8.3 2CC constants, certified relative
to their printed closed forms (review caveat C3)…".

**RF7 [quotation not in any frozen source].**
`results/research_cycle_07.md` §2 (Scope bullet):

> "…says nothing about tightness of the full PPSZ analysis ("no tight
> instances for PPSZ are known" — Scheder)."

and `research_cycle_07/corner_realizability.md` §6:

> "…the recognized hard regime for PPSZ ("researchers do not know any
> tight instances for PPSZ" per Scheder)…"

These are two DIFFERENT wordings of the same allegedly quoted sentence,
and **neither occurs in either frozen Scheder source**: this audit
searched the extracted text of ECCC TR21-069 rev 1 (3 hits for "tight",
none about instances) and the TheoretiCS-2024/arXiv-2207 PDF (1 hit,
"This would be tight if…").  The verifiable frozen sentence in the
neighborhood is TR21-069 §1.2: "we do not even fully understand the
true success probability of PPSZ" (plus the CTTS/PTS exponential-
lower-bound citations).  *Fix:* in both documents either substitute the
verifiable frozen sentence as the quote, or remove the quotation marks
and state it as a paraphrase with a pinpointed source.  (The
surrounding claim itself — the family being easy says nothing about
PPSZ tightness — is independently sound and unaffected.)

---

## OPTIONAL POLISH (not blocking)

* **OP1.** `audits/cycle07_jc_validation.md` R3: "ε_I = 0.0731…" — the
  trailing ellipsis is misleading (the exact value is
  0.07307238160252154687…, so "0.0731" is a rounding, not a prefix).
  Write "0.0731 (exactly 0.0730723816…)"; same display without ellipsis
  in the report's R3 bullet is acceptable as the paper's rounding.
* **OP2.** `corner_realizability.md` header: "Full machine verification
  of every finite claim by two independent implementations" — scope to
  the 21-instance claims; the δ-existence scan (26 ≤ n ≤ 1200) and the
  girth scan (to n = 800) are reviewer-only single-implementation
  artifacts.  (§6's status labels already scope this correctly.)
* **OP3.** `corner_realizability.md` §2/§5: "so `n_0 = 28` suffices" —
  add the reviewer's qualifier: verified by scan to n = 1200; beyond
  that the corrected counting argument gives a valid δ for all large n
  (the review says "n_0 = 28 suffices *empirically*").
* **OP4.** `RESEARCH_STATE.md` Cycle-7 section: "Realizability map: the
  whole edge `(0, t, 0)`, `t ≤ 0.32` at the verified sizes" — reads as
  a continuum claim; the verified sizes realize 11 discrete densities
  {0, 0.04, 0.05, 0.0583…0.0769, 0.12, 0.24, 0.32}.  Suggest "realized
  points spanning t = 0…0.32".
* **OP5.** `results/research_cycle_07.md` §1 item 2: "transcript
  byte-identical to the frozen one" — `stageV_log.md` says
  byte-identical *modulo CRLF*; add "(modulo CRLF)".
* **OP6.** `stageV_log.md` V4 Part C says "§8 closed forms re-derived by
  exact symbolic integration (all match the printed forms…)" — as a
  running log it should not be rewritten, but an append-only correction
  note recording review caveat C3 (the three §8.3 constants evaluated
  from printed forms, not re-integrated) would align the log with the
  review.
* **OP7.** `audits/cycle07_jc_validation.md` header "Date: 2026-08-25" —
  the document incorporates 2026-08-26 artifacts (the repair-review
  verdict and the hardened re-run); date it "2026-08-25 → 26".

---

## Per-item findings

### A1. Verdict-form compliance — **PASS**

* `audits/cycle07_jc_validation.md` line 15: "## VERDICT:
  **JC-SOUND-WITH-REPAIRS**" — exactly one of the three mandated forms;
  the spelling is identical at every occurrence
  (report §0 twice + §1; `stageV_log.md` V5; `RESEARCH_STATE.md`).
  No variant or hedged form found (grep).
* The SOUND-WITH-REPAIRS obligations are met immediately below the
  verdict: the corrected frontier ("Repaired frontier (unchanged from
  the paper's claim): randomized general 3-SAT in `O(1.307031578^n)`;
  Unique-3-SAT in `O(1.306969598^n)`"), with the honest R5 rider that
  no repair moves a number but the fixed-`w` quantifier form is
  downgraded; and the explicit Stage-I meaningfulness decision
  ("Stage-I gate decision: Stage V passes strongly enough to proceed …
  well-posed against the frontier 1.307031578").  Unambiguous.

### A2. Number consistency — **PASS** (zero numeric discrepancies)

Every number checked in every document where it appears, against the
primary transcripts.  Highlights (transcript values shown exact):

| quantity | primary transcript value | documents | match |
|---|---|---|---|
| γ* | `independent_checker_output.txt` 18h: [0.000068779380458836, …37] | corner doc CR-2, RESEARCH_STATE | exact |
| i₁* | 18i: [0.060043244708778326, …27] | corner doc, stageV_log, jc_validation (0.0600432…), instances.json | exact |
| frontier | base table: 2^(p₀−γ_new) < 1.306969598 (margin 4.84·10⁻¹⁰); 2^(p₀−0.000000364) < 1.307031578 (margin 6.88·10⁻¹¹) | all docs: 1.307031578 / 1.306969598; jc_validation R5's 4.8·10⁻¹⁰ / 6.9·10⁻¹¹ | exact / correct roundings |
| F1 minimax | v = 31273/475913718, crossing 7192790/79318953 | all docs | exact (audit re-derived 1/v = 15218 + 1204/31273 = 15218.0385…) |
| F1 shortfall | 43/258659105733 = 1.66241972…·10⁻¹⁰ | stageV_log 1.662·10⁻¹⁰, jc_validation 1.66·10⁻¹⁰ | exact (audit re-derived 1204 = 28·43 reduction) |
| F1 guards | v ≥ 1/15219 margin 4.15·10⁻⁹; 2^(p₀−v) = 1.3069723767157… < 1.306972377 margin 2.84·10⁻¹⁰; 2^(p₀−1/15218) = 1.306972376565153… | stageV_log, jc_validation | exact |
| R2 margin | OCB*(4) = 0.000869965583 vs 1/1150 = 0.000869565217 → 4.00·10⁻⁷ | "4.0·10⁻⁷" everywhere | exact |
| BFS−DFB | 0.030966519315 vs 0.030966 → 5.19·10⁻⁷ | "5.2·10⁻⁷" (jc_validation, stageV_log, RC7-JC-01) | exact |
| Lemma 55 | 0.001687361857 (= −707/6 + 170 ln 2) vs 0.001687 → 3.62·10⁻⁷ | "3.6·10⁻⁷" | exact |
| dual slacks | b₀−2b₁ = 1.34097398093794778…·10⁻³; b_T+(b₁/A)S = 1.38537454842306473…·10⁻² | lp_reconstruction 1.34097·10⁻³/1.38537·10⁻²; jc_validation 1.3410·10⁻³/1.3854·10⁻² | exact / correct roundings |
| checker tally | 89 `[PASS]` + 1 `[FAIL]` (09d) counted in the transcript | "89/90", "1 FAIL = F1", "exit 1 by design" everywhere | exact |
| safe-branch margins | excesses 4.15293…·10⁻¹⁴ and 5.05818…·10⁻¹⁴ over 2.69/2.70·10⁻¹¹ | "tightest 4.15·10⁻¹⁴"; "4.2/5.1·10⁻¹⁴" | exact / correct 2-s.f. roundings |
| ε_R, ε_I | 0.1024756190168075228998451658; 0.07307238160252154687451293138 | jc_validation R1 (full digits), RC7-JC-01, transcripts | exact (see OP1 on "0.0731…") |
| 21/21, n, m₁ | transcript: 21 PASS lines; n ∈ {26,30,40,50,60,80,100,120}; m₁ = round(i₁*n) ∈ {2,2,2,3,4,5,6,7}; breadth m₁ ∈ {0,2,6,12,16} at n = 50 | report "n = 26…120"; corner doc §5 lists; realized t-set {0, 0.04, 0.05, 0.058…0.077, 0.12, 0.24, 0.32}; i₁ = 0.06 exactly at n ∈ {50,100}; \|0.06−i₁*\| = 4.32·10⁻⁵ | exact |
| review replication | clause counts, profiles, girths 5–30, 8,656,936 (= "8.66M") subsets, 1,350 + 800 differential cases, 72,673 scanned pairs, sole δ-failure (27,2) | review B5/B8, corner doc §5, report §2 | exact |
| repair-review anchors | mutation refuted at ε = 0.111 past √7/24 ≈ 0.110243; c_T envelope margin 1.206·10⁻³, cover ≥ 33.5×; E(162) = 0.097692 | jc_validation, stageV_log ("0.0977") | exact |
| γ*−γ_new | 8.046·10⁻¹¹ (lp_reconstruction) | jc_validation "8.05·10⁻¹¹" | correct rounding |

Also checked: `instances.json` holds exactly 21 instances with the
stored `g`-maps and `i1_star` field matching i₁*; Thr_JC = 2.2168·10⁻⁴
and Thr_Scheder = 2.1963·10⁻⁴ match the transcript; the "nine JSON
reported intervals" count matches the checker report; "≥ 17–65
significant digits" matches the checker report's precision statement
(≥ 65 for exact-input quantities, 17–18 for the data-limited η's).
**No cross-document numeric discrepancy of any kind was found.**

### A3. Overclaim hunt — **PASS on scope/status/attribution/novelty; ISSUES RF2–RF7 on five sentences**

* **(i) No-go corollary scope: PASS.**  CR-2 and the report both
  restrict to "constraint on `(i_0, i_1, tau)` … valid for every
  uniquely satisfiable 3-CNF"; the "even jointly with n" strengthening
  is exactly the reviewer's B6(iii) addition ("n-joint constraints …
  cannot raise the asymptotic value either"), verified and adopted.
  Both documents explicitly list what is NOT ruled out (improving the
  imported estimates; new statistics with new proved estimates —
  concretely the Hertli-2014 1C route; the sparse m = O(n) restriction,
  recorded OPEN) and state the instances are algorithmically easy and
  say nothing about PPSZ tightness.  No overbroad "PPSZ cannot be
  improved" claim exists anywhere.
* **(ii) Theorem CR status honesty: PASS** (minor nits OP2/OP3).  The
  header and §6 state: PROOF CANDIDATE; hostile review verdict SOUND
  WITH REPAIRS with all repairs R-A–R-E applied; finite claims
  MACHINE-VERIFIED BY TWO INDEPENDENT IMPLEMENTATIONS (21 instances,
  both variants, both Definition-31 readings); asymptotic arguments
  ADVERSARIALLY REVIEWED with repairs; UNFORMALIZED.  The
  machine-verified vs asymptotic split is explicit; the development
  bugs (4) and review-caught text errors (R-A–R-D + R-E caveat) are
  disclosed in both the theorem doc and the report; the review's
  verdict wording matches ("SOUND WITH REPAIRS").
* **(iii) "Repaired frontier unchanged" vs repair content: PASS.**
  Each of R1–R5 in `cycle07_jc_validation.md` ends "**No number
  changes.**", and the audit confirmed none of the repaired quantities
  feeds the LP constants: R1 withdraws a *range* (operating point
  re-certified); R2 tightens a *quantifier* (both Thr values comply);
  R3 corrects a *range* (ε_I complies); R4 relabels a definition; R5
  repackages quantifiers with the O(·) claims surviving on certified
  slack.  The verdict header's "No repair changes the certified bases,
  the LP, its optimum, or its dual slacks" is accurate, and the R5
  quantifier downgrade is disclosed in the same paragraph, in §6, and
  in the report.
* **(iv) Errata attribution: PASS.**  The Scheder ledger's I6 verifies
  the endgame constants verbatim in the source ("15218 ✓; 1.306973 ✓"),
  its defects section is explicitly titled "Source-internal defects …
  (**not JC transcription errors**)", and I6's severity is "none (JC's
  'unrounded base' is derived, not quoted — consistent)".  The report
  and RC7-JC-01 attribute F1 and the other false constants to ECCC
  TR21-069 rev 1 with [JC26]'s reproduction faithful — matching the
  ledger exactly.
* **(v) Novelty: PASS.**  All novelty language is "potentially new" /
  "NOT FOUND by the logged searches" (novelty audit's own method note:
  "never 'proven nonexistent'"); the report §3 caps it ("no novelty
  claims beyond the audited search outcomes"), and the corner doc §6
  separates claimed-potentially-new from explicitly-not-claimed (the
  1C class, PPSZ tightness).  "First arms-length validation **on
  record**" is properly hedged and backed by V-b.
* **ISSUES:** RF2 ("every displayed number"), RF3 (wrong §-pointer),
  RF4/RF5 (repair-certification status wording vs C3), RF6 ("full §8
  family re-integrated"), RF7 (unfrozen quotation) — all listed above
  with exact quotes.

### A4. Stop-rule application (S7-C) — **PASS**

* The Cycle-7 mandate document itself is not stored in-repo; compliance
  was audited against the coordinator-quoted wording ("the LP corner is
  shown realizable… Produce the realizability/obstruction map and
  STOP") and its frozen ancestor in `audits/cycle06_target_selection.md`
  §8: "**S-C** the LP corner is realizable / no valid inequality
  survives bounded falsification → record the realizability map, stop."
* The cycle stops there: report §3 records "no inequality was proposed,
  because step 0 (falsification-first realizability) closed the route";
  the Hertli-1C fourth-estimate idea is *recorded* as next-cycle
  material and explicitly "recorded, not pursued" / "explicitly outside
  the Stage-I scope"; `RESEARCH_STATE.md` "Next action: Stop.  Do not
  begin Research Cycle 8 automatically."  No continued optimization, no
  re-certification attempt, no candidate-inequality artifact exists.
* The realizability map is present: the realized-edge inventory
  (11 densities, corner exact at n ∈ {50, 100}, deviation ≤ 1/(2n)),
  the 21-instance dataset `certificates/cycle07_corner/instances.json`,
  "No obstruction exists anywhere on this edge", and the sparse-case
  OPEN record.

### A5. Quarantine compliance — **PASS**

Unfiltered grep of all cycle-7 documents (`results/research_cycle_07.md`,
both cycle-7 audits, all `research_cycle_07/*.md`) for Theorems
A/E/C/F, SEG, `RR_n`, and Cycle-5 references: the only occurrences are
the two explicit non-dependence statements in the report (header
"nothing in this cycle depends on Theorems A/E/C/F, SEG, `RR_n`, or any
other Cycle-5 result"; §3 restatement) and the corner doc §6's
non-dependence declaration.  No cycle-7 argument, artifact, or number
depends on any Cycle-5 result.

### A6. Artifact-index accuracy — **PASS after RF1**

* Every file listed in report §4 exists on disk (verified by listing):
  Stage V — `audits/cycle07_jc_validation.md`; `stageV_log.md`,
  `lp_reconstruction.md`, `scheder_import_ledger.md`,
  `ss_lifting_import_ledger.md`, `novelty_frontier_audit.md`;
  `frozen_sources/` (24 files incl. `sha256_manifest_raw.txt`,
  `scheder_manifest.txt`, `ss_manifest.txt`);
  `checkers/independent_checker.py` + `_output.txt` + `_report.md`;
  `repair_certifications.py` + `_output.txt` + `_review.md`.
  Stage I — `stage1_semantics.md`, `corner_realizability.md`,
  `corner_family_verification_output.txt`,
  `experiments/cycle07_corner_family.py`,
  `certificates/cycle07_corner/instances.json`,
  `audits/cycle07_corner_theorem_review.md`, and all six
  `checkers/cr_review_*` files.  Cycle-level —
  `failure_knowledge.jsonl` entries RC7-O18-01 / RC7-JC-01 / RC7-ENG-01
  present as the last three entries; `RESEARCH_STATE.md` Cycle-7
  section present; `audits/cycle07_final_adversarial.md` is created by
  this audit, closing the index.
* Quoted verdicts all match the reviewed files verbatim: SS ledger
  "**CLEAN**" ✓; Scheder ledger "**MISMATCHES FOUND**" with the I1–I10
  severity table (HIGH/MEDIUM/MEDIUM-LOW/LOW/STRUCTURAL) ✓; CR review
  "Overall verdict: **SOUND WITH REPAIRS**" ✓; repair-certifications
  review "VERDICT: SOUND WITH CAVEATS" ✓; novelty audit "SUPPORTED
  (high confidence, with two caveats)" ✓.
* Repairs R-A–R-E are genuinely applied in `corner_realizability.md`:
  R-A (the `{p_i} ∩ {s_i}` clause deleted from §2's δ-condition, with
  the reviewer's vacuity finding recorded), R-B (corrected δ-existence
  counting, `n_0 = 28`, sole failure (27,2)), R-C (false girth bound
  replaced by the reviewer's `girth > 17` for `n > 96 + 51δ`, j = 3
  triangle case included), R-D (girth-free triangle-free
  pairs-uniqueness argument), R-E (triples variant promoted to primary
  carrier of the no-go; pairs iterated-closure sensitivity disclosed).
* The single accuracy defect is the stale engine/transcript hashes —
  RF1.

### A7. Label discipline — **PASS**

House labels (per `RESEARCH_STATE.md` and Cycle-5/6 precedent:
MACHINE-VERIFIED, ADVERSARIALLY REVIEWED, PROOF CANDIDATE,
UNFORMALIZED, PROVISIONAL, OPEN) are used consistently:
`corner_realizability.md` §6 gives the full status vector (finite
claims MACHINE-VERIFIED BY TWO INDEPENDENT IMPLEMENTATIONS; asymptotic
arguments ADVERSARIALLY REVIEWED — SOUND WITH REPAIRS, applied; CR-2
ADVERSARIALLY REVIEWED; UNFORMALIZED); `RESEARCH_STATE.md` repeats it
verbatim; the report presents Theorem CR only as "(adversarially
reviewed, repairs applied)" and never as proved/verified unqualified;
UNFORMALIZED is disclosed (no Lean layer this cycle); nothing labeled
PROVISIONAL is cited as settled.  No claim was found presented as
stronger than its label.  (The RF2/RF4–RF6 sentences are
evidence-description overclaims, not label violations.)

### A8. No new frontier bound, no complexity consequence — **PASS**

Report §0: "No new frontier bound is claimed."; §3: "no P-versus-NP
attempt; nothing in this cycle implies any complexity separation."
`RESEARCH_STATE.md` critical rule intact.  The only base "strictly
below 1.307031578" phrase anywhere is `cycle07_jc_validation.md` §6's
statement of the (then-open) Stage-I *target*, written at the Stage-V
gate before S7-C closed the route — a target statement, not a claim,
and superseded by the report.  Grep found no claimed improvement, no
new exponent, and no complexity-theoretic consequence in any cycle-7
document.

---

## Residual observations (no action)

* The mandate text for Cycle 7 is quoted in the cycle documents but not
  itself frozen in-repo; A1/A4 were audited against the
  coordinator-supplied wording plus the frozen S-A–S-D ancestors in the
  Cycle-6 selection audit.  Consistent; recording the mandate verbatim
  in future cycles would remove the dependency.
* `stage1_semantics.md` pins TR21-069 rev 1 at SHA `e4d634c4…` —
  matches `scheder_manifest.txt` exactly.
* The five breadth instances at n = 50 with i₁ ∈ {0.12, 0.24, 0.32}
  exceed Theorem CR's stated range m₁ ≤ n/10; they are correctly
  presented as machine-verified extra coverage, and CR-1 claims only
  the segment t ≤ 1/10 — no inconsistency.
* jc_validation's F1 paragraph and the checker agree that [JC26]'s
  printed "unrounded base 1.306972376565153…" equals 2^(p₀−1/15218)
  exactly — i.e., JC's *derivation* from the (false) printed constant is
  faithful; the attribution chain is coherent end to end.

## Bottom line

**INTEGRATION SOUND AFTER LISTED FIXES.**  Apply RF1–RF7 (all
documentation edits; no number, verdict, or label changes) before the
final commit.  With those applied, every claim in the cycle's summary
documents is backed by its cited artifact, internally consistent, and
within its label.

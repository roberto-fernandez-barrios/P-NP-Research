# Cycle 7 Stage V — evidence log (running)

**Started:** 2026-08-25.  **Branch:** `cycle07-o18-fable` (base `3918bd6`).
**Target:** hostile independent validation of [JC26] = Jiang–Cai,
*A Better Analysis For PPSZ For 3-SAT*, arXiv:2607.10697v1.

## V0. Source freeze (complete)

Live-web verification 2026-08-25 (~12:05–12:13 UTC):

* arXiv:2607.10697 exists; title *A Better Analysis For PPSZ For 3-SAT*;
  authors Tao Jiang, Shaowei Cai; **v1 only**, submitted
  Sun 12 Jul 2026 10:40:39 UTC (13 KB source); subject cs.DS.
  Abstract snapshot: `frozen_sources/arxiv_abs_2607.10697.html`.
* Artifact repository `github.com/jiangxioabai/A-Better-Analysis-For-PPSZ`
  exists; branch `main`; 2 commits; head
  `3e732e06fee90d10e31c157fb433699e7f766fdc` (2026-07-12T08:27:55Z,
  "Update README.md"); parent `324e8f1e…` ("Add files via upload",
  2026-07-12T08:26:42Z).  All fetches pinned to the head commit SHA.

Frozen files and SHA-256 (`frozen_sources/sha256_manifest_raw.txt`):

| file | SHA-256 | note |
|---|---|---|
| `jc_README.md` | `9fb22aae04cccc799e82943a2136bc2eef6d4883b2aa04729c555c599d8ab529` | repo README (blob `1cbee1ba…`) |
| `ppsz_certificate.json` | `d683abf6fad7ed6b9983c782ae4308a66511cbfb938106b7dac1ee9ebb2aca5c` | matches README's own checksum |
| `verification_output.txt` | `1b5a8779d9d65bb785f895ec6c46fd4a94b0a987f3dca19ef6e88209c2ff0879` | matches README checksum |
| `verify_ppsz_constants.py` | `1d29144b25b7a72de963787b587b804c443c3fef7ff3bfc33782a07ffd956be5` | committed as `verify_ppsz_constants(1) (1).py` (blob `f3f2d281…`); bytes match README checksum for `verify_ppsz_constants.py` |
| `arxiv_2607.10697v1.pdf` | `c2930b052b0d2da5186e09fc2297df6a1e777c1812c64b05f39daf28516b6db3` | 335,705 bytes |
| `arxiv_2607.10697v1_src.gz` | `30a0de3271e5b96c97caa5bdf4a764dad71f31f2cb5226c98438a1074110dd87` | e-print archive |
| `arxiv_src/a_better_analysis_for_ppsz_3_.tex` | `ec1a49684387e4dd3542d2239d8badaeafe6353db27558c70a78c8da0cdf9758` | full LaTeX source, 40,703 bytes |
| `arxiv_abs_2607.10697.html` | `0331d2cf43870d1fd7bfbcaa67b1aa52f10ab183dab54e6b09dddc7d07c14f68` | abs-page snapshot |

**Provenance anomalies (do not affect arithmetic; to report):**
1. Repo certificate is version `2026-07-12-rational-v5`; the paper's
   Appendix B says `2026-07-12-rational-v6`.  No v6 artifact is public.
2. README lists `REVISION_NOTES.md` with SHA-256
   `567c1f51345e3a436ad852eed4b80d83fe87b315d68e5702627239157bd6b86e`,
   but no such file exists in the repository at the head commit.
3. Checker committed under an upload-artifact filename with spaces and
   parentheses; bytes match the README's checksum for the clean name.

## V1. Authors' checker run (complete)

* Code inspected before execution: pure Python 3 stdlib (json,
  fractions, decimal-for-printing); no network/filesystem writes; no
  search; interval arithmetic with directed rounding by exact rationals;
  atanh-series ln with geometric tail bound (verified correct by
  inspection); Taylor exp with geometric tail (verified); binary-entropy
  and f_KL as in the paper.
* Run 2026-08-25 with Python 3.13.12:
  `python verify_ppsz_constants.py ppsz_certificate.json` → exit 0,
  final line `ALL CHECKS PASSED`.
* Transcript byte-identical to frozen `verification_output.txt` modulo
  CRLF (`diff --strip-trailing-cr`: no differences).  Saved as
  `frozen_sources/authors_checker_rerun_output.txt`.
* Noted: the authors' checker verifies sign/margin/enclosure claims and
  the containment of the paper's displayed intervals; it does NOT verify
  the 1/15218 one-dimensional endgame (background claim) — the
  independent checker covers that too.

## V2. LP reconstruction (complete)

`research_cycle_07/lp_reconstruction.md`: from-scratch re-derivation of
the two affine bounds from the four imports; the octant relaxation is in
the sound direction; dual certificate re-derived; **corner verified from
first principles: unique optimum at `(i_0, i_1, tau) =
(0, 0.060043244708778326…, 0)` with zero duality gap and strictly
positive dual slacks on `i_0` and `tau`** (subgradient optimality over
the octant, not certificate trust).  Hostile pass over all non-imported
proof steps: sound modulo the imports (details in that file, §6).

## V3. Parallel workstreams (launched 2026-08-25; interrupted once by a
## session usage limit and resumed/relaunched)

1. Independent exact-rational checker (arms-length) — **COMPLETE**
   (`checkers/independent_checker.py`, `_output.txt`, `_report.md`).
   90 sub-checks: **89 PASS, 1 FAIL (Finding F1, below)**; exit 1 by
   design to signal the finding.  Fractions throughout, own-derived
   tails (ln atanh N=120, exp Taylor N=100, both ≠ authors' N=90),
   outward 2⁻²⁵⁶ rounding; independence held (authors' checker and
   transcript never accessed).  All of [JC26]'s NEW-result arithmetic
   replicated: every sign, dual margin, γ*, corner equality
   (|L_reg−γ*|, |L_irr−γ*| < 10⁻⁷⁷), root-bracket signs, η intervals,
   branch margins, and all four base comparisons — strictly, with the
   tightest margin 4.15·10⁻¹⁴ (safe-branch margins over the claimed
   2.69/2.70·10⁻¹¹).  All 9 JSON `reported_intervals` contain the
   independent enclosures.  Bonus: Scheder's parameter pair (0.1,0.029)
   reproduces 0.0000657190847…, matching [JC26] App. A's claim.

   **Finding F1 (confirmed by a third, main-loop exact computation):**
   [JC26] eq. (2)'s terminal inequality
   `max{(1−irr)/10118 − 1/41391, irr/1380} ≥ 1/15218` is exactly FALSE.
   True minimax value: `v = 31273/475913718 ≈ 6.5711491006·10⁻⁵`,
   attained at `irr* = 7192790/79318953`; `v < 1/15218` with shortfall
   exactly `43/258659105733 ≈ 1.662·10⁻¹⁰`; the valid clean bound is
   `≥ 1/15219` (margin 4.15·10⁻⁹).  The denominator 15218 is a
   wrong-direction rounding of 15218.0385….  Impact (certified):
   [JC26]'s Theorem 1.1/Corollary 1.2 and the entire dual certificate
   never use eq. (2) — unaffected; `γ_new > γ_old` survives a fortiori;
   Scheder's ROUNDED published base 1.306972377 survives the correction
   (2^{p0−v} = 1.3069723767157… < 1.306972377, margin 2.8·10⁻¹⁰), but
   the "unrounded base 1.306972376565153…" that [JC26] print for
   Scheder is not the true value of the corrected endgame
   (true: 1.3069723767157…).  Attribution (JC transcription vs
   Scheder's own printed constant) pending ledger item I6.
2. Scheder import ledger (ECCC TR21-069 rev 1 + TheoretiCS), items
   I1–I10 — IN FLIGHT (relaunched fresh after transcript loss; PDFs
   already frozen: `scheder_tr21069_rev1.pdf`,
   `scheder_theoretics_24_5.pdf`, `scheder_arxiv_2207.pdf` +
   `scheder_manifest.txt`).
3. Scheder–Steinberger lifting ledger — **COMPLETE, verdict CLEAN**
   (`ss_lifting_import_ledger.md`, 43 KB; `ss_manifest.txt` 4 files).
   Highlights: SS journal version open access, all items
   journal-verified; L1 Main Theorem 1.17 UNCHANGED (SS's printed
   statement under-declares monotone/closure hypotheses which its own
   proof uses; JC add them — safe direction); L2 PARTIAL-attribution
   (the small-liquid restriction claim is an unproved in-proof assertion
   in SS; JC prove it themselves as Lemma C.1 — checked sound); L3
   UNCHANGED (SS Thm 1.10 addresses exactly JC's `P^(w)`; JC's
   width-3w bridge sound but not even needed); L4/L5 UNCHANGED
   (`p* = (2−log₂e)/2 = 1−1/(2ln2)`, `q0` digit-exact); L7 consistent
   (liquid = not frozen; under complete heuristic guessed iff liquid).
   Baselines: **no fetched source claims any general-3-SAT base at or
   below 1.307031578**; only prior explicit general decimal is Hertli's
   1.30704 (for a slightly modified PPSZ).  Deviations D1–D7 all
   attribution/normalization-level.
4. Novelty/frontier audit — **COMPLETE**
   (`novelty_frontier_audit.md`; 19 searches + 22 fetches logged).
   V-a JC frontier claim SUPPORTED (HKZZ 1.306995 and Qin–Watanabe
   1.306984 are Unique-only; AGR 2025 puts the frontier at Scheder
   ~1.307); V-b no follow-ups/v2/uptake (0 citations, repo untouched);
   V-c no better general bound found before or after JC; V-d the
   Stage-I idea (new structural inequality on critical-clause
   statistics in the recombination) has no prior art found.
   Key literature fact: Scheder's TheoretiCS 2024 version deliberately
   dropped the k=3 numeric part, stating in §1.4 that "a simple
   tightening of inequalities and a better choice of constants and
   functions would already yield a better bound" — exactly the
   tightening JC execute; but it means the imported §7.8/§8.4 displays
   live only in the unrefereed ECCC revision (I10 confirms pending).
   Caveats recorded: JC cite neither Hertli nor HKZZ nor QW; the "old"
   general base 1.307031594 is JC's own computation, published nowhere
   else.

## V4. Scheder import ledger (complete) and repair certifications

* Ledger delivered (`scheder_import_ledger.md`, I1–I10): transcription
  layer glyph-exact everywhere; hypothesis-layer mismatches → repairs
  R1 (ε_R = 0.10248 > printed 0.1 promise of Prop C.12; claimed range
  0.13 false), R2 (hidden Thr ≤ 1/1150), R3 (source's 256/600 rests on
  a false bound; corrected 64/600), R4 (TwoCC = closure-based
  Definition 31), R5 (fixed-w packaging is JC's, source proves only
  w(n) slowly growing); I6 confirms the 1/15218 constants are verbatim
  Scheder — so finding F1 is a SOURCE defect inherited by [JC26]'s
  background eq. (2).  I10: the refereed TheoretiCS version dropped the
  entire k=3 numeric part; imports I2–I6 live only in the unrefereed
  ECCC revision.
* Main-loop second-eyes pass on ECCC pp. 77–80 (rendered pages): Prop
  C.12/C.13 statements and proof structure confirmed as extracted;
  η/s/f/g definitions pinned.
* **Repair certification engine** (`checkers/repair_certifications.py`,
  main-loop implementation; exit 0; transcript
  `repair_certifications_output.txt`): ALL PASS —
  Part A: all four C.12 claims certified at ε_R (and at 0.1) in exact
  rationals via t = √(1−2r) piecewise-polynomialization; certified
  refutation of the source's "s′ ≤ 1.05 provided ε ≤ 0.13" at ε = 0.13
  (exact witness, s′ = 1.05 + 1.135·10⁻²);
  Part B: C.13(2) hairline margin 4.0·10⁻⁷ certified; full d-sweep
  5…161 certified by exact closed forms; d ≥ 162 chain certified
  (E(162) = 0.0977 ≤ 0.1);
  Part C: §8 closed forms re-derived by exact symbolic integration
  (all match the printed forms; the printed "JUNK₂ ≤ 0.000184" is
  certified FALSE, actual 2.0304·10⁻⁴, downstream 0.0028 still holds;
  Lemma-55 constant = −707/6 + 170·ln2 ≥ 0.001687, margin 3.6·10⁻⁷;
  BFS−DFB ≥ 0.030966, margin 5.2·10⁻⁷; m₂-values 5/21, 3721/181440
  (= half the printed aggregate 3721/90720), 15/14);
  Part D: ε_I admissibility under the corrected constraint; JC Lemma
  A.1 derivative bounds certified (exact factorization
  φ_TwoCC + 5 = (1/2−r)(160r²+20r+10));
  Part E: c_T robustness envelope margin 1.206·10⁻³, covering the
  unreconciled §7.7 recon concern 33.5×.
  Adversarial review of this script: agent in flight
  (`checkers/repair_certifications_review.md` when done).

## V5. VERDICT

**JC-SOUND-WITH-REPAIRS** — full statement, repairs R1–R5, finding F1,
provenance/publication-status findings, and the Stage-I gate decision in
`audits/cycle07_jc_validation.md`.  Repaired frontier unchanged:
general 3-SAT `O(1.307031578^n)`, Unique `O(1.306969598^n)`.
Stage I proceeds (falsification-first), with closure-based TwoCC
semantics (`research_cycle_07/stage1_semantics.md`).

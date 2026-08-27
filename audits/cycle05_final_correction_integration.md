# Cycle 5 final correction integration

**Date:** 2026-08-27

**Branch:** `cycle05-finalized`

**Audited candidate:** `cycle05-fable` at `18ba9cf4071f618113aa9657d847d44828c6da2d`

**Controlling audit:** `audits/cycle05_sol_final_cross_model_validation.md`
at `931341e4b180097b4ab2857ad31e84d700d110cc`

## Integration result

Every correction required by the Sol final cross-model audit has been
applied to the operative Cycle-5 proof, theorem, result, provenance,
novelty, certificate, and coverage text.  All repairs are
conclusion-preserving.  Defective historical arguments are retained only in
dated audit records where they are expressly labelled false or superseded;
they are not presented as alternative proofs.

O01 remains `OPEN`.  No statement about P versus NP was added or changed.
No merge was performed and no later research cycle was started.

## Mathematical correction map

| Sol-audit finding | Files changed | Exact resolution | Verification | Conclusion changed? |
|---|---|---|---|---|
| Theorem A status and composition provenance | `research_cycle_05/switch_structure_theory.md`; `RESEARCH_STATE.md`; `results/research_cycle_05.md`; `failure_knowledge.jsonl`; the three `experiments/cycle05_audit_thm_*` diagnostics | Froze the sound hypothesis as the precomposition relative map `pi_i^{-1} o pi_j`; retained the postcomposition form only as a falsified historical statement.  Tool output now calls its examples counterexamples to the discarded formulation. | Both stored counterexamples rechecked; affine and merge-clause exhaustive tests pass; the current A.2 proof includes the `|A|=q-3` boundary. | No |
| Theorem E parameter type | `research_cycle_05/dense_circle_obstruction.md`; summaries and ledger | Quantified `d` as a nonnegative integer, so every hull-chain index and the imported parameter `k=3d+5` are integral. | Exhaustive hull uniqueness/nestedness checks at `q in {11,13}`, `d in {1,2}` and pair-swap defect checks through `q=37` pass. | No |
| Theorem E common reference | Same theorem file and summaries | After one global relabeling, normalized only the common reference `O*=id`; removed the unsupported assertion `O*=O_1`. | Proof reread confirms that list membership of the reference is never used. | No |
| Theorem E FLSY range and copy quantifier | Same theorem file; `research_cycle_05/flsy_reconstruction.md`; summaries | States every finite integer `t>=1`, permits `d` to grow, and imports FLSY with the actual strict integer parameter `k=3d+5<(n-2)^(1/5)`.  The proof processes one accepting chain, so its conclusion is uniform in `t`. | Parameter inequalities and every theorem quantifier were rechecked; the finite theorem pipeline reports no violation. | No |
| SEG W1/W2/W3 and integrality (R3) | `audits/cycle05_seg_deep_independent_validation.md`; `audits/cycle05_seg_arms_length_referee.md`; `research_cycle_05/flsy_reconstruction.md`; `research_cycle_05/switch_structure_theory.md` | Replaced real-indexed first-passage shorthand by real-threshold W1, rounded W2, tracking radius `floor(d)`, integer passage level `delta=ceil(d)`, and the analytic inequality `ceil(3d)-2 floor(d)>=ceil(d)`.  No computed margin is used in the proof. | Exact hitting-time DP/formula/reflection checks, SEG grid self-tests, and the deterministic referee arithmetic all pass. | No |
| SEG offset first leg (R1) | Same SEG proof and referee files | Added `|z_1-h_0|>=ceil(3d)-|sigma'|>=2d>d`, proving `b_1>=1`; later legs use the maintained radius-`floor(d)` invariant.  The zero-length chaser event is empty once a milestone exists. | Direct proof reconstruction plus linear/cyclic chain-versus-grid exhaustive checks. | No |
| SEG tail arithmetic (R2) | Same SEG proof and referee files | Uses `K<=L/(6912d^3)`.  For the lower bound, splits exactly into `d^2 in [13824,27648)` using `K>=1`, and `d^2>=27648` using floor absorption, yielding `Kd>=L^(3/5)/27648` without a gap. | Referee exact-arithmetic checks and proof-level recomputation pass. | No |
| SEG cyclic full endpoint (R4) | Same SEG proof and referee files | Removed the defective length-`L-1` argument.  For each terminal split `u+v=L-1`, appends the last point to one extension walk, producing total grid length `L`; S3 is applied before the at-most-`L+1` union bound.  The old failure at `L=j^5+1` is explicitly labelled false. | Native cyclic DFS versus independent grid DP: 512,000 checks at `N=11`, zero mismatches; the referee full-`B` and cutpoint checks pass. | No |
| SEG final constant (R5) | Same SEG proof, referee, FLSY reconstruction, and theorem statement | Sets `C=6`, with explicit `c=min{1/2,(1/6)^2/(8*27648^2)}` and `L_0=ceil(13824^(5/2))`. | Final union-bound bookkeeping recomputed in both proof audits. | No |
| SEG provenance and strict FLSY boundary | `research_cycle_05/flsy_reconstruction.md`; SEG proof/status files; summaries | Classifies SEG as `NEW BUT PROVED IN THIS REPOSITORY`, not published verbatim.  Separates the published Fréchet/milestone/first-passage engine from the repository grid, offset, rounding, first-leg, and cyclic-full lemmas.  Keeps FLSY's actual integer `k<N^(1/5)` rather than the source display's non-strict enlargement at perfect fifth powers. | Primary-source reconstruction and Sol audit provenance check incorporated; no citation is substituted for a repository proof step. | No |
| Theorem C integer segment length | `research_cycle_05/switch_structure_theory.md`; SEG deep proof consequence section; summaries | Replaced the false real run-length claim by `M=floor((q-7)/(D+1))`; for `L*=(q-7)/(D+1)>=2`, uses `M>=L*/2` and absorbs `2^(1/5)` into the decay constant.  SEG is applied with ambient `N=q`, total `sigma=+1`, `k=2`, and a proper cyclic endpoint. | Block-count arithmetic independently reread; switch-depth finite DP passes at `q=13,17,21`. | No |
| Theorem F run sandwich and two branches | `research_cycle_05/switch_structure_theory.md`; SEG deep proof consequence section; summaries | Extended Lemma RS to every finite state, explicitly covering sizes `1`, `2`, `q-2`, and `q-1`.  The long-run branch uses SEG with `k=2`; the short-run density branch separately uses published FLSY with `k=11+3 floor(n^(1/5)/7)<(n-2)^(1/5)` for sufficiently large `n`. | Endpoint cases and both strict ranges independently reread; SEG and Theorem-E checks pass. | No |
| Arbitrary-list `D_mid` | `research_cycle_05/switch_structure_theory.md`; summaries | Defines `D_mid(P)` by the minimum partition of the middle states into consecutive blocks having nonempty common label intersection, maximized over chains. | For `t=2`, equivalence with the exact alternation DP was checked on the committed range. | No |
| Switch count wording | `research_cycle_05/hybrid_definitions.md`; summaries | Defines switch count as the minimum adjacent label changes; equivalently one less than the minimum number of disjoint common-label blocks.  Endpoint-sharing is now only a geometric representation, not a second overlapping partition definition. | Certificate verifier independently recomputed minimum switch count. | No |
| Pair-swap construction and scope | `research_cycle_05/switch_structure_theory.md`; `research_cycle_05/dense_circle_obstruction.md`; summaries and ledger | Prepended `I_3={0,1,3}` and common `I_4={0,1,2,3}`.  Claims only the all-`q` lower bound `D_mid>=(q-7)/2`; equality is restricted to exact-DP-certified `q in {13,17,21}`.  The displayed odd-`q` pair-swap order ends with `q-2,q-3,q-1`. | Exact DP reproduces depths `3,5,7`; pair-swap defect checker passes. | No |
| Transposition scope | `research_cycle_05/README.md`; `results/research_cycle_05.md`; `RESEARCH_STATE.md`; `failure_knowledge.jsonl` | Keeps the all-`q` `D_mid<=1` case analysis as a proof candidate and limits exact claims to finite DP evidence. | Exact committed switch-depth table rerun. | No |

## Computational, provenance, novelty, and coverage correction map

| Sol-audit finding | Files changed | Exact resolution | Verification | Conclusion changed? |
|---|---|---|---|---|
| `n=24` distinct-record wording and schema | `results/research_cycle_05.md`; `RESEARCH_STATE.md`; `research_cycle_05/README.md`; historical audit amendments | Everywhere current-facing: **14,864 stored records**, **8,258 distinct `(permutation, word)` examples**, **6,606 duplicate `swap`/`xswap` labels**.  The README states that `n=24` lacks the `min_switches` and `canonical` fields. | Independent verifier reproduced all three counts, 440 permutations, 414 words, and switch count 1 for every record. | No |
| `n=22` annotation provenance | `research_cycle_05/README.md`; `research_cycle_05/hybrid_definitions.md` | Labels `min_switches` and `canonical` as separately verified manual postprocessing not reproduced by the committed generator; reproduction writes to a scratch file. | All 122 stored records and annotations independently verified. | No |
| Transposition rescue threshold | `results/research_cycle_05.md`; `RESEARCH_STATE.md`; `failure_knowledge.jsonl` | States zero rescue through distance 8 and exact rescuing distances `{9,10}` at `n=22`. | Independent finite verifier reproduced the full distance profile. | No |
| Percentage/range wording | Same summaries, ledger, and structure theory | Uses `85.6--87.9%` for exhaustive `n=24..34` and `85.7--87.9%` for pair-swap at `n=24,26,28,30`. | Recomputed from committed scan counts. | No |
| Uncommitted diagnostic provenance | `results/research_cycle_05.md`; `RESEARCH_STATE.md` | Labels `revB`, bit-reversal, xor-block, shifted-pair-swap, and the sampled `n=42` triple where applicable as non-reproducible diagnostics rather than canonical evidence. | Stale-provenance scan confirms no generator claim remains. | No |
| SEG/C/F epistemic labels | Operative theorem files, `RESEARCH_STATE.md`, results, README, `failure_knowledge.jsonl`, barrier and historical audit notices | Records SEG/C/F as `ADVERSARIALLY REVIEWED PROOF CANDIDATES; UNFORMALIZED`, with all Fable and Sol repairs applied and C/F's dependency on SEG explicit.  Removes the misleading “conditional on an unproved SEG” label without presenting SEG as published or formalized. | Cross-document status scan completed. | No |
| N1--N5 and broad hybridity prior art | `research_cycle_05/novelty_audit_theorems.md`; `research_cycle_05/common_interval_literature.md`; `literature/novelty_log.md`; README, results, state, and audit amendments | N1 and aggregate N4 are `UNCLEAR`; narrow N2/N3 are `POTENTIALLY NOVEL`; N5's literal-union object is `KNOWN` from FLSY Lemma 2.3; RR-specific N5 analysis is at most `POTENTIALLY NOVEL`; SEG novelty is `UNCLEAR`.  Records Algaba--van den Brink--Dietz Example 4.7 as prior art for the broad extra-chain phenomenon.  No Cycle-5 item retains strong novelty support. | Repository-wide stale-novelty scan performed; generic verdict-scale text is retained only as a scale and expressly awards no item its top category. | No |
| Infinity-moving scope | `results/research_cycle_05.md`; `RESEARCH_STATE.md`; structure theory | States that a common moved anchor globally reduces to the infinity-fixing case; only different-anchor/general infinity-moving lists remain outside. | Relabeling scope reread against Theorem A/E/C/F hypotheses. | No |
| Literature-search count | `results/research_cycle_05.md`; README/state novelty summaries | Replaces “approximately 40 searches” by “20 documented query strings plus direct source/catalog scans.” | Counted the numbered queries in the novelty audit. | No |
| Formal coverage and build count | `formal/coverage.md`; current summaries | Records the clean 8,663-job pinned build and standard-axiom audit.  Explicitly leaves literal `RR_n`, Theorems A/E/C/F, SEG/RS/M, and every probability/asymptotic statement unformalized. | A genuine `lake clean` followed by `formal/check.ps1` completed all 8,663 jobs.  The eleven-family axiom audit reports only `propext`, `Classical.choice`, and `Quot.sound`. | No |
| Historical disposition tables | `audits/cycle05_final_integration_disposition.md`; `audits/cycle05_fable_independent_validation.md`; `audits/cycle05_final_integration_adversarial.md`; `audits/cycle05_seg_lemma_adversarial.md`; `audits/cycle05_theorems_adversarial.md`; `audits/barriers/cycle05_hybrid_obstructions.md` | Added precise supersession notices and current statuses while preserving the dated findings as audit history. | Repository-wide stale-status scan; every surviving defective formula is in an explicitly false/superseded discussion. | No |

## Regression and independent verification

The following checks were run after applying the corrections:

1. `python -B experiments/cycle05_hybrid_core.py` -- PASS.
2. `python -B experiments/cycle05_switch_depth.py` -- exact pair-swap depths
   `3,5,7` at `q=13,17,21`; recorded affine/transposition/block-swap values
   reproduced.
3. `python -B experiments/cycle05_audit_thm_lemmas.py` -- all Theorem-A and
   Theorem-E lemma checks PASS, including the repaired A.2 boundary.
4. `cycle05_audit_thm_pipeline.cpp --selftest` plus
   `cycle05_audit_thm_diffsmall.py` -- PASS; zero differential mismatches at
   `n=10,12` for pair-swap and multiplier controls.
5. `cycle05_audit_thm_a_counterexample.py 0` and `1` -- both discarded
   postcomposition counterexamples reproduced; neither satisfies the repaired
   precomposition hypothesis.
6. `cycle05_audit_seg_selftest.py` -- PASS for all listed exact coloring/DP
   configurations.
7. `seg_bruteforce_chains.py` -- linear 614,400 and cyclic 512,000 checks,
   zero mismatches.
8. `seg_engine.cpp` plus `seg_battery.py xval` -- translation exact; C++ and
   Python probabilities agree in all five configurations.
9. `seg_referee/referee_checks.py` -- all W1/W2/S1/S2, unconditioning,
   monotone-decay, offset, parity, and split checks PASS; 24,000 DP self-test
   cases and the listed exhaustive chain checks have zero mismatches.
10. Independent C++ enumeration of every normalized word at even
    `n=2,4,...,24` returned rejected counts
    `0,0,0,0,0,0,0,0,0,0,21,414`; therefore the first hybrid-only
    opportunity is `n=22`.
11. `verify_finite_claims.py` checked all five manifest blobs, every stored
    witness chain, per-copy rejection, literal-union acceptance, switch count,
    the canonical `n=22` example, infinity-moving samples, and the complete
    transposition profile.  It reproduced `n=22: 122/122 switch-one` and
    `n=24: 14864 records, 8258 distinct, 6606 duplicates, 14864/14864
    switch-one`.
12. `failure_knowledge.jsonl` parses as 39 JSON objects with 39 unique IDs.
13. A genuine clean Lean run (`lake clean`, then `formal/check.ps1`) built
    all 8,663 jobs and passed the forbidden-token scan.  The separate
    eleven-family kernel audit reports only `propext`, `Classical.choice`,
    and `Quot.sound`.
14. `git diff --check` reports no whitespace error.  Generated executables
    and scratch dumps were removed after testing.
15. Repository-wide searches found no live `14,864 distinct` claim, no live
    strong Cycle-5 novelty classification, no current “conditional on
    unproved SEG” status, and no prose expanding Lean's scope.  Historical
    counts and invalid derivations occur only in clearly dated or superseded
    audit records.

## Diff inspection

The complete diff against `cycle05-fable` was inspected by changed-file
list, statistics, whitespace check, and content review.  It contains the Sol
audit/tooling commit, the conclusion-preserving corrections mapped above,
and this integration report.  No certificate payload, Lean theorem source,
master branch, or unrelated research-cycle artifact was modified.

## Final epistemic state

| Item | Final Cycle-5 status |
|---|---|
| THEOREM A | Validated; repaired precomposition statement sound as stated |
| THEOREM E | Sound with all conclusion-preserving repairs applied |
| SEG | Complete repository proof with Fable and Sol repairs applied; cross-model adversarially validated; unformalized |
| THEOREM C | Sound with repairs; adversarially reviewed proof candidate depending explicitly on SEG; unformalized |
| THEOREM F | Sound with repairs; adversarially reviewed proof candidate depending explicitly on SEG; unformalized |
| HYBRID MINIMALITY | Independently confirmed at `n=22`; all verified witnesses have minimum switch count 1 |
| CERTIFICATES | Validated with corrected record/distinct/duplicate wording |
| FORMAL COVERAGE | Clean, pinned, and restricted to the accurately listed deterministic core |
| NOVELTY | Conservative bounded-search classifications; no unjustified strong claim |
| O01 | OPEN |

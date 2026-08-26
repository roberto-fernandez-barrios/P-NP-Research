# Research Cycle 5 artifacts: hybrid multi-order routing

**Base commit:** `745f2bdf8b6d1e472279da913245aa048b36112c`
**Branch:** `cycle05-fable`
**Summary report:** `../results/research_cycle_05.md`

## Documents

| File | Content |
|---|---|
| `hybrid_definitions.md` | Phase 5A: provenance-invariant definitions (label sets, pure/hybrid chains, switch counts, `H/I/G`), interval-walk reformulation (Lemma 5A.1), one-switch normal form, subset accounting |
| `switch_structure_theory.md` | Phases 5B/5E/5H: Theorem A (affine ⟹ `G = 0`, unconditional); transposition `D_mid ≤ 1` (all-`q` proof candidate, finite-DP checked); pair-swap `D_mid ≥ (q-7)/2` for all odd `q` (equality finite-DP checked); SEG, C, and F (`ADVERSARIALLY REVIEWED PROOF CANDIDATES; SOUND WITH APPLIED REPAIRS; UNFORMALIZED`, with C/F explicitly dependent on SEG); Lemma M (open `t ≥ 3` gap); relaxed positive target |
| `dense_circle_obstruction.md` | Theorem E: unconditional `t`-independent obstruction for common-reference `D`-dense circle lists, for integer `D ≥ 0` with `D = o(n^{1/5})`; kills pair-swap-type families |
| `flsy_reconstruction.md` | Primary-source verification of the named Cycle-4 FLSY imports; reconstruction of the interval theorem's proof mechanism and upper-bound construction; SEG is **NEW BUT PROVED IN THIS REPOSITORY**, not a theorem published verbatim by FLSY; multi-order `Σ_π` treatment; follow-up/withdrawal status |
| `common_interval_literature.md` | Cited survey: linear/circular common intervals, strong interval trees, counts/randomness, multiplication maps, and the boundary between known feasible-word/extra-chain phenomena and the exact interval-specific quantitative theory |
| `novelty_audit_theorems.md` | Original Phase-8 search log (20 documented query strings plus source/catalog scans); final cross-model classification: N1 and aggregate N4 `UNCLEAR`, narrow N2/N3 `POTENTIALLY-NOVEL`, N5 literal-union object `KNOWN` from FLSY Lemma 2.3, RR-specific structural analysis at most `POTENTIALLY-NOVEL` |

Scope note: a list whose copies move the distinguished point to one common
anchor is globally relabeling-equivalent to the ∞-fixing setting.  The open
∞-moving boundary means different-anchor or otherwise non-reducible lists.

## Experiments (all under `../experiments/`)

| File | Role |
|---|---|
| `cycle05_hybrid_core.py` | From-scratch core library: literal families, brute-force induced-DAG reference, fast multi-order interval DP with cross/eq arrows, witness extraction + independent chain checking, single-copy recurrence, self-tests (`python -B experiments/cycle05_hybrid_core.py`) |
| `cycle05_hybrid_only_search.py` | Phase 5C structured search (word-preserving and cross-orbit arc moves, random coset control); reproduces raw finds but not the stored `n=22` annotation fields |
| `cycle05_verify_hybrid_certificates.py` | Independent certificate checker (reference DPs only) + exact minimum-switch computation |
| `cycle05_union_scan.cpp` (`.exe`) | Exact exhaustive / sampled two-copy scans; `--list-cross` structural profiles; `CYCLE05_DUMP_COMMON=1` per-word dumps |
| `cycle05_run_scans.py` | Experiment battery driver (`trans`, `blocks`, `controls`, `big`, `sample`) |
| `cycle05_switch_depth.py` | Exact finite-instance middle switch-depth DP; its outputs are not an all-`q` proof |
| `cycle05_infmoving_probe.py` | Different-anchor ∞-moving relabeling probe (reference semantics only) |
| `cycle05_triple_probe.py` | Three-copy probe {id, pair-swap, shifted pair-swap}, exhaustive `n=28` + sampled `n=42` |
| `cycle05_audit_*` | Scripts written by the independent adversarial reviewers |

## Certificates (all under `../certificates/cycle05_hybrid/`)

| File | Content |
|---|---|
| `hybrid_only_n22_candidates.json` | 122 verified `n = 22` hybrid-only examples; transposition distances `δ ≤ 8` rescue none and the rescuing distances are exactly `{9,10}`; `min_switches` and `canonical` were added by separately verified manual postprocessing not reproduced by the committed search generator |
| `hybrid_only_n24_candidates.json` | 14,864 verified stored records, representing 8,258 distinct `(permutation, word)` examples; 6,606 records duplicate a find under `swap`/`xswap` labels.  This artifact does not store the `min_switches` or `canonical` fields used by the `n=22` schema; minimum switch count 1 was independently recomputed for every record |
| `scan_results.jsonl` | Every scan row: family tag, exact/sampled counters (`total, rej1, rej2, commonrej, rescued, unionrej`) |
| `infmoving_probe_n22.json` | 32 ∞-moving hybrid-only finds among 550 probed candidates (reference semantics) |
| `triple_probe.json` | Three-copy counters: `n = 28` exhaustive (3 union rejects of 20,058,300), `n = 42` sampled |
| `cycle05_hybrid_SHA256SUMS.txt` | SHA-256 manifest of the certificate payloads (LF byte-stable via `.gitattributes`) |

## Audits (under `../audits/`)

* `cycle05_theorems_adversarial.md` — independent adversarial review of Theorems A and E (found and repaired the Theorem-A composition-order bug; differential-evidence dumps `audit_*`/`proposer_*`/`*.sorted` alongside)
* `cycle05_seg_lemma_adversarial.md` — first skeptic review of Lemma SEG against the primary source
* `cycle05_seg_deep_independent_validation.md` — independent proof reconstruction
* `cycle05_seg_arms_length_referee.md` — arms-length R1–R5 proof repairs
* `barriers/cycle05_hybrid_obstructions.md` — Phase-7 barrier audit
* `cycle05_final_integration_adversarial.md` — final repository-level integration audit
* `cycle05_sol_final_cross_model_validation.md` — final cross-model hostile validation; supersedes earlier SEG/novelty status judgments where they differ

## Reproduction quick reference

```powershell
python -B experiments/cycle05_hybrid_core.py                      # core self-tests
# NOTE: point --out at a scratch path.  In the stored n=22 artifact,
# min_switches/canonical were separately checked manual annotations; this
# generator emits raw finds and does not reproduce those fields.
python -B experiments/cycle05_hybrid_only_search.py --n 22 --out hybrid_only_n22_rerun.json
python -B experiments/cycle05_verify_hybrid_certificates.py certificates/cycle05_hybrid/hybrid_only_n22_candidates.json
g++ -O2 -std=c++17 -o experiments/cycle05_union_scan.exe experiments/cycle05_union_scan.cpp
python -B experiments/cycle05_run_scans.py trans                  # etc.
python -B experiments/cycle05_triple_probe.py                     # t=3 probe
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1       # Lean build
```

Format note: `certificates/cycle04_rr_acceptance/cycle04_rr_failures_n*.txt`
store binary words (length `q`, LSB = position 0 at the right);
`certificates/cycle04_multi_rr/*_failure_necklaces_*.txt` store hex.  The
Cycle-5 parsers validate length and weight after parsing.

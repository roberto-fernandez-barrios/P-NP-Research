# Post-correction disposition: TR26-043 true-filtration reconstruction

**Date:** 2026-08-21  
**Prior audit:** [`cycle02_true_filtration_adversarial.md`](cycle02_true_filtration_adversarial.md)  
**Disposition:** **PASS.** All requested corrections from the prior audit are present and internally consistent. No remaining defect was found within this narrow correction scope.

No integration artifact was edited and nothing was committed during this disposition.

## Correction-by-correction result

| Correction | Disposition | Evidence |
|---|---|---|
| Current retraction status | **PASS** | The report now identifies official ECCC Revision 1, dated May 11, 2026, as a one-page retraction note acknowledging the Lemma 4.1 conditional-filtration gap and dependence of all paper results on that lemma. The certificate records the direct Revision-1 URL and the independently verified SHA-256 `a3a6251ce8b4f859046656bba1e09582ed7bcb12409c63c9fb126758f1e89363`. It also correctly separates the retraction's general acknowledgement from the repository's exact finite minima. |
| Complete-path policy label | **PASS** | Section 7 now explicitly introduces the displayed atom-count table with “Under eager comparison.” |
| First-exhaustion policy labels and counts | **PASS** | The report states eager `9,664` and query-minimal `9,488` terminal filtration atoms, total mass one under each policy, and the shared residual law. The certificate has `reveal_policy: eager` plus a separate query-minimal comparison containing `9,488`. |
| Query-minimal stopping regression | **PASS** | `test_first_exhaustion_distribution` now checks minimal total mass, `9,488` terminal atoms, equality of both residual distributions and odd masses, and 35 reachable probe subsets. |
| Eager/query-minimal martingale summary | **PASS** | Section 9 now says the smallest eager active witness is `n=4` and the query-minimal active minimum is `n=6`. |
| `SCALE_START`/`RECURSE` phase reconciliation | **PASS** | The schema phase enum now contains `SCALE_START` and no longer contains the unused `RECURSE`; it agrees with the multiscale transition endpoints at the design-contract level. |
| Frontier status/value schema | **PASS** | The frontier `oneOf` now has three disjoint cases: `null`, `UNREVEALED` with no permitted value, and `REVEALED_UNCONSUMED` with required value in `{-1,+1}`. |
| Design-level, non-trace contract | **PASS** | Both schema and transition JSON explicitly say they are design-level contracts rather than serializers/validators for the Python enumerator's lowercase trace events. The schema `$comment` lists the semantic invariants checked externally. This resolves the previous interface ambiguity without pretending to provide a serialization pipeline. |
| `U4` logarithmic constant | **PASS** | The report and transition JSON retain the primary missing-lower-bound defect and now also state that division by two requires additive `(3/2)ln 2 ≈ 1.03972`, so the printed `+1` implication is false even if the unsupported lower bound is assumed. |
| Odd recursive residual witness | **PASS** | The report gives the explicit family `n=2k`, odd `k>=701`: alternating left signs with sum `+1`, a right half of sum `-1` with positive first frontier, and left choices at zero-height ties. This exhausts the left block with zero right progress and leaves an odd residual of recursive size `k`. |
| Ambiguous certificate names | **PASS** | The eager smallest certificates are now named `lemma_4_1_eager_minimal_certificate` and `lemma_3_3_eager_active_minimal_certificate` and each contains `reveal_policy: eager`. |

## Executable verification

The full targeted suite was rerun:

```text
python -B experiments/test_tr26_043_true_filtration.py -v
```

Result: **8 tests passed** in approximately six seconds:

- exact probability mass;
- first-exhaustion distribution under both policies;
- independent complete-coloring cross-check;
- maximum forced probabilities;
- parametric first-step atom;
- reachable prefix-pair counts;
- all smallest-counterexample classifications;
- state invariants.

Direct reruns of first exhaustion returned:

| Policy | terminal atoms | mass | odd residual mass |
|---|---:|---:|---:|
| eager | `9,664` | `1` | `997/1792` |
| query-minimal | `9,488` | `1` | `997/1792` |

## JSON and structural verification

All four relevant JSON files parse successfully:

- [`tr26_043_true_process_state.schema.json`](../research_cycle_02/tr26_043_true_process_state.schema.json)
- [`tr26_043_v0_transition_system.json`](../research_cycle_02/tr26_043_v0_transition_system.json)
- [`tr26_043_true_filtration_counterexamples.json`](../certificates/tr26_043_true_filtration_counterexamples.json)
- [`tr26_043_n10_reachable_probe_subsets.json`](../certificates/tr26_043_n10_reachable_probe_subsets.json)

Additional programmatic assertions confirmed:

- `SCALE_START` is present and `RECURSE` absent from the phase enum;
- the two non-null frontier variants enforce the corrected value rules;
- the design-level/non-serialization contract is explicit;
- certificate stopping counts are `9,664` and `9,488` under the named policies;
- the recorded Revision-1 hash is exact;
- `U4` contains the `(3/2)ln 2` correction;
- all corresponding report passages are present.

## Remaining limitations, not correction failures

The schema intentionally remains a design-level contract and does not validate enumerator traces or all mathematical state invariants. This is now explicit rather than an integration defect. The reconstruction also remains unformalized, and none of these corrections establish the numerical tail bound, the withdrawn v0 theorem, O01, or the unrestricted balanced-chain target.

**Final disposition: PASS; prior audit corrections are closed.**

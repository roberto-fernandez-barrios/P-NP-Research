# Final integration disposition

**Date:** 2026-08-13
**Scope:** disposition of the three independent read-only integration audits
before freezing research cycle 1.

The validator reports are retained unchanged as audit evidence:

* [`final_integration_circuits.md`](final_integration_circuits.md);
* [`final_integration_proof_sat.md`](final_integration_proof_sat.md); and
* [`final_integration_meta.md`](final_integration_meta.md).

Their material findings were applied to the canonical Phase 0/1 files as
follows.

| Finding | Disposition |
|---|---|
| O04 mixed all-threshold MCSP with a fixed threshold slice. | O04 and K18 now use the all-threshold language `(x,theta)` throughout. |
| O22 called the CCC 2022 `B_2` gate frontier a wire frontier. | O22 now counts fan-in-two `B_2` gates and quantifies one admissible nondecreasing threshold function. |
| O20, O21, and O24 were directions rather than truth-valued statements. | Replaced by, respectively, `NEXP` versus polynomial `THR o THR`, an explicit-P super-`n^{5/2}` threshold-wire target, and the exact STACS small-`mu` deterministic one-tape target. |
| O14 did not freeze CDCL semantics. | Replaced by a global simulation question with unit propagation, arbitrary decisions, 1-UIP learning, no restarts, permanent learned clauses, and conflict count as size. |
| O19 used the unquantified denominator `log^{o(1)} n`. | Frozen to `exp(sqrt(log log n))` in Tamaki's exact depth-two SYM/THR model. |
| O06 omitted the field, graph-family, and charge quantifiers. | Frozen to an existential fixed field, explicit connected simple 4-regular expander family, and odd Tseitin charges. |
| O13 was a repository-defined repair whose structure was only in a draft. | Its `Phi/Psi`, closure, collision predicate, and quantitative union statement are now visible in `open_problems.md`; status is `OPEN AFTER SEARCH`, potentially false, and not novelty-audited. |
| The O01 DAG edge pointed toward an mABP separation. | Replaced by the exact FLSY implication: over every infinite field O01 yields a nonuniform full-rank family of mABP size `O(n^{C+1})`; no progress edge to `mVBP!=mVP` remains. |
| Hardness/randomness and PIT edges overstated their conclusions. | The `E`-hardness theorem has no NP-circuit edge; the PIT disjunction is recorded without splitting it into two implications. O10/O19 no longer point to a general circuit lower bound. |
| Algebraic endpoints lacked fields. | The canonical graph now fixes characteristic zero for `VP`/`VNP` and an infinite field for the general multilinear-ABP endpoint. |
| Internal counterexamples could be mistaken for external/formal results. | Every canonical summary now labels them internally adversarially reviewed and `UNFORMALIZED`; no novelty or external-review claim is made. |
| Ranking ties and shortlist wording were ambiguous. | Candidate ID is the final stable tie-breaker; all 25 targets are ranked, exactly five are shortlisted, and exactly one is selected. |

Replacing the three unfrozen candidates changes the shortlist to exactly
`O01, O03, O02, O18, O05`.  It does not change the sole selection, O01.

The audits also identified a broken hard-clique link, an incorrect STACS 2021
paper title, and several proof-model wording issues; these were corrected.
All remaining uncertainty labels are intentional and appear in the canonical
state rather than being silently resolved.

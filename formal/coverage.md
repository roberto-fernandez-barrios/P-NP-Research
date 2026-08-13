# Formal verification coverage

**Updated:** 2026-08-13.  No Lean project or machine-checked theorem was
created in research cycle 1.  Computational checking is recorded separately
and is not formal proof.

| Result / definition | Coverage | Evidence and next obligation |
|---|---|---|
| Balanced coloring, maximal chain, chain imbalance, 1-balanced-chain system, `N(n)` | UNFORMALIZED | Definitions copied from FLSY TR26-001.  First Lean target in cycle 2. |
| FLSY worst-case-from-average symmetrization | UNFORMALIZED | Source proof checked informally.  Formalization should separate finite counting from probabilistic existence. |
| Withdrawn TR26-043 two-block process and filtration | UNFORMALIZED | Independent human reconstruction found explicit failures.  Formalize the actual revealed state before any probability lemma. |
| `n=10` counterhistory to TR26-043 Lemmas 4.1 and 3.3 | UNFORMALIZED | Exact rational derivation plus `experiments/verify_balanced_chain_counterhistory.py`; computational checking is not formal verification. |
| Polynomial 1-balanced-chain target O01 | UNFORMALIZED | OPEN; only a target, not a theorem. |
| Counterexample to Alekseev--Gaevoy Conjecture 1.4/4.2 | UNFORMALIZED | Parametric proof independently reconstructed; finite coordinate instance checked by `experiments/verify_affine_union_counterexample.py`. |
| Finite affine-union instances at `L=3,5` | UNFORMALIZED | Computationally tested: enumeration asserts exact cover/private-layer identities, but no proof assistant checked them. |

The Phase 0/1 dependency DAG and rankings are non-theorem research artifacts,
so no formalization-status label is assigned to them.  Citations and
independent audits, rather than a proof assistant, are their validation
mechanism.

## Planned Lean order for O01

1. finite balanced colorings and maximal chains;
2. certificate checker for a finite 1-balanced-chain family;
3. exact transition histories for a two-block process;
4. the `n=10` conditional-probability counterexample;
5. FLSY symmetrization; and
6. any new supermartingale/stopping-time lemma only after its filtration is
   fixed.

No entry is `PARTIALLY FORMALIZED` or `FULLY FORMALIZED` in this cycle.

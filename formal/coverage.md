# Formal verification coverage

**Updated:** 2026-08-21. No Lean project or machine-checked theorem was
created in Research Cycles 1 or 2. Computational checking is recorded
separately and is not formal proof.

| Result / definition | Coverage | Evidence and next obligation |
|---|---|---|
| Balanced coloring, maximal chain, chain imbalance, 1-balanced-chain system, `N(n)` | UNFORMALIZED | Definitions copied from FLSY TR26-001. First Lean target if a later O01 cycle is authorized. |
| FLSY worst-case-from-average symmetrization | UNFORMALIZED | Source proof checked informally.  Formalization should separate finite counting from probabilistic existence. |
| Withdrawn TR26-043 two-block process and filtration | UNFORMALIZED | Exact state reconstruction, schema, transition relation, and independent audit exist. The JSON schema is design-level, not a proof assistant or trace validator. |
| Smallest TR26-043 counterhistories under eager/query-minimal reveals | UNFORMALIZED | Exact rational enumeration and an independent complete-coloring implementation certify the stated minima through `n=10`; no proof assistant checked them. |
| Exact `N(2)=3,N(4)=6,N(6)=12,N(8)=20` | UNFORMALIZED | MILP witnesses, standard-library exhaustive lower checker, and a third independent implementation agree. This is computational certification, not formal verification. |
| CF-LOGGAP cached-frontier logarithmic-gap obstruction | UNFORMALIZED | Written primitive-Dyck proof and independent adversarial audit pass for the precisely restricted process/tail contract. A Lean development should formalize sampling without replacement, primitive Dyck counting, and uniform bounded-`d` asymptotics. |
| Variable-threshold reserve lemma | UNFORMALIZED | Elementary inequalities independently checked; it is not a complete scale transition. |
| Geometric-log distinct-subset accounting | UNFORMALIZED | Written geometric-series proof independently checked under globally quantified description families. |
| Polynomial fixed-order recursive-cover obstruction | UNFORMALIZED | Uses FLSY Lemma 3.2 plus a union bound; the cited source theorem itself has not been formalized here. |
| Polynomial 1-balanced-chain target O01 | UNFORMALIZED | OPEN; only a target, not a theorem. |
| Counterexample to Alekseev--Gaevoy Conjecture 1.4/4.2 | UNFORMALIZED | Parametric proof independently reconstructed; finite coordinate instance checked by `experiments/verify_affine_union_counterexample.py`. |
| Finite affine-union instances at `L=3,5` | UNFORMALIZED | Computationally tested: enumeration asserts exact cover/private-layer identities, but no proof assistant checked them. |

The Phase 0/1 dependency DAG and rankings are non-theorem research artifacts,
so no formalization-status label is assigned to them.  Citations and
independent audits, rather than a proof assistant, are their validation
mechanism.

## Planned Lean order if O01 work is later authorized

1. finite balanced colorings and maximal chains;
2. certificate checker for a finite 1-balanced-chain family;
3. exact transition histories for a two-block process;
4. the eager `n=8` and query-minimal `n=10` conditional-probability
   counterexamples;
5. the CF-LOGGAP primitive-Dyck obstruction;
6. FLSY symmetrization; and
7. any new supermartingale/stopping-time lemma only after its filtration is
   fixed.

No entry is `PARTIALLY FORMALIZED` or `FULLY FORMALIZED` in this cycle.

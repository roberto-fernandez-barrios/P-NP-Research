# Research Cycle 3 artifact index

Research Cycle 3 is the structural-DAG attack on O01.  The integrated report
is [`results/research_cycle_03.md`](../results/research_cycle_03.md).
O01 remains **OPEN**; no finite computation in this directory has an
asymptotic implication.

## Hardened foundation and literature

- [`foundation_independent_audit.md`](foundation_independent_audit.md)
  independently rechecks the path-DAG reformulation, Lemmas S1/S2,
  `tau`/`sigma`, and the scope boundary around CF-LOGGAP.
- [`literature_novelty_audit.md`](literature_novelty_audit.md) updates the
  primary-source and equivalent-object search through 2026-08-21.  Negative
  searches are recorded only as `PRIOR-ART-NOT-FOUND`.

## Exact finite frontier

- [`exact_n10.md`](exact_n10.md) records the exhaustively checked finite
  determination `N(10)=35`, with no asymptotic inference.
- [`certificates/balanced_chain_n10/README.md`](../certificates/balanced_chain_n10/README.md)
  indexes the standard-library lower and upper certificates.
- Run `python -B experiments/check_balanced_chain_n10_exact.py` from the
  repository root to recompute the exact finite certificate.

## Structural classes, recursion, formalization, and audits

- [`cp_s_recursion_attack.md`](cp_s_recursion_attack.md) defines and rejects
  the literal two-rail and quadratic-width star spines, and isolates the
  unproved one-sided defect-router condition behind an additive lift.
- [`cp_p_hierarchy_attack.md`](cp_p_hierarchy_attack.md) gives exact laminar
  hierarchy accounting, finite shape exhaustion, a layer-cover-without-path
  counterexample, and failed two-point recursions.
- [`cp_g_gluing.md`](cp_g_gluing.md) defines exact gluing subclasses,
  falsifies adjacent-interface and middle-only rules, and proves the
  unformalized prefix-defect surcharge lemma.
- [`cp_m_matching_equivalence.md`](cp_m_matching_equivalence.md) gives the
  canonical-support and literal-prefix-union reductions, corrects a false
  seed-menu argument using hybrid paths, and exhausts the quadratic cyclic
  interval family through its first failure at `n=22`.
- [`lean_formalization.md`](lean_formalization.md) records the Lean-accepted
  finite core; [`formal/coverage.md`](../formal/coverage.md) gives the exact
  formal/unformalized boundary.
- [`formal_adversarial_audit.md`](formal_adversarial_audit.md) independently
  checks the Lean theorem types, assumptions, and axiom dependencies.
- [`audits/cycle03_n10_structural_adversarial.md`](../audits/cycle03_n10_structural_adversarial.md)
  independently reconstructs `N(10)=35` and audits CP-S/P/G.

The final CP-M and integration disposition is recorded in
[`audits/cycle03_final_integration_adversarial.md`](../audits/cycle03_final_integration_adversarial.md).
Failed classes and precise retry conditions are retained in
[`failure_knowledge.jsonl`](../failure_knowledge.jsonl).

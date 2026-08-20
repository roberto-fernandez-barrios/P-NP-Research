# Research Cycle 2 artifact index

The canonical integrated report is
[`results/research_cycle_02.md`](../results/research_cycle_02.md). O01 remains
OPEN. This cycle stops at a precisely restricted construction-family
diagnostic and does not begin Research Cycle 3.

## Core analyses

* [`construction_family_obstruction.md`](construction_family_obstruction.md)
  — CF-LOGGAP statement, proof, and exact scope.
* [`tr26_043_true_filtration_audit.md`](tr26_043_true_filtration_audit.md)
  — source-faithful process reconstruction and smallest counterhistories.
* [`exact_balanced_chain_values.md`](exact_balanced_chain_values.md)
  — exact `N(2),N(4),N(6),N(8)`, models, witnesses, and lower certificates.
* [`small_system_structure.md`](small_system_structure.md) — proved terminal
  invariants and finite candidate construction principles.
* [`proof_sat_repair_track.md`](proof_sat_repair_track.md) — separate A/B/C
  audit of every required repair family.
* [`literature_novelty_audit.md`](literature_novelty_audit.md) — primary-source
  baseline, prior-art searches, status qualifications, and negative findings.

## Machine-readable and executable artifacts

* [`tr26_043_true_process_state.schema.json`](tr26_043_true_process_state.schema.json)
  and [`tr26_043_v0_transition_system.json`](tr26_043_v0_transition_system.json)
  are design-level process specifications, not a trace-validation pipeline.
* [`experiments/check_proof_sat_repairs.py`](experiments/check_proof_sat_repairs.py)
  and [`certificates/proof_sat_repair_diagnostics.json`](certificates/proof_sat_repair_diagnostics.json)
  check finite repair diagnostics with exact arithmetic.
* Repository-level `experiments/` contains the true-filtration enumerator,
  exact optimizer, and independent certificate checkers.
* Repository-level `certificates/` contains all finite process and exact-`N`
  certificates, including one full chain for every balanced coloring.

## Independent audits

* [`cycle02_true_filtration_adversarial.md`](../audits/cycle02_true_filtration_adversarial.md)
  and its post-correction
  [`PASS disposition`](../audits/cycle02_true_filtration_disposition.md)
* [`cycle02_exact_n_adversarial.md`](../audits/cycle02_exact_n_adversarial.md)
  and its post-integration
  [`PASS disposition`](../audits/cycle02_exact_n_disposition.md)
* [`cycle02_repair_obstruction_adversarial.md`](../audits/cycle02_repair_obstruction_adversarial.md)
* [`cycle02_obstruction_scope_audit.md`](../audits/cycle02_obstruction_scope_audit.md)
  and its post-correction
  [`PASS disposition`](../audits/cycle02_obstruction_disposition.md)

Failed ideas and exact retry conditions are preserved in the canonical
[`failure_knowledge.jsonl`](../failure_knowledge.jsonl).

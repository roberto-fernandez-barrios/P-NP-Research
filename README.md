# P vs NP Research Engine

Long-horizon research program exploring complexity theory,
circuit lower bounds, proof complexity, meta-complexity and SAT.

Ultimate motivation: P vs NP.

Operational goal: discover rigorously verified intermediate results.

## Current research state

Research Cycle 3 completed the structural-DAG attack on O01 on 2026-08-21.
It independently hardened the Cycle-2 finite core, certified the exact finite
computational result `N(10)=35`, falsified the observed size-30 pattern,
tested four explicit shared-state construction classes, isolated the remaining
routing obligations, and formalized the reusable path core and Lemmas S1/S2 in
Lean.  O01 remains **OPEN**; no asymptotic or complexity separation is claimed.
The cycle stopped under S3-D, and Research Cycle 4 has not begun.

Start with:

* [`RESEARCH_STATE.md`](RESEARCH_STATE.md)
* [`results/research_cycle_03.md`](results/research_cycle_03.md)
* [`research_cycle_03/README.md`](research_cycle_03/README.md)
* [`audits/cycle03_final_integration_adversarial.md`](audits/cycle03_final_integration_adversarial.md)
* [`failure_knowledge.jsonl`](failure_knowledge.jsonl)
* [`results/research_cycle_02.md`](results/research_cycle_02.md)
* [`research_cycle_02/construction_family_obstruction.md`](research_cycle_02/construction_family_obstruction.md)
* [`results/research_cycle_01.md`](results/research_cycle_01.md)
* [`literature/known_results.md`](literature/known_results.md)
* [`literature/open_problems.md`](literature/open_problems.md)
* [`audits/first_target_selection.md`](audits/first_target_selection.md)

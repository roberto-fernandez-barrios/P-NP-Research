# P vs NP Research Engine

Long-horizon research program exploring complexity theory,
circuit lower bounds, proof complexity, meta-complexity and SAT.

Ultimate motivation: P vs NP.

Operational goal: discover rigorously verified intermediate results.

## Current research state

Research Cycle 4 completed the randomized-relabeling / RR-cover attack on
O01 on 2026-08-21.  It verified the FLSY symmetrization reduction, computed
exact `RR_n` acceptance data through `n=34`, and proved a restricted
stretched-exponential obstruction:

`A_n <= (n/2)2^(-c(n-2)^(1/5))`

for all sufficiently large even `n`.  The proof reduces a rooted RR witness
exactly to FLSY's ordinary one-interval family.  This stops the
inverse-polynomial single-copy acceptance route under S4-D, but does not
obstruct hybrid paths in multi-copy literal unions.  Exact finite certificates
also give two-copy covers for `n=22,24,26,28,30`; they are not extrapolated.
O01 remains **OPEN**, and Research Cycle 5 has not begun.

Start with:

* [`RESEARCH_STATE.md`](RESEARCH_STATE.md)
* [`results/research_cycle_04.md`](results/research_cycle_04.md)
* [`research_cycle_04/README.md`](research_cycle_04/README.md)
* [`audits/cycle04_final_integration_adversarial.md`](audits/cycle04_final_integration_adversarial.md)
* [`failure_knowledge.jsonl`](failure_knowledge.jsonl)
* [`results/research_cycle_03.md`](results/research_cycle_03.md)
* [`research_cycle_03/README.md`](research_cycle_03/README.md)
* [`audits/cycle03_final_integration_adversarial.md`](audits/cycle03_final_integration_adversarial.md)
* [`results/research_cycle_02.md`](results/research_cycle_02.md)
* [`research_cycle_02/construction_family_obstruction.md`](research_cycle_02/construction_family_obstruction.md)
* [`results/research_cycle_01.md`](results/research_cycle_01.md)
* [`literature/known_results.md`](literature/known_results.md)
* [`literature/open_problems.md`](literature/open_problems.md)
* [`audits/first_target_selection.md`](audits/first_target_selection.md)

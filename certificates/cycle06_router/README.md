# Cycle-6 defect-router certificates (PROVISIONAL)

Finite data for the Cycle-3 one-sided 2-defect router obligation,
produced by the bounded Cycle-6 reassessment experiments.  Single
implementation; cross-validated against previously audited balanced-side
values (`N(4)=6`, `N(6)=12`, `tau(8)`, `L(8)=19`); not independently
adversarially reviewed.  See
`results/research_cycle_06_reassessment.md` Section 2.

* `cycle06_router_values.json` — exact per-level cover minima
  `rho(n,k)` for `n = 2..10` (branch-and-bound, canonical-first
  symmetry), rigorous lower bounds `sum rho`, verified upper witness
  families, lemma-check outcomes (R-SYM, R-PARITY, R-DUAL), the
  balanced-side self-test, and the DEFECT-LIFT finite recheck
  (`|X_4|=6`, `|D_4|=7`, lift size 15, valid on six points).
  Produced by `experiments/cycle06_defect_router_exact.py`
  (deterministic, seed 20260825).
* `cycle06_router_values_deep.json` — deeper upper-bound search:
  verified routers of sizes 26 (`n=8`) and 50 (`n=10`).
  Produced by `experiments/cycle06_router_ub_deep.py`.

Headline values: `R(2)=3`, `R(4)=7`, `R(6)=15` exact;
`R(8) in [24,26]`; `R(10) in [41,50]`.  Families are lists of subset
bitmasks over the ground set `{0,...,n-1}`; every family was verified on
both the `+2` and `-2` sides by literal reachability.

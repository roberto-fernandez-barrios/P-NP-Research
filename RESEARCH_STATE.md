# Research State

## Current phase

PHASE 1 COMPLETE — Research frontier constructed

## Current objective

First research cycle complete. Preserve the audited Phase 0/1 ground truth and
begin no proof attack until the next cycle explicitly starts.

## Audited cycle findings

* Phase 0 state-of-the-art and barrier map completed with primary-source
  citations.
* Typed dependency DAG completed.
* Twenty-five unresolved intermediate targets audited and ranked.
* Alekseev--Gaevoy ECCC TR26-007 Conjecture 1.4/4.2 refuted as written by a
  parametric counterexample, computational finite checks, and an independently
  derived blinded construction. Current epistemic state:
  `ADVERSARIALLY REVIEWED; UNFORMALIZED` (not externally peer reviewed or
  novelty-audited).
* Withdrawn ECCC TR26-043 Lemmas 4.1 and 3.3 independently falsified by an
  explicit positive-probability `n=10` history. This invalidates that proof,
  not the general balanced-chain target. Current epistemic state:
  `ADVERSARIALLY REVIEWED WITHIN THIS CYCLE; UNFORMALIZED`; this is not an
  external publication claim.

## Active conjectures

None promoted to the Phase 3 conjecture state. The selected OPEN target is
recorded below but has not been attacked or relabeled as an original
conjecture.

## Falsified conjectures

* Alekseev--Gaevoy affine-union robustness, Conjecture 1.4/4.2 of ECCC
  TR26-007: FALSE AS WRITTEN for every fixed `q>1,r>0`, according to the
  internally adversarially reviewed but `UNFORMALIZED` proof recorded here.
* The conditional-drift and block-deviation martingale lemmas in withdrawn
  TR26-043 are FALSE AS STATED according to the internally adversarially
  reviewed but `UNFORMALIZED` counterhistory. The general polynomial
  balanced-chain existence statement remains OPEN.

## Current target

**O01 — Polynomial-size 1-balanced-chain set systems.**

For every positive even `n`, prove that there is an absolute constant `C`
such that `N(n)<=n^C`, where `N(n)` is the minimum size of a set system that
contains a maximal imbalance-at-most-one chain for every balanced `+/-1`
coloring of `[n]`.

Established range: `Omega(n^2)<=N(n)<=n^{O(log n/log log n)}`.

Status: OPEN (high confidence in the audited public literature). The only
claimed polynomial proof was withdrawn.

## Next action

When a new research cycle is authorized, begin with the bounded
repair-or-obstruction diagnostic in `audits/first_target_selection.md`:

1. formalize the actual two-block filtration;
2. enumerate and certify smallest counterhistories;
3. compute exact small `N(n)` where feasible; and
4. test posterior-state, nonadaptive, multi-block, and deterministic-recursion
   repairs while accounting for the total fixed set-system size.

Stop that diagnostic after either a precise restricted-construction
obstruction or a fully checked replacement conditional potential. Do not
infer a result about unrestricted `N(n)` from failure of one construction.

## Critical rule

Do not directly attempt P vs NP yet.

## Cycle 1 artifacts

* `results/research_cycle_01.md`
* `literature/known_results.md`
* `literature/barriers.md`
* `literature/dependency_graph.md`
* `literature/open_problems.md`
* `audits/first_target_selection.md`
* `audits/final_integration_disposition.md`
* `formal/coverage.md`

# Research State

## Current phase

RESEARCH CYCLE 2 COMPLETE — qualified construction-family Stop A reached

## Current objective

Preserve the completed O01 bounded repair-or-obstruction diagnostic and begin
no Research Cycle 3 work without explicit authorization.

## Main Cycle-2 disposition

O01 remains OPEN and unclaimed. No positive repair met all three obligations:
actual-filtration return control (A), residual/block-size control (B), and a
polynomial bound on all distinct generated subsets (C).

The cycle stopped at the following internally adversarially reviewed,
`UNFORMALIZED` construction-family obstruction:

> **CF-LOGGAP.** The greedy, uniformly bounded-`d`, single-consumption
> cached-frontier process cannot satisfy its posted `1-O(1/M)` guarantee that
> all directly filled balanced-return gaps are `O(log M)`.

The primitive-Dyck certificate gives
`Pr[T_bal>C log M]=Omega_D((log M)^(-3/2))`, which is larger than `K/M` for
all sufficiently large admissible `M`. This is a Stop-A result only for the
frozen process and tail contract. It is not a broader fixed-`d` obstruction,
a lower bound on unrestricted `N(n)`, an mABP/min-partition-rank lower bound,
an algebraic or Boolean separation, or a P-versus-NP result. A weaker return
theorem combined with a new compressed gap cover remains open.

Status: `ADVERSARIALLY REVIEWED; UNFORMALIZED; NOVELTY UNCLEAR`; no external
peer review.

## Exact Cycle-2 findings

### True filtration and withdrawn TR26-043

* The actual state includes every inspected-but-unconsumed frontier, tie
  coin, block position, posterior count, and recursion state.
* Lemma 4.1 first fails at `n=8` under eager height-zero comparison and at
  `n=10` under query-minimal height-zero exposure.
* The Lemma 3.3 load-martingale claim first fails literally at `n=2`; with
  both blocks active it first fails at `n=4` under eager comparison and at
  `n=6` under query-minimal comparison.
* Every two-block prefix-grid subset is reachable for every even `n<=10`.
  This is a finite exhaustive result only.
* The v0 multiscale prose is a partial, nondeterministic transition relation:
  odd residual splitting, canonical gap filling, small-size entry, and one
  next-scale guard are not fully defined or justified.

These claims have exact rational certificates and an independent audit. They
invalidate the cited proof claims, not every possible tail/residual theorem
and not O01.

### Exact finite balanced-chain numbers

Independently certified values under the FLSY set-system convention are:

`N(2)=3`, `N(4)=6`, `N(6)=12`, and `N(8)=20`.

The `n=8` lower bound exhausts every size-19 lower prefix without a color,
permutation, singleton, or complement quotient. It checks 100,800 level-four
branches, none covering more than 64 of 70 balanced colorings. All extremal
families and one complete witness chain for every signed balanced coloring
are stored in `certificates/balanced_chain_exact/`.

Status: `COMPUTATIONALLY TESTED AND ADVERSARIALLY REVIEWED; UNFORMALIZED`.
`N(2),N(4)` are routine known facts. Prior public `N(6),N(8)` computations
were not found, but novelty remains `UNCLEAR`. No value is claimed for
`n>=10`, and no asymptotic inference is made.

### Repair audit

* Posterior augmentation restores measurability but not the posted return
  tail or the false load martingale.
* Fresh-expose/defer leaves a linear residual and can create exponentially
  many tie-history subsets; its conditional bias also fails.
* Consuming complete fixed batches solves B/C but not A: internal reordering
  cannot change batch-end sums, whose drift is only `-dH/R`.
* Increasing to a uniformly bounded number of blocks retains the cached-
  frontier heavy tail. A growing full prefix grid is not polynomial with one
  fixed exponent, although sparse compression is not ruled out.
* Fixed/logarithmic-horizon constant-bias domination is incompatible with the
  primitive-Dyck tail; direct superlogarithmic gap filling lists too many
  subsets absent a new compression theorem.
* Polynomial lists of fixed orders miss some coloring when each order is
  required to have power-sublinear zero-to-zero gaps; this does not obstruct
  shared-state DAGs.
* The variable-threshold reserve lemma fixes one numerical transition error
  but does not supply A, parity, closure, or a full next-scale theorem.
* Geometric-log accounting proves C only when residual identities and local
  families are globally polynomial across all colorings and histories.

Every rejected route and retry condition is in `failure_knowledge.jsonl`.

## Cycle-1 findings retained

* Phase 0 ground truth, barriers, typed dependency DAG, and 25 ranked open
  targets remain in force.
* Alekseev--Gaevoy ECCC TR26-007 Conjecture 1.4/4.2 is refuted as written by
  an internally adversarially reviewed, `UNFORMALIZED` parametric
  counterexample. This is not an external publication claim.
* The conditional-drift and block-load martingale claims of withdrawn
  TR26-043 are false as stated; the polynomial balanced-chain target remains
  open.

## Current target

**O01 — Polynomial-size 1-balanced-chain set systems.**

For every positive even `n`, determine whether there is an absolute constant
`C` such that `N(n)<=n^C`.

Known public range:

`Omega(n^2)<=N(n)<=n^{O(log n/log log n)}`.

Status: OPEN with high confidence in the audited public literature. The only
located polynomial proof was withdrawn; no public correction was found
through the Cycle-2 search cutoff.

## Next action

Stop. Do not proceed to Research Cycle 3 automatically and do not change
targets. If a later cycle is authorized, do not retry the unchanged greedy
single-consumption cached-frontier/logarithmic-direct-fill template. Possible
future choices require a fresh user decision: test a rule that consumes or
reconciles all revealed frontiers, or reassess O01 against O03/O02/O18/O05.
Because Stop A was achieved, Cycle 2 makes no automatic abandon-O01
recommendation.

## Critical rule

Do not directly attempt P versus NP. No Boolean or algebraic complexity
separation follows from this cycle.

## Canonical Cycle-2 artifacts

* `results/research_cycle_02.md`
* `research_cycle_02/construction_family_obstruction.md`
* `research_cycle_02/tr26_043_true_filtration_audit.md`
* `research_cycle_02/exact_balanced_chain_values.md`
* `research_cycle_02/small_system_structure.md`
* `research_cycle_02/proof_sat_repair_track.md`
* `research_cycle_02/literature_novelty_audit.md`
* `audits/cycle02_repair_obstruction_adversarial.md`
* `audits/cycle02_exact_n_adversarial.md`
* `audits/cycle02_exact_n_disposition.md`
* `audits/cycle02_true_filtration_adversarial.md`
* `audits/cycle02_true_filtration_disposition.md`
* `audits/cycle02_obstruction_scope_audit.md`
* `audits/cycle02_obstruction_disposition.md`
* `failure_knowledge.jsonl`
* `formal/coverage.md`

## Canonical Cycle-1 artifacts

* `results/research_cycle_01.md`
* `literature/known_results.md`
* `literature/barriers.md`
* `literature/dependency_graph.md`
* `literature/open_problems.md`
* `audits/first_target_selection.md`
* `audits/final_integration_disposition.md`

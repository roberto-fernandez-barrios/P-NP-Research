# Greedy cached-frontier logarithmic-gap construction-family obstruction

**Cycle:** Research Cycle 2  
**Date:** 2026-08-13  
**Scope:** uniformly bounded numbers of equal ordered blocks, greedy
minimum-absolute-imbalance selection, one frontier consumed per step, all
other inspected frontiers retained, and the posted high-confidence
logarithmic-gap contract  
**Claim status:** `ADVERSARIALLY REVIEWED` internally; no external review  
**Formal status:** `UNFORMALIZED`

This result is deliberately narrower than O01. It is not a lower bound on
`N(n)`, does not exclude a different bounded-block rule, and does not exclude
a weaker return estimate combined with a new compressed gap cover.
It is not an mABP lower bound, a min-partition-rank lower bound, or an
algebraic-complexity separation.

## 1. The construction family

Fix `D>=2`. For each `M`, choose an integer `d=d(M)` with `2<=d<=D` and
`d | 2M`. Partition `2M` ordered points into `d` ordered blocks of length
`2M/d`. Give the points a uniformly random balanced `+/-1` coloring.

The process `CACHED-FRONTIER(D)` does the following while every block is
active.

1. Inspect the current frontier of every block whose frontier value is not
   already known.
2. If the current signed imbalance is `H`, consume one frontier minimizing
   `|H+s|`, where `s` is its sign.
3. Resolve a tie by any nonanticipating rule measurable on the complete
   revealed history, possibly using fresh independent coins.
4. Advance only the consumed block. Every inspected but unconsumed frontier
   remains known and remains at the frontier.

The true filtration contains all inspections, cached frontiers, past tie
outcomes, positions, and remaining posterior counts. The family includes the
withdrawn two-block transition rule and its literal fixed-`d` generalization.
“Nonanticipating” means that a tied frontier is chosen from this revealed
history plus private randomness independent of the coloring, before the next
uninspected color is exposed. The policy may depend on block labels, loads,
cached signs, time, and earlier coins; it may not reveal deeper points or
consume multiple frontiers.

The high-confidence logarithmic-return property sought by that construction
is the following. For constants `C,K`, with probability at least `1-K/M`,
every gap between consecutive visits to the balanced band `|H|<=1` before
block exhaustion has length at most `C log M`. It is enough to refute this
property for the first gap following `E_d`, whose probability is bounded below
by a positive constant uniformly over `2<=d<=D` for all sufficiently large
`M`.

## 2. Obstruction theorem

> **CF-LOGGAP (greedy single-consumption cached-frontier logarithmic-gap
> obstruction).** For every fixed
> `D>=2`, every nonanticipating tie policy, and all constants `C,K>0`, the
> process family above fails the high-confidence logarithmic-return property
> for all sufficiently large admissible `M`. More quantitatively, there is a
> constant `c_D>0` such that, for an integer
> `k=Theta(C log M)` satisfying `2k>C log M`, the probability that the first
> post-initial balanced-band gap has length exactly `2k` is at least
> `c_D k^(-3/2)`. This is asymptotically larger than `K/M`.

This is a **CONSTRUCTION-FAMILY OBSTRUCTION**. It says that no posterior
potential can prove the stated high-confidence logarithmic-return conclusion
for this unchanged process, because the conclusion itself is false.
It has no direct mABP or algebraic-complexity consequence.

## 3. Exact finite formula

Let `E_d` be only the event that all `d` initial frontiers have the same sign;
the tie policy then consumes one of them. Let `T_bal` be the number of subsequent
consumptions before the next visit to `|H|<=1`. If

`1 <= k <= M-d` and `2k+1 < 2M/d`,

then

`Pr[T_bal=2k | E_d]
 >= Cat_(k-1) (M-d)_k (M)_k / (2M-d)_(2k)`,

and

`Pr[E_d]=2(M)_d/(2M)_d`.

Here `(x)_r` is a falling factorial and `Cat_j` is the `j`th Catalan number.
The inequalities and the event probability are independent of the
nonanticipating tie policy.

## 4. Proof

By sign symmetry, suppose the initial frontiers are all positive. After one
is consumed, `H=1`, there are `d-1` cached positive frontiers, and the
uninspected population contains `M-d` positives and `M` negatives.

Until the next balanced-band visit, each step exposes exactly one new sign.
A newly exposed negative sign is the unique improving choice and is consumed.
A newly exposed positive sign makes all frontiers positive; a tie consumes
one positive frontier and still leaves `d-1` positives cached. Therefore the
newly exposed signs have their ordinary ordered sampling-without-replacement
law, even though the location of the next exposure is adaptive.

Consider sign words of length `2k` having `k` signs of each type, positive
strict partial sums, and final sum zero. These are the primitive Dyck words;
there are `Cat_(k-1)` of them. Every such word keeps
`H=1+partial_sum` outside the balanced band at every proper intermediate
time and returns it to one at time `2k`. Every word has probability

`(M-d)_k (M)_k / (2M-d)_(2k)`.

The room condition prevents any block from exhausting even if every one of
the `2k+1` consumptions occurs in a single block. Summing the disjoint word
events proves the finite lower bound. Direct sampling gives the formula for
`Pr[E_d]`.

Uniformly for `2<=d<=D` and `k=o(sqrt M)`, falling-factorial expansion gives

`(M-d)_k (M)_k/(2M-d)_(2k)=(1+o(1))4^(-k)`.

Since `Cat_(k-1)/4^k=Theta(k^(-3/2))` and `Pr[E_d]` is bounded below by a
positive constant depending only on `D`, choosing `k=Theta(log M)` proves
CF-LOGGAP. The estimates are uniform when `d=d(M)` varies within
`{2,...,D}`: the error term is `O_D((k+k^2)/M)`, the room condition holds
eventually, and `Pr[E_d]` has a positive lower bound depending only on `D`.

## 5. Exact checks

The exact rational checker in
[`check_proof_sat_repairs.py`](experiments/check_proof_sat_repairs.py)
brute-counts the primitive words and verifies, among other cases:

* `d=2`, `2M=20`, `k=4`: conditional probability `175/7293` and
  unconditional lower bound `525/46189`;
* `d=3`, `2M=120`, `k=4`: conditional probability `50445/2500238`.

The finite checks test the formula; the asymptotic conclusion comes from the
displayed derivation, not from extrapolation.

## 6. What the theorem does not say

CF-LOGGAP does not show that the process has only a negligible probability of
producing logarithmic gaps. It refutes the stronger `1-O(1/M)` guarantee used
by the withdrawn analysis. In particular, it does not exclude:

* a weaker actual-filtration tail estimate sufficient for a redesigned
  construction;
* a polynomial universal cover for longer gaps that avoids listing every
  subset;
* a rule that consumes or reconciles all inspected frontiers;
* a block process outside the single-consumption cached-frontier definition;
* polynomial unrestricted `N(n)`.

Accordingly, the precise Cycle-2 disposition is:

> **Stop A reached for the greedy, uniformly bounded-`d`, single-consumption
> cached-frontier process and its posted `1-O(1/M)` logarithmic direct-gap
> guarantee. No broader fixed-`d`, mABP, `N(n)`, or O01 obstruction is
> claimed.**

Separately, the old block-load martingale is false and no replacement
residual concentration theorem was found. The full A/B/C disposition is in
[`proof_sat_repair_track.md`](proof_sat_repair_track.md).
The independent mathematical audit is
[`cycle02_repair_obstruction_adversarial.md`](../audits/cycle02_repair_obstruction_adversarial.md),
and the separate scope audit is
[`cycle02_obstruction_scope_audit.md`](../audits/cycle02_obstruction_scope_audit.md).

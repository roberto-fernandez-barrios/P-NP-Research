# Research State

## Current phase

RESEARCH CYCLE 4 COMPLETE — RR relabeling route stopped under S4-D

## Current objective

Preserve the completed Cycle-4 disposition.  Do not begin Research Cycle 5
without explicit authorization.

## Primary target and status

**O01 — Polynomial-size 1-balanced-chain set systems.**  For every positive
even `n`, determine whether an absolute constant `C` satisfies

`N(n) <= n^C`.

O01 remains **OPEN**.  The audited public range is

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`.

No Cycle-3 result proves a polynomial construction, an unrestricted lower
bound, an mABP separation, an algebraic or Boolean complexity separation, or
P versus NP.

No Cycle-4 result changes that status.  In particular, the asymptotic result
below is an obstruction to one restricted construction route, not a lower
bound on `N(n)`.

## Cycle-4 stopping result

The proposed symmetrization implication is valid.  For a fixed family
`F`, balanced coloring `f`, and uniform permutation `pi`,

`Pr[pi(F) accepts f]`

equals the acceptance fraction of `F`.  For `t` independent copies, the
fixed-color rejection probability is `(1-A)^t`.  If
`M=binom(n,n/2)` and `0<A<1`, the exact least integer certified by the
all-color union bound is

`floor(ln(M)/(-ln(1-A)))+1`.

For the corrected `RR_n`, the literal union of `t` relabelings has at most

`2+t(n-1)^2`

distinct subsets.  Hence `A_n>=n^(-O(1))` would indeed imply O01.  This is a
direct specialization of the published FLSY worst-case-to-average-case
lemma, not a new theorem.

The premise is false.  Normalize infinity negative and fix a positive finite
rank-one root `r`.  Complementing and reversing the nested cyclic intervals
of an RR witness is an exact bijection with a 1-balanced maximal chain in the
ordinary one-interval family on the other `n-2` points.  If `p_N` is that
family's success probability, then

`A_n <= (n/2)p_(n-2)`.

FLSY Theorem 4.4 (Theorem 1.7) gives an absolute `c>0` with

`p_N <= 2^(-c N^(1/5))`

for all sufficiently large even `N`.  Therefore

`A_n <= (n/2)2^(-c(n-2)^(1/5)) = exp(-Omega(n^(1/5)))`.

Status: `RIGOROUS COROLLARY; INDEPENDENTLY RECONSTRUCTED AND FINITE-CHECKED;
ADVERSARIALLY REVIEWED`.  Formal coverage is recorded separately.  This
reaches S4-D for individual-copy acceptance and random symmetrization.  It
does not rule out hybrid chains in literal unions of multiple copies.

Exact finite necklace computation, independently recounted through `n=30`
and certificate-checked through `n=34`, gives normalized rejection counts

`21, 414, 4700, 40392, 292407, 1885203, 11191257`

for `n=22,24,...,34`.  These data have no asserted asymptotic implication.

Separately, full literal-union certificates prove

`t_RR(n)=2` for `n=22,24,26,28,30`.

The second copies fix infinity and use finite modular multipliers
`2,2,2,4,5`.  Their individual rejection sets are disjoint.  The resulting
distinct-subset counts are `821,991,1177,1379,1597`.  This is exact finite
evidence only; no all-`n` two-copy claim is made.

## Cycle-3 stopping result

The mandated anti-anchoring target was decisive:

`N(10)=35`.

This is an exact finite computational determination under the FLSY convention
that counts the empty and full sets.  It falsifies the observed identity
`N(2m)=m(m+1)` at `n=10`, where that expression gives 30.  It has no
asymptotic implication.

The exact level-cover vector is

`tau(10,k) = 1,1,5,3,5,3,5,3,5,1,1`,

with sum 33.  A symmetry-normalized exhaustive prefix search checks all
4,060 live triple choices and 1,686,060 rank-four branches and proves that
the exact-minimum lower profile `1,1,5,3,5` cannot reach all 252 signed
balanced colorings.  Complementation supplies the upper obstruction.  The
two disjoint defects exclude size 34; a stored 35-subset family passes all
252 colorings under direct induced-DAG checking.

Status: `EXHAUSTIVELY COMPUTATIONALLY VERIFIED; INDEPENDENTLY ADVERSARIALLY
REVIEWED; UNFORMALIZED`.  Prior art for the exact value was not found in the
recorded search, but novelty remains `UNCLEAR`.

The exact finite table now retained is:

| `n` | `N(n)` | `L(n)=sum_k tau(n,k)` | `sigma(n)` |
|---:|---:|---:|---:|
| 2 | 3 | 3 | 0 |
| 4 | 6 | 6 | 0 |
| 6 | 12 | 12 | 0 |
| 8 | 20 | 19 | 1 |
| 10 | 35 | 33 | 2 |

These values are finite evidence only.  `sigma` is aggregate level excess;
it is not automatically a number of removable bridge subsets over embedded
minimum covers.

## Hardened foundation

Cycle 2 was treated as a set of claims, not as authority.  Cycle 3
independently rechecked:

* the consecutive-pair characterization;
* the exact contracted subset path functionality;
* the distinction between raw even-state count and `N(n)`, with an explicit
  polynomial odd-intermediary conversion;
* Lemmas S1 and S2;
* the definitions and dependencies of `tau`, `L`, and `sigma`; and
* the non-transfer boundary around CF-LOGGAP.

A fixed maximal chain covers `2^(n/2)` signed balanced colorings.  Two stale
Cycle-1 passages saying two were corrected.  CF-LOGGAP still concerns only
the frozen greedy, bounded-block, single-consumption cached-frontier process
and its posted logarithmic-gap tail contract.  It was not generalized to any
Cycle-3 deterministic subset DAG.

## Structural-class dispositions

All counts below are counts of distinct literal subsets, not paths,
descriptions, abstract control nodes, or hardware switches.

### CP-S and recursion

* The literal two-rail diamond spine has at most `6m-4` states and has no
  valid member for `n=2m>=10`.
* The wider CP-SQ profile has exactly `m(m+1)` states for `n>=4` but also has
  no valid member for `n>=10`.
* An adversarially reviewed, unformalized terminal-fanout proof candidate says
  that a valid family with a unique singleton has at least `ceil(m/2)`
  selected triples.
* The conditional lift
  `R(X,D)=X union ({a}+D) union {U+{b},U+{a,b}}` has exact size
  `|X|+|D|+2` when `D` is a one-sided `+/-2` defect router.  No polynomial
  router construction or preserved recursion is proved.  Reusing `X` loses
  the defect property at `n=6` and balanced coverage after the next lift at
  `n=8`.

### CP-P

For the exact recursively laminar hierarchy,

`h(T)=2h(A)+2h(B)-4`.

Complete balanced trees have `(2n^2+4)/3` states but fail at `n=4`.  A
28-state `n=6` hierarchy covers every coloring at every level yet has no
full path for plus set `{0,1,2}`.  All unlabelled shapes were exhausted
through `n=12`; those are construction-class data only.  Full two-point
insertion preserves coverage but costs `4|X|`; the sparse additive splice
does not preserve its terminal routing invariant.

### CP-G

Exact-minimum layer gluing first fails at `n=8`; aggregate surcharge one and
middle-only repair first fail at `n=10`.  Layer coverage plus a compatible
edge across every adjacent interface is already insufficient at `n=4`, with
the seven-mask family `[0,1,3,5,10,11,15]`.  The unformalized prefix-defect
lemma forces surplus in a failed rank band and, by complementation, in its
dual band.

### CP-M

For live, fixed-length, syntactically read-once pair programs, the
canonical-support proof candidate gives a unique literal used support at
each vertex.  If `Q(n)` is the optimum canonical even-support count, then

`Q(n) <= N(n) <= Q(n)+min(Q(n)^2,Q(n)*binom(n,2))`.

The exact literal-prefix-union reduction identifies the required compression
but does not construct it.  In particular, a union of listed paths can have
additional hybrid paths; a factor-only `n=10` counterargument was caught and
retracted because the literal family contains the hybrid order
`3,9,4,2,5,6,7,1,8,0`.

The corrected cyclic interval family `RR_n` has exactly `(n-1)^2+2` literal
subsets.  Exhaustive induced-DAG/deque checking proves it valid for every
even `n<=20`.  It first fails at `n=22`, on exactly the 21 rotations of
`1^8 0^5 1^3 0^5`.  An adversarially reviewed, unformalized recurrence proof
candidate gives a countercolor for the same family at every even `n>=22`.
This is a restricted quadratic construction theorem and obstruction, not
O01.

Full submatching closure, stage-only support abstraction, and
compatibility-signature quotienting fail for separately recorded accounting
or read-once reasons.  Their retry conditions are in
`failure_knowledge.jsonl`.

## Formal verification

Lean 4.32.1 with pinned mathlib 4.32.1 accepts, without `sorry`, `axiom`, or
`admit`:

* balanced coloring and 1-balanced-chain definitions;
* insertion-order maximal chains and prefix lemmas;
* both directions of the consecutive-pair characterization;
* both directions of the contracted path reformulation for path
  functionality on even ground cardinality; and
* Lemmas S1 and S2.

These named declarations are `FORMALLY VERIFIED` within the encoded
representations.  A separate graph object and its state accounting, the
order-theoretic extensional maximal-chain equivalence, `tau`/`sigma`, exact
`N` values, CF-LOGGAP, all Cycle-3 structural claims, and O01 remain
unformalized.  An independent trust-level-zero elaboration and axiom audit
found no `sorryAx`.

Cycle 4 additionally formalizes the reusable relabeling/equivariance layer.
`acceptsColoring_relabel_iff` checks exact full-family acceptance
equivariance; `isOneBalancedChain_relabel_iff` checks worst-case invariance;
and `iUnion_isOneBalancedChain_of_pointwise_accepts` together with
`union_relabelings_isOneBalancedChain` checks the deterministic literal-union
step.  Phase 4A is therefore `PARTIALLY FORMALIZED`: uniform permutation
fibers, independence, the union bound, exact `t`, and subset cardinality are
not formalized.  The literal RR/deque/rooted equivalence, imported FLSY
interval theorem, exhaustive finite counts, and O01 also remain outside the
Lean development.  The exact boundary is in
`research_cycle_04/lean_formalization.md` and `formal/coverage.md`.

## Literature status through 2026-08-21

Fabris--Limaye--Srinivasan--Yehudayoff is published at CCC 2026, LIPIcs 383,
Article 22, DOI `10.4230/LIPIcs.CCC.2026.22`; ECCC TR26-001 is the full
version.  Its pair-open read-once program is the closest exact known model.
Cycle 4 uses its worst-case-to-average-case Lemma 2.3 (Lemma 1.5) and its
ordinary one-interval Theorem 4.4 (Theorem 1.7).  The exact attribution and
conference numbering are audited in
`research_cycle_04/literature_novelty_audit.md`.

The polynomial claim in arXiv:2604.00746 / ECCC TR26-043 remains withdrawn;
the revision notice says the conditional-filtration gap affects all results.
No primary source was found for exact `N(6)`, `N(8)`, `N(10)`, the falsified
quadratic formula, or the normalized finite canonical-support computations.
All such search outcomes remain `PRIOR-ART-NOT-FOUND`, never novelty claims.

## Cycle-2 findings retained

CF-LOGGAP remains `ADVERSARIALLY REVIEWED; UNFORMALIZED; NOVELTY UNCLEAR` for
its frozen construction family only.  The true-filtration failures of the
withdrawn TR26-043 proof, the finite exact values through `n=8`, the repair
audit, and all precise retry conditions remain canonical in
`results/research_cycle_02.md` and `research_cycle_02/`.

Cycle-1 barrier, dependency, target-selection, and Alekseev--Gaevoy
counterexample records remain retained.  No Cycle-1 or Cycle-2 claim is
promoted by Cycle 3.

## Next action

Stop.  Do not begin Research Cycle 5 automatically.  A later cycle requires
fresh authorization.  It must not retry the inverse-polynomial single-copy
`RR_n` acceptance premise, which is now rigorously false, nor the unchanged
greedy single-consumption cached-frontier construction.  The multi-RR hybrid
route remains open: finite two-copy successes do not supply an all-`n`
theorem, while the S4-D obstruction does not apply to chains that splice
states from different copies.

## Critical rule

Do not directly attempt P versus NP.  No Boolean or algebraic complexity
separation follows from this cycle.

## Canonical Cycle-4 artifacts

* `results/research_cycle_04.md`
* `research_cycle_04/README.md`
* `research_cycle_04/symmetrization_independent.md`
* `research_cycle_04/rooted_interval_obstruction.md`
* `research_cycle_04/rr_probability_attack.md`
* `research_cycle_04/literature_novelty_audit.md`
* `research_cycle_04/cycle04_rr_exact_count.md`
* `research_cycle_04/cycle04_multi_rr.md`
* `research_cycle_04/lean_formalization.md`
* `audits/cycle04_rr_obstruction_adversarial.md`
* `audits/barriers/cycle04_rr_interval_obstruction.md`
* `audits/cycle04_final_integration_adversarial.md`
* `certificates/cycle04_rr_acceptance/`
* `certificates/cycle04_multi_rr/`
* `formal/BalancedChain.lean`
* `formal/coverage.md`
* `failure_knowledge.jsonl`

## Canonical Cycle-3 artifacts

* `results/research_cycle_03.md`
* `research_cycle_03/README.md`
* `research_cycle_03/foundation_independent_audit.md`
* `research_cycle_03/literature_novelty_audit.md`
* `research_cycle_03/exact_n10.md`
* `research_cycle_03/cp_s_recursion_attack.md`
* `research_cycle_03/cp_p_hierarchy_attack.md`
* `research_cycle_03/cp_g_gluing.md`
* `research_cycle_03/cp_m_matching_equivalence.md`
* `research_cycle_03/lean_formalization.md`
* `research_cycle_03/formal_adversarial_audit.md`
* `certificates/balanced_chain_n10/`
* `audits/cycle03_n10_structural_adversarial.md`
* `audits/cycle03_final_integration_adversarial.md`
* `formal/BalancedChain.lean`
* `formal/coverage.md`
* `failure_knowledge.jsonl`

## Canonical earlier-cycle artifacts

* `results/research_cycle_02.md`
* `research_cycle_02/`
* `results/research_cycle_01.md`
* `literature/known_results.md`
* `literature/barriers.md`
* `literature/dependency_graph.md`
* `literature/open_problems.md`

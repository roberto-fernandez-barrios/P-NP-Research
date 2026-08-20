# Exact finite values of the 1-balanced-chain number

**Track:** Research Cycle 2, exact `N(n)` computation  
**Date:** 2026-08-13  
**Status:** `COMPUTATIONALLY VERIFIED; ADVERSARIALLY REVIEWED; UNFORMALIZED`;
novelty status recorded separately (`KNOWN` for the routine `n=2,4` cases,
`UNCLEAR` for `n=6,8`)  
**Scope:** finite `n=2,4,6,8` only; no asymptotic inference is claimed.

## 1. Result

For the definition in the Cycle-1 selection audit, the independently checked
finite optima are

| `n` | balanced colorings | exact `N(n)` | level counts of the displayed optimum |
|---:|---:|---:|---|
| 2 | 2 | **3** | `1,1,1` |
| 4 | 6 | **6** | `1,1,2,1,1` |
| 6 | 20 | **12** | `1,1,3,2,3,1,1` |
| 8 | 70 | **20** | `1,1,4,2,4,2,4,1,1` |

Here a set system counts the empty set and the full set, as in the stated
definition.  The certificates use the zero-based ground set
`{0,...,n-1}`; bit `i` of an integer mask denotes element `i`.

These values were obtained by a SciPy/HiGHS mixed-integer optimizer and then
checked without SciPy by a separate exhaustive program.  The second program
does not trust the solver objective, dual bound, selected flows, symmetry
quotient, or optimal-status flag.

No exact value is claimed for `n=10`.  Even before adding useful level
inequalities, the same complement-quotiented flow formulation has 1,024
binary vertex variables, 317,520 commodity-flow variables, and approximately
719,712 endpoint/conservation constraints.  More importantly, this cycle did
not produce an independent exhaustive lower-bound checker analogous to the
`n=8` no-size-19 certificate.  Stopping the exact track at `n=8` is therefore
an evidence boundary, not evidence about the growth of `N(n)`.

## 2. Formal finite definition

For even `n`, write a balanced coloring as a set `P subseteq [n]` of its
`n/2` positive elements.  The signed imbalance of a subset `S` is

`d_P(S) = 2|S intersect P|-|S|`.

A family `X subseteq P([n])` is 1-balanced-chain when for every such `P`
there is a chain

`emptyset=C_0 subset C_1 subset ... subset C_n=[n]`

with `|C_i|=i`, every `C_i in X`, and `|d_P(C_i)|<=1` for every `i`.
`N(n)` is the minimum cardinality of such an `X`.

Equivalently, for each `P`, take the Boolean-lattice DAG induced by the
vertices satisfying `|d_P(S)|<=1`.  The selected vertices must contain an
empty-to-full path in every one of these DAGs.  This equivalence is simply the
definition of a maximal chain, not a relaxation.

### Consecutive-pair characterization

If a chain adds elements in the order `(pi_1,...,pi_n)`, it is good for `P`
if and only if every consecutive pair

`{pi_1,pi_2}, {pi_3,pi_4}, ..., {pi_{n-1},pi_n}`

is bichromatic.  Indeed, an even prefix has even imbalance, so imbalance at
most one forces it to be zero.  The difference between consecutive even
prefixes is the signed sum of the newly added pair.  Conversely, bichromatic
pairs make every even prefix zero and every odd prefix `+/-1`.

Thus one maximal chain defines an ordered, oriented perfect matching and is
good for exactly `2^{n/2}` of the signed balanced colorings.  This observation
helps interpret the witnesses but is not used as a lower bound on the number
of subsets: different chains can share most of their prefix sets.

## 3. One extremal family for each `n`

The lists below are grouped by subset size.  The JSON files retain the same
families both as integer masks and element lists.

### `n=2`, size 3

* level 0: `emptyset`;
* level 1: `{0}`;
* level 2: `{0,1}`.

### `n=4`, size 6

* level 0: `emptyset`;
* level 1: `{0}`;
* level 2: `{0,1}`, `{0,2}`;
* level 3: `{0,1,2}`;
* level 4: `{0,1,2,3}`.

### `n=6`, size 12

* level 0: `emptyset`;
* level 1: `{0}`;
* level 2: `{0,1}`, `{0,2}`, `{0,4}`;
* level 3: `{0,1,2}`, `{0,1,4}`;
* level 4: `{0,1,2,3}`, `{0,1,2,4}`, `{0,1,3,4}`;
* level 5: `{0,1,2,3,4}`;
* level 6: `{0,1,2,3,4,5}`.

### `n=8`, size 20

* level 0: `emptyset`;
* level 1: `{0}`;
* level 2: `{0,1}`, `{0,2}`, `{0,4}`, `{0,6}`;
* level 3: `{0,1,2}`, `{0,4,6}`;
* level 4: `{0,1,2,3}`, `{0,1,2,4}`, `{0,2,4,6}`,
  `{0,4,5,6}`;
* level 5: `{0,1,2,3,4}`, `{0,2,4,5,6}`;
* level 6: `{0,1,2,3,4,5}`, `{0,1,2,3,4,6}`,
  `{0,1,2,4,5,6}`, `{0,2,3,4,5,6}`;
* level 7: `{0,1,2,3,4,5,6}`;
* level 8: `{0,1,2,3,4,5,6,7}`.

Each exact certificate contains one explicit permutation and all `n+1` prefix
masks for every balanced coloring (all `2,6,20,70` signed colorings,
respectively), not merely one witness per complement pair.

## 4. Optimizer and exact formulation

The search implementation is
[`balanced_chain_optimize.py`](../experiments/balanced_chain_optimize.py).
It uses:

* one binary variable `x_S` for every subset `S`;
* for each balanced coloring modulo global sign, continuous unit-flow
  variables on its compatible Boolean-lattice edges;
* flow conservation from `emptyset` to `[n]`;
* `flow_edge <= x_tail,x_head`; and
* objective `min sum_S x_S`.

With binary vertex variables, a feasible positive flow contains a selected
source-to-sink path because the lattice is a DAG.  Splitting continuous flow
therefore cannot manufacture feasibility without a path.

Two proved reductions strengthen the model:

1. **Global sign.** `d_{P^c}(S)=-d_P(S)`, so a coloring and its complement
   have exactly the same compatible DAG.  The optimizer keeps one of each
   pair.  The independent checker uses both.
2. **Canonical-chain relabeling.** Every feasible family contains at least
   one witness maximal chain.  Relabel its added elements in chain order.
   This maps the chain to the canonical prefix chain, preserves the number of
   sets, and merely permutes all balanced colorings.  Hence forcing the
   canonical chain is without loss.  No complement-closed or
   permutation-invariant family is assumed.

### Equivalent SAT decision model

For a proposed size bound `B`, introduce a Boolean selector `x_S` for every
subset and, for each balanced coloring `P`, a Boolean reachability witness
`r_(P,S)`. Add:

* units `r_(P,emptyset)` and `r_(P,[n])`;
* `not r_(P,S)` for every incompatible `S`;
* `r_(P,S) -> x_S`; and
* for every nonempty compatible `S`,
  `r_(P,S) -> OR_(i in S) r_(P,S minus {i})`.

Finally encode `sum_S x_S <= B` with an exact cardinality circuit or
sequential counter. If `r_(P,[n])` is true, the parent clauses trace a
selected compatible path backward through strictly decreasing levels to the
empty set. Conversely, a witness chain gives a satisfying reach assignment.
Thus binary search on `B` is an exact SAT formulation. It was recorded as an
independent formulation but was not used as a third optimality oracle in this
cycle; the exhaustive checker filled that validation role.

### Per-level set-cover model

At a fixed level `k`, let a `k`-set cover exactly those balanced colorings for
which it has imbalance at most one. Minimizing

`sum_(|S|=k) x_S`

subject to

`sum_(S compatible with P) x_S >= 1` for every balanced coloring `P`

is the set-cover model defining `tau(n,k)` below. It supplies valid layer
lower bounds but deliberately ignores connectivity between layers. The
`n=8` no-size-19 enumeration restores color-specific reachability and shows
why layerwise set cover alone is insufficient there.

The independently certified per-level lower bounds below were also added as
valid MILP inequalities.  On the recorded run, HiGHS returned equal integer
objectives and dual bounds, with `0,1,1,9` branch-and-bound nodes for
`n=2,4,6,8`.  The `n=8` model had 19,856 variables, 45,588 constraints, and
solved in about 37 seconds on the current machine.  These solver facts are
reproducibility data, not the independent proof of optimality.

## 5. Lower-bound certificates

### 5.1 Per-level covering minima

Let `tau(n,k)` be the smallest number of `k`-sets such that every balanced
coloring has imbalance at most one on at least one selected set.  A witnessing
chain uses a compatible set at every level, so

`N(n) >= sum_{k=0}^n tau(n,k)`.

The exhaustive level certificate gives:

| `n` | `tau(n,0),...,tau(n,n)` | sum |
|---:|---|---:|
| 2 | `1,1,1` | 3 |
| 4 | `1,1,2,1,1` | 6 |
| 6 | `1,1,3,2,3,1,1` | 12 |
| 8 | `1,1,4,2,3,2,4,1,1` | 19 |

The checker enumerates every smaller same-level collection and verifies an
explicit collection of the displayed size.  Some elementary explanations
for the small numbers are:

* `tau(n,k)=tau(n,n-k)`, since a balanced coloring gives
  `d_P([n]\S)=-d_P(S)`.
* At level 2, selected pairs form a graph.  A balanced coloring has no
  bichromatic selected edge exactly when its positive side is a union of
  connected components.  With fewer than `2,3,4` edges on `4,6,8` vertices,
  respectively, the component sizes have a subcollection summing to
  `n/2`; the certificate checks all cases.  The displayed star/matching
  examples attain the bounds.
* One 3-set can be monochromatic for `n=6,8`, so two are necessary; two
  suitable triples suffice.
* For `n=8,k=4`, two 4-sets never suffice.  If their intersection has size
  other than two, one of the sets itself is incompatible with both.  If the
  intersection has size two, choose a 4-set containing both common elements,
  one element private to each, and no element outside their union; it meets
  both in three points.  Three explicitly recorded 4-sets cover all
  colorings.

Consequently the level sum proves the full optimum for `n=2,4,6`.  For
`n=8`, it leaves only the possibility `N(8)=19` below the size-20 upper
family.

### 5.2 Exhaustive refutation of `N(8)=19`

The independent checker proves the remaining one-unit lower bound as follows.
A size-19 family would have to attain every level minimum, hence have counts

`1,1,4,2,3,2,4,1,1`.

The checker uses all 70 balanced colorings and no permutation or complement
symmetry.  It propagates, for every selected subset, the exact bitset of
colorings having a compatible selected path to that subset.

* All 8 singleton choices and all choices of four reachable level-2 sets are
  enumerated: 280 branches, all still cover every coloring.
* Across them, 42,840 pairs of reachable level-3 sets are checked.  Exactly
  840 survive; 42,000 already miss a coloring.
* For every survivor, all triples of reachable level-4 sets are checked:
  100,800 branches.  None covers all 70 colorings.  Exactly 25,200 cover 60,
  25,200 cover 62, and 50,400 cover 64.  Thus every branch misses at least
  six colorings before the upper half of the chain can be chosen.

Why it is complete to omit an unreachable selected vertex: if a size-19
family used one, it would have fewer reachable vertices than the already
certified cover minimum on that level, so some coloring could not reach that
level at all.

The branch totals, coverage histogram, and a SHA-256 digest of every branch
are stored in
[`n8_no_size19.json`](../certificates/balanced_chain_exact/n8_no_size19.json).
The checker recomputes rather than trusts them.  Combining this exhaustion
with the level lower bound 19 proves `N(8)>=20`, while the displayed family
proves `N(8)<=20`.

## 6. Independent verification path

[`check_balanced_chain_certificates.py`](../experiments/check_balanced_chain_certificates.py)
uses only the Python standard library and the finite definition.  It:

1. checks uniqueness/range/level counts of every displayed family;
2. verifies the explicit maximal chain for every signed balanced coloring;
3. exhausts every collection smaller than each claimed `tau(n,k)`;
4. verifies a matching level-cover example; and
5. reruns the unsymmetrized `n=8` no-size-19 enumeration and digest.

Command and observed output:

```text
python -B experiments/check_balanced_chain_certificates.py
PASS n=2: upper witnesses exhaustive; lower bound=3
PASS n=4: upper witnesses exhaustive; lower bound=6
PASS n=6: upper witnesses exhaustive; lower bound=12
PASS n=8: upper witnesses exhaustive; lower bound=20
PASS n=8 no-size-19 enumeration: 100800 level-4 branches
ALL BALANCED-CHAIN CERTIFICATES PASS
```

This is independent in formulation and code path, but it is not a Lean proof
or external review. The original computation track performed no novelty
search; the later independent search and its qualified statuses are recorded
in [`literature_novelty_audit.md`](literature_novelty_audit.md) and
[`novelty_log.md`](../literature/novelty_log.md).

## 7. Post-validation structural observations

The following observations were made only after both certificate paths
passed.

1. **Stars at the ends.** In the displayed `n=6,8` optima, the level-2
   subsets form a star centered at the unique singleton.  Complements of the
   level-`n-2` subsets form another star centered at the element omitted by
   the unique co-singleton.  For a family attaining the level minima with a
   unique singleton, the lower star is forced: any usable 2-set must contain
   that singleton, and fewer than the minimum number of usable pairs misses a
   coloring.
2. **Paired third levels.** For `n=8`, the two selected triples share the star
   center and partition its four leaves into two pairs.  The reverse pattern
   appears at level 5 after taking complements.
3. **A genuine finite connectivity surcharge.** Abstractly, three 4-sets
   cover all balanced `n=8` colorings, but no three 4-sets reachable from a
   minimum-size lower prefix do so.  The optimum pays one extra middle set,
   explaining `20` rather than the level-sum lower bound `19`.
4. **Many colorings per shared path family.** The displayed optimal families
   contain `1,2,8,16` maximal chains for `n=2,4,6,8`.  Each individual chain
   covers `2^{n/2}` signed colorings, and their overlaps collectively cover
   all colorings.
5. **Numerical fit only.** The three values for `n=4,6,8` equal
   `(n/2)(n/2+1)`.  Four finite data points do not justify an asymptotic
   formula or even a conjecture, and none is promoted here.

## 8. Artifacts and reproducibility

* Search code:
  [`balanced_chain_optimize.py`](../experiments/balanced_chain_optimize.py)
* Independent checker:
  [`check_balanced_chain_certificates.py`](../experiments/check_balanced_chain_certificates.py)
* Certificate index:
  [`README.md`](../certificates/balanced_chain_exact/README.md)
* Exact upper/lower files:
  [`exact_n2.json`](../certificates/balanced_chain_exact/exact_n2.json),
  [`exact_n4.json`](../certificates/balanced_chain_exact/exact_n4.json),
  [`exact_n6.json`](../certificates/balanced_chain_exact/exact_n6.json),
  [`exact_n8.json`](../certificates/balanced_chain_exact/exact_n8.json), and
  [`level_cover_lower_bounds.json`](../certificates/balanced_chain_exact/level_cover_lower_bounds.json).

At generation time, the search-track proposer had not read another Cycle-2
track and made no commit. Later editorial integration, literature status, and
independent validation are recorded in the repository audits.

# Structural diagnostics from exact small balanced-chain systems

**Data boundary:** `n=2,4,6,8` only  
**Status:** finite observations and candidate construction principles;
`UNFORMALIZED`; no asymptotic inference

This note extracts reusable statements from the independently certified
optima in [`exact_balanced_chain_values.md`](exact_balanced_chain_values.md).
Only the first two statements below are proved for general even `n`. The
remaining items are precisely stated research candidates, not conclusions
from four data points.

## 1. Two exact general invariants

### Lemma S1: a unique singleton forces a half-star

Let `X` be a 1-balanced-chain system on even `n`, and suppose its only
singleton is `{v}`. Then `X` contains at least `n/2` two-sets incident with
`v`.

**Proof.** Every selected two-set not containing `v` is unreachable from the
only selected singleton and cannot occur in a witness chain. Let `Gamma` be
the set of neighbors `u` for which `{v,u}` is selected. If
`|Gamma|<=n/2-1`, choose a balanced coloring whose positive side contains
`{v} union Gamma`; fill it arbitrarily to size `n/2`. Every reachable
selected pair is then monochromatic, so no witness chain exists. Thus
`|Gamma|>=n/2`. The displayed `n=4,6,8` optima meet this bound exactly.

### Lemma S2: the dual half-star

If the only selected `(n-1)`-set is `[n] minus {w}`, then `X` contains at
least `n/2` selected `(n-2)`-sets whose omitted pair contains `w`.

This follows from Lemma S1 by complementing every selected set and reversing
every chain. The finite optima again meet the bound exactly.

These lemmas explain the terminal stars without assuming the optimizer's
particular labeling. They do not imply that an optimum must have unique
terminal sets.

## 2. Exact connectivity surcharge at n=8

Define `tau(n,k)` as the minimum number of level-`k` sets that merely cover
all balanced colorings by compatibility, ignoring whether the compatible
sets join into chains. Define

`L(n)=sum_(k=0)^n tau(n,k)` and `sigma(n)=N(n)-L(n)`.

The certificates prove

| `n` | `L(n)` | `N(n)` | `sigma(n)` |
|---:|---:|---:|---:|
| 2 | 3 | 3 | 0 |
| 4 | 6 | 6 | 0 |
| 6 | 12 | 12 | 0 |
| 8 | 19 | 20 | 1 |

For `n=8`, every family attaining all layer minima loses at least six of the
70 colorings by level four. One additional middle four-set suffices. Thus the
first observed obstruction is not layerwise coverage but simultaneous
color-sensitive reachability.

This sparse gluing pattern is absent from both baseline constructions. FLSY
starts from prefixes of fixed random orders and recursively fills long walk
gaps. The withdrawn local process materializes a rectangular grid of two
block-prefix positions. The certified optima instead use a non-rectangular
subset DAG: terminal half-stars feed a few shared middle vertices, with one
extra vertex at `n=8` used for connectivity rather than for layer coverage.
This is only a finite structural contrast, not a proof that either baseline
can be replaced asymptotically.

## 3. Exact path-DAG reformulation

Contract every two consecutive steps of a maximal chain. An even-level state
`S` transitions to `S union {a,b}` through a selected odd intermediary
`S union {a}` or `S union {b}`. For a balanced coloring, this two-step edge is
usable exactly when `{a,b}` is bichromatic and at least one required odd
intermediary is selected.

Therefore O01 is equivalently a request for a polynomial-vertex layered
subset DAG, fixed before the coloring is known, in which every balanced cut
has a source-to-sink path labeled by crossing pairs. This makes explicit what
the small optima share: many ordered perfect matchings are encoded by a much
smaller collection of common prefix vertices. It also explains why counting
chains or permutation descriptions is the wrong C-accounting measure.

## 4. Candidate construction principles

### CP-S: two-anchor star spine

Fix distinct anchors `v,w`. Require exactly one selected singleton `{v}`, one
selected co-singleton `[n] minus {w}`, the minimum `n/2` lower star edges at
`v`, and the dual `n/2` upper star edges at `w`. Seek polynomially many middle
vertices that connect, for every balanced cut, at least one usable lower-star
edge to at least one usable upper-star edge.

This is a concrete construction class. Its three proof obligations are:

1. **coverage:** every balanced cut has compatible choices at both stars;
2. **colored connectivity:** compatible terminal choices connect through the
   same fixed middle DAG; and
3. **accounting:** the union of all middle vertices is polynomial.

Lemmas S1--S2 settle only the first terminal condition. The `n=8` surcharge
shows that independently optimal middle layers need not settle connectivity.

### CP-P: paired-leaf hierarchy

The certified `n=8` optimum groups the four lower-star leaves into two pairs:
its two triples are `{v}` plus those pairs. This suggests testing the precise
class in which star leaves are organized by a fixed laminar hierarchy and an
odd-level vertex is the anchor together with one hierarchy node. The dual
hierarchy is used from the upper anchor.

The falsification test is exact: for each `n`, enumerate balanced cuts and
ask whether some polynomial-size collection of hierarchy-union states gives
a full crossing-pair path. A single uncovered cut rejects the hierarchy. No
claim is made that a fixed binary hierarchy works asymptotically.

### CP-G: layer-cover gluing

Given compatible-set covers `F_k` at every level, form the color-specific
reachability relation between consecutive covers. The candidate principle is
to add a polynomial-size set `B` of bridge vertices so that every balanced
coloring obtains a source-to-sink path in `union_k F_k union B`.

This separates two quantitative questions that must both be proved:

* `sum_k |F_k|` is polynomial; and
* the gluing surcharge `|B|` is polynomial.

For `n=8`, the optimum bridge surcharge is one relative to minimum layer
covers. The finite value does not suggest a bound for larger `n`; CP-G could
be equivalent in difficulty to O01 if either bullet is left as an
assumption.

### CP-M: shared matching-state compression

A single chain is an ordered perfect matching and covers exactly `2^(n/2)`
signed balanced colorings through independent pair orientations. The finite
optima contain `1,2,8,16` maximal chains but share most prefix states. A valid
construction principle must therefore bound **distinct subset vertices**, not
the number of matching descriptions.

The precise target is a polynomial-size subset DAG whose paths realize a
crossing perfect matching for every balanced cut. Any proposal specified as a
list of exponentially many orders must additionally prove that their union
of prefix subsets is polynomial; description compression alone is not C.

## 5. Rejected extrapolation

The values for `n=4,6,8` fit `(n/2)(n/2+1)`. This cycle records that equality
only as a finite numerical coincidence. It is not promoted to a conjecture,
an upper-bound ansatz, or evidence for O01. The next exact instance is not
certified.

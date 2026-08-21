# CP-P paired-leaf / laminar hierarchy attack

**Cycle:** Research Cycle 3
**Date:** 2026-08-21
**Role:** independent CP-P construction proposer and falsifier
**Mathematical status:** elementary statements below are `PROOF CANDIDATE;
UNFORMALIZED`; finite searches are `COMPUTATIONALLY TESTED` by the same
track, not independently validated
**Novelty status:** `UNCLEAR`; no novelty claim
**Scope:** one exact recursively laminar subset-family class and two explicit
two-point recursions. No assertion about unrestricted `N(n)` follows.

## 1. Disposition

The most economical fixed binary hierarchy has an exact quadratic number of
**distinct subset states**, but it is not a 1-balanced-chain system: the
complete balanced hierarchy first fails at `n=4`.

A broader enumeration gives a sharper warning. At `n=6` there is a
28-state paired hierarchy for which every balanced coloring has a compatible
state at every level, yet the coloring with plus set `{0,1,2}` has no
source-to-sink path. Thus layer coverage does not repair the hierarchy's
block-exhaustion obstruction.

Some other tree shapes are valid in the tested range, but they pay for
flexibility by duplicating subset frontiers. Exhaustion of every unlabelled
rooted full binary tree shape through `n=12` gives the following minimum
numbers of states among valid shapes:

`4,16,48,160,448,1152` for `n=2,4,6,8,10,12`.

This is finite construction-class data only. In particular, it is not a
lower bound on `N(n)` and no growth rate is inferred.

The natural two-new-leaf recursion exposes the exact accounting problem:
it is always valid but replaces `X` by four disjoint marker copies, so its
size is `4|X|`. A sparse top-splice using only `O(n^2)` new states works for
one step under an explicit two-defect terminal-routing invariant. Even after
symmetrization, however, the splice loses that invariant at `n=6` and its
next iterate fails balanced coverage at `n=8`. Preserving the invariant at
successive scales requires routing larger defects; the literal union of all
residual frontiers has `2^(n-1)` possible even residual sets.

Accordingly CP-P, in the exact form tested here, does **not** provide a
polynomial O01 construction. The remaining noncircular target is a genuinely
compressed all-defect routing lemma; no such lemma is claimed.

## 2. Dependency and scope audit

I read `AGENTS.md`, `INITIAL_RESEARCH_MISSION.md`, `RESEARCH_STATE.md`, the
Cycle-2 exact-value and structural reports, and the Cycle-3 foundation and
literature audits before defining the class.

Only the following audited elementary fact is used. If a maximal chain adds
elements in order `pi_1,...,pi_n`, it is 1-balanced for a coloring exactly
when every pair

`{pi_1,pi_2}, {pi_3,pi_4}, ..., {pi_(n-1),pi_n}`

is bichromatic. The reason is that every even prefix imbalance must be the
even integer zero; conversely, crossing pairs give even imbalance zero and
odd imbalance `+/-1`. I also used the exact selected-subset DAG semantics:
paths may use every inclusion-by-one edge whose two endpoints are actually
selected. I did not count only described traversals.

The class below contains every singleton and every co-singleton. Lemmas S1
and S2 therefore do not force its terminal structure; their unique-terminal
hypotheses are absent. The `tau/L/sigma` values are not used. The `n=6`
example below is only a direct demonstration that layerwise coverage and
path connectivity differ; it does not compute a surcharge.

CF-LOGGAP is not a dependency and is not generalized here. This is a fixed,
deterministic subset family, not the greedy single-consumption cached-
frontier stochastic process.

The updated literature audit records no located source for the particular
CP-P formulation, but it also explains that FLSY's pair-open program and
classical routing/switching objects are nearby prior art. Search failure is
not novelty evidence. See
[`literature_novelty_audit.md`](literature_novelty_audit.md).

No exact value of `N(10)` is used in this attack. Its `n=10` computation is
an independent falsification of this hierarchy class only.

## 3. Exact hierarchy-frontier class

### 3.1 States

Let `T` be a rooted non-plane full binary tree whose leaves are bijectively
labelled by a finite ground set `L(T)`. Define the family `H(T)` recursively.

For a leaf labelled `x`,

`H(x)={emptyset,{x}}`.

If the root children are `A,B`, with disjoint leaf sets also denoted `A,B`,
set

```
H(T) = H(A)
       union H(B)
       union {A union S : S in H(B)}
       union {B union S : S in H(A)}.
```

The four terms are families of literal subsets of `L(T)`. Their union is
taken before counting. There are no arbitrary bridge states and no states
chosen after seeing the coloring.

One motivation is that these are the prefixes seen by recursively traversing
one child before the other, allowing either child order at every internal
node. Importantly, that description does **not** restrict the witness paths:
the permitted path graph is the full Boolean-lattice DAG induced by `H(T)`.
Thus a path may splice prefixes generated by different traversal
descriptions whenever the literal selected states have an inclusion edge.

Equivalently, for a coloring `P`, the color-specific graph has vertex set

`{S in H(T): |2|S intersect P|-|S||<=1}`

and every arc `S -> S union {x}` between selected vertices. The construction
succeeds on `P` only if this graph contains an empty-to-full path. In the
contracted graph, an even state can add a pair only through a selected odd
intermediary, and the pair must cross `P`.

### 3.2 Exact state accounting

Write `h(T)=|H(T)|`. The four displayed pieces overlap only at the following
four states:

- `emptyset` between `H(A)` and `H(B)`;
- `A` between `H(A)` and `A union H(B)`;
- `B` between `H(B)` and `B union H(A)`; and
- `A union B` between the two completed-child pieces.

All other cross-intersections are empty because `A,B` are nonempty and
disjoint. Therefore

`h(leaf)=2`,

`h(T)=2h(A)+2h(B)-4`.

This is an equality for distinct subsets, not a count of tree nodes,
descriptions, or paths.

For the complete balanced hierarchy on `n=2^q` leaves, the recurrence solves
to

`h(T)=(2n^2+4)/3`.

Thus this particularly attractive subfamily has quadratic global state
accounting.

At the other extreme, if one root child is a leaf `a`, induction gives the
exact product identity

`H(T)={S union Q : S in H(B), Q subseteq {a}}`,

and hence `h(T)=2h(B)`. A full caterpillar therefore has `2^n` states: it is
the entire Boolean lattice. This identity is the first indication that leaf
insertion obtains flexibility by cloning frontiers.

### 3.3 Terminal and low-layer coverage

**Claim H1 (`PROOF CANDIDATE`).** Every `H(T)` contains `emptyset`, the full
set, all singletons, and all co-singletons, and is closed under complement in
`L(T)`.

**Proof.** All statements hold for a leaf. At an internal node, complementation
exchanges `H(A)` with `B union H(A)` after complementing inside `A`, and
exchanges `H(B)` with `A union H(B)`. The singleton claim follows by taking
singletons inside each child; complementation gives the co-singletons.

It follows that levels `0,1,n-1,n` cover every balanced coloring. Every
singleton and co-singleton has imbalance `+/-1`.

If the root has a leaf child `a`, then every pair `{a,x}`, `x != a`, is
selected: `{x}` is selected in the other child and the product identity adds
`a`. Hence level two contains a spanning star and covers every balanced
coloring. Complement closure gives the same conclusion at level `n-2`.
This proves terminal/near-terminal coverage where asserted; it says nothing
about a connected full path.

### 3.4 Root block-exhaustion rule

**Claim H2 (`PROOF CANDIDATE`).** If both root children `A,B` have at least
two leaves, every maximal chain contained in `H(T)` completely exhausts one
root child before taking an element of the other.

**Proof.** A selected state meeting both children either contains all of `A`
or contains all of `B`, directly from the four-term definition. Starting
with a nonempty proper subset of one child, a chain therefore cannot add an
element of the other child until the first child is complete. The same holds
with the children exchanged.

When a child is a singleton this conclusion deliberately fails: the product
identity permits that leaf to be inserted at any point of a chain in the
other child. That extra freedom is exactly the factor-two frontier clone.

## 4. Falsification results

### 4.1 Quadratic balanced hierarchies fail at `n=4`

**Claim H3 (`PROOF CANDIDATE`).** Every complete balanced hierarchy with
`n=2^q>=4` leaves is not a 1-balanced-chain family.

**Proof.** Color one root child entirely plus and the other entirely minus.
This is balanced. Since both children have size at least two, every selected
two-set lies within one child: a cross-child state at rank two would have to
contain an entire child. Thus every selected two-set is monochromatic, so no
compatible path reaches level two.

The smallest instance is `n=4`. With root cherries `{0,1}` and `{2,3}`, the
12 distinct states have level counts `1,4,2,4,1`; plus set `{0,1}` misses
level two. This kills the exact quadratic hierarchy before any extrapolation
from the Cycle-2 optimizers.

The alternative four-leaf comb is valid, but its family has 16 states and is
the complete Boolean lattice. Therefore the check did not force all tree
shapes to resemble the balanced optimizer-inspired display.

### 4.2 Layer coverage without a colored path at `n=6`

Take the exact labelled tree

`T=((0,1),((2,3),(4,5)))`.

It has 28 distinct states, with level counts

`1,6,3,8,3,6,1`.

**Claim H4 (`PROOF CANDIDATE`).** Every balanced coloring has a compatible
state at every level of `H(T)`.

**Proof.** Levels `0,1,5,6` are covered by Claim H1. The selected pairs are
exactly `{0,1},{2,3},{4,5}`. If none crossed a balanced 3-versus-3 coloring,
the plus set would be a union of two-element components and so would have
even size, a contradiction. Complementation handles level four. At level
three there are eight distinct selected triples. For a fixed balanced
coloring, only the plus triple and its complement are monochromatic; every
other triple has one or two plus elements and is compatible. Thus at least
six selected triples are compatible.

**Claim H5 (`PROOF CANDIDATE`).** For plus set `P={0,1,2}`, `H(T)` has no
compatible source-to-sink path.

**Proof.** Claim H2 forces a path to exhaust either `A={0,1}` or
`B={2,3,4,5}` first. If it exhausts `A` first, its first consecutive pair is
the monochromatic plus pair `{0,1}`. If it exhausts `B` first, those four
positions occupy two complete pair slots but contain one plus and three
minus elements, so they cannot be partitioned into two crossing pairs. Both
orders fail.

This is a color-specific connectivity obstruction after all layer coverage
obligations have passed. It is not a statement about minimum layer covers or
about `sigma(6)`.

### 4.3 Exhaustion of alternative shapes and labels

The checker enumerates all rooted non-plane full binary shapes. Relabelling
does not need separate search: for every ground-set bijection `phi`, induction
gives

`H(phi(T))={phi(S):S in H(T)}`.

The same bijection permutes the complete set of balanced colorings and maps
selected paths to selected paths. State count and universal coverage are
therefore shape invariants.

For each canonical shape, the checker constructs all literal subset masks
from the recursive definition and searches the actual induced DAG for every
signed balanced coloring. The results are:

| `n` | unlabelled shapes | valid shapes | minimum states, any shape | state counts among valid shapes |
|---:|---:|---:|---:|---|
| 2 | 1 | 1 | 4 | `4` |
| 4 | 2 | 1 | 12 | `16` |
| 6 | 6 | 2 | 28 | `48,64` |
| 8 | 23 | 3 | 44 | `160,192,256` |
| 10 | 98 | 6 | 76 | `448,576,640,768,1024` |
| 12 | 451 | 11 | 108 | `1152,1408,1664,1792,2176,2304,2560,3072,4096` |

Every valid shape in this finite range also passed the two-defect terminal
property defined below. That is a finite observation only.

At the mandated `n=10` falsification frontier, every one of the 98 shapes has
at least 76 states and every valid one has at least 448. Hence this exact
class contains no size-30 construction. This conclusion is internal to
`H(T)` and says nothing about unrestricted size-30 families or exact `N(10)`.

The enumeration digest is

`56447a269b36f4e423c469d241a59bd9514a226d03ed1e331134e87bd3ac4a57`.

## 5. Recursion analysis

### 5.1 A valid recursion with exponential state cloning

Let `X` be any 1-balanced-chain family on an even ground set `V`, and let
`a,b` be new elements. Define the full insertion lift

`I(X)={S union Q : S in X, Q subseteq {a,b}}`.

**Claim R1 (`PROOF CANDIDATE`).** `I(X)` is 1-balanced-chain on
`V union {a,b}` and `|I(X)|=4|X|`.

**Proof.** The four marker signatures are disjoint, proving the count. Fix a
balanced coloring of the larger ground set.

If `a,b` are opposite, the restriction to `V` is balanced. Follow an
`X`-witness and append `a,b`; their pair crosses.

If `a,b` have the same sign `s`, the restriction to `V` has imbalance
`-2s`. Choose an old vertex `x` of sign `-s` and flip it to `s`; the modified
old coloring is balanced. In an `X`-witness for the modified coloring, let
`y` be the mate of `x`. Under the original coloring, both `x,y` have sign
`-s`; every other witness pair is still crossing. Replace the ordered pair
`x,y` by `a,x,b,y` (respecting whichever of `x,y` came first). The two new
pairs cross. Every new prefix is an old selected prefix carrying one of the
four marker signatures, hence belongs to `I(X)`.

Adding one new leaf above a hierarchy exactly doubles its family, and adding
two successive root leaves realizes `I`. Iterating this recursion gives

`|X_n|=4^((n-n_0)/2)|X_(n_0)|`,

so this unchanged recursion is exponential. This is an exact obstruction to
the recursion's accounting, not a lower bound on other recursions.

### 5.2 An explicit additive splice and its missing invariant

For a family `X` on even `V`, define the **two-defect terminal property**
`DTP(X)`:

> For every coloring of `V` with total imbalance `+2` or `-2`, there is a
> selected chain from `emptyset` through rank `|V|-2` whose consecutive pairs
> all cross the coloring and whose two omitted vertices both have the
> majority sign.

This is stronger than ordinary balanced coverage and is directly finite and
falsifiable.

Let `W=V union {a,b}`. Define the symmetric sparse top-splice `R(X)` to
contain `X`, embedded with neither new element, together with:

- `(V minus {x,y}) union {z}` for every pair `{x,y}` in `V` and
  `z in {a,b}`;
- `(V minus {y}) union {z}` for every `y in V` and `z in {a,b}`;
- `V union {a}` and `V union {b}`;
- `W minus {y}` for every `y in V`; and
- `W`.

The number of newly listed distinct subsets is at most

`2 binom(n,2)+3n+3`.

**Claim R2 (`PROOF CANDIDATE`).** If `X` is 1-balanced-chain and has DTP,
then `R(X)` is 1-balanced-chain and

`|R(X)| <= |X|+2 binom(n,2)+3n+3`.

**Proof.** If the new colors are opposite, use a balanced witness in `X` and
append `a,b` through `V union {a}` and `W`.

If the new colors agree, the old coloring has imbalance two in the opposite
direction. DTP supplies a selected crossing-pair prefix ending at
`B=V minus {x,y}`, with `x,y` both opposite to `a,b`. Continue

`B, B union {a}, B union {a,x}, B union {a,x,b}, W`.

These are respectively an old state, a first-bullet state, a second-bullet
state, `W minus {y}`, and `W`; the two new consecutive pairs cross. The
displayed union bound proves accounting.

This has the requested one-step form `|R(X)|<=|X|+poly(n)`. To make it a
recursion, however, DTP must be independently preserved.

### 5.3 Preservation is false for the posted sparse splice

Start with the valid three-state family

`X_2={emptyset,{0},{0,1}}`,

which has DTP. Exact search gives:

| family | states | balanced coverage | DTP |
|---|---:|---|---|
| `X_2` | 3 | pass | pass |
| `R(X_2)` on 4 points | 14 | pass | pass |
| `R^2(X_2)` on 6 points | 41 | pass | **fail** for plus set `{4,5}` |
| `R^3(X_2)` on 8 points | 92 | **fail** for balanced plus set `{0,1,2,3}` | already unavailable |

The third line is the precise missing-lemma counterexample. In the failing
near-balanced coloring, the two newest points are plus and all four older
points are minus. Routing to rank four while leaving two majority minuses
requires handling an old restriction of imbalance four. DTP on the previous
family controls only imbalance two.

More generally, define `D_r` to require a crossing-pair selected prefix for
every coloring of imbalance `+/-2r`, ending after `n-2r` points and leaving
all `2r` majority points unconsumed. Ordinary validity is `D_0` and DTP is
`D_1`. Preserving `D_1` after adding a same-colored pair invokes `D_2` on the
old family; subsequent scales expose higher defects.

A literal all-defect splice lists a base `V minus M` for each possible even
majority residual `M`. Across all even residual sizes the number of candidate
bases is

`sum_r binom(n,2r)=2^(n-1)`.

This is an exact exponential frontier-union count for that literal
implementation. It is not a proof that every all-defect routing family is
exponential: different residuals could conceivably share a smaller subset
DAG.

The precise missing lemma is therefore:

> Construct an explicit property `P` that supplies all defect-routing cases
> needed by the two-point splice, prove that `P` is preserved, and realize
> the required residual choices with only an additive `poly(n)` number of
> **distinct subset states**, rather than the literal `2^(n-1)` residual
> frontier.

No such compression lemma survived this attack. Calling the requirement
itself a construction would be circular.

## 6. Failure-ledger proposals

These lines are proposed for integration into `failure_knowledge.jsonl`.
This track did not edit the shared ledger directly.

```jsonl
{"id":"RC3-CPP-01","date":"2026-08-21","family":"CP-P complete balanced laminar frontier","candidate":"Use the recursively defined hierarchy family H(T); complete balanced trees have (2n^2+4)/3 distinct subset states.","failure":"FALSIFIED at n=4: coloring one root cherry plus and the other minus makes every selected level-two pair monochromatic. The same root-cut countercolor fails every complete balanced tree on 2^q>=4 leaves.","retry_condition":"Add cross-child partial states and reprove the total distinct-subset count; tree-node or path-description counts are insufficient.","evidence":"research_cycle_03/cp_p_hierarchy_attack.md; experiments/cycle03_check_cp_p_hierarchy.py","scope":"Complete balanced hierarchy-frontier subclass only; not unrestricted CP-P or O01."}
{"id":"RC3-CPP-02","date":"2026-08-21","family":"CP-P laminar layer-cover gluing","candidate":"Use independently compatible levels of a paired hierarchy as evidence for a full colored path.","failure":"FALSIFIED at n=6 by T=((0,1),((2,3),(4,5))): its 28 states cover every balanced coloring at every level, but plus set {0,1,2} has no path because root block exhaustion makes either the plus pair or the 1-plus/3-minus four-block impossible.","retry_condition":"Supply color-specific reachability across the root split, using only explicitly counted cross-child states.","evidence":"research_cycle_03/cp_p_hierarchy_attack.md; experiments/cycle03_check_cp_p_hierarchy.py","scope":"This exact recursively laminar family; not a claim about sigma(6) or arbitrary layer covers."}
{"id":"RC3-CPP-03","date":"2026-08-21","family":"CP-P two-leaf insertion recursion","candidate":"Preserve coverage by adjoining two freely insertable leaf markers to every old hierarchy frontier.","failure":"COVERAGE PROVED BUT ACCOUNTING FAILS: the exact lift is X times the four marker signatures, so |I(X)|=4|X| and iteration is exponential.","retry_condition":"Relocate same-color defect pairs through a sparse set of splice states without cloning every old prefix, and prove the required routing invariant is preserved.","evidence":"research_cycle_03/cp_p_hierarchy_attack.md; experiments/cycle03_check_cp_p_hierarchy.py","scope":"Full marker-product insertion recursion only; not a lower bound on other recursions."}
{"id":"RC3-CPP-04","date":"2026-08-21","family":"CP-P symmetric sparse top-splice recursion","candidate":"Assume the two-defect terminal property and add at most 2*binom(n,2)+3n+3 top splice states when adjoining two points.","failure":"The one-step coverage lemma holds, but the required property is not preserved: starting from the three-state n=2 family, the n=6 second iterate fails DTP on plus set {4,5}; the unsupported n=8 third iterate then misses balanced plus set {0,1,2,3}.","retry_condition":"Use a preserved all-defect routing invariant and compress the literal residual union, which contains 2^(n-1) candidate even residual frontiers.","evidence":"research_cycle_03/cp_p_hierarchy_attack.md; experiments/cycle03_check_cp_p_hierarchy.py","scope":"The explicitly listed symmetric sparse top-splice only; no general recursion or O01 obstruction."}
```

## 7. Reproduction and evidence boundary

Run from the repository root:

```powershell
python -B experiments/cycle03_check_cp_p_hierarchy.py
```

Expected final lines include:

```text
PASS n=6 gluing obstruction: all layers cover, plus={0,1,2} has no path
PASS complete balanced hierarchy: exact quadratic count and explicit cut failure
PASS recursion falsification: sparse splice loses DTP at n=6 and fails balanced coverage at n=8
shape-record sha256=56447a269b36f4e423c469d241a59bd9514a226d03ed1e331134e87bd3ac4a57
ALL CP-P HIERARCHY CHECKS PASS
```

The checker is deterministic and standard-library-only. It independently
recomputes the families, state counts, complement closure, terminal states,
every balanced-color path decision through `n=12`, the `n=6` layer-cover
claim, the complete-balanced formula instances, and the recursion
counterexamples. It does not trust an optimizer, a stored witness, or a
claimed exact value of `N(n)`.

These are internally generated proof candidates and finite computations.
They have not been Lean-formalized or externally reviewed. They do not prove
or disprove O01, do not imply an mABP separation, and make no claim about P
versus NP.

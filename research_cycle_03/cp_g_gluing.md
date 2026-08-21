# CP-G: layer-cover gluing audit

**Cycle:** Research Cycle 3, independent CP-G role
**Date:** 2026-08-21
**Status:** general CP-G construction `OPEN`; several exact subclasses
`FALSIFIED`; finite checks `EXHAUSTIVE COMPUTATION; UNFORMALIZED`; general
prefix-defect lemma `PROOF CANDIDATE; UNFORMALIZED`
**Boundary:** no asymptotic conclusion and no novelty claim

## 1. Disposition

The independent attack did not produce a general gluing construction.  It
did isolate four distinctions that any later CP-G proposal must respect.

1. Exact minimum compatibility covers at every rank need not glue.  The first
   exact failure is `n=8`.
2. Giving every color a compatible edge across every adjacent pair of ranks
   still need not give that color one composable source-to-sink path.  This
   local rule already fails at `n=4`.
3. At `n=10`, the obstruction to minimum layers occurs before the middle and,
   by complementation, after the middle.  Thus glue confined to rank five
   cannot work, however many rank-five states it uses.  A total surcharge of
   one state cannot work either.
4. The number
   `sigma(n)=N(n)-sum_k tau(n,k)` is an aggregate level-count excess.  It need
   not count removable vertices added to a fixed collection of minimum
   covers.  In each surplus rank of the displayed `n=8` and `n=10` optima,
   no `tau(n,k)`-member subfamily even covers all colors.

The useful surviving invariant is a **prefix defect**: an exact-minimum
prefix may fail before the central layer.  Disjoint lower and upper prefix
defects force distinct units of global level surplus.  This is a finite
obstruction mechanism, not a polynomial construction.

## 2. Exact language

Let `Omega_n` be the signed balanced colorings, represented by their positive
sets `P` of size `n/2`.  For `S subseteq [n]`, put

`K(S)={P in Omega_n: |2|S intersect P|-|S||<=1}`.

For a family `X`, write `X_k={S in X: |S|=k}`.  Define color-specific forward
reachability recursively by

* `R_0(emptyset)=Omega_n`; and
* for `S in X_k`,

  `R_k(S)=K(S) intersect union_(T in X_(k-1), T subset S) R_(k-1)(T)`.

The subset relation here is automatically a one-element extension because
the ranks differ by one.

### Lemma G1: layer coverage is necessary

If `X` is 1-balanced-chain, then for every rank `k`,

`union_(S in X_k) K(S)=Omega_n`.

**Proof.** A witness chain for `P` uses some compatible selected state at
every rank.  Hence `X_k` is a compatibility cover for every `P`.  Therefore
`|X_k|>=tau(n,k)`.  This is an elementary proof candidate and remains
unformalized here.

### Lemma G2: the reachability recursion is exact

Assume `emptyset in X`, and initialize `R_0(emptyset)=Omega_n` only in that
case (otherwise initialize it to the empty set).  For every selected `S` and
coloring `P`, `P in R_k(S)` if and only if the color-compatible sub-DAG
induced by `X` contains a selected path from `emptyset` to `S`.  If
`[n] in X` as well, consequently `X` is 1-balanced-chain if and only if

`R_n([n])=Omega_n`.

**Proof.** Induct on `k`.  The recurrence records exactly the possible last
edge of a path.  At rank `n` the only possible state is `[n]`.  This is an
elementary proof candidate and remains unformalized here.

### Lemma G3: distinct-state accounting

Ranks are disjoint, so

`|X|=sum_k |X_k|=L(n)+sum_k (|X_k|-tau(n,k))`,

where `L(n)=sum_k tau(n,k)`.  If one explicitly chooses minimum covers
`F_k` and a bridge set `B`, the union has

`|union_k F_k union B|=L(n)+|B minus union_k F_k|`,

not the number of bridge descriptions, paths, or occurrences.  This formula
does not imply that an arbitrary low-surplus family contains minimum covers
as subfamilies.

## 3. Exact CP-G construction classes

These definitions make the falsified claims reproducible rather than leaving
“gluing” informal.

### CP-G0: exact-minimum profile

`G_0(n)` consists of the 1-balanced-chain families satisfying

`|X_k|=tau(n,k)` for every `k`.

Every member would have exactly `L(n)` distinct subsets.  Layer coverage is
forced by Lemma G1, while source-to-sink connectivity is the separate
condition in Lemma G2.

The exact systems at `n=2,4,6` show that this class is nonempty there.  It is
empty at `n=8`: `L(8)=19`, while the independently certified value is
`N(8)=20`.  The normalized prefix recomputation in this audit gives a more
local certificate: no prefix with counts `1,1,4,2,3` reaches all 70 signed
colors through rank four.

**Status:** `FALSIFIED`, first positive even failure `n=8`.

### CP-Gb: bounded aggregate surcharge

For an integer `b>=0`, `G_b(n)` consists of the 1-balanced-chain families
with

`sum_k (|X_k|-tau(n,k))<=b`.

This class counts distinct subsets exactly and does not assume the surplus
states are removable from a minimum-cover skeleton.  Its members have size
at most `L(n)+b`.

At `n=8`, the displayed size-20 family belongs to `G_1(8)`.  At `n=10`,
`L(10)=33` and the exact finite value `N(10)=35` makes `G_1(10)` empty.

**Status of the constant-one claim:** `FALSIFIED`, first positive even
failure `n=10`.

### CP-GM: glue confined to the middle rank

For even `n=2m`, `G_mid(n)` consists of valid families satisfying

`|X_k|=tau(n,k)` for every `k != m`,

with no restriction on `|X_m|`.  Its exact state count is

`L(n)-tau(n,m)+|X_m|`.

The displayed `n=8` optimum is in this class: its only unit of level excess
is at rank four.  The class is empty at `n=10`, regardless of how many
rank-five states are allowed, because ranks zero through four would still be
an impossible exact-minimum prefix.

**Status of the single-middle-layer principle:** `FALSIFIED`, first positive
even failure `n=10`.

### CP-GA: adjacent-interface gluing

A family satisfies the adjacent-interface predicate if every layer covers
all colors and, for every rank `k` and every `P`, there is at least one edge

`T subset S`, with `T in X_(k-1)`, `S in X_k`, and `P in K(T) intersect K(S)`.

This is an exact local condition, but it is not sufficient for Lemma G2.
Exhausting every family with both endpoints at `n=2` finds no counterexample.
Exhausting all `2^14=16,384` endpoint-containing families at `n=4` finds 556
counterexamples, 24 of minimum size seven.  The lexicographically first is

`{0,1,3,5,10,11,15}`

in bit-mask notation.  For the coloring with positive mask `3={0,1}`, the
four interfaces are each locally covered.  In particular, the rank-one to
rank-two witness is `1 -> 5`, whereas the rank-two to rank-three witness is
`10 -> 11`.  State `10` is unreachable from the selected singleton, so the
two witnesses do not compose.  The family misses positive masks `3` and
`12` globally.

**Status of adjacent interfaces as a gluing theorem:** `FALSIFIED`, smallest
positive even counterexample `n=4`.

### CP-GB: an actual minimum-cover skeleton plus bridges

An exact skeleton-augmentation instance is a tuple `(F_0,...,F_n,B)` such
that each `F_k` is a compatibility cover of cardinality `tau(n,k)` and

`X=(union_k F_k) union B`.

Coverage and distinct accounting are settled by Lemmas G1 and G3.  It is a
construction only if the recurrence in Lemma G2 reaches every color, and it
is polynomial only after separately proving both `L(n)<=poly(n)` and
`|B minus union F_k|<=poly(n)`.

No such general theorem was found.  Moreover this class must not be silently
identified with low aggregate surcharge.  The displayed `n=8` optimum has
four rank-four states but none of its four three-state subfamilies covers all
colors.  Likewise neither six-state surplus rank in the displayed `n=10`
optimum contains a five-state compatibility cover.  Thus those particular
optima cannot be decomposed into an embedded minimum skeleton plus one
removable state at each surplus rank.

## 4. Prefix-defect surcharge lemma

Call ranks `0,...,r` **minimum-prefix infeasible** if no selected prefix with
counts `tau(n,0),...,tau(n,r)` gives every balanced coloring a compatible path
from `emptyset` through rank `r`.

### Lemma G4

If ranks `0,...,r` are minimum-prefix infeasible, every 1-balanced-chain
family `X` satisfies

`sum_(k=0)^r (|X_k|-tau(n,k)) >= 1`.

By complementation, it also satisfies

`sum_(k=n-r)^n (|X_k|-tau(n,k)) >= 1`.

If `2r<n`, the two rank intervals are disjoint, so the total surcharge is at
least two.

**Proof.** Lemma G1 makes every summand nonnegative.  If the first displayed
sum were zero, all counts in the prefix would equal their minima.  Restricting
a full witness path to rank `r` would produce the prohibited minimum prefix.
For the dual claim, complement every selected subset and reverse every path;
balanced compatibility is preserved because
`d_P([n] minus S)=-d_P(S)`.  Add the two inequalities when the intervals are
disjoint.  `QED` as an unformalized proof candidate.

At `n=8`, the exhaustive obstruction has `r=4`; the lower and upper intervals
meet at the middle rank, so one central unit can satisfy both inequalities.
At `n=10`, the obstruction has `r=4` and `2r=8<10`; the intervals are
`0,...,4` and `6,...,10`.  Therefore every valid family has at least one unit
of excess in ranks `1,...,4` and at least one in ranks `6,...,9`.  End ranks
cannot have excess.  Every size-35 optimum consequently has exactly one unit
in each of those two bands and no surplus at rank five.  This statement is a
finite consequence of the exhaustive prefix certificate, not an asymptotic
theorem.

## 5. Independent finite computation

The standard-library checker
[`check_cycle03_cp_g_gluing.py`](../experiments/check_cycle03_cp_g_gluing.py)
does not import the earlier optimizer or certificate checkers.  It recomputes
the literal color signatures and performs the following searches.

| check | exhaustive work | result |
|---|---:|---|
| adjacent-interface rule, `n=2` | all 4 endpoint-containing families | no counterexample |
| adjacent-interface rule, `n=4` | all 16,384 endpoint-containing families | minimum bad size 7 |
| `n=8` minimum prefix | 153 triple choices; 360 terminal rank-four choices | maximum 64/70 colors |
| `n=10` minimum prefix | 4,060 triple choices; 1,686,060 terminal choices | maximum 250/252 colors |
| `n=8` upper | literal reachability in 20 distinct masks | 70/70 colors |
| `n=10` upper | literal reachability in 35 distinct masks | 252/252 colors |

It also independently exhausts one-smaller compatibility covers after
normalizing one member by the transitive `S_n` action.  At the hardest
`n=10`, rank-four case it checks `binom(209,3)=1,499,784` branches.  This
re-establishes the needed `tau` profiles

* `n=8`: `1,1,4,2,3,2,4,1,1`, sum 19; and
* `n=10`: `1,1,5,3,5,3,5,3,5,1,1`, sum 33.

The compact expected-output certificate is
[`cycle03_cp_g_gluing.json`](../certificates/cycle03_cp_g_gluing.json).
Reproduction:

```text
python -B experiments/check_cycle03_cp_g_gluing.py
```

Observed result:

```text
PASS adjacent-interface gluing: exhaustive first failure at n=4
PASS exact-minimum prefix obstruction: n=8 and n=10
PASS distinct-state/reachability checks: size 20 at n=8; size 35 at n=10
ALL CYCLE-3 CP-G CHECKS PASS
```

The implementation is independent code, but the general lemmas and the
interpretation in this report still require a separate adversarial validator.

## 6. Surviving target and circularity boundary

A flexible CP-G theorem would have to construct rank families `X_k` for all
even `n` such that

1. `sum_k |X_k|<=poly(n)` as a count of distinct subsets; and
2. the exact recurrence `R_n([n])=Omega_n`.

Merely postulating polynomial layer covers and polynomial glue restates the
two missing obligations.  Requiring an embedded minimum skeleton may be
strictly stronger than necessary, as the displayed finite optima warn.  No
bound on general prefix defect, no polynomial gluing algorithm, and no
recursion preserving such a bound was obtained here.

Accordingly CP-G remains an open organizational viewpoint, not a solution of
O01.  The prefix-defect lemma is the precise reusable result from this role;
its next legitimate use is as a lower-bound diagnostic for a proposed
construction class, not as evidence for any asymptotic formula.

# CP-S two-anchor star-spine and recursion attack

**Cycle:** Research Cycle 3
**Date:** 2026-08-21
**Scope:** CP-S and `X_n -> X_{n+2}` only
**Overall status:** negative structural result plus one conditional lift lemma;
`UNFORMALIZED`; no novelty claim; O01 remains open

## 1. Result ledger

| ID | Statement | Epistemic status |
|---|---|---|
| `CPSD-COUNT` | A literal two-rail diamond spine has at most `6m-4` distinct subsets on `n=2m` points, with its exact count given by an explicit union below. | `PROVED; UNFORMALIZED` |
| `TFO` | In any valid family with a unique singleton, the number of selected triples is at least `ceil(m/2)`; dually the number of level-`n-3` states has the same lower bound. | `PROOF CANDIDATE; FINITELY TESTED; UNFORMALIZED` |
| `CPSD-COVER-FAIL` | No literal two-rail diamond spine is 1-balanced-chain for `n>=10`: its first diamonds expose at most four star leaves, fewer than S1 requires. | `PROOF CANDIDATE; COMPUTATIONALLY TESTED; UNFORMALIZED` |
| `CPSQ-COUNT/COVER` | The quadratic minimum-star/two-odd-width envelope has exactly `m(m+1)` subsets and its terminal half-stars separately cover every balanced coloring. | `PROVED; UNFORMALIZED` |
| `CPSQ-BOTTLENECK` | No member of that envelope is 1-balanced-chain for `n>=10`; two level-three states can continue at most four lower-star leaves. | `PROOF CANDIDATE; COMPUTATIONALLY TESTED; UNFORMALIZED` |
| `N10-EXACT` | `tau(10,k)=(1,1,5,3,5,3,5,3,5,1,1)`; a minimum-prefix obstruction and its dual exclude sizes 33 and 34; an all-color size-35 witness gives `N(10)=35`. | `INDEPENDENT FINITE RECOMPUTATION; UNFORMALIZED` |
| `DEFECT-LIFT` | A balanced family plus a one-sided `+/-2` defect router gives a one-step family on two more points of size `|X|+|D|+2`. | `PROOF CANDIDATE; FINITELY CHECKED; UNFORMALIZED` |
| `SELF-LIFT-FAIL` | The natural choice `D=X` loses the required defect property at `n=6`, and continued use loses balanced coverage at `n=8`. | `COMPUTATIONALLY TESTED; UNFORMALIZED` |

The independently rechecked exact value `N(10)=35` falsifies the finite identity
`N(n)=(n/2)(n/2+1)` at its first new test point.  This is a finite
falsification, not asymptotic evidence in either direction.

## 2. Foundation recheck

### 2.1 Definition and contracted path DAG

For a balanced coloring `P subseteq U`, `|U|=n=2m` and `|P|=m`, put

`d_P(S)=2|S intersect P|-|S|`.

A selected maximal chain is 1-balanced exactly when all its vertices satisfy
`|d_P(S)|<=1`.  At an even level the imbalance is even, so it must be zero.
Consequently, between consecutive even prefixes `S` and
`T=S union {a,b}`, the pair `{a,b}` must be crossing for the cut
`(P,U minus P)`.  Conversely, a crossing pair changes even imbalance zero
back to zero and either intermediate odd prefix has imbalance `+1` or `-1`.

The exact contracted object associated with a family `X` is therefore:

* vertices are the selected even sets;
* an arc `S -> S union {a,b}` is present when the endpoint sets are selected
  and at least one of `S union {a}` and `S union {b}` is selected; and
* for coloring `P`, that arc is usable exactly when `{a,b}` crosses `P`.

Expansion of each arc through one selected odd intermediary turns every
colored source-to-sink path into a selected maximal chain.  Contracting the
odd steps of a selected chain gives the reverse implication.  Thus the
reformulation in `small_system_structure.md` is exact, provided the odd
intermediary condition is retained as part of the arc definition.

The accounting equivalence is also polynomially sound.  A polynomial-size
family gives polynomially many even vertices and arcs.  Conversely, a
polynomial-size explicitly represented contracted DAG, with one selected odd
intermediary backing every arc, gives a polynomial-size union of subset
states.  Merely giving exponentially many paths by a short description would
not meet this accounting condition.

### 2.2 Lemmas S1 and S2

Let `{v}` be the only selected singleton.  Every selected witness chain must
use `{v}` and then a selected pair `{v,u}`.  Write

`Gamma={u : {v,u} is selected}`.

If `|Gamma|<=m-1`, choose the positive side of a balanced coloring to contain
`{v} union Gamma` and fill it to size `m`.  Every selected pair reachable
from `{v}` is then positive monochromatic, contradicting the mandatory zero
imbalance at level two.  Hence `|Gamma|>=m`.  This independently rechecks S1.

Complementing all selected sets and reversing every chain maps the unique
co-singleton `U minus {w}` to the unique singleton `{w}` and maps an
`(n-2)`-set to its omitted pair.  S1 then gives S2: at least `m` selected
`(n-2)`-sets have omitted pairs containing `w`.

Both arguments use only the definition.  The standard-library checker also
exhausted the claims for all families at `n=2,4` and checked the constructive
countercolor for every even `n<=12`.

### 2.3 Connectivity surcharge dependencies

Let `tau(n,k)` be the minimum number of level-`k` sets whose compatibility
sets cover all balanced colorings, and set

`L(n)=sum_k tau(n,k)`, `sigma(n)=N(n)-L(n)`.

Every witness family contains a compatible selected vertex at every level,
so `|X intersect binom(U,k)|>=tau(n,k)` independently at each level.  Summing
proves `N(n)>=L(n)` and makes `sigma(n)` a nonnegative integer.  The recorded
values through `n=10` depend on two separate finite certificates: exact
per-level covering minima, and exact `N(n)`.  In particular `sigma(8)=1`
depends on both `L(8)=19` and `N(8)=20`; neither follows from the other.
At `n=10`, the independently recomputed dependencies are `L(10)=33`,
`N(10)=35`, and `sigma(10)=2`.

The word “surcharge” is numerical.  For general `n`, it must not be read as a
theorem that one can start with an arbitrary minimum cover at every level and
repair it using exactly `sigma(n)` bridge vertices.  At `n=8` the stored
size-20 witness does realize the one-unit difference by an extra level-four
state, and the unsymmetrized lower-prefix enumeration proves that every
size-19 profile fails.  No general gluing principle follows.

### 2.4 Separation from CF-LOGGAP

CF-LOGGAP concerns a random balanced coloring, a uniformly bounded number of
ordered blocks, greedy minimum-absolute-imbalance selection, consumption of
one frontier while retaining other exposed frontiers, and a particular
`1-O(1/M)` logarithmic return-gap claim.  The construction class below is a
fixed deterministic subset DAG.  It has no blocks, random order, cached
frontiers, or return-time assertion.  This attack uses no probabilistic
conclusion from CF-LOGGAP.  Conversely, failure of CP-SD/CP-SQ below says nothing
about the cached-frontier process.  The only reused material is the common
balanced-chain definition.

## 3. Exact CP-S construction classes

### 3.1 Literal two-rail diamond spine `CP-SD(n)`

Fix `n=2m>=4`, distinct anchors `v,w`, and two nested sequences of odd sets

`A(r,0) subset A(r,1) subset ... subset A(r,m-1)`, for `r in {0,1}`,

where `|A(r,j)|=2j+1`, both rails start at `A(r,0)={v}`, both end at
`A(r,m-1)=U minus {w}`, and every successive difference has size two.  The
literal diamond-spine family is the fixed union of:

1. `emptyset` and `U`;
2. every distinct checkpoint `A(r,j)`; and
3. for every rail step `A(r,j) -> A(r,j+1)` with difference `{a,b}`, the two
   distinct-subset candidates `A(r,j) union {a}` and
   `A(r,j) union {b}`.

This is an exact construction rule, not a promise of unspecified polynomial
middle states.  Its exact size is the cardinality of that displayed union.
There are at most `2m-2` distinct odd checkpoints (the two endpoints are
shared) and at most `4(m-1)` distinct even intermediates, so

`|CP-SD| <= 2+(2m-2)+4(m-1)=6m-4`.

Collisions are counted once.  The checker reconstructs the stored `n=4,6,8`
families exactly from two explicit checkpoint rails; their union sizes are
respectively `6,12,20`.  This equality is checked on subset masks, not on
path descriptions.

### 3.2 Quadratic two-odd-width envelope `CP-SQ(n)`

To test the apparent `m(m+1)` state profile even after relaxing the literal
diamonds, fix `n=2m>=4` and define `CP-SQ(n;v,w)` by the following exact
conditions.  The lower anchor `v` and the point `w` omitted by the upper
anchor are allowed to coincide; none of the bottleneck arguments assumes
they are distinct.

1. `emptyset,U` are the unique level-zero and level-`n` states.
2. `{v}` is the unique singleton and `U minus {w}` is the unique
   co-singleton.
3. Level two consists of exactly `m` distinct star pairs `{v,u}`.
4. Level `n-2` consists of exactly `m` states whose omitted pair contains
   `w`.
5. Every internal even level `2,4,...,n-2` has exactly `m` selected states.
6. Every internal odd level `3,5,...,n-3` has exactly two selected states.

This broader class specifies both terminal incidence and every layer width;
the identities of its middle states remain variables in the falsification
search.  Every literal diamond spine matching these widths is a subclass.
There are `m-1` internal even levels and `m-2` internal odd levels, so its
number of **distinct subsets**, including both endpoints, is exactly

`2 + 2 + m(m-1) + 2(m-2) = m(m+1)`.

This is state accounting, not a count of paths or descriptions.

### 3.3 General terminal-fanout lemma

**Candidate lemma `TFO`.**  Let `X` be 1-balanced-chain on `n=2m` points and
suppose `{v}` is its unique singleton.  If `q` triples are selected, then

`q >= ceil(m/2)`.

**Proof.**  Let `Lambda` contain every `u` such that the reachable lower pair
`{v,u}` is contained in at least one selected triple.  Each triple contributes
at most two such leaves, so `|Lambda|<=2q`.  If `2q<=m-1`, choose a balanced
positive side containing `{v} union Lambda` and fill it to size `m`.  Every
maximal selected path must begin with `{v}`, then a pair `{v,u}`, then a
selected triple containing that pair.  Hence `u in Lambda`, making the
mandatory even prefix `{v,u}` positive monochromatic, a contradiction.
Therefore `2q>=m`.  Complementation and chain reversal prove the dual lower
bound at level `n-3` when the co-singleton is unique.

This is stronger than applying S1 and then discarding dead pairs: it directly
counts the next-level fanout needed by colored paths.  It does not constrain
families having several selected singletons.

### 3.4 Terminal coverage and the two class failures

Let `Gamma` be the `m` lower-star leaves.  If `v` is positive, at most `m-1`
other points are positive, so some point of `Gamma` is negative.  If `v` is
negative, the sign-reversed argument gives a positive leaf.  Thus some
selected lower-star pair is crossing for every balanced coloring.  Applying
the same argument after complementation proves compatible coverage by the
upper half-star.

Thus CP-SQ's two terminal stars separately cover all balanced colorings.
This establishes only terminal compatible choices.  It does not say that a
lower choice continues to level three, much less that it reaches a compatible
upper choice.

The literal diamond class CP-SD has at most four lower intermediates, because
each of its two first rail steps contributes two.  For `m>=5`, S1 requires at
least `m` lower star pairs.  Hence CP-SD already fails terminal coverage for
every `n>=10`, regardless of all later diamonds.  Since explicit valid
members were checked at `n=4,6,8`, `n=10` is the first size at which the
entire class is ruled out; individual parameter choices can fail earlier.

**Candidate theorem `CPSQ-BOTTLENECK`.** No `CP-SQ(n;v,w)` family is
1-balanced-chain when `n=2m>=10`.

**Proof.**  A selected level-three set can contain at most two pairs of the
form `{v,u}`.  The two selected triples can therefore continue at most four
lower-star leaves.  Let `Lambda` be those leaves whose pair is contained in
at least one selected triple.  Then `|Lambda|<=4<m`.

Choose a balanced coloring whose positive side contains `{v} union Lambda`
and fill it arbitrarily to size `m`.  Any selected maximal path must begin

`emptyset, {v}, {v,u}, T`

with `T` a selected triple, hence `u in Lambda`.  But `{v,u}` is then positive
monochromatic and has imbalance two.  Thus no colored source-to-sink path
exists.  The contradiction occurs before any upper or middle state can help.

This is the `q=2` specialization of TFO.

The stored families at `n=4,6,8` were independently checked from their mask
lists to equal literal CP-SD constructions, to satisfy all six CP-SQ
conditions (and additionally have no uncolored dead state), and to cover
every signed balanced coloring.  At `n=10`, the checker fixes the five-leaf
star by relabeling and exhausts all `binom(120,2)=7140` pairs of triples; the
maximum number of live leaves is four and it constructs the countercolor
above in every branch.  Thus `n=10` is the smallest even ground-set size
`n>=4` for which neither exact class contains a valid family.  This does not
assert that every smaller parameter choice in either class is valid.

This failure is structural: the two-rail odd width is already too narrow at
the first terminal gluing step.  Additional states at levels four through
eight cannot repair it.  A retry must increase the level-three and
level-`n-3` widths at least as `ceil(n/4)` or abandon the unique-terminal-star
architecture.

## 4. Independent exact `n=10` recomputation

The CP-SD/CP-SQ obstructions kill the two precise star-spine classes.  A separate
level-cover exhaustion kills **every** size-30 family.

For all 252 signed balanced colorings, the checker recomputes the compatible
color set of every `k`-subset.  A proposed cover of size `tau(10,k)` is
checked directly.  To refute a cover of one smaller size, point transitivity
allows any member of a nonempty cover to be relabeled to the canonical set
`{0,...,k-1}`.  The checker then enumerates every choice of the remaining
members.  A still smaller cover could be padded, so enumerating size exactly
`tau-1` is complete.  Complementation supplies levels above five.

| `k` | exact `tau(10,k)` | lower branches after canonical first set | largest signed-color coverage below `tau` |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 0/252 |
| 1 | 1 | 1 | 0/252 |
| 2 | 5 | 13,244 | 250/252 |
| 3 | 3 | 119 | 250/252 |
| 4 | 5 | 1,499,784 | 248/252 |
| 5 | 3 | 251 | 244/252 |

The resulting vector is

`(1,1,5,3,5,3,5,3,5,1,1)`

and its sum is 33.  Hence

`N(10)>=L(10)=33>30`.

This is an independent standard-library exhaustion: it imports neither the
Cycle-2 optimizer nor the Cycle-3 `n=10` search programs.  Candidate upper
cover masks are treated only as claims and are rechecked against all 252
colors.  The result is machine-checked finite evidence, not a Lean theorem or
an asymptotic statement.

For the stronger lower bound, normalize the unique singleton of a
hypothetical minimum prefix and its five necessarily live pairs to
`{0},{0,1},...,{0,5}`.  Exact color-signature propagation gives 30 reachable
triple candidates.  Of all `binom(30,3)=4060` triple choices, 90 reach every
color at level three.  Across those 90 branches, an independent loop tests
1,686,060 choices of five reachable four-sets.  None reaches all 252 colors;
the maximum is 250, attained by 15,120 branches.  Omitting a globally dead
state is complete because it would leave fewer live states than the already
rechecked `tau(10,k)` at that level.

Thus the exact-minimum lower prefix with counts `1,1,5,3,5` is impossible.
A size-34 family would have exactly one state above the level minima.  A
surplus at level 5 through 9 leaves this forbidden lower prefix; a surplus at
level 1 through 4 leaves its complement-dual forbidden upper suffix; levels
0 and 10 cannot have a surplus.  This excludes size 34 (and the all-minimum
size 33).

Finally, the checker reads only the 35 candidate masks from
`upper_size35.json` and independently performs literal reachability for all
252 signed balanced colorings, without trusting the stored witness chains.
It accepts.  Therefore the finite conclusion is

`N(10)=35`, and `sigma(10)=35-33=2`.

This recomputes the dependencies relevant to the CP-S falsification.  It is
not an asymptotic inference and does not imply that later optima resemble the
displayed size-35 family.

## 5. `X_n -> X_{n+2}` recursion attack

### 5.1 The append-only lift fails immediately

Let `a,b` be two new points.  Keeping `X` on the old ground set and adding
only top states can handle a larger balanced coloring when `a,b` are
opposite: the restriction to the old ground set is balanced, a chain in `X`
can be followed by the two new points.  If `a,b` have the same sign, however,
the old restriction has total imbalance `+2` or `-2` and is outside the
hypothesis on `X`.

This is not a technical edge case.  Starting with the canonical family on
two old points, the attempted `n=2 -> 4` append-only lift fails for the
balanced coloring in which both new points are positive and both old points
are negative: every old-complete state has imbalance `-2`.  Thus “append the
new pair” has its smallest counterexample at `n=4`.

### 5.2 Exact one-step repair: one-sided defect routing

Call `D subseteq P(U)` a **one-sided 2-defect router** when:

* for every coloring of `U` with total `+2`, `D` contains a maximal chain all
  of whose prefix imbalances lie in `[0,2]`; and
* for every coloring with total `-2`, `D` contains a maximal chain all of
  whose prefix imbalances lie in `[-2,0]`.

Global sign reversal makes the two requirements equivalent at the level of
compatible-state DAGs, but both are stated to keep the lift explicit.

**Candidate lemma `DEFECT-LIFT`.**  If `X` is 1-balanced-chain on `U`, `D` is
a one-sided 2-defect router on `U`, and `a,b` are new points, then

`R(X,D) = X union { {a} union S : S in D }`

`          union { U union {b}, U union {a,b} }`

is 1-balanced-chain on `U union {a,b}`.  Its exact distinct-state count is

`|R(X,D)|=|X|+|D|+2`.

**Proof.**  If `a,b` are opposite, their deletion leaves a balanced coloring
of `U`.  Follow an `X` witness to `U`, add `b`, then add `a`; the last three
imbalances are `0,+/-1,0`.

If both new signs equal `s`, the old total is `-2s`.  Follow a defect chain
`emptyset=S_0,...,S_n=U`, but in the larger ground set use

`emptyset, {a}, {a} union S_1, ..., {a} union U, U union {a,b}`.

For `s=+1`, the old prefix sums lie in `[-2,0]`, so adding `a` shifts them
into `[-1,1]`; for `s=-1`, `[0,2]` shifts to the same band.  Adding `b`
returns the total to zero.  All displayed subsets belong to `R(X,D)`.

The three pieces in the union are disjoint: old states omit `a,b`, shifted
router states contain `a` but omit `b`, the first top state contains `b` but
omits `a`, and the full state contains both.  This proves the accounting.

### 5.3 The precise missing lemma

For an absolute constant `c`, make the auxiliary property explicit:

`P_c(n;X,D)` means that `X` is 1-balanced-chain on `n` points, `D` is a
one-sided 2-defect router on the same points, and `|D|<=n^c`.

`DEFECT-LIFT` proves the balanced-family part of

`P_c(n;X_n,D_n) -> X_(n+2)=R(X_n,D_n)`

with the required additive accounting

`|X_(n+2)|<=|X_n|+n^c+2`.

For this to be a recursion with **preserved** property, one must also produce
a fixed `D_(n+2)` and prove that it is a 2-defect router of size at most
`(n+2)^c`.  Neither `R` nor the balanced-chain hypothesis supplies that
object.  If there were an absolute constant `c` and such fixed routers `D_n`
for every even `n`, induction from any base family would give

`|X_{n+2}|<=|X_n|+n^c+2`

therefore:

> **DR-POLY (OPEN).** There are polynomial-size one-sided 2-defect routers
> for every even ground-set size.

No proof or literature/novelty status for DR-POLY is claimed here.  If one
defines `P` to include an entire future sequence `(D_n,D_(n+2),...)`, then
preservation is tautological but DR-POLY has simply been assumed.  This is
`CIRCULARITY DETECTED`, not a construction.  `DEFECT-LIFT` is consequently a
valid one-step conditional lemma, not a completed recursion.

The obstruction to the most direct preservation attempt is defect
escalation.  To make a `+2` defect chain after adjoining `a,b`, the case where
both new points have sign `-1` leaves total `+4` on the old ground set.
Thus a 2-defect hypothesis does not reproduce itself; a recursive proof asks
for 4-defect routing, then 6-defect routing, and so on, unless a new operation
prevents this escalation.

### 5.4 Exact falsification of the natural self-router recursion

Define property `P_self(X)` to mean that `X` is both 1-balanced-chain and a
one-sided 2-defect router, and take the exact natural transformation

`R_self(X)=R(X,X)`.

The lemma proves balanced coverage of `R_self(X)` whenever `P_self(X)` holds,
but the required preservation statement

`P_self(X) implies P_self(R_self(X))`

is false.  Starting from `{emptyset,{0},{0,1}}` at `n=2`, exhaustive path
checks give:

| ground-set size | family size | balanced coverage | 2-defect routing |
|---:|---:|---|---|
| 2 | 3 | pass | pass |
| 4 | 8 | pass | pass |
| 6 | 18 | pass | **fail** |

At `n=6` the two failing defect colorings have positive sides `{4,5}` and
`{0,1,2,3}`.  Continuing the same transformation despite the lost property
produces a size-38 family at `n=8` that misses the balanced colorings with
positive sides `{0,1,2,3}` and `{4,5,6,7}`.  These are complement pairs, as
required by global sign symmetry.

This candidate also has the wrong accounting recurrence
`|R_self(X)|=2|X|+2`.  Declaring `|X|` polynomial in order to rewrite the
extra `|X|` as `poly(n)` would assume the desired bound and is therefore
`CIRCULARITY DETECTED`.  A viable recursion needs a separate polynomial
router and an independently proved way to produce the next router.

## 6. Checker and reproducibility

Run:

```text
python -B experiments/check_cycle03_cp_s_recursion.py
```

The checker uses only the standard library and performs four independent
tasks:

1. reconstructs the stored `n=4,6,8` masks from literal CP-SD rails, checks
   the CP-SQ profile, and tests all signed balanced colorings;
2. exhausts the 7,140 local `n=10` two-triple choices;
3. proves all six lower-half `tau(10,k)` values by canonical-first exhaustive
   enumeration, independently reruns the minimum-prefix obstruction, and
   checks the size-35 family by fresh reachability rather than stored paths;
   and
4. reconstructs the self-router lift and its smallest defect/balanced
   countercolorings.

Observed final line:

```text
ALL CYCLE-3 CP-S/RECURSION CHECKS PASS
```

## 7. Proposed failure-ledger entries

These lines are proposed for integration; this track does **not** append the
shared ledger directly.

```json
{"id":"RC3-CPS-00","date":"2026-08-21","family":"CP-SD literal two-rail diamond spine","candidate":"Take two nested odd checkpoint rails from one singleton anchor to one co-singleton anchor and include exactly both even intermediates of every two-element rail step; at most 6m-4 distinct subsets on n=2m points.","failure":"FALSIFIED for every n>=10: the two first diamonds expose at most four lower-star pairs, while S1 requires at least m>=5. The stored n=4,6,8 families are literal instances, so n=10 is the smallest tested failure.","retry_condition":"Use a growing number of rails or a non-diamond terminal fan, and count the union of distinct subset states after all collisions.","evidence":"research_cycle_03/cp_s_recursion_attack.md; experiments/check_cycle03_cp_s_recursion.py","scope":"Literal two-rail diamond construction only; not all laminar or multi-rail spines."}
{"id":"RC3-CPS-01","date":"2026-08-21","family":"CP-SQ quadratic minimum-star/two-odd-width envelope","candidate":"Use unique lower/upper anchors, m terminal star states, m states at every internal even level, and two states at every internal odd level; total m(m+1) distinct subsets for n=2m.","failure":"FALSIFIED for every n>=10: two selected triples continue at most four lower-star leaves, while a balanced countercolor can make the anchor and all live leaves the same sign. Independently, the exact finite value N(10)=35 rules out size 30.","retry_condition":"Use at least ceil(n/4) live level-three and level-(n-3) states, or abandon the unique-terminal-star architecture; reprove all middle connectivity and distinct-state accounting.","evidence":"research_cycle_03/cp_s_recursion_attack.md; experiments/check_cycle03_cp_s_recursion.py","scope":"Exact CP-SQ width-profile class and the finite size-30 target only; not an obstruction to broader star systems or O01."}
{"id":"RC3-REC-01","date":"2026-08-21","family":"append-only n-to-n+2 lift","candidate":"Keep X_n on the old ground set and append the two new points using O(1) top states.","failure":"FALSIFIED first at n=2 to n=4: when the two new points have the same sign, the old restriction has total imbalance +/-2, outside the balanced-chain promise; the old-complete state is incompatible.","retry_condition":"Supply fixed one-sided defect-routing states for same-sign new pairs and count their distinct shifted subsets.","evidence":"research_cycle_03/cp_s_recursion_attack.md","scope":"Append-only transformation; does not rule out recursions that interleave new points."}
{"id":"RC3-REC-02","date":"2026-08-21","family":"self-router defect lift","candidate":"Require X_n itself to route balanced and one-sided +/-2 defect colorings, and set R_self(X)=X union ({a}+X) union two top states.","failure":"FALSIFIED preservation: the recursively generated n=4 family has P_self, but its n=6 image fails defect colorings with positive sides {4,5} and {0,1,2,3}; continuing then misses the corresponding balanced pair at n=8. Accounting is |R_self(X)|=2|X|+2, not additive polynomial without assuming |X| is already polynomial.","retry_condition":"Construct a separate polynomial-size defect router D_n and prove a non-escalating preservation rule producing D_(n+2); simply reusing X_n is invalid.","evidence":"research_cycle_03/cp_s_recursion_attack.md; experiments/check_cycle03_cp_s_recursion.py","scope":"Exact self-router transformation only; DR-POLY and other interleaving recursions remain open."}
```

## 8. Disposition

The apparent quadratic star-spine pattern is decisively rejected at `n=10`:
its exact layer profile is too small even for compatibility coverage, and its
two-rail terminal gluing already fails locally.  The recursion attack yields
a clean one-step reduction to one-sided defect routing, but no preserved
polynomial auxiliary property.  The missing router lemma has not survived
the validation required for a Cycle-3 stopping theorem and is not promoted
beyond `OPEN`.

O01 remains open.  No mABP or complexity separation follows.

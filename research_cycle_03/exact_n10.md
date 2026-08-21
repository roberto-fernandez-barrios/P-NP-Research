# Exact finite determination of `N(10)`

**Cycle:** Research Cycle 3, structural DAG attack
**Scope:** the single finite instance `n=10`
**Status:** `EXHAUSTIVELY COMPUTATIONALLY VERIFIED; INDEPENDENTLY
ADVERSARIALLY REVIEWED; UNFORMALIZED`; novelty status is separate
**Asymptotic boundary:** this result does not imply a bound for any larger
`n` and does not resolve O01.

## 1. Result

Under the repository's FLSY convention, including the empty and full sets,

\[
N(10)=35.
\]

The exact per-level compatibility-cover minima are

\[
(\tau(10,0),\ldots,\tau(10,10))
=(1,1,5,3,5,3,5,3,5,1,1),
\]

whose sum is `33`.  A separate exhaustive color-specific reachability
enumeration rules out the minimum lower prefix with counts `1,1,5,3,5`.
Complementation transfers the same obstruction to a minimum upper suffix.
This rules out sizes `33` and `34`; an explicit family of size `35` supplies
the upper bound.

Consequences restricted to the finite instance are:

* the size-30 test target is impossible;
* the numerical identity `N(n)=(n/2)(n/2+1)` seen at `n=4,6,8` is false at
  `n=10`; and
* the finite connectivity surcharge is
  `sigma(10)=N(10)-sum_k tau(10,k)=2`.

No asymptotic behavior is inferred from these facts.

## 2. Exact level-cover preprocessing

For a balanced positive set `P` and subset `S`, compatibility is

`|2|S intersect P|-|S|| <= 1`.

At each level `k`, a SciPy/HiGHS set-cover search found the displayed
`tau(10,k)`.  The lower bounds do not trust HiGHS.  The standard-library
checker uses all 252 signed balanced colorings, verifies an explicit cover of
the claimed size, and exhausts every cover one smaller after the following
valid normalization:

1. choose any member of a hypothetical nonempty cover;
2. relabel it to the canonical set `{0,...,k-1}`; and
3. enumerate every choice of the remaining distinct same-level sets.

It is enough to refute size `tau-1`, because any smaller cover could be
padded with distinct same-level sets without losing coverage.  The hardest
case is `k=4`, where the checker fixes one canonical four-set and exhausts all
`binom(209,3)=1,499,784` choices of the remaining three sets.  The executable
certificate records the exact branch count and digest rather than relying on
this prose rendering.  Complementation proves the symmetric upper-level
minima because, for balanced `P`,

`d_P([10] minus S)=-d_P(S)`.

The resulting level sum gives the rigorous finite lower bound `N(10)>=33`,
already excluding size 30.

## 3. Minimum-prefix obstruction

Assume a valid selected prefix has the exact level counts

`1,1,5,3,5`

through level four.  Relabel its unique singleton to `{0}`.  Every pair used
by any witness chain must contain `0`.  If one of the five selected pairs
were unused, the other four would cover all colorings at level two,
contradicting `tau(10,2)=5`.  Thus all five pairs are incident with `0`, and
their distinct other endpoints may be relabeled `1,...,5`.

The checker propagates, for each selected state, the exact bitset of signed
colorings having a compatible selected path to that state.

* The normalized five-pair star has 30 reachable triple candidates.
* All `binom(30,3)=4,060` triple choices are tested.
* Exactly 90 choices reach all 252 colorings at level three.
* For those 90 choices, every choice of five reachable level-four states is
  tested: 1,686,060 branches in total.
* None reaches all colorings.  The maximum is 250 of 252; 15,120 branches
  attain that maximum.

The restriction to globally reachable candidate states is complete.  If one
of the three selected triples were unreachable for every coloring, the other
two would cover all colorings, contradicting `tau(10,3)=3`.  The same
argument at level four uses `tau(10,4)=5`.  A state reachable for some but not
all colors is retained with its exact color signature; only states unreachable
for every color are omitted.

Therefore no valid family can have the exact minimum counts on levels zero
through four.

## 4. Why size 34 is impossible

Every valid size-34 family has at least `tau(10,k)` states on every level.
Because the minima sum to 33, exactly one level `j` has one state above its
minimum and every other level is at its minimum.

* `j=0` and `j=10` are impossible because those levels contain only one
  subset.
* If `j>=5`, levels `0,...,4` form the forbidden exact-minimum prefix.
* If `1<=j<=4`, levels `6,...,10` form an exact-minimum suffix.  Complement
  every selected set and reverse every witness chain.  Balanced compatibility
  is preserved with sign reversed, so this suffix becomes a forbidden
  exact-minimum prefix.

These cases exhaust the possible surplus level.  Hence `N(10)>=35`.

## 5. Size-35 upper family

One certified family has masks

```text
0, 64, 65, 66, 72, 80, 88, 90, 120, 122, 194, 202, 218, 219,
378, 474, 506, 507, 576, 577, 579, 705, 706, 707, 715, 723, 731,
739, 755, 763, 987, 1011, 1018, 1019, 1023
```

and level counts

`1,1,5,3,6,3,6,3,5,1,1`.

The stored certificate contains a full maximal-chain witness for each of all
252 signed balanced colorings.  An independent standard-library checker
reconstructs the finite definition and accepts every witness.

Finite structural data for this displayed optimum, not asserted for all
optima, are:

* its unique singleton is `{6}` and its unique co-singleton omits `2`;
* its level-two and complemented level-eight families are minimum half-stars
  at those respective anchors;
* it contains 60 maximal chains, each covering 32 signed colorings;
* coloring path multiplicities range from 1 to 30, with 22 signed colorings
  having a unique path; and
* every one of the 35 subsets is essential in this displayed family: deleting
  any single subset loses between 4 and 252 signed balanced colorings (the
  endpoint deletions account for the upper extreme).

The two units above the level-cover sum occur at levels four and six in this
family.  Every size-35 optimum does, however, have one unit of excess in the
lower band of levels `1,...,4` and one unit in the disjoint upper band
`6,...,9`, with no excess at level five.  Indeed, an exact-minimum lower
prefix through level four is impossible, and complementation gives the same
obstruction for the upper suffix; the total excess is exactly two.  This does
not force the particular levels four and six, nor any other displayed
incidence or path structure.

## 6. Independent formulations and evidence boundary

Three search formulations were investigated.

1. **Level-cover preprocessing:** at most 252 selector variables per level;
   the final lower bounds are independently exhausted without SciPy.
2. **Direct SAT reachability:** one selector `x_S` per subset and backward
   witness variables `r_(P,S)` with clauses
   `r_(P,S) -> x_S` and
   `r_(P,S) -> OR_i r_(P,S minus {i})`.  CaDiCaL 1.9.5 through Python-SAT
   returned UNSAT at bound 33 both with and without anchor pruning.  No DRAT
   or LRAT proof was obtained, so this is corroborating solver evidence only
   and is not used in the exact lower bound.
3. **Selector-only vertex-cut generation:** failed colorings generate valid
   compatible-DAG boundary cuts.  It produced more than two thousand cuts
   quickly but became slower than the exhaustive prefix route.  The temporary
   multi-megabyte checkpoints were deleted; the formulation source is kept as
   a reproducible diagnostic, not as a certificate.

The exact result rests on the standard-library level-cover exhaustion,
standard-library reachability-prefix exhaustion, the elementary surplus-level
case split, and the explicit upper witnesses.

## 7. Reproduction

From the repository root, the complete exact checker is:

```text
python -B experiments/check_balanced_chain_n10_exact.py
```

Expected output:

```text
PASS exact tau(10,k): [1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1]; level sum 33
PASS no minimum prefix through level 4: 1686060 terminal branches, maximum 250/252
PASS every possible size-34 surplus level is excluded
PASS size-35 upper family for all 252 signed colorings
EXACT FINITE COMPUTATIONAL RESULT: N(10)=35
```

The checker uses only the Python standard library.  The principal artifacts
are indexed in
[`certificates/balanced_chain_n10/README.md`](../certificates/balanced_chain_n10/README.md).

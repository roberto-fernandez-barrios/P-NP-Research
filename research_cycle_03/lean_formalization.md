# Research Cycle 3: Lean formalization of the finite core

**Date:** 2026-08-21
**Toolchain:** Lean 4.32.1 and mathlib 4.32.1, pinned in `formal/`
**Status:** the declarations named below are `FORMALLY VERIFIED`; all stated
boundaries remain unformalized
**Scope:** reusable finite/combinatorial definitions, consecutive pairs,
contracted subset paths, and Lemmas S1--S2 only

## Representation choices

The ground set is an arbitrary finite type `alpha`.  A coloring is its finite
set `P` of positive elements and is balanced when

`2 * |P| = |alpha|`.

The imbalance of `S` is the sum of the signs on `S`.  Lean proves the useful
identity

`imbalance(P,S) = 2 * |S intersect P| - |S|`.

A maximal chain is represented by an equivalence

`Fin |alpha| equiv alpha`,

namely the insertion order.  Its `k`-prefix is the set of elements whose
inverse position is below `k`.  Lean checks that the zero prefix is empty,
the full prefix is the universe, one successor inserts exactly the next
fresh element, and a prefix of index `k <= |alpha|` has cardinality `k`.
This is a faithful concrete presentation of Boolean-lattice maximal chains.
The additional extensional theorem comparing it with a separately defined
order-theoretic maximal-chain predicate was not required and was not added.

`IsOneBalancedChain X` has the intended quantifier order: for every balanced
`P`, there exists an insertion order whose every prefix belongs to the fixed
family `X` and has absolute imbalance at most one.

## Kernel-accepted results

All declarations below are in `formal/BalancedChain.lean` and contain no
`sorry`, `axiom`, or `admit`.

### Consecutive pairs

- `compatible_even_imbalance_zero`
- `good_even_prefix_zero`
- `chainGood_implies_consecutivePairsCross`
- `consecutivePairsCross_even_prefix_zero`
- `consecutivePairsCross_implies_chainGood`
- `chainGood_iff_consecutivePairsCross`

The last theorem proves, without assuming the coloring is globally balanced,
that a represented maximal chain has imbalance at most one at every prefix
if and only if positions `(0,1),(2,3),...` have opposite colors.  This also
formally prevents the stale stronger claim that signs must alternate between
positions `1` and `2` of adjacent pairs.

### Exact contracted subset-path functionality

`ContractedArc X P S a b` is an oriented two-element transition.  It records
that `S`, the selected odd intermediary `insert a S`, and the even target
`insert b (insert a S)` are in `X`, that `a,b` are fresh, and that their
colors differ.  The orientation loses no functionality: using the other odd
intermediary is represented by swapping `a,b`.

Lean checks:

- `chainContained_and_pairs_implies_contractedPath`;
- `contractedPath_implies_chainContained`;
- `contractedPath_implies_consecutivePairsCross`;
- `chainContained_and_good_iff_contractedPath`; and
- `oneBalancedChain_iff_contractedPaths`.

Thus, for an even-size finite ground set, the original family property is
equivalent to the existence of a source-to-sink path of open contracted arcs
for every balanced coloring.  This is the exact path-functionality statement.
The separate numeric conversion between raw family size, even-state vertex
count, and arc/odd-intermediary count is not formalized and must not be folded
into the theorem.

### Lemmas S1 and S2

Lean checks `unique_singleton_half_star`: if `X` is 1-balanced-chain and has
unique singleton `{v}`, then at least `|alpha|/2` selected pairs contain `v`.
The proof formalizes the full countercolor construction.  If fewer neighbors
exist, mathlib's `Finset.exists_superset_card_eq` extends the anchor and all
neighbors to a half-size positive set.  The witness chain's first pair is
then forced to be monochromatic, contradicting the consecutive-pair theorem.

Lean also checks `unique_cosingleton_dual_half_star`: if the unique selected
co-singleton omits `w`, then at least `|alpha|/2` selected complements of
two-sets omit a pair containing `w`.  This is proved directly at the final
pair.  Helper theorems identify the last two prefixes with the complement of
the last one or two inserted elements.  Consequently S2 does not rely on an
unformalized complement-family transport theorem.

Both theorems cover the `n=2` boundary.  Neither claims that optimum families
must have unique terminal states.

## Explicit boundary

The formal development does not prove any exact value of `N(n)`, the
Cycle-3 `n=10` computation, a polynomial upper bound, the distinct-state
accounting conversion, or CF-LOGGAP.  It also does not perform a novelty
audit.  O01 remains OPEN, and no mABP or P-versus-NP conclusion follows.

## Reproduction

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

The project manifest fixes the dependency revisions.  Generated `.lake/`
artifacts are ignored and are not research evidence.  The checked source and
manifest are the machine-reproducible artifacts.

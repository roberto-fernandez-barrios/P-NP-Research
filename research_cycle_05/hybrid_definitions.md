# Cycle 5, Phase 5A: exact definitions for multi-copy hybrid routing

**Base commit:** `745f2bdf8b6d1e472279da913245aa048b36112c`
**Date:** 2026-08-21
**Status:** definitions and elementary reformulation lemmas; the reformulation
is proved below and cross-checked computationally against the literal
induced-DAG reference semantics on every normalized coloring for
`n ∈ {8,10,12}` and on randomized copy lists (`experiments/cycle05_hybrid_core.py`).

## 1. Setting

Fix even `n = 2m`, `q = n-1`, ground set `U = Z_q ∪ {∞}`.  The corrected
literal family `RR_n` is

* rank 0: `∅`; rank `n`: `U`;
* rank 1: every finite singleton `{x}`, `x ∈ Z_q`;
* rank `k`, `2 ≤ k ≤ n-1`: `{∞} ∪ I` for every cyclic interval `I ⊆ Z_q`
  with `|I| = k-1`.

For a permutation `π` of `U`, the copy `π(RR_n) = {π(S) : S ∈ RR_n}`.  For a
finite list `P = (π_1, …, π_t)`,

```text
F(P) = ⋃_j π_j(RR_n)
```

is a set of literal subsets of `U` (deduplicated; provenance is forgotten).

**Acceptance (full induced-subset-DAG semantics).**  A balanced coloring
`f : U → {±1}` is accepted by a family `F` iff there is a chain
`∅ = C_0 ⊂ C_1 ⊂ … ⊂ C_n = U` with `|C_k| = k`, every `C_k ∈ F`, and every
`|f(C_k)| ≤ 1`.  Only membership of the literal sets matters.

**Normalization.**  Acceptance is invariant under `f ↦ -f`; we normalize
`f(∞) = -1` and identify `f` with the word `w ∈ {0,1}^{Z_q}` of its finite
plus set, `|w| = m` ones.

## 2. Provenance invariance and label sets

A subset lying in several copies has no unique copy label.  All definitions
below therefore use only the **label set**

```text
L(S) = { j : S ∈ π_j(RR_n) } ⊆ {1,…,t},
```

which is determined by the literal set `S` alone.  For an accepted chain
`C = (C_0,…,C_n)` in `F(P)`, every `L(C_k)` is nonempty.

* `C` is **copy-pure** iff `⋂_k L(C_k) ≠ ∅`, i.e. one copy contains the whole
  chain.
* `C` is **hybrid** iff it is not copy-pure.

**Switch count.**  A labeling of `C` is a function
`ℓ : {0,…,n} → {1,…,t}` with `ℓ(k) ∈ L(C_k)`.  Define `s(C)` to be the
minimum, over all such labelings, of the number of indices `k` for which
`ℓ(k+1) ≠ ℓ(k)`.  This is the number of **copy switches** of `C`, and is
the 0/1-cost shortest path computed by
`experiments/cycle05_verify_hybrid_certificates.py::min_switches`.

Equivalently, `s(C)+1` is the minimum number of blocks in a partition of
`{0,…,n}` into consecutive runs such that every run `R` has
`⋂_{k∈R} L(C_k) ≠ ∅`.  The equivalence and optimality of the greedy
maximal-run partition follow by extending each feasible run as far right as
possible.  In particular, `C` is copy-pure iff `s(C) = 0`.

**Switch data.**  Minimal labelings and block partitions need not be unique;
the greedy partition (extend each run maximally from the left) fixes canonical
block endpoints.  For geometric bookkeeping, adjacent pure blocks may be
extended to share a boundary state `S` when `{j,j'} ⊆ L(S)`; the switch is
then said to happen **at the common state** `S`.  If no such shared endpoint
is available, the label change is **across the cross step**
`(C_k, C_{k+1})`, with `j ∈ L(C_k)` and `j' ∈ L(C_{k+1})`.  Thus the
minimum-block partition itself remains disjoint; only the endpoint-sharing
segment representation used to name a common-state switch overlaps.  Both
switch types exist and neither implies the other.

## 3. Acceptance quantities

Over uniformly random normalized colorings:

* `A_j` = acceptance fraction of the single copy `π_j(RR_n)` (all equal to
  the acceptance fraction `A_n` of `RR_n` by relabeling equivariance —
  as fractions over all balanced colorings; over a fixed coloring the
  accepting **sets of colorings** differ),
* `I(P)` = fraction of colorings accepted by at least one individual copy,
* `H(P)` = acceptance fraction of the literal union `F(P)`,
* `G(P) = H(P) - I(P) ≥ 0` = **hybrid gain**; the colorings counted by
  `G(P)` are exactly the **hybrid-only** colorings: rejected by every
  individual copy but accepted by the union.

`H(P) = 1` iff `F(P)` is a 1-balanced-chain family.  Note
`I(P) ≤ Σ_j A_j = t·A_n`; by the Cycle-4 obstruction
`A_n ≤ (n/2)·2^{-c(n-2)^{1/5}}`, so for `t = poly(n)` the individual term
`I(P)` is asymptotically negligible: any all-`n` polynomial multi-RR theorem
must obtain `H(P) = 1` almost entirely from hybrid-only colorings.

## 4. Interval-walk reformulation for ∞-fixing copies

Assume every `π_j` fixes `∞`, and let `O_j` be the cyclic order on `Z_q`
whose position `i` holds `π_j(i)`; `Int(O_j) = {π_j(I) : I std cyclic
interval}` is the interval family of the circle `O_j`.

**Lemma 5A.1.**  For normalized `f` with plus word `w`, `F(P)` accepts `f`
iff there exists a nested sequence `I_1 ⊂ I_2 ⊂ … ⊂ I_{q-1}` of subsets of
`Z_q` with `|I_j| = j`, such that

1. every `I_j` is a cyclic interval of at least one order `O_{j'}`
   (automatic for `j ∈ {1, q-1}`), and
2. the plus counts `p_j = |I_j ∩ w|` satisfy `2p_j - j = 1` for odd `j` and
   `2p_j - j ∈ {0,2}` for even `j`.

*Proof.*  Every rank-1 member of `F(P)` is a finite singleton and every
rank-2 member is `{∞, x}`; nesting forces `C_2 = {∞} ∪ C_1`, and
`|f(C_2)| ≤ 1` with even rank forces `f(C_1) = +1`.  For `2 ≤ k ≤ n-1`
every member is `{∞} ∪ I` with `I ∈ ⋃_j Int(O_j)`, `|I| = k-1`; write
`I_{k-1} = C_k \ {∞}`.  Nesting of the `C_k` is nesting of the `I_j` with
one point added per step, and `f(C_{j+1}) = f(I_j) - 1`, so the rank
constraints `|f(C_k)| ≤ 1` are exactly condition 2.  The final step
`C_n = U` adds the last finite point and is always available; balancedness
gives `|f(C_n)| = 0`.  Conversely any sequence satisfying 1–2 lifts to the
chain `∅, I_1, {∞}∪I_1, …, {∞}∪I_{q-1}, U`, whose members are literal
members of `F(P)`.  ∎

Equivalently: after the plus root, points are appended in opposite-sign
pairs (in either order), and the growing set must at every moment be an
interval of at least one of the `t` circles.

**Non-∞-fixing copies** are covered by the literal set-level definitions and
the reference DP (`brute_accepts`); their rank ≥ 2 members contain `π_j(∞)`
instead of `∞`, and no interval-walk reformulation is asserted for them.

## 5. Common states and cross pairs

For orders `O, O'` on `Z_q`:

* a **common interval** is a set `S ∈ Int(O) ∩ Int(O')`.  Sizes
  `0, 1, q-1, q` are always common (in a cyclic order, complements of
  intervals are intervals; singletons and co-singletons are intervals of
  every circle).
* a **cross pair from `O` to `O'`** is a pair `(A, A ∪ {x})` with
  `A ∈ Int(O)`, `A ∪ {x} ∈ Int(O')`.  It is **strict** if moreover
  `A ∉ Int(O')` and `A ∪ {x} ∉ Int(O)`.

Complementation `S ↦ Z_q \ S` is a bijection between cross pairs from `O`
to `O'` at sizes `(j, j+1)` and cross pairs from `O'` to `O` at sizes
`(q-j-1, q-j)`, preserving strictness.

In an accepted chain, a switch between blocks labeled `j, j'` occurs either
at a common state of `O_j, O_{j'}` or across a cross step; a cross step from
`O_j` to `O_{j'}` is precisely a cross pair.  A chain with `s` switches
decomposes into `s+1` copy-pure interval-growth segments (consecutive runs),
adjacent segments joined at common states or across cross pairs.

## 6. One-switch normal form for two copies

For `t = 2` define forward states `Fwd_1(j) ⊆ Int(O_1)` at size `j`
(reachable by a pure `O_1` prefix satisfying 5A.1(2)) and backward states
`Bwd_2(j) ⊆ Int(O_2)` (from which a pure `O_2` completion to `Z_q` exists,
satisfying 5A.1(2) at all later sizes).  Then `f` has an accepting chain with
`s(C) ≤ 1` and first block in copy 1 iff

```text
∃ j, A ∈ Fwd_1(j):  A ∈ Bwd_2(j)          (switch at a common state)
                or  ∃x: A∪{x} ∈ Bwd_2(j+1)  (switch across a cross pair).
```

All 122 verified `n=22` hybrid-only certificates have independently checked
minimum switch count exactly 1, i.e. they satisfy this normal form.  Their
stored `min_switches` and `canonical` annotations were added by manual
postprocessing not reproduced by the committed search generator.

## 7. Distinct-subset accounting

For any `P` with `t` copies, `F(P)` has at most `2 + t(n-1)^2` distinct
literal subsets (rank-wise union of `t` rows of at most `n-1` sets; ranks
`1, 2, n-1` coincide across ∞-fixing copies, giving the sharper
`2 + 3(n-1) + (t… )` only for specific lists; the general bound suffices for
O01 accounting).  Hence:

* (H1 target) constant `t` with `H(P_n) = 1` for all even `n` would give
  `N(n) = O(n^2)`;
* (H2 target) `t(n) = poly(n)` with `H(P_n) = 1` would give
  `N(n) ≤ poly(n)`, resolving O01 positively.

No such theorem is claimed.  These are targets.

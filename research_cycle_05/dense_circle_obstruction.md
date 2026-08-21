# Cycle 5, Theorem E: unconditional obstruction for dense-circle multi-RR unions

**Base commit:** `745f2bdf8b6d1e472279da913245aa048b36112c`
**Date:** 2026-08-21
**Status:** `ADVERSARIALLY REVIEWED — SOUND AFTER REPAIRS`
(`audits/cycle05_theorems_adversarial.md`: the single repair, a Step-5
chain-indexing slip, is applied below; the hull uniqueness/nestedness
lemma was verified exactly tight by exhaustive subset checks at
`q ∈ {11,13}`, `d ∈ {1,2}`; the pipeline conclusion was checked on every
rescued coloring at `n = 24, 26` — minimum `k = 2` against the claimed
bound `3d+4 = 10` — and all per-word flags re-verified independently).
Uses
only (i) the Cycle-4 verified interval-walk semantics (Lemma 5A.1),
(ii) elementary hull combinatorics, and (iii) the published FLSY
Theorem 4.4 (= Theorem 1.7; published Theorem 23 (8)) in its stated
`(ε, k)` form with `k = O(1) < N^{1/5}` — the same import class Cycle 4
used with `k = 1`, re-verified verbatim against both primary versions in
`flsy_reconstruction.md` §1.3.

## 1. Statement

Fix even `n = 2m`, `q = n-1`, and a reference cyclic order `O*` on `Z_q`
(after relabeling the whole union we take `O* = O_1 = id`).  For a cyclic
order `O` on `Z_q` and `S ∈ Int(O)`, let `hull(S)` denote a minimal
`O*`-interval containing `S` (any minimizer), and

```text
def(S) = |hull(S) ∖ S|
```

its `O*`-defect.  Call `O` **`d`-dense** (w.r.t. `O*`) if every
`S ∈ Int(O)` has `def(S) ≤ d`.

**Theorem E.**  There is a universal `c > 0` (the FLSY constant) such that
for all sufficiently large even `n`, every `t ≥ 1`, and every list
`P = (π_1, …, π_t)` of ∞-fixing relabelings whose circles `O_1, …, O_t` are
all `d`-dense w.r.t. one common reference circle `O*` with

```text
6d + 8 < (n-2)^{1/5},
```

the literal union satisfies

```text
H(P) ≤ (n/2) · 2^{-c (n-2)^{1/5}}.
```

The bound is uniform in `t`: the list may be arbitrarily long.

**Corollaries.**
1. The adjacent-pair-swap circle is `2`-dense (machine-checked for
   `q = 13, 21, 29, 37` and proved in §2), so
   `H(id, pairswap) ≤ (n/2)·2^{-c(n-2)^{1/5}}` — the family with the
   highest measured finite-`n` hybrid rescue dies asymptotically.
2. Any list of circles obtained from `O*` by permutations of displacement
   `≤ Δ` (i.e. `|ρ(x) - x| ≤ Δ` cyclically) is `O(Δ)`-dense, hence dead for
   `Δ = o(n^{1/5})`.
3. Combined with FLSY Lemma 2.3, no such list can even achieve
   `H(P) ≥ 1/poly(n)`; dense-circle unions cannot resolve O01 positively.

**Scope.**  The theorem needs one common reference circle for the whole
list.  It does not cover lists mixing circles that are far from every
common reference (e.g. a transposition circle has unbounded defect:
`(I∖{u})∪{v}` with `v` far from `I`).  Those lists are addressed,
conditionally, by the switch-depth Theorem C, and the affine case exactly
by Theorem A.  No claim is made about arbitrary 1-balanced-chain families
or about `N(n)`.

## 2. The defect of the pair-swap circle

Let `q` be odd and `O₂` the circle `(1, 0, 3, 2, …, q-3, q-2, q-1)` (pairs
`(2k, 2k+1)` swapped, `q-1` fixed).  A position-interval `[i, j]` of `O₂`
holds the points `π([i,j])` where `π` is the pair-swap involution.  All
interior aligned pairs contribute both their points; at the left position
end `i`: if `i` is odd (position `i` holds `i-1`), the set contains `i-1`
and omits `i` — one substitution `i → i-1`; symmetrically at the right end
even positions substitute `j → j+1`; positions at the fixed point `q-1`
substitute nothing.  Hence every `S ∈ Int(O₂)` is a standard interval with
at most one substitution at each end, so `hull(S)` exceeds `S` by at most
the two holes left behind: `def(S) ≤ 2`.  (Exhaustive verification for
`q ≤ 37` found the bound `2` attained and never exceeded.)

## 3. Proof of Theorem E

Let `f` be a normalized balanced coloring (plus word `w`, `f(∞) = -1`)
accepted by `F(P)`, and let `I_1 ⊂ … ⊂ I_{q-1}` be the finite parts of an
accepting chain (Lemma 5A.1): `|I_j| = j`, each `I_j ∈ Int(O_{c(j)})` for
some copy index `c(j)`, and the running sums satisfy `f(I_j) = 1` (odd
`j`), `f(I_j) ∈ {0, 2}` (even `j`).  Recall the root is plus:
`f(I_1) = +1`.

**Step 1 (hull uniqueness and nestedness).**  For a nonempty `S ⊆ Z_q`, a
minimal `O*`-interval containing `S` is the complement of a largest gap
(maximal complement run) of `S`.  Two facts:

* *(Uniqueness.)*  If `|S| = j` and `def(S) ≤ d` with `j ≤ q - 2d - 1`,
  the largest gap is unique: some gap has size `≥ q - j - d` (the
  complement of any witnessing hull), and two disjoint gaps of that size
  would give `2(q - j - d) + j ≤ q`, i.e. `j ≥ q - 2d`.  Write `hull(S)`
  for the unique minimal hull; `|hull(S)| ≤ j + d`.
* *(Nestedness.)*  If additionally `S ⊆ T`, `|T| = j + 1 ≤ q - 2d - 1`,
  `def(T) ≤ d`, then `hull(S) ⊆ hull(T)`: `hull(T)^c` is an interval of
  size `≥ q - j - 1 - d` inside `S`'s complement, hence inside a single
  gap of `S`; a gap other than the largest would give
  `(q - j - d) + (q - j - 1 - d) + j ≤ q`, i.e. `j ≥ q - 2d - 1`,
  excluded.  So `hull(T)^c` lies inside the largest gap of `S`, i.e.
  `hull(S) = (largest gap)^c ⊆ hull(T)`.

Set `j* = q - 2d - 2` and `H_j = hull(I_j)` for `1 ≤ j ≤ j*`
(`H_1 = I_1` is the plus root).  By the two facts, the `H_j` are
`O*`-intervals, nested, `j ≤ |H_j| ≤ j + d`, every `H_j ∋` the root, and
`|f(H_j)| ≤ |f(I_j)| + d ≤ 2 + d`.

**Step 2 (stepwise refinement).**  `0 ≤ |H_{j+1}| - |H_j| ≤ d + 1`.
Insert, between `H_j` and `H_{j+1}`, the `O*`-intervals obtained by adding
the points of `H_{j+1} ∖ H_j` one at a time end-first (each intermediate
set is an interval, since it lies between two nested intervals and is
formed by extending `H_j` along `H_{j+1}`).  Each intermediate `G`
satisfies `|f(G)| ≤ |f(H_j)| + (d + 1) ≤ 3 + 2d`.  The concatenation is a
chain of `O*`-intervals from the root singleton up to `H_{j*}`, growing
one point per step, with all sums `≤ 3 + 2d`.

**Step 3 (bottom and top completion).**  Bottom: prepend `∅ ⊂ H_1`.
Top: `|H_{j*}| ≥ j* = q - 2d - 2`, so at most `2d + 2` points of `Z_q`
are missing from `H_{j*}`.  Append them one at a time, at each step
extending the current interval by an adjacent missing point (always
possible: the complement of a cyclic interval is an interval).  Sums along
this completion change by at most one per step, so they are bounded by
`(2 + d) + (2d + 2) = 3d + 4`.  The result is a maximal chain
`∅ = G_0 ⊂ G_1 ⊂ … ⊂ G_q = Z_q` of cyclic `O*`-intervals, every
`G_i ⊇ {root}` for `i ≥ 1`, with

```text
max_i |f(G_i)| ≤ 3d + 4 =: k₀.
```

**Step 4 (parameter check).**  `k₀ = 3d + 4` and the final `k` below is
`k₀ + 1 = 3d + 5`; the hypothesis `6d + 8 < (n-2)^{1/5}` leaves the
required margin `k < N^{1/5}` with room to spare.

**Step 5 (rooted complement reduction — Cycle-4 verified pattern).**  Let
`r` be the root (`f(r) = +1`, forced by rank 2 of the accepting chain).
Every `G_i` (for `i ≥ 1`) is a cyclic `O*`-interval containing `r`; its
complement is a cyclic interval avoiding `r`, i.e. an ordinary linear
interval of the cut order `V_r = (r+1, …, r-1)` on `N = q - 1 = n - 2`
points.  The complement sequence `V_r = G_1^c ⊃ G_2^c ⊃ … ⊃ G_q^c = ∅`
read backwards is a maximal chain `∅ ⊂ … ⊂ V_r` of ordinary linear
intervals (sizes `0, 1, …, N`), with sums
`f(G_i^c) = f(Z_q) - f(G_i) = 1 - f(G_i)`, all bounded by
`k := k₀ + 1 = 3d + 5` in absolute value.

**Step 6 (probability).**  Under uniform normalized `f` conditioned on
`f(r) = +1` (probability `m/q`), the restriction `f|V_r` is uniformly
balanced on the `N = n-2` linearly ordered points (Cycle-4 audited fiber
argument).  By FLSY Theorem 4.4 with parameter `k = 5 + 3d < N^{1/5}`
(hypothesis `6d + 8 < N^{1/5}` gives margin), for `N` large:

```text
Pr[ ∃ k-balanced maximal linear-interval chain on V_r ] ≤ 2^{-c N^{1/5}}.
```

Every accepted `f` produces such a chain for its root `r`, so

```text
H(P) ≤ Σ_r Pr[f(r) = +1] · 2^{-cN^{1/5}} = q·(m/q)·2^{-cN^{1/5}}
     = (n/2)·2^{-c(n-2)^{1/5}}.        ∎
```

## 4. Remarks

1. **Why `t` does not appear.**  The hull argument processes one accepting
   chain; which copy owns each `I_j` never matters — only that every copy's
   intervals are `d`-dense.  This is strictly stronger than a union bound
   over copies.
2. **Sharpness of the density hypothesis.**  A single transposition circle
   already has defect `Θ(q)` sets, and there hybrid rescue is real at
   finite `n` (the 122 verified certificates), so some hypothesis is
   necessary; whether the `n^{1/5}` threshold is optimal is open (it is
   inherited from FLSY's exponent).
3. **Relation to the finite data.**  The bound is asymptotic; at
   `n = 62` the right-hand side is far above 1, so the measured 69.7%
   pair-swap rescue is fully consistent.  The theorem says the observed
   slow decay cannot flatten out.
4. **What it kills.**  All bounded-displacement or bounded-defect circle
   families, with any polynomial (or even exponential) number of copies,
   including every "local shuffle" derandomization candidate.  Any
   surviving multi-RR route must use circles at defect `≥ n^{1/5}` from
   every common reference — i.e. genuinely global relabelings — while, by
   Theorem C (conditional) and the empirical record, all tested global
   families have low switch depth or no mid-range structure at all.

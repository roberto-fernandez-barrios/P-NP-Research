# Cycle 5: switch structure of multi-RR unions — theorems and obstructions

**Base commit:** `745f2bdf8b6d1e472279da913245aa048b36112c`
**Date:** 2026-08-21
**Scope:** literal unions of ∞-fixing relabelings of the corrected `RR_n`,
under the interval-walk semantics of `hybrid_definitions.md` (Lemma 5A.1,
computationally cross-checked against the literal induced-DAG reference).
Notation: `q = n-1` odd, orders `O_1 = id, O_2, …, O_t` on `Z_q`,
plus word `w` (m ones), middle sizes `[3, q-3]`.

Epistemic labels follow the repository state machine.  Theorem A is
self-contained and unconditional.  Theorem C imports Lemma SEG, whose status
is `PROOF CANDIDATE (reconstruction of FLSY's own technique)`, so Theorem C
is `CONDITIONAL`.

---

## 1. Where switching can happen

Recall (5A): in an accepted chain of the union, a switch between copies
occurs either **at a common interval** of the two circles or **across a
cross pair** `(A, A∪{y})`, `A ∈ Int(O_i)`, `A∪{y} ∈ Int(O_j)`.  Sizes
`0, 1, q-1, q` are common for every pair of circles, so switching at the
extreme sizes is always free.  The middle sizes are where structure decides.

**Definition (middle switch depth).**  `D_mid(P)` is the maximum, over all
coloring-free nested sequences `I_1 ⊂ … ⊂ I_{q-1}` (`|I_j| = j`, each an
interval of ≥ 1 order of `P`), of the number of switches counted among sizes
in `[3, q-3]` (for `t = 2`: the number of adjacent unequal pairs in the
subsequence of single-label chain elements of middle size; computed exactly
by `experiments/cycle05_switch_depth.py`).

Every accepted chain of every coloring switches at most `D_mid(P)` times in
the middle, by definition.

**Exact computed values** (`cycle05_switch_depth.py`, q = 13, 17, 21):

| relative structure | `D_mid` |
|---|---|
| multiplier `a` (invertible, `a ≠ ±1`) | 0, 0, 0 |
| transposition `(0,2)` | 0, 0, 0 |
| transposition `(0, q/4)`, `(0, ⌊q/2⌋)` | 0–1, 1, 1 |
| block swap (len 3 or q/4, offset ⌊q/2⌋) | 1, 1, 1 |
| adjacent pair-swap `(1,0,3,2,…)` | 3, 5, 7 = `(q-7)/2` |

---

## 2. Theorem A: affine relative structure has exactly zero hybrid gain

**Theorem A (repaired statement).**  Let `q ≥ 7` and let
`P = (π_1, …, π_t)` be ∞-fixing relabelings such that for every pair
`i ≠ j` the **precomposition** relative map `π_i^{-1} ∘ π_j` is affine on
`Z_q`: `x ↦ a_{ij} x + b_{ij}` with `a_{ij} ∉ {1, q-1}` (mod `q`; pairs
with `π_i^{-1} ∘ π_j` dihedral, i.e. `a_{ij} ∈ {±1}`, have literally
identical interval circles and are merged first).  Equivalently: `P` is a
global relabeling `π ∘ (φ_1, …, φ_t)` of a list of affine maps `φ_j`.
Then

```text
G(P) = 0:
```

the literal union `F(P)` accepts a balanced coloring iff some individual
copy accepts it.  In particular `H(P) = I(P) ≤ t·A_n = t·exp(-Ω(n^{1/5}))`.

Status: `ADVERSARIALLY REVIEWED — SOUND AFTER REPAIRS`
(`audits/cycle05_theorems_adversarial.md`).  **Warning recorded by the
audit:** the cycle's original statement hypothesized the *postcomposition*
map `π_j ∘ π_i^{-1}` affine; that version is **FALSE** — the two
compositions differ by conjugation, and the audit exhibits verified
counterexamples `P = (π, ψ∘π)`, `ψ = ×2`, with hybrid-only colorings at
`n = 22` and `n = 24` (two independent implementations).  The proof below
needs exactly the precomposition form: the pair of circles
`(π_i(Std), π_j(Std))` is ground-set-isomorphic to `(Std, ρ(Std))` for
`ρ = π_i^{-1}π_j`, and `Std`'s stabilizer is the dihedral subgroup of the
affine group.  Empirical confirmation (all with `π_1 = id`, where the two
readings coincide): exhaustive scans at `n = 22..30` for all invertible
multipliers tested (`common rejects` up to 667, `rescued = 0` in every
case: `scan_results.jsonl`, tags `mult:*`), consistent with the Cycle-4
certificates (`hybrid-only accepts = 0`).

The proof has three lemmas.  Throughout, `O` is the standard circle and
`O'` the image circle of an affine map `φ(x) = ax+b`; `Int(O')` is the set
of arithmetic progressions with difference `a` (as subsets of `Z_q`), since
`φ` maps intervals to such APs and all APs of difference `a` arise so.  The
offset `b` is irrelevant (it rotates the image circle, which fixes its
interval family), so we take `φ(x) = ax`.

**Lemma A.1 (AP–interval overlap).**  For `2 ≤ s ≤ q-2` and `a ∉ {±1}`, no
difference-`a` AP of size `s` is a cyclic interval.

*Proof.*  For a set `S` of size `s ≤ q-1`, call `x ~ x+1` (both in `S`) an
adjacency.  The adjacency graph on `S` has maximum degree 2 and no cycle
(a cycle forces `S = Z_q`), so `S` is an interval iff it has `s-1`
adjacencies.  Let `h = a^{-1} mod q`, `1 ≤ h ≤ q-1`.  In the AP
`{c, c+a, …, c+(s-1)a}`, an adjacency is a pair of indices `j₂ = j₁ + r`
with `ra ≡ 1`, i.e. integer index difference `r ∈ {h, h-q}`.  The number of
adjacencies is therefore `max(0, s-h) + max(0, s-(q-h))`.  Setting this
equal to `s-1`: if both terms are positive it equals `2s-q`, forcing
`s = q-1`, excluded; if only the first, `h = 1` (`a = 1`), excluded; if only
the second, `q-h = 1` (`a = -1`), excluded; if neither, `s = 1`.  ∎

Consequently the only common intervals of `(O, O')` have sizes
`0, 1, q-1, q`.

**Lemma A.2 (cross-pair exclusion).**  For `a ∉ {±1}` and `q ≥ 7`, every
cross pair `(A, A∪{y})` between `O` and `O'` (either direction) has
`|A| ≤ 2` or `|A| ≥ q-3`.

*Proof.*  Direction `O → O'`: `A` is an interval of size `j`,
`B = A∪{y}` a difference-`a` AP of size `s = j+1`.  If `y` is adjacent to
`A` then `B` is an interval and an AP, so by Lemma A.1 `s ≤ 1` or
`s ≥ q-1`, giving the boundary cases.  Otherwise `B`'s adjacency graph is a
path on the `j` points of `A` plus the isolated vertex `y`, so it has a
component of size `j = s-1` and one of size 1.  In index space the
adjacency graph of the AP is the graph on `{0,…,s-1}` with steps `h` and
`q-h` (`h = a^{-1}`).  By complement symmetry of cyclic intervals and APs
(`Int` of both circles is complement-closed, and complementing swaps the
direction and sizes `(j, j+1) ↔ (q-j-1, q-j)`), it suffices to treat
`s ≤ (q+1)/2`.

If `s ≤ (q+1)/2` and `s < min(h, q-h) + 1` the graph is empty
(`s-1 = j ≤ 1`).  Otherwise let `g = min(h, q-h) ≤ s-1`.  If `g < s-1` and
the other step is `≥ s`, the components are the residue classes mod `g`
inside `{0,…,s-1}`: `g` paths of sizes `⌈s/g⌉` or `⌊s/g⌋`.  Component
sizes `(s-1, 1)` force `g = 2` and `⌈s/2⌉ = s-1`, i.e. `s ≤ 3`, giving
`j ≤ 2`.  If both steps are `≤ s-1` then `h + (q-h) = q ≤ 2s-2 ≤ q-1`,
impossible.  The remaining boundary `g = s-1` gives a single edge and
components `(2, 1, …)`, so `j ≤ 2`.

(The complement reduction is used only inside direction `O → O'`;
direction `O' → O` below is handled directly at all sizes, so there is no
circularity.)

Direction `O' → O` (repaired per the adversarial audit): `A` is an AP of
size `j`, `B = A∪{y}` an interval of size `j+1`, `A = B∖{y}`.  If `y` is
an endpoint of `B`, `A` is an interval and an AP: Lemma A.1 gives
`j ≤ 1` or `j ≥ q-1`.  If `y` is interior, `A` is a union of two runs
separated by the one-point hole `{y}`, with gap multiset `{1, q-j-1}` and
adjacency count `j-2`.  As an AP its adjacency count is
`max(0, j-h) + max(0, j-(q-h))`.  Equating: both terms active gives
`j = q-2` (allowed boundary); neither gives `j = 2` (allowed); one term
active gives `min(h, q-h) = 2`, i.e. `a = ±(q+1)/2`, whose size-`j` APs
are two runs of sizes `⌈j/2⌉, ⌊j/2⌋` with gaps
`(q+1)/2 - ⌈j/2⌉` and `(q-1)/2 - ⌊j/2⌋`.  For middle sizes
`3 ≤ j ≤ q-4` both gaps are `≥ 2`, so the required multiset `{1, q-j-1}`
cannot match; the matches occur exactly at `j ∈ {q-3, q-2, q-1}` (gap
multiset `{2, 1}` at `j = q-3`, e.g. `{0,1,4,5}` at `q = 7`) and at
`j = 2` — all inside the allowed boundary `|A| ≤ 2` or `|A| ≥ q-3`.  ∎

**Lemma A.3 (boundary conversion).**  Let `O'' ∈ P` be any order and `f`
normalized.  (i) If `T` is an `O''`-interval of size 3 with `f(T) = 1`,
then there is a pure-`O''` compatible chain `I_1 ⊂ I_2 ⊂ I_3 = T`.
(ii) If `S` is an `O''`-interval of size `q-3` with `f(S) ∈ {0, 2}`, then
there is a pure-`O''` compatible continuation `S ⊂ I_{q-2} ⊂ I_{q-1}`.

*Proof.*  (i) `T` consists of three `O''`-consecutive points with signs
summing to 1, so signs are `{+,+,-}` in some arrangement.  Of the two
`O''`-sub-pairs (first two, last two), at least one is bichromatic (if the
first two were monochromatic `++`, the last point is `-`, so the last two
are `+-`).  Take `I_2` = that pair (`f = 0`) and `I_1` its plus point.
(ii) The complement `T' = Z_q ∖ S` is an `O''`-interval of size 3 with
`f(T') = 1 - f(S) ∈ {1, -1}`.  Its sign pattern (two of one sign, one of
the other) always has at least one endpoint of the majority sign; if
`f(S) = 0` (`f(T') = 1`, pattern two `+` one `-`) pick a plus endpoint `y`;
if `f(S) = 2` (`f(T') = -1`) pick a minus endpoint `y`.  Then
`I_{q-2} = S ∪ {y}` is an `O''`-interval with `f = 1`, and
`I_{q-1} = I_{q-2} ∪ {z}` for either remaining point is a co-singleton
(interval of every circle) with `f ∈ {0, 2}`.  ∎

*Proof of Theorem A.*  Let `C` be an accepted chain for `f`, with
finite parts `I_1 ⊂ … ⊂ I_{q-1}`.  By Lemmas A.1–A.2 applied to every pair
of orders, each `I_j` with `3 ≤ j ≤ q-3` is an interval of exactly one
order, and consecutive middle sets cannot lie in different orders (that
would be a cross pair at middle size).  Hence one order `O''` owns the
entire middle: `I_j ∈ Int(O'')` for all `3 ≤ j ≤ q-3`.  The chain's own
compatibility gives `f(I_3) = 1` and `f(I_{q-3}) ∈ {0,2}`.  Replace sizes
`1, 2` by Lemma A.3(i) applied to `T = I_3`, and sizes `q-2, q-1` by
Lemma A.3(ii) applied to `S = I_{q-3}`.  The rebuilt chain is pure `O''`
and compatible at every size, so the copy `O''` accepts `f` individually.
∎

**Remarks.**  (1) The theorem is sharp in two directions: for `q = 5` the
middle range is empty and the statement is vacuous; and dropping the affine
hypothesis destroys it already for a single transposition (the verified
`n = 22` hybrid-only certificates).  (2) The proof gives slightly more: for
ANY list `P`, an accepted chain that is pure on `[3, q-3]` certifies
individual acceptance.  Hybrid gain therefore lives entirely on chains that
switch at middle sizes.

---

## 3. Transposition pairs: `D_mid ≤ 1`

**Theorem B.**  Let `O₂` be obtained from the standard circle by
transposing two non-adjacent points `u, v`.  Then:

1. The common intervals of middle size are exactly the intervals `I` with
   `|I ∩ {u,v}| ≠ 1`, together with the four exceptional sets
   `[u, v-1], [u+1, v], [v, u-1], [v+1, u]`.
2. Every `O₂`-interval containing exactly one of `u, v` has the form
   `(I ∖ {u}) ∪ {v}` or `(I ∖ {v}) ∪ {u}` for a standard interval `I`
   containing exactly the other point.
3. `D_mid ≤ 1`: within middle sizes, no chain alternates
   `O₁`-only → `O₂`-only → `O₁`-only or `O₂`-only → `O₁`-only → `O₂`-only.

Status: parts 1–2 `PROVED`: `π` fixes every point other than `u, v`, so a
set containing neither or both occupies the same positions in both circles
(common), and `Int(O₂) = π(Int(O₁))` consists of the unchanged intervals
plus the images `(I∖{u})∪{v}` (for `I ∋ u ∌ v`) and symmetrically; such an
image is itself a standard interval iff removing `u` leaves an interval
(`u` an endpoint) and adding `v` extends it (`v` adjacent to the result),
which happens exactly for the four listed arcs.  The count of common
intervals per size derived this way matches the exhaustive `--list-cross`
profiles at `n = 22` exactly.  Part 3 `PROOF CANDIDATE (recorded case
skeleton below; exact D_mid DP confirmation for q ≤ 21)` — the skeleton
covers the anchored-shape cases; a fully written-out case enumeration has
not been produced this cycle, and the claim is used only qualitatively
(transposition-class families are in the low-depth regime).

*Skeleton of 3.*  Sets containing neither or both of `u, v` are common
(their occupied position sets are unchanged by the swap).  So every
single-label ("only") chain element contains exactly one of `u, v`; since
the chain is nested, all only-elements of one chain contain the same first
point, say `v`.  `O₁`-only elements are standard intervals `J ∋ v ∌ u`;
`O₂`-only elements are `S = (I∖{u})∪{v}` with `I` a standard interval
`∋ u ∌ v`.  If `u` is interior to `I`, then `S ∖ {v}` has points on both
sides of `u`, and a standard interval covering `S` while avoiding `u` must
be the co-singleton `Z_q∖{u}` (size `q-1`, not middle), while a standard
interval inside `S` containing `v` must stop at the isolated point `v`, so
has size ≤ 2 unless `S ⊇ [α, v]`, which forces `d = v-1` and makes the
relevant sets the exceptional common intervals.  If `u` is an endpoint of
`I` (`S = [u+1, d] ∪ {v}` up to reflection), the same computation shows:
any `O₁`-only superset of `S` in middle sizes is `[u+1, β]` with `β > v`,
and any `O₂`-only superset of such a `[u+1, β]` again requires a standard
interval avoiding `v` that contains points on both sides of `v` — a
co-singleton.  Dually for subsets.  Hence after the unique possible
`O₁`-only ↔ `O₂`-only boundary, the chain can never return: at most one
middle alternation.  ∎

Combined with the sweep data (`trans:*` rows), `D_mid ≤ 1` families show
hybrid rescue rates that decay monotonically in `n`
(best-δ ratio 36.4% → 24.5% → 17.9% → 13.9% → 10.9% for `n = 22 … 30`).

---

## 4. Pair-swap circles: `D_mid = Θ(q)`

Let `O₂` be the adjacent-pair-swap circle `(1, 0, 3, 2, 5, 4, …, q-2)` on
odd `q` (last point fixed).

**Theorem D (deep alternation).**  `D_mid ≥ (q-7)/2`, witnessed by the
nested chain that from `{0,1,2,3}` repeatedly adjoins
`4k` (an `O₁`-only prefix `{0..4k}`), then `4k+1` (common), then `4k+3`
(an `O₂`-only set `{0..4k+1} ∪ {4k+3}`), then `4k+2` (common).
Status: `PROVED (explicit construction, machine-verified)`;
the exact DP gives equality `D_mid = (q-7)/2` for `q = 13, 17, 21`
(3, 5, 7), so the construction is optimal at least there.

This is the family outside every low-depth obstruction, and empirically it
is the one whose rescue rate decays slowest: 87.4–87.9% of common rejects
rescued at `n = 24, 26, 28, 30` (`pairswap:*` rows), then a slow decline
83.3% → 69.7% over `n = 38 … 62` in the sampled regime
(`pairswap-sample:*`).  Despite its linear switch depth, this family is
killed **unconditionally** by the density obstruction (Theorem E in
`dense_circle_obstruction.md`): its circle is 2-dense w.r.t. the standard
one, so `H(id, pairswap) ≤ (n/2)·2^{-c(n-2)^{1/5}}`.  Switch depth and
hull density are thus genuinely independent parameters, and the measured
slow decay is the finite-`n` shadow of a stretched-exponential collapse.

---

## 5. Lemma SEG and the conditional low-depth obstruction

**Lemma SEG (segment interval obstruction; status: PROOF CANDIDATE —
reconstruction of FLSY's technique; independently adversarially reviewed
with verdict SOUND WITH REPAIRS, all repairs statement-level; see
`audits/cycle05_seg_lemma_adversarial.md` §7 for the endorsed form with
full quantifiers.  NOT a published theorem: the conditional label on the
theorems below stands regardless.)**  Endorsed form, abbreviated: there
are universal `c, C > 0, L₀` such that for every `N`, every `σ` with
`|σ| ≤ 1`, `f` uniform on colorings of `[N]` with `f([N]) = σ`, fixed
intervals `∅ ≠ A ⊆ B ⊆ [N]` with `L = |B∖A| ≥ L₀`, and `1 ≤ k < L^{1/5}`:

```text
Pr[ ∃ interval chain A = D_0 ⊂ D_1 ⊂ … ⊂ D_L = B, all |f(D_i)| ≤ k ]
    ≤ C·√N·exp(-c L^{1/5}),
```

with an extra factor `(L+1)` for "some `B ⊇ A` of the given length", and
verbatim on the cyclic order `Z_N` provided `B ≠ Z_N` (cut at any point of
the complement).  The FLSY engine (anti-concentration of the discrete
Fréchet distance of the two independent extension walks, milestones +
first-passage lower tails) is translation invariant; the anchor enters
only through bookkeeping, and the initial offset `f(A)` is bounded by `k`
on the event itself.  The audit's Monte Carlo (N = 2000, exact DP,
92k balanced colorings) shows clean monotone decay with no anomaly.

**Theorem C (conditional).**  Assume Lemma SEG.  There are universal
`c', C > 0` such that for every ∞-fixing list `P` with `t` orders and
`D = D_mid(P)`, and `L* = (q-7)/(D+1) ≥ C (log q)^5`:

```text
H(P) ≤ t·A_n + G(P),
G(P) ≤ t · q^4 · O(√q) · exp(-c' (L*)^{1/5}).
```

*Proof sketch.*  A hybrid-only accepted chain switches at most `D` times in
the middle, so it contains a pure run of `≥ L*` consecutive middle sizes in
one order `o`: a compatible pure-`o` interval growth from some `A` to some
`B ⊇ A`, `|B∖A| ≥ L*`, with all running sums in `{0,1,2}` (2-balanced with
offset ≤ 2).  Union-bound over the order (`t`), the pair `(A, B)`
(≤ `q²·q` choices: `A` by size and start, `B ⊇ A` by extension split), and
apply Lemma SEG with `k = 2 < (L*)^{1/5}` on the cyclic order `o` (cutting
the circle at an endpoint of the complement of `B`, which the growth never
enters).  The `O(√q)` unconditioning and polynomial union factors are
absorbed for `L* ≥ C (log q)^5`.  ∎

**Corollaries (conditional on SEG).**
1. Transposition and block-swap pairs (`D ≤ 1`):
   `H(P) ≤ exp(-Ω(q^{1/5}))` — hybrid routing cannot make such pairs (or
   any `poly(n)`-size list of them: `D_mid` of a list is bounded by pairwise
   contributions only if switching stays pairwise… state carefully: for a
   list, `D = D_mid(P)` of the whole list is the parameter; a list of many
   transpositions can have larger joint depth and is NOT covered pairwise)
   — scope: the stated bound applies to the list's own `D_mid`.
2. Any family with `D_mid = O(q^{1-δ})`: `H(P) ≤ exp(-Ω(q^{δ/5}))`, still
   stretched-exponentially far from the `1/poly` needed (via FLSY
   Lemma 2.3) to imply O01.

**What Theorem C does not cover:** `D_mid = Ω(q/polylog q)` families —
in particular pair-swap-type circles.  Those are instead covered
unconditionally by the density obstruction (Theorem E,
`dense_circle_obstruction.md`) whenever all circles are `o(n^{1/5})`-dense
w.r.t. one common reference.  The class escaping **both** theorems needs
circles that are simultaneously far (defect `≥ n^{1/5}`) from every common
reference and of switch depth `≥ q/polylog(q)`; no structured family with
both properties has been found in this cycle (transpositions and block
swaps are far but have depth ≤ 1; pair-swap has linear depth but is
2-dense; multipliers and random pairs have no middle structure at all).

---

## 5b. Theorem F: unified two-copy obstruction (conditional on SEG)

The proof of Theorem E never uses the family-wide density hypothesis, only
the density of the accepting chain's own states.  Record this as:

**Lemma E\* (chain version of Theorem E).**  If `f` is accepted by an
∞-fixing union via a chain all of whose finite parts have `O*`-defect
`≤ d` for one circle `O*`, and `6d + 8 < (n-2)^{1/5}`, then `f` admits a
`(5+3d)`-balanced maximal linear-interval chain on the `n-2` points of the
cut order at its (plus) root.  (Proof: Steps 1–5 of Theorem E verbatim.)

**Lemma RS (run sandwich, t = 2).**  Let `P = (id, π)` be a two-copy
∞-fixing union and let a chain have all pure runs of length `≤ L` in the
middle.  Then every middle state has `O_1`-defect `≤ L + 2`.

*Proof.*  A state `S` in an `O_1`-run has defect 0.  A state `S` in an
`O_2`-run: with `t = 2` the next run (or the first common state after the
run, or the co-singleton at size `q-1`) lies in `Int(O_1)`; let `B` be that
first later chain state in `Int(O_1)`.  Then `S ⊆ B`, `B` is an
`O_1`-interval, so the minimal `O_1`-hull of `S` is contained in `B` and
`def(S) ≤ |B| - |S| ≤ L + 2`.  ∎

**Theorem F (conditional on Lemma SEG).**  There is `c'' > 0` such that
for all sufficiently large even `n` and EVERY ∞-fixing permutation `π`,

```text
H(id, π) ≤ poly(n) · exp(-c'' n^{1/25}).
```

*Proof sketch.*  Set `L = ⌊n^{1/5}/7⌋`.  Every accepting chain either has
a pure middle run of length `> L` — an event bounded, by the union bound
over (order, endpoints) and Lemma SEG with `k = 2`, by
`poly(n)·exp(-c L^{1/5}) = poly(n)·exp(-c' n^{1/25})` — or has all runs
`≤ L`, hence by Lemma RS is `(L+2)`-dense w.r.t. `O_1`, and Lemma E\* with
`d = L + 2` (`6d + 8 < (n-2)^{1/5}` holds by the choice of `L`) plus FLSY
Theorem 4.4 with `k = 5 + 3d < (n-2)^{1/5}` bounds that event by
`(n/2)·2^{-c(n-2)^{1/5}}`.  ∎

This removes every structural hypothesis in the two-copy case: **no single
relabeled partner can give the RR family more than stretched-exponentially
small union acceptance** (conditional on SEG; the density branch is
unconditional).  It retro-explains all `t = 2` scan data: every measured
family's rescue rate decays.

**The `t ≥ 3` stitching gap.**  For `t ≥ 3` the sandwich argument gives
each `O_i`-run density w.r.t. the order of the NEXT other-order run, which
varies along the chain; the hull argument needs one reference for the whole
chain.  The isolated missing statement is:

> **Lemma M (open).**  There are `d(n), D(n)` with `d = o(n^{1/5})` and
> `D = o(q/(log q)^5)` such that in every ∞-fixing union, every accepting
> chain either has ≤ `D` middle switches or has all middle states of
> defect ≤ `d` w.r.t. a single circle (which may depend on the chain, drawn
> from the list or not, at a union-bound cost).

SEG + Lemma M + Lemmas E\*/RS-style bookkeeping would extend Theorem F to
every `poly(n)`-size ∞-fixing list, closing the multi-RR route entirely.
Lemma M is TRUE for `t = 2` (Lemma RS).  Its status for `t ≥ 3` is open;
no candidate counterexample family is known (all tested families are
covered), but absence of a counterexample is not evidence of a proof.

## 6. The relaxed positive target

By FLSY Lemma 2.3 (verified import), a `(p, 1)`-balanced-chain system of
size `s` yields a 1-balanced-chain system of size `O(s·n/p)`.  Since
`|F(P)| ≤ 2 + t(n-1)²`:

**Observation.**  If for some explicit or existential list `P_n` with
`t(n) = poly(n)` the union satisfies `H(P_n) ≥ n^{-O(1)}`, then
`N(n) = poly(n)` and O01 is resolved positively.  Full coverage
(`H = 1`) is NOT required.

This sharpens the Cycle-5 mission: the battle is whether
`sup_{|P| ≤ poly} H(P)` is inverse-polynomial or stretched-exponential.
Theorem A (unconditional) settles it for relabelled-affine lists, Theorem
E (unconditional) for common-reference-dense lists — pair-swap included —
and Theorems C/F (conditional on SEG) for low-depth lists and for every
two-copy union.  What remains open is exactly the `t ≥ 3`
far-and-deep-switching class of §5b and ∞-moving relabelings.

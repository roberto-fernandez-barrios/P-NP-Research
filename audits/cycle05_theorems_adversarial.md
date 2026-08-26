# Cycle 5 adversarial audit: Theorem A (affine hybrid-vanishing) and Theorem E (dense-circle obstruction)

**Supersession notice (2026-08-27):** This audit is retained as historical
evidence.  The final cross-model audit independently validated the repaired
precomposition Theorem A as sound as stated and identified three additional
conclusion-preserving quantifier/normalization corrections for Theorem E
(integer `D`, normalization of the common reference only, and the actual
growing FLSY parameter).  The finalized canonical proofs apply those
corrections; consult `cycle05_sol_final_cross_model_validation.md` and
`cycle05_final_correction_integration.md` for the authoritative status.

**Role:** SKEPTIC (independent adversarial review).
**Date:** 2026-08-21.  **Base commit:** `745f2bd`.
**Objects audited:** `research_cycle_05/switch_structure_theory.md` §2 (Theorem A, Lemmas A.1–A.3),
`research_cycle_05/dense_circle_obstruction.md` (Theorem E, Steps 1–6 and §2), against the semantics of
`research_cycle_05/hybrid_definitions.md` (Lemma 5A.1, trusted per upstream machine cross-check) and the
verified FLSY import (`research_cycle_05/flsy_reconstruction.md` §1.3).

**Method.** Every lemma was independently re-derived by hand (derivations summarized below), and every
computational claim was checked with auditor-written code that shares no logic with the proposer's tools:
a from-scratch literal induced-subset-DAG DP built directly from the corrected `RR_n` definition
(`experiments/cycle05_audit_thm_pipeline.cpp`), plus direct set-computation lemma checks
(`experiments/cycle05_audit_thm_lemmas.py`).  The proposer's `brute_accepts` and `cycle05_union_scan.exe`
were used only as the *second side* of differential tests.  My implementation was validated against the
proposer's literal reference on **all** normalized colorings at n = 10, 12 for two union families
(0 mismatches), and its `COMMON <hex> <flag>` dumps were diffed against the proposer's engine at
n = 24, 26 (pairswap) and n = 28 (mult 2): **byte-identical** in every case.

## Reproduction commands

```
python -B experiments/cycle05_audit_thm_lemmas.py
g++ -O2 -std=c++17 -o experiments/cycle05_audit_thm_pipeline.exe experiments/cycle05_audit_thm_pipeline.cpp
./experiments/cycle05_audit_thm_pipeline.exe --selftest
python -B experiments/cycle05_audit_thm_diffsmall.py          # my DP vs proposer brute_accepts, n=10,12

# Theorem A computational checks (independent literal DP; ~1.3 s each at n=22, ~3 min at n=28)
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 22 --copy2 mult:2:0
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 22 --copy2 mult:5:0
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 22 --copy2 mult:8:0
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 22 --copy2 mult:2:3     # b != 0
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 22 --copy2 mult:13:5    # b != 0
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 28 --copy2 mult:2:0 --dump audits/audit_common_n28_mult2.txt

# Theorem A falsification search and standalone counterexample verification
./experiments/cycle05_audit_thm_pipeline.exe --conj --n 24 --a 2 --seed 1 --iters 30000 --max-finds 2
./experiments/cycle05_audit_thm_pipeline.exe --conj --n 22 --a 2 --seed 7 --iters 400000 --max-finds 1
python -B experiments/cycle05_audit_thm_a_counterexample.py 0   # n=24 case, proposer-reference check
python -B experiments/cycle05_audit_thm_a_counterexample.py 1   # n=22 case

# Theorem E pipeline checks (exhaustive; minimax over rescued colorings)
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 22 --copy2 pairswap --dump audits/audit_common_n22_pairswap.txt
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 24 --copy2 pairswap --dump audits/audit_common_n24_pairswap.txt
./experiments/cycle05_audit_thm_pipeline.exe --scan --n 26 --copy2 pairswap --dump audits/audit_common_n26_pairswap.txt

# Differentials vs the proposer engine (dumps compared with sort + diff; all IDENTICAL)
CYCLE05_DUMP_COMMON=1 ./experiments/cycle05_union_scan.exe --n 24 --perm 1,0,3,2,...,21,20,22 2> audits/proposer_common_n24_pairswap.txt
CYCLE05_DUMP_COMMON=1 ./experiments/cycle05_union_scan.exe --n 26 --perm 1,0,3,2,...,23,22,24 2> audits/proposer_common_n26_pairswap.txt
CYCLE05_DUMP_COMMON=1 ./experiments/cycle05_union_scan.exe --n 28 --mult 2 2> audits/proposer_common_n28_mult2.txt
```

---

# T1. Theorem A — affine relative structure gives exactly zero hybrid gain

## T1.a Lemma A.1 (AP–interval overlap) — verdict: PASS

Independent re-derivation.  For `S = {c, c+a, …, c+(s-1)a}` (all distinct, `gcd(a,q)=1`, `q` odd, `q`
**not** assumed prime), an adjacency `{x, x+1} ⊆ S` corresponds to a unique ordered index pair
`(j₁, j₂)` with integer difference `j₂ − j₁ ≡ h (mod q)`, `h = a^{-1}`; within `{0,…,s−1}` the only
representatives are `h` and `h − q`, giving exactly `max(0, s−h) + max(0, s−(q−h))` adjacencies — no
double counting is possible because the pair `{x, x+1}` fixes `(j₁, j₂)` and hence a single integer
difference (and `h = q−h` cannot occur for odd `q`).  The adjacency graph is a subgraph of the `q`-cycle,
so for `s ≤ q−1` it is a disjoint union of paths (a cycle would force `S = Z_q`), and
`S` interval ⟺ `s−1` edges ⟺ connected: correct.  The four-way case split is exhaustive and each branch
forces `s = q−1`, `a = 1`, `a = −1`, or `s = 1` exactly as written.  Note the both-terms-positive count
`2s − q` never exceeds `s−1` for `s ≤ q−1`, so the formula never contradicts the path-forest structure.

Machine check (`cycle05_audit_thm_lemmas.py::check_A1`): `q ∈ {7, 11, 21, 25}` (both composite values
included), **all** invertible `a`, **all** `s ∈ [2, q−1]`, three offsets `c`: formula exact everywhere;
statement (no AP of size `2..q−2` is an interval for `a ∉ {±1}`) exact; controls (`a = ±1` APs are
intervals; every size-`q−1` AP is an interval) exact.  **PASS.**

## T1.b Lemma A.2 (cross-pair exclusion) — verdict: statement PASS, proof REPAIRED

**Statement is true** — verified two ways: (i) exhaustive direct set computation of *every* cross pair in
both directions for `q ∈ {7, 11, 21, 25}` and all invertible `a ∉ {±1}` (`check_A2`): every cross pair has
`|A| ≤ 2` or `|A| ≥ q−3`; (ii) my own general-`q` derivation below.

**Direction `O → O'`** (interval + point = AP), `s ≤ (q+1)/2`: re-derived and correct, including:
the `y`-adjacent case routes through A.1 correctly (the corner where `y` is adjacent on *both* sides forces
`A = Z_q∖{y}`, `|A| = q−1`, inside the allowed boundary); empty-graph case gives `j = 1`; the residue-class
case (`g < s−1`, other step `≥ s`) is right — components are residue classes mod `g`, `(s−1, 1)` forces
`g = 2` and `s ≤ 3`; the `g = s−1` boundary gives one edge, components `(2,1,…)`, `j ≤ 2`; both steps
`≤ s−1` contradicts `s ≤ (q+1)/2` via `h + (q−h) = q ≤ 2s−2`.  All sub-cases close.

**Complement-symmetry reduction:** complementing maps an `O → O'` cross pair at sizes `(j, j+1)` to an
`O' → O` cross pair at sizes `(q−j−1, q−j)` — it **swaps direction**.  So "it suffices to treat
`s ≤ (q+1)/2`" inside direction `O → O'` is legitimate *only because* direction `O' → O` is subsequently
handled at **all** sizes with no back-reference (it is; no circularity).  Valid but fragile drafting; a
clarifying sentence is recommended.

**Direction `O' → O`, `y` interior — the write-up is wrong in three places (REPAIR REQUIRED):**

1. The gap multiset of `A = B∖{y}` (`B` an interval of size `j+1`, `y` interior) is `{1, q−j−1}`
   (the one-point hole plus the outer gap), **not** "`{2, q−j}`" as written.
2. The APs of `a = ±(q+1)/2` (`h = 2` resp. `q−2`) of size `j` are, up to rotation/reflection, the two runs
   `[0, ⌈j/2⌉−1] ∪ [(q+1)/2, (q+1)/2+⌊j/2⌋−1]`, whose two gaps are `(q+1)/2 − ⌈j/2⌉` and
   `(q−1)/2 − ⌊j/2⌋` — **`j`-dependent**, not "`(q±1)/2` on both sides".
3. "Matching … forces `q ≤ 5`" is **false**: the match succeeds at `j = q−3` for *every* odd `q` (gaps
   `{2, 1}`).  Explicit witness at `q = 7`: `A = {0,1,4,5}` is the difference-4 AP `0,4,1,5` **and**
   `B∖{6}` for the interval `B = [4,1]`; machine check found 128 such `|A| = q−3` witnesses across the
   four tested `q`.  These sit inside the *allowed* boundary `|A| ≥ q−3`, so the lemma survives, but the
   proof text as written proves the wrong thing.

**Exact repair for the interior case.**  Equating adjacency counts `j−2 = max(0, j−h) + max(0, j−(q−h))`
gives four cases: both active ⟹ `j = q−2` (allowed boundary); neither active ⟹ `j = 2` (allowed); one
active ⟹ `min(h, q−h) = 2`, i.e. `a = ±(q+1)/2`.  In the last case, for **middle sizes**
`3 ≤ j ≤ q−4` both AP gaps are `≥ 2` (first gap `≥ (q+1)/2 − (q−3)/2 = 2`, second `≥ 2` likewise), so the
required multiset `{1, q−j−1}` cannot match and no interior-`y` cross pair exists at middle sizes; the
matches at `j ∈ {q−3, q−2, q−1}` (and `j = 2`) are exactly the allowed boundary.  This proves the stated
conclusion for all `q ≥ 7` (for `q = 5` the middle range is empty).  The `y`-endpoint case (A.1 ⟹ `j ≤ 1`
or `j ≥ q−1`) is correct as written.

## T1.c Lemma A.3 (boundary conversion) — verdict: PASS

(i) All sign patterns of a sum-`+1` triple (`++−`, `+−+`, `−++`) contain a bichromatic consecutive
sub-pair; the constructed `I₁ ⊂ I₂ ⊂ T` is compatible (`+1, 0, +1`) and `I₂` is an `O''`-interval, `I₁` a
singleton.  (ii) `f(Z_q) = 2m − q = +1` (normalized), so `f(T') = 1 − f(S) ∈ {+1, −1}`; every such triple
has an endpoint of the majority sign (all six patterns checked); `S ∪ {y}` is an `O''`-interval because `y`
is an endpoint of the complementary interval; `f(S∪{y}) = 1` in both branches (`0+1` and `2−1`); the
co-singleton step lands in `{0, 2}` for either `z`.  Machine check: local pattern enumeration plus an
end-to-end sweep at `q = 9` over all normalized colorings and all size-`q−3` intervals with
`f(S) ∈ {0,2}`: construction always valid.  Note A.3 holds for an **arbitrary** circle `O''` (only
`O''`-consecutiveness is used) — important since the middle-owner circle need not be standard.  **PASS.**

## T1.d Main proof mechanics — verdict: PASS *given the pairwise standard/AP reduction* (but see T1.e)

With A.1/A.2 available for every pair of orders:

* Sizes `3 ≤ j ≤ q−3` lie in `[2, q−2]`, so by A.1 each middle `I_j` is an interval of exactly one order.
* Consecutive middle ownership: a switch at step `j → j+1` with both sizes in `[3, q−3]` requires a cross
  pair with `|A| = j ∈ [3, q−4]` — excluded by A.2.  Boundary steps checked one by one:
  `2→3` cross pairs are **allowed** (`|A| = 2`) and `q−3→q−2` cross pairs are **allowed** (`|A| = q−3`;
  they exist for every `q`, see T1.b) — both are harmless because the rebuilt chain replaces sizes
  `1, 2` (A.3(i) from `I₃`, which the chain's own compatibility makes `f = 1`) and `q−2, q−1`
  (A.3(ii) from `I_{q−3}`, `f ∈ {0,2}`).  Steps `3→4` (`|A| = 3`) and `q−4→q−3` (`|A| = q−4 ≥ 3`) are
  excluded for all `q ≥ 7`; at `q = 7` the middle is `{3, 4}` and the single interior step `3→4` is
  exactly the excluded one.  No switch sneaks through.
* Common-state switches inside the middle are excluded by A.1 (single ownership).
* The rebuilt chain is pure `O''` and compatible at every size, so copy `O''` accepts individually
  (Lemma 5A.1 for `t = 1`; sizes 1 and `q−1` are intervals of every circle).
* **Merging clause:** `π_j = π_i ∘ δ` with `δ ∈ D_q` (affine `a = ±1`) gives literally identical copies
  (`δ` maps standard intervals onto standard intervals), so merging is sound — **but only under the
  precomposition reading**.  Machine check (`check_merge_composition`): `π∘δ` gives the identical interval
  family; `δ∘π` generally does **not**.  This is independent evidence for the composition-order bug below.

## T1.e The hypothesis as stated is FALSIFIED — composition-order bug (critical finding)

**The bug.**  Theorem A hypothesizes: "for every pair `i ≠ j` the relative finite map `π_j ∘ π_i^{-1}` is
affine".  The proof's reduction ("`O` is the standard circle and `O'` the image circle of an affine map")
is valid for the pair `(O_i, O_j)` iff some ground-set relabeling `σ` maps `Int(O_i)` to the standard
intervals and `Int(O_j)` to an AP family.  Since `Int(O_i) = π_i(Std)` and the stabilizer of `Std` is the
dihedral group `D_q ⊂ Affine`, this happens **iff `π_i^{-1} ∘ π_j` is affine** — not `π_j ∘ π_i^{-1}`.
The two differ by conjugation, and conjugates of affine maps by arbitrary permutations are not affine.
Concretely, `P = (π, ψ∘π)` with `ψ` affine and `π` arbitrary satisfies the stated hypothesis
(`π_2π_1^{-1} = ψ`), yet the pair of circles is `(π(Std), ψπ(Std))`, isomorphic to `(Std, τ(Std))` with
`τ = π^{-1}ψπ` — an arbitrary permutation of `ψ`'s cycle type.

**Lemma-level demonstration** (`check_composition_bug_common_interval`): for `q = 21`, `ψ = ×2`, an
explicit `π` produces a pair satisfying the stated hypothesis with a **common size-3 interval**
(`{1,4,16}`), contradicting the proof's application of Lemma A.1 at middle sizes.

**Theorem-level counterexamples (G(P) > 0 under the stated hypothesis).**  Found by
`--conj` search and verified end-to-end by **two independent implementations** (my literal C++ DP and the
proposer's own `brute_accepts` reference over the literal induced-subset DAG):

* `n = 22` (`q = 21`, `ψ(x) = 2x`): `π₁ = π = [7,13,17,0,20,2,12,8,3,9,5,14,11,18,6,16,10,4,1,19,15]`
  (∞-fixing), `π₂ = ψ∘π`.  Hypothesis holds: `π₂∘π₁^{-1} = x ↦ 2x mod 21`, `a = 2 ∉ {±1}`.
  Normalized balanced coloring `f = 0xae2b3` is rejected by both copies and **accepted by the literal
  union**: `G(P) > 0`.
* `n = 24` (`q = 23`, `ψ(x) = 2x`): `π = [5,17,9,19,22,13,8,14,20,4,7,12,18,2,10,11,0,6,15,16,21,3,1]`,
  colorings `f = 0x2793aa` and `f = 0x27d2aa` are both hybrid-only.
* In both cases `π_1^{-1}π_2 = π^{-1}ψπ` is *not* affine (step sets printed by the verification script),
  so the repaired theorem (below) does not cover these pairs — consistent.

**Why the empirical record missed it:** every scanned family (`mult:*`) has `π_1 = id`, where the two
compositions coincide.

**Exact repair (statement).**  Replace the hypothesis by: *for every pair `i ≠ j` the map
`π_i^{-1} ∘ π_j` is affine on `Z_q` with multiplier `a_{ij} ∉ {1, q−1}`* (pairs with `a_{ij} ∈ {±1}` have
identical literal copies and are merged first).  Equivalently: `π_j = π ∘ α_j` for one common permutation
`π` and affine maps `α_j`, with the multipliers of `α_i^{-1}α_j` never `±1` — i.e. the class is exactly
the global relabelings of genuinely affine lists.  With this hypothesis, relabeling by `π_i^{-1}` maps the
pair `(O_i, O_j)` to `(Std, AP_{a_{ij}})`; sizes are relabeling-invariant, so A.1/A.2 give exactly the
per-pair facts the main proof uses, A.3 is circle-agnostic, and the proof closes (T1.a–T1.d).  The
merging clause is also correct precisely under this reading.

## T1.f Computational falsification program (as tasked) — all PASS for the repaired reading

Restriction justification (as required): `G(P)` counts exactly the colorings rejected by every individual
copy but accepted by the union (`hybrid_definitions.md` §3); a union-accepted coloring outside the common
rejects is accepted by some copy and belongs to `I(P)`, not `G(P)`.  So `G(P) = 0` ⟺ no common reject is
union-accepted, and common rejects ⊆ copy-1 rejects.  At `n = 22` my independent scan of all 352,716
words derives `rej1 = 21` and confirms the set **equals the 21 rotations of `1^8 0^5 1^3 0^5`**
(not imported — recomputed from the literal family definition).

| run (my independent literal DP) | total | rej1 | rej2 | common | rescued |
|---|---|---|---|---|---|
| n=22, x↦2x | 352716 | 21 | 21 | 0 | 0 |
| n=22, x↦5x | 352716 | 21 | 21 | 0 | 0 |
| n=22, x↦8x | 352716 | 21 | 21 | 0 | 0 |
| n=22, x↦2x+3 (b≠0) | 352716 | 21 | 21 | 0 | 0 |
| n=22, x↦13x+5 (b≠0) | 352716 | 21 | 21 | 0 | 0 |
| n=28, x↦2x | 20058300 | 40392 | 40392 | **54** | **0** |

* At `n = 22` all multiplier/affine pairs have **empty** common-reject sets, so `G = 0` holds there
  *vacuously*; this vacuity is itself independently verified.  The first non-vacuous test is `n = 28`,
  `a = 2`: **54 common rejects, all union-rejected** (`G = 0` non-vacuously), and the COMMON dump is
  byte-identical to the proposer engine's.
* `b ≠ 0` checks: my program builds both union families and confirms `F(id, x↦ax+b)` is **literally
  identical** (rank-by-rank mask sets) to `F(id, x↦ax)` for `(a,b) ∈ {(2,3), (13,5)}` — verifying the
  proof's "offset `b` is irrelevant" claim at the strongest possible level.
* Lemma A.1 exhaustively verified for `q ∈ {7, 11, 21, 25}`, all invertible `a`, all `s` (T1.a).

## Theorem A verdict

* Lemma A.1: **PASS**.  Lemma A.2: statement **PASS**, proof **REPAIRED** (exact fix in T1.b).
  Lemma A.3: **PASS**.  Main-proof mechanics: **PASS** under the pairwise reduction.
* Hypothesis/statement: **FALSIFIED as written** — explicit counterexamples `(π, ψπ)` at `n = 22` and
  `n = 24` with `G(P) > 0`, verified by two independent implementations.
* Repaired statement (`π_i^{-1}π_j` affine): **proof complete** after the T1.b repair; empirically
  confirmed non-vacuously at `n = 28` (54/0) and vacuously at `n = 22, 24`.

**Overall: UNSOUND AS STATED (counterexample given) — SOUND AFTER REPAIRS, where the repair is to the
statement's hypothesis (composition order), not merely to the proof.**  All downstream uses in the
repository that instantiate `P = (id, mult a)` or affine lists sit inside the repaired class and are
unaffected; any future use of Theorem A for `t ≥ 2` lists *not* containing the identity must check the
precomposition hypothesis.

---

# T2. Theorem E — d-dense circles obstruction

## T2.a Step 1 (hull uniqueness and nestedness) — verdict: PASS

Re-derivation.  Minimal `O*`-hulls of `S ≠ ∅` are complements of largest gaps (any interval ⊇ `S` has its
complement inside a single gap; maximality ⟺ the whole largest gap); `def(S) ≤ d` ⟺ maxgap `≥ q−j−d`.
*Uniqueness:* two disjoint gaps of size `≥ q−j−d` plus the `j` points of `S` give
`2(q−j−d) + j ≤ q` ⟹ `j ≥ q−2d`, contradicting `j ≤ q−2d−1`.  Exactly the document's bound; distinct
maximal gaps are automatically disjoint (separated by points of `S`).  *Nestedness:* `hull(T)^c` is an
interval of size `≥ q−j−1−d` avoiding `S`, hence inside one gap of `S`; if not the largest, the largest
(`≥ q−j−d`) and it (`≥ q−j−1−d`) are distinct gaps, so `(q−j−d) + (q−j−1−d) + j ≤ q` ⟹ `j ≥ q−2d−1`,
excluded since `|T| = j+1 ≤ q−2d−1` gives `j ≤ q−2d−2`.  Degenerate cases: `S` a single point has one gap
(uniqueness trivial; `hull = S`, matching `H₁ = I₁`); `S` an interval (def 0) has one gap; equal-size gap
ties are exactly what the counting kills; the largest use of nestedness is `|T| = j* = q−2d−2 < q−2d−1`,
inside range.  `H_j ⊇ I_j ∋ I₁` gives root containment; `|f(H_j)| ≤ |f(I_j)| + d ≤ 2 + d` since
`|H_j∖I_j| ≤ d`.  The density hypothesis applies to every `I_j` because Lemma 5A.1 guarantees each `I_j`
(all `1 ≤ j ≤ q−1`) is an interval of at least one listed circle.

Machine check (`check_E_step1`): `q ∈ {11, 13}`, `d ∈ {1, 2}`, **all** subsets: uniqueness and nestedness
hold everywhere in the stated ranges; both bounds are **tight** (non-unique largest gaps occur at
`|S| = q−2d`; nestedness fails at `|T| = q−2d`) — so the document's inequalities have no slack and any
weakening would be false.  **PASS.**

## T2.b Step 2 (stepwise refinement) — verdict: PASS

`0 ≤ |H_{j+1}| − |H_j| ≤ (j+1+d) − j = d+1`.  Nested proper cyclic intervals (`|H_{j+1}| ≤ j*+d = q−d−2
< q`) can be grown one endpoint at a time inside `H_{j+1}` ("end-first"; note the parenthetical justifies
only this order — an arbitrary insertion order would be wrong, but end-first is what is prescribed).
Intermediates satisfy `|f(G)| ≤ |f(H_j)| + |G∖H_j| ≤ (2+d) + (d+1) = 3+2d`.  Duplicate hulls
(`H_{j+1} = H_j`) contribute no steps.  Concatenation grows one point per step from `H₁ = I₁` (the plus
root singleton).  **PASS.**

## T2.c Step 3 (top completion) and Step 5 (rooted complements) — verdict: Step 3 PASS, Step 5 REPAIRED (indexing slip)

Step 3: `|H_{j*}| ≥ j* = q−2d−2` leaves `≤ 2d+2` missing points; the complement of a proper cyclic
interval is a nonempty interval whose endpoints are adjacent to the current set, so one-point interval
extensions always exist; sums drift by `±1` per step from `|f(H_{j*})| ≤ 2+d`, giving the bound
`(2+d) + (2d+2) = 3d+4 = k₀ ≥ 3+2d` (the bottom-part bound), so `max_i |f(G_i)| ≤ 3d+4` over the whole
maximal chain; sizes `0..q` are each hit exactly once.  **PASS.**

Step 5 — **REPAIR (one line):** the document writes "the reversed complement sequence
`V_r = G_0^c ⊃ G_1^c ⊃ …`".  `G_0 = ∅`, so `G_0^c = Z_q ∋ r` is *not* a subset of the cut order
`V_r` (which has `N = q−1` points); the correct identity is `V_r = G_1^c` (since `G_1 = {r}`), and the
maximal chain on `V_r` is `∅ = G_q^c ⊂ G_{q-1}^c ⊂ … ⊂ G_1^c = V_r`, sizes `0..N` each once — i.e. simply
drop `G_0` from the complement sequence.  Everything else is correct: every `G_i` (`i ≥ 1`) is a cyclic
interval containing `r`, so `G_i^c` is a cyclic interval avoiding `r` = a linear interval of `V_r`
(including `∅` and the full `V_r`, both in `𝓘_{N,1}` per the verified import);
`f(G_i^c) = f(Z_q) − f(G_i) = 1 − f(G_i)`, so `|f(G_i^c)| ≤ 1 + k₀ = 3d+5 = k`.  The chain is maximal in
exactly FLSY's sense (`C_i ∈ 𝒳`, `|C_i| = i`, `l = N`).  Minor wording note (no repair needed): "we take
`O* = O_1 = id`" — `O*` need not be a listed circle; only "`O* = id` after relabeling" is used.

## T2.d Step 6 (probability) — verdict: PASS

* **Contrapositive reading of FLSY:** Theorem 4.4 ("`𝓘_{N,1}` is not an `(ε,k)`-balanced-chain system for
  `ε > 2^{−cN^{1/5}}`, `k < N^{1/5}`") gives `Pr_f[cbal ≤ k] ≤ 2^{−cN^{1/5}}` for `k < N^{1/5}` and large
  even `N` — exactly the reading verified verbatim in `flsy_reconstruction.md` §1.3/§1.5(ii).  The event
  "∃ `k`-balanced maximal linear-interval chain on `V_r`" is precisely `cbal_{𝓘(N,1)}(f|V_r) ≤ k` and is
  measurable in `f|V_r` alone.
* **Margin:** the theorem needs `k = 3d+5 < N^{1/5}`; the hypothesis `6d+8 < N^{1/5}` implies it with a
  factor-2 margin (`3d+5 < 6d+8` for `d ≥ 0`).  The hypothesis is *stronger than necessary* — a
  presentation choice, not an error.
* **Fiber argument:** uniform normalized `f` (all `C(q, m)` words equally likely): `Pr[f(r) = +1] = m/q`
  exactly; conditioned on it, `f|V_r` is uniform over words with `m−1 = (n−2)/2` pluses on `N = n−2`
  points, i.e. uniformly balanced — the Cycle-4 audited fiber fact (also elementary).
* **Union bound:** accepted ⟹ Lemma 5A.1 chain exists ⟹ its root `r` has `f(r) = +1` (rank-2 forcing,
  part of 5A.1) and Steps 1–5 build the `k`-chain on `V_r` — Steps 1–5 need only `q ≥ 2d+3`, no
  asymptotics, so "every accepted `f` has some root with the constructed chain" is airtight.  Hence
  `H(P) ≤ Σ_r (m/q)·2^{−cN^{1/5}} = m·2^{−cN^{1/5}} = (n/2)·2^{−c(n−2)^{1/5}}`.  Uniformity in `t` is
  genuine: only the density of the accepting chain's own states is used.  **PASS.**

## T2.e Section 2 (pairswap 2-density) — verdict: PASS

Independent re-derivation of the end-substitution structure.  Blocks are `{2k, 2k+1}` plus the fixed
singleton `{q−1}` (note `q−1` is even for odd `q`).  For a position interval with left end `i`, right end
`j` (wrap-around included — the wrap point sits between interior positions and creates no partial block):
`i` odd ⟹ substitute point `i → i−1` (block `{i−1, i}` half-covered); `i` even ⟹ no substitution
(including `i = q−1`, the fixed point); `j` even and `j ≠ q−1` ⟹ substitute `j → j+1`; `j` odd or
`j = q−1` ⟹ none.  So `S` = interval with `≤ 1` one-point end substitution per end; its complement is the
outer gap plus `≤ 2` singleton holes, hence `def(S) = q − maxgap − |S| ≤ #holes ≤ 2` whenever the outer
gap is nonempty, and `def ≤ #holes − 1 ≤ 1` in the corner where the outer gap vanishes (`|S| + holes =
q`); lengths `1` and `q−1` give honest intervals (`def = 0`).  Machine check (`check_E_pairswap`):
`q ∈ {13, 21, 29, 37}`, **all** position intervals: `def ≤ 2` everywhere, bound attained at every `q`.
**PASS** (both parities of both ends, the fixed point, wraps, and extreme lengths all covered).

## T2.f Pipeline falsification (most important) — verdict: PASS (no bookkeeping failure found)

My own end-to-end scan (independent literal induced-DAG DP, validated as described above) of the
`(id, pairswap)` union:

| n | total words | rej1 | rej2 | common | rescued | max over rescued of min-k | bound 3d+4 (d=2) |
|---|---|---|---|---|---|---|---|
| 22 | 352716 | 21 | 21 | **0** | 0 | — (vacuous) | 10 |
| 24 | 1352078 | 414 | 414 | 14 | 12 | **2** | 10 |
| 26 (bonus) | 5200300 | 4700 | 4700 | 360 | 316 | **2** | 10 |

* At `n = 22` there are **no** colorings rejected by both copies (hence none rescued): the tasked check is
  vacuous there, and the vacuity itself is independently established (and matches the proposer's engine:
  both dumps empty).
* At `n = 24` and `n = 26`, **every** rescued coloring was checked by a minimax DP (min over plus roots
  `r` of the min over maximal rooted cyclic-interval chains `{r} = G₁ ⊂ … ⊂ G_q = Z_q` of
  `max_i |f(G_i)|`; DP verified against an independent memoized recursion at `q = 9`): the worst value over
  all 12 + 316 rescued colorings is **2**, far inside the theorem's `3d+4 = 10`.  No rescued coloring
  needs `k > 10`; Steps 1–3's bookkeeping survives an exhaustive finite-`n` attack (consistent with the
  proposer's n=28 spot value min-k = 2).
* Flags cross-checked: my COMMON dumps (word + union-accept flag, all computed by my own DP) are
  **byte-identical** to `cycle05_union_scan.exe` dumps (`CYCLE05_DUMP_COMMON=1`) at `n = 24` (14 lines),
  `n = 26` (360 lines), and `n = 28` mult-2 (54 lines) — i.e. I re-verified *all* flags, not a sample.

## Theorem E verdict

Step 1 **PASS**, Step 2 **PASS**, Step 3 **PASS**, Step 4 **PASS** (margin noted), Step 5 **REPAIRED**
(`G_0^c → G_1^c` indexing slip; fix supplied, one line, no downstream effect), Step 6 **PASS**, §2
**PASS**, pipeline **PASS** (exhaustive at n = 22, 24 plus bonus 26; zero violations).

**Overall: SOUND AFTER REPAIRS** — the single repair is cosmetic (chain indexing in Step 5); no
mathematical gap was found, the hull lemma's inequalities are exactly tight (so the constants are not
accidental), and the structural conclusion survives exhaustive falsification at every reachable `n`.
The theorem's probability bound is asymptotic (`6d+8 < (n−2)^{1/5}`), as the document itself flags; the
finite-`n` checks here test the unconditional Steps 1–5, which is everything except the verified FLSY
import.

---

# Files produced by this audit

* `experiments/cycle05_audit_thm_lemmas.py` — lemma-level direct set computations (A.1 formula/statement,
  A.2 both directions all sizes, A.3 local + end-to-end, merge-clause composition probe, the
  common-middle-interval demonstration of the composition bug, Theorem E Step 1 exhaustive + tightness,
  pairswap defect).
* `experiments/cycle05_audit_thm_pipeline.cpp` / `.exe` — independent literal induced-DAG DP; `--selftest`
  (family counts, DFS cross-check, minimax vs reference recursion), `--scan` (exhaustive counts, COMMON
  dumps, n=22 rotation check, b-irrelevance family comparison, Theorem-E minimax), `--conj` (Theorem A
  literal-hypothesis falsification search with full in-program re-verification).
* `experiments/cycle05_audit_thm_diffsmall.py` — differential vs proposer `brute_accepts` at n = 10, 12.
* `experiments/cycle05_audit_thm_a_counterexample.py` — standalone counterexample verification via the
  proposer's own reference (cases 0: n=24, 1: n=22).
* `audits/audit_common_n{22,24,26}_pairswap.txt`, `audits/audit_common_n28_mult2.txt` — my COMMON dumps;
  `audits/proposer_common_*.txt` — proposer-engine dumps; `audits/{m,p}2{4,6,8}.sorted` — diffed copies
  (all diffs empty).

# Summary of verdicts

| Item | Verdict |
|---|---|
| T1.a Lemma A.1 | PASS |
| T1.b Lemma A.2 | statement PASS; proof REPAIRED (interior-case numerics; fix supplied) |
| T1.c Lemma A.3 | PASS |
| T1.d main-proof mechanics + merging | PASS (under precomposition reading only) |
| T1 hypothesis as stated | **FALSIFIED** (explicit counterexamples n=22, n=24; two independent verifiers) |
| T1.e computational program | PASS (incl. non-vacuous n=28: 54 commons, 0 rescued; b-irrelevance literal) |
| **Theorem A overall** | **UNSOUND AS STATED; SOUND AFTER REPAIRS** (hypothesis `π_j∘π_i^{-1}` → `π_i^{-1}∘π_j`, plus A.2 write-up fix) |
| T2.a Step 1 | PASS (tightness confirmed) |
| T2.b Step 2 | PASS |
| T2.c Steps 3/5 | Step 3 PASS; Step 5 REPAIRED (G_0^c → G_1^c; fix supplied) |
| T2.d Step 6 | PASS |
| T2.e §2 pairswap density | PASS |
| T2.f pipeline | PASS (exhaustive n=22, 24 + bonus 26; max min-k = 2 ≤ 10; all flags re-verified) |
| **Theorem E overall** | **SOUND AFTER REPAIRS** (single cosmetic repair) |

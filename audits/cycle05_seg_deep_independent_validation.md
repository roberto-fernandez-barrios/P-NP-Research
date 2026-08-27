# Deep independent validation of Lemma SEG (standalone hostile investigation)

**Role:** standalone hostile mathematical investigator.  This is NOT Research
Cycle 6 and continues no O01 research.  SEG was treated as FALSE until proved.
**Date:** 2026-08-22.
**Target:** the true mathematical status of Lemma SEG (segment interval
anti-concentration), an unpublished repository reconstruction on which
Theorems C and F of `research_cycle_05/switch_structure_theory.md` depend.
**Original branch audited:** `cycle05-fable` at `bd12e5c`.
**Correction note (2026-08-27):** the later independent Sol cross-model
validation found that the original R3 discussion was incomplete and that the
arms-length R4 argument was false.  The exact conclusion-preserving repairs
from `audits/cycle05_sol_final_cross_model_validation.md` §§5.4--5.8 are now
incorporated below.  This report therefore records the corrected proof, not
the superseded derivations.

## Verdict

```text
SEG-SOUND-WITH-REPAIRS
```

**The frozen statement is unchanged**, but its proof needs R1--R5.  SEG is
not published verbatim by FLSY: the paper supplies the random-walk machinery,
while the fixed-segment grid, nonzero-offset lemma, exact rounding, and full
cyclic endpoint reduction are new repository derivations.  Section D now
proves those obligations with explicit constants.  After the deep audit,
arms-length referee, and final independent cross-model correction, the
appropriate status is **ADVERSARIALLY REVIEWED PROOF CANDIDATE;
UNFORMALIZED**.

Consequences for Theorems C and F are stated in §H, within the limits the
mandate imposes.

---

## A. Method and independence discipline

Order of operations (mandate-compliant):

1. Read the corrected Cycle-5 state (`RESEARCH_STATE.md`,
   `audits/cycle05_fable_independent_validation.md`) and extracted only the
   *statements* of SEG, Theorem C, Theorem F.
2. Fetched the primary source myself: ECCC TR26-001 (Fabris, Limaye,
   Srinivasan, Yehudayoff), 42 pp., from
   `https://eccc.weizmann.ac.il/report/2026/001/download`; verified no
   revisions are listed on the report page; confirmed by my own full-text
   scan that no segment/localized statement exists anywhere in the paper
   ("segment" occurs only inside Lemma 4.7's proof, for walk blocks); spot
   confirmed the published version (LIPIcs 383 Art. 22) metadata and that
   its abstract/keywords carry no segment variant.
3. Reconstructed all of §4 (Definition 4.1, Lemmas 4.2, 4.3, 4.5, 4.6, 4.7,
   Theorem 4.4, pp. 18–25) from the paper, line by line, including the exact
   first-passage law and every constant (§B).
4. Formed my own segment theorem and complete proof (§D) **before** reading
   the repository's proof materials.
5. Built an independent implementation from the definitions only
   (`audits/independent_validation/seg_deep/`: `seg_engine.cpp`,
   `seg_bruteforce_chains.py`, `seg_battery.py`) — no code, constants, or
   seeds reused from `experiments/cycle05_audit_seg_mc.py`, from
   `audits/independent_validation/my_seg_mc.py`, or from any repository
   engine (neither file was opened at any point) — and ran an aggressive
   counterexample hunt (§F).
6. Only then read `research_cycle_05/flsy_reconstruction.md` §§2–3 and
   `audits/cycle05_seg_lemma_adversarial.md` and compared (§G).

---

## B. The FLSY machinery, reconstructed from the primary source

Definitions (verified verbatim): a *partition* is `f: [n] → {±1}`;
`f(S) := Σ_{x∈S} f(x)`; `𝓘 = 𝓘_{n,1}` is the set of intervals of the LINEAR
order `[n]` (Definition 2.1 with `m = 1`; `∅` is the empty union, `l = 0`);
`cbal_𝓘(f) = min_{maximal chains C ⊆ 𝓘} max_{i∈[n]} |f(C_i)|`
(Definition 1.2); `(ε,k)`-balanced-chain means
`Pr_f[cbal ≤ k] ≥ ε` for uniform balanced `f` (Definition 1.4).

**Theorem 4.4 (= 1.7 = published 23).**  Universal `c > 0`: for every
sufficiently large even `n`, `𝓘_{n,1}` is not `(ε,k)`-balanced-chain for
`ε > 2^{−cn^{1/5}}` and `k < n^{1/5}`.

Proof architecture (all re-derived; page references to the ECCC version):

* **Lemma 4.2 (reduction, pp. 18–21).**  A maximal chain grows from
  `C_1 = {s}` one endpoint at a time; with `e` the last element added
  (necessarily `e ∈ {1, n}`), the cyclic bookkeeping `P = [s,e] ∋ s+1`,
  `N = [n]∖P` splits each chain element as `S_+(m) ∪ S_−(m)`, giving two
  *growth walks* `X(i) = f([s, s+i−1])` (length `l = |P|`),
  `Y(j) = −f([s−j, s−1])` (length `r = n−l`), reads of DISJOINT coordinate
  sets, with `f(C_t) = X(α(t)) − Y(β(t))` for the staircase `(α, β) =
  (|S_+|, |S_−|)`.  The chain event implies `d_F(X,Y) ≤ k` in the discrete
  Fréchet distance of Definition 4.1.  Union over `(s,e) ∈ [n]²` and the
  pointwise unconditioning `Pr_f[E] ≤ Pr_g[E]/Pr_g[bal] = O(√n)·Pr_g[E]`
  give `Pr_f[cbal ≤ k] ≤ O(n^{5/2}) max_l Pr_W[d_F(X_l, Y_{n−l}) ≤ k]`.
* **Lemma 4.3 (Fréchet anti-concentration, pp. 24–25).**  For independent
  fresh walks of lengths `l + r = n`, `ε ∈ (0,1/4)`,
  `d := n^{1/4−ε} ≥ (2/3)ln n`:
  `Pr[d_F < d] ≤ exp(−c₁ min{n^{1/4−ε}, n^{4ε}})`.  Proof: milestones with
  gaps `Δ = 3d` on the longer walk (Lemma 4.7: `≥ n/(2c₃Δ³)` of them, else
  probability `exp(−Ω(Δ))`); if `d_F < d` the shorter walk must visit the
  `d`-neighborhoods of all milestones in order.  At the nominal
  paper level the leg distance is written `Δ−2d=d`.  This does
  **not** define a real-indexed `F_d` in the corrected SEG proof:
  §D rounds the milestone/tracking gap and dominates the integer variable
  `F_δ` with `δ=⌈d⌉`.  The sum's lower tail
  (Lemma 4.6, powered by the first-passage law, Lemma 4.5) is
  `exp(−Ω(n/d⁴))`.  Balancing `d = n/d⁴` yields `ε = 1/20`, exponent
  `n^{1/5}`.
* **Lemma 4.5 (pp. 21–22).**  `Pr[F_δ ≥ z] = Θ(δ/√z)` for `Ω(δ²) ≤ z ≤ n/2`,
  from the hitting-time law `Pr[F_δ = y] = (δ/y)2^{−y}·binom(y, (y+δ)/2)`.
* **Lemma 4.6 (pp. 22–23).**  `Pr[Σ_{i≤k} F^{(i)}_δ ≤ n] ≤ exp(−Ω((kδ)²/n))`
  for `kδ² ≤ c₄n`, `(kδ)² = ω(n)`; via Chernoff on the counting process
  `C_t = #{i: F^{(i)} ≥ t}` at `t = (2n/(ckδ))²`.
* **Lemma 4.7 (pp. 23–24).**  For `Δ ≥ 2 log n`, a walk of length `n` has a
  `(g,Δ)`-milestone sequence of length `n/(c₃Δ³)` except with probability
  `exp(−Ω(Δ))`; via the two-sided passage `D_Δ` and a `Δ`-block split, each
  block escaping `[−2Δ, 2Δ]` with probability `≥ 1/2` by Lemma 4.5.

**Paper-level slops found in my own pass** (all presentational; none affects
truth; found before reading the repository's audits, which record the same
five): (i) the p. 25 extraction claim ("for every strictly increasing
`(a_i)` there is a strictly increasing `(b_i)`") is false as universally
quantified and true for `Δ`-separated milestones (`Δ = 3d > 2d` forces
`b_i` strictly increasing); (ii) Lemma 4.5's stated range `z ≤ n/2` is
violated by its own use in Lemma 4.7 (`z =` block length) — repaired by
stating 4.5 for the infinite walk (the event `{F_δ ≥ z}` is
prefix-measurable); (iii) Definition 4.1 takes `l, r ∈ [n]` but Lemma 4.2's
`max_{r∈[n]}` needs the degenerate `r = 0` (tube) case; (iv) `log` vs `ln`
in 4.7's hypothesis (constants only; `ln` is the reading under which its
final display closes); (v) `≤` vs `<` at the threshold in Theorem 4.4's
proof (integer `d_F`; or perturb `ε`).  Two further presentational nits my
pass adds: Lemma 4.2's walk-normalization sentence carries an off-by-one
(`X(i) = f([s, s+i])` vs the `i`-point interval; the injection is stated
correctly), and Definition 1.2 requires `∅ ∈ 𝒳` for maximal chains to
exist, which Definition 2.1 supplies as the empty union.

**The load-bearing structural facts for localization** (my own census,
verified line by line):

1. The chain anchor (`C_0 = ∅`, walks starting at value 0) enters ONLY in
   Lemma 4.2's bookkeeping (choice of `(s,e)`; both walks normalized to 0;
   `O(√n)` unconditioning) and in the milestone base case `z₀ := 0`,
   `Y(0) = 0` of Lemma 4.3's proof (via 4.7's `x₀ := 0`).
2. Lemmas 4.5, 4.6, 4.7 are stated and proved for ARBITRARY walk lengths.
   There is nothing global-`n` in the walk layer; localization has nothing
   to modify there.
3. Everything downstream of the milestones is translation invariant: the
   `(g,Δ)`-sequence condition constrains increments only; the p. 25
   domination chain invokes "translation invariance of random walks"
   explicitly and uses only consecutive gaps `|z_i − z_{i−1}| ≥ Δ` plus the
   invariant `|Y(T_{…z_{i−1}}) − z_{i−1}| ≤ d`.

---

## C. The SEG statement under investigation (endorsed form, quoted)

There exist universal `c > 0, C > 0, L₀` such that for every `N` and every
`σ ∈ ℤ` with `|σ| ≤ 1` and `σ≡N (mod 2)`, for `f` uniform on
`{g: [N] → {±1}, g([N]) = σ}`,
fixed intervals `∅ ≠ A ⊆ B ⊆ [N]` with `L := |B∖A| ≥ L₀`, and integer
`1 ≤ k < L^{1/5}`:

```text
Pr_f[ ∃ chain A = D_0 ⊂ D_1 ⊂ … ⊂ D_L = B, each D_i an interval of [N],
      with |f(D_i)| ≤ k for all 0 ≤ i ≤ L ]  ≤  C·√N·exp(−c·L^{1/5}),
```

with the variants: (i) uniform `g` on `{±1}^{[N]}`: no `√N` factor;
(ii) "some `B ⊇ A` with `|B∖A| = L`": extra factor `(L+1)`; (iii) cyclic
order `Z_N`, `B ≠ Z_N`: verbatim; `B = Z_N`: extra factor `(L+1)`;
(iv) relative form `|f(D_i) − f(A)| ≤ k`: offset 0.

The corrected proof permits the explicit witnesses
`c=min{1/2,(1/6)²/(8·27648²)}`, `C=6`, and
`L₀=⌈13824^{5/2}⌉=22,469,029,418`.  There is no separate
large-`N` hypothesis.

## D. Theorem S: complete statement and proof

This section is a self-contained proof of the endorsed form.  Constants are
explicit but deliberately unoptimized (FLSY's own are unspecified `Ω`s);
what matters is that every constant is absolute — no hidden dependence on
`N`, on positions, or on the split.

**Notation.**  A *walk of length `ℓ`* is `W: {0,…,ℓ} → ℤ` with
`W(t) − W(t−1) ∈ {±1}`; *fresh* means increments i.i.d. uniform.  `F_δ`
(`δ ≥ 1`) is the one-sided first passage of a fresh infinite walk from 0 to
`+δ` (a.s. finite).  `d_F` is Definition 4.1 verbatim, extended to
`l, r ∈ {0,…,n}` (slop (iii) repaired: for `r = 0`, `β ≡ 0` is forced).
Definition 4.1 never requires `X(0) = Y(0)`; it is well-posed for offset
walks.

### D.0 Lemma W1 (first-passage law at a real threshold)

For integers `a ≥ 1`, `y ≥ 1`,
`Pr[F_a = y] = (a/y)·2^{−y}·binom(y,(y+a)/2)` when
`y ≡ a (mod 2)`, and the probability is zero otherwise.  More
importantly for the rounding used below, for every **real** `t ≥ 4a²`,

```text
a/(6√t) ≤ Pr[F_a ≥ t] ≤ 1.85a/√t.                         (W1)
```

*Proof of the real-threshold form.*  Put `u = ⌈t⌉−1`.  Since
`F_a` is integer-valued, reflection gives

```text
Pr[F_a ≥ t] = Pr[F_a > u]
            = Σ_{x∈[-a,a), x≡u (mod 2)} Pr[W_u=x].
```

The sum contains exactly `a` parity-compatible masses.  The central
binomial mode is at least `1/(2√u)`.  For a relevant mass write
`j=(|x|−ε)/2`, where `ε∈{0,1}` is the central parity.
Its ratio to a central mode is a product of adjacent ratios.  If
`u=2m`, the factors are
`(m−s+1)/(m+s)=1−(2s−1)/(m+s)`; if
`u=2m+1`, they are
`(m−s+1)/(m+s+1)=1−2s/(m+s+1)`.  Here
`u≥4a²−1` and `|x|≤a`, so the sum of the factor losses
is at most `1/8` in either parity.  The inequality
`∏(1−v_s)≥1−Σv_s` therefore gives ratio at least
`7/8`.  Hence the sum is at least
`7a/(16√u) ≥ a/(6√t)`.  Conversely every summand is at most the
mode, the standard mode bound is at most `1/√u`, and
`u ≥ 3t/4` because `t ≥ 4`; this is already less than
`1.85a/√t`.  These analytic inequalities, not the finite
measurements below, fix the constants.

*Independent check only:* exact DP (`seg_engine.exe fp`) agrees with the
hitting-time formula and gives much larger empirical slack; no measured
margin is used in (W1).

### D.1 Lemma W2 (rounded milestones)

Let `g` be a fresh walk of integer length `ℓ`, let real
`Δ ≥ max(3,2 ln ℓ)`, set `c₃=256`, and
`K=⌊ℓ/(c₃Δ³)⌋`.  A milestone exit is taken at the integer level
`a_Δ=⌈Δ⌉`.  Then, except with probability
`e^{−Δ/6}`, there are `K` successive milestone times
whose consecutive value gaps are at least `a_Δ≥Δ`.

*Proof.*  Put `b=⌊256Δ²⌋`.  Inside the first
`⌊256Δ³⌋` steps take `⌊Δ⌋` disjoint blocks of
length `b`; they fit because
`⌊Δ⌋b≤256Δ³`.  If the walk never exits
distance `a_Δ` from the starting value, every block increment
walk misses the level `⌈2Δ⌉`.  By (W1),

```text
Pr[F_{⌈2Δ⌉} > b] ≤ Pr[F_{⌈2Δ⌉} ≥ b]
                 ≤ 1.85⌈2Δ⌉/√b < 0.30                 (Δ≥2);
```

indeed, `⌈2Δ⌉≤(5/2)Δ` and
`b≥(256−1/4)Δ²` for `Δ≥2`.  These inequalities imply
both `b≥4⌈2Δ⌉²` and
`1.85⌈2Δ⌉/√b<0.30`.  Blocks have disjoint increments.
Moreover `⌊Δ⌋/Δ≥3/4` for `Δ≥3`, and
`(3/4)ln(10/3)>ln 2`, proving
`0.30^{⌊Δ⌋}≤2^{−Δ}`.  Thus a two-sided
milestone passage takes more than `256Δ³` steps with probability
at most `2^{−Δ}`.

Successive passage durations are i.i.d. by strong Markov.  If each of the
first `K` durations is at most `ℓ/K`, their sum is at
most `ℓ`; and `ℓ/K≥256Δ³`.  Therefore

```text
Pr[fewer than K milestones]
 ≤ K2^{−Δ} ≤ ℓ2^{−Δ}
 ≤ exp(−Δ(ln 2−1/2)) ≤ exp(−Δ/6),
```

using `Δ≥2 ln ℓ`.  This is the real-`Δ` version needed
by S3.

### D.2 Lemma W3 (sum lower tail at a real threshold)

Let `F^{(1)},…,F^{(K)}` be i.i.d. copies of `F_a` for
an integer `a≥1`, and let real `T≥1` satisfy
`Ka²≤T`.  With `c_lo=1/6`,

```text
Pr[Σ_{i≤K}F^{(i)}≤T]
 ≤ exp(−c_lo²(Ka)²/(16T)).                              (W3)
```

*Proof.*  Set the real threshold
`t*=(2T/(c_lo K a))²`.  The hypothesis gives
`t*≥4a²`, so the real form of (W1) gives
`p=Pr[F_a≥t*]≥c_lo a/√t*=:p₀=c_lo²Ka²/(2T)`;
also `p₀≤c_lo²/2≤1`.
If the sum is at most `T`, at most
`T/t*=Kp₀/2` variables can be at least `t*`.
Monotone coupling with `Bin(K,p₀)` and the Chernoff lower tail
give
`Pr[ΣF^{(i)}≤T]≤exp(−Kp₀/8)`, which is (W3).  No ceiling loss or
empirical constant enters.

### D.3 Lemma S3 (offset Fréchet anti-concentration)

Let

```text
c₁ = min{1/2,(1/6)²/(8·27648²)}
   = 4.542344518777...·10^{−12},
L₀' = ⌈13824^{5/2}⌉ = 22,469,029,418.
```

For `L≥L₀'`, every split `m+p=L`, and every integer
offset `σ'` with `|σ'|≤d:=L^{1/5}`, let `X,Y`
be independent fresh walks of lengths `m,p` starting at
`σ',0`.  Then

```text
Pr[d_F(X,Y)<d] ≤ 2exp(−c₁L^{1/5}).                       (S3)
```

*Proof.*  Put real `Δ=3d`, integer tracking radius
`r=⌊d⌋`, and integer first-passage level `δ=⌈d⌉`.
By symmetry let the longer walk `M`, of length
`ℓ≥L/2`, supply milestones, and let `H`, of length
`r'≤L/2`, chase them.  Write `z₀=M(0)` and
`h₀=H(0)`, so `|z₀−h₀|=|σ'|≤d`.

Apply W2 to `M−z₀`.  At `L₀'`,
`d²=L^{2/5}≥13824`, `3d≥2 ln L≥2 ln ℓ`, and
`K=⌊ℓ/(256Δ³)⌋≥1`; the logarithmic inequality holds at
`L₀'` and remains monotone thereafter.  Except with probability
`e^{−Δ/6}≤e^{−d/2}`, obtain `K` milestones
`z_i=M(x_i)` with integer gaps at least `⌈3d⌉`.

Suppose `d_F(M,H)<d` and fix a witnessing staircase.  All walk
values are integral, so its pointwise discrepancies are at most
`r=⌊d⌋`.  At the first milestone,

```text
|z₁−h₀| ≥ ⌈3d⌉−|σ'| ≥ 2d>d.                              (R1)
```

Thus the first extracted chaser time `b₁` is at least one.  The
minimal staircase preimages of successive milestone times give
`b₁<⋯<b_K≤r'`; equality of two consecutive `b_i` would
put two milestones within `2r<⌈3d⌉`.  Define `τ₀=0` and
let `τ_i` be the first time after `τ_{i−1}` that
`H` enters the radius-`r` ball around `z_i`.
R1 gives `τ₁≤b₁`, and every later leg has the same invariant by
the definition of `τ_{i−1}`.  Moreover

```text
⌈3d⌉−2⌊d⌋ ≥ ⌈d⌉=δ.                                      (R3)
```

Hence each leg dominates first passage through the integer distance
`δ`.  The target direction is measurable at the preceding
stopping time; reflection and strong Markov make the resulting variables
i.i.d. copies of `F_δ`.  Consequently

```text
Pr[d_F<d | M] ≤ Pr[Σ_{i≤K}F_δ^{(i)}≤L/2].
```

(If `r'=0`, R1 contradicts `b₁≤0`, so the event is
empty whenever the milestone event holds.)

It remains to check W3 exactly.  The upper estimate
`K≤L/(6912d³)` and `δ≤2d` give

```text
Kδ²≤L/(1728d)≤L/2.
```

For the lower estimate put `x=d²/13824`.  Since
`K≥⌊x⌋`, there are exactly two cases:

* if `13824≤d²<27648`, then `K≥1` and
  `Kd≥d≥d³/27648`;
* if `d²≥27648`, then `x≥2` and
  `K≥⌊x⌋≥x/2`, again giving `Kd≥d³/27648`.

Thus no interval is omitted, `Kδ≥Kd`, and

```text
(Kδ)²/(16(L/2)) ≥ (Kd)²/(8L)
                 ≥ L^{1/5}/(8·27648²).                  (R2)
```

W3 now gives the second failure probability
`exp(−(1/6)²d/(8·27648²))`.  Adding the milestone failure yields
(S3) with the displayed exact `c₁`.  This proves all rounding and
the noninteger Chernoff threshold analytically; simulation is not part of
the constant argument.  ∎

### D.4 Lemma S1 (grid normal form)

Linear case: let `A = [a₁, a₂] ⊆ B = [b₁, b₂] ⊆ [N]`, `p := a₁ − b₁`,
`m := b₂ − a₂`, `L = p + m`.  The intervals `D` with `A ⊆ D ⊆ B` are
exactly `D_{j,i} := [a₁−j, a₂+i]`, `0 ≤ j ≤ p`, `0 ≤ i ≤ m`; the
`(A,B)`-segment chains are exactly the monotone unit-step lattice paths
`(0,0) → (p,m)`; and `f(D_{j,i}) = f(A) + λ(j) + ρ(i)` where
`λ(j) := f([a₁−j, a₁−1])`, `ρ(i) := f([a₂+1, a₂+i])` are partial-sum reads
of the two DISJOINT arcs of `B∖A`.  (Trivial verification; an interval
containing `[a₁,a₂]` inside `[b₁,b₂]` is `[x,y]` with
`b₁ ≤ x ≤ a₁ ≤ a₂ ≤ y ≤ b₂`.)

Cyclic case, `B ≠ Z_N`: pick any `c ∈ Z_N ∖ B`.  Every cyclic interval `D`
with `A ⊆ D ⊆ B` is an arc inside the arc `B`, hence avoids `c`, hence is a
linear interval of the cut order starting at `c+1`; the cut is a
measure-preserving relabeling (the measure `f([N]) = σ` is exchangeable),
and the linear normal form applies verbatim.  For the cyclic case
`B=Z_N`, `A≠∅`, fix a terminal split
`u+v=L−1`, where `L=N−|A|`.  The proper states use
`u` points from the left extension arc and `v` from the
right; one point is added only in the terminal step.  Append that last point
to the end of the left extension sequence.  The two coordinate sequences
remain disjoint and now have total length `(u+1)+v=L`.  The actual
cyclic chain is a staircase on this length-`L` grid which postpones
the appended left step to its endpoint.  There are `L` terminal
splits, so a union bound costs at most `L+1`.  This length-`L`
encoding is essential: the formerly proposed length-`L−1` reduction
is false when `L=j⁵+1` and `k=j`.

*Machine validation (this audit's own):* literal DFS enumeration of nested
interval chains (never told about the grid or any cut) vs. an independent
lattice DP: linear `N = 11`, all 2,048 colorings × 300 configurations =
614,400 checks, 0 mismatches; native cyclic (extensions wrap mod `N`) vs.
cut-and-grid: 512,000 checks, 0 mismatches (`seg_bruteforce_chains.py`);
second, independent C++ pair (BFS over cyclic interval states vs. bitmask
grid DP): full enumeration at `N = 16, σ = 0` (926,640 checks) and
`N = 17, σ = 1` (1,750,320 checks), 0 mismatches (`seg_engine.exe cyc`).

### D.5 Lemma S2 (unconditioning)

For `|σ| ≤ 1` with `σ ≡ N (mod 2)`:
`Pr_g[g([N]) = σ] = binom(N, (N+σ)/2)·2^{−N} ≥ 1/(3√N)` for all `N ≥ 1`
(central binomial bound `binom(2m,m)4^{−m} ≥ 1/(2√m)` and its odd-`N`
analogue).  Hence for EVERY event `E`:
`Pr_{f | f([N])=σ}[E] ≤ Pr_g[E] / Pr_g[g([N]) = σ] ≤ 3√N·Pr_g[E]`.
This is a pointwise counting inequality; no independence or correlation
structure is used, and it prices the GLOBAL conditioning, which is why the
factor is `√N`, not `√L`.  (If `σ ≢ N (mod 2)` the conditioned measure does
not exist and the SEG statement is read as vacuous — a hygiene note, not a
defect; the applications have matching parity.)

### D.6 Theorem S (= endorsed SEG) and proof

**Theorem S.**  With `c:=c₁` from S3, `C:=6`, and
`L₀:=L₀'=22,469,029,418`: for
every `N`, every `σ` with `|σ| ≤ 1` (and `σ ≡ N mod 2`), `f` uniform on
`{g([N]) = σ}`, fixed intervals `∅ ≠ A ⊆ B ⊆ [N]` with `L = |B∖A| ≥ L₀`,
and `1 ≤ k < L^{1/5}`:

```text
Pr_f[∃ (A,B)-segment chain with all |f(D_i)| ≤ k]  ≤  6·√N·exp(−c·L^{1/5}),
```

together with variants (i)–(iv) of §C.

*Proof.*  By S1 the event equals: `|f(A)| ≤ k` and some lattice path
`(0,0) → (p,m)` has `|f(A) + λ(j) + ρ(i)| ≤ k` at every visited cell.
Setting `X(i) := f(A) + ρ(i)` (length `m`, start `f(A)`) and
`Y(j) := −λ(j)` (length `p`, start 0), the path is a staircase of
Definition 4.1 achieving `max_t |X(α(t)) − Y(β(t))| ≤ k`, i.e.
`d_F(X, Y) ≤ k < L^{1/5} = d` (the `t = 0` constraint `|f(A)| ≤ k` is an
extra conjunct, used only to bound the offset).  Under uniform `g` the
triple `(g(A), ρ-increments, λ-increments)` is mutually independent
(disjoint coordinate sets), so conditioning on `g(A) = σ'`:

```text
Pr_g[event] ≤ Σ_{|σ'| ≤ k} Pr[g(A) = σ']·Pr[d_F(X^{σ'}, Y) < d]
            ≤ max_{|σ'| ≤ k} Pr[d_F(X^{σ'}, Y) < d] ≤ 2·e^{−c₁L^{1/5}}
```

by S3 (`|σ'| ≤ k < d`).  This is variant (i).  The main form follows by
S2 (`×3√N`).  Variant (ii): `B` with `|B∖A| = L` is determined by its split
`(p, m)`, `p + m = L` — at most `L+1` choices (fewer if `[N]` truncates);
union bound.  Variant (iii): S1's cut for `B ≠ Z_N`; for
`B=Z_N`, S1's terminal-split union is over `L` grid
events whose two walk lengths sum to `L`.  Apply S3 before this
`L`-way union; the original strict hypothesis
`k<L^{1/5}` and all constants are unchanged.  Variant
(iv): the same grid with `V(j,i) := λ(j) + ρ(i)` and offset 0 — S3 with
`σ' = 0`, no `|f(A)| ≤ k` conjunct needed.  ∎

**Dependency list (exhaustive).**  Hitting-time theorem for simple walks
(classical; machine-verified exactly); reflection identity; Stirling
point-mass bounds; Chernoff's lower tail for binomials; strong Markov
property; FLSY's proof pattern of Lemmas 4.6/4.7 and §4.4 (re-derived in
full above — no step of the paper is used as a black box); and the endorsed
statement's own hypotheses.  The segment grid, offset lemma, rounded
thresholds, and cyclic-full encoding are repository lemmas proved here, not
claims published verbatim by FLSY.  No unpublished external source is used.

---

## E. Mandated uniformity and usage audit

| Quantity | Where it enters | Uniform? |
|---|---|---|
| Segment starting point (position of `A`) | Nowhere: S1 reads `f` only on `B`; the measure is exchangeable | YES — exactly (machine: identical exact counts at `a₁ ∈ {0,4,13}`, `N = 14`; translation/reflection exact in all scans) |
| Segment length `L` | Sole decay parameter via S3 (`d = L^{1/5}`, milestones `K = Θ(L/d³)`) | YES — `c₁, L₀'` absolute |
| Endpoint values | `f(A)` = the offset, bounded by `k < d` ON the event; `f(B)` constrained by the event itself, unused by the proof | YES — offset enters only the base case of the S3 invariant |
| Conditioning / history | Only the global `f([N]) = σ`, removed pointwise at `3√N` (S2).  Applications (C/F) use SEG through union bounds over DETERMINISTIC `(o, A, B)`; no conditioning on chain history ever occurs | YES |
| Translation | Walk lemmas W1–W3 are statements about fresh increments; S3's milestone condition constrains increments only; explicit in the p. 25 "translation invariance" step | YES |
| Parity | `σ ≡ N (mod 2)` needed for the measure to exist (hygiene note); `k ≥ 1` because `k = 0` is parity-impossible for `L ≥ 1`; W1's law lives on `y ≡ δ (mod 2)`; nothing else | YES (with the vacuity reading for mismatched `σ`) |
| Split `(p, m)` | S3 is proved for every split, `max(m,p) ≥ L/2` carries milestones; `p·m = 0` degenerate case strictly easier (tube) | YES — verified extremal split is balanced (scan + walk battery) |

**Where first-passage estimates are used (mandate item 5), exhaustively:**
(1) W1 lower bound → W3 (the chaser's leg-sum lower tail — the exponential
engine); (2) W1 upper bound → W2 (each `c₃Δ²`-block escapes `[−2Δ,2Δ]`
with probability ≥ 1/2 — milestone supply); (3) the domination step of S3
(each chaser leg ⪰ fresh `F_⌈d⌉` via strong Markov).  All three are
statements about fresh walks of length ≤ `L`; localization does not touch
them.

**What localization changes (mandate item 6):** only a polynomial factor —
`O(n^{5/2})` (= `n²` for `(s,e)` × `√n` unconditioning) becomes `3√N` (no
`(s,e)` enumeration at all; `(L+1)` only for the union-over-`B`/`B = Z_N`
variants) — plus the re-parameterization `n → L` inside an engine whose
lemmas were already length-generic.  The exponent `1/5` is unchanged
(`ε = 1/20` balances `min{L^{1/4−ε}, L^{4ε}}` exactly as in the paper).
The probabilistic mechanism is unchanged, but the localization proof is not
verbatim: S3 must prove the offset base case R1 and use the integer distance
`⌈d⌉` with the rounded milestone gap
`⌈3d⌉−2⌊d⌋≥⌈d⌉`.  These are repository proof obligations, now
discharged analytically in §D.0--D.3.

---

## F. Aggressive counterexample search (independent implementation)

Tooling (`audits/independent_validation/seg_deep/`, written from the
definitions only): `seg_engine.cpp` (exact binomial-weighted enumeration
over `f|_B` — exact rationals for `N ≤ 60` via `__int128`, `lgamma`
log-weights beyond; native-cyclic BFS evaluator; coloring MC; pure-walk
offset-Fréchet MC; exact first-passage DP), `seg_bruteforce_chains.py`
(literal chain DFS vs. grid DP), `seg_battery.py` (driver).  Cross-engine
agreement: C++ exact = Python enumeration exactly (5 configs, `N = 14`,
e.g. 1160/3432, 1040/3432, 560/3432, 2214/3432, 2652/3432); walk MC vs.
exact uniform-limit values: 0.2403/0.2415, 0.1795/0.1789, 0.3266/0.3265.

**Structural attacks (exact, zero tolerance):**
* Grid normal form and cyclic cut: 3.8 million per-coloring equality checks
  across four independent evaluators — 0 mismatches (§D.4).
* Translation/reflection: exact count equality at shifted/wrapped positions
  and under `p ↔ m` — holds exactly everywhere tested.
* Unconditioning: exact conditional probabilities converge monotonically
  DOWN to the uniform limit as `N` grows at fixed `(A, L, k)`
  (e.g. `p = m = 6, k = 1`: 0.4611 (`N=15`) → 0.2850 (41) → 0.2429 (1001)
  → 0.24146 (10^7+1)); worst conditional/uniform ratio observed 1.91 at
  `N = L + 3` — far inside the `3√N` bound.  No configuration approaches
  the bound.

**Rate attacks (the only attackable content, since the event is monotone
and the statement asymptotic):**
* Exact adversarial scan (`N = 41, σ = 1`, all `|A| ≤ 3`, all splits,
  `L = 6..20`): the maximizing configuration is always the balanced split
  with the smallest-offset `A` (`|A| = 1` for `k = 1`, `|A| = 2` i.e.
  `σ_A = 0` available for `k = 2`); the max decays strictly and
  monotonically in `L` (k=1: 0.455 → 0.188; k=2: 0.688 → 0.442).  No
  anomalous family.
* Walk-level battery to `L = 2048` (400k samples/point): `k = 1` balanced
  split: 5.15e-2 (L=32) → 1.03e-2 (64) → 6.0e-4 (128) → 2.5e-6 (256) →
  0/400k (512+); `k = 2`: 1.14e-1 (64) → 3.99e-3/2.98e-3/2.54e-3 at
  offsets 0/1/2 (256) → ~2.5e-6 (1024) → 0/400k (2048).  Decay is far
  FASTER than `exp(−cL^{1/5})` everywhere — the claimed bound is loose in
  the safe direction, consistent with the skeptic audit's pure-exponential
  fits.
* Offset attack (the specific mechanism SEG adds): at `k = 2` the
  offset-2/offset-0 ratio is 0.68 (L=64) → 0.64 (L=256), constant across a
  30× probability drop; at `k = 1` the offset-1 start is actually FAVORED
  (ratio ≈ 1.25, stable L=32..128 — a parity effect: `V(j,i) ≡ σ' + i + j
  (mod 2)`, so an odd offset lets odd-time states sit at 0).  In both
  directions the offset moves constants, never the rate — exactly S3's
  content.  (Consistent with the committed audit's coloring-level 0.68.)
* Split attack (`L = 256, k = 1`): one-sided and skewed splits give 0/400k
  while the balanced split gives 2.5e-6 — the extremal case is the one S3
  covers at its stated rate; one-sided cases are tube-confined and
  enormously smaller, as predicted.
* `k`-boundary: for `k` at the edge of its allowed range the constraint
  `k < L^{1/5}` admits only `k = 1` below `L = 32`, `k = 2` below 243, so
  small-`L` tables with larger `k` sit OUTSIDE SEG's scope and cannot
  refute it; inside scope, all data decays.

**Conclusion of the hunt: no counterexample, no anomalous parameter
regime, no structural failure.  Every attack surface (position,
translation, parity, split, offset, conditioning tilt, cyclic wrap,
degenerate split, `k`-edge) was probed; the exact reductions hold with
zero mismatches and the measured rates are uniformly inside the claim.**

---

## G. Comparison with the repository proof (performed last)

Read after §§B–F were complete: `research_cycle_05/flsy_reconstruction.md`
§§2–3, `audits/cycle05_seg_lemma_adversarial.md` (verdict SOUND WITH
REPAIRS; endorsed form §7), and the SEG portions of
`switch_structure_theory.md`, `results/research_cycle_05.md`,
`RESEARCH_STATE.md`, and the prior independent validation.

* **Agreement and later correction.**  The independent anchor census,
  `√N` unconditioning, proper cyclic cut, and theorem statement
  agree with the earlier reconstruction.  The original claim that no
  discrepancy emerged is **superseded**.  The arms-length report identified
  R1, R2, and R5.  The later Sol validation then showed that its R3 remained
  incomplete and its R4 was false: the missed equality is
  `L=j⁵+1`, not `L=j⁵`.  Section D now contains the
  analytic real-threshold/rounded proof and the length-`L`
  terminal-split encoding required by the final audit.
* **What this audit adds beyond the repository's state.**  (1) The complete
  standalone written proof (§D) with explicit absolute constants and the
  careful i.i.d. domination construction — the artifact whose absence was
  the recorded blocker ("a full standalone write-up does not exist");
  (2) exact-arithmetic validation of the grid/cyclic reductions (3.8M
  checks) — the repository had validated its DP only by MC-era spot
  brute-force; (3) exact probabilities across `N` spanning six orders of
  magnitude, nailing the unconditioning slack empirically; (4) the
  walk-level isolation of the offset effect (their evidence was
  coloring-level); (5) the parity hygiene note (σ ≡ N mod 2, vacuous
  otherwise) — cosmetic, no repair needed for truth; (6) independent
  confirmation that no revision of TR26-001 exists and the published
  version adds no segment statement.
* **Integrated boundary points.**  The statement records
  `σ≡N (mod 2)`; the cyclic-full variant records the
  `(L+1)` factor; and Theorem F's Lemma RS must cover every finite
  state, including the size-2 and size-`q−2` boundary cases.

---

## H. Consequences for Theorems C and F

**Theorem C.**  There are `q−5` middle states.  If
`h=D_mid(P)+1`, one common-label block has at least
`⌈(q−5)/h⌉` states and therefore at least

```text
M=⌊(q−7)/h⌋
```

additions.  The earlier assertion of at least the real number
`L*=(q−7)/h` additions was false when `L*` is
nonintegral.  Since `M≥L*/2` for `L*≥2`, applying SEG
with ambient `N=q`, total `σ=+1`, `k=2`, a
proper cyclic endpoint, and segment length `M` preserves the
displayed theorem after replacing the decay constant by
`c₁/2^{1/5}`.  The polynomial order/endpoint budget has slack.

**Theorem F.**  Its long-run branch applies SEG to a proper cyclic segment
with `k=2` and added length at least
`⌊n^{1/5}/7⌋`.  Its short-run branch is separate: the run-sandwich
argument gives `O_1`-defect at most `L+2` for **every**
finite state (prepend size 2 to the first later-copy middle run when needed,
use the universal co-singleton for size `q−2`, and note that sizes
1 and `q−1` are common).  The chain form of Theorem E then invokes
the published FLSY Theorem 4.4 on `n−2` points with

```text
k=5+3(L+2)=11+3⌊n^{1/5}/7⌋,
```

not SEG's `k=2`.  Both applications lie strictly inside their
respective ranges for sufficiently large `n`.

The subsequent arms-length and Sol audits now supply the independent checks
that were still pending when this report was first written.  SEG, C, and F
are therefore recorded as **ADVERSARIALLY REVIEWED PROOF CANDIDATES;
UNFORMALIZED**, with C and F retaining an explicit dependency on SEG.  SEG
remains unpublished: neither version of FLSY contains the segment theorem.

---

## I. Files and reproduction

* This audit: `audits/cycle05_seg_deep_independent_validation.md`.
* Engine: `audits/independent_validation/seg_deep/seg_engine.cpp`
  (`g++ -O2 -std=c++17 -o seg_engine.exe seg_engine.cpp`); modes:
  `fp` (first-passage law, exact DP vs. formula), `exact N σ a p m k`,
  `scan N σ L kmax`, `cyc N σ`, `mc`, `walk L split off k samples seed`.
* Brute force: `seg_bruteforce_chains.py` (chain DFS vs. grid, linear +
  cyclic; seed 20260822).
* Battery driver: `seg_battery.py` (`xval | decay | split | nscale | scan |
  offset`); walk battery command and seeds recorded in
  `walk_battery.out`'s generating loop (seeds `L+off+99`, `L+off+7`,
  `L+sp+3`).
* Primary source: ECCC TR26-001 PDF (scratchpad copy, fetched 2026-08-22);
  full-text scan `flsy_fulltext.txt` (scratchpad).

No branch was merged and no later research cycle was started.  Corrected
verdict: **SEG-SOUND-WITH-REPAIRS**, with R1--R5 integrated in §D and the
dependency/status consequences for Theorems C and F recorded in §H.

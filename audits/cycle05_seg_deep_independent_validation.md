# Deep independent validation of Lemma SEG (standalone hostile investigation)

**Role:** standalone hostile mathematical investigator.  This is NOT Research
Cycle 6 and continues no O01 research.  SEG was treated as FALSE until proved.
**Date:** 2026-08-22.
**Target:** the true mathematical status of Lemma SEG (segment interval
anti-concentration), currently an unpublished reconstruction (repository
status `PROOF CANDIDATE`), on which Theorems C and F of
`research_cycle_05/switch_structure_theory.md` are conditional.
**Branch audited:** `cycle05-fable` at `bd12e5c`, working tree carrying only
untracked prior-audit tooling.  Nothing tracked was modified by this
investigation; all new files are untracked
(`audits/independent_validation/seg_deep/`, this file).

## Verdict

```text
SEG-PROVABLE-AS-STATED
```

**"As stated" = the endorsed form** of `audits/cycle05_seg_lemma_adversarial.md`
§7, which the repository designates as the operative statement of SEG
(`switch_structure_theory.md` §5 defers to it explicitly).  Answer to the
mandated core question: **SEG follows rigorously from the published FLSY
machinery; the localization does NOT require a genuinely new unproved
statement.**  The only statement not literally present in the paper — an
offset-tolerant restatement of FLSY Lemma 4.3 — has a proof that is the
published proof verbatim: the published induction maintains the invariant
"the chasing walk is within `d` of the current milestone", and the perturbed
base case `|Y(0) − z₀| = |f(A)| ≤ k < d` is an instance of that invariant.
Localization changes **only a polynomial factor** (`O(n^{5/2}) → 3√N`, or
`3√N·(L+1)` for the union-over-`B` form) and re-parameterizes the decay from
`n^{1/5}` to `L^{1/5}`; the exponent `1/5`, the walk lemmas, and the
first-passage engine are untouched.  A complete standalone proof with all
dependencies explicit is given in §D below — the write-up whose absence was
the recorded reason for the conditional labels.

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
  `d`-neighborhoods of all milestones in order, each leg stochastically
  dominating a fresh first passage `F_{Δ−2d} = F_d`; the sum's lower tail
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
`σ ∈ ℤ` with `|σ| ≤ 1`, for `f` uniform on `{g: [N] → {±1}, g([N]) = σ}`,
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

### D.0 Lemma W1 (first-passage law; explicit Lemma 4.5)

For integers `δ ≥ 1`, `y ≥ 1`: `Pr[F_δ = y] = (δ/y)·2^{−y}·binom(y,(y+δ)/2)`
when `y ≡ δ (mod 2)`, else 0 (hitting-time theorem).  Consequently, by the
reflection identity `Pr[F_δ ≥ z] = Pr[−δ < g(z−1) < δ] + Pr[g(z−1) = −δ]`
and the point-mass bounds `binom(u,⌈u/2⌉)2^{−u} ≤ 0.8/√u` and
`Pr[g(u) = x] ≥ 0.35/√u` for `|x| ≤ √u/2` (Stirling with explicit error, or
finitely many small cases absorbed): there are absolute `c_lo ≥ 1/6`,
`c_hi ≤ 4` with

```text
c_lo·δ/√z  ≤  Pr[F_δ ≥ z]  ≤  c_hi·δ/√z        for all integers z ≥ 4δ².
```

*Machine check (exact DP, `seg_engine.exe fp`):* the DP law equals the
formula exactly at `δ ∈ {1,2,3,5}`, `y` up to 1001; the ratio
`Pr[F_δ ≥ z]·√z/δ` lies in `[0.75, 0.7979]` on `z ≥ 4δ²`
(→ `√(2/π) ≈ 0.798`), comfortably inside `[1/6, 4]`.

### D.1 Lemma W2 (milestones; explicit Lemma 4.7)

Let `g` be a fresh walk of length `ℓ`, `Δ ≥ max(2, 2 ln ℓ)`, `c₃ := 256`,
`K := ⌊ℓ/(c₃Δ³)⌋`.  Call `x_1 < … < x_j` a `(g,Δ)`-sequence if
`|g(x_i) − g(x_{i−1})| ≥ Δ` for all `i` (with `x₀ := 0`), and `L_Δ` the
maximum length.  Then `Pr[L_Δ < K] ≤ e^{−Δ/6}`.

*Proof.*  Let `D_Δ := inf{t > 0 : |g(t) − g(0)| = Δ}` (two-sided).
(1) `Pr[D_Δ > c₃Δ³] ≤ 2^{−Δ}`: split the first `c₃Δ³` steps into `Δ`
blocks of `c₃Δ²` steps.  On `{D_Δ > c₃Δ³}` the walk stays in
`(g(0)−Δ, g(0)+Δ)`, so each block's increment walk stays in `(−2Δ, 2Δ)`,
hence does not hit `+2Δ`, an event of probability
`≤ Pr[F_{2Δ} ≥ c₃Δ²] ≤ c_hi·2Δ/(√c₃·Δ) = 8/16 = 1/2` by W1
(`c₃Δ² ≥ 4(2Δ)²` since `c₃ = 256 ≥ 16`).  Blocks have disjoint increments,
hence are independent: probability `≤ 2^{−Δ}`.
(2) Let `D^{(1)}, D^{(2)}, …` be the successive two-sided passage times
(strong Markov: i.i.d. copies of `D_Δ`); if `Σ_{i≤K} D^{(i)} ≤ ℓ` the
points `x_i = D^{(1)} + … + D^{(i)}` form a `(g,Δ)`-sequence of length `K`
(increments exactly `±Δ`).  So
`Pr[L_Δ < K] ≤ Pr[∃ i ≤ K: D^{(i)} > ℓ/K] ≤ K·2^{−Δ} ≤ ℓ·2^{−Δ}
= e^{ln ℓ − Δ ln 2} ≤ e^{−Δ(ln 2 − 1/2)} ≤ e^{−Δ/6}`,
using `ℓ/K ≥ c₃Δ³` and `Δ ≥ 2 ln ℓ`.  ∎

### D.2 Lemma W3 (sum lower tail; explicit Lemma 4.6)

Let `F^{(1)}, …, F^{(K)}` be i.i.d. copies of `F_δ` (`δ ≥ 1`) and `T ≥ 1`
with `Kδ² ≤ T`.  Then

```text
Pr[ Σ_{i≤K} F^{(i)} ≤ T ]  ≤  exp( − c_lo²·(Kδ)²/(16T) ).
```

*Proof.*  Set `t* := (2T/(c_lo·K·δ))²`.  From `Kδ² ≤ T` and `c_lo < 1`:
`t* ≥ 4δ²`, so W1 gives `p := Pr[F_δ ≥ t*] ≥ c_lo·δ/√t* = c_lo²Kδ²/(2T) =: p_lo`
(and `p_lo ≤ 1` since `c_lo² < 2`).  On `{Σ F^{(i)} ≤ T}` at most `T/t*`
of the `F^{(i)}` are `≥ t*`; and `T/t* = c_lo²(Kδ)²/(4T) = K·p_lo/2`.
By monotone coupling and the Chernoff lower tail
`Pr[Bin(K, p_lo) ≤ Kp_lo/2] ≤ e^{−Kp_lo/8}`:
`Pr[Σ F ≤ T] ≤ e^{−Kp_lo/8} = exp(−c_lo²(Kδ)²/(16T))`.  ∎

### D.3 Lemma S3 (offset Fréchet anti-concentration; the one formally new statement)

There are absolute `c₁ > 0` and `L₀' ∈ ℕ` such that for all `L ≥ L₀'`, every
split `m + p = L` (`m, p ≥ 0`), every integer offset `σ'` with
`|σ'| ≤ d := L^{1/5}`, and `X` a fresh walk of length `m` with
`X(0) = σ'`, `Y` an independent fresh walk of length `p` with `Y(0) = 0`:

```text
Pr[ d_F(X, Y) < d ]  ≤  2·exp(−c₁·L^{1/5}).
```

(The general-`ε` form, mirroring Lemma 4.3 with `min{L^{1/4−ε}, L^{4ε}}`,
holds by the same proof; SEG needs only `ε = 1/20`.)

*Proof.*  Set `Δ := 3d`.  By symmetry of `d_F` (Definition 4.1 is symmetric
under swapping `(X,l,α) ↔ (Y,r,β)`) assume the walk of length
`ℓ := max(m,p) ≥ L/2` is the *milestone walk* `M`, the other (`length
r' = min(m,p) ≤ L/2`) the *chaser* `H`.  Exactly one of `M, H` carries the
offset; write `z₀ := M(0)`, `h₀ := H(0)`, so `|z₀ − h₀| = |σ'| ≤ d` in both
cases.

**Milestones.**  Apply W2 to the increment walk `M − z₀` (fresh, length
`ℓ`), with this `Δ`: except with probability `e^{−Δ/6} ≤ e^{−d/2}`, there
are times `x_1 < … < x_K ≤ ℓ`, `K := ⌊ℓ/(c₃Δ³)⌋`, with milestone values
`z_i := M(x_i)` satisfying `|z_i − z_{i−1}| ≥ Δ` for all `i ∈ [K]` —
including `i = 1`, whose gap is measured from `z₀ = M(0)` (W2's `x₀ = 0`).
W2's hypotheses hold for `L ≥ L₀'`: `Δ = 3L^{1/5} ≥ 2 ln L ≥ 2 ln ℓ`
(true once `L^{1/5} ≥ (2/3)ln L`) and `K ≥ 1` (true once
`L/2 ≥ c₃·27·L^{3/5}`, i.e. `L^{2/5} ≥ 13824`).

**Extraction.**  Condition on such an `M`.  Suppose `d_F(M, H) < d` (the
event is symmetric).  Fix a witnessing staircase `(α, β)`.  Since `α` is
nondecreasing onto `{0,…,ℓ}` with unit steps, each `x_i` has a minimal time
`t_i` with `α(t_i) = x_i`; `x_i` strictly increasing forces `t_i` strictly
increasing, and `t_i ≥ 1` (as `x_i ≥ x_1 > 0 = α(0)`).  Setting
`b_i := β(t_i)`: `|z_i − H(b_i)| < d` for all `i ∈ [K]`, `b_i`
nondecreasing; and `b_i = b_{i−1}` is impossible since it would give
`|z_i − z_{i−1}| < 2d < Δ`.  So `b_1 < … < b_K ≤ r'`, i.e. `H` visits the
`d`-neighborhoods of `z_1, …, z_K` in order within its lifetime.
(This is the corrected form of the p. 25 extraction: it needs only the
milestone gaps `> 2d`, which are offset-invariant.)

**Domination.**  Define stopping times `τ₀ := 0`,
`τ_i := inf{t > τ_{i−1} : |H(t) − z_i| ≤ d}` (on the infinite extension of
`H`; on the event above, `τ_i ≤ b_i ≤ r'` for all `i ≤ K`).  Maintain the
invariant `|H(τ_{i−1}) − z_{i−1}| ≤ d`: for `i ≥ 2` it holds by definition
of `τ_{i−1}`; for `i = 1` it is the hypothesis `|h₀ − z₀| = |σ'| ≤ d` —
**this is the entire role of the offset, and it is an instance of the
invariant the published induction already maintains.**  Then
`|z_i − H(τ_{i−1})| ≥ |z_i − z_{i−1}| − d ≥ Δ − d`, so to enter the
`d`-ball of `z_i` the walk must first traverse to the near boundary, a net
displacement `≥ Δ − 2d = d` on the side of `z_i`; by the intermediate-value
property of `±1` walks, `τ_i − τ_{i−1} ≥ F̃^{(i)}`, where `F̃^{(i)}` is the
first passage of the post-`τ_{i−1}` increment walk to displacement `d`
toward `z_i`.  Conditional on `𝓕_{τ_{i−1}}`, `F̃^{(i)}` has exactly the law
of `F_d` (strong Markov; the target side is `𝓕_{τ_{i−1}}`-measurable and
the law is symmetric), a fixed law — hence `(F̃^{(1)}, …, F̃^{(K)})` are
i.i.d. copies of `F_d` by induction.  Therefore
`Pr[d_F < d | M] ≤ Pr[Σ_{i≤K} F̃^{(i)} ≤ r'] ≤ Pr[Σ_{i≤K} F^{(i)}_d ≤ L/2]`.

**Tail.**  Apply W3 with `δ := d`, `T := L/2`:  hypothesis
`Kd² ≤ (L/(2c₃·27d³))·d² = L/(13824·d) ≤ L/2 = T` holds; and
`Kd ≥ (L/2 − c₃Δ³)/(c₃Δ³)·d ≥ L·d/(4c₃Δ³) = L/(27648·d²)` for `L ≥ L₀'`
(absorbing the floor), so
`(Kd)²/(16T) ≥ 2L²/(27648²·d⁴·16L) = L^{1/5}/(8·27648²)`.
Hence `Pr[Σ ≤ L/2] ≤ exp(−c_lo²·L^{1/5}/(8·27648²))`.

**Total.**  `Pr[d_F < d] ≤ e^{−d/2} + exp(−(c_lo²/(8·27648²))·L^{1/5})
≤ 2 exp(−c₁ L^{1/5})` with
`c₁ := min{1/2, c_lo²/(8·27648²)} ≥ 4.5·10^{−12}` absolute.  Degenerate
split `r' = 0`: the domination step gives `τ_1 ≥ 0`, `τ_2 ≥ 1 > 0 = r'`,
and `Pr[Σ_{i≤K} F̃ ≤ 0] = 0` for `K ≥ 1`, so the bound holds a fortiori
(this is the tube case; classically `≤ exp(−Ω(L/d²))`).  `L₀'` is the
absolute threshold making `L^{1/5} ≥ (2/3)ln L` and `L^{2/5} ≥ 13824`
(crudely `L₀' ≤ 3·10^{10}`; with FLSY's unoptimized-`Ω` style the same
statement holds "for sufficiently large `L`").  ∎

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
and the linear normal form applies verbatim.  Cyclic case `B = Z_N`,
`A ≠ ∅`: every PROPER cyclic interval containing `A` is `[a₁−u, a₂+v]`
with `u + v ≤ L − 1` (`L := N − |A|`), the two extension arcs stay disjoint
through step `L − 1`, and the final step adds the last remaining point; the
terminal split `(u, v)`, `u + v = L − 1`, is not determined, so union over
its `L` values (factor `≤ L + 1`).

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

**Theorem S.**  With `c := c₁` from S3, `C := 3`, `L₀ := L₀'` from S3: for
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
union bound.  Variant (iii): S1's cut for `B ≠ Z_N`; for `B = Z_N`, S1's
terminal-split union over `L` grid events of total length `L−1`, each
bounded as above (with `L−1 ≥ L₀ − 1`; absorb into constants).  Variant
(iv): the same grid with `V(j,i) := λ(j) + ρ(i)` and offset 0 — S3 with
`σ' = 0`, no `|f(A)| ≤ k` conjunct needed.  ∎

**Dependency list (exhaustive).**  Hitting-time theorem for simple walks
(classical; machine-verified exactly); reflection identity; Stirling
point-mass bounds; Chernoff's lower tail for binomials; strong Markov
property; FLSY's proof pattern of Lemmas 4.6/4.7 and §4.4 (re-derived in
full above — no step of the paper is used as a black box); the endorsed
statement's own hypotheses.  **Nothing else.**  In particular: no new
probabilistic estimate, no new combinatorial lemma, no appeal to any
unpublished source.

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
(each chaser leg ⪰ fresh `F_d` via strong Markov).  All three are
statements about fresh walks of length ≤ `L`; localization does not touch
them.

**What localization changes (mandate item 6):** only a polynomial factor —
`O(n^{5/2})` (= `n²` for `(s,e)` × `√n` unconditioning) becomes `3√N` (no
`(s,e)` enumeration at all; `(L+1)` only for the union-over-`B`/`B = Z_N`
variants) — plus the re-parameterization `n → L` inside an engine whose
lemmas were already length-generic.  The exponent `1/5` is unchanged
(`ε = 1/20` balances `min{L^{1/4−ε}, L^{4ε}}` exactly as in the paper).
Nothing is invalidated.  The one formally new statement is S3's offset
tolerance, whose proof is the published induction with its own maintained
invariant covering the perturbed base case; the offset degrades the `i = 1`
leg's domination from `F_{Δ−d}` at worst to `F_{Δ−d−k} ⪰ F_{Δ−2d}` — the
SAME bound the published proof uses for every leg.

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

* **Agreement.**  My independent anchor census (§B, 3 bookkeeping uses + 1
  milestone base case) coincides with the reconstruction's §3(a)–(b) and
  the skeptic audit's §0.  My offset analysis (`F_{Δ−d−k} ⪰ F_{Δ−2d}` iff
  `k ≤ d`; alternatively an invariant-instance with no degradation at all)
  matches their §2.  My `√N`-placement reasoning matches their §3; my
  cyclic-cut and `B = Z_N` terminal-split treatment matches their §4; the
  five paper-level slops I found independently are their §5 items 1–5,
  one-for-one.  My Theorem S is exactly their §7 endorsed form, clause by
  clause, including variants (i)–(iv).  I find their audit's reasoning
  correct at every point I re-derived; no discrepancy of any kind emerged.
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
* **Residual nits (cosmetic, non-blocking).**  (a) The endorsed form would
  ideally record `σ ≡ N (mod 2)` (or the vacuity convention);
  (b) `switch_structure_theory.md` §5's abbreviated display could cite the
  `B = Z_N` factor as `(L+1)` explicitly rather than only by exclusion;
  (c) prior-audit finding F5 (Lemma RS wording, Theorem F's sizes-from-2
  coverage) is unaffected by this audit and stands.

---

## H. Consequences for Theorems C and F

**Logical consequence of the verdict.**  Theorem S proves the exact
statement Theorems C and F import: Theorem C uses the absolute event,
`k = 2 < (L*)^{1/5}` (its regime `L* ≥ C(log q)⁵` gives `(L*)^{1/5} > 2`),
cyclic order with `|A| ≥ 3` and `|B| ≤ q − 3 < q` (cut point exists),
ambient `|f(Z_q)| = σ = 1` with matching parity (`q` odd), relabeled orders
covered by exchangeability of the measure under `π`, and a
`t·q³`-to-`t·q⁴` union-bound slack that absorbs `3√q·(L+1)` for
`L* ≥ C(log q)⁵`.  Theorem F's long-run branch uses the same import at
`k = 2`, `L = ⌊n^{1/5}/7⌋` — inside Theorem S's hypotheses for large `n`.
**Therefore: if the proof in §D is correct, Theorems C and F hold as
stated** (their own derivations were audited separately:
`cycle05_theorems_adversarial.md`, the prior independent validation §C, and
spot-rechecked here), with C's and F's constants inheriting `c₁`'s
absolute-but-unoptimized value.

**Status discipline (what the verdict does and does not support).**  SEG
remains UNPUBLISHED and UNREFEREED; no segment statement exists in either
version of FLSY (re-verified at source).  The repository's stated gate for
lifting the conditional labels (skeptic audit §9) is: "(a) SEG is written
out in full and independently verified as a standalone proof, or (b) an
equivalent statement appears in the literature."  This audit supplies the
full write-up of (a) and constitutes one independent derivation of the
endorsed statement (formed before comparison); but the write-up and its
verification are the work of a single investigation, so the arms-length
verification step of gate (a) remains open.  Accordingly:

* Supported NOW: re-scoping the condition on Theorems C and F from
  "conditional on an unproved reconstruction-level statement (proof
  candidate, outline only)" to "conditional on the correctness of the
  complete written proof of Theorem S
  (`audits/cycle05_seg_deep_independent_validation.md` §D), which derives
  SEG from the published FLSY machinery with no new probabilistic
  estimates".  SEG's own label may move from `PROOF CANDIDATE
  (reconstruction/outline)` to `PROOF CANDIDATE — COMPLETE STANDALONE
  WRITE-UP AVAILABLE (this audit §D); awaiting arms-length verification`.
* NOT supported: upgrading Theorems C or F to unconditional/`PROVED`, or
  removing "refuting SEG" from the reopen-conditions of
  `RESEARCH_STATE.md`, until §D survives an independent check by a
  reviewer who did not produce it (or SEG appears refereed in the
  literature).  This audit performs no such upgrade and modifies no
  repository status text.

**If §D is verified, the downstream picture** (stated for the record, not
enacted): C and F become theorems resting solely on published, refereed
inputs plus repository-internal proofs, closing the two-copy and
low-switch-depth obstruction tracks unconditionally; the open boundary of
Cycle 5 would then be exactly Lemma M (`t ≥ 3` stitching) and ∞-moving
relabelings, as `RESEARCH_STATE.md` already isolates.

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

Per the mandate: no branches merged, no Cycle 6 started, no repository
status files modified.  Verdict: **SEG-PROVABLE-AS-STATED**, with the
complete proof in §D and the consequences for Theorems C and F exactly as
bounded in §H.  Stop.

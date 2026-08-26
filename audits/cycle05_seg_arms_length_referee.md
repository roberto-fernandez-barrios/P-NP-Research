# Arms-length hostile referee report: Lemma SEG (Theorem S)

**Role:** arms-length hostile referee for one mathematical lemma only.  Not
Research Cycle 6; no O01 research; no new constructions; SEG assumed FALSE
throughout the review until forced otherwise.
**Date:** 2026-08-25.
**Submission under review:** the standalone proof of Lemma SEG in
`audits/cycle05_seg_deep_independent_validation.md` (treated as an anonymous
mathematical submission; referred to below as **[SUB]**, its sections as
[SUB §D] etc.).  The original review did not modify the submission.
**Correction note (2026-08-27):** the later Sol cross-model validation found
the original R3 justification incomplete and R4 false.  This report now
incorporates the exact replacement arguments from
`audits/cycle05_sol_final_cross_model_validation.md` §§5.4--5.8;
the superseded R3/R4 reasoning is not retained as valid.
**Primary source:** ECCC TR26-001 (Fabris–Limaye–Srinivasan–Yehudayoff),
fetched independently for this review from
`https://eccc.weizmann.ac.il/report/2026/001/download` (990,707 bytes) and
read directly as page images: pp. 1–8 (definitions 1.2/1.4, Theorems 1.3,
1.6, 1.7, Corollary 1.8) and pp. 16–25 (§3 and the whole of §4: Definition
4.1, Lemmas 4.2, 4.3, 4.5, 4.6, 4.7, Theorem 4.4, with complete proofs).
Every FLSY citation below was verified against those page images, not
against any repository reconstruction.
**Independent tooling:** `audits/independent_validation/seg_referee/`
(`referee_checks.py`, `referee_results.json`), written for this review from
the definitions only.  No code, constants, or random seeds from
`experiments/cycle05_audit_seg_mc.py`, `audits/independent_validation/my_seg_mc.py`,
or `audits/independent_validation/seg_deep/*` were reused or opened; seed
family 250825xxx is disjoint from all recorded prior families (20260821,
20260822, `L+off+99`, `L+off+7`, `L+sp+3`).

---

## Verdict

```text
SEG-SOUND-WITH-REPAIRS
```

The frozen SEG statement (§1) is sound with the exact proof repairs R1--R5
in §5.  None changes the theorem statement, hypotheses, quantifiers,
exponent, or constants.  R1 supplies the missing first-leg base case; R2
replaces a false floor inequality on a bounded window; R3 supplies a fully
analytic integer-level/real-threshold proof; R4 replaces the false
length-`L−1` cyclic reduction by a length-`L` encoding;
and R5 fixes the declared bookkeeping constant to `C=6`.

**Do the repairs affect Theorems C and F?  No.**  C and F import only the
statement of SEG (frozen form, §1), which is unchanged; the repairs are
internal to the proof.  The instantiation check (§7) passes: C and F invoke
SEG strictly inside its proven parameter range, and F's density-branch
parameter `k = 11 + 3⌊n^{1/5}/7⌋ ≈ (3/7)n^{1/5}` is an application of
published FLSY Theorem 4.4 (not of SEG) and sits inside ITS range
`k < (n−2)^{1/5}` for all `n` beyond an absolute threshold.

Epistemic status after the subsequent independent cross-model check:
**ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED**.  SEG remains an
unpublished repository derivation, not a theorem stated verbatim by FLSY.
C and F retain their explicit dependency on SEG but no longer need the stale
label "conditional on an unproved outline."

---

## 1. The frozen claim

Extracted verbatim from [SUB §C, §D.6] (the repository's operative form,
endorsed by `audits/cycle05_seg_lemma_adversarial.md` §7).  Nothing below
was strengthened or weakened during review.

> **Theorem S.**  There exist universal constants `c > 0`, `C > 0`,
> `L₀ ∈ ℕ` such that: for **every** `N ∈ ℕ`; every `σ ∈ ℤ` with `|σ| ≤ 1`
> (and `σ ≡ N (mod 2)`; otherwise the conditioned measure is empty and the
> statement is read as vacuous); `f` uniform on
> `{g : [N] → {±1}, g([N]) = σ}`; **fixed** intervals `∅ ≠ A ⊆ B ⊆ [N]`
> with `L := |B∖A| ≥ L₀`; and every **integer** `1 ≤ k < L^{1/5}`:
>
> `Pr_f[∃ chain A = D₀ ⊂ D₁ ⊂ … ⊂ D_L = B, each D_i an interval of [N],`
> `      |f(D_i)| ≤ k for all 0 ≤ i ≤ L]  ≤  C·√N·exp(−c·L^{1/5})`
>
> with variants: (i) `g` uniform on `{±1}^{[N]}`: no `√N` factor;
> (ii) "some `B ⊇ A` with `|B∖A| = L`": extra factor `(L+1)`;
> (iii) cyclic order `Z_N` with `B ≠ Z_N`: verbatim; `B = Z_N` (and
> `A ≠ ∅`): extra factor `(L+1)`; (iv) relative form
> `|f(D_i) − f(A)| ≤ k` for `i ≥ 1`: same bounds with offset 0.

Frozen parameters/conventions: the chain has length exactly `L+1` (strict
nestings force one added point per step); the `i = 0` conjunct
`|f(A)| ≤ k` is part of the event; endpoints `A, B` are deterministic
(fixed before `f` is drawn) except in variant (ii); in variant (iii) with
`B ≠ Z_N` the cut point is an arbitrary `c ∈ Z_N ∖ B` and the claim is
cut-point-independent (verified exactly, §6); `d := L^{1/5}` is used as a
real parameter, `d_F` is integer-valued; [SUB]'s claimed explicit witnesses are
`c=c₁=min{1/2,(1/6)²/(8·27648²)}`
(`=4.542344518777...·10⁻¹²`) and `C=6` (the "`C:=3`"
in [SUB §D.6] is a bookkeeping slip: `3√N` from S2 times `2e^{−c₁L^{1/5}}`
from S3 gives the displayed `6√N·exp(−cL^{1/5})`; see R5), and `L₀` = the
exact threshold `L₀=⌈13824^{5/2}⌉=22,469,029,418`; at it
`L^{1/5} ≥ (2/3)ln L` also holds.  Sufficiently-large regime: none beyond
`L ≥ L₀`; `N` is unrestricted.

Honest-disclosure note (not a defect): with these unoptimized constants the
numeric bound is `> 1` until astronomically large `L`; the theorem's
content, like FLSY's own unspecified-`Ω` statements, is the existence of
universal `(c, C, L₀)`.  Theorems C and F consume it asymptotically, which
is exactly what is proved.

## 2. Dependency DAG

```text
Theorem S [SUB D.6]
├─ S1  grid normal form (linear / cyclic-cut / B=Z_N split)   [SUB D.4]
│      NEW combinatorics, replaces FLSY Lemma 4.2 (strictly simpler:
│      no (s,e) enumeration, no cyclic bookkeeping).  Proof obligation
│      discharged in [SUB D.4] + machine-verified exactly (here, §6).
├─ S2  unconditioning ×3√N                                    [SUB D.5]
│      = FLSY p.21 step, MODIFIED (explicit constant 3; σ ∈ {0,±1} not
│      only balanced).  Own proof: central binomial bound.  Verified §6.
├─ S3  offset Fréchet anti-concentration                      [SUB D.3]
│      = FLSY Lemma 4.3 (ECCC p.18, proof §4.4 pp.24–25), MODIFIED:
│      n → L, initial offset |σ'| ≤ d, per-split statement, explicit
│      constants.  Own full proof.  THE formally new statement.
│   ├─ W2  milestones = FLSY Lemma 4.7 (p.23), MODIFIED (real Δ,
│   │      integer exit ⌈Δ⌉, ⌊Δ⌋ blocks, explicit c₃ = 256,
│   │      e^{−Δ/6}, arbitrary length ℓ).  Own proof.
│   │   └─ W1 (upper bound branch)
│   ├─ W3  first-passage-sum lower tail = FLSY Lemma 4.6 (p.22),
│   │      MODIFIED (real threshold, explicit
│   │      exp(−c_lo²(Kδ)²/16T); hypothesis Kδ² ≤ T
│   │      replaces kδ² ≤ c₄n ∧ (kδ)² = ω(n)).  Own proof (Chernoff).
│   │   └─ W1 (lower bound branch)
│   ├─ corrected p.25 extraction (gaps > 2d ⟹ b_i strictly increasing)
│   └─ strong-Markov i.i.d. domination construction (τ_i, F̃^{(i)})
└─ W1  first-passage law = FLSY Lemma 4.5 (p.21), MODIFIED (infinite
       walk, real t ≥ 4δ², c_lo = 1/6, c_hi = 1.85).  Own proof
       (hitting-time theorem + reflection + Stirling).  Verified §6.
External inputs only: hitting-time theorem, reflection principle,
Stirling-type binomial bounds, Chernoff lower tail, strong Markov.
FLSY Lemma 4.2 and Theorem 4.4 are NOT in the DAG.
```

Every imported FLSY statement is used **modified**, and each modification
carries its own complete proof in [SUB §D] — the correct discipline.  My
line-by-line verification of those proofs, against the primary source and
from scratch, is §§3–5.

## 3. Attack on the offset-tolerant Lemma 4.3 (= S3) — proof holds after R1--R3

Worked under the standing assumption that the offset version is false, and
reconstructed the induction from scratch.

* **Perturbed base case.**  Put `r=⌊d⌋` and
  `δ=⌈d⌉`.  The offset enters at exactly two points: (1) the
  invariant base `|H(τ₀)−z₀|=|σ'|≤d`; (2) **R1**: the extraction
  produces `b₁≥1` because
  `|z₁−h₀|≥⌈3d⌉−|σ'|≥2d>d`, so the chaser cannot already
  sit in the `d`-ball of `z₁` at time 0; this is what makes `τ₁ ≤ b₁`
  legitimate (`τ₁` is an inf over `t > 0`).  The proof
  uses the stated load-bearing hypothesis `|σ'|≤d`,
  which holds because the segment event gives `|σ'|≤k<d`.
* **First leg vs later legs.**  Every leg `i≥1` starts within
  `r≤d` of `z_{i−1}`
  (base case: offset hypothesis; inductive case: definition of `τ_{i−1}`),
  and must traverse the integer distance
  `⌈3d⌉−2⌊d⌋≥⌈d⌉=δ`.  This is the same guarantee on every leg.
* **Conditioning/domination.**  Conditioning on the milestone walk `M` is
  harmless (`M ⊥ H`; the τ's are stopping times of `H`'s filtration with
  the `z_i` constants).  Conditional on `𝓕_{τ_{i−1}}`, the target side is
  measurable and the symmetric first-passage law gives
  `F̃^{(i)}~F_δ` exactly, independent of the past — so
  `(F̃^{(1)},…,F̃^{(K)})` are genuinely i.i.d. `F_δ`,
  not merely dominating: the coupling asked about
  in the mandate exists in the strongest form.  Verified by induction on
  finite-dimensional distributions.
* **Extraction.**  `t_i` = minimal preimage of `x_i` under the staircase's
  `α` (onto, unit steps ⟹ exists, strictly increasing, `t_i ≥ 1`);
  `b_i := β(t_i)` nondecreasing; `b_i = b_{i−1}` would force
  `|z_i−z_{i−1}|≤2⌊d⌋<⌈3d⌉` — contradiction.  This is the corrected p.25
  extraction; it needs only gaps `> 2d`, which are offset-invariant.  Holds.
* **Degenerate splits.**  `r' = 0` (one-sided growth): `b₁ ≤ r' = 0`
  contradicts `b₁ ≥ 1`, so the event (given milestones, `K ≥ 1`) is
  empty; [SUB]'s phrasing ("τ₁ ≥ 0, τ₂ ≥ 1") is garbled but its
  conclusion (bound holds a fortiori) is correct.  Repair folded into R1's
  added sentence.
* **Parity.**  Nothing in S3 needs parity; `W1`'s law lives on
  `y ≡ δ (mod 2)` internally.  The event-level parity facts (`k = 0`
  impossible; `σ ≡ N (mod 2)` hygiene) sit in the statement, correctly.
* **W2 hypotheses at the instantiation.**  `Δ = 3d = 3L^{1/5} ≥ 2 ln ℓ`
  (since `ℓ ≤ L` and `L^{1/5} ≥ (2/3)ln L` at `L ≥ L₀`), `K ≥ 1`
  (`L^{2/5} ≥ 13824`).  Checked.
* **The W3 instantiation (R2 after R3 rounding).**  Since
  `δ=⌈d⌉≤2d`, the hypothesis is
  `Kδ²≤L/(1728d)≤T=L/2`.  The upper bound is
  `K≤ℓ/(c₃Δ³)≤L/(6912d³)`; [SUB]'s
  intermediate expression `L/(13824d)` uses the lower-bound direction of
  `ℓ` in an upper bound — harmless slip, conclusion unaffected.  The
  serious item: [SUB]'s chain
  `Kd ≥ (L/2 − c₃Δ³)/(c₃Δ³)·d ≥ L·d/(4c₃Δ³)` — the second `≥` is
  equivalent to `L^{2/5} ≥ 27648` and is **strictly false** in the window
  `L^{2/5} ∈ [13824, 27648)` admitted by `L₀`.  The CONCLUSION
  `Kd ≥ L·d/(4c₃Δ³) = L^{3/5}/27648` nevertheless holds on the whole
  range `L ≥ L₀`: in the window, `K ≥ 1` gives `Kd ≥ d = L^{1/5}`, and
  `L^{1/5} ≥ L^{3/5}/27648 ⟺ L^{2/5} ≤ 27648` — exactly the window.  The
  two cases together prove the inequality for all `L ≥ L₀`, and the final
  exponent remains valid because `Kδ≥Kd`:
  `(Kδ)²/(16T)≥L^{1/5}/(8·27648²)`.
  **Repair R2 = replace the one-line floor-absorption by this two-case
  argument.**  (This was my best candidate for a fatal gap; it closes.)

Conclusion: assuming S3 false and hunting for the failure point produced
no failure.  The induction is sound with R1 and R2 added.

## 4. Attack on the localization — FAILED (nothing global is used)

Systematic search for information from outside the segment:

* **Global starting value / prior history:** the event and the whole proof
  are measurable w.r.t. `f|_B` (S1 reads only `f(A)`, `λ`, `ρ`, all inside
  `B`); no chain history conditioning occurs anywhere.
* **Global endpoint / total balance:** enters exactly once, through S2's
  pointwise inequality `Pr_{f|σ}[E] ≤ Pr_g[E]/Pr_g[g([N]) = σ] ≤ 3√N·Pr_g[E]`,
  valid for every event regardless of correlation; after it, everything
  runs under uniform `g`, where `(g(A), λ-increments, ρ-increments)` are
  mutually independent (disjoint coordinates).  The `√N` (not `√L`) is
  forced and correctly priced; exact computation (§6) shows the true ratio
  far below `3√N` and converging down to the uniform value.
* **Absolute position / translation:** the walk lemmas W1–W3 are
  statements about fresh increments of arbitrary-length walks (nothing
  global-`n` exists in FLSY's own walk layer — confirmed against pp.
  21–24); the milestone condition constrains increments only; exchange-
  ability of the conditioned measure makes position irrelevant — verified
  EXACTLY by machine (§6: identical accept counts under translation).
* **Conditioning on the segment anchor:** the decomposition over
  `g(A) = σ'` is an exact partition; independence means the conditional
  walk laws are the unconditional ones with an offset — no probability
  changes.
* **Cost of localization:** `O(n^{5/2})` (FLSY 4.2's `(s,e)` union ×
  unconditioning) → `3√N`, plus `(L+1)` only in variants (ii)/(iii-full).
  Polynomial, exactly as claimed.  The exponent `1/5` and the engine are
  untouched (`ε = 1/20` balances `min{L^{1/4−ε}, L^{4ε}}` verbatim).

## 5. Attack on the probability argument — constants and boundary regimes

Re-derived W1, W2, W3 in full (independently of [SUB]'s text, then
compared).  Findings:

* **W1, including real thresholds (R3).**  For integer `a≥1` and
  real `t≥4a²`, put `u=⌈t⌉−1`.  Reflection expresses
  `Pr[F_a≥t]` as exactly `a` parity-compatible binomial
  masses in `[−a,a)` at time `u`.  The central mode is
  at least `1/(2√u)`, and an elementary adjacent-binomial product
  comparison puts every relevant mass at least `7/8` of that
  mode.  The standard mode upper bound gives

  ```text
  a/(6√t) ≤ Pr[F_a≥t] ≤ 1.85a/√t.
  ```

  This is analytic and covers the noninteger Chernoff threshold directly;
  the independent DP is only a check.
* **W2 with real `Δ` (R3).**  Exit at integer level
  `⌈Δ⌉`.  Use `⌊Δ⌋` independent blocks of
  `⌊256Δ²⌋` steps.  Failure to exit forces every block to miss
  `⌈2Δ⌉`.  W1 bounds each miss by less than `0.30` for
  `Δ≥2`, and
  `0.30^{⌊Δ⌋}≤2^{−Δ}` for `Δ≥3`.  The old
  "lost block absorbed by measured slack" argument is superseded.
  Strong-Markov concatenation then gives
  `K2^{−Δ}≤ℓ2^{−Δ}≤e^{−Δ/6}` exactly as required.
* **W3 with integer passage distance (R3).**  Take
  `δ=⌈d⌉`.  Since tracking at strict distance `<d` means
  integer radius at most `⌊d⌋`,
  `⌈3d⌉−2⌊d⌋≥⌈d⌉=δ`.  Also
  `Kδ²≤L/(1728d)≤L/2` and `Kδ≥Kd`.  The real-threshold
  W1 applies directly to
  `t*=(2T/(c_lo Kδ))²`, so the Chernoff proof loses no constant.
* **Exponent `1/5`.**  R2 gives
  `Kd≥L^{3/5}/27648` on both
  `d²∈[13824,27648)` and `d²≥27648`.  Therefore
  `(Kδ)²/(16T)≥L^{1/5}/(8·27648²)`, and
  `c₁=min{1/2,(1/6)²/(8·27648²)}` is exact.
* **3√N:** exact central-binomial minimum `3√N·Pr[g([N]) = σ] ≥ 1`
  verified for all `N ≤ 400` (min 1.197 at N=1) and asymptotically
  (`→ 3·√(2/π)·… > 2.39`).  **(L+1):** variant (ii) is a count of splits
  (≤ L+1, exact); variant (iii-full) a count of terminal splits (L),
  machine-verified as an event identity (§6).
* **Cyclic-full boundary (R4).**  The former R4 is false.  Equality occurs
  at `L−1=j⁵`, namely `L=j⁵+1`, not at
  `L=j⁵`.  For example, with cyclic `N=34`,
  `A={0}`, `L=33`, `k=2`, the one-sided
  increments `+,-,-,(+,-)^15` keep every cyclic chain sum in
  `{0,1,2}`, while dropping the terminal point leaves
  length-32 Fréchet distance exactly 2.  The valid repair fixes a terminal
  split `u+v=L−1`, appends the final point to one extension
  sequence, and obtains disjoint walk lengths `(u+1)+v=L`.  The
  actual chain postpones that appended coordinate step to the endpoint.
  Apply S3 at length `L`, then take the `L`-way union.

**Repairs list.**
* **R1** (S3, domination): add "`b₁ ≥ 1`, since
  `|z₁−h₀|≥⌈3d⌉−|σ'|≥2d>d`;
  hence `τ₁ ≤ b₁`", and align the degenerate-split sentence to it.
* **R2** (S3, tail): two-case proof of `Kd ≥ Ld/(4c₃Δ³)` (window
  `L^{2/5} < 27648` via `K ≥ 1`; beyond it via floor absorption); fix the
  `13824` slip in the `Kd² ≤ T` check to `6912`.
* **R3** (W1/W2/W3): use the analytic real-threshold W1, rounded W2, and
  integer `δ=⌈d⌉` argument above; no simulated margin.
* **R4** (D.6, variant iii, `B=Z_N`): replace the false
  length-`L−1` inclusion by the length-`L` terminal-split
  encoding above.
* **R5** (D.6): set the theorem's final constant to `C=6`;
  `C:=3` is inconsistent with its displayed bound.
None changes the statement, hypotheses, exponent, exact `c₁`,
`C=6`, or
`L₀=22,469,029,418`; **Theorems C and F are unaffected once their
own floor/RS wording repairs are made**.

## 6. Independent counterexample search (fresh implementation)

Scope note: with the explicit constants, the frozen bound exceeds 1 for
every computationally reachable `L`, so no simulation can exhibit a
violation of the *statement*; a genuine kill must therefore come from the
exact combinatorial reductions (any mismatch falsifies the proof's
skeleton) or from an anomalous rate regime contradicting the mechanism.
Both were attacked.  Tooling: `referee_checks.py` (definition-literal
bitmask BFS that tries EVERY candidate point and tests interval-ness from
contiguity — it knows nothing of grids, endpoints, or cuts; an independent
scalar/vectorized grid DP, self-tested against a path-enumeration brute
force on 24,000 instances, 0 mismatches; exact first-passage DP; exact
enumeration over conditioned colorings).  Results
(`referee_results.json`):

* **W1 law:** exact DP = closed formula to 1.7e−18 (δ ∈ {1,2,3,5},
  y ≤ 401); reflection identity exact to 4.3e−14; constants scan
  (δ ≤ 8, z ≤ 200,000): ratio `Pr[F_δ ≥ z]·√z/δ ∈ [0.7500, 0.8385]` on
  integer `z ≥ 4δ²` (claimed [1/6, 4] — ≥ 4.5× slack both sides; the
  0.8385 max is the δ = 1 parity staircase at z = 5); real-z constant
  ≥ 0.6988 ≥ 1/6 (repair R3 confirmed numerically, 4.2× margin).
* **W2 mechanism:** exact band DP: `Pr[D_Δ > 256Δ³]` < 1e−300 for
  Δ = 4 and Δ = 6, vs claimed bounds 6.3e−2, 1.6e−2 — the inequality
  holds with astronomical room (the c₃ = 256 spacing is extravagantly
  safe; its cost is only in the constant `c₁`).
* **S2:** `min_{N ≤ 400} 3√N·Pr[g([N]) = σ] = 1.500` (at N = 1) ≥ 1.  ✔
* **S1 exactness (the kill zone):** literal BFS vs grid DP:
  linear N=10, σ=0 (all A with |A| ≤ 3, all splits p, m ≤ 4, all 252
  balanced colorings): **87,696 checks, 0 mismatches**; native cyclic
  N=12 (σ=0), N=13 (σ=1), N=14 (σ=0), k ∈ {1,2}, incl. seam-wrapping A:
  **72,864 checks, 0 mismatches**, and translation-by-3 accept counts
  **exactly equal** config-by-config at all three N; `B = Z_N` native
  BFS vs terminal-split union (N=11 σ=1, N=12 σ=0, three A each):
  **8,316 checks, 0 mismatches**; native cyclic vs explicit cut-order
  relabeling at two different cut points: **1,848 checks, 0 mismatches**.
  Total **170,724 exact reduction checks, zero failures**.
* **Unconditioning in action:** exact conditional probability
  (N=13, σ=1, |A|=2, p=m=4, k=1: 384/1716 = 0.2238) vs exact uniform
  (128/1024 = 0.1250): ratio 1.790 ≤ 3√13 = 10.82.  ✔ (Conditional
  exceeds uniform, as expected at N close to L, and sits far inside the
  pointwise S2 price.)
* **Rate battery (fresh seeds 250825xxx):** balanced split, offset 0:
  k=1: 1.33e−1 (L=16) → 5.06e−2 (32) → 1.07e−2 (64) → 7.5e−4 (128) →
  1.7e−5 (256); k=2: 2.56e−1 (32) → 1.15e−1 (64) → 3.27e−2 (128) →
  4.17e−3 (256); strictly monotone decay, no plateau, consistent with
  (much faster than) `exp(−cL^{1/5})`.  Offset attack (k=2, offsets
  0/1/2): off-2/off-0 ratio 0.677 (L=64), 0.731 (L=256) — a stable
  constant across a 30× probability drop: offsets move constants, not
  rates (S3's content), independently reproducing the prior audits'
  ~0.68.  Parity attack (k=1): off-1/off-0 = 1.30 (L=32), 1.42 (L=128)
  — the odd-offset start is FAVORED (the parity effect the prior audit
  recorded); harmless, a constant, and inside S3's uniform bound.
  Split attack (k=1, L=128): balanced 4.8e−4 ≫ quarter-split 1.0e−5 ≫
  eighth-split 0/100,000 ≫ one-sided 0/100,000 — the balanced split is
  the extremum, exactly the case S3 covers at its stated rate; skewed
  splits are tube-suppressed as predicted.  (The two independent
  balanced-split estimates at k=1, L=128 — 7.5e−4 and 4.8e−4 from
  disjoint seeds — bracket the rate within Poisson noise.)
* **k-boundary:** all tested (L,k) respect `k < L^{1/5}` only for k=1
  (L ≤ 242) and k=2 (L ≥ 33); tables outside that scope cannot refute SEG
  and were not counted as attacks.

**No counterexample.  No mismatch.  No anomalous regime.**

## 7. Paper-level slops and C/F instantiation

* All five FLSY slops recorded by the prior audits were re-verified
  against the page images and are real and repairable as described: the
  p.25 extraction over-quantification (false in general — e.g. no
  strictly increasing `(b_i)` of length `> r+1` exists — true for
  `Δ`-separated milestones); Lemma 4.5's `z ≤ n/2` vs its use at
  `z = c₃Δ²` on length-`c₃Δ²` blocks in 4.7 (repair: infinite-walk form,
  exactly [SUB]'s W1); Definition 4.1's `l, r ∈ [n]` vs Lemma 4.2's
  `r = n` endpoint; `log` vs `ln` in 4.7 (moot for SEG: at `Δ ≥ 352` both
  readings hold; and 4.7's own display closes under either base with its
  hypothesis read consistently); `≤` vs `<` at Theorem 4.4's threshold
  (does not arise in SEG: `d_F ≤ k < d` strictly).  None changes a
  load-bearing hypothesis; SEG's proof imports none of them unrepaired.
* Confirmed from my own reading of §4: **no segment/localized statement
  exists in the paper**; the proof of Theorem 4.4 uses Lemma 4.2's global
  anchoring exactly as the prior censuses record (3 bookkeeping uses + 1
  milestone base case, p.24 `z₀ := 0`).
* **Theorem C:** put `h=D+1`.  Among `q−5` middle
  states a common-label block has at least `⌈(q−5)/h⌉` states,
  hence at least `M=⌊(q−7)/h⌋` additions.  The earlier claim of
  the real number `L*=(q−7)/h` additions was false when
  `L*` is nonintegral.  For `L*≥2`,
  `M≥L*/2`.  Apply SEG with `N=q`, `σ=+1`,
  `k=2`, a proper cyclic endpoint, and segment length `M`;
  absorb `2^{1/5}` into the decay constant.  The displayed
  `tq⁴O(√q)` union budget has slack.
* **Theorem F:** long-run branch: SEG at `k = 2`, `L = ⌊n^{1/5}/7⌋` ⟹
  `k < L^{1/5} ⟺ n` beyond an absolute threshold, `L ≥ L₀` likewise;
  `B` proper (runs live in middle sizes), `σ = ±1` ✔.  Density branch:
  the mandate's `k ≈ (3/7)n^{1/5}` is `k = 5 + 3d`, `d = L+2`, i.e.
  `k = 11 + 3⌊n^{1/5}/7⌋`, applied to **published FLSY Theorem 4.4** on
  the cut order of `n−2` points (even ✔), and
  `11 + (3/7)n^{1/5} < (n−2)^{1/5}` holds for all `n` beyond an absolute
  threshold (`3/7 < 1`).  In the short-run branch, Lemma RS must
  cover all finite states: prepend size 2 to the first copy-2 middle run if
  necessary, use the co-singleton for size `q−2`, and use that
  sizes 1 and `q−1` are common.  The `L+2` defect bound
  survives.  Both branches instantiate inside the proven ranges.

## 8. Independently reconstructed proof skeleton (referee's own)

Recorded to establish non-endorsement-by-reading; formed from the primary
source before comparing with [SUB §D], then checked against it.

1. **Reduce to two offset walks (S1).**  Nested interval chains
   `A → B` = monotone lattice paths on the `(p+1)×(m+1)` grid of
   left/right extension counts; `f(D_{j,i}) = f(A) + λ(j) + ρ(i)` with
   `λ, ρ` partial sums on the two disjoint arcs of `B∖A`.  Cyclic case:
   any `c ∉ B` linearizes (nested intervals inside `B` never wrap);
   `B = Z_N`: for each of the `L` terminal splits,
   append the last point to one extension sequence so the two walk lengths
   total `L`; the actual staircase delays that coordinate step to
   its endpoint.
2. **Decouple the offset (S2 + independence).**  Price the global
   conditioning `f([N]) = σ` once, pointwise, at `3√N`; under uniform `g`
   the triple `(g(A), λ, ρ)` is independent; condition on `g(A) = σ'`
   (`|σ'| ≤ k < d`) to get two independent fresh walks with initial
   offset `σ'`, and the chain event inside `d_F(X, Y) ≤ k < d`.
3. **Milestones (W2 ← W1 upper).**  On the longer walk (`ℓ ≥ L/2`),
   `K = ⌊ℓ/(c₃Δ³)⌋` successive two-sided
   `⌈Δ⌉`-passages exist except with
   probability `≤ ℓ·2^{−Δ} ≤ e^{−Δ/6}` (`Δ = 3d ≥ 2 ln ℓ`; per-block
   escape via the first-passage upper bound; blocks independent).
4. **Order-preserving visit extraction.**  If `d_F < d`, minimal
   `α`-preimages of the milestone times force strictly increasing chaser
   times `b₁ < … < b_K ≤ r'` with integer discrepancy at most
   `⌊d⌋` (consecutive milestone gaps `≥⌈3d⌉`;
   `b₁ ≥ 1` because the offset `≤ d` keeps
   `h₀` outside the `d`-ball of `z₁`).
5. **i.i.d. first-passage domination.**  Stopping times `τ_i` (entry to
   the radius-`⌊d⌋` ball of `z_i`) satisfy
   `τ_i ≤ b_i ≤ r'`; each inter-arrival dominates a fresh
   `F_δ`, `δ=⌈d⌉`, because
   `⌈3d⌉−2⌊d⌋≥δ`.  Strong Markov and symmetry make the
   `K` variables exactly i.i.d. `F_δ`.  The offset's
   only role is the `i = 1` instance of the same invariant.
6. **Lower tail (W3 ← W1 lower).**
   `Pr[Σ_{i≤K}F_δ≤L/2]` is at most
   `exp(−c_lo²(Kδ)²/(8L))≤exp(−L^{1/5}c_lo²/(8·27648²))` (two-case
   `Kd ≥ L^{3/5}/27648`).  Total: `e^{−d/2} + e^{−Ω(L^{1/5})}` ⟹ S3;
   times `3√N` (and `(L+1)` where applicable) ⟹ Theorem S.

The skeleton uses FLSY's published probabilistic mechanism, but the segment
grid, offset base case, rounding, and cyclic-full encoding are repository
derivations.  The exact differences are R1--R4 above; R5 is final
bookkeeping.

## 9. Disposition

* Verdict: **SEG-SOUND-WITH-REPAIRS**.  R1--R5 are now folded into [SUB];
  the frozen statement, exact constants, and hypotheses are unchanged.
* With the later independent Sol check, SEG/C/F have status
  **ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED**.  C and F retain
  explicit dependency on SEG and incorporate their separate floor/RS
  wording repairs.
* SEG is not published verbatim.  FLSY supplies the probability engine;
  the localized segment, offset, rounding, and cyclic-full arguments are
  proved in this repository.

*Stop.*

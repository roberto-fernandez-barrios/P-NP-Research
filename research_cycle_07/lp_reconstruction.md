# Cycle 7 — independent reconstruction of the Jiang–Cai recombination LP

**Date:** 2026-08-25.  **Branch:** `cycle07-o18-fable`.
**Source being validated:** [JC26] = Jiang–Cai, *A Better Analysis For PPSZ
For 3-SAT*, arXiv:2607.10697v1 (frozen at
`frozen_sources/arxiv_src/a_better_analysis_for_ppsz_3_.tex`,
SHA-256 `ec1a4968…0cd9758`).
**Author of this reconstruction:** main-loop auditor (this document is a
from-scratch re-derivation from the frozen paper text; it uses no code or
prose from the authors' checker).

## 1. Frozen objects

Setting: `F` a 3-CNF (clauses of width at most 3) on `n` variables with
unique satisfying assignment normalized to all-ones.  For each variable
`x` one canonical critical clause `(x ∨ ¬y ∨ ¬z)` is chosen; arcs
`x→y`, `x→z` form the critical-clause graph.  `J_i` = variables of
indegree `i`; `TwoCC` = variables with at least two critical clauses;
`ID_i = J_i \ TwoCC` for `i ∈ {0,1}`.

Normalized coordinates (the LP variables):

    i_0 = |ID_0|/n,   i_1 = |ID_1|/n,   tau = |TwoCC|/n.

Imported analytic inputs (validity to be established by the import
ledgers, not here):

* (E-R) Regular estimate [JC26, Imported estimate 2.3; claimed source:
  Scheder TR21-069 rev 1, §7.8 final coefficient inequality]: for fixed
  `0 ≤ ε_R ≤ 0.13`, fixed `Thr > 0`, admissible finite strength `w`:
  `P[PPSZ_w(F)=α] ≥ 2^{−p0·n + gain_R − ξ_R(w)n − r_{R,w}(n)}` with

      gain_R ≥ (0.001687 ε_R − 0.006404 ε_R²)|H_low| + 0.9·Thr·|H_high|
               + (0.009307 − 0.055 ε_R − 0.1503 f_KL(ε_R))|TwoCC|
               − 1.1 ε_R Thr n,

  `f_KL(t) = (1−t)ln(1−t) + t` (natural log), `p0 = 2 ln 2 − 1`.
* (E-I) Irregular estimate [Imported estimate 2.4; claimed source §8.4
  final display]: for fixed `0 ≤ ε_I ≤ 1/5`, admissible `w`:
  `P[PPSZ_w(F)=α] ≥ 2^{−p0·n + gain_I − ξ_I(w)n − r_{I,w}(n)}` with

      gain_I ≥ b1(ε_I)|ID_1| + b0(ε_I)|ID_0| + bT(ε_I)|TwoCC|,
      b1(ε) = 0.030966ε − 0.0028ε² − 0.4027 f_KL(ε),
      b0(ε) = 0.06259ε − 0.344 f_KL(ε),
      bT(ε) = 0.009307 − 0.2405ε − 0.03125ε² − 0.06183 f_KL(5ε).

* (S-1) Sibling-graph inequality [claimed source Eq. (11)]:
  `(18/17)|H_low| + 2|H_high| + 3|TwoCC| ≥ |H|`.
* (S-2) Degree-two subgraph bound [claimed source Lemma 34 + A.3]:
  `|H| ≥ n − |J_1| − 2|J_0|`.

All four are used as black boxes; the reconstruction below is pure
algebra on top of them.

## 2. Elementary set inequality (re-proved)

`J_i = ID_i ∪ (J_i ∩ TwoCC)` disjointly, so

    |J_1| + 2|J_0| = |ID_1| + 2|ID_0| + |J_1∩TwoCC| + 2|J_0∩TwoCC|.

`J_0∩TwoCC` and `J_1∩TwoCC` are disjoint subsets of `TwoCC`, hence

    |J_1∩TwoCC| + 2|J_0∩TwoCC| ≤ 2(|J_0∩TwoCC| + |J_1∩TwoCC|) ≤ 2|TwoCC|.

With (S-2):

    (S-2')   |H| ≥ n − |ID_1| − 2|ID_0| − 2|TwoCC|.

Verified: identical to [JC26] eq. (11)→(12) chain.  Sound.

## 3. Derivation of the two affine bounds (re-derived)

Fix `ε_R` and set

    c_L = 0.001687 ε_R − 0.006404 ε_R²,
    c_T = 0.009307 − 0.055 ε_R − 0.1503 f_KL(ε_R),
    A   = (17/18) c_L   (so c_L = (18/17)A),
    Thr = 2A/0.9        (so 0.9·Thr = 2A; Thr > 0 requires A > 0),
    P_reg = 1.1 ε_R Thr = (22/9) ε_R A,
    S   = c_T − 5A.

Provided `A ≥ 0` (certified: `A ≈ 9.9758·10⁻⁵ > 0`), multiply (S-1) by
`A` and use it inside (E-R):

    gain_R ≥ (18/17)A|H_low| + 2A|H_high| + c_T|TwoCC| − P_reg·n
           ≥ A(|H| − 3|TwoCC|) + c_T|TwoCC| − P_reg·n          [by (S-1)]
           ≥ A(n − |ID_1| − 2|ID_0| − 2|TwoCC|) − 3A|TwoCC|
             + c_T|TwoCC| − P_reg·n                            [by (S-2')]
           = n·[ A(1 − i_1 − 2 i_0) − P_reg + S·tau ].

So `gain_R/n ≥ L_reg(i_0,i_1,tau) := A(1 − i_1 − 2i_0) − P_reg + S·tau`.
This reproduces [JC26] eq. (14)–(16) exactly, including the decomposition
of the `−5A` into `−3A` (from S-1) and `−2A` (from S-2').  The step needs
`A ≥ 0` twice (once per structural inequality) and nothing else.  Sound.

`gain_I/n ≥ L_irr(i_0,i_1,tau) := b0·i_0 + b1·i_1 + bT·tau` is (E-I)
divided by `n`.  Sound.

## 4. The LP, its feasible region, and the soundness direction

The recombination value is

    Γ = inf { max{L_reg(x), L_irr(x)} : x = (i_0,i_1,tau) ∈ R³, x ≥ 0 }.

**Frozen normalization.**  Variables are per-`n` densities; feasible
region is the closed nonnegative octant — deliberately a RELAXATION of
the true realizable set (real instances satisfy at least
`i_0 + i_1 + tau ≤ 1` and more).  Relaxing the feasible set can only
DECREASE `Γ`, and `Γ` is used as a LOWER bound on
`max{gain_R,gain_I}/n`; so the relaxation is in the sound direction.
Every uniquely satisfiable 3-CNF has some nonnegative `(i_0,i_1,tau)`,
and at that point `max{gain_R,gain_I}/n ≥ max{L_reg,L_irr} ≥ Γ`.  Sound.

**Dual certificate (re-derived).**  For any `λ ≥ 0` and any `x ≥ 0`:

    max{L_reg, L_irr} ≥ (λ L_reg + L_irr)/(1+λ)
      = [ λ(A−P_reg) + (b0−2λA) i_0 + (b1−λA) i_1 + (bT+λS) tau ] / (1+λ).

If `b0 − 2λA ≥ 0`, `b1 − λA ≥ 0`, `bT + λS ≥ 0`, then
`Γ ≥ λ(A−P_reg)/(1+λ)`.  With `λ = b1/A` (so the `i_1` coefficient
vanishes identically), the conditions reduce to `b0 − 2b1 ≥ 0` and
`A·bT + b1·S ≥ 0` (multiplying by `A > 0`), and

    Γ ≥ γ* := b1(A − P_reg)/(A + b1).

Both margins are certified strictly positive
(`b0 − 2b1 ≈ 1.34097·10⁻³`, `bT + (b1/A)S ≈ 1.38537·10⁻²`).
This reproduces [JC26] Proposition 3.1 + eq. (22)–(24).  Sound.

## 5. Location of the optimum — verified from first principles

Mandate item: verify the optimum sits at the corner
`i_0 = 0, tau = 0, i_1 > 0`, not merely by trusting the certificate.

Certified signs: `A > P_reg > 0`, `S > 0`, `b0 > b1 > 0`, `bT < 0`.

*Attainment.*  At `x* = (0, i_1*, 0)` with `i_1* = (A−P_reg)/(A+b1)`:

    L_reg(x*) = A(1 − i_1*) − P_reg
              = (A − P_reg) − A·(A−P_reg)/(A+b1)
              = (A−P_reg)·(1 − A/(A+b1)) = b1(A−P_reg)/(A+b1) = γ*,
    L_irr(x*) = b1·i_1* = b1(A−P_reg)/(A+b1) = γ*.

So `max{L_reg,L_irr}(x*) = γ*`, matching the dual bound: **zero duality
gap; `Γ = γ*` exactly and the infimum is attained at `x*`.**
`i_1* > 0` because `A > P_reg`; and `i_1* < 1` because `b1 > −P_reg`.

*Optimality and uniqueness of the corner.*  `Φ = max{L_reg, L_irr}` is a
maximum of two affine functions, hence convex; any local minimum on the
convex feasible set is global.  At `x*` both branches are active.  The
subdifferential of `Φ` at `x*` is the convex hull of the two gradients

    ∇L_reg = (−2A, −A, S),      ∇L_irr = (b0, b1, bT).

With weights `(y_R, y_I) = (λ,1)/(1+λ)`, `λ = b1/A`, the convex
combination is

    ( (b0 − 2b1)/(1+λ),  0,  (bT + λS)/(1+λ) )  ≥  (>0, 0, >0).

A point of a convex program over the nonnegative octant is optimal iff
some subgradient `g` satisfies `g ≥ 0` on coordinates at their lower
bound 0 and `g = 0` on free coordinates.  Here `i_0 = tau = 0` carry
strictly positive subgradient components (`0.00134…/(1+λ)` and
`0.01385…/(1+λ)`), and the free coordinate `i_1` carries exactly `0`.
So `x*` is optimal, and moreover:

* strict positivity on the `i_0` and `tau` components means every
  optimal point has `i_0 = tau = 0` (moving either up strictly increases
  `Φ` to first order and, by convexity, globally);
* on the ray `{(0,t,0)}`, `Φ(t) = max{A(1−t)−P_reg, b1 t}` is strictly
  decreasing then strictly increasing with unique minimizer `t = i_1*`.

**Conclusion: the optimum is exactly the singleton
`(i_0, i_1, tau) = (0, 0.060043244708778326…, 0)`, with strictly
positive dual slacks on the `i_0` and `tau` constraints (margins
`b0−2b1` and `bT+λS` up to the positive factor `1/(1+λ)`).**  This
confirms the [JC26] claim and the Cycle-6 reconnaissance independently.

Interpretation for Stage I: the binding structure is the tradeoff
between the regular bound (decreasing in `i_1`) and the irregular bound
(increasing in `i_1`) on the `i_1`-axis; `i_0` and `tau` are slack.  A
new valid constraint improves `Γ` iff it excludes `x*` from the feasible
region (together with a neighborhood of it along the descent
directions).

## 6. Hostile pass over the paper's own (non-imported) proof steps

* **Prop. 3.1 (dual certificate).**  Pure algebra; re-derived above.  SOUND.
* **Combination of the two estimates** (proof of Thm 3.2):
  `log₂P ≥ −p0 n + max{gain_R − e_R, gain_I − e_I}
        ≥ −p0 n + max{gain_R, gain_I} − max{e_R, e_I}` with
  `e_X = ξ_X(w)n + r_{X,w}(n) ≥ 0`.  Valid since
  `max{a−c, b−d} ≥ max{a,b} − max{c,d}` for `c,d ≥ 0`.  Requires both
  estimates to bound the SAME probability for the SAME instance
  simultaneously — an import-layer fact (ledger item I7).  Conditionally
  SOUND.
* **Finite-strength bookkeeping** (Thm 3.2): `Δ = γ* − γ_new ≈
  8.046·10⁻¹¹ > 0` certified; `w0` with `ξ < Δ/4`, then `n0` with
  `r < Δn/4`; total error `< Δn/2`; `γ* − Δ/2 = (γ*+γ_new)/2 > γ_new`.
  Quantifier order (fix target exponent → fix `w` → let `n → ∞`) is
  coherent; the fixed-`w` linear error `ξ(w)n` is never hidden in
  `o(n)`.  SOUND, conditional on the imported error structure
  (`ξ_X(w) → 0`, `r_{X,w}(n) = o(n)` per fixed `w`) — ledger items
  I2(vi)/I3(vi).
* **Monotonicity in `w`** (end of Thm 3.2 proof): along the unique
  satisfying assignment the residual formula after any prefix is
  determined by the prefix set alone (all retained values are `α`'s), so
  the forced set at each step is monotone in `w`; hence
  `#guesses(π)` is pointwise nonincreasing in `w` and
  `P[PPSZ_w(F)=α] = E_π 2^{−#guesses(π)}` is nondecreasing in `w`.
  SOUND (this argument re-derived here; the paper asserts it in one
  line).
* **Lemma C.1 (liquid restriction).**  Re-derived: for `β ⊇ α|_L`
  satisfying `F`, the first `π`-disagreement `x` between `β` and `α`
  would be liquid when processed (both completions witness the two
  values), so `x ∈ L`, contradicting agreement on `L`.  SOUND, modulo
  the SS definition of "liquid" = both values extendable to satisfying
  assignments of the current residual (ledger item L7).
* **Lemma C.2 (prefix realization).**  Re-derived: `P[A_R] = 1/C(n,r)`;
  soundness of the implication heuristic forces prefix-inferred values
  to equal `α` (inductively, `α` satisfies the residual as long as the
  partial assignment agrees with `α`); at most `r` unbiased prefix
  guesses give factor `≥ 2^{−r}`; prefix decisions are measurable in the
  prefix order and prefix bits, so conditioned on `A_R`, the prefix
  order, and prefix success, the suffix is a fresh uniform-order
  `PPSZ_w` run on `F|_{α|_R}` (relative suffix order uniform; unused
  bits fresh).  SOUND.  The padding step (extend `ρ` to exactly `r`
  variables along the unique residual solution) preserves unique
  satisfiability.  SOUND.
* **Branch arithmetic of Prop. 4.2.**  Large-I branch:
  `−p_w n + q_w δn = −p0 n + (q0δ − ε_w(1−δ))n` — checked, exact.
  Unique-residual branch: `C(n,r) ≤ 2^{n h2(r/n)}` (standard), exponent
  `−h2(δ_n) − δ_n − p0(1−δ_n) + γ(1−δ_n) = −p0 + u_γ(δ_n)` — checked,
  exact; `δ_n = ⌊δn⌋/n ≤ δ` and `u_γ` decreasing, so the continuity
  step is even conservative.  `E_Q[I] < δn` gives a support point
  `I ≤ ⌊δn⌋` by integrality — checked.  SOUND modulo the two SS imports
  (Thm 4.1 = SS 1.17; `p_w = p0 + ε_w` with `ε_w → 0` = ledger L3) and
  the "3-CNF = width ≤ 3, closed under restrictions" convention
  (ledger).
* **Root/branch analysis (§4).**  `q0δ` strictly increasing;
  `u_γ' = −γ − (1−p0) − h2'(δ) < 0` on `(0,1/2)` where
  `h2'(δ) = log₂((1−δ)/δ) > 0`; `u_γ(0) = γ > 0 = q0·0` and
  `u_γ(1/2) < 0 < q0/2`, so the crossing exists, is unique, and
  `η_∞(γ) = q0 δ_γ`.  Root-equation algebra
  (`q0δ = u_γ(δ) ⟺ h2(δ) + (1−p*+γ)δ = γ`, using `1−p0+q0 = 1−p*`)
  — checked, exact.  Monotonicity in `γ` (implicit differentiation) —
  checked; also implied directly since `u_γ` is pointwise increasing in
  `γ`.  SOUND.
* **Lemma A.1 (`ε_I ≤ 1/5` admissibility).**  Derivatives re-computed
  from the quoted Definition-67 densities:
  `γ_ID' = 20r(1−2r)(1−4r) = 10x(1−x)(1−2x)` for `x = 2r` (max abs
  `≈ 0.962 < 5/2`); `γ_pID' = (61/6)r²(1−2r)(3−10r)
  = (61/24)x²(1−x)(3−5x)` (max abs `≈ 0.135·(61/24) ≈ 0.346 < 61/54`);
  `γ_TwoCC' = 20r²(3−8r) ≥ −5` on `[0,1/2]` (minimum at `r = 1/2`).
  Lower bound `−5/2 − 2·61/54 = −257/54 > −5`; density
  `1 + ε_I γ' ≥ 0` iff `ε_I ≤ 1/5` against the worst case `−5`.
  Internally SOUND (bounds are loose but valid); external validity
  hangs on Definition 67 and the combination pattern `−a φ_ID + m φ_pID`
  (`a ∈ {0,1}`, `m ∈ {0,1,2}`) being faithful to the source — ledger
  item I3(viii).

## 7. What this reconstruction does NOT establish

* The truth of (E-R), (E-I), (S-1), (S-2) — Scheder import ledger.
* SS Main Theorem 1.17, Lifting 1.18, `p_w = p0 + ε_w` — SS ledger.
* The numeric enclosures — the two exact-rational checkers (authors' and
  independent).
* The frontier/novelty framing ("best currently known") — novelty audit.

## 8. Anomalies noted so far (running list)

1. Certificate JSON in the artifact repository is version
   `2026-07-12-rational-v5`; the paper's Appendix B claims
   `2026-07-12-rational-v6`.  No v6 file is public.
2. The repo README lists `REVISION_NOTES.md` with a SHA-256, but the
   file is absent from the repository (head commit `3e732e0`).
3. The checker file is committed under the name
   `verify_ppsz_constants(1) (1).py` (upload artifact name); its bytes
   hash to exactly the README's checksum for `verify_ppsz_constants.py`.
None of these three affects the mathematics; all three are provenance
defects to report.

# Independent Exact-Rational Certificate Check — Report

**Target:** Tao Jiang, Shaowei Cai, *A Better Analysis For PPSZ For 3-SAT*, arXiv:2607.10697v1.
**Audit stance:** hostile validation; arms-length replication. Every claim treated as potentially wrong.
**Date of run:** 2026-08-25 (deterministic; the transcript contains no timestamps).
**Deliverables (this directory):**

| file | role |
|---|---|
| `independent_checker.py` | from-scratch exact-rational interval checker (Python 3 stdlib only) |
| `independent_checker_output.txt` | transcript of the complete run (90 sub-checks) |
| `independent_checker_report.md` | this report |

**How to reproduce:** `python independent_checker.py` (Python 3.13; runtime ≈ 0.6 s).
**Exit code of the recorded run: 1 — deliberate.** The checker exits nonzero iff any checked claim fails; exactly one paper claim is genuinely false (Finding F1, Section 5). All 89 other sub-checks PASS, including every piece of arithmetic that the paper's *new* results depend on.

---

## 1. Verdict at a glance

* **Certificate arithmetic for the new results (Theorem 1.2, Corollary 1.3): fully replicated. PASS.**
  All coefficients, dual margins, γ\*, the tight corner, both root brackets, both lifted bonuses, both branch margins at δ₀, and all five running-time-base inequalities are certified with enclosures whose width is ≤ 2.6·10⁻⁷³ (except the data-limited η quantities, Section 7).
* **One exact refutation (FINDING F1):** the terminal inequality of the paper's eq. (2) — the *historical* re-derivation of Scheder's old bonus γ_old = 1/15218 — is false by exactly 43/258659105733 ≈ 1.66·10⁻¹⁰. The displayed pair of estimates supports only the smaller constant 31273/475913718 = 1/(15218 + 1204/31273); the clean bound derivable from eq. (1) is ≥ 1/15219. This does **not** touch the paper's new results (impact analysis in Section 5.3).
* **Provenance flags (not arithmetic failures):** JSON/paper certificate-version mismatch (v5 vs v6), an equation-numbering discrepancy in the audit brief, and three JSON-only thresholds (Section 6).

---

## 2. Independence statement

Only two inputs were read:

1. `frozen_sources/arxiv_src/a_better_analysis_for_ppsz_3_.tex` (frozen paper source; all formulas were transcribed from it by hand, with tex line numbers cited in the checker's comments), and
2. `frozen_sources/ppsz_certificate.json` (pure data).

The authors' checker `frozen_sources/verify_ppsz_constants.py` and its transcript `frozen_sources/verification_output.txt` were **not** read, opened, grepped, or accessed in any way; neither were the authors' rerun transcript, README, or the Scheder / Scheder–Steinberger PDFs also present in `frozen_sources` (the last point matters for Finding F1 attribution, Section 5.4). All algorithmic choices — series depths (120/100 vs the authors' stated 90/90), the 2⁻²⁵⁶ outward-rounding scheme, tail bounds, check structure — are our own.

Exactness policy: every proof-relevant number is a `fractions.Fraction`; no float appears in any load-bearing computation (the `Iv` constructor and the JSON loader actively reject floats; a source scan confirms every decimal literal in the program is inside a string). `limit_denominator` is never used. The run is deterministic and performs no search: the root brackets are taken as given data, and range reduction by exact powers of two is bounded normalization, not search.

---

## 3. Method and self-derived error bounds

### 3.1 Interval arithmetic

Closed intervals [lo, hi] with exact rational endpoints. Sums, differences, products (min/max of the four endpoint products) and quotients (min/max of the four endpoint quotients; divisor certified to exclude 0) are the standard sound endpoint formulas, computed exactly. Strict claims `X > c` are certified as `X.lo > c`, `X < c` as `X.hi < c`; a comparison whose truth is not decided by the enclosure would be reported as a failure, never resolved by assumption. (At the chosen depths every comparison resolved on the first run; no depth tuning was needed or performed.)

### 3.2 Outward rounding (soundness)

After each transcendental enclosure, endpoints are rounded outward to denominator 2²⁵⁶:
lo → ⌊lo·2²⁵⁶⌋/2²⁵⁶ ≤ lo and hi → ⌈hi·2²⁵⁶⌉/2²⁵⁶ ≥ hi.
The rounded interval is a **superset** of the original, and any superset of an enclosure is an enclosure — soundness is preserved unconditionally; the width grows by < 2·2⁻²⁵⁶ ≈ 1.7·10⁻⁷⁷ per rounding. This keeps all denominators bounded (the raw series values have denominators with thousands of digits) while remaining far below every margin in the certificate (smallest margin ≈ 4.2·10⁻¹⁴).

### 3.3 Logarithm — atanh series with proved tail (own derivation)

For rational y with 1 ≤ y ≤ 2 put z = (y−1)/(y+1) ∈ [0, 1/3]. Then (1+z)/(1−z) = y, so

  ln y = 2·atanh z = 2·Σ_{j≥0} z^{2j+1}/(2j+1).

Let S_N = 2·Σ_{j=0}^{N−1} z^{2j+1}/(2j+1) and R_N = ln y − S_N.

* **Lower bound:** every omitted term is ≥ 0, hence R_N ≥ 0.
* **Upper bound (geometric domination):** for j ≥ N,
  z^{2j+1}/(2j+1) ≤ z^{2j+1}/(2N+1) = (z^{2N+1}/(2N+1))·(z²)^{j−N},
  and Σ_{k≥0} (z²)^k = 1/(1−z²) since z² < 1. Therefore

  0 ≤ R_N ≤ 2·z^{2N+1} / ((2N+1)·(1−z²)).  ∎

So ln y ∈ [S_N, S_N + 2z^{2N+1}/((2N+1)(1−z²))], all quantities exact rationals.

**Range reduction.** For arbitrary rational x > 0, exact halvings/doublings maintain the invariant ln x = ln r + k·ln 2 and terminate with r ∈ [1, 2), k ∈ ℤ; ln 2 itself is the case y = 2, z = 1/3. This is exactly what tiny arguments need (e.g. δ ≈ 3.4·10⁻⁶ reduces with k = −19): ln(m·2^k) = ln m + k·ln 2 with k·[ln 2 enclosure] formed by exact interval scaling. Interval arguments use monotonicity: ln [a,b] ⊆ [ln_lo(a), ln_hi(b)].

**Depth:** N = 120 ⇒ tail ≤ 2·(1/3)²⁴¹/(241·(8/9)) < 10⁻¹¹⁵, so the 2⁻²⁵⁶ rounding dominates every width.

### 3.4 Exponential — positive Taylor series with proved tail (own derivation)

For rational x with 0 ≤ x < N+1:

  exp x = Σ_{j≥0} x^j/j!, S_N = Σ_{j=0}^{N−1} x^j/j!, R_N = exp x − S_N ≥ 0.

For j ≥ N, x^j/j! = (x^N/N!)·x^{j−N}/((N+1)(N+2)⋯j) ≤ (x^N/N!)·(x/(N+1))^{j−N}, since each factor N+1,…,j is ≥ N+1. Summing the geometric series (ratio x/(N+1) < 1):

  0 ≤ R_N ≤ (x^N/N!) / (1 − x/(N+1)).  ∎

So exp x ∈ [S_N, S_N + (x^N/N!)/(1 − x/(N+1))]. Negative arguments via exp x = 1/exp(−x) with outward reciprocal ([c,d] ∋ exp(−x), c > 0 ⇒ exp x ∈ [1/d, 1/c]); intervals via monotonicity. **Depth:** N = 100; the largest argument used is |t·ln 2| ≤ 0.27, giving tails ≪ 10⁻¹⁵⁰.

### 3.5 Derived functions

log₂x = ln x / ln 2 (outward interval division); 2^t = exp(t·ln 2); f_KL(t) = (1−t)·ln(1−t) + t (**natural** log; tex lines 210–213); h₂(d) = −d·log₂d − (1−d)·log₂(1−d) (**binary** log; tex 516–519); p₀ = 2ln2 − 1; p\* = 1 − 1/(2ln2); q₀ = p₀ − p\*.

### 3.6 Plumbing self-tests

Before any paper check, the run verifies textbook constants (ln 2, e, ln 10, √2 to 26+ digits) and exact identities (ln 3 + ln 5 ∋ ln 15, h₂(1/2) ∋ 1, e⁻¹·e ∋ 1, (2^{1/2})² ∋ 2), and that all core widths are < 10⁻⁷⁰. A failure aborts with exit 2 (implementation bug — distinct from a refuted paper claim). All passed.

---

## 4. What was verified (90 sub-checks) — results and margins

All enclosures below are certified two-sided intervals; the transcript prints 30 significant digits of every endpoint. "exact" = width 0 (pure rational arithmetic).

### Checks 1–3: parameters and coefficients

* ε_R = 0.1024756190168075228998451658 and ε_I = 0.07307238160252154687451293138 parse exactly; JSON = paper `eq:parameter-values` (**01a–01b PASS**); admissibility ε_R ≤ 0.13, ε_I ≤ 1/5 (**01c**); γ_new consistent across JSON fields and paper (**01d**); 26 shared literals JSON↔paper all equal as exact rationals (**01e**).
* c_L, A, Thr, P_reg are **exact rationals** (polynomials in ε_R):
  A = 9.97582178549107508119194827694·10⁻⁵, P_reg = 2.49890303097001597806119835647·10⁻⁵.
* c_T, S, b0, b1, bT enclosed with widths ≤ 2.6·10⁻⁷⁷:
  S = 2.35445147822041139237…·10⁻³, b1 = 1.14549739595903309354…·10⁻³, b0 = 3.63196877285601397166…·10⁻³, bT = −1.31818020145823793042…·10⁻².

### Check 4: sign pattern (PASS)

A > 0, P_reg > 0, S > 0, b0 > 0, b1 > 0, bT < 0, and **A − P_reg = 7.47691875452105910313074992047·10⁻⁵ exactly** (matches the paper's 0.00007476918754521059…).

### Check 5: dual margins (PASS)

* b0 − 2b1 = 1.34097398093794778458…·10⁻³ > 0 (paper: 0.00134097398093794778…).
* Product form A·bT + b1·S = 1.38202496012236695418…·10⁻⁶ > 0 (division-free, as specified).
* Division form bT + (b1/A)·S = 1.38537454842306473932…·10⁻² > 0 (paper: 0.01385374548423064739…); λ = b1/A = 11.4827371678296700112… ∈ JSON's [11.4827371678, 11.4827371679].

### Checks 6–7: γ\* and the tight corner (PASS)

* γ\* = b1(A−P_reg)/(A+b1) = 6.87793804588365655035…·10⁻⁵ > γ_new;
  **γ\* − γ_new = 8.04588365655035494349…·10⁻¹¹** (paper: 8.045883656550355·10⁻¹¹ — agrees to all printed digits).
* i₁ = (A−P_reg)/(A+b1) = 6.00432447087783266273…·10⁻² ∈ (0,1) strictly (hence i₀+i₁+τ = i₁ < 1).
* **Symbolic corner identity (own derivation):** with i₀ = τ = 0,
  L_irr = b1·i₁ = b1(A−P_reg)/(A+b1) = γ\* by definition, and
  L_reg = A(1−i₁) − P_reg = (A−P_reg) − A(A−P_reg)/(A+b1) = (A−P_reg)(1 − A/(A+b1)) = (A−P_reg)·b1/(A+b1) = γ\*. ∎
  Numerically: the independent interval evaluations give L_reg − γ\* and L_irr − γ\* both ⊂ [−8.64·10⁻⁷⁸, +8.64·10⁻⁷⁸] ∋ 0.

### Checks 8, 10, 15, 16: the four strict base inequalities (all PASS, strict)

| quantity | certified enclosure (30 digits in transcript) | threshold | margin |
|---|---|---|---|
| 2^(p₀−γ_new) | 1.30696959751624698244591485362…3 | < 1.306969598 | 4.83753017554·10⁻¹⁰ |
| 2^(p₀−1/15218) | 1.30697237656515325941127755593…4 | < 1.306972376566 | 8.46740588722·10⁻¹³ |
| 2^(p₀−0.000000364) | 1.30703157793120525344360860676…7 | < 1.307031578 | 6.87947465563·10⁻¹¹ |
| 2^(p₀−0.0000003465837065) | 1.30703159370976209827300656342…3 | < 1.307031593710 | 2.37901726993·10⁻¹³ |
| 2^(p₀−0.0000003640269421) | 1.30703157790679664699705621718…9 | < 1.307031577907 | 2.03353002943·10⁻¹³ |

Check 16 justification (own): t ↦ 2^(p₀−t) is strictly decreasing, and the true η_∞ exceeds the lower end of its certified interval; hence 2^(p₀−η_lo) upper-bounds the true limiting base, and we certify 2^(p₀−η_lo) < threshold. Also certified: new limiting base < safe theorem base < old limiting base (16e). Bonus: 2^{p₀} = 1.30703190770259900010… (paper prefix 1.3070319… confirmed).

### Check 9: Scheder's one-dimensional endgame — **FINDING F1** (see Section 5)

Exact rational arithmetic, no series: crossing x\* = 7192790/79318953, minimax v = 31273/475913718; 09d **FAIL** (v < 1/15218); corrected bound v ≥ 1/15219 certified (09g, margin 3341/804770097138 ≈ 4.15·10⁻⁹); impact guard 2^(p₀−v) = 1.30697237671575588853… < 1.306972377 certified (09h, margin 2.84·10⁻¹⁰).

### Check 11: p\* and q₀ (PASS)

p\* = 0.278652479555518296320037659499…500 (target 0.27865247955551829632 ✓),
q₀ = 0.107641881564372322514426583417…418 (target 0.10764188156437232251 ✓; paper prefix 0.107641881564372 ✓); q₀ > 0 and p\* < 1 certified; plumbing identity q₀ = 2ln2 − 2 + 1/(2ln2) confirmed by intersection.

### Check 12: root brackets (PASS)

g_γ(d) = h₂(d) + (1−p\*+γ)d − γ:

| point | certified g enclosure | sign |
|---|---|---|
| γ_old, d = 0.00000321978491531273261 | [−9.5644921009968253424·10⁻²³, −9.5644…228·10⁻²³] | < 0 ✓ |
| γ_old, d = 0.00000321978491531273262 | [+9.4015207370927611261·10⁻²³, +9.4015…445·10⁻²³] | > 0 ✓ |
| γ_new, d = 0.00000338183369577144614 | [−1.1776323288047999666·10⁻²², −1.1776…748·10⁻²²] | < 0 ✓ |
| γ_new, d = 0.00000338183369577144615 | [+7.1188509861847326103·10⁻²³, +7.1188…769·10⁻²³] | > 0 ✓ |

(Enclosure widths ≈ 5·10⁻⁷⁷ against endpoint values ≈ 10⁻²² — sign certification has ~54 spare orders of magnitude.)

**Uniqueness argument (as required):** h₂′(d) = log₂((1−d)/d), so g′(d) = log₂((1−d)/d) + 1 − p\* + γ. On (0, 1/2], log₂((1−d)/d) ≥ 0, and 1 − p\* + γ > 0 because p\* < 1 (certified, check 11c) and γ > 0. Hence g′ > 0, g is strictly increasing on (0, 1/2], and the certified sign change proves there is exactly one root δ_γ in (0, 1/2], lying inside the bracket. ∎

### Check 13: lifted bonuses (PASS)

Since q₀ > 0 and δ_γ lies in its bracket, η_∞(γ) = q₀·δ_γ ∈ q₀·[bracket]:

* η_old ∈ [3.46583706516845732042·10⁻⁷, 3.46583706516845733119·10⁻⁷] ⊂ [0.0000003465837065, 0.0000003465837066] ✓ (ours strictly inside the paper interval)
* η_new ∈ [3.64026942150633545839·10⁻⁷, 3.64026942150633546917·10⁻⁷] ⊂ [0.0000003640269421, 0.0000003640269422] ✓
* η_new > η_old strict; gap = 1.744323563378781…·10⁻⁸ (paper: 0.0000000174432356… ✓)
* η_new/η_old − 1 = 0.0503290700220495871445…935 > 0.0503 (margin 2.90700220495·10⁻⁵) ✓

### Check 14: branch margins at δ₀ = 338183369/10¹⁴ (PASS)

* q₀·δ₀ − η_safe = 2.69415293842239828333…·10⁻¹¹ > 2.69·10⁻¹¹ (margin 4.15293842239·10⁻¹⁴; paper 2.6941529384·10⁻¹¹ ✓)
* u_{γ_new}(δ₀) − η_safe = 2.70505818649784988536…·10⁻¹¹ > 2.70·10⁻¹¹ (margin 5.05818649784·10⁻¹⁴; paper 2.7050581864·10⁻¹¹ ✓), where u_γ(d) = γ(1−d) − (1−p₀)d − h₂(d) and u_{γ_new}(δ₀) = 3.64027050581864978498…·10⁻⁷.

### Check 17: γ_new − γ_old (PASS, exact)

γ_new − 1/15218 = 233416937/76090000000000 = 3.06764275200420554606…·10⁻⁶ > 0 (paper: 0.0000030676427520042… ✓); γ_new/γ_old − 1 = 233416937/5000000000 = 0.0466833874 exactly > 0.04668 ✓.

### Check 18: JSON `reported_intervals` (PASS; version string printed)

All nine two-sided entries (A, P_reg, S, b1, b0, bT, lambda, gamma_star, tight_i1): **our enclosure strictly inside the JSON interval** (nonempty intersection trivially satisfied; containment relation "ours inside theirs" in every case). One-sided `safe_branch_margin_lower` = 2.69·10⁻¹¹: both branch margins certified ≥ it. JSON version string printed: `2026-07-12-rational-v5`.

### Check 19 (bonus): second data point

At Scheder's parameters (ε_R, ε_I) = (0.1, 0.029), the same pipeline gives γ\* = 6.57190847632252457647…·10⁻⁵, matching the paper's Appendix A value 0.000065719084… (tex line 702), with all certificate side conditions holding — an independent end-to-end validation of every formula in checks 2–6. Also certified: γ\*(ε_R, ε_I) > γ\*(0.1, 0.029).

---

## 5. FINDING F1 — the terminal inequality of eq. (2) is false (by 1.66·10⁻¹⁰)

### 5.1 The claim (tex lines 63–78)

Eq. (1) (`eq:old-endgame-inputs`): gain_R ≥ |H|/10118 − n/41391, gain_I ≥ (|J₁|+2|J₀|)/1380. With irr = (|J₁|+2|J₀|)/n and |H|/n ≥ 1−irr, eq. (2) (`eq:old-endgame`) displays

  (1/n)·max{gain_R, gain_I} ≥ max{ (1−irr)/10118 − 1/41391, irr/1380 } **≥ 1/15218**,

and the paper continues: "Thus Scheder's published unique-case bonus is γ_old = 1/15218".

### 5.2 The exact refutation

f(irr) = (1−irr)/10118 − 1/41391 is strictly decreasing, g(irr) = irr/1380 strictly increasing, f(0) > 0 = g(0), f(1) < 0 < g(1), so over irr ∈ [0,1] the minimax of max{f, g} is attained exactly at the crossing:

* crossing: **x\* = 7192790/79318953** = 0.0906818575883118376512…, with f(x\*) = g(x\*) verified as an exact rational identity;
* minimax value: **v = x\*/1380 = 31273/475913718** = 0.0000657114910060230707617…;
* **1/v = 15218 + 1204/31273 = 15218.03849966… > 15218**, hence **v < 1/15218**;
* shortfall: **1/15218 − v = 43/258659105733 = 1.66241972723692189353·10⁻¹⁰** exactly.

Hand re-derivation (independent of the code): 31273·15218 = 475,912,514 < 475,913,718; the difference is 1,204; 1204/4 = 301 = 7·43 and (475913718·15218)/28 = 258,659,105,733 — confirming the reduced fraction 43/258659105733.

So the displayed max dips below 1/15218 for irr near x\* (both branches there equal v ≈ 1/15218.0385). The largest integer D with minimax ≥ 1/D is D = 15219; check 09g certifies **v ≥ 1/15219** with exact margin 3341/804770097138 ≈ 4.15·10⁻⁹. In other words, the constant 15218 appears to have been obtained by rounding 1/v = 15218.0385 **down**, which is the unsound direction for a denominator.

### 5.3 Impact analysis

* **The paper's new results are unaffected.** Theorem 1.2 (γ_new = 0.0000687793 via the dual certificate), the tight corner, the lifting computation for γ_new, Corollary 1.3 (general 3-SAT base 1.307031578), and every certified enclosure in checks 2–8 and 11–16 make no use of eq. (2). They all PASS here.
* **The comparison claims survive — and would strengthen.** γ_new > 1/15218 > v, so "γ_new > γ_old" holds a fortiori under the corrected γ_old′ = v (gap grows from 3.0676·10⁻⁶ to ≈ 3.0678·10⁻⁶). Likewise η and base comparisons.
* **What is actually wrong:** (i) the terminal "≥ 1/15218" of eq. (2) as an algebraic consequence of eq. (1); (ii) consequently the framing "Thus Scheder's published unique-case bonus is γ_old = 1/15218" as *derived from the displayed pair*, and the associated unrounded old-base display 1.306972376565153… (which is 2^(p₀−1/15218), correctly computed *from the constant* — check 10 — but the constant itself overshoots what eq. (1) supports). Under the corrected constant the old unique base becomes 2^(p₀−v) = 1.30697237671575588853… (certified, 09h).
* **Scheder's rounded published base survives:** 2^(p₀−v) < 1.306972377 certified with margin 2.84·10⁻¹⁰ (09h), so the abstract-level claim "Scheder's analysis: O\*(1.306972377ⁿ)" remains valid even under the correction. The second decimal in the abstract's old general-case row (1.307031594) is likewise safe: the corrected old lifted bonus would be *smaller* than η_old, making the old general base *larger*, i.e. the paper's new-vs-old improvement direction is preserved and slightly amplified.
* **Downstream conditional checks remain valid as computations:** checks 10, 12 (old bracket), 13 (η_old), 16 (old base) verify statements *about the constant 1/15218* and are internally correct; they inherit the caveat that the constant itself is not supported by eq. (1) as displayed.

### 5.4 Attribution caveat

Whether the unsound rounding originates in Scheder's own final simplification (ECCC TR21-069 rev. 1, Section 6 / Theorems 35–36, per the paper's Appendix A provenance table) or in Jiang–Cai's transcription of it cannot be adjudicated here: Scheder's papers are outside this checker's allowed inputs (Section 2). What is established exactly is that *the chain as displayed in this paper* does not support 1/15218. Note the paper's own γ_new derivation deliberately does *not* reuse the eq. (2) simplification — the authors describe it as the step their method replaces.

---

## 6. Provenance observations (flagged, not arithmetic failures)

1. **Certificate-version mismatch (real provenance observation).** The frozen JSON says
   `"version": "2026-07-12-rational-v5"` (ppsz_certificate.json, line 2), while the paper's Appendix B says: "The certificate version is `2026-07-12-rational-v6`." (tex line 720). The shipped data file therefore does not carry the version string the paper names. All 26 shared numerical literals in the JSON nevertheless agree exactly with the paper (check 01e), so the discrepancy looks like a stale version stamp rather than divergent data — but under a hostile audit it means the artifact named by the paper is not bit-identical to the artifact shipped.
2. **Equation numbering in the audit brief.** The brief calls the parameter display "eq. (13)". In the frozen v1 source, counting numbered displays, `\label{eq:parameter-values}` compiles as eq. (20); eq. (13) is `\label{eq:Rlinear}`. The check was performed against `\label{eq:parameter-values}` (the display containing ε_R, ε_I), which is unambiguous.
3. **JSON-only thresholds.** `old_unique_base_upper = 1.306972376566`, `relative_improvement_lower = 0.0503`, and `unique_relative_improvement_lower = 0.04668` do not appear in the tex; all three are nevertheless verified true here (checks 10a, 13e, 17c). Conversely `safe_branch_margin_lower = 2.69e-11` *does* correspond to the paper's "both limiting branches exceed η by more than 2.69·10⁻¹¹" (tex line 626) and is certified (18j).
4. **Series depths.** JSON `series: {log_terms: 90, exp_terms: 90}` matches Appendix B's "uses N = 90 for both series". (This checker independently uses 120/100 and proves its own tails; the authors' N is reported, not relied on.)

---

## 7. Precision statement (what "≥ 20 significant digits" means here)

* Every quantity determined by exact point inputs (all coefficients, margins, γ\*, i₁, p\*, q₀, all g-values, all 2^x bases, both branch margins at δ₀) is enclosed with **relative width ≤ 10⁻⁶⁵** — endpoints agree to ≥ 65 significant digits, far beyond the required 20. Purely rational quantities (A, P_reg, A−P_reg, Thr, c_L, everything in checks 9 and 17) are **exact** (width 0).
* The η quantities are **data-limited**: η_∞(γ) is only known through the certificate's root bracket of width 10⁻²³, so η_old, η_new have width ≈ 1.1·10⁻²⁴ (≈ 17–18 significant digits of agreement), and their difference/ratio ≈ 15–16 digits. No arithmetic can narrow these without tightening the brackets themselves (which would be search, excluded by design). Our added slack beyond the propagated input width is < 10⁻⁷⁴. Every strict comparison involving them resolves with margins ≥ 2.9·10⁻⁵ (ratio) and ≥ 1.7·10⁻⁸ (gap).

---

## 8. What this audit does NOT cover

This is **arithmetic-layer verification only**. Explicitly outside scope (imported by the paper as published, per its Appendix A provenance table):

* the two **imported Scheder estimates** — the regular bound (Imported estimate 2.2 / eq. (5), from SchederFull §7.8) and the irregular bound (Imported estimate 2.3 / eqs. (6)–(9), from §8.4) — including the integrals and auxiliary numerics behind their coefficients (0.001687, 0.009307, 0.030966, …);
* the two **imported structural inequalities** — (18/17)|H_low| + 2|H_high| + 3|TwoCC| ≥ |H| (eq. (10), SchederFull eq. (11)) and |H| ≥ n − |J₁| − 2|J₀| (SchederFull Lemma 34), hence eq. (11);
* the **Scheder–Steinberger theorem** (Main Theorem 1.17 / Lifting Theorem 1.18) and the change-of-measure inequality (eq. (4));
* **all probabilistic semantics**: PPSZ correctness, the finite-strength error model p_w = p₀ + ε_w, the liquid-set restriction lemma, the prefix-realization/conditioning argument (Appendix C), the admissibility calculus in Appendix A's Lemma, and any claim that the analyzed quantities describe the algorithm.

What IS covered: every numerical definition, inequality, enclosure, bracket, margin, and running-time base in Sections 1, 3, 4 and Appendix B, plus the JSON data file, re-derived from scratch in exact rational interval arithmetic.

---

## 9. Complete discrepancy list

| # | severity | item |
|---|---|---|
| F1 | **refuted claim** | eq. (2) terminal "≥ 1/15218": exact minimax of the displayed pair is 31273/475913718 = 1/(15218+1204/31273), short by 43/258659105733 ≈ 1.66·10⁻¹⁰; correct clean constant from eq. (1) is 1/15219. New results unaffected; Scheder's rounded base survives (Section 5). |
| P1 | provenance | JSON version `2026-07-12-rational-v5` ≠ paper Appendix B `2026-07-12-rational-v6` (quotes in Section 6.1). |
| P2 | provenance (brief) | audit brief's "eq. (13)" is eq. (20) in the frozen source (Section 6.2). |
| P3 | provenance (minor) | three JSON thresholds absent from the tex (all verified true; Section 6.3). |

No other discrepancy of any size was found: every one of the paper's printed decimals cross-checked (22 reference decimals) agrees with our independent enclosures to every printed digit, and all nine JSON `reported_intervals` strictly contain our tighter enclosures.

---

## 10. Conclusion

The numerical certificate underlying the paper's **new** claims — γ_new = 0.0000687793, unique base < 1.306969598, lifted bonus η = 0.000000364, general base < 1.307031578, and all comparisons against the old analysis — **replicates exactly** under a from-scratch, float-free, exact-rational interval checker with self-derived error bounds; the tightest certified margin is 4.15·10⁻¹⁴ (high-branch margin over 2.69·10⁻¹¹) and all enclosure widths are ≤ 2.6·10⁻⁷³ (data-limited η's aside). The single genuine defect found is the historical eq. (2) chain for Scheder's old constant 1/15218, refuted exactly (F1) with a fully quantified, headline-preserving impact; plus the v5/v6 version-stamp mismatch. The recorded run exits 1 solely to signal F1, as the audit specification requires.

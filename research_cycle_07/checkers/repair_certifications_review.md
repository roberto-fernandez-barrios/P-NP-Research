# Hostile adversarial review of `repair_certifications.py`

* **Date:** 2026-08-26 (review commissioned 2026-08-25)
* **Reviewer stance:** assume wrong until proven right; every identity re-derived independently; every certified number cross-checked by an independent float pipeline built from the *source* definitions in r-space (not the script's t-substitution); certifier probed white-box with seeded negatives.
* **Files reviewed:**
  * `C:\Users\masteria.DOMINE\rf\P-NP-Research\research_cycle_07\checkers\repair_certifications.py` (the script; NOT modified)
  * `C:\Users\masteria.DOMINE\rf\P-NP-Research\research_cycle_07\checkers\repair_certifications_output.txt` (stored output)
  * `C:\Users\masteria.DOMINE\rf\P-NP-Research\research_cycle_07\frozen_sources\scheder_extracts.md`
  * `C:\Users\masteria.DOMINE\rf\P-NP-Research\research_cycle_07\frozen_sources\scheder_tr21069_rev1.pdf` — pages read directly: 24–27, 38, 46–47, 51, 55, 77–80
* **Independent tooling:** `xcheck.py` (session scratchpad), pure `math`/`fractions`, no dependency on the script's code except verbatim copies of the certifier functions for white-box probing.

---

## VERDICT: SOUND WITH CAVEATS

No broken certificate, no unsound inference direction, no wrong-way inequality was found anywhere in the script. Every exact result was independently reproduced (four integrals re-derived fully by hand; nine more by high-resolution Simpson quadrature; all four C.12 claims re-checked on 10^5-point grids from the source's r-space definitions; the d = 161 margin reproduced to 7 significant digits). The rerun is byte-identical to the stored output (Python 3.13.12, exit 0).

The caveats (Section "Issues found", items C1–C4) are **certificate-coverage gaps and latent-robustness issues, not errors**: three side-conditions the script *uses* without *certifying* (all verified true here with large margins), plus one documented inherited-trust boundary. None invalidates any PASS line.

---

## R1. The t-substitution algebra — **CONFIRMED** (independent derivations)

Substitution: t = sqrt(1−2r), t ∈ [0,1] ⇔ r ∈ [0,1/2]; r = (1−t²)/2, 1−r = (1+t²)/2, 1−2r = t², dt/dr = −1/t.

1. **γ = (1−t²)t³/2**: γ(r) = r(1−2r)^{3/2} = ((1−t²)/2)·(t²)^{3/2} = (1−t²)t³/2 (t ≥ 0). ✔
2. **φ = γ′ = t(5t²−3)/2**: γ′(r) = (1−2r)^{3/2} + r·(3/2)(1−2r)^{1/2}·(−2) = √(1−2r)·[(1−2r)−3r] = √(1−2r)(1−5r); in t: 1−5r = (5t²−3)/2, so φ = t(5t²−3)/2. ✔ (matches source p. 24, eq. (12) remark)
3. **2γ/(1−r) = 2(1−t²)t³/(1+t²)**: [(1−t²)t³]·[2/(1+t²)] directly. ✔
4. **γ/(1−r) − φ = t(3−7t⁴)/(2(1+t²))**: numerator over 2(1+t²): 2(1−t²)t² − (5t²−3)(1+t²) = 2t²−2t⁴−5t²−5t⁴+3+3t² = 3−7t⁴. ✔
5. **δ_max compact form vs. (13)/(14)/(16)** (source p. 27 verified visually):
   δ_root = 1.2εγ·max(0,−φ), δ_non-root = 1.2εγ²/(1−r).
   δ_nr + δ_root = 1.2εγ[γ/(1−r) + max(0,−φ)] = 1.2εγ·max(γ/(1−r), γ/(1−r)−φ), so
   max(2δ_nr, δ_nr+δ_root) = 1.2εγ·max(2γ/(1−r), γ/(1−r), γ/(1−r)−φ), and the middle entry is dominated by the first because γ ≥ 0, 1−r > 0. Hence = 1.2εγ·max(2γ/(1−r), γ/(1−r)−φ), which is exactly (16). **φ ≥ 0 case checked explicitly:** then δ_root = 0, max = 2δ_nr = 1.2εγ·2γ/(1−r), and the compact form also selects 2γ/(1−r) since 2γ/(1−r) ≥ γ/(1−r) ≥ γ/(1−r)−φ. ✔ Both constructions agree numerically everywhere (fuzz max dev 8.7e−19).
6. **δ_max = 0.3ε(1−t²)t⁴K(t)/(1+t²)**, K = max(4(1−t²)t², 3−7t⁴): both max-entries share the nonnegative factor t/(2(1+t²)) (entry 1: 2(1−t²)t³/(1+t²) = [t/(2(1+t²))]·4(1−t²)t²; entry 2 from item 4), which pulls out of the max; 1.2·(1/2)·(1/2) = 0.3. ✔
7. **η = δ_max/(1−r) = 0.6ε(1−t²)t⁴K/(1+t²)²**: divide by (1+t²)/2. ✔
8. **s′(r) = 1 − η′(r) = 1 + (1/t)dη/dt** since dη/dr = (dη/dt)(dt/dr) = −(1/t)dη/dt. ✔ Fuzzed against finite differences (max dev 6e−12).
9. **"s′ ≤ 1.05 ⇔ dη/dt ≤ 0.05t per smooth piece"**: for t > 0 multiply by t > 0 (equivalence); at t = 0 both sides vanish (η has a t⁴ factor), and s′ → 1 < 1.05. ✔
10. **Piece structure**: K = 3−7t⁴ ⇔ q(t) := 3t⁴+4t²−3 ≤ 0 ⇔ t ≤ t0 (q strictly increasing on [0,1], q(0) = −3, q(1) = 4). t0² = (√13−2)/3, i.e. r_kink = (5−√13)/6 ≈ 0.23241 — **exactly the kink point the source names on p. 78**. Script's 40-step bisection bracket [0.731562545848, 0.731562545849] confirmed (t0 = 0.7315625458…). Piece-1 certificates run on [0, T0HI] ⊇ [0,t0], piece-2 on [T0LO, 1] ⊇ [t0,1]: sound overlapping cover of the kink. ✔

## R2. Reduction of the four C.12 claims to polynomial nonnegativity — **CONFIRMED** (independent derivations)

Source proof structure read directly from pp. 77–78; the script's four claims + range facts are exactly the proof's ingredients (claim 1 = the 0.95 display, claim f ≥ 0.98f(s), claim s′ ≤ 1.05, claim g ≥ 0.945g(s), plus s ∈ [0,1/2] for the FTC substitution and 0.95·0.98/1.05 ≥ 0.88, 0.945/1.05 = 0.9).

* **Claim 1 (A2)**: 2δ_max(1−r) ≤ 0.05r(1−2r). In t: LHS = 0.3ε(1−t²)t⁴K, RHS = 0.025(1−t²)t². Dividing by 0.025(1−t²)t² > 0 on (0,1) gives **12εt²K ≤ 1**; at t ∈ {0,1} the original holds as 0 ≤ 0, and the certified form is *stronger*, so certifying `1 − 12εt²K ≥ 0` implies the claim on all of [0,1]. ✔ Direction sound. (Side finding: max t²K = 2/√7 at t = 7^{−1/4} (piece 1), so claim 1 is true iff ε ≤ √7/24 ≈ 0.110243; eps_R ≈ 0.102476 sits ~7% below the cliff — "hairline but true" is real.)
* **Claim 2 (A3)**: with SD = ED = (1+t²)², SN := s·SD = (1−t²)ED/2 − EN (verified: SN/SD ≡ s, fuzz dev < 1e−15): f(r) = 2t²(1−t²)/SD (= FN/FD, FN = 2t²(1−t²), FD = SD ✔), and from s = SN/SD: 1−2s = (SD−2SN)/SD, 1−s = (SD−SN)/SD, hence **f(s) = SN(SD−2SN)/(SD−SN)²** ✔. Then f(r) − 0.98f(s) = N3/[SD·(SD−SN)²] with **N3 = FN(SD−SN)² − 0.98·SN(SD−2SN)·SD** — matches the code (0.98 = 49/50). **Denominator-clearing positivity**: SD ≥ 1 trivially; SD−SN > 0 *strictly* because SD−SN = ED(1+t²)/2 + EN ≥ 1/2 once EN ≥ 0, which follows from certified A1A (K ≥ 0). So N3 ≥ 0 ⇔ claim 2. ✔ (Identity fuzzed: dev < 5e−16.)
* **Claim 4 (A5)**: g(r) = 8t⁴/GD, GD = (1+t²)³ ✔; **g(s) = (SD−2SN)²·SD/(SD−SN)³** (from the same s-fractions; re-derived) ✔; multiplying by GD(SD−SN)³ > 0 gives **N5 = 8t⁴(SD−SN)³ − 0.945(SD−2SN)²·SD·GD ≥ 0** ⇔ claim 4 (0.945 = 189/200 ✔). The odd power (SD−SN)³ makes strict positivity of SD−SN load-bearing — covered as above. ✔ (Fuzz dev < 7e−16.)
* **Claim 3 (A4)**: η = EN/ED with EN, ED polynomials in t (per piece), so **dη/dt = (EN′ED − EN·ED′)/ED²** is the quotient rule — yes, this is really dη/dt on each smooth piece. dη/dt ≤ 0.05t ⇔ **N4 = 0.05t·ED² − (EN′ED − EN·ED′) ≥ 0** (multiply by ED² > 0). ✔ Verified numerically: s′(r) − 1.05 = −N4/(t·ED²) to 4e−11 against an *independently derived* r-space piecewise formula for s′ (branch condition φ + γ/(1−r) ≤ 0 for the K1 branch).
* **Range facts**: s ≥ 0 (A1B via SN ≥ 0, SD > 0), s ≤ 1/2 (A3b via SD−2SN = t²[ED + 1.2ε(1−t²)t²K] ≥ 0), η ≥ 0 (A1A) — these are exactly what the source's chain needs (r·s^{d−1} ≥ s^d for MLB; f(s), g(s) ≥ 0; image of s in [0,1/2]). The endpoint identities s(0) = 0, s(1/2) = 1/2 needed by the FTC substitution hold *identically* because EN carries the factors (1−t²)t⁴ (verified by inspection; see nit N5).
* **Constant chain**: 0.95·0.98/1.05 = 133/150 = 0.88666… ≥ 0.88 and 0.945/1.05 = 9/10 exactly — both verified as exact fractions. ✔
* **A-REFUTE (ε = 0.13)**: valid. The witness t = 1126106135847/2748779069440 ≈ 0.409675 lies strictly inside piece 1 (< T0LO < t0), where η is smooth with the K1 formula; N4 < 0 there exactly ⇒ s′(r) = 1.05 + 1.135199e−2 at r ≈ 0.416083. Independently reproduced: s′ = 1.061351988 (float, r-space formula). This refutes the source's printed "s′(r) ≤ 1.05 … provided ε ≤ 0.13" (p. 78). Grid scan shows max s′(0.13) = 1.06207 at r ≈ 0.4254 — the script's witness need not be the maximizer and isn't; it only needs one violation. ✔

## R3. The bisection certifier — **CONFIRMED**

* **`pieval` is a genuine enclosure**: interval Horner with exact-corner products of exact rationals; by induction each step encloses the partial Horner value for every t in [lo,hi] (interval multiplication treats the two t-dependences as independent — over-approximates, never under-approximates). Fuzz-tested: 500 random polynomials × 60 sample points, 0 violations.
* **PASS direction is the sound one**: a PASS requires vlo ≥ 0 on every leaf; since the enclosure contains the true value, no polynomial that is negative anywhere in [a,b] can pass (its leaf would have vlo ≤ p(t*) < 0). The factoring uses only "Q ≥ 0 on [a,b] ⊆ [0,1] ⇒ P = t^j(1−t)^m·Q ≥ 0 on [a,b]" — the valid direction. The converse failure mode (Q < 0 only at an endpoint zero of the monomial factors) could at worst cause an honest false FAIL, never a false PASS; and a refutation of Q at any point spills by continuity to a genuine violation of P ≥ 0.
* **Refutations honest**: interval-refute (vhi < 0 ⇒ p < 0 on the whole subinterval) and exact-point-refute (p(mid) < 0, exact rational arithmetic) are both valid.
* **FAIL/INCONCLUSIVE honest**: node-budget exhaustion and width < 2^−60 both report False → FAILURES → exit 1. White-box probes: interior tangency (t−1/3)²(t+1) → INCONCLUSIVE (never falsely certified); (t−1/4)(t−3/4) → REFUTED; t − 10^−20 (negative only on a boundary sliver) → INCONCLUSIVE, not certified; `factor_t`/`factor_one_minus_t` round-trip t²(1−t)³(2+t) exactly (synthetic-division recurrence h_{i−1} = h_i − q_i re-derived and confirmed; the internal `assert` makes any inconsistency a crash, not a silent pass).
* **Non-vacuity (mutation test)**: the A2 polynomial rebuilt at ε = 0.111 — just past claim 1's true threshold √7/24 ≈ 0.110243 — is **correctly REFUTED** by the copied certifier. The pipeline is not a rubber stamp.
* **Kink handled soundly**: piece-1 certified on [0, T0HI], piece-2 on [T0LO, 1], overlapping the exact-rational bracket that provably contains t0 (bisection invariant q(lo) < 0 ≤ q(hi), q strictly increasing). Since each piece's formula is certified on a *superset* of where it is active, and s is continuous piecewise-C¹, the claims transfer to the max/min-composite η, s, s′ (one-sided derivatives at the kink both bounded ⇒ 1.05-Lipschitz-above, which is what the C.12 integral argument uses).

## R4. The closed-form integral engine — **CONFIRMED**

* `to_x_poly`: r = 1−x by Horner-style basis build — correct; **direction/sign**: ∫₀^{1/2} h(r)dr = ∫_{1/2}^1 h(1−x)dx (dr = −dx swaps the orientation that the flipped bounds restore) — correct.
* `integral_poly_over_xpow` cases over [1/2, 1]: m ≥ 0 and m ≤ −2 share the antiderivative x^{m+1}/(m+1) and the code's single expression `(1 − (1/2)^{m+1})/(m+1)` is correct for both (Fraction negative powers give (1/2)^{m+1} = 2^{−(m+1)}); m = −1 contributes exactly ln 2 = ln 1 − ln(1/2). ✔
* **Hand-derived spot checks (full antiderivative computations, independent of the engine):**
  1. `L55` = ∫₀^{1/2} r²(1−2r)⁵/(1−r)⁴ dr: expanding (1−x)²(2x−1)⁵ = −1+12x−61x²+170x³−280x⁴+272x⁵−144x⁶+32x⁷ and integrating over [1/2,1] gives F(1)−F(1/2) = −386/3 − (−65/6 − 170ln2) = **−707/6 + 170 ln 2** — exactly the script's value; = 0.00168736… ≥ 0.001687 (margin 3.6e−7, genuinely hairline, certified exactly). **CONFIRMED.**
  2. ∫₀^{1/2} φ_TwoCC² dr = ∫(60r²−160r³)² = 720r⁵ − 3200r⁶ + 25600r⁷/7 at 1/2 = 22.5 − 50 + 200/7 = **15/14**. **CONFIRMED.**
  3. (bonus) BFS = −20∫(r³−6r⁴+8r⁵)/(1−r)² dr = −20(79/6 − 19ln2) = **380 ln 2 − 790/3**. **CONFIRMED.**
  4. (bonus) I_ocb(4) = ∫₀^{1/2} r⁵(1−2r)/(1−r)² dr = **7 ln 2 − 4657/960**, so OCB*(4) = 0.88·I(4) = 0.000869965583 — matches the script to all printed digits.
* Nine further integrals matched against Simpson quadrature at n = 2^15 (table below), max deviation 2.8e−12 (quadrature-limited). The integrand transcriptions match Definition 68 (p. 47) verbatim given Q_r = r²/(1−r)² and P_r = r/(1−r) — both forms confirmed *from the source itself* (P_r printed on p. 51; Q′_r = 2r/(1−r)³ printed on p. 80; the exact match of five independent printed closed forms is further mutual corroboration).

## R5. The B-part logic — **CONFIRMED**

* **OCB\*(d) = 0.88·∫₀^{1/2} f(r)r^d dr with f = r(1−2r)/(1−r)²**: f·r^d = r^{d+1}(1−2r)/(1−r)² = `I_ocb(d)`'s integrand ✔; **MLB\*(d) = 0.9·∫ g(r)r^d dr**, g = (1−2r)²/(1−r)³ = `J_mlb(d)` ✔ — both match Prop. C.12's display (p. 77) verbatim; 0.88 = 22/25, 0.9 = 9/10 exact.
* d ≤ 4 checks and Thr: OCB*(4) − 1/1150 = **+4.0e−7** (the hairline is real and certified in exact rationals; enclosure width ~1e−62 is negligible against it). Thr_JC = 2A/0.9 ≈ 2.2168e−4 and Thr_Scheder = 2/(0.9·10118) ≈ 2.1963e−4, both ≤ 1/1150 ≈ 8.696e−4 ✔ (this is the "hidden Thr constraint" of C.13(2), and both choices comply comfortably).
* d-sweep 5..161: enclosure arithmetic on (rational, ln2-coeff) pairs is sound; the ln2 coefficients stay small (≤ ~d+3) so the enclosure width (~1e−61) cannot mask the 1e−53-scale margins. Float Simpson reproduces the worst absolute margin at d = 161 as 1.045712e−53 — **agreement to 7 significant digits** — and shows the worst *relative* margin is at d = 5 (10.5%), all positive.
* **g ≤ f/2 on [0.45, 1/2] ⇔ r²−5r+2 ≤ 0 — re-derived**: g ≤ f/2 ⇔ 2(1−2r)(1−r)² ≤ r(1−r)(1−2r)·… more precisely multiply by 2(1−r)³ > 0 and cancel (1−2r) ≥ 0 (the r = 1/2 case is 0 ≤ 0): 2(1−2r) ≤ r(1−r) ⇔ r²−5r+2 ≤ 0. ✔ Convex quadratic ⇒ max at endpoints; −(r²−5r+2) at 0.45 and 0.5 is 19/400, 1/4 > 0 ✔ (script's endpoint values exact). Float grid: max(g − f/2) = −1e−5 < 0 ✔.
* **g ≤ 1 on [0,1/2]**: (1−r)³ − (1−2r)² = r(1−r−r²) — expansion re-derived ✔, and 1−r−r² ≥ 1/4 on [0,1/2] certified by bisection ✔. (Used for ∫₀^θ g r^d ≤ θ^{d+1}/(d+1) on p. 79.)
* **((d−1)/(d+1))^d ≥ 1/10**: exact rational powers for d = 2..20 ✔ (min = 1/9 at d = 2); for d ≥ 21: (d+1)/(d−1) = 1+u, u = 2/(d−1), and (1+u)^d ≤ e^{ud} (since ln(1+u) ≤ u) ⇒ **((d−1)/(d+1))^d ≥ e^{−2d/(d−1)}** — direction re-derived and correct; 2d/(d−1) = 2 + 2/(d−1) ≤ 2.1 ⇔ d ≥ 21 exactly ✔; e^{−x} decreasing ⇒ ≥ e^{−2.1}, whose certified *lower* bound 0.122456 ≥ 1/10 ✔. (The script's route avoids relying on the source's unproved "increases in d" remark — good.)
* **r_min ≥ 0.45 for d ≥ 19**: (d−1)/(2(d+1)) ≥ 9/20 ⇔ 10(d−1) ≥ 9(d+1) ⇔ d ≥ 19 — exact algebra ✔.
* **E(162) ≤ 1/10 and ratio**: E(d) = (9/10)^d(9/16)(d+3)³ is exactly the p. 79 bound (2θ)^d·5θ(d+3)³/4 at θ = 0.45 (re-derived, including r_max−r_min = 2/((d+1)(d+3)) and the (2/(d+3))²·(1/10)·2^{−d} chain). E(162) = 0.097692 ≤ 0.1 exact ✔; E(d+1)/E(d) = (9/10)((d+4)/(d+3))³ ≤ (9/10)(166/165)³ = 0.916463 < 1 for d ≥ 162 (ratio decreasing in d) ⇒ E(d) ≤ 1/10 for all d ≥ 162 by induction ✔. The final p. 79 arithmetic 0.9·(11/10)·(1/2) = 0.495 ≤ 1/(2·0.88)·0.88 = 0.5 closes the chain ✔.

## R6. ln2/exp enclosures — **CONFIRMED**

* `ln2_interval`: ln 2 = 2·atanh(1/3); after the loop p = z^{2N+1} exactly; dropped terms 2z^{2j+1}/(2j+1) (j ≥ N) are positive and termwise ≤ 2z^{2N+1}z^{2(j−N)}/(2N+1), so 0 ≤ tail ≤ 2z^{2N+1}/((2N+1)(1−z²)) — geometric domination valid (z² = 1/9 < 1). Enclosure [s, s+tail] ∋ ln 2, width 4.93e−64 at N = 64 (order confirmed by hand: 2·3^{−129}·(9/8)/129).
* `exp_lower/upper`: partial Taylor sum is a lower bound for x ≥ 0; the tail after N terms is ≤ (first dropped term)·Σ(x/(N+2))^i = term·x/(N+1)/(1 − x/(N+2)), valid for x < 1 (asserted). `exp_neg_interval`: e^{−x} via reciprocal (1/upper ≤ e^{−y} ≤ 1/lower, positive) and k-fold squaring of a positive interval — directions correct; for x = 2.1: k = 2, y = 0.525 < 1 ✔.
* `ln_pos_interval` (Part E): range-reduce to y ∈ [1,2] with x = y·2^k; atanh series for ln y has z = (y−1)/(y+1) ∈ [0,1/3] so the same tail bound applies; the k·ln2 term uses LN2[0]/LN2[1] swapped by the sign of k — directed rounding correct in both directions. `fkl_interval`: (1−tv) > 0 multiplies the ln-interval monotonically; endpoint pairing correct.

## R7. Part D and Part E logic — **CONFIRMED, two caveats (C1, C2)**

* **2(r−1/4)² identity**: 2(r−1/4)² = 2r² − r + 1/8 = 1/8 − r(1−2r) — exact ✔; hence max r(1−2r) = 1/8 (attained at r = 1/4), max γ_ID = 10·(1/8)² = **10/64** (float grid: 0.156250 exactly). The source's p. 51 "γ_ID ≤ 10/256" is **false** (10/64 at r = 1/4), read directly from the PDF; with the printed requirement εγ_ID ≤ 1/60 the corrected constraint is ε ≤ (1/60)/(10/64) = **64/600** ≈ 0.10667 — the script's version is the *corrected, more restrictive* one, and eps_I ≈ 0.07307 complies with margin ✔. 5·eps_I ≤ 1, eps_I ≤ 4/5 (Lemma 73's condition), eps_I < 1/5 all exact ✔.
* **φ_TwoCC + 5 = (1/2 − r)(160r² + 20r + 10)**: expansion re-derived: RHS = 5 + 60r² − 160r³ = LHS ✔; both factors ≥ 0 on [0,1/2] ⇒ φ_TwoCC ≥ −5, tight at r = 1/2 (φ_TwoCC(1/2) = −5 exactly, so a bisection could not have certified this; the exact factorization is the right tool). |φ_ID| ≤ 5/2 and |φ_pID| ≤ 61/54 certified via (bound² − φ²) ≥ 0 — sound square trick; float ranges (max|φ_ID| = 0.962, max|φ_pID| = 0.345) show the bounds are comfortably true. **Caveat C2**: (36) needs |φ_TwoCC| ≤ 5, i.e. also φ_TwoCC ≤ 5 — true (max = 5/4 at r = 1/4) but **not certified** by the script.
* **c_T_min = A(5 + |bT|/b1) — re-derived from the dual-feasibility condition**: A·bT + b1·S > 0 with S = c_T − 5A ⇔ b1·c_T > 5A·b1 − A·bT ⇔ (divide by b1 > 0) c_T > A(5 − bT/b1) = A(5 + |bT|/b1) **when bT ≤ 0**. ✔ The reduction is valid **only under b1 > 0, bT ≤ 0, A > 0** — see Caveat C1: the script never asserts these. All three verified independently: b1 = +0.001145497, bT = −0.013181802, A = +9.9758e−5, and the interval widths (~1e−60, from f_KL enclosures only) cannot straddle 0. Direct evaluation of the raw condition: A·bT + b1(c_T − 5A) = +1.382e−6 > 0 = b1·margin ✔ (consistency).
* **Worst-case interval endpoints**: c_T's lower endpoint uses the *upper* f_KL endpoint (0.1503·fk_hi subtracted) ✔; b1's lower endpoint likewise ✔; |bT|'s upper endpoint = −bT_lo ✔ (valid given bT < 0); c_T_min's upper bound uses largest |bT| over smallest b1 with exact positive A ✔. margin = c_T_lo − cTmin_hi — the conservative pairing ✔. Coefficients 0.1503 ≥ 5/(48ln2) and 0.006404 ≥ 0.0064 are the printed final-display replacements, both in the gain-decreasing (safe) direction, consistent with the frozen extract's note on p. 45. Margin 0.001206 covers the 3.6e−5 recon degradation 33.5×, reproduced exactly in floats.

## R8. Execution + independent numerical cross-check — **CONFIRMED**

Re-run: Python 3.13.12, ~4s, exit code 0, output **byte-identical** to `repair_certifications_output.txt` except the elapsed-time line.

Independent float pipeline (r-space, source definitions, 10^5-point grids, Simpson n = 2^15; no code shared with the script):

| Item | Script (exact) | Independent (float) | Agree |
|---|---|---|---|
| C.12 claim 1 @ eps_R, min slack | certified ≥ 0 (poly, both pieces) | +2.4999e−07 (min at grid edge r→0; interior healthy) | ✔ |
| C.12 claim 2 @ eps_R, min slack | certified ≥ 0 | +1.0001e−07 (r→0 edge) | ✔ |
| C.12 claim 3 @ eps_R | s′ ≤ 1.05 certified | max s′ = 1.0489267 @ r = 0.42541 | ✔ (margin 0.0011 — hairline, real) |
| C.12 claim 4 @ eps_R, min slack | certified ≥ 0 | +4.4e−11 (r→1/2 structural zero, factored t⁴) | ✔ |
| C.12 all four @ ε = 0.1 | certified | all hold; max s′ = 1.0477448 | ✔ |
| s′-claim @ ε = 0.13 | REFUTED, witness s′ = 1.05 + 1.135199e−2 | witness reproduced: 1.061351988; grid max 1.0620682 @ r = 0.4254 (claims 1,2,4 also fail at 0.13) | ✔ |
| OCB*(0..4), MLB*(0..4) | e.g. OCB*(4) = 0.000869965583 | all 10 match to ≤ 5e−13; hand-exact I(4) = 7ln2 − 4657/960 | ✔ |
| OCB*(4) − 1/1150 | ~4.00e−7 > 0 | +4.0037e−07 | ✔ |
| d-sweep 5..161 | all ≥ 0; worst abs margin d=161: 1.045712e−53 | 0 negatives; d=161 margin 1.045712e−53; worst relative margin d=5 (10.5%) | ✔ |
| BFS | 380ln2 − 790/3 = 0.062595279446 | Simpson dev 1.2e−14; hand-derived exactly | ✔ |
| BFS − DFB | 0.030966519315 ≥ 0.030966 | 0.030966519315 | ✔ |
| JUNK2 | 2.030441e−4 > 1.84e−4 (printed bound FALSE) | 2.0304414e−04 (Simpson of the defining integral) | ✔ |
| JUNK1 + 2·JUNK2 | 0.002742008 ≤ 0.0028 | 0.002742008 | ✔ |
| ∫φ_ID², ∫φ_pID², ∫φ_TwoCC² | 5/21, 3721/181440, 15/14 | Simpson devs ≤ 2e−15; 15/14 hand-derived | ✔ |
| KL ratios | ≤ 0.4027 / 0.344 / 0.06183 | 0.402672852 / 0.343498819 / 0.061829787 | ✔ (0.06183 has margin 2e−7 — hairline, certified with directed rounding) |
| L55 | −707/6 + 170ln2 ≥ 0.001687 | 0.001687361857; hand-derived exactly | ✔ |
| 8.3 printed-form decimals | 0.009307639 / 0.240474134 / 0.029297276 | same | ✔ |
| Thr_JC, Thr_S | 2.216849286e−4, 2.196305814e−4 | identical | ✔ |
| E(162), ratio, exp(−2.1) | 0.097692, 0.916463010, ≥ 0.122456 | 0.097692, 0.916463010, 0.122456 | ✔ |
| Part E: c_T, c_T_min, margin | 0.002853243, 0.001646758, 0.001206485 | identical to printed precision; b1 > 0 and bT < 0 confirmed | ✔ |

## Issues found

**BROKEN: none.** Every PASS line in the output is backed by a valid certificate whose logical direction I verified.

**Caveats (should be addressed or at least acknowledged in Stage V):**

* **C1 (Part E — unchecked sign preconditions).** `cTmin_hi = A_val*(5 + absbT[1]/b1i[0])` and `absbT = (-bTi[1], -bTi[0])` are valid *only if* b1 > 0, bT ≤ 0 (and A > 0). The script computes these but never asserts them; if a future re-tune made b1i[0] ≤ 0 or bTi[1] > 0, the formula would silently produce an unsound (too small) c_T_min and a spurious PASS. Currently harmless: b1 = +1.1455e−3, bT = −1.3182e−2, A = +9.9758e−5, with enclosure widths ~1e−60 (no straddle possible). One `report(...)` line asserting `b1i[0] > 0 and bTi[1] < 0` would close it.
* **C2 (Part D vs. (36)).** The script certifies φ_TwoCC ≥ −5 only. Equation (36) rests on |φ_TwoCC| ≤ 5 (source p. 55: "−5 … is its maximal absolute value"), which also needs φ_TwoCC ≤ 5 on [0,1/2]. That upper side is trivially true (max = 5/4 at r = 1/4; verified) but is not among the certificates. (The −5 side is the tight one — equality at r = 1/2 — and it *is* the certified one.)
* **C3 (Part C — inherited-trust boundary, documented).** The Section-8.3 constants (Bonus2CC = 104/3 − 50ln2, DFS2CC+DFD2CC = 15347/3 − 7380ln2, JUNK2CC = 17923400/7 − 3694000ln2) are certified only *relative to the printed closed forms*; B(r) and the 8.3 integrals are not re-derived. The script's header and comments say so explicitly ("closed forms taken as printed; B(r) not re-derived"). Any Stage-V verdict should carry this dependency forward explicitly.
* **C4 (Part C — uncertified source-side claim in the (37) chain).** p. 55's "One checks that Ψ_{1,2} ≤ Ψ_{1,1} ≤ Ψ_{1,0}" (needed for (34), hence for (37)'s |ID_{0,1}| coefficient) is not certified by the script. Verified true here numerically: Ψ_{1,0} = 0.238095, Ψ_{1,1} = 0.137572, Ψ_{1,2} = 0.078064. An exact certificate would be cheap (the Ψ's are polynomial integrals).

**Nits (no action strictly required):**

* **N1.** The B1 report label "endpoints of concave-up −(r²−5r+2)" misstates the shape (−(r²−5r+2) is concave *down*); the argument actually printed and used — r²−5r+2 convex ⇒ max at endpoints ⇒ min of its negation at endpoints — is correct, as are the endpoint values 19/400 and 1/4.
* **N2.** A3a's label says "1−s > 0" but the bisection certifies only ≥ 0. The strict positivity that denominator-clearing needs follows from SD−SN = ED(1+t²)/2 + EN ≥ 1/2 given A1A (EN ≥ 0) — true and cheap, but the label overstates the certificate itself.
* **N3.** The script's comment justifying the printed 3721/90720 ("(I_y+I_z)² ≤ 2(I_y+I_z) over 0/1/2-valued indicators") paraphrases the source differently from the actual p. 55 mechanism (Ψ_{0,j} = j²Ψ_{0,1} plus ¼|A_{0,1}|+|A_{0,2}| ≤ ½(|A_{0,1}|+2|A_{0,2}|) ≤ ½|ID₁|). The certified arithmetic (2·∫φ_pID² = 3721/90720 = Ψ_{0,2}/2) is exactly what (37) needs either way.
* **N4 (frozen-extract nit, not a script issue).** `scheder_extracts.md`'s recon annotation "OCB*(4) = 0.00087004 — margin ≈ 5·10⁻⁷" is slightly wrong: the true value is 0.000869965583 (= 0.88·(7ln2 − 4657/960)), margin 4.00e−7. The script is correct; the extract's side-note should not be quoted as the number.
* **N5.** The endpoint facts s(0) = 0 and s(1/2) = 1/2 (used by C.12's FTC substitution) hold identically from EN's (1−t²)t⁴ factors; they are verified by inspection here but are not explicit certificates in the script.

**Corroborating observations (not issues):** at ε = 0.13 *all four* C.12 claims fail on the grid (not only s′), consistent with the extract's recon; claim 1's exact failure threshold is ε = √7/24 ≈ 0.110243 (derived here), so eps_R ≈ 0.102476 clears it by ~7% — the repair at JC's parameters is tight but real, and the exact certificates are the right instrument for it.

---

## Method appendix

* Independent cross-check script: `xcheck.py` in the session scratchpad (r-space source-definition formulas; Simpson n = 2^15; 10^5-point claim grids; verbatim-copied certifier functions probed with seeded negatives P1–P7 — all behaved correctly: 0 enclosure violations, honest INCONCLUSIVE on tangency and boundary slivers, correct refutation of a genuinely false claim at ε = 0.111).
* Hand-derived exact integrals (full antiderivative computations in this review): L55 = 170ln2 − 707/6; ∫φ_TwoCC² = 15/14; BFS = 380ln2 − 790/3; I_ocb(4) = 7ln2 − 4657/960.
* Source pages read directly from `scheder_tr21069_rev1.pdf` and checked against both the script and the frozen extracts: 24–27 ((12), Cor. 42, f_KL, Lemmas 43–45, (13)–(16)), 38 (Lemma 55), 46–47 (Defs. 67–68, Thm. 69), 51 (Lemma 75 Cases 3–4, incl. the false 10/256), 55 ((34)–(37)), 77–80 (C.10–C.13 with proofs, MLB/OCB definitions (21)/(22), Lemma D.1 giving Q′_r = 2r/(1−r)³). No transcription discrepancy between source, extracts, and script was found other than extract nit N4.

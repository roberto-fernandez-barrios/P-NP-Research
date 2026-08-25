# VERBATIM IMPORT LEDGER — Jiang–Cai (arXiv:2607.10697v1) vs. Scheder "PPSZ is better than you think"

Hostile independent validation, 2026-08-25. Both papers treated as potentially wrong.

**Frozen sources** (SHA-256 re-verified this session against `frozen_sources/scheder_manifest.txt`):

| tag | file | identity | SHA-256 (verified) |
|---|---|---|---|
| JC | `frozen_sources/arxiv_src/a_better_analysis_for_ppsz_3_.tex` (946 lines, read in full) + compiled `arxiv_2607.10697v1.pdf` | Jiang–Cai, "A Better Analysis For PPSZ For 3-SAT", July 2026 | (tex from frozen arXiv source bundle) |
| ECCC | `frozen_sources/scheder_tr21069_rev1.pdf` | ECCC TR21-069 **Revision 1**, Oct 15 2021, 81 pp. — JC's normative "SchederFull" | `e4d634c4…2dc4e506` ✓ |
| THEO | `frozen_sources/scheder_theoretics_24_5.pdf` | TheoretiCS Vol. 3 (2024) Art. 5, 37 pp. — JC's "SchederJournal" | `fbcb127d…19e0ae94` ✓ |
| (arXiv 2207.11071v2) | `frozen_sources/scheder_arxiv_2207.pdf` | byte-identical to THEO | `fbcb127d…19e0ae94` ✓ |

Method: my own `pdftotext` extraction of both Scheder PDFs for navigation, **plus rendered-page (visual)
verification of every load-bearing display** (ECCC pp. 5, 6, 19, 20–22, 24–25, 36–40, 44–48, 51–56, 61,
77–80; THEO p. 7). Full verbatim quotes with page numbers are archived in
`frozen_sources/scheder_extracts.md`. Anything I could not see is recorded as such. Float-level numeric
checks are quarantined in sections marked **NON-CERTIFYING RECONNAISSANCE** (scripts archived as
`frozen_sources/recon_scheder.py`, `frozen_sources/recon2_scheder.py`) and play no role in the verdicts.

**Numbering note (task-brief vs. actual).** The tasking referred to "Imported estimates 2.3/2.4", change
of measure "eq. (5)" and sibling inequality "eq. (10)". In the frozen .tex as compiled (verified against
`arxiv_2607.10697v1.pdf`): the imported estimates are **Imported estimate 2.1** (regular) and
**Imported estimate 2.2** (irregular); the change of measure is **JC eq. (4)**; the regular gain display
is JC eq. (5); b₁/b₀/b_T are JC eqs. (7)/(8)/(9); the sibling inequality is **JC eq. (10)**; the
degree-two bound is JC eq. (11). Content identification is unambiguous; the ledger uses the actual numbers.

Throughout: "§n" = section of ECCC; ϵ = Scheder's ε; JC's ε_R, ε_I as in JC eq. (20)
(`eq:parameter-values`): ε_R = 0.1024756190168075228998451658, ε_I = 0.07307238160252154687451293138.

---

## I1. Change of measure — JC eq. (4)

**(a) JC verbatim** (.tex lines 210–221):
> "All logarithms in the coefficient functions are natural. For 0 ≤ t ≤ 1, define
> f_KL(t) = (1−t) ln(1−t) + t, with 0 ln 0 = 0. Let U be uniform on variable placements and let D ≪ U be
> one of Scheder's auxiliary distributions. If Forced(π) is the number of variables inferred when the run
> follows the unique satisfying assignment, then
> E_{π∼U}[2^{−n+Forced(π)}] ≥ 2^{−n+E_{π∼D}[Forced(π)]−KL₂(D‖U)}.  (4)
> This is Equation (2) of the full version [SchederFull] and Equation (3) of the journal version
> [SchederJournal]."

**(b) Source verbatim.** ECCC p. 6, Equation **(2)** [VISUALLY VERIFIED]:
> E_Q[2^X] = Σ_ω Q(ω)2^{X(ω)} = Σ_ω P(ω)·(Q(ω)/P(ω))·2^{X(ω)} = E_{ω∼P}[2^{X(ω)−log₂(P(ω)/Q(ω))}]
> ≥ 2^{E_P[X]−E_{ω∼P}log₂(P(ω)/Q(ω))} = 2^{E_P[X]−KL(P||Q)}.  (2)
> "Here, KL(P||Q) := Σ_ω P(ω) **log₂**(P(ω)/Q(ω)) … If Q and P are continuous distributions … with
> density functions f_Q and f_P, then (2) still holds, for KL(P||Q) := ∫_Ω f_P(ω) log₂(f_P(ω)/f_Q(ω))."

THEO p. 7, Equation **(3)** [VISUALLY VERIFIED]: identical chain and identical log₂ definitions.

**(c) Source hypotheses.** Generic distributions Q (reference) and P (auxiliary) on the same space;
derivation is the convexity (Jensen) step applied to 2^t; discrete case as a sum, continuous case via
densities f_P, f_Q. Absolute continuity of P w.r.t. Q is implicitly required for P(ω)/Q(ω), f_P/f_Q to
make sense; the source does not write "P ≪ Q" explicitly. **KL is base-2 in both versions (log₂ printed).**
No parameter restrictions.

**(d) JC usage.** Specialization Q = U (uniform on placements), P = D, X = Forced(π), with the constant
−n carried through. This is exactly how the source itself uses (2): ECCC p. 45 [VISUAL]:
"Pr[ppsz(F) succeeds] = E_π[2^{−n+Forced(π)}] (by (1)) ≥ 2^{−n+E_{π∼D}[Forced(π)]−KL(D||U)} (by (2))".
JC's KL₂ = base-2 KL matches; JC's explicit "D ≪ U" is a (correct, mild) formalization of what the
source leaves implicit. JC's f_KL is a separate natural-log function and matches the source's f_KL
(ECCC p. 25; see I2(ii)).

**(e) VERDICT: UNCHANGED.** Display, KL base (binary), and both citation targets (full (2), journal (3))
verified. (Task-brief labelled it JC eq. (5); actual compiled number is (4) — a tasking slip, not a JC error.)

---

## I2. Regular estimate — JC Imported estimate 2.1 / JC eq. (5)

**(a) JC verbatim** (.tex lines 242–262):
> "**Imported estimate 2.1** (Regular lower bound from Scheder). For every fixed 0 ≤ ε_R ≤ 0.13, every
> fixed Thr > 0, and every admissible finite strength w,
> P[PPSZ_w(F) = α] ≥ 2^{−p₀n+gain_R−ξ_R(w)n−r_{R,w}(n)}, where
> gain_R ≥ (0.001687 ε_R − 0.006404 ε_R²)|H_low| + 0.9 Thr |H_high|
>          + (0.009307 − 0.055 ε_R − 0.1503 f_KL(ε_R))|TwoCC| − 1.1 ε_R Thr n.  (5)"
> Followed by: "Equation (5) is the final coefficient inequality in Section 7.8 of [SchederFull].
> Scheder substitutes ε_R = 0.1 in his final simplification; we use the inequality before that
> substitution."

**(b) Source verbatim.** ECCC §7.8, p. 45 [VISUALLY VERIFIED]:
> gain := 0.001687 ϵ|H_low| + 0.9 Thr|H_high| + (0.009307 − 0.055 ϵ)|TwoCC| − 1.1 ϵThr n
>         − 0.0064 ϵ²|H_low| − (5/(48 ln(2))) f_KL(ϵ)|TwoCC|
>       = **(0.001687 ϵ − 0.006404 ϵ²)|H_low| + 0.9 Thr|H_high|
>         + (0.009307 − 0.055 ϵ − 0.1503 f_KL(ϵ))|TwoCC| − 1.1 ϵThr n**
> then "Setting ϵ = 0.1, the gain is at least …", then "We set Thr := 2/(0.9·10118) ≤ 1/4553 …",
> concluding gain ≥ |H|/10118 − n/41391 (proof of Theorem 35). Success statement carrying the display:
> "Pr[ppsz(F) succeeds] = E_π[2^{−n+Forced(π)}] ≥ 2^{−n+E_D[Forced(π)]−KL(D||U)} = 2^{−n+s₃n+gain}"
> (per-variable o(1)/oh(1) errors from Lemmas 53/55/58/66 are suppressed in this chain; Theorem 35's
> statement carries the −o(n)).

**Sub-check (i) — the seven coefficients.** All verified glyph-by-glyph on p. 45:
0.001687 ✓ (Lemma 55, p. 38: "≥ s₃ − o(1) − 1.1 ϵThr + 0.001687 ϵ", from ϵ∫₀^{1/2}γ²(r)(1−Q_r)²);
0.006404 ✓ (printed in the collected line; NB the first line has 0.0064 from Lemma 45 — the printed "="
between the lines is therefore actually a "≥", valid because −0.006404ϵ² ≤ −0.0064ϵ², i.e. safe direction);
0.9 ✓ (Lemma 58, p. 40: "Pr_D[Cut(Tx)] ≥ s₃ − o(1) − 1.1 ϵThr + 0.9 Thr", via Lemma 64 = C.10);
0.009307 and 0.055 ✓ (Lemma 66, p. 44: "Pr_D[Tx] ≥ s₃ + 0.009307 − 0.055 ϵ", with Cut2CC = s₃ + 104/3 −
50 ln 2 ≈ s₃ + 0.009307); 0.1503 ✓ (from 5/(48 ln 2) = 0.150281…, rounded up = safe under subtraction);
1.1 ✓ (Lemma 53, p. 36/38: −0.56 ϵThr − 0.54 ϵThr = −1.1 ϵThr). **JC transcription: exact.**

**Sub-check (ii) — f_KL.** ECCC p. 25 [VISUAL]: "We write f_KL(ϵ) := (1 − ϵ) ln(1 − ϵ) + ϵ." Natural
log (the surrounding constants divide by ln(2), and Lemma 43 uses ln(1−ϵ) ≤ −ϵ−ϵ²/2). JC's
f_KL(t) = (1−t)ln(1−t)+t: **identical, natural log confirmed.**

**Sub-check (iii) — validity range of ε_R.** The 0.13 appears at ECCC p. 24 [VISUAL]: "We will also
choose some ϵ ≤ 0.13, and thus 1 + ϵφ(x) and 1 + ϵφ(x)φ(y) are really probability density functions."
Also hypotheses "ϵ ≤ 0.13" in Corollary 42, Lemma 44, Lemma 45, Lemma 55, Propositions 51/52.
**MISMATCH:** the H_high chain behind the 0.9 Thr term is proved via Lemma 64 = Lemma C.10, whose proof
rests on **Proposition C.12 (ECCC p. 77), printed hypothesis "Provided that ϵ ≤ 0.1"**, and its proof
(p. 78) says "referring … to **our promise that ϵ ≤ 0.1**" (one internal claim there, s′(r) ≤ 1.05, is
stated "provided ϵ ≤ 0.13"). So the printed source proof covers the full display only for ϵ ≤ 0.1, not
ϵ ≤ 0.13 as JC assert. **JC's own chosen ε_R = 0.10247… exceeds 0.1**, i.e. lies outside the printed
hypothesis of a load-bearing component; no statement in the source covers (0.1, 0.13] for the 0.9 Thr term.

**Sub-check (iv) — definitions of H, H_low, H_high, Thr, TwoCC.**
H: any subset of **edges of the sibling graph SG** with (V,H) of maximum degree 2 (Theorem 35, p. 20);
SG = undirected **multigraph** on the variables, one edge {y,z} per variable's canonical critical clause
(x ∨ ȳ ∨ z̄), |E| = n counting multiplicity (p. 20). |H|, |H_low|, |H_high| are **edge counts**.
H_free ⊆ H = TwoCC-free edges (p. 22, Observation 37: |H_free| ≥ |H| − 3|TwoCC|); H_high ⊆ H_free =
edges with LabelDensity ≥ Thr (either direction); H_low = H_free \ H_high \ H_rest minus a 1/18-fraction
so components have ≤ 17 edges (p. 22). Thr: "We choose some threshold Thr > 0. Our final choice will be
Thr := 2/(0.9·10118) ≈ 1/4553" (p. 22). TwoCC: **vertex** set per Definition 31 (p. 19) — variables with
≥ 2 critical clauses **in F̃** (see I8). LabelDensity ((9)/(10), p. 22) is ϵ-free, so the partition
depends only on (F, H, Thr). JC's reconciliation table matches all of this except the TwoCC/F̃ nuance (I8).

**Sub-check (v) — unconditional?** YES. Standing hypotheses from §5 on: 3-CNF with unique satisfying
assignment, normalized to all-ones (p. 6: "Everything from Section 5 on deals exclusively with the case
of Unique-3-SAT"; p. 7). Theorem 35 holds "for every H ⊆ E(SG) such that (V,H) has maximum degree 2" —
no regularity case-hypothesis. "The regular case" (§7 title) is a label, not a hypothesis. Every variable
falls into exactly one of the four per-variable buckets of §7.8 (H_low-edge variables, H_high-edge
variables, TwoCC, rest), for any uniquely satisfiable 3-CNF.

**Sub-check (vi) — finite-strength structure.** The source states Theorem 35 as
"2^{−n+s₃n+gain₁−o(n)}" for PPSZ with "w = w(n) … some fixed, slowly growing function" (p. 3), i.e. in
the joint limit; "the growth rate of w only influences how fast this o(1) error term vanishes" (p. 4);
per-variable errors are Error(r,h) → 0 as h → ∞ (Lemma 13), with h = max{h : w ≥ (k−1)^{h+1}} (p. 8),
plus a second height h′ "sufficiently large compared to h, but still a slowly growing function in n"
(§7.6, p. 40); Lemma A.2 says "o(1) converges to 0 as w grows". **The source nowhere states a
fixed-strength decomposition of the form ξ_R(w)n + r_{R,w}(n) with ξ_R(w) → 0 and r_{R,w}(n) = o(n)
per fixed w.** JC's Imported estimate 2.1 asserts it as part of the import. It is a plausible
reformulation of the proof structure (per-variable errors depend on (h, h′) only, both determined by w),
but it is JC's packaging, not a quoted statement; the h ≪ h′ interplay under fixed w is nowhere spelled out.

**Hidden Thr constraint (affects "every fixed Thr > 0").** Proposition C.13(2), ECCC p. 79 [VISUAL]:
"For d ≤ 4, OCB*(d), MLB*(d) ≥ **1/1150 ≥ Thr**", used in the first case of Lemma 64's proof (p. 80:
"(45) ≥ min(MLB(4), OCB(4)) ≥ Thr"). The proof of the 0.9 Thr term therefore **requires Thr ≤ 1/1150 ≈
8.696·10⁻⁴**. JC's "every fixed Thr > 0" is an overclaim. (JC's actual Thr = 2A/0.9 ≈ 2.2168·10⁻⁴
satisfies the constraint; Scheder's is 2.1963·10⁻⁴.)

**(d) JC usage.** JC use the display with ≥, both parameters symbolic, then substitute
ε_R = 0.1024756…, Thr = 2A/0.9 with A = (17/18)(0.001687ε_R − 0.006404ε_R²) (JC eqs. (12)–(14)).
The Thr value differs from Scheder's (2.2168·10⁻⁴ vs 2.1963·10⁻⁴), legitimate only if the estimate is
Thr-parametric — which it is, **subject to Thr ≤ 1/1150** (satisfied).

**(e) VERDICT: PARTIAL.**
- Display and all seven coefficients: verbatim, UNCHANGED (with the source-internal footnote that the
  printed "=" is really a safe-direction "≥", and that §7.8's "fact 1" misquotes (11) with "2|TwoCC|" —
  a typo that is never used; the final chain uses the correct 3|TwoCC|).
- Hypotheses: **CHANGED** in two places. (1) ε-range: JC claim [0, 0.13]; the printed proof of the
  0.9 Thr component only covers ϵ ≤ 0.1 (Prop C.12 + p. 78 "promise"), and **JC's chosen
  ε_R = 0.10248 > 0.1 violates the printed hypothesis**. (2) Thr-quantifier: "every fixed Thr > 0" vs
  the source proof's Thr ≤ 1/1150 (C.13(2)); JC's numeric choice complies.
- Finite-strength (ξ_R, r_{R,w}) clause: JC reformulation, not present in the source.

**NON-CERTIFYING RECONNAISSANCE (kept out of the verdict).** Float-level checks of Prop C.12's four
numeric claims (with δ_max per (13)–(16)): all four hold at ϵ = 0.1 and — razor-thin — at JC's
ε_R = 0.1024756 (binding claim s′(r) ≤ 1.05: max s′ ≈ 1.04893); they fail from ϵ ≈ 0.105–0.11 upward
(at ϵ = 0.11: s′ ≈ 1.0525 > 1.05 and two other claims negative; at ϵ = 0.13: s′ ≈ 1.0621, so the
source's own "provided ϵ ≤ 0.13" on the s′-claim appears false). So JC's chosen point happens to sit in
the (unprinted) numeric slack of C.12, but the claimed range up to 0.13 does not, for the source's
specific constants 0.95/0.98/1.05/0.945. Additional recon on §7.7: DFS2CC = −∫Q·B·φ_A computes to
≈ 0.04575 vs the printed "≤ 0.0455", and JUNK2CC computes to ≈ +0.00098 vs the printed "≤ −0.019"
(dropping −ϵ²·JUNK2CC in Lemma 66 is then not conservative); if real, the imported TwoCC coefficient
0.009307 − 0.055ϵ is optimistic by ≈ 3.4·10⁻⁵ per TwoCC variable at ε_R (≈ 1%); this would perturb JC's
S = c_T − 5A but leaves their dual margins (b_T + λS ≈ 0.0139) and certificate value materially intact.
Also recon-confirmed as safe: 0.28/0.54 in Lemma 53 (0.2754/0.5318), Lemma 44's 0.004434 (margin 2·10⁻⁷),
∫γ²(1−Q)² = 0.00168736 ≥ 0.001687 (margin 4·10⁻⁷), Corollary 50's 1.02-claim up to ϵ = 0.13.

---

## I3. Irregular estimate — JC Imported estimate 2.2 / JC eqs. (6)–(9)

**(a) JC verbatim** (.tex lines 264–289):
> "**Imported estimate 2.2** (Irregular lower bound from Scheder). For every fixed 0 ≤ ε_I ≤ 1/5 and
> every admissible finite strength w, P[PPSZ_w(F) = α] ≥ 2^{−p₀n+gain_I−ξ_I(w)n−r_{I,w}(n)}, where
> gain_I ≥ b₁(ε_I)|ID₁| + b₀(ε_I)|ID₀| + b_T(ε_I)|TwoCC|  (6) and
> b₁(ε) = 0.030966 ε − 0.0028 ε² − 0.4027 f_KL(ε),  (7)
> b₀(ε) = 0.06259 ε − 0.344 f_KL(ε),  (8)
> b_T(ε) = 0.009307 − 0.2405 ε − 0.03125 ε² − 0.06183 f_KL(5ε).  (9)"
> Followed by: "Equation (6) is the final lower bound in Section 8.4 of [SchederFull], before the
> substitution ε_I = 0.029. Appendix A verifies that the larger value used here satisfies the
> source-side admissibility conditions."

**(b) Source verbatim.** ECCC §8.4, p. 56 [VISUALLY VERIFIED] — after combining (37), (31), (33),
"the 'gain' log₂ Pr[success] + n − s₃n is at least":
> ≥ |ID₁| (0.030966 ϵ − 0.0028 ϵ² − 0.4027 f_KL(ϵ))
>   + |ID₀| (0.06259 ϵ − 0.344 f_KL(ϵ))
>   + |TwoCC| (0.009307 − 0.2405 ϵ − 0.03125 ϵ² − 0.06183 f_KL(5ϵ))
> "For ϵ = 0.029, this is at least |ID₁|/1380 + |ID₀|/600 + |TwoCC|/617 ≥
> (|ID₁| + 2|ID₀| + 2|TwoCC|)/1380. This completes the proof of Theorem 36."

**Sub-check (i) — coefficients.** All nine decimals verified glyph-by-glyph on p. 56: 0.030966, 0.0028,
0.4027, 0.06259, 0.344, 0.009307, 0.2405, 0.03125, 0.06183. **JC transcription: exact** (including the
argument 5ϵ inside f_KL of the TwoCC coefficient).

**Sub-check (ii) — f_KL.** Same function as I2(ii) (p. 55 repeats "for f_KL(ϵ) = (1−ϵ) ln(1−ϵ) + ϵ").
Natural log ✓; f_KL(5ϵ) enters via (36): KL(D_ϵ^{γTwoCC}||U) = KL(D_{5ϵ}^{γTwoCC/5}||U) ≤
(f_KL(5ϵ)/ln 2)(1/25)Ψ_TwoCC, using |φ_TwoCC/5| ≤ 1 (φ_TwoCC attains −5 at r = 1/2) — this is where the
implicit source-side restriction **5ϵ ≤ 1** originates (domain/series of Lemma 43 at parameter 5ϵ).

**Sub-check (iii)+(viii) — ε-range and admissibility.** The source states **no global ε-range for §8**;
the printed local restrictions are: Lemma 73 (p. 48): "provided that ϵ ≤ 4/5"; Lemma 75 Case 3 (p. 51):
"ϵ ≤ 1"; Lemma 75 Case 4 (p. 51): "this holds for all ϵ ≤ 256/600"; implicit 5ϵ ≤ 1 via (36); and
Definition 38's proviso that densities be nonnegative — which the source **never verifies for the §8
choices** (JC's Lemma A.1 supplies exactly this check, correctly framed as an admissibility verification).
- **Definition 67 quote check:** verbatim match [VISUAL, p. 46]: γ_ID0,1(r) := 10r²(1−2r)²,
  γ_pID0,1(r) := (61/6) r³(1−2r)², γ_TwoCC(r) := 20 r³(1−2r), all "defined to be 0 for r ≥ 1/2".
  JC's Lemma A.1 quotes exactly these (renaming ID0,1 → ID). ✓
- **Density form:** ✓ — Definition 38 densities 1 + ϵφ; Definition 67: each x sampled independently from
  D_ϵ^{γ_x}, density 1 + ϵγ_x′(r) (explicit on p. 46: "density f_{π(x)}(r) = 1 − ϵφ_ID0,1(r)"; p. 52:
  "1 − ϵφ₁(r)I_x + ϵφ₂(r)(I_y + I_z)"). JC's "1 + ε_I γ_v′" matches. ✓
- **Combinations:** ✓ — Definition 67 gives γ_x = −γ_ID0,1·I_x + γ_pID0,1·(I_y + I_z) for x ∉ TwoCC,
  so derivatives are −aφ_ID + mφ_pID with a = I_x ∈ {0,1}, m = I_y + I_z ∈ {0,1,2}, exactly as JC's
  Lemma A.1 claims; Definition 70's γ_u^B is the same family; TwoCC variables get φ_TwoCC ≥ −5. ✓
- **The three restrictions JC cite (4/5, 256/600, 5ϵ ≤ 1): all located** (pp. 48, 51, 55). The only
  further printed condition is Case 3's ϵ ≤ 1 (implied by ϵ ≤ 1/5), and Lemma 72's condition
  γ_TwoCC ≥ 2rγ_ID0,1/(1−2r) is ϵ-free and holds with identical equality (p. 80, Lemma D.1). **No other
  ε-condition found in §8/App. D** — JC missed nothing that is printed.
- **MISMATCH (source-side arithmetic error inherited into JC's range claim):** the printed 256/600
  rests on p. 51's claim "γ_ID0,1(r) = 10r²(1−2r)² ≤ **10/256** for all 0 ≤ r ≤ 1/2" — this is FALSE:
  max r²(1−2r)² = 1/64 (at r = 1/4), so max γ_ID0,1 = 10/64 and the correct conclusion of the printed
  argument is **ϵ ≤ 64/600 ≈ 0.10667**, not 256/600 ≈ 0.4267. Consequence: JC's Lemma A.1 sentence
  "This range [ε_I ≤ 1/5] also implies the restrictions ε_I ≤ 4/5, ε_I ≤ 256/600, and 5ε_I ≤ 1 used
  elsewhere in the source" is faithful to the **printed** source, but under the corrected constraint the
  claimed range [0, 1/5] is NOT fully admissible: for ε_I ∈ (64/600, 1/5] the source's Lemma 75 Case 4
  argument fails as printed-and-corrected. **JC's fixed ε_I = 0.07307 < 64/600 remains admissible.**

**Sub-check (iv) — sets in the display.** Verified: the display's |ID₁|, |ID₀| are the **Section-8**
sets (excluding TwoCC; see (vii)), |TwoCC| per Definition 31.

**Sub-check (v) — unconditional?** YES — same standing hypotheses as I2(v); Theorem 36 and the §8.4
display have no case hypothesis; the sets ID₀, ID₁, TwoCC are whatever they are for the given formula.

**Sub-check (vi) — finite-strength.** Same situation as I2(vi): the source's (31) carries "−o(n)",
Theorem 36 is stated with −o(n) under w(n) slowly growing; the ξ_I(w)n + r_{I,w}(n) split is JC's
reformulation, not a source statement. PARTIAL.

**Sub-check (vii) — the ID_i notation switch. VERIFIED, JC's reconciliation is CORRECT:**
- §6, p. 20 [VISUAL]: "For i ∈ N₀, let ID_i be the set of variables x with deg_in(x) = i." (ALL
  variables — JC's J_i.) Theorem 36's statement (pp. 21 and 46) uses this convention: "where ID_i is the
  set of variables with in-degree i in the critical clause graph."
- §8, p. 45 [VISUAL]: "Additionally, let ID_i be the set of variables **in V \ TwoCC** that have
  in-degree i in the critical clause graph." (JC's ID_i = J_i \ TwoCC.)
- §8.4's final display refers to the **Section-8 sets** (the proof works entirely inside §8's
  convention), and the very last line "≥ (|ID₁| + 2|ID₀| + 2|TwoCC|)/1380" is precisely the bridge back
  to Theorem 36's Section-6 sets (using |J_i ∩ TwoCC| contributing ≤ 2|TwoCC|). The same bridge
  inequality appears in JC (.tex lines 302–310). A reader conflating the two conventions would get a
  different estimate; JC did not conflate them.

**(d) JC usage.** Import with ≥, symbolic ε_I, then ε_I = 0.07307238… (> Scheder's 0.029; admissibility
argued via their Lemma A.1). Coordinates i₀, i₁, τ built on the §8 sets. Consistent.

**(e) VERDICT: PARTIAL.**
- Display, coefficients, f_KL, set conventions, Definition 67 quote, density form, combination family,
  and the located restrictions: verbatim, UNCHANGED.
- The claimed parameter range [0, 1/5] is **supported only by the printed (erroneous) 256/600**; under
  the corrected source arithmetic (64/600) the range claim is false on (64/600, 1/5], though JC's actual
  parameter 0.07307 is safely inside. This is a source-defect inherited by JC's Lemma A.1's secondary
  sentence, not a transcription error.
- Finite-strength clause: JC reformulation (as I2).

**NON-CERTIFYING RECONNAISSANCE.** All coefficient closed forms verified numerically (Simpson +
closed-form): BFS = 380ln2 − 790/3 = 0.0625953; DFB = 0.0316288; BFS − DFB = 0.0309665 ≥ 0.030966 ✓
(margin 5·10⁻⁷); JUNK₁ + 2JUNK₂ = 0.0027420 ≤ 0.0028 ✓ (note the printed intermediate "JUNK₂ ≤
0.000184" is false — actual 0.000203044 — but harmless downstream); (5/21 + 3721/90720)/ln2 =
0.4026729 ≤ 0.4027 ✓; (5/21)/ln2 = 0.3434988 ≤ 0.344 ✓; Bonus2CC = 0.0093076 ≥ 0.009307 ✓;
DFS2CC + DFD2CC = 0.2404721 ≤ 0.2405 ✓ (the printed intermediate "DFD2CC ≤ 0.074135" is a hairline
misprint: actual 0.0741353); JUNK2CC = 0.0292973 ≤ 0.03125 ✓; 15/(350 ln2) = 0.0618298 ≤ 0.06183 ✓.
So every printed coefficient in the §8.4 display is a safe-direction rounding of the exact closed form.
At ϵ = 0.029: b₁ = 0.00072466 ≥ 1/1380, b₀ = 0.0016690 ≥ 1/600, b_T = 0.0016223 ≥ 1/617 ✓ (source's
final line consistent). JC's Lemma A.1 nonnegativity: min density at ε = 1/5 is ≈ 6·10⁻⁵ ≥ 0 (attained
by the TwoCC density at r → 1/2, where 1 + (1/5)(−5) = 0 — the bound 1/5 is exactly tight), and their
stated derivative bounds |φ_ID| ≤ 5/2, |φ_pID| ≤ 61/54, φ_TwoCC ≥ −5 all hold (actual maxima ≈ 0.962,
0.345, −5). Lemma 73's printed "ϵ ≤ 4/5" looks generous under every natural reading of Prop 52's
condition (recon ceilings ≈ 0.40–0.71), but all readings exceed 1/5, so JC's range is unaffected by it.

---

## I4. Sibling-graph inequality — JC eq. (10)

**(a) JC verbatim** (.tex lines 293–297):
> "Scheder's sibling-graph construction gives (18/17)|H_low| + 2|H_high| + 3|TwoCC| ≥ |H|.  (10)"
> Provenance table: "sibling-graph inequality — full version Eq. (11)".

**(b) Source verbatim.** ECCC p. 22, Equation **(11)** [VISUALLY VERIFIED]:
> (18/17)|H_low| + 2 |H_high| + 3 |TwoCC| ≥ |H|.  (11)

**(c) Source hypotheses.** Holds by construction of H_low/H_high/H_rest from any max-degree-2 H ⊆ E(SG)
and any Thr > 0 (Observation 37: |H_free| ≥ |H| − 3|TwoCC|; |H_rest| ≤ |H_high|; removal of a
1/18-fraction to cap components at 17 edges: "Let H_low be the set of remaining edges, and observe that
(11)"). All H-sets are edge sets of the sibling multigraph; TwoCC per Definition 31.

**(d) JC usage.** Verbatim, to eliminate |H_low|, |H_high| in favor of |H| after equalizing coefficients
(their eqs. (12)–(14)); Thr chosen so 0.9 Thr matches 2A. Same direction and same sets.

**(e) VERDICT: UNCHANGED.** (Ledger note: the source's own §7.8 "fact 1" restates (11) with "2 |TwoCC|"
— a typo in the restatement only; (11) itself and the final chain use 3|TwoCC|, and JC import the correct 3.)

---

## I5. Degree-two subgraph bound — JC eq. (11)

**(a) JC verbatim** (.tex lines 298–311):
> "His Lemma 34 gives |H| ≥ n − |J₁| − 2|J₀|. Since J_i = ID_i ∪̇ (J_i ∩ TwoCC) for i ∈ {0,1} and
> |J₁ ∩ TwoCC| + 2|J₀ ∩ TwoCC| ≤ 2|TwoCC|, we obtain |H| ≥ n − |ID₁| − 2|ID₀| − 2|TwoCC|.  (11)"
> Provenance table: "degree-two subgraph bound — full version Lemma 34 and Lemma A.3".

**(b) Source verbatim.** ECCC p. 20 [VISUAL], **Lemma 34**: "There is a set H ⊆ E(SG) of maximum degree
2 (i.e., H consists of paths and cycles) with |H| ≥ n − |ID₁| − 2 |ID₀|." — here ID_i is the §6
(all-variables) set, i.e. exactly JC's J_i. ECCC p. 61 [VISUAL], **Lemma A.3** = "(Lemma 34, restated)",
same statement verbatim, with the marking proof.

**(c) Source hypotheses.** Only the standing Unique-3-SAT setup (SG well-defined via canonical critical
clauses). Degrees in SG count parallel edges; deg_SG(y) = deg_in(y) in CCG (p. 20).

**(d) JC usage.** J_i := source's §6 ID_i ✓; the ∪̇-split and ≤ 2|TwoCC| step are JC's own (elementary,
and the same bridge the source uses in the last line of §8.4). Existence statement used with the same H
as in Theorem 35 (legitimate: Theorem 35 quantifies over every max-degree-2 H).

**(e) VERDICT: UNCHANGED.** (Source-internal note: Lemma A.3's proof prints "The total number of edges
is n, thus Σ_{x∈V} deg_SG(x) = n" — the sum of degrees is 2n; the subsequent identity
0 = Σ_x(deg(x)−2) is exactly the 2n statement, so the proof is correct modulo this typo. Does not affect
the imported statement.)

---

## I6. Published endgame — JC eqs. (1)–(2), bonus 1/15218

**(a) JC verbatim** (.tex lines 63–84):
> "the final simplification in Section 6 of the full version is gain_R ≥ |H|/10118 − n/41391,
> gain_I ≥ (|J₁| + 2|J₀|)/1380.  (1)   Writing irr = (|J₁| + 2|J₀|)/n and using |H|/n ≥ 1 − irr gives
> (1/n) max{gain_R, gain_I} ≥ max{(1 − irr)/10118 − 1/41391, irr/1380} ≥ 1/15218.  (2)
> Thus Scheder's published unique-case bonus is γ_old = 1/15218 = 0.000065711657247995…, with unrounded
> base 1.306972376565153…." Provenance: "published 1/15218 endgame — full version Theorems 35–36 and end
> of Section 6".

**(b) Source verbatim.** ECCC pp. 20–21 [VISUALLY VERIFIED]:
- **Theorem 35**: "…success probability of PPSZ is at least 2^{−n+s₃n+gain₁−o(n)} for
  gain₁ ≥ |H|/10118 − n/41391." (10118 ✓, 41391 ✓)
- **Theorem 36**: "…at least 2^{−n+s₃n+gain₂−o(n)}, gain₂ ≥ (|ID₁| + 2|ID₀|)/1380, where ID_i is the
  set of variables with in-degree i in the critical clause graph." (1380 ✓; §6 convention = JC's J_i ✓)
- End of §6 (p. 21): "gain := n·max((|H|/n)/10118 − 1/41391, irr/1380) ≥ n·max((1−irr)/10118 − 1/41391,
  irr/1380) (by Lemma 34) ≥ n/15218. Thus, the success probability of PPSZ is at least Ω(1.306973^{−n}),
  which proves Theorem 6." (15218 ✓; 1.306973 ✓)
- **Theorem 6** (p. 5): "The success probability of PPSZ on 3-CNF formulas with a unique satisfying
  assignment is at least 1.306973^{−n}." Base 1.306973 also in the abstract (p. 1).

**(c) Source hypotheses.** Unique-3-SAT (all-ones normalized); o(n) with w(n) slowly growing; H from
Lemma 34. The source's final unique statement is "Ω(1.306973^{−n})" / "at least 1.306973^{−n}" — the
"unrounded base 1.306972376565153…" is **JC's own back-computation** from 1/15218 (it is not printed in
the source; the source prints only the rounded 1.306973).

**(d) JC usage.** Reference values for comparison only (γ_old, base); their improvement claim is
γ_new = 0.0000687793 > 1/15218.

**(e) VERDICT: UNCHANGED** (all four constants, the max-structure, and the final base located verbatim;
the unrounded base is JC's derived value, consistent — see recon — but not a source quote).

**NON-CERTIFYING RECONNAISSANCE:** 1/15218 = 6.5711657…·10⁻⁵ ✓ matches JC's decimal;
2^{1−s₃−1/15218} = 1.3069723765651533 ✓ matches JC's "1.306972376565153…"; also reproduced JC's claim
that the same affine recombination at Scheder's (0.1, 0.029) yields 0.000065719084… (float agreement).

---

## I7. Simultaneity of the two estimates

**(a) JC's implicit claim** (.tex lines 481–487): "The two imported estimates bound the same success
probability. Hence log₂ P[PPSZ_{w₀}(F) = α] ≥ −p₀n + max{gain_R, gain_I} − …".

**(b)–(c) Source structure (quoted).** Theorem 35 (p. 20) and Theorem 36 (p. 21) are **both
unconditional statements about the success probability of the same algorithm on the same formula class**
(uniquely satisfiable 3-CNF, all-ones normalized): neither carries a case hypothesis; "almost regular" /
"highly irregular" are names in the theorem headers, not assumptions. Each theorem is proved by running
the change-of-measure bound (2) against a different auxiliary distribution D (§7.2's correlated D for
Theorem 35; Definition 67's product D for Theorem 36) — the distribution is an analysis device, not an
algorithm change. The source itself takes the max (p. 21): "Combining the two theorems, we see that the
success probability of PPSZ is at least 2^{−n+s₃n+gain−o(n)}, for gain := n·max(…)". No side conditions.

**(d) JC usage.** max{gain_R, gain_I} over the same formula with the same coordinate sets (ID₀, ID₁,
TwoCC per Definition 31 — identical in both imports).

**(e) VERDICT: UNCHANGED / CONFIRMED.** Both bounds hold simultaneously for every uniquely satisfiable
3-CNF; taking the max is exactly the source's own step.

---

## I8. Setup: canonical critical clauses, arcs, J_i, TwoCC

**(a) JC verbatim** (.tex lines 206–207):
> "By complementing variables, we normalize the unique satisfying assignment to the all-one assignment.
> Choose one canonical critical clause (x ∨ ȳ ∨ z̄) for each variable x and put arcs x → y and x → z in
> the critical-clause graph. Let J_i be the indegree-i class, and let TwoCC be the set of variables
> having at least two critical clauses."

**(b) Source verbatim.**
- Normalization: p. 7: "We assume that α = (1, …, 1) is the unique satisfying assignment." ✓
- Canonical selection: p. 7 [§3.1]: "This is called a critical clause. **If there are several to pick
  from, we ask x to select one to be its canonical critical clause.**" ✓ ONE canonical per variable,
  arbitrary choice; TwoCC variables also select one (CCG has out-degree exactly 2 at every vertex, p. 20).
- Arcs: p. 20 [VISUAL]: "for every variable x, if the canonical critical clause of x is (x ∨ ȳ ∨ z̄),
  we create arcs (x, y) and (x, z)." ✓
- J_i: p. 20: "For i ∈ N₀, let ID_i be the set of variables x with deg_in(x) = i" — the §6 sets = JC's
  J_i ✓ (JC's table row "J_i — all indegree-i variables … called ID_i in Section 6" is exact).
- TwoCC: **Definition 31 (p. 19) [VISUAL]: "Let F̃ be the CNF formula F plus all 3-clauses that can be
  inferred from pairs of 3-clauses of F … Let TwoCC be the set of variables that contain at least two
  critical clauses in F̃."** This is the operative definition for the entire k = 3 analysis (§5.1
  announces the generalization "for technical reasons"; the proof of Proposition 56, p. 38, explicitly
  relies on it: "recall that we included these 'derived' critical clauses in our definition of TwoCC").

**(c)–(d) Comparison.** JC's phrase "variables having at least two critical clauses" matches the
source's *loose* restatements (pp. 8, 22, 45) but **omits the F̃-closure of Definition 31**, which is
what Sections 5–8 (hence both imported estimates and Observation 37/(11)) actually use. JC use TwoCC
purely as an opaque cardinality |TwoCC| = τn, identical in both imports and in the structural
inequalities, so their recombination is internally consistent *provided their TwoCC symbol is read as
Definition 31's set*; but their printed definition denotes a (generally smaller) set.

**(e) VERDICT: PARTIAL.** Canonical-clause convention, arcs, J_i: UNCHANGED. TwoCC: **CHANGED
(definition omits the F̃-closure of Definition 31)** — no impact on the LP recombination's validity
(the symbol is used opaquely and consistently), but the definition as stated in JC §2.1 and in their
reconciliation table does not match the source's operative definition.

---

## I9. p₀ = 2 ln 2 − 1, baseline 1.3070319, and general-3-SAT statements in the source

**(a) JC verbatim** (.tex lines 54–61): "the classical exponent is P[PPSZ(F) = α] ≥ 2^{−p₀n−o(n)},
p₀ = 2 ln 2 − 1, so the corresponding running-time base is 2^{p₀} = 1.3070319…".

**(b) Source facts.**
- **p₀ = 2 ln 2 − 1 (equivalently s₃ = 2 − 2 ln 2) is NOT printed anywhere** in either version
  (exhaustive text search of both extractions: "2 ln 2", "2 − 2 ln", 0.6137…, 0.3862…, "ln 4" — zero
  hits). The source defines s_k only via the branching-process integral: Lemma 13 (p. 10):
  "s_k := ∫₀¹ Q_r^{(k)} dr", with Q_r^{(3)} = (r/(1−r))² for r < 1/2 (p. 9).
- The **numeric baseline is printed in both versions**: ECCC p. 5 / THEO p. 5: "it improves the success
  probability from 1.3070319^{−n} from Theorem 3 [THEO: 'in Theorem 1.3'] to 1.306995^{−n}" (HKZZ
  comparison). The source's exponent statements are written as 2^{−n+s₃n+…}, i.e. with s₃, not p₀.
- **General 3-SAT:** TR21-069 rev 1 contains **Theorem 5** (p. 5): "For every k ≥ 3 there is ϵ_k > 0
  such that the success probability of PPSZ on satisfiable k-CNF formulas is at least 2^{−n(1−s_k−ϵ_k)}"
  — a *qualitative* general-SAT statement (no number), via **Theorem 4** (p. 5), the unique-to-general
  lifting theorem — which both versions cite as "([8])" although the surrounding text attributes it to
  Scheder–Steinberger ([12] resp. [14]); an apparent mis-citation in the source. The TheoretiCS version
  has the same pair (Theorem 1.5 / Theorem 1.4). **Neither version states any numeric general-3-SAT
  bound anywhere.** The only numeric result is Unique-3-SAT: Theorem 6, 1.306973^{−n} (ECCC only).

**(e) VERDICT: PARTIAL.** The numeric baseline 1.3070319 is in the source (both versions); the closed
form p₀ = 2 ln 2 − 1 is a JC-added standard identity (recon: s₃ = ∫ = 0.6137056389 = 2 − 2 ln 2 and
2^{1−s₃} = 1.3070319077 — consistent), NOT a source quote. General-3-SAT: only the qualitative Theorem
5/1.5 exists; **no numeric general-3-SAT bound appears in TR21-069 rev 1 or the TheoretiCS version** —
so JC's general-case number has no Scheder-side counterpart to conflict with (their Corollary 1.2 relies
on Scheder–Steinberger, outside this ledger's scope).

---

## I10. Journal version vs. ECCC full version — publication status of the imports

**(b) Journal version's own remarks (verbatim).**
- THEO p. 1 footnote: "An extended abstract of this work has already been published [12], and a full
  version is publicly accessible at [13]." References (p. 33): [12] = FOCS 2021, pages 205–216;
  [13] = "Electron. Colloquium Comput. Complex. 69, 2021" (= TR21-069; no revision number given).
- THEO §1.4 "The case k = 3" (pp. 6–7): "The full version of Hansen et al. and the ECCC version of this
  result [13] invest considerable energy to hammer out a concrete numerical result … And although the
  k = 3 part of [13] follows roughly the same approach as the general-k case in this paper, it
  introduces several new concepts and methods that are not needed for Theorem 1.5. Furthermore, it is
  highly technical … Finally, the analysis for k = 3 in [13] does not hit any natural wall, and
  therefore a simple tightening of inequalities and a better choice of constants and functions would
  already yield a better bound. **We therefore decided not to include the k = 3 part in this paper.**"

**Content audit of the journal version** (grep over all 37 pages, plus TOC): it contains the
change-of-measure **Equation (3)** (p. 7, VISUALLY VERIFIED — identical to ECCC (2), log₂ KL),
Theorem 1.5 (qualitative, satisfiable k-CNF), critical clause trees/cuts, the general-k proof (§4), and
appendix A. It contains **zero occurrences** of: 10118, 41391, 1380, 15218, 1.306973, 0.001687,
0.030966, 0.009307, Definition 67, TwoCC, H_low/H_high, LabelDensity, sibling graph. I.e. **there is no
§7.8-equivalent or §8.4-equivalent display in the journal version; the k = 3 numeric part was dropped
in its entirety**, exactly as the parallel novelty audit reported, and with the journal's own stated
reason that the k = 3 constants are not tight.

**(e) VERDICT / publication status of JC's imports:**
- I1 (change of measure): **refereed** — appears verbatim in TheoretiCS (Eq. (3)) and in ECCC (Eq. (2)).
- I2, I3, I4, I5, I6 (both coefficient displays, Eq. (11), Lemma 34/A.3, Theorems 35–36, all endgame
  constants, Theorem 6's 1.306973): **present ONLY in the unrefereed ECCC report TR21-069 Revision 1.**
  A refereed FOCS 2021 extended abstract exists ([12], 12 pages), which presumably states the headline
  k = 3 result, but it is not among the frozen sources and I did NOT verify what it contains; the
  detailed §7.8/§8.4 displays with all constants cannot be assumed to appear in a 12-page extended
  abstract. JC's own normative citation (SchederFull) is explicitly the ECCC revision.
- The journal version moreover *disavows tightness* of the dropped k = 3 constants ("a simple tightening
  of inequalities … would already yield a better bound") — consistent with JC's enterprise, but it means
  the imported displays never passed journal refereeing.

---

# Summary table

| # | Import | Verdict | Mismatch severity |
|---|---|---|---|
| I1 | Change of measure (JC (4) = ECCC (2) = THEO (3)), base-2 KL | **UNCHANGED** | none |
| I2 | Regular display (Imported estimate 2.1 = §7.8 final display) | **PARTIAL** — display verbatim; hypotheses broadened | **HIGH**: JC's ε-range [0, 0.13] vs printed ϵ ≤ 0.1 for the 0.9 Thr component (Prop C.12), and **JC's own ε_R = 0.10248 > 0.1**; "every Thr > 0" vs source's Thr ≤ 1/1150 (Prop C.13(2)) — JC's Thr complies; finite-strength (ξ_R, r_{R,w}) is JC packaging |
| I3 | Irregular display (Imported estimate 2.2 = §8.4 final display) | **PARTIAL** — display & Definition 67 verbatim; range claim inherits source bug | **MEDIUM**: printed 256/600 rests on false "10r²(1−2r)² ≤ 10/256" (true max 10/64 ⇒ 64/600 ≈ 0.1067), so claimed range (64/600, 1/5] unsupported; JC's ε_I = 0.0731 safe; finite-strength packaging as I2 |
| I4 | Sibling-graph inequality (JC (10) = ECCC (11)) | **UNCHANGED** | none (source's §7.8 restatement typo "2\|TwoCC\|" noted; unused) |
| I5 | Degree-two bound (Lemma 34 / Lemma A.3; J_i = §6 ID_i) | **UNCHANGED** | none (source proof's "Σdeg = n" typo noted; harmless) |
| I6 | Endgame 10118 / 41391 / 1380 / 15218, base 1.306973 | **UNCHANGED** | none (JC's "unrounded base" is derived, not quoted — consistent) |
| I7 | Simultaneity of the two estimates (max legitimate) | **UNCHANGED / CONFIRMED** | none — source itself takes the max; both theorems unconditional |
| I8 | Setup (canonical clause, arcs, J_i, TwoCC) | **PARTIAL** | **MEDIUM-LOW**: JC's TwoCC definition omits Definition 31's F̃-closure (operative for all of §§5–8); usage is opaque/consistent so the LP is unaffected, but JC's printed definition denotes the wrong set |
| I9 | p₀ = 2ln2−1, baseline, general-3-SAT statements | **PARTIAL** | LOW: 1.3070319 present; closed form p₀ = 2ln2−1 **not in source** (JC-added standard identity, recon-consistent); no numeric general-3-SAT bound in either version (qualitative Theorem 5/1.5 only); source mis-cites its lifting theorem as [8] |
| I10 | Journal vs ECCC (publication status) | **CONFIRMED** (journal dropped all k = 3 numerics) | **STRUCTURAL**: every k = 3 numeric import (I2–I6) exists only in the unrefereed ECCC revision; journal keeps only I1 and states the k = 3 constants are not tight; FOCS extended abstract exists but was not frozen/verified |

## Source-internal defects found while checking (in TR21-069 rev 1; not JC transcription errors)

1. p. 51 (Lemma 75, Case 4): "10r²(1−2r)² ≤ 10/256" is false (max = 10/64); printed conclusion
   "ϵ ≤ 256/600" should be "ϵ ≤ 64/600". [Feeds I3's range claim.]
2. p. 77–78 (Prop C.12): hypothesis "ϵ ≤ 0.1" vs §7.2's standing "ϵ ≤ 0.13"; internal s′-claim printed
   "provided ϵ ≤ 0.13" is (recon) false at 0.13. [Feeds I2's range claim.]
3. p. 79 (Prop C.13(2)): "≥ 1/1150 ≥ Thr" silently constrains Thr ≤ 1/1150. [Feeds I2's Thr quantifier.]
4. p. 45 (§7.8): the "=" between the two gain lines is actually "≥" (0.0064 → 0.006404 and
   5/(48 ln 2) = 0.150281 → 0.1503 are strict weakenings; safe direction).
5. p. 44 (§7.8 fact 1): restates (11) with "2|TwoCC|" instead of 3 (typo; unused — the p. 45 chain uses 3).
6. p. 47 (Definition 68): "JUNK₂ … ≤ 0.000184" is false (exact value 8767591/192 − 65880 ln 2 =
   0.000203044…); the downstream "JUNK ≤ 0.0028" used in §8.4 remains true (0.0027420). [recon]
7. p. 54: "DFD2CC … ≤ 0.074135" is a hairline misprint (exact 0.0741353…); the 0.2405 used in §8.4
   still covers DFS2CC + DFD2CC = 0.2404721. [recon]
8. p. 44 (§7.7, recon only): printed "DFS2CC ≤ 0.0455" computes to ≈ 0.04575, and printed
   "JUNK2CC ≤ −0.019" computes to ≈ +0.00098 with the printed γ_A, γ̃, B; if real, Lemma 66's
   "0.009307 − 0.055ϵ" (imported into JC's c_T) is optimistic by ≈ 3.4·10⁻⁵ per TwoCC variable at
   ε_R ≈ 0.1025 (≈ 1% of the coefficient); JC's dual margins absorb this comfortably, but the
   discrepancy could not be reconciled with the printed text. NON-CERTIFYING.
9. p. 61 (Lemma A.3 proof): "Σ_{x∈V} deg_SG(x) = n" (should be 2n); conclusion unaffected.
10. p. 5 / THEO p. 5: the unique-to-general lifting theorem (Theorem 4 / 1.4) is cited "([8])" while the
    text attributes it to Scheder–Steinberger ([12]/[14]) — apparent mis-citation.
11. p. 48 (Lemma 73): printed "ϵ ≤ 4/5" appears generous (recon ceilings 0.40–0.71 under the natural
    readings of Prop 52's condition); all readings still exceed JC's 1/5. NON-CERTIFYING.

## Overall verdict

**MISMATCHES FOUND.** The *transcription layer* is clean — every display JC quote (change of measure,
both coefficient displays with all sixteen decimals, Eq. (11), Lemma 34, the endgame constants,
Definition 67's three densities) matches the frozen ECCC revision glyph-for-glyph, and JC's
ID-notation reconciliation (§6 vs §8) is verified correct. The mismatches are in the **hypothesis
layer** and in **provenance status**:

1. **[HIGH] I2 ε-range / parameter choice.** Imported estimate 2.1 claims validity for ε_R ≤ 0.13 and
   JC evaluate it at ε_R = 0.1024756…, but the source's printed proof of the 0.9 Thr term (Prop C.12)
   carries the hypothesis ϵ ≤ 0.1. JC's chosen parameter is outside the printed hypothesis; recon shows
   the underlying numeric claims do (barely) hold at 0.10248 and fail well below 0.13, so the theorem
   JC actually need is true-but-unproved-in-print at their operating point, and their stated range
   0.13 is unsupported.
2. **[MEDIUM] I2 Thr-quantifier.** "Every fixed Thr > 0" overstates the source, whose proof needs
   Thr ≤ 1/1150 (JC's Thr = 2.217·10⁻⁴ complies).
3. **[MEDIUM] I3 ε-range.** The claimed range [0, 1/5] leans on the source's erroneous 256/600
   (corrected: 64/600 ≈ 0.1067); JC's fixed ε_I = 0.0731 stays admissible.
4. **[MEDIUM-LOW] I8 TwoCC definition.** JC's stated definition omits Definition 31's F̃-closure; usage
   is opaque and consistent, so no downstream damage, but the printed definition is not the source's.
5. **[LOW] I9.** p₀ = 2 ln 2 − 1 is JC's added closed form, not a source statement (numerically
   consistent); JC's finite-strength error decomposition (ξ_X(w)n + r_{X,w}(n)) is likewise their own
   packaging of the source's o(n)-with-slowly-growing-w(n) statements.
6. **[STRUCTURAL] I10.** All k = 3 numeric imports live only in the unrefereed ECCC revision; the
   refereed TheoretiCS version deliberately dropped them (and remarks they are not tight); only the
   change-of-measure identity is refereed. JC's fixed-parameter certificate therefore inherits the
   evidentiary status of an unrefereed technical report at every numeric layer above I1.

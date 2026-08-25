# Scheder source extracts — frozen page quotes for the import ledger

Compiled 2026-08-25 for the hostile import validation of Jiang–Cai (arXiv:2607.10697v1).

Sources (SHA-256 verified against `scheder_manifest.txt` on 2026-08-25):

* **ECCC** = `scheder_tr21069_rev1.pdf` (TR21-069 Revision 1, dated October 15, 2021, 81 pp.,
  SHA-256 `e4d634c4...2dc4e506` — matches manifest). Page numbers below are the printed page numbers,
  which coincide with PDF page numbers.
* **THEO** = `scheder_theoretics_24_5.pdf` (TheoretiCS Vol. 3 (2024), Art. 5, 37 pp.,
  SHA-256 `fbcb127d...19e0ae94` — matches manifest; byte-identical to `scheder_arxiv_2207.pdf`).

Extraction method: my own `pdftotext -layout` run (files `eccc_layout.txt`, `theoretics_layout.txt` in the
session scratchpad), plus **visual verification with the Read tool (rendered pages)** of every load-bearing
formula quoted below. Quotes marked [VISUAL] were verified glyph-by-glyph on the rendered page; the
pdftotext extraction drops some epsilon glyphs, so no epsilon-sensitive formula is quoted from extraction
alone. In the quotes below, `eps` denotes the source's ϵ and `fKL` its f_KL.

---

## ECCC p. 3–4 — PPSZ convention and error terms

> "Let w = w(n) be some fixed, slowly growing function." (p. 3, definition of ppsz)

> "The o(1)-term converges to 0 as w tends to infinity; thus, the growth rate of w only influences how
> fast this o(1) error term vanishes, but (as far as we know) does not materially influence the success
> probability of PPSZ." (p. 4)

> **Observation 2** ([8]): "Suppose we run PPSZ with a fixed permutation π. Then ppsz(F, π) succeeds,
> i.e., finds α, with probability exactly 2^(−n+Forced(π))."

> **Equation (1)** (p. 4): Pr[ppsz(F) succeeds] = E_π[2^(−n+Forced(π))] ≥ 2^(−n+E_π[Forced(π)]).

> **Lemma 13** ([8], p. 10): "Let Tx be a critical clause tree of height h. Then Pr[Cutr(Tx)] ≥
> Q_r^(k) − Error(r, h), for some function Error(r, h) that converges to 0 as h → ∞, and
> Pr[Cut(Tx)] ≥ s_k − o(1), where s_k := ∫₀¹ Q_r^(k) dr."

> **Lemma 8** ([8], p. 8): "Suppose w ≥ (k−1)^(h+1), where w is the strength parameter of PPSZ. …
> then Forced(x, π) = 1." Followed by: "From now on, we take h = h(n) to be the largest integer such
> that w ≥ (k−1)^(h+1) … Note that lim_{n→∞} h(n) = ∞ because lim_{n→∞} w(n) = ∞."

> Lemma A.2 (p. 58): "… where o(1) converges to 0 as w grows."

## ECCC p. 5 — Theorems 4, 5, 6 [VISUAL]

> **Theorem 4 ([8]).** "If the success probability of PPSZ is at least 2^(−n+s_k n+ϵn) on k-CNF formulas
> with a unique satisfying assignment, for some ϵ > 0, then it is at least 2^(−n+s_k n+ϵ′n) on k-CNF
> formulas with multiple solutions, too, for some (smaller) ϵ′ > 0)."
> [Note: cited to [8] = PPSZ; the preceding paragraph attributes the lifting theorem to [12] = Scheder–Steinberger.]

> **Theorem 5 (Improvement for all k).** "For every k ≥ 3 there is ϵ_k > 0 such that the success
> probability of PPSZ on satisfiable k-CNF formulas is at least 2^(−n(1−s_k−ϵ_k))."

> **Theorem 6 (Improved success probability for 3-SAT).** "The success probability of PPSZ on 3-CNF
> formulas with a unique satisfying assignment is at least 1.306973^(−n)."

> Baseline mention (p. 5): "for 3-SAT, it improves the success probability from 1.3070319^(−n) from
> Theorem 3 to 1.306995^(−n)." [HKZZ comparison]

Note: neither "p0 = 2 ln 2 − 1" nor "s3 = 2 − 2 ln 2" is printed anywhere in either version
(searched: "2 ln 2", "2 − 2 ln", 0.6137…, 0.3862…, "ln 4"; zero hits in both extractions).

## ECCC p. 6 — Equation (2), change of measure [VISUAL]

> E_Q[2^X] = Σ_{ω∈Ω} Q(ω) 2^(X(ω)) = Σ_{ω∈Ω} P(ω)·(Q(ω)/P(ω))·2^(X(ω))
>          = E_{ω∼P}[2^(X(ω) − log₂(P(ω)/Q(ω)))]
>          ≥ 2^(E_P[X] − E_{ω∼P} log₂(P(ω)/Q(ω)))
>          = 2^(E_P[X] − KL(P||Q)) .   **(2)**

> "Here, KL(P||Q) := Σ_ω P(ω) **log₂**(P(ω)/Q(ω)) is the Kullback-Leibler divergence from Q to P.
> If Q and P are continuous distributions (over Ω = [0,1]^n, for example) with density functions f_Q
> and f_P, then (2) still holds, for KL(P||Q) := ∫_Ω f_P(ω) log₂(f_P(ω)/f_Q(ω))."

Also p. 6: "Everything from Section 5 on deals exclusively with the case of Unique-3-SAT."

## ECCC p. 7–8 — critical clauses, canonical selection, TwoCC (first form)

> (p. 7, §3.1): "We assume that α = (1, …, 1) is the unique satisfying assignment. That means that for
> every variable x, we can find a clause of the form (x ∨ ȳ₂ ∨ · · · ∨ ȳ_k). This is called a critical
> clause. If there are several to pick from, we ask x to select one to be its **canonical critical clause**."

> (p. 8): "Case (1) motivates the definition of the set TwoCC ⊆ V, the set of variables that have two or
> more critical clauses."

## ECCC p. 19 — Definition 31 (operative TwoCC for k = 3) and Definition 32 [VISUAL]

> (§5.1): "Recall the definition of TwoCC, the set of variables that have two or more critical clauses.
> For k = 3, we will slightly generalize this definition, for technical reasons."

> **Definition 31.** "Let F̃ be the CNF formula F plus all 3-clauses that can be inferred from pairs of
> 3-clauses of F; for example, if F contains (x ∨ ȳ ∨ z̄) and (a ∨ x̄ ∨ ȳ), then F̃ additionally contains
> (a ∨ ȳ ∨ z̄). **Let TwoCC be the set of variables that contain at least two critical clauses in F̃.**"

> **Definition 32 (Canonical nodes).** "The node u in Tx is called a canonical node if for all 0 ≤ i ≤ d,
> (1) z_i ∉ TwoCC and (2) the clause label of u_i is the canonical critical clause of z_i."

Corroboration that Def. 31 is operative in Section 7: proof of Proposition 56 (p. 38) [VISUAL]:
> "…meaning that a has two critical clauses (recall that we included these 'derived' critical clauses in
> our definition of TwoCC)."

## ECCC p. 20 — Section 6: CCG, ID_i (all-variables form), sibling graph, Lemma 34, Theorem 35 [VISUAL]

> "Recall the critical clause digraph CCG defined in Section 4.1: its vertex set is V, the set of
> variables; for every variable x, if the canonical critical clause of x is (x ∨ ȳ ∨ z̄), we create arcs
> (x, y) and (x, z). Each vertex (variable) has out-degree 2, giving a total of 2n arcs. …
> **For i ∈ N₀, let ID_i be the set of variables x with deg_in(x) = i.** Let ID_{0,1} = ID₀ ∪ ID₁."

> "We define the **sibling graph** SG = (V, E), an undirected multigraph on the set of variables V: for
> every x ∈ V, let (x ∨ ȳ ∨ z̄) be its canonical critical clause. We add the edge {y, z} to E. Note that
> |E| = n (counting parallel edges by their multiplicity). What is deg_G(y)? … it is deg_in(y), its
> in-degree in the (directed) critical clause graph."

> **Lemma 34.** "There is a set H ⊆ E(SG) of maximum degree 2 (i.e., H consists of paths and cycles)
> with |H| ≥ n − |ID₁| − 2 |ID₀|."  — "See Lemma A.3 in the appendix for a proof."

> **Theorem 35 (PPSZ on almost regular formulas).** "Let H ⊆ E(SG) be a subset of edges of the sibling
> graph such that (V, H) has maximum degree 2. Then the success probability of PPSZ is at least
> 2^(−n+s₃n+gain₁−o(n)) for gain₁ ≥ |H|/10118 − n/41391."

## ECCC p. 21 — Theorem 36 and the 1/15218 endgame [VISUAL]

> **Theorem 36 (PPSZ on highly irregular formulas).** "The success probability of PPSZ is at least
> 2^(−n+s₃n+gain₂−o(n)), gain₂ ≥ (|ID₁| + 2 |ID₀|)/1380, **where ID_i is the set of variables with
> in-degree i in the critical clause graph.**"

> "We define irr := (|ID₁| + 2 |ID₀|)/n … Combining the two theorems, we see that the success
> probability of PPSZ is at least 2^(−n+s₃n+gain−o(n)), for
>   gain := n · max( (|H|/n)/10118 − 1/41391 , irr/1380 )
>        ≥ n · max( (1 − irr)/10118 − 1/41391 , irr/1380 )   (by Lemma 34)
>        ≥ n/15218 .
> Thus, the success probability of PPSZ is at least Ω(1.306973^(−n)), which proves Theorem 6."

## ECCC p. 22 — Section 7 opening, Observation 37, LabelDensity, Thr, Equation (11) [VISUAL]

> "Also, recall the definition of TwoCC ⊆ V, the set of variables that have two or more critical
> clauses. We say an edge {y, z} in the sibling graph is TwoCC-free if y ∉ TwoCC and z ∉ TwoCC and, for
> all x ∈ V whose canonical critical clause is (x ∨ ȳ ∨ z̄), also x ∉ TwoCC. Let H_free ⊆ H be the set
> of all TwoCC-free edges in H."   **Observation 37.** |H_free| ≥ |H| − 3 |TwoCC|.

> **(9)** LabelDensity(z, T_y, r) := Σ_{v∈Can(T_y), varlabel(v)=z} (1−2r)²/(1−r)³ · r^(d(v)+1)
> **(10)** LabelDensity(z, T_y) := ∫₀^{1/2} LabelDensity(z, T_y, r) dr
> [No ϵ anywhere in (9)/(10).]

> "We choose some threshold Thr > 0. **Our final choice will be Thr := 2/(0.9·10118) ≈ 1/4553.**"
> [Construction of H_high, H_rest, H_low; components of H_low have ≤ 17 edges; a 1/18-fraction is removed.]

> **(11)**  (18/17)|H_low| + 2 |H_high| + 3 |TwoCC| ≥ |H| .

## ECCC p. 24–25 — γ, ϵ ≤ 0.13, f_KL, KL lemmas [VISUAL]

> **(12)** γ(r) := r(1−2r)^{3/2} if r ≤ 1/2, and 0 if r > 1/2. "Note that γ(r) is continuous
> differentiable, and φ(r) := γ′(r) is continuous. One checks that −1/√5 ≤ φ(r) ≤ 1 for all r ∈ [0,1].
> **We will also choose some ϵ ≤ 0.13**, and thus 1 + ϵφ(x) and 1 + ϵφ(x)φ(y) are really probability
> density functions on [0,1] and [0,1] × [0,1]."

> **Corollary 42** (p. 25): "… holds for our particular choice γ(r) = r(1−2r)^{3/2}. Furthermore, if
> |E(G)| ≤ 17 and ϵ ≤ 0.13, this is at least r + 1.2 ϵγ(r) Σ_{v:{u,v}∈E} T_v⁻."

> (§7.2.3, p. 25): "**We write f_KL(ϵ) := (1 − ϵ) ln(1 − ϵ) + ϵ.**"  [natural log; the neighboring
> constants are m₂/ln(2), so ln is unambiguous]

> **Lemma 43.** "If |φ(x)| ≤ 1 for all x ∈ [0,1] then KL(D_ϵ^γ || U) ≤ (m₂/ln(2)) · f_KL(ϵ). Using
> ln(1−ϵ) ≤ −ϵ − ϵ²/2, this is at most (m₂/(2 ln(2)))(ϵ² + ϵ³)."

> **Lemma 44.** "Let G be a cycle or a path, consisting of at most t edges. For γ(r) = r(1−2r)^{3/2},
> φ(r) = γ′(r), ϵ ≤ 0.13, and t ≤ 17, it holds that KL(D^G || U) ≤ **0.0064** ϵ² t."

> **Lemma 45** (p. 26): "For our particular choice of γ and γ_TwoCC, ϵ ≤ 0.13, and every component of
> H_low having at most 17 edges … KL(D||U) ≤ 0.0064 ϵ² |H_low| + (5/(48 ln 2)) f_KL(ϵ) |TwoCC|."
> [§7's γ_TwoCC(r) := max(0, 40 r^{7/2}(1 − 2r)²), p. 26 — distinct from §8's γ_TwoCC.]

## ECCC p. 27 — δ_root, δ_non-root, δ_max (Eqs. (13)–(16))

> (13) δ_root := 1.2 ϵ γ(r) max(0, −φ(r));  (14) δ_non-root := 1.2 ϵ γ²(r)/(1−r);
> (15) δ_v := Σ_{u: v◁u} (δ_root if u is the root, δ_non-root otherwise);
> (16) δ_max := max(2δ_non-root, δ_non-root + δ_root) = 1.2 ϵ γ(r) max( 2γ(r)/(1−r), γ(r)/(1−r) − φ(r) ).

## ECCC p. 36–38 — Lemmas 53 and 55 [VISUAL]

> **Lemma 53.** "If x ∉ TwoCC then Pr_D[Cut(Tx)] ≥ ∫₀¹ Pr_D[Cut_r(T′_r)] ≥ s₃ − o(1) − 1.1 ϵThr."
> Final chain (p. 38): "Pr[Cut(Tx)] ≥ s₃ − 0.56 ϵThr − 9.792 ϵThr Σ_{d=1}^∞ (d+1)^{d+1}/(d+3)^{d+3}
> ≥ s₃ − 0.56 ϵThr − 0.54 ϵThr = s₃ − 1.1 ϵThr."

> **Lemma 55.** "For our choice γ(r) = r(1−2r)^{3/2} and ϵ ≤ 0.13, it holds that Pr_D[Cut(Tx)] ≥
> s₃ − o(1) − 1.1 ϵThr + ϵ ∫₀^{1/2} γ²(r)(1 − Q_r)² ≥ s₃ − o(1) − 1.1 ϵThr + **0.001687 ϵ**."
> [Section title 7.5: "The case that x ∉ TwoCC and {y, z} ∈ H_low".]

## ECCC p. 40 — Lemma 58 [VISUAL]

> "For technical reasons, let Tx be a critical clause tree of height h′, where h′ is sufficiently large
> compared to h, but still a slowly growing function in n."
> **Lemma 58.** "Pr_D[Cut(Tx)] ≥ s₃ − o(1) − 1.1 ϵThr + **0.9 Thr**."
> [Section title 7.6: "The case that x ∉ TwoCC and {y, z} ∈ H_high". Proof runs through Lemma 61,
> Lemma 62 (OCB), Lemma 63 (MLB), Lemma 64.]
> **Lemma 64** (p. 42): "Σ_{v∈B₁} OCB(d(v)) + Σ_{v∈B_z} MLB(d(v)) ≥ 0.9 Thr." — "See Lemma C.10 for a proof."

## ECCC p. 44 — Section 7.7 constants and 7.8 facts 1–2 [VISUAL]

> Theorem 65 display: Pr_D[Cut(Tx)] ≥ Cut2CC − ϵ(DFS2CC + DFD2CC) − ϵ²JUNK2CC − o(1), where
> Cut2CC := ∫₀¹ Q_r B(r) dr = s₃ + 104/3 − 50 ln(2) ≈ s₃ + 0.009307.
> Applied with γ_A = γ_TwoCC = 40r^{7/2}(1−2r)², γ_rest = γ̃ = 2.4ϵγ²(r)/(1−r):
> "DFS2CC ≤ 0.0455, DFD2CC ≤ 0.0095, JUNK2CC ≤ −0.019."
> **Lemma 66.** "Pr_D[Tx] ≥ s₃ + 0.009307 − 0.055 ϵ. for sufficiently large h."

> §7.8 fact 1 (as printed): "18/17 |H_low| + 2 |H_high| + **2** |TwoCC| ≥ |H|, by (11)."
> [Sic — (11) itself has 3|TwoCC|; the final chain on p. 45 uses 3|TwoCC|. Restatement typo, unused.]
> §7.8 fact 2: "KL(D||U) ≤ 0.0064 ϵ²|H_low| + (5/(48 ln(2))) f_KL(ϵ) |TwoCC|, by Lemma 45."

## ECCC p. 45 — THE REGULAR FINAL DISPLAY (Section 7.8) and Section 8 opening [VISUAL]

> Items: 3. Pr[Cut(Tx)] ≥ s₃ − 1.1 ϵThr + 0.001687 ϵ when {y,z} ∈ H_low, by Lemma 55;
> 4. … ≥ s₃ − 1.1 ϵThr + 0.9 Thr when {y,z} ∈ H_high, by Lemma 58;
> 5. … ≥ s₃ + 0.009307 − 0.055 ϵ when x ∈ TwoCC, by Lemma 66;
> 6. … ≥ s₃ − 1.1 ϵThr for all other x, by Lemma 53.

> Pr[ppsz(F) succeeds] = E_π[2^(−n+Forced(π))]  (by (1))
>   ≥ 2^(−n+E_{π∼D}[Forced(π)]−KL(D||U))  (by (2))  = 2^(−n+s₃n+gain), where
>
> gain := 0.001687 ϵ|H_low| + 0.9 Thr|H_high| + (0.009307 − 0.055 ϵ)|TwoCC| − 1.1 ϵThr n
>         − 0.0064 ϵ²|H_low| − (5/(48 ln(2))) f_KL(ϵ)|TwoCC|
>      **= (0.001687 ϵ − 0.006404 ϵ²)|H_low| + 0.9 Thr|H_high|
>         + (0.009307 − 0.055 ϵ − 0.1503 f_KL(ϵ))|TwoCC| − 1.1 ϵThr n**
>
> "Setting ϵ = 0.1, the gain is at least gain ≥ |H_low|/9555 + 0.9 Thr|H_high| + |TwoCC|/335 − 0.11 Thr n
> … We set Thr := 2/(0.9·10118) ≤ 1/4553 so 0.9·10118·Thr ≥ 2 and
> gain ≥ [18/17|H_low| + 2|H_high| + 3|TwoCC|]/10118 − n/41391 ≥ |H|/10118 − n/41391, where the last
> inequality follows from (11). This completes the proof of Theorem 35."
> [Note: the printed "=" between the two gain lines replaces 0.0064 by 0.006404 and 5/(48 ln 2) =
> 0.150281… by 0.1503; both replacements only decrease the expression, so as a lower bound it is valid;
> as an equality it is not.]

> **Section 8 opening (p. 45):** "As before TwoCC be the set of all variables that have two or more
> critical clauses. Additionally, **let ID_i be the set of variables in V \ TwoCC that have in-degree i
> in the critical clause graph.**"

## ECCC p. 46 — Definition 67 [VISUAL]

> π(x) ∼ D_{−ϵ}^{γ_ID0,1}, "i.e., with density f_{π(x)}(r) = 1 − ϵφ_ID0,1(r) whenever x ∈ ID_{0,1} :=
> ID₀ ∪ ID₁ … Pr[π(x) < r] = r − ϵγ_ID0,1(r)."

> **Definition 67.** "For each variable x, define γ_x : [0,1] → R by
>   γ_x(r) := −γ_ID0,1(r) I_x + γ_pID0,1(r)(I_y + I_z)  if x ∉ TwoCC and (x ∨ ȳ ∨ z̄) is its critical clause;
>   γ_x(r) := γ_TwoCC(r)  if x ∈ TwoCC.
> Then let D be the distribution on placements that samples each variable x independently from D_ϵ^{γ_x}
> independently."
> "The functions γ_ID0,1(r), γ_pID0,1(r) are defined to be 0 for r ≥ 1/2; for r < 1/2, they are defined by
>   **γ_ID0,1(r) := 10 r²(1 − 2r)²,  γ_pID0,1(r) := (61/6) r³(1 − 2r)²,  γ_TwoCC(r) := 20 r³(1 − 2r).**"
> "This γ_TwoCC(r) is not the 40r^{7/2}(1 − 2r)² from the previous section."

## ECCC p. 47 — Definition 68 and Theorem 69 [VISUAL]

> BFS := −∫₀¹ φ_ID0,1(r) Q_r dr = 380 ln(2) − 790/3 ≥ 0.06259
> DFC := ∫₀¹ γ_ID0,1(r) P_r(1−Q_r) dr = 915/4 − 330 ln(2) ≤ 0.01144
> DFS := −∫₀¹ φ_pID0,1(r) Q_r dr = 1586 ln(2)/3 − 52765/144 ≤ 0.0202
> DFB := DFC + DFS = 596 ln(2)/3 − 19825/144 ≤ 0.03163
> JUNK₁ := max(0, −∫₀¹ φ_ID0,1 γ_ID0,1 P_r(1−Q_r) dr) = 46800 ln(2) − 227075/7 ≤ 0.00235
> JUNK₂ := max(0, ∫₀¹ φ_pID0,1 γ_ID0,1 P_r(1−Q_r) dr) = 8767591/192 − 65880 ln(2) ≤ 0.000184
>   [NB recon: 8767591/192 − 65880 ln 2 = 0.000203044…, i.e. the printed "≤ 0.000184" is false;
>    the downstream bound JUNK = JUNK₁ + 2JUNK₂ ≤ 0.0028 remains true (actual ≈ 0.0027420).]
> JUNK := JUNK₁ + 2 JUNK₂.

> **Theorem 69.** "Let x ∉ TwoCC and let (x ∨ ȳ ∨ z̄) be its critical clause. Then
> Pr_D[Cut(Tx)] ≥ s₃ + ϵI_x BFS − ϵ(I_y + I_z)DFB − ϵ²I_x(I_y+I_z)JUNK₁ − ϵ²(I_y+I_z)²JUNK₂ − o(1)."

## ECCC p. 48 — Lemmas 71–73 [VISUAL]

> **Lemma 71**: "Let x ∈ V \ TwoCC and let (x ∨ ȳ ∨ z̄) be its unique critical clause. …"
> **Lemma 72 (TwoCC-cleanup in the irregular case)**: "… provided that γ_TwoCC(r) ≥ 2rγ_ID0,1/(1−2r)."
> "The condition in the lemma justifies our particular choice for γ_TwoCC: the above inequality is
> satisfied with equality."  [Indeed 2r·10r²(1−2r)²/(1−2r) = 20r³(1−2r) identically; ϵ-free.]
> **Lemma 73**: "… provided that **ϵ ≤ 4/5**." — "in this section, δ_max = ϵγ_ID0,1(r), and a simple
> calculation shows that the condition r(1 − 2r) ≥ 2δ_max, required by Proposition 52, holds."

## ECCC p. 51 — Lemma 75, Cases 3–4 (the 256/600 claim) [VISUAL]

> Case 3: "(we check that 1 − r + δ_u is always positive for r ≤ 1/2 and **ϵ ≤ 1**, by a wide margin)".
> Case 4 final step: "= r/60 − ϵrγ_ID0,1 , (since P_r = r/(1−r)) which is non-negative if and only if
> ϵγ_ID0,1(r) ≤ 1/60. **Since γ_ID0,1(r) = 10 r²(1 − 2r)² ≤ 10/256 for all 0 ≤ r ≤ 1/2, this holds for
> all ϵ ≤ 256/600.** This concludes the proof of Lemma 75."
> [NB: max_{[0,1/2]} r²(1−2r)² = 1/64 at r = 1/4, not 1/256. The printed bound 10/256 is false; with the
> correct maximum 10/64 the conclusion becomes ϵ ≤ 64/600 ≈ 0.10667.]

## ECCC p. 53 — Equation (31) [VISUAL]

> Σ_{x∉TwoCC} Pr_D[Cut(Tx)] ≥ s₃(n − |TwoCC|) − o(n) + ϵ(|ID_{0,1}|BFS − |ID₁|DFB)
>   − ϵ²|ID₁|(JUNK₁ + 2 JUNK₂).   **(31)**

## ECCC p. 54–55 — Section 8.3 constants, (33)–(37) [VISUAL]

> **(32)** Pr_D[Cut(Tx)] ≥ s₃ + Bonus2CC − ϵ(DFS2CC + DFD2CC) − ϵ²JUNK2CC − o(1), with
> Bonus2CC := ∫₀¹ Q_r B(r) dr − s₃ = 104/3 − 50 ln(2) ≈ 0.009307
> DFS2CC := −∫₀¹ Q_r B(r) φ_TwoCC(r) dr = 39094/3 − 18800 ln(2) ≤ 0.16634
> DFD2CC := ∫₀¹ 2rγ_ID0,1(r)B(r)/(1−r)³ dr = 11420 ln(2) − 23747/3 ≤ 0.074135
>   [recon: = 0.0741353…, a hair above the printed 0.074135; the 0.2405 used in 8.4 covers the sum]
> JUNK2CC := ∫₀¹ 2rγ_ID0,1(r)B(r)φ_TwoCC(r)/(1−r)³ dr = 17923400/7 − 3694000 ln(2) ≈ 0.03125
>   [recon: = 0.0292973 ≤ 0.03125, safe]

> **(33)** log₂ Pr[ppsz succeeds] ≥ −n + Σ_x Pr_D[Cut(Tx)] − KL(D||U).

> **(36)** KL(D_ϵ^{γTwoCC}||U) = KL(D_{5ϵ}^{γTwoCC/5}||U) ≤ (f_KL(5ϵ)/ln(2))·(1/25)·Ψ_TwoCC, for
> Ψ_TwoCC := ∫₀¹ φ²_TwoCC(r) dr = 15/14.  ["φ_TwoCC(r) is −5 for r = 1/2, and this is its maximal
> absolute value. Thus, |φ_TwoCC(r)/5| ≤ 1" — Lemma 43 applied at parameter 5ϵ.]

> **(37)** KL(D||U) ≤ (f_KL(ϵ)/ln(2))·( (5/21)|ID_{0,1}| + (3721/90720)|ID₁| )
>          + (f_KL(5ϵ)·15)/(25 ln(2)·14) |TwoCC|.

## ECCC p. 56 — THE IRREGULAR FINAL DISPLAY (Section 8.4) [VISUAL]

> "Combining (37), (31), and (33), we see that the 'gain' log₂ Pr[success] + n − s₃n is at least
> [regrouped exact expression] ≥
>   **|ID₁| (0.030966 ϵ − 0.0028 ϵ² − 0.4027 f_KL(ϵ))
>   + |ID₀| (0.06259 ϵ − 0.344 f_KL(ϵ))
>   + |TwoCC| (0.009307 − 0.2405 ϵ − 0.03125 ϵ² − 0.06183 f_KL(5ϵ))**
>
> For ϵ = 0.029, this is at least |ID₁|/1380 + |ID₀|/600 + |TwoCC|/617 ≥ (|ID₁| + 2|ID₀| + 2|TwoCC|)/1380.
> This completes the proof of Theorem 36."
> [ID_i here in the Section-8 sense, i.e. excluding TwoCC; the last inequality is the bridge to
> Theorem 36's Section-6/all-variables ID_i.]

## ECCC p. 61 — Lemma A.3 [VISUAL]

> **Lemma A.3 (Lemma 34, restated).** "There is a set H ⊆ E(SG) of maximum degree 2 (i.e., H consists
> of paths and cycles) with |H| ≥ n − |ID₁| − 2 |ID₀|."
> Proof marks deg−2 edges at each vertex of degree ≥ 3; uses "The total number of edges is n, thus
> Σ_{x∈V} deg_SG(x) = n" [sic — should be 2n; the following identity 0 = Σ_x(deg(x) − 2) requires 2n]
> and 0 = Σ_x(deg(x)−2) = Σ_{deg≥3}(deg_SG(x)−2) − |ID₁| − 2|ID₀|.

## ECCC p. 77–80 — Propositions C.11–C.13 and the end of Lemma 64's proof [VISUAL]

> **Proposition C.12.** "**Provided that ϵ ≤ 0.1**, it holds that
>   OCB(d) = ∫₀^{1/2} OCB(d, r) dr ≥ 0.88 · ∫₀^{1/2} r(1−2r)/(1−r)² · r^d dr =: OCB*(d)
>   MLB(d) = ∫₀^{1/2} MLB(d, r) dr ≥ 0.9 · ∫₀^{1/2} (1−2r)²/(1−r)³ · r^d dr =: MLB*(d)."
> Proof (p. 78): "Referring to the definition of δ_max in (16) and to **our promise that ϵ ≤ 0.1**, we
> can verify numerically that [r(1−2r) − 2δ_max(1−r)]/(1−r)² ≥ 0.95·r(1−2r)/(1−r)²."
> "Claim. f(r) ≥ 0.98 · f(s(r))." — "Claim. s′(r) ≤ 1.05 for r ∈ [0,1/2], **provided ϵ ≤ 0.13**."
> "Claim. g(r) ≥ 0.945 · g(s(r))."
> [recon at ϵ = 0.13: max s′ ≈ 1.062 > 1.05, so the s′-claim's stated range 0.13 appears false; all four
> claims hold numerically at ϵ ≤ 0.1 and — barely — at ϵ = 0.1024756…, failing from ϵ ≈ 0.105–0.11.]

> **Proposition C.13.** "1. For d ≥ 5, it holds that OCB*(d) ≥ MLB*(d).
> 2. For d ≤ 4, **OCB*(d), MLB*(d) ≥ 1/1150 ≥ Thr**."
> [Point 2 requires Thr ≤ 1/1150 ≈ 0.00086957. recon: OCB*(4) = 0.00087004 — margin ≈ 5·10⁻⁷.]

> End of Lemma 64's proof (p. 80): "There are two cases. If A_z contains some u with d_{T_y}(u) ≤ 3
> then (45) ≥ min(MLB(4), OCB(4)) ≥ Thr, and the statement of Lemma 64 holds. Otherwise, (45) ≥
> Σ MLB*(d(u)+1) = 0.9·Σ ∫₀^{1/2}(1−2r)²/(1−r)³·r^{d(u)+1}dr = 0.9·LabelDensity(z, T_y) ≥ 0.9·Thr."

> **Lemma D.1 (Lemma 72 restated, p. 80):** "… provided that γ_TwoCC(r) ≥ 2rγ_ID0,1/(1−2r)."  [ϵ-free.]

## TheoretiCS (journal) version

> (p. 1): "An extended abstract of this work has already been published [12], and a full version is
> publicly accessible at [13]."
> References (p. 33): [12] = "Dominik Scheder. PPSZ is better than you think. 62nd IEEE Annual
> Symposium on Foundations of Computer Science, FOCS 2021, Denver, CO, USA, February 7-10, 2022,
> pages 205–216. IEEE, 2021." — [13] = "Dominik Scheder. PPSZ is better than you think. Electron.
> Colloquium Comput. Complex. 69, 2021."

> (p. 2): "…which we formally explain below in (3)."

> **Equation (3)** (p. 7/37) [VISUAL]: identical chain to ECCC (2), ending "= 2^(E_P[X]−KL(P||Q)) . (3)",
> followed by "The term KL(P||Q) := Σ_ω P(ω) log₂(P(ω)/Q(ω)) is known as the Kullback-Leibler
> divergence from Q to P. If Q and P are continuous distributions … then (3) still holds, for
> KL(P||Q) := ∫_Ω f_P(ω) log₂(f_P(ω)/f_Q(ω))."

> **§1.4 "The case k = 3"** (pp. 6–7) [VISUAL for the final sentence]: "The full version of Hansen et
> al. and the ECCC version of this result [13] invest considerable energy to hammer out a concrete
> numerical result how much they can improve over s₃. And although the k = 3 part of [13] follows
> roughly the same approach as the general-k case in this paper, it introduces several new concepts and
> methods that are not needed for Theorem 1.5. Furthermore, it is highly technical, and the set of
> people interested in it is most likely a clear subset of those interested in the general-k case.
> Finally, the analysis for k = 3 in [13] does not hit any natural wall, and therefore a simple
> tightening of inequalities and a better choice of constants and functions **would already yield a
> better bound. We therefore decided not to include the k = 3 part in this paper.**"

> **Theorem 1.5** (p. 6): "For every k ≥ 3 there is ϵ_k > 0 such that the success probability of PPSZ
> on satisfiable k-CNF formulas is at least 2^(−n(1−s_k−ϵ_k))."  [Only main theorem; no numeric bound.]

> Journal-version content check (grep over the whole 37-page text): zero occurrences of 10118, 41391,
> 1380, 15218, 1.306973, 0.001687, 0.030966, 0.009307, "Definition 67", "TwoCC", "H_low", "LabelDensity",
> "sibling". Baseline "1.3070319^(−n) … to 1.306995^(−n)" appears once (p. 5, HKZZ comparison).

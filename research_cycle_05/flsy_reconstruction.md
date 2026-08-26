# FLSY Reconstruction: "Multilinear Algebraic Branching Programs and the Min-Partition Rank Method"

**Reconstruction date:** 2026-08-21.
**Sources actually fetched and read (primary, not memory):**

- **[ECCC]** Full version: ECCC TR26-001, Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, Amir Yehudayoff, dated January 1, 2026, 40 numbered pages + title/contents (42 PDF pages). Downloaded from `https://eccc.weizmann.ac.il/report/2026/001/download` and read page-by-page as a PDF (all pages 1–40 read visually; the entire technical content was inspected). No revisions are listed on the ECCC report page (903 downloads as of fetch).
- **[CCC]** Published version: CCC 2026, LIPIcs vol. 383, Article 22, pp. 22:1–22:20, DOI 10.4230/LIPIcs.CCC.2026.22, published July 23, 2026. Downloaded from `https://drops.dagstuhl.de/storage/00lipics/lipics-vol383-ccc2026/LIPIcs.CCC.2026.22/LIPIcs.CCC.2026.22.pdf`; full text extracted with pdftotext and searched. (PDF metadata: "LIPIcs, Vol.383, CCC 2026", created 2026-07-21 with lipics-v2021.cls.)
- ECCC TR26-043 page, arXiv abs/2604.00746 page, ECCC author page for Deepanshu Kush, ECCC TR26-090 page, plus web searches (details in §7).

Notation note: the full version writes "mABP"; the published version writes "mlABP" for the same object. Below, statement numbers "X.Y" are ECCC full-version numbers; "published Theorem/Lemma N" are the LIPIcs continuous numbers. All quotations are verbatim from the fetched text (modulo restoring math symbols lost in text extraction, marked where relevant).

---

## 1. Verification of the imported statements

### 1.1 Definition of chain-balance and balanced-chain set systems

**ECCC Definition 1.2 (Balanced-chain set systems), p. 3 — verified verbatim from fetched PDF:**

> "Let X be a finite set with n elements and let 𝒳 ⊆ 𝒫(X) be a family of subsets of X. Denote by 𝒞(𝒳) the set of *maximal chains* of 𝒫(X) contained in 𝒳; i.e., a chain (C_0, …, C_l) is in 𝒞(𝒳) iff l = n and |C_i| = i for each i ∈ {0, …, l}.
> For a function f : X → {−1,1} which we will call a *partition*, and S ⊆ X, let f(S) := Σ_{x∈S} f(x). We say that f is *balanced* (or that f is a *balanced partition* of X) if f(X) = 0. We define the *chain-balance* of 𝒳 with respect to f as
> cbal_𝒳(f) := min_{(C_0,…,C_n) ∈ 𝒞(𝒳)} max_{i∈[n]} |f(C_i)|.
> We define the chain-balance of 𝒳 to be cbal(𝒳) := max_{balanced f : X → {−1,1}} cbal_𝒳(f).
> We say that 𝒳 is a *k-balanced-chain set system* if cbal(𝒳) ≤ k."

This matches the repository's "1-balanced-chain" notion exactly (maximal chain ∅ = C_0 ⊂ C_1 ⊂ … ⊂ C_n, |C_i| = i, each C_i ∈ 𝒳, every |f(C_i)| ≤ 1, for every balanced ±1 coloring). Note the chain must be *contained in 𝒳*, so ∅ and X must belong to 𝒳. The repository's N(n) is **exactly the paper's N(n)**: the proof of Theorem 3.3 (ECCC p. 17) literally opens "For every n ∈ ℕ, let N(n) be the minimum size of a 1-balanced-chain set system over [n]". [Verified.]

**ECCC Definition 1.4 ((ε,k)-balanced-chain set systems), p. 5 — verified verbatim:**

> "For ε ∈ [0,1] and k ∈ ℝ_{≥0}, we call an mABP set system 𝒳 an *(ε,k)-balanced-chain set system* if, for a uniformly random balanced f : X → {±1}, we have ℙ_f[cbal_𝒳(f) ≤ k] ≥ ε. Note that a k-balanced-chain set system is also a (1,k)-balanced-chain set system."

(Published Definition 5, p. 22:6, is identical, including the stray words "an mlABP set system 𝒳" — apparently a typo in both versions for "a set system 𝒳"; nothing in the definition uses an ABP.) [Verified. This matches the repository's usage: p_N := ℙ_f[cbal_{I(N,1)}(f) ≤ 1] and "(ε,k)-balanced-chain system" means ℙ_f[cbal ≤ k] ≥ ε.]

### 1.2 Definition of interval families

**ECCC Definition 2.1, p. 10 = published Definition 11, p. 22:12 — verified verbatim:**

> "For every n, m ∈ ℕ, we denote by 𝓘_m := 𝓘_{n,m} the *m-interval set system* over [n] defined as
> 𝓘_{n,m} := { I_1 ∪ … ∪ I_l | I_1, …, I_l are intervals of [n] and l ≤ m }."

With l = 0 allowed, ∅ ∈ 𝓘_{n,m}; and [n] ∈ 𝓘_{n,m}. So 𝓘_{n,1} = {∅} ∪ {[i,j] : 1 ≤ i ≤ j ≤ n} — exactly the repository's "ordinary one-interval family I(N,1) = all intervals of the linear order [N] (plus ∅)". [Verified; no discrepancy.] The paper also notes (ECCC p. 10 / published p. 22:12): "Assume that m ≤ n/2. … the size of the m-interval set system is at most |𝓘_{n,m}| ≤ (n/m)^{O(m)}."

The introduction (ECCC p. 4) uses 𝓘 = {[i,j] | 1 ≤ i ≤ j ≤ n} for the same family. Section 5.5 (ECCC p. 35) additionally defines the *permuted* interval family: "Given a bijection π : X → [n], we denote by 𝓘_{X,π} the set system consisting of intervals with respect to π contained in the set X. Formally, 𝓘_{X,π} := {{x_{π(i)}, x_{π(i+1)}, …, x_{π(j)}} | 1 ≤ i, j ≤ n}." [Verified.]

### 1.3 The interval theorem (the key import)

**ECCC Theorem 4.4 (Theorem 1.7), p. 19 — verified verbatim:**

> "**Theorem 4.4** (Theorem 1.7)**.** There is a universal constant c > 0 such that, for every sufficiently large even number n ∈ ℕ, the 1-interval set system 𝓘_{n,1} is not an (ε,k)-balanced-chain set system for ε > 2^{−cn^{1/5}} and k < n^{1/5}."

**Published Theorem 23 (Theorem 8), p. 22:17 — verified verbatim (pdftotext):**

> "Theorem 23 (Theorem 8). There is a universal constant c > 0 such that, for every sufficiently large even number n ∈ N, the 1-interval set system In,1 is not an (, k)-balancedchain set system for  > 2−cn^{1/5} and k < n^{1/5}."

**Verdict on the repository's import: EXACT MATCH, no discrepancy.** All details check out: universal constant c > 0; "for every sufficiently large **even** number n" (parity condition present); the exponent is genuinely n^{1/5} (both conditions: ε > 2^{−cn^{1/5}}, strict, and k < n^{1/5}, strict). The claimed numbering is also exactly right: ECCC Theorem 4.4 = ECCC intro Theorem 1.7 = published Theorem 23 = published intro Theorem 8. (Nuance: the ECCC *intro* statement, Theorem 1.7 on p. 6, is stated with an unspecified constant — "for ε ≥ 2^{−n^c} and k ≤ n^c" — while the published intro Theorem 8 already states "for any ε > 2^{−Ω(n^{1/5})} and k < n^{1/5}". The technical statements in both versions carry the 1/5.) The consequence imported by the repository, p_N = ℙ_f[cbal_{𝓘(N,1)}(f) ≤ 1] ≤ 2^{−cN^{1/5}} for large even N, follows immediately by taking k = 1 < N^{1/5}: otherwise 𝓘(N,1) would be a (p_N, 1)-balanced-chain system with p_N > 2^{−cN^{1/5}}, contradicting the theorem. [Verified inference, one line.]

Also relevant, the intro's worst-case fact (ECCC pp. 4, published p. 22:5): the "mountain–valley" partition f(j) = 1 for j ∈ [n/4] ∪ [(3n/4)+1, n], −1 otherwise, shows cbal(𝓘) ≥ Ω(n) in the worst case ("any chain in 𝒞(𝓘) contains a set S … |f(S)| ≥ Ω(n). Note that unbalance n/2 is the worst possible"). The published intro adds: "Our Theorem 8 shows … for most balanced partitions, I has chain-balance at least n^{Ω(1)}." [Verified.]

### 1.4 The worst-case-to-average-case lemma

**ECCC Lemma 2.3 (Lemma 1.5), p. 13 — verified verbatim:**

> "**Lemma 2.3** (Lemma 1.5)**.** Let n ∈ ℕ be an even number, and X be a set of n elements. Let l ∈ [n] and p ∈ (0,1]. If 𝒳 is a (p,l)-balanced-chain set system, over X, of size s, then there is an l-balanced-chain set system 𝒴, over X, of size O(sn/p)."

**Published Lemma 14 (Lemma 6), p. 22:13 — verified verbatim:** "Lemma 14 (Lemma 6). Let n ∈ N be an even number, and X be a set of n elements. Let l ∈ [n] and p ∈ (0, 1]. If X is a (p, l)-balanced-chain set system, over X, of size s, then there is an l-balanced-chain set system Y, over X, of size O(sn/p)." (Intro form, published Lemma 6: "If there is an (ε,k)-balanced-chain set system, over the set [n], of size s, then there is a k-balanced-chain set system, over the set [n], of size at most O(sn/ε).")

**Verdict: EXACT MATCH with the repository's import** ("Lemma 2.3 (Lemma 1.5), published as Lemma 14 (Lemma 6)"), and it is indeed a worst-case-to-average-case statement via random relabelings. Proof mechanism (ECCC pp. 13–14, read in full): take r := ⌈n/(p lg e)⌉ independent uniformly random permutations σ_1,…,σ_r of X and set 𝒴 := 𝒳 ∪ (∪_{i=1}^r σ_i𝒳) where σ_i𝒳 := {σ_i(S) | S ∈ 𝒳}. For any fixed balanced g and random π, g∘π^{-1} is a uniformly random balanced partition, so each σ_i "covers" g with probability ≥ p; ℙ_σ[some g ∈ B uncovered] < 2^n e^{−rp} < 1, and a union bound over all 2^n balanced partitions plus the probabilistic method gives a deterministic 𝒴 of size (r+1)s = O(sn/p) with cbal(𝒴) ≤ l. [Verified in full.]

### 1.5 Discrepancy flags

**No substantive discrepancy found between the repository's imported theorem
statements and the paper.**  Minor notes only: (i) the ECCC intro version of
the interval theorem (Theorem 1.7) uses an unnamed exponent c, with the 1/5
appearing in Theorem 4.4 / published Theorems 8 and 23; (ii) the theorem is
an "is not an (ε,k)-system" statement, equivalently
ℙ_f[cbal_𝓘(f) ≤ k] ≤ 2^{−cn^{1/5}}; (iii) Lemma 2.3 uses letters (p,l)
instead of (ε,k); (iv) balanced partitions require even n; and (v) the
Theorem 4.4 proof display has the strict-threshold boundary slip recorded
and repaired in §2 below.  Item (v) concerns the printed derivation, not the
published theorem statement.

---

## 2. Reconstruction of the proof of Theorem 4.4 / 1.7 (the interval theorem)

**One-line answer to "what is the actual mechanism":** it is an *anti-concentration result for the discrete Fréchet distance of two independent one-dimensional random walks*, proved by a milestone (pattern-avoidance) argument combined with lower-tail bounds for sums of first-passage times, obtained from Chernoff bounds applied to the associated counting process. It is neither a potential-function nor an entropy/compression argument, and the "min-partition rank method" of the title is the *algebraic motivation*, not the proof technique of this combinatorial theorem. The abstract itself (ECCC p. 1, verified): "we prove that two independent random walks are 'far' from each other in discrete Fréchet distance."

The proof has two independent components, Lemma 4.2 (reduction to Fréchet distance) and Lemma 4.3 (Fréchet anti-concentration), combined in a four-line proof of Theorem 4.4 (ECCC p. 19, verified):

> "Suppose 𝓘 := 𝓘_{n,1} is an (ε,k)-balanced-chain set system for any ε > 2^{−cn^{1/5}} and k < n^{1/5} with c := c_1/2. By Lemma 4.2, we have that ℙ_f[cbal_𝓘(f) ≤ n^{1/5}] ≤ O(n^{5/2}) max_{r∈[n]} ℙ_W[d_F(X_r, Y_{n−r}) ≤ n^{1/5}], and, by Lemma 4.3, max_{r∈[n]} ℙ_W[d_F(X_r, Y_{n−r}) ≤ n^{1/5}] ≤ exp(−c_1 n^{1/5}). Hence, ℙ_f[cbal_𝓘(f) ≤ k] ≤ ℙ_f[cbal_𝓘(f) ≤ n^{1/5}] ≤ O(n^{5/2}) exp(−c_1n^{1/5}) ≤ exp(−c_1n^{1/5}/2) = exp(−cn^{1/5}), a contradiction."

**Strict-threshold correction.**  The quoted source display has a harmless
boundary slip: at a perfect fifth power it enlarges the event from the
theorem's actual integer `k<n^{1/5}` to the non-strict event
`cbal≤n^{1/5}`.  The corrected derivation keeps the actual
integer `k<n^{1/5}` throughout, applies Lemma 4.2 at threshold
`k`, and applies the Lemma 4.3 argument at `k` (or at
any real `d` with `k<d<n^{1/5}`).  This restores the
strict boundary without changing Theorem 4.4's statement, exponent, or any
Cycle-5 use of the theorem.

### Step A. The chain-to-two-walks dictionary (Lemma 4.2 and its proof, ECCC §4.2, pp. 18–21) [verified in full]

**Definition 4.1 (discrete Fréchet distance), ECCC p. 18 = published Definition 20:** for l + r = n and X : {0,…,l} → ℝ, Y : {0,…,r} → ℝ, d_F(X,Y) := min_{α,β} max_{t∈[n]} |X(α(t)) − Y(β(t))|, minimum over nondecreasing α : {0,…,n} → {0,…,l}, β : {0,…,n} → {0,…,r} with α(0) = 0 = β(0), α(n) = l, β(n) = r, and for every t, α(t) ≤ α(t−1)+1, β(t) ≤ β(t−1)+1, and α(t) − α(t−1) + β(t) − β(t−1) = 1 (exactly one walk advances one step per time step — the "staircase" coupling; note this makes the parameterizations exactly the maximal chains below).

**Lemma 4.2 (Discrepancy and Fréchet distance), ECCC p. 18 — verbatim:** "Let n ∈ ℕ be an even number, and let 𝓘 := 𝓘_{n,1} be the 1-interval set system (Definition 2.1). Let l, r ∈ [n] such that l + r = n, and let W_{l,r} := (W_l, W_r) be a pair of two independent random walks W_l and W_r (Definition 3.1) of length l and r, respectively. For f being a uniformly random balanced partition, and W := (X,Y) = W_{n,n}, and X_l := X↾_{{0,…,l}} and Y_r := Y↾_{{0,…,r}}, we get that, for every k ∈ ℝ, ℙ_f[cbal_𝓘(f) ≤ k] ≤ O(n^{5/2}) max_{r∈[n]} ℙ_W[d_F(X_r, Y_{n−r}) ≤ k]."

**Proof mechanism (pp. 19–21):** A maximal chain of intervals starts at C_1 = {s} (s = first element added) and grows one element per step at the left or right end; let e be the last element added. The chain element of size m decomposes as R = S_+(m) ∪ S_−(m), the parts on the two sides of s (formally R∩P and R∩N for the cyclic interval P = [s,e] with s+1 ∈ P — the cyclic-interval bookkeeping only uniformizes the endpoint cases). Define the two "growth walks" X(i) := f([s, s+i]) (length l = |P|) and Y(j) := −f([s−j, s−1]) (length r = n − l). Then f(C_j) = f(S_+) + f(S_−) = X(α) − Y(β), and *the chain is exactly a staircase parameterization*; hence "the chain can be interpreted as an 'alignment' of these two random walks that ensures that they stay within distance k at all time steps, or equivalently, these two random walks are at distance at most k from each other in discrete Fréchet distance" (ECCC p. 9, verified). This yields, for each (s,e), an **injection** from {balanced f with a k-balanced chain whose first/last added elements are s,e} into {(X,Y) walk pairs of lengths (l_{s,e}, r_{s,e}) with d_F(X,Y) ≤ k}. Finally (p. 21, displayed chain of inequalities, verified): union bound over the ≤ n² pairs (s,e), and replacement of the uniformly random *balanced* f by a fully uniform g at cost O(n^{1/2}) (since ℙ[g balanced] = Θ(n^{−1/2})): ℙ_f[cbal_𝓘(f) ≤ k] ≤ O(n^{1/2}) Σ_{s,e} ℙ_g[g ∈ 𝓕_{s,e}] ≤ O(n^{5/2}) max_{l∈[n]} ℙ_W[d_F(X_l, Y_{n−l}) ≤ k]. Under uniform g the two growth walks are restrictions of g to disjoint coordinate sets, hence genuinely independent random walks.

### Step B. Fréchet anti-concentration (Lemma 4.3 and its proof, ECCC §§4.3–4.4, pp. 21–25) [verified in full]

**Lemma 4.3 (Fréchet distance of two random walks), ECCC p. 18 — verbatim:** "There is a positive constant c_1 ∈ ℝ such that, for every sufficiently large n ∈ ℕ, and every l := l(n) ∈ [n], and every ε := ε(n) ∈ (0, 1/4) such that n^{1/4−ε} ≥ (2/3) ln n, we have, for (X,Y) := W = W_{l,n−l}, ℙ_W[d_F(X,Y) < n^{1/4−ε}] ≤ exp(−c_1 · min{n^{1/4−ε}, n^{4ε}})."

Supporting lemmas, all proved in §4.3 [each verified]:

- **Lemma 4.5 (first-passage tail):** for a random walk g of length n, F_δ := inf{t > 0 | g(t) = δ}; for Ω(δ²) ≤ z ≤ n/2, ℙ_g[F_δ ≥ z] = Θ(δ/√z). (Classical ballot-type computation with Stirling; refs. Feller and Bhattacharya–Waymire.)
- **Lemma 4.6 (lower tail for sums of first-passage variables):** there is c_4 > 0 such that if kδ² ≤ c_4 n and (kδ)² = ω(n), then for k independent copies F^{(1)},…,F^{(k)} of F_δ: ℙ[Σ_{i=1}^k F^{(i)} ≤ n] ≤ exp(−Ω((kδ)²/n)). Proof: the counting process C_t := #{i : F^{(i)} ≥ t} is Binomial(k, p_t) with p_t ≥ ckδ/√t by Lemma 4.5; if the sum is ≤ n then C_t ≤ n/t; choose t := (2n/(ckδ))² and apply Chernoff to get exp(−Ω(kδ/√t)) = exp(−Ω((kδ)²/n)).
- **Lemma 4.7 (milestones / spread sequence):** for Δ ≥ 2 log n, call {x_i}_{i∈[l]} ⊆ [n] a (g,Δ)-sequence if |g(x_i) − g(x_{i−1})| ≥ Δ (x_0 := 0); L_Δ := max length. Then ℙ_g[L_Δ < n/(c_3Δ³)] ≤ exp(−Ω(Δ)). Proof: D_Δ := first time |g| reaches Δ from a fresh start satisfies ℙ[D_Δ > c_3Δ³] ≤ 2^{−Δ} (split c_3Δ³ steps into Δ segments of length c_3Δ²; each segment escapes [−2Δ,2Δ] with probability > 1/2 by Lemma 4.5); then sum n/(c_3Δ³) independent copies.

**Proof skeleton of Lemma 4.3 (§4.4, informal outline quoted from p. 24, then formal):** W.l.o.g. X is the longer walk (length ≥ n/2). Set d := n^{1/4−ε} (the target Fréchet distance), Δ := 3d, L := n/(2c_3Δ³).
1. By Lemma 4.7, except with probability exp(−Ω(Δ)) = exp(−Ω(d)), X contains a milestone sequence z_1, …, z_L of values with consecutive gaps |z_i − z_{i−1}| ≥ Δ. ("We … identify a pattern in it that h can not possibly follow" — ECCC p. 9.)
2. Condition on such an X. If d_F(X,Y) < d then, extracting from the staircase coupling the times when X sits at its milestones, Y must come within distance d of z_1, …, z_L *in order*, within its r ≤ n steps. At the paper's nominal/asymptotic level, the waiting time to go from (within d of) z_{i−1} to (within d of) z_i is written as dominating a fresh first-passage variable F_{Δ−2d} = F_d (translation invariance of the walk; the needed net displacement is ≥ Δ − 2d = d). So the paper writes the total-time domination as a sum of L copies of F_d.
3. In the same paper-level shorthand, Lemma 4.6 is invoked with k := L = Θ(n/d³) and δ := d (hypotheses: kδ² = Θ(n/d) ≤ c_4n ✓, kδ = Θ(n/d²) = Θ(n^{1/2+2ε}) = ω(√n) ✓), giving exp(−Ω((kδ)²/n)) = exp(−Ω(n/d⁴)) = exp(−Ω(n^{4ε})).  This `F_d` notation is **not** an exact integer-parameter proof when real `d=n^{1/4−ε}` is nonintegral and is not retained as an alternative SEG derivation.  The operative repository proof uses the analytic real-threshold estimate and the integer level `δ=⌈d⌉` described in §3(b) and proved in `audits/cycle05_seg_deep_independent_validation.md` §D.
4. Total: ℙ[d_F < d] ≤ exp(−Ω(d)) + exp(−Ω(n/d⁴)) ≤ exp(−c_1 min{n^{1/4−ε}, n^{4ε}}). ∎

**Source of the 1/5 exponent [verified + inference]:** balance the two failure terms d and n/d⁴: d = n/d⁴ ⟺ d = n^{1/5}, i.e., ε = 1/20 in Lemma 4.3 (min{n^{1/4−ε}, n^{4ε}} maximized at 1/4 − ε = 4ε). Structurally, the 4 in n/d⁴ decomposes as: milestones must be spaced ~Δ³ = Θ(d³) time steps apart (Δ² is the *typical* first-passage time; the extra factor Δ ensures each milestone appears except with probability 2^{−Δ}, which is what caps the first term at exp(−Ω(d))), giving L = n/Θ(d³) milestones each forcing displacement Θ(d), so (Lδ)²/n = n/Θ(d⁴). The polynomial factor O(n^{5/2}) from Lemma 4.2 (n² for the (s,e) union bound, n^{1/2} for un-conditioning balancedness) is absorbed into the exponential. If milestones could be taken at typical spacing d², the same computation would give exponent 1/3 rather than 1/5; the paper does not claim optimality of 1/5 (and nothing in the paper claims the true answer for cbal of intervals under random f is n^{1/5±o(1)}; the published intro says only "chain-balance at least n^{Ω(1)}" for most partitions).

**Relation to CKSS24 [verified, ECCC p. 6 / published p. 22:8]:** "the above is a considerable generalization of a recent result of Chatterjee, Kush, Saraf and Shpilka [CKSS24], whose results imply such a bound for the subset 𝓘_0 of 𝓘 that consists only of intervals of the form [i] … The set system 𝓘_0 contains just one maximal chain, while the set system 𝓘 contains *exponentially* many chains, which makes the arguments from [CKSS24] inapplicable for 𝓘." I.e., the prefix-only case is a single walk staying in a tube (classical); FLSY's contribution is handling the exponential adaptivity of two-ended growth, which is exactly the Fréchet minimization over staircases.

---

## 3. Segment version (the key question)

**Question:** does/could the proof bound ℙ[random balanced coloring admits a k-balanced interval-growth path from a FIXED interval A to a FIXED (or arbitrary) B ⊇ A, |B∖A| = L] ≤ 2^{−cL^{1/5}} for k < L^{1/5}?

**Answer: yes, but this is NEW REPOSITORY MATHEMATICS, not a theorem
published verbatim and not a zero-change/cosmetic restatement.**  FLSY's
probability engine localizes, while the fixed-segment grid, offset base case,
integer rounding, and full cyclic endpoint reduction require separate
proofs.  Those proofs are in
`audits/cycle05_seg_deep_independent_validation.md` §D, checked in
`audits/cycle05_seg_arms_length_referee.md`, and corrected finally
in `audits/cycle05_sol_final_cross_model_validation.md` §§5.4--5.8.
Details:

**(a) What the chain-from-∅ is actually used for.** In the entire proof, the anchoring appears in exactly three places, all in Lemma 4.2's reduction, none in Lemma 4.3:
1. C_1 = {s} identifies a *single anchor point* s from which the interval grows two-sidedly; the union bound over (s,e) ∈ [n]² costs O(n²). — In the segment version A is fixed, so the two growth directions are anchored at the two ends of A; *no union bound over s is needed at all*. A maximal chain from A to B = [a′,b′] ⊇ A = [a,b] inside 𝓘 automatically consists of intervals A ⊆ C ⊆ B, and decomposes canonically into a left-extension walk U(i) := f([a−i, a−1]), i ≤ L_left = a − a′, and a right-extension walk V(j) := f([b+1, b+j]), j ≤ L_right = b′ − b, with L_left + L_right = L.
2. Both published walks start at value 0 and the chain-balance values f(C_j) are anchored at f(∅) = 0. — In the segment version f(C_j) = f(A) + U(i) + V(j); setting X(i) := f(A) + U(i), Y(j) := −V(j), the exact grid dictionary identifies the k-balanced growth condition with d_F(X,Y) ≤ k, now with initial offset X(0) − Y(0) = f(A). Since A itself is in the chain, |f(A)| ≤ k is part of the event.
3. The balancedness of f is removed at cost O(√n). — Identical trick in the segment version: for f a random balanced coloring of the ambient [N], pass to uniform g at cost O(√N) (ℙ[g balanced] = Θ(N^{−1/2})); under uniform g, U, V, and f(A) live on disjoint coordinate sets and are mutually independent — exactly the independence Lemma 4.2 needs.

**(b) What localizes and what must be proved.**  The published milestone and
first-passage mechanism uses only fresh increments, translation, reflection,
and strong Markov; it has no dependence on absolute position, earlier/future
chain history, or the final value.  The offset extension nevertheless has a
real base-case obligation.  With `d=L^{1/5}`,
`Δ=3d`, integer milestone gap `⌈3d⌉`, and
`|σ'|≤d`,

```text
|z_1-h_0| ≥ ⌈3d⌉-|σ'| ≥ 2d>d,
```

so the first chaser time is positive.  Later legs use the same maintained
invariant.  To make every parameter legal, the repository proof uses
tracking radius `⌊d⌋` and integer first-passage level
`δ=⌈d⌉`, justified by
`⌈3d⌉−2⌊d⌋≥⌈d⌉`.  It proves W1 directly for real Chernoff
thresholds, and proves the real-`Δ` milestone estimate with
`⌊Δ⌋` blocks and target `⌈2Δ⌉`.  These are proof
changes, not citation substitutions.

**(c) Resulting SEG statement (reconstructed, not in the paper).**  Valid
explicit constants are

```text
c=min{1/2,(1/6)^2/(8·27648^2)},
C=6,
L_0=⌈13824^(5/2)⌉=22,469,029,418.
```

For `L≥L_0`, fixed linear
`∅≠A⊆B⊆[N]`, and integer `1≤k<L^{1/5}`, a random
coloring conditioned on admissible total `σ`,
`|σ|≤1` and `σ≡N (mod 2)`,
has a k-balanced interval segment from A to B with probability at most
`C√N exp(−cL^{1/5})`.  The unconditioned form omits
`√N`; varying B at fixed added length costs `L+1`.
A proper cyclic B is cut outside B.  When `B=Z_N`, for each
terminal split `u+v=L−1` the last point is appended to one
extension sequence, giving disjoint walk lengths `(u+1)+v=L`;
apply the length-L estimate and then the L-way union (cost at most
`L+1`).  This avoids the false
length-`L−1` argument at `L=j^5+1`.

**(d) What genuinely breaks / limits.**
1. **Small L regime:** the bound is vacuous when L ≤ (C log N)^5, because the O(√N) unconditioning factor (and any union bound over segment positions in a larger argument) swamps 2^{−cL^{1/5}}. Any DAG/composition argument over many segments must budget for one poly(N) factor per union-bounded choice.
2. **Hypotheses of Lemma 4.3 in terms of L:** needs L^{1/4−ε} ≥ (2/3) ln L and L sufficiently large; with ε = 1/20 this is L^{1/5} ≳ ln L — harmless for large L.
3. **Balanced ambient coloring vs. balanced segment:** for f balanced on [N] with L ≪ N, the restriction of f to B∖A is *not* balanced and is slightly negatively correlated across coordinates; the paper's own O(√N)-unconditioning step handles this cleanly (pass to uniform g first), so no new argument is needed — but the price is √N, not √L. If one instead wants the probability under a *conditioned* segment sum (e.g., f(B∖A) = σ fixed), a fresh (routine but not written) local-CLT argument replacing the Θ(N^{−1/2}) estimate would be needed.
4. **One-sided degenerate case:** if B extends A on one side only (L_right = 0 say), the Fréchet machinery degenerates: the event is a single walk of length L confined to a width-2k tube around −f(A), with probability ≤ exp(−Ω(L/k²)) by classical confinement — stronger than exp(−cL^{1/5}) for k < L^{2/5}. The Fréchet bound is needed *only* because two-sided growth may interleave adaptively (with knowledge of the whole coloring). So a segment version is if anything easier at extreme splits; Lemma 4.3 as stated already covers all splits uniformly.
5. **What is independently proved in the repository:** the segment grid
normal form, the offset-tolerant anti-concentration lemma including its first
leg, every integer/real threshold convention, the exact tail arithmetic,
and the cyclic-full length-L encoding.  None is stated verbatim in FLSY.

**Bottom line:** SEG is **NEW BUT PROVED IN THIS REPOSITORY** from FLSY's
published probability machinery.  It gives stretched-exponential decay in
the added length L with the displayed ambient-conditioning and endpoint
factors.  When a later application wants those polynomial factors absorbed,
it must impose the corresponding `L^{1/5}≫log N` regime; that is
an application-level condition, not an extra hypothesis in SEG itself.

---

## 4. Upper bound N(n) ≤ n^{O(log n/log log n)} and the Ω(n²) lower bound

**Both are from this paper.** [Verified.]

**Upper bound = ECCC Theorem 1.6 = Theorem 3.3 = published Theorem 7 = Theorem 18.** Verbatim (ECCC p. 16): "For every sufficiently large even number n ∈ ℕ, there is a 1-balanced-chain set system 𝒳_n over [n] of size n^{O(ln n/ln ln n)}." The paper stresses this is the first superpolynomial improvement over the "easy" n^{O(log n)} bound (which follows either from Raz via Theorem 1.3, or directly from Theorem 2.2 below).

**The construction (proof of Theorem 3.3, ECCC p. 17, read in full) is recursive/hierarchical AND randomized (probabilistic-method), with structure "prefix ⊙ translated recursive system, then symmetrize by random permutations":**
1. Let N(n) = min size of a 1-balanced-chain system, A_t an optimal system on [t]. Define B_m := { [1,i] ⊙ A_t | t ∈ [m], 0 ≤ i ≤ n−t }, where [1,i] ⊙ A_t := { [1,i] ∪ {i+j | j ∈ R} | R ∈ A_t } — i.e., a prefix interval [1,i] followed by a translated copy of the recursive system on the next t points. |B_m| ≤ n²N(m).
2. Random-walk fact: view a uniformly random balanced f on [n] as a random bridge; let E_m = event that the maximum gap between consecutive zeros of the bridge is ≤ m. **Lemma 3.2 = "Lemma 10 from [CER85]"** (Csáki–Erdős–Révész 1985, *On the length of the longest excursion*): for a random bridge B of length 2n and a ≥ n^{2/3}, ℙ_B[λ(B) ≤ 2a] = C(n,a) min{(n+1)^{−1/2}, a^{−1/2}} exp(−βn/a) with C_1 ≤ C(n,a) ≤ C_2. With m := 2⌈n/(2 ln n)⌉ this gives δ_m := ℙ_f[E_m] ≥ c/n^{b+1/2} ≥ 1/poly(n).
3. If f ∈ E_m, then B_m contains a 1-balanced maximal chain for f: between consecutive zeros z_i, z_{i+1} of f (gap ≤ m), use [1,z_i] ⊙ A_{z_{i+1}−z_i} and the recursive 1-balancedness of A on the gap, concatenating over gaps ("we identify … f … as a uniformly random walk … A random walk that returns to 0 many times would give us many intervals … does contain a *non-maximal* chain of balanced intervals ∅ ⊆ [i_1] ⊆ … ⊆ [i_r] = [n] where each subsequent interval … adds at most m elements … we only need to add sets to 'fill in' the missing sets" — ECCC p. 8, verified). So B_m is a (δ,1)-balanced-chain system with δ ≥ 1/poly(n).
4. Apply **Lemma 2.3** (worst-case-to-average, random permutations): N(n) ≤ O(|B_m|·n/δ) ≤ n^d · N(n/ln n). Solving the recursion: N(n) ≤ n^{O(ln n/ln ln n)} — the log n/log log n is exactly the recursion depth (each level shrinks n to n/ln n and pays poly(n)).

**Is it "a union of interval families of multiple orders (a union over permutations π of {intervals in order π})"?** Not literally, and the paper explicitly flags this (Remark, ECCC p. 9, verbatim): "While we only used the family of intervals in the above construction, it should be noted that the overall family constructed above consists of sets that are very different from intervals. This is because we need to carry out the aforementioned average-case to worst-case argument at each stage, which is done by randomly permuting the elements in the sets. This does not preserve the property of being an interval. It seems interesting to derandomize this 'construction'." Accurate description: it is a **log n/log log n-level hierarchy, where each level is a union over poly(n) random permutations of {prefix-interval ∪ shifted copy of the previous level}**. At the top level (before symmetrization) the sets are unions {prefix of the identity order} ∪ {permuted recursive blocks}; after one application of σ_i these are no longer intervals in any single order, so the final system is a union over *compositions* of permutations of interval-derived sets — richer than a one-level union ∪_π 𝓘_{[n],π}. Whether a one-level union of single-interval families over poly-many orders can be a 1-balanced-chain system is not addressed in the paper (see §5). Also note the construction is non-uniform (probabilistic method at every level); derandomizing it is one of their open problems.

**Lower bound Ω(n²): ECCC Remark in §2.1, pp. 12–13 = published Observation 13.** Verbatim (ECCC p. 12): "we can prove a Ω(n²/k) lower bound for the size of any k-balanced-chain set system for k ≤ n/5. More specifically, a result by Alon, Kumar, and Volk [AKV20] can be rephrased as follows: for every k ∈ ℕ and sufficiently large n ∈ ℕ, if a collection S_1, …, S_m ⊆ [n] of sets satisfies that 2k ≤ |S_i| ≤ n − 2k for every i ∈ [m] and, for every balanced partition f of n, there is an i ∈ [m] such that |f(S_i)| ≤ 2k, then m ≥ Ω(n/k)." The proof of the corollary is a level-by-level slicing: for a 2k-balanced-chain system 𝒳, each level set 𝒳_l := {S ∈ 𝒳 : |S| = l}, l ∈ {2k, …, n−2k}, is a "balancing set system" in the AKV20 sense, hence has size Ω(n/k); summing over the ≥ n − 4k levels, |𝒳| ≥ Ω((n−4k)n/k). For k = O(1) this is Ω(n²). So the repository's claimed range Ω(n²) ≤ N(n) ≤ n^{O(log n/log log n)} is exactly the paper's Theorem 1.6 + §2.1 Remark. [Verified. Note it is a *rephrasing* of AKV20 (Combinatorica 2020, "Unbalancing sets and an almost quadratic lower bound for syntactically multilinear arithmetic circuits"), not a new proof; the AKV20 balancing-set bound Ω(n/k) per level is what the paper's intro calls "tight … via intervals" for the non-chain version.]

---

## 5. Multi-order and multi-interval statements

**w > 1 disjoint intervals in a single order — yes, treated.** Definition 2.1/11 defines 𝓘_{n,m} for all m (unions of ≤ m intervals of ONE fixed linear order), with |𝓘_{n,m}| ≤ (n/m)^{O(m)}. The one theorem about it:

> **ECCC Theorem 2.2 = published Theorem 12 [verified verbatim]:** "For every even number n ∈ ℕ, the chain-balance of the (2⌈lg n⌉)-interval set system is 1."

I.e., **𝓘_{n, 2⌈lg n⌉} is a 1-balanced-chain set system**, of size n^{O(log n)} — this is the "easy" upper bound, proved by an explicit deterministic induction (ECCC pp. 11–12, read in full): grow symmetrically from both ends of the current window when no zero of the restricted coloring is available, find the nearest point t_1 with f([l_1,t_1]) = 0, recurse on the half-length window; each recursion level adds 2 intervals, depth lg n. (The published version omits this proof, deferring to the full version — published p. 22:12: "We omit this proof but it can be found in the full version of this paper.") **Notable gap the paper leaves open (relevant to the repository): nothing is proved about 𝓘_{n,m} for 1 < m < 2⌈lg n⌉ — in particular no (ε,k) negative result for w = 2 or any constant w. Theorem 4.4's negative result is stated and proved only for m = 1.** Whether the Fréchet argument extends to constant w (each chain now = 2w interleaved growth walks, Fréchet-type alignment of a walk against a *set* of milestone sequences) is not discussed anywhere in the paper. [Verified absence: I read every section; §4 mentions only 𝓘_{n,1}; §6 does not raise the m-interval question explicitly beyond the general gap question.]

**Unions over several orders/permutations — the Σ_π argument does not analyze hybrid chains; Lemma 2.3 separately constructs a literal union.** Section 5.5 (ECCC pp. 35–37 = published §5.4) defines 𝓘_{X,π} (intervals w.r.t. a bijection π, quoted in §1.2 above), π-interval mABPs (layered mABPs whose layer-i vertices are labeled with size-i sets from 𝓘_{X,π}), and the model **Σ_π mABP := sums of interval mABPs "(possibly with respect to different orderings π)"** (footnote 7: notation from CKSS24 with subscript π added). The result:

> **ECCC Theorem 5.14 (Corollary 1.8) = published Corollary 9 [verified]:** "Let n ∈ ℕ be sufficiently large even number, and X be a set of n variables, and 𝔽 be any field. Let P be a full rank polynomial in 𝔽[X]. If 𝒜 is a Σ_π mABP of size s computing P, then s ≥ 2^{Ω(n^{1/5})}."

**Proof mechanism (ECCC pp. 36–37, verified — important for the repository's multi-order question):** the multiple orders in §5.5 are handled by *rank subadditivity plus averaging*, NOT by analyzing hybrid chains in the union set system ∪_i 𝓘_{X,π_i}. Verbatim skeleton: 𝒜 = 𝒜_1 + … + 𝒜_t, each 𝒜_i a π_i-interval mABP computing P_i; 2^{n/2} = rank(M_f(P)) ≤ Σ_i rank(M_f(P_i)) for every balanced f, "hence by averaging, there is an i such that P_i is (1/t, 1/t)-almost full-rank. Since 𝒜_i is layered with valid labelling comming from the set-system 𝓘_{X,π_i}, Lemma 5.11 implies that 𝓘_{X,π_i} is a (1/t, lg(st))-balanced-chain set-system. Note that t ≤ s and hence 𝓘_{X,π_i} is a (1/s, 2 lg(s))-balanced-chain set-system. On the other hand, it follows from Theorem 4.4 that 𝓘_{X,π_i} is *not* an (ε,k)-balanced-chain set-system, for k < n^{1/5} and some ε = exp(−Ω(n^{1/5})). This implies that s ≥ exp(Ω(n^{1/5}))." So the single-order interval theorem is applied **"almost as a black box"** (the paper's own phrase in the published Further-questions section) to one summand at a time.

That is not the paper's only encounter with literal unions.  Lemma 2.3 separately defines `𝒴=𝒳∪⋃_i σ_i𝒳`, exactly a literal union of relabeled copies, and proves an upper bound on its chain-balance by ensuring that every coloring has a **pure witness chain inside one copy**.  It does not classify provenance, compare pure and hybrid acceptance, or rule out additional chains that hop among copies.  Thus §5.5/Σ_π supplies no hybrid-chain analysis, while Lemma 2.3 supplies a one-sided union construction and chain-balance bound without such an analysis.  A union of t single-interval orders remains different from 𝓘(N,w), and FLSY's w-interval result (Theorem 2.2) concerns w disjoint intervals in ONE order, yet a third object.

**The set-multilinear variant (ECCC §5.6, p. 37):** both directions of Theorem 1.3 carry over with base-N logarithms; "In the interesting case that N = n^{Θ(1)} … For any c, there is a set-multilinear ABP of size n^{O(c)} computing a full-rank polynomial if and only if there is an O(c)-balanced-chain set-system of size n^{O(c)}" — a perfect characterization in the set-multilinear setting. [Verified.]

**Open problems section — ECCC Section 6 "Further questions" (p. 37), complete contents [verified]:**
1. "Can we close the gap between the lower bound Ω(n²/k) and upper bound n^{O(ln n/ln ln n)} for the size of k-balanced-chain set systems?"
2. "Can we obtain a uniform construction of full rank multilinear ABPs of size n^{o(ln n)}? A possible approach for this question is a derandomization of our construction. In particular, it is sufficient to derandomize our application of the worst-case to average-case reduction, which uses random permutations of a given set system (Lemma 2.3)."

The **published** Further-questions section (p. 22:19, verified from pdftotext) is an expanded version, adding two remarks worth recording: "Both directions are interesting since Theorem 3 shows that sufficiently high lower bounds on the size of balanced-chain set systems imply new lower bounds for the size of mlABPs computing full rank polynomials, and a poly(n) upper bound implies that the min-partition rank method cannot be used to prove superpolynomial lower bounds for mlABPs. **Can we prove n^{Ω(1)} lower bounds for the chain-balance of other families of restricted set systems?** In Theorem 8, we showed an Ω(n^{1/5})-lower bound for the chain-balance of intervals set systems, and applied it almost as a black box to obtain an exponential lower bound against the Σ_π mlABP model. Thus, it is natural to ask whether we can reduce the problem of showing lower bounds for other interesting restricted versions of mlABPs to the question of showing lower bounds for the chain-balance of restricted set systems." Plus the derandomization question (published wording cites Lemma 14 and allows field extensions "as the constructions in [15, 7]").

---

## 6. Motivation: N(n)-type quantities vs. mABP lower bounds (one paragraph)

The paper's stated motivation (ECCC §1, pp. 1–5; verified) is that the min-partition rank method Γ(P) := min_Π rank(M_Π(P)) over equipartitions (Raz) underlies essentially all multilinear lower bounds, yet the best mABP bound is only the near-quadratic RSY08a/AKV20 bound obtained by applying the layer-wise decomposition P = Σ_{v in layer i} L_v·R_v; FLSY observe the decomposition holds for *any* source–sink vertex cut, and by a graph-theoretic duality the failure of all cuts is equivalent to an a–b path whose vertex-sets form a *chain* of subsets that is balanced w.r.t. the partition — whence Definition 1.2 and the two-directional near-equivalence **Theorem 1.3** (published Theorem 3): "Let s = s(n) be any growing function of n with s ≥ n. If any (log s)-balanced-chain set system has size at least s, then any mABP computing a full-rank polynomial has size at least s^{Ω(1)}. Conversely, if there is an O(1)-balanced-chain set system of size s, then there is an mABP computing a full-rank polynomial of size at most s·poly(n)" — with a *perfect* characterization in the set-multilinear case (ECCC §5.6) and, as the published open-problems section states explicitly, the contrapositive stakes: superpolynomial lower bounds on N(n)-type quantities would give the first superpolynomial mABP lower bounds via this method, while a poly(n) upper bound on N(n) would prove the min-partition rank method *cannot* give superpolynomial mABP lower bounds (this is precisely what the withdrawn TR26-043 claimed, see §7). Their Theorem 1.6 (N(n) ≤ n^{O(log n/log log n)}) already recovers, non-uniformly, the DMPY12 superpolynomial separation between mABPs and multilinear formulas (Corollary 5.7), and Theorem 4.4 + Theorem 5.14 give a 2^{Ω(n^{1/5})} lower bound for sums of interval mABPs, generalizing CKSS24's ordered set-multilinear ABP bound.

---

## 7. Follow-up work and status of the withdrawn claim (as of 2026-08-21)

**Withdrawn claim — arXiv:2604.00746 = ECCC TR26-043: confirmed WITHDRAWN, no replacement.** [Verified from fetched arXiv and ECCC pages today.]
- **Paper:** Deepanshu Kush, "An Unconditional Barrier for Proving Multilinear Algebraic Branching Program Lower Bounds", arXiv:2604.00746, v1 April 1, 2026; ECCC TR26-043, April 1, 2026. The abstract (fetched verbatim from arXiv) claimed exactly the barrier direction: "We show that the min-partition rank method cannot prove superpolynomial mABP lower bounds: there exists a full-rank multilinear polynomial computable by a polynomial-size mABP. … Our proof resolves an open problem of Fabris, Limaye, Srinivasan, and Yehudayoff (ECCC 2026), who showed that the power of this method is governed by the minimum size N(n) of a combinatorial object called a 1-balanced-chain set system, and proved N(n) ≤ n^{O(log n/log log n)}. We prove N(n) = n^{O(1)} by giving the chain-builder a binary choice at each step, biasing what was a symmetric random walk into one where the imbalance increases with probability at most 1/4; a supermartingale argument combined with a multi-scale recursion yields the polynomial bound."
- **Withdrawal:** arXiv v2, May 11, 2026, is a withdrawal notice (1 KB): "An anonymous referee pointed out a gap in the proof of Lemma 4.1: the bound on the forced probability holds unconditionally but not conditionally on the filtration F_t, which is what the supermartingale argument requires." The ECCC page shows Revision #1 (May 11, 2026) acknowledging the same gap ("a gap in the proof of Lemma 4.1"; ECCC has no formal withdrawal mechanism, so the report page remains up with the acknowledging revision).
- **Status today (2026-08-21):** still withdrawn — arXiv lists only v1 and v2 (no v3); Kush's ECCC author page (fetched today) lists TR26-043 as his only 2026 report, "Revised (1 revision)", with no successor report; web searches for a replacement or repaired proof ("Kush balanced-chain … replacement", "1-balanced-chain set system … 2026") surfaced nothing newer. **Consequence: N(n) = n^{O(1)} is NOT established; the FLSY range Ω(n²) ≤ N(n) ≤ n^{O(log n/log log n)} stands as the state of the art.** (Flag: the claimed technique — biasing the chain-builder's binary choice to fight the symmetric walk, supermartingale + multi-scale recursion — is exactly the kind of adaptive-choice argument the repository should treat as *plausible but unproven*; the identified gap is a conditioning/filtration error, i.e., the per-step "forced probability ≤ 1/4" bound was not valid conditionally on the past.)

**Other follow-ups citing/improving FLSY:** searches ("balanced-chain set system"/"chain-balance" 2026 ECCC; Fabris Limaye Srinivasan Yehudayoff citations; "1-balanced-chain" arXiv 2026) found **no** published improvement of either the interval theorem (n^{1/5}), the upper bound n^{O(log n/log log n)}, or the Ω(n²) lower bound as of today. TR26-043 (above) is the only work found that directly attacks the FLSY open problem, and it is withdrawn. ECCC TR26-090 (Boyapati–Chillara–Vempati, "Multilinear Formula Lower Bounds for Sparse Determinants", June 2, 2026), surfaced by keyword search, does not cite TR26-001 (verified by fetch) and is in the Raz partial-derivatives line, not the balanced-chain line. No probability-theory follow-up on the random-walk Fréchet-distance lemma was found either. ECCC TR26-001 itself shows no revisions since January 1, 2026. [All: verified searches; absence-of-results claims are of course only as good as the searches run — queries and sources listed above.]

Related prior work referenced for context (from the paper's own comparisons, verified in the fetched text): CKSS24 = Chatterjee–Kush–Saraf–Shpilka, "Lower bounds for set-multilinear branching programs", CCC 2024 (LIPIcs 300, 20:1–20:20) — the ordered/prefix special case; BDS25 = Bhargava–Dwivedi–Saxena, TCS 2025 — smABP lower bounds for low degree imply general ABP lower bounds; AKV20 — the Ω(n/k) balancing-set bound behind the Ω(n²).

---

## Summary of Tasks 3 and 4

**Task 3 (segment version):** FLSY publishes the translation-invariant
milestone/first-passage engine, but not SEG.  SEG is a new repository
derivation with proved grid, offset-first-leg, rounding, tail, and
cyclic-full obligations; its exact provenance and constants are recorded in
§3 above and the three cited audits.  **Task 4 (upper bound):**
N(n) ≤ n^{O(log n/log log n)} is FLSY's own Theorem 1.6/3.3, proved by a
log n/log log n-depth recursion in which level i takes the family {prefix
[1,i] ∪ shifted copy of the level-(i+1) system}, uses the
Csáki–Erdős–Révész longest-excursion bound to obtain inverse-polynomial
average-case success, and symmetrizes with random permutations via Lemma
2.3.  It is hierarchical and randomized, explicitly not a one-level union
of interval families; the Ω(n²) lower bound for O(1)-balance is the
level-slicing consequence of the Alon–Kumar–Volk balancing-set bound.

# SS Lifting-Import Ledger — Jiang–Cai arXiv:2607.10697v1, LIFTING layer

Hostile independent validation of the LIFTING-layer imports of Jiang–Cai (JC), "A Better
Analysis For PPSZ For 3-SAT" (arXiv:2607.10697v1, July 2026), against the primary sources.
Audit date: **2026-08-25**. Method: every source quote below was extracted from a file fetched
and hashed on the audit date (see `frozen_sources/ss_manifest.txt`); nothing is quoted from
memory. JC quotes are from the frozen source
`frozen_sources/arxiv_src/a_better_analysis_for_ppsz_3_.tex` (compiled numbering
cross-checked against `frozen_sources/arxiv_2607.10697v1.pdf`).

## 0. Sources fetched and versions used

| tag | file (in `frozen_sources/`) | what it is | sha256 (prefix) |
|---|---|---|---|
| **SS-J** | `ss_springer_00037-024-00259-y.pdf` | Scheder–Steinberger, *comput. complex.* **33**:13 (2024), pp. 1–48, **journal version, open access (CC "The Author(s) 2024"), complete 48 pp.** Fetched from `link.springer.com/content/pdf/10.1007/s00037-024-00259-y.pdf` | `20eae9e7…` |
| **SS-C** | `ss_ccc2017_LIPIcs.CCC.2017.9.pdf` | Scheder–Steinberger, CCC 2017, LIPIcs vol. 79, 9:1–9:15 (conference version), drops.dagstuhl.de | `43ff64c4…` |
| **H** | `hertli_1103.2165.pdf` | Hertli, "3-SAT Faster and Simpler …", arXiv:1103.2165**v2** (the version arXiv serves; 12 pp.) | `3c777557…` |
| **HKZZ** | `hkzz_fasterksat_mit.pdf` | Hansen–Kaplan–Zamir–Zwick, "Faster k-SAT Algorithms using Biased-PPSZ", STOC '19 pp. 578–589, **author copy** from people.csail.mit.edu/virgi/6.s078/papers/fasterksat.pdf | `bc5b703a…` |

Access notes, recorded honestly:

- The **journal version was obtained in full** (48 pages, not paywalled). All L1–L5/L7
  verifications below are against **SS-J (journal numbering)**, with SS-C used as
  cross-reference. No item is conference-only.
- **HKZZ has no arXiv version** that I could locate (searched 2026-08-25: dblp, TAU CRIS, ACM
  DL, general web). The STOC paper repeatedly defers to "the full version of this paper"
  (p. 588) for the computer-assisted 3-SAT analysis behind Theorem 7.8; **no public full
  version was located**. The fetched author copy is the STOC '19 camera-ready.
- Springer-PDF quirk (not JC's issue): the visible page-1 header of SS-J prints
  "https://doi.org/10.1007/s00037-024-00259-**1**", while the PDF's XMP metadata (`/doi`),
  the Springer URL, and JC's bibliography all say `10.1007/s00037-024-00259-y`. Both text
  extractors agree the printed glyph is "1"; treated as a Springer typesetting artifact.

### Conference ↔ journal numbering map (established from the two fetched PDFs)

| SS journal 2024 (SS-J) | SS CCC 2017 (SS-C) | content / difference |
|---|---|---|
| Example 1.3, P^(w) (p. 7) | "Example: P_d" (pp. 9:3–9:4) | ≤w-clause implication heuristic. Journal: "RandomDecode(F, P^(w)) is called **weak PPSZ**". Conference: "RandomDecode(F, P_d) **becomes PPSZ**". |
| Example 1.4, BWR(w) "strong PPSZ" (p. 7) | — (absent) | bounded-width resolution heuristic, journal only |
| Example 1.5, P^(∞) (pp. 7–8) | "Example: P_∞" (p. 9:4) | complete heuristic; induces Q |
| Definition 1.8 (error) (p. 9) | Definition 2 (p. 9:4) | identical content |
| Theorem 1.9 (p. 9) | Theorem 3 (p. 9:4) | P^(1) error 1−1/k |
| **Theorem 1.10** (p. 9) | **Theorem 4** (p. 9:4) | P^(w) error bound. **Naming trap: the constant is `c_k` in the journal but `s_k` in the conference version** (journal reserves s_k for the finite-component probability / "savings"). |
| Hertli's Theorem 1.12 (p. 10) | Theorem 6 (p. 9:5) | identical (conference adds Conjecture 7 that p∗ is removable) |
| Definition 1.14 (closed under restrictions) (p. 11) | Definition 8 (p. 9:6) | identical |
| Definition 1.15 (monotone) (p. 11) | Definition 9 (p. 9:6) | identical |
| Observation 1.16 (p. 12) | in-text display (p. 9:6) | Q(π,α) = (1/n!)·2^(−I(π,α)) |
| **Main Theorem 1.17** (p. 12) | **Theorem 10** (p. 9:6) | **journal adds the hypothesis "for some p ≥ p∗"**; conference states none |
| **Lifting Theorem 1.18** (p. 13) | **Theorem 11** (p. 9:6) | **journal adds "p > p∗" and the quantitative "ε′ ≥ C·ε/log(1/ε)"**; conference has only "ε′ > 0 if ε > 0" |
| Theorem 1.19 (HKZZ) (p. 13) | — | new in journal |
| Theorem 1.20 (Scheder 2021) (p. 13) | — | new in journal |
| — | Theorem 12 (Hertli ICALP'14 Unique-3-SAT) (p. 9:6) | dropped in journal |
| — | Theorem 13 (general 3-SAT, O(2^((s3−ε′)n))) (p. 9:6) | dropped in journal (replaced by 1.19/1.20) |
| Lemma 3.3 (stated p. 22, restated p. 30) | Lemma 15 (pp. 9:7, 9:11) | requires monotone + closed under restrictions |
| §3.1 proof of 1.18 (pp. 28–29) | §3 proof of Thm 11 (pp. 9:8–9:9) | both contain the **unproved** restriction assertion (see L2) |

JC cite the journal numbering (Main Theorem 1.17, Lifting Theorem 1.18, Theorem 1.10).
**All three numbers exist in the fetched journal PDF and denote exactly the statements JC
say they denote.**

---

## L1. SS Main Theorem (JC Imported theorem 4.1, first sentence + eq. (28))

**JC verbatim** (Imported theorem 4.1, §4; compiled eq. (28)):

> "Let P be a monotone proof heuristic of error at most p ≥ p∗ on a formula class closed
> under restrictions. Let Q be the distribution induced by the complete proof heuristic and
> let I be the number of variables that are liquid when processed, in the notation of
> [SchederSteinberger]. For every satisfiable formula F on n variables,
> P[RandomDecode(F, P) succeeds] ≥ 2^(−pn+(p−p∗)·E_Q[I])."
> Followed by: "Equation (28) is Main Theorem 1.17 of [6], and the corresponding
> unique-to-general statement is their Lifting Theorem 1.18."

**Source verbatim** — SS-J, **Main Theorem 1.17, p. 12 of 48**:

> "**Main Theorem 1.17.** Suppose P has error at most p against C for some
> p ≥ p∗ := (2−log(e))/2 ≈ 0.279 and set q := p − p∗ ≥ 0. If F ∈ C is satisfiable then
> RandomDecode returns a satisfying assignment with probability at least
> 2^(−pn + q·E_{(π,α)∼Q}[I(π,α)])."

Restated inside the proof of Lifting Theorem 1.18, SS-J p. 29, eq. (3.8):
"Pr[RandomDecode(F, P) successful] ≥ 2^(−pn+q·E_Q[I])".

Cross-reference — SS-C, **Theorem 10, p. 9:6** (conference wording): "Suppose P has error at
most p against C, and set q := p − p∗ for p∗ := (2−log(e))/2 ≈ 0.279. Let F ∈ C be
satisfiable. Then RandomDecode returns a satisfying assignment with probability at least
2^(−pn+q·E_{(π,α)∼Q}[I(π,α)]), where q := p − p∗." (No p ≥ p∗ hypothesis; "where q := p − p∗"
is printed twice.)

**Hypotheses and definitions the SS statement depends on** (all from SS-J):

- *Proof heuristic* (p. 5): "A proof heuristic is a deterministic procedure P which on input
  F and x outputs a value b ∈ {0, 1, ?}. Correctness means that whenever P(F, x) = b ∈ {0,1}
  then in fact F ⊨ (x = b) … incompleteness means that we allow P(F, x) to output '?' …
  when we say proof heuristic, we always mean a correct but possibly incomplete heuristic."
- *RandomDecode* (Algorithm 3, p. 7): "π := a random permutation on V; c := a random string
  in {0,1}^n; α := Decode(c, π, F, P); return α if it satisfies F, else failure." (Decode,
  Algorithm 2 p. 6: processes variables in π-order, sets α(x) := b if P(F|β, x) = b ∈ {0,1},
  else consumes the next bit of c.)
- *Error* (**Definition 1.8, p. 9**): "Let C be a class of formulas and P be a proof
  heuristic. We say that P has error at most p against C if for every F ∈ C, solution α, and
  variable x in F it holds that E_π[J_x(π,α)] ≤ p." Here E_π is **with respect to the uniform
  distribution on permutations** (fixed in Observation 1.6, p. 8), per variable, for **every**
  solution α; J_x (p. 9) is the indicator that x is frozen in the residual F|β when processed
  but P answers "?".
- *Frozen/liquid* (p. 8): see L7 for verbatim.
- *I* (pp. 8–9): I_x(π,α) = 1 iff "in Line 4 of Encode, x is liquid in F|β" (β = α restricted
  to the variables preceding x in π); I = Σ_x I_x. So I is exactly "the number of variables
  that are liquid when processed" along (π, α), as JC paraphrase.
- *Q* (p. 12 + Observation 1.16): "The procedure RandomDecode(F, P^(∞)) chooses a uniformly
  random permutation π ∈ Sym(V) and always outputs a satisfying assignment. Thus, it defines
  a distribution Q on Sym(V) × sat(F)." "Observation 1.16. Q(π,α) = (1/n!) · 2^(−I(π,α))."
- *p∗* := (2−log(e))/2 ≈ 0.279, log = log₂ (see L5 for the numeric check).

**Task checks:**
- (a) *Every satisfiable formula, not just unique?* **YES** — "If F ∈ C is satisfiable then …".
- (b) *Base 2 with E_Q[I] exactly as JC state?* **YES** — 2^(−pn+q·E_{(π,α)∼Q}[I(π,α)]) with
  q = p − p∗; JC write the identical exponent with q spelled out as (p − p∗).
- (c) *Is "formula class closed under restrictions" a hypothesis in SS's Main Theorem 1.17?*
  **NO — and neither is "monotone".** SS-J's Theorem 1.17 statement carries only "error at
  most p against C" and "p ≥ p∗". JC added both extra hypotheses. This is
  hypothesis-STRENGTHENING (JC claim strictly less than SS claim), hence safe. Moreover it is
  arguably the *correct* hypothesis set: SS's own proof of Main Theorem 1.17 (p. 28:
  "Assuming Lemma 3.3 … we can finish the proof of the Main Theorem 1.17") invokes
  **Lemma 3.3**, whose restatement (p. 30) reads: "Let C be a formula class closed under
  restrictions, P a monotone proof heuristic with error at most p against C. Then for every
  F ∈ C and every frozen variable x of F it holds that E_R[J_x] ≤ p." So the SS journal's
  Main Theorem 1.17 **statement omits two hypotheses its own proof uses**; JC's import
  restores them. JC's application (P = P^(w), C = 3-CNF, p = p_w ≥ p₀ > p∗) satisfies every
  hypothesis.

**Verdict: UNCHANGED** (inequality, quantifiers, base, and success event identical to SS-J
Main Theorem 1.17; JC add the hypotheses "monotone" and "closed under restrictions", a
safe-direction strengthening that matches what SS's proof actually requires — flagged as
deviation D1 below).

---

## L2. The restriction claim and "Lifting Theorem 1.18"

**JC verbatim** (Imported theorem 4.1, second sentence):

> "Moreover, if E_Q[I] ≤ δn, there is a restriction of at most δn variables, consistent with
> a satisfying assignment, whose residual formula is uniquely satisfiable."
> and the attribution: "…the corresponding unique-to-general statement is their Lifting
> Theorem 1.18."

**Source verbatim** — SS-J, **Lifting Theorem 1.18, p. 13 of 48** (the actual numbered
statement):

> "**Lifting Theorem 1.18.** Suppose P is a monotone proof heuristic with error rate at most
> p against class C. We assume that C is closed under restrictions and that p > p∗.
> (i) If procedure RandomDecode solves Unique-C-SAT with success probability at least
> 2^((−p+ϵ)n), then it solves C-SAT with success probability 2^((−p+ϵ′)n).
> (ii) If there is a probabilistic algorithm A for Unique-C-SAT with success probability
> 2^((−p+ϵ)n), then there is a probabilistic algorithm A′ for C-SAT with success probability
> at least 2^((−p+ϵ′)n) and running time n times that of A.
> (iii) If there is Monte Carlo algorithm B solving Unique-C-SAT running in time 2^((p−ϵ)n),
> then there exists a Monte Carlo algorithm B′ solving C-SAT in time 2^((p−ϵ′)n).
> In all three cases, ϵ′ > 0 if ϵ > 0, and in particular ϵ′ ≥ C · ϵ/log(1/ϵ) for some C
> depending on p − p∗."

The restriction claim JC quote is **not the statement of Theorem 1.18**. It appears in SS in
two places, both times **asserted without proof**:

1. Prose before 1.18, SS-J p. 12: "…or E_Q[I] < δn, in which case there is a restriction ρ
   such that F|ρ has a unique satisfying assignment and ρ sets fewer than δn variables."
2. Inside the proof of 1.18, SS-J p. 29: "In the second case, we assume that E_Q[I] ≤ δn. In
   particular, I(π,α) ≤ δn for some permutation π and satisfying assignment α. **This means
   that** there is a partial assignment ρ fixing δn variables such that F|ρ has a unique
   satisfying assignment."
   (Conference parallel, SS-C p. 9:8: "Otherwise, assume that E_Q[I] ≤ δn. In particular,
   I(π,α) ≤ δn for some permutation π and assignment α. This means that there is a partial
   assignment ρ fixing δn variables such that F|ρ has a unique satisfying assignment.")

**Deviations found (all benign, enumerated):**
- **D2 (attribution granularity):** JC package this claim inside "Imported theorem 4.1" and
  attribute the "unique-to-general statement" to Lifting Theorem 1.18; in SS it is an
  intermediate *unproved* step inside the proof of 1.18 (and pre-1.18 prose), not the numbered
  theorem. JC do not import SS's ε′-conclusion at all — they derive their own quantitative
  version (Proposition 4.2) and **prove the restriction claim themselves** (Lemma C.1, whose
  proof I checked against SS's definitions — sound; see L7). Net effect: the mathematical
  content JC use is available and correct, but the citation "this is their Lifting Theorem
  1.18" is loose.
- **D3 (trivial size bookkeeping):** SS write "fixing δn variables" (p. 29) / "fewer than δn"
  (p. 12); JC write "at most δn". JC's form is the one that actually follows (|ρ| = I(π,α) ≤
  δn); SS's two phrasings are internally inconsistent with each other. Safe.
- JC add "consistent with a satisfying assignment". SS do not say this explicitly, but it is
  implied by SS's own conclusion (a restriction with a uniquely *satisfiable* residual is
  automatically consistent with a satisfying assignment of F), and SS's ρ is constructed along
  a satisfying assignment α. Safe explicitation.

**Verdict: PARTIAL** — content verified present in SS-J (p. 12 prose + p. 29 proof step,
asserted without proof) and SS-C (p. 9:8); it is *not* the statement of Lifting Theorem 1.18.
JC supply the missing proof themselves (Lemma C.1). No mathematical discrepancy.

---

## L3. Finite-strength error p_w = p₀ + ε_w (JC eq. (3); the task brief called it "eq. (4)" — in the compiled arXiv v1 PDF it is numbered **(3)**; eq. (4) is the change-of-measure)

**JC verbatim** (§2.1):

> "Let P^(w) be the weak implication heuristic that infers x = b when some set of at most w
> residual clauses implies x = b. We write PPSZ_w for the corresponding random decoder. The
> heuristic is sound and monotone under restrictions. For fixed w, one run takes n^{O(w)}
> time and polynomial space.
> A set of at most w clauses of a 3-CNF contains at most 3w variables. Resolution
> completeness on those variables gives a derivation of width at most 3w for every
> implication certified by P^(w). Hence the standard bounded-width implementation of
> original PPSZ at width 3w forces every variable forced by P^(w) and has at least the same
> success probability.
> … Paturi et al.'s error bound, in the notation of Scheder and Steinberger, is
> p_w = p₀ + ε_w, ε_w ≥ 0, ε_w → 0 (w → ∞)."   [compiled eq. (3)]
> Appendix A provenance row: "finite-strength error p_w — Paturi et al.; Scheder–Steinberger
> Theorem 1.10 — Equation (3)".

**Source verbatim** — SS-J, **Theorem 1.10, p. 9 of 48**, with the constant defined just
before it:

> "Paturi et al. (2005) prove the following bound on the error of P^(w) (although they do not
> use this exact wording). Consider the infinite (k−1)-ary rooted tree. For each vertex v in
> this tree, choose π_v ∈ [0,1] uniformly at random. Delete each vertex v with π_v < π_root.
> Let s_k be probability that the root is contained in a finite connected component, and c_k
> the probability that said component is infinite. It is easy to see that c₂ = 0, and a
> simple calculation shows that c₃ = 2 ln(2) − 1 ≈ 0.3863.
> **Theorem 1.10 (Paturi et al. 2005).** P^(w) has error c_k + ϵ_{w,k} against k-CNF
> formulas, where ϵ_{w,k} → 0 as w → ∞."

And the heuristic itself, SS-J **Example 1.3, p. 7**:

> "P^(w), a heuristic that generalizes P^(1). It answers P^(w)(F, x) = b if F is a CNF
> formula and it contains a subset G of at most w clauses for which G ⊨ (x = b). … 
> RandomDecode(F, P^(w)) is called weak PPSZ."

Cross-reference — SS-C Theorem 4, p. 9:4: "P_d has error s_k + ε_{d,k} against k-CNF
formulas, where ε_{d,k} → 0 as d → ∞" (conference calls the constant s_k; s₃ = 2 ln(2) − 1,
p. 9:4), and "Example: P_d … It answers P_d(F,x) = b if F is a CNF formula and it contains a
subset G of at most d clauses for which G ⊨ (x = b). With this heuristic,
RandomDecode(F, P_d) becomes PPSZ, although Paturi, Pudlák, Saks, and Zane [7] state it
slightly differently." (pp. 9:3–9:4).

**Checks:**
- *Exact heuristic in SS Theorem 1.10:* it is **P^(w) itself — "some set of at most w clauses
  implies x = b"** — i.e., *literally the same heuristic JC define*. Not width-w resolution
  (that is SS's separate Example 1.4, BWR(w), "strong PPSZ", about which Theorem 1.10 says
  nothing), and identical in content to Hertli's "s-implication" (Hertli p. 4: the PPSZ bound
  "holds if we use s-implication instead of a preprocessing step of s-bounded resolution";
  corroborated by HKZZ p. 578-579: "Hertli [3] noticed that the current analysis of PPSZ also
  works when the bounded resolution is replaced by weaker bounded implication, i.e., an
  implication by a small subset of the clauses").
- *For 3-CNF:* error ≤ c₃ + ϵ_{w,3} = (2 ln 2 − 1) + ϵ_{w,3} with ϵ_{w,3} → 0. JC's
  p_w = p₀ + ε_w with p₀ = 2 ln 2 − 1: **exact match** (c₃ = p₀ verified: SS p. 9; JC §1).
- *ε_w ≥ 0:* SS do not assert nonnegativity. **D4 (trivial):** JC's "ε_w ≥ 0" is a harmless
  normalization — "error at most p" is upward-closed, so ε_w := max(ϵ_{w,3}, 0) preserves
  Theorem 1.10's conclusion and JC's two properties. No effect on any downstream inequality
  (JC only ever use p_w as an upper bound and p_w ≥ p₀ ≥ p∗).
- *Attribution:* JC say "Paturi et al.; Scheder–Steinberger Theorem 1.10" — matches SS's own
  attribution ("Theorem 1.10 (Paturi et al. 2005)"). Correct.
- *JC's bridging argument (§2.1), audited step by step:*
  1. |G| ≤ w clauses of a 3-CNF ⇒ |vars(G)| ≤ 3w. ✔ (≤3 variables per clause.)
  2. If P^(w) certifies x = b from satisfiable F, then G ⊨ (x = b) with G ⊆ F satisfiable,
     which forces x ∈ vars(G) (else a satisfying assignment of G could be extended with
     x = ¬b). ✔
  3. G ⊨ (x = b) ⟺ G ∪ {(x ≠ b)} unsatisfiable ⟹ (resolution refutation completeness) a
     refutation exists all of whose clauses mention only vars(G), hence width ≤ 3w; the
     standard weakening transformation (re-adding the literal x = b) converts it into a
     resolution derivation of the unit clause (x = b) from G alone, still over vars(G), so
     width ≤ 3w. Since G ⊆ F, BWR(3w)(F, x) = b in SS's Example 1.4 sense. ✔
  4. Therefore BWR(3w) forces a superset of the variables P^(w) forces at every step;
     pointwise (per permutation and per satisfying assignment) the encoding length C can only
     drop, so by Observation 1.6 each per-α return probability — and hence the total success
     probability, a sum over disjoint per-α return events — can only rise. ✔
  **Assessment: SOUND.** Note, however, that the bridge is *not needed for the lifting layer
  at all*: SS's Theorem 1.10 is stated directly for P^(w), and JC's Theorem 4.1/Proposition
  4.2/Appendix C work directly with PPSZ_w = RandomDecode(F, P^(w)). The bridge only serves
  to identify PPSZ_w with "the standard bounded-width implementation of original PPSZ"
  (relevant to the Scheder-analysis layer, outside this audit's scope).

**Verdict: UNCHANGED** (SS import exact; heuristic identical; constant identical; the ε_w ≥ 0
normalization is D4, cosmetic; JC's bridging paragraph is their own and is sound).

---

## L4. Monotone proof heuristic

**JC verbatim** (§2.1): "The heuristic is sound and monotone under restrictions."
(and Imported theorem 4.1's hypothesis "monotone proof heuristic"; Appendix C: "monotonicity
permits a coupling in which PPSZ_{w′} makes no more guesses than PPSZ_{w_G} along any fixed
satisfying assignment").

**Source verbatim** — SS-J, **Definition 1.15, p. 11**, and the following remark, p. 12:

> "**Definition 1.15.** We say that a proof heuristic P is monotone if P(F, x) ∈ {0, 1}
> implies P(F|_{y=b}, x) ∈ {0, 1} for every F, y ≠ x, and b ∈ {0, 1}."
> "In other words, if P can deduce the value of x, then it can also do so after we add the
> additional information that y = b. Note that P^(0), P^(1), P^(w), P^(∞) defined above are
> all monotone."

(Conference parallel: Definition 9 + "Note that P₀, P₁, P_d, P_∞ define above are all
monotone", p. 9:6.)

**Checks:** SS's monotonicity is under *single-variable restrictions with arbitrary values*
(y ≠ x, any b), which subsumes JC's "monotone under restrictions" usage (JC only ever restrict
along satisfying assignments). "Sound" = SS's "correct" (built into "proof heuristic",
SS-J p. 5). **P^(w) is explicitly listed by SS as monotone** (p. 12) — so JC's claim is a
direct citation, and it is also independently trivially provable (a subset of ≤ w clauses
restricts to a subset of ≤ w clauses whose satisfying assignments are the restricted ones, so
implication survives restriction). JC's w-monotonicity claim in Appendix C (P^(w′) forces a
superset of P^(w) for w′ ≥ w) is immediate from the definition (a set of ≤ w clauses is a set
of ≤ w′ clauses) — consistent with SS's framework though not stated by SS.

**Verdict: UNCHANGED.**

---

## L5. p∗ and the complete proof heuristic

**JC verbatim** (§4, eq. (27)): "p∗ = (2 − log₂ e)/2 = 1 − 1/(2 ln 2), q₀ = p₀ − p∗ =
0.107641881564372…" and (Imported theorem 4.1) "Let Q be the distribution induced by the
complete proof heuristic…", "error at most p ≥ p∗".

**Source verbatim** — SS-J:

- **Example 1.5, pp. 7–8:** "P^(∞). This heuristic employs the whole power of propositional
  logic. It answers P^(∞)(F, x) = b ∈ {0,1} if F implies (x = b). Obviously, determining this
  is itself NP-hard, so this is not an efficient heuristic. … Note that if F is satisfiable,
  then RandomDecode(F, P^(∞)) always outputs a satisfying assignment. Thus, it defines a
  distribution Q on pairs (π, α)…"
- **p. 9:** "Also, J(π,α) = 0 for P^(∞), **since this heuristic is complete**." — SS's own
  word "complete" for P^(∞); JC's phrase "the complete proof heuristic" is SS's terminology.
- **p. 12 (before Obs 1.16):** "The procedure RandomDecode(F, P^(∞)) chooses a uniformly
  random permutation π ∈ Sym(V) and always outputs a satisfying assignment. Thus, it defines
  a distribution Q on Sym(V) × sat(F)." + Observation 1.16: Q(π,α) = (1/n!)·2^(−I(π,α)).
- **p∗ in Main Theorem 1.17 (p. 12):** "p∗ := (2−log(e))/2 ≈ 0.279" (log = log₂; the ≈0.279
  is only consistent with base 2). Also in Hertli's Theorem 1.12 (p. 10) and restated in the
  proof of 1.18 (p. 29: "p > p∗ := (2−log(e))/2").

**Numeric check** (float, 15+ digits): (2 − log₂e)/2 = 1 − 1/(2 ln 2) =
**0.278652479555518…** ✔ (task's reference value 0.2786524… confirmed; JC's two closed forms
are algebraically identical since log₂e = 1/ln 2). q₀ = p₀ − p∗ = (2 ln 2 − 1) −
(1 − 1/(2 ln 2)) = **0.107641881564372266** ✔ = JC's printed 0.107641881564372… .

**Role clarification (as the task asked):** p∗ is a *k-independent proof-artifact threshold*,
NOT the error of the complete heuristic (the complete heuristic has error 0, since J ≡ 0 for
P^(∞)). SS p. 10: "Note the mysterious p∗ in the theorem. We suspect that it is an artifact
of the proof." (SS-C even conjectures it removable, Conjecture 7.) The theorem's requirement
is that the *error bound* p of the heuristic in use satisfies p ≥ p∗; for k = 3 this holds
because c₃ = 2 ln 2 − 1 ≈ 0.3863 ≥ p∗ (SS p. 10: "since c_k ≥ p∗ for all k ≥ 3, Hertli's
theorem works for the current version of PPSZ"). JC's application uses p = p_w = p₀ + ε_w ≥
p₀ = c₃ > p∗ — hypothesis satisfied with slack ≈ 0.1076. JC never misstate p∗'s role.

**Verdict: UNCHANGED.**

---

## L6. Baseline numbers (critical for the frontier claim)

### (a) Hertli, arXiv:1103.2165v2

- **Abstract (p. 1):** "For k ≥ 5 the same bounds hold for general k-SAT. We show that this
  is also the case for k = 3, 4, **using a slightly modified PPSZ algorithm**. … This
  improves our previous best bounds with Moser and Scheder [2] for 3-SAT to **O(1.308^n)**
  [sic — the extracted glyphs render the display bounds; the theorems give the digits] and
  for 4-SAT to O(1.469^n)."
- **Theorem 1 (p. 2):** "There exists a randomized algorithm for **3-SAT** with one-sided
  error that runs in time **O(1.30704^n)**." (General 3-SAT, randomized.)
- Underlying exponent: **Theorem 15 (p. 8):** "p_success(F, s) ≥ 2^(−c(F))" with
  c(F) ≤ n(F)·S, S = S_k + ε_k(s); **p. 5:** "For k = 3, we can show that S₃ = 2 ln 2 − 1",
  table "2^{S_k} (rounded up): 3 → 0.3862944, 1.307032"; **p. 8:** "we choose s such that
  ε_k(s) becomes small enough and 2^S < 1.30704 for 3-SAT". So the underlying general-3-SAT
  base is 2^(2 ln 2 − 1) = **1.3070319077…** (+ arbitrarily small ε), stated as the decimal
  1.30704.
- **Algorithm caveat (p. 5 & §4 p. 11):** "because we immediately fix implied variables, the
  algorithm is slightly different"; "We have adapted PPSZ slightly by immediately using
  s-implied literals." — Hertli's general bound is for a **modified** PPSZ, not original
  PPSZ.
- **Deterministic (§4, pp. 10–11):** for general 3-SAT only derandomized-Schöning-line bounds
  (O(1.3303^n) Makino–Tamaki–Yamamoto); Unique 3-SAT deterministic O(1.30704^n) via Rolf.
- **Does Hertli give general 3-SAT ≤ 1.307031578?** **NO.** His exact-decimal claim is
  1.30704 and his underlying limiting base is 1.3070319077… > 1.307031578.

### (b) HKZZ, STOC 2019 (author copy)

- **Abstract (p. 578):** "We introduce a biased version of the PPSZ algorithm … For k = 3 we
  also improve on Herli's [sic] result and get a much more noticeable improvement over PPSZ,
  though still relatively small. In particular, **for Unique 3-SAT, we improve the current
  bound from 1.308^n to 1.307^n**."
- **Footnote 1 (p. 578):** "With a slight 'tongue in cheek'. The base of the exponent of PPSZ
  is 1.30703…. Our current base is 1.30699…."
- **§1.2 (p. 579):** "The improvement we obtain is **for Unique k-SAT. By [15], this implies
  some improvement also for k-SAT**." ([15] = Scheder–Steinberger CCC 2017 — verified in
  their reference list, p. 589.)
- **Theorem 7.1 (p. 586):** "For every k ≥ 3 there exists δ_k > 0 such that biased-PPSZ
  solves **Unique k-SAT** instances in time 2^((S_k − δ_k)n)."
- **Theorem 7.8 (p. 588):** "**Unique 3-SAT** can be solved in time O(1.307^n)." — proved via
  "a rigorous computer assisted search … **In the full version of this paper**" (p. 588); no
  public full version located.
- **§8 (p. 588):** "The numerical bound we currently have **for Unique 3-SAT is
  1.306995^n**." And: "**We hope** that the improved bounds we obtained for Unique 3-SAT also
  apply directly to 3-SAT, using essentially the arguments of Hertli [3], **avoiding the
  'reduction' of Scheder and Steinberger [15] and the associated loss that comes with it**."
- **Erratum:** none found (web search 2026-08-25; ACM DL page shows no correction notice; no
  arXiv version exists to carry a revision). Recorded as *no erratum located*, not as proof
  none exists.
- **Does HKZZ claim general 3-SAT at 1.306995 (or ≤ 1.307031578)?** **NO.** Every concrete
  number (1.307, 1.306995) is explicitly Unique-3-SAT; the general-3-SAT consequence is an
  unquantified "some improvement" through SS's lifting, and the direct transfer is labelled a
  hope, not a claim. (Independent corroboration: Scheder, ECCC TR21-069 rev. 1 §1.2, frames
  HKZZ's 1.306995 in the Unique-SAT discussion; and SS-J's own Theorem 1.19 (p. 13) states
  HKZZ's general consequence as "success probability at least 2^((−c_k+ϵ_k)n) on k-SAT, where
  ϵ_k > 0 for all k ≥ 3" — with unquantified ϵ_k.)

### (c) SS journal 2024 ("…and 3-SAT Faster")

- **Abstract (p. 1):** "…we show a 'lifting result': if you improve PPSZ for k-CNF formulas
  with a unique satisfying assignment, you will immediately get a (weaker) improvement for
  general k-CNF formulas. In combination this with results by Hansen et al. (…2019) and
  Scheder (…2021), who all prove improved time bounds for Unique-k-SAT, this gives improved
  bounds for general k-SAT." — **no number**.
- **Theorem 1.19 (p. 13, quoting HKZZ):** "The probabilistic algorithm Biased PPSZ, which has
  subexponential running time, has success probability at least 2^((−c_k+ϵ_k)n) on k-SAT,
  where ϵ_k > 0 for all k ≥ 3." — general, **unquantified ϵ**.
- **Theorem 1.20 (p. 13, quoting Scheder 2021):** "The success probability of PPSZ on k-CNF
  formulas is at least 2^((−c_k+ϵ_k)n) for some ϵ_k > 0." — general, **unquantified ϵ**.
- Grep of the full 48-page text finds **no decimal of the form 1.30x anywhere**; the only
  3-SAT constant is c₃ = 2 ln(2) − 1 ≈ 0.3863 (p. 9). The quantitative content of the lifting
  is only "ϵ′ ≥ C·ϵ/log(1/ϵ) for some C depending on p − p∗" (Theorem 1.18, p. 13), with C
  never instantiated.
- **Conference version cross-check (SS-C):** Theorem 12 (p. 9:6, Hertli ICALP'14):
  "There exists a Monte-Carlo algorithm solving **Unique-3-SAT** in time O(2^((s₃−ε)n)) for
  some ε > 0"; **Theorem 13 (p. 9:6):** "There is a Monte-Carlo algorithm solving **3-SAT**
  in time O(2^((s₃−ε′)n)) for some ε′ > 0." Intro (p. 9:2): "PPSZ [7] in time
  O(2^((2 ln(2)−1)n)) ≈ O(1.308^n). The improvements by Hertli [2] and this paper are quite
  small (think of in the ballpark of tenth digit after the dot)…". — **no explicit general
  base either.**

### (context, already-frozen source) Scheder, "PPSZ is better than you think", ECCC TR21-069 rev. 1

- Abstract (p. 1): "For **Unique-3-SAT** we bound its running time by **O(1.306973^n)**…"
- Theorem 5 (§1.3): "For every k ≥ 3 there is ε_k > 0 such that the success probability of
  PPSZ on satisfiable k-CNF formulas is at least 2^(−n(1−s_k−ε_k))." — general,
  **unquantified**. Theorem 6: unique-3-SAT ≥ 1.306973^(−n).
- On HKZZ (§1.2): "for 3-SAT, it improves the success probability from 1.3070319^(−n) from
  Theorem 3 to 1.306995^(−n)" — in the Unique-SAT-case discussion.

### Baseline table

| paper (version fetched) | Unique-3-SAT claim | general-3-SAT claim | key quote | page |
|---|---|---|---|---|
| Hertli arXiv:1103.2165v2 | = PPSZ bound O(1.30704^n) (his point: general matches unique); det. Unique O(1.30704^n) via Rolf | **O(1.30704^n)** randomized one-sided error, **modified** PPSZ; underlying base 2^(2ln2−1) = 1.3070319077… | "There exists a randomized algorithm for 3-SAT with one-sided error that runs in time O(1.30704^n)." | Thm 1, p. 2; S₃ table p. 5; "2^S < 1.30704" p. 8 |
| HKZZ STOC'19 (author copy; no arXiv) | **O(1.307^n)** (Thm 7.8); numerically **1.306995^n** (§8); rests partly on unlocated "full version" | **no number** — "By [15], this implies some improvement also for k-SAT"; direct transfer only "hoped" | quotes above | pp. 578, 579, 586, 588 |
| SS journal 2024 | none stated | **no number** — 2^((−c₃+ϵ₃)n), ϵ₃ > 0 unquantified (Thms 1.19, 1.20) | quotes above | pp. 1, 13 |
| SS CCC 2017 | Thm 12 (Hertli'14): O(2^((s₃−ε)n)), ε>0 unquantified | Thm 13: **O(2^((s₃−ε′)n)), ε′>0 unquantified** | quotes above | p. 9:6 |
| Scheder ECCC TR21-069 rev1 (context) | **O(1.306973^n)** | **no number** — 2^(−n(1−s₃−ε₃)), ε₃>0 unquantified (Thm 5) | quotes above | p. 1, §1.3 |
| **JC (paper under audit)** | 1.306969598 | **1.307031578** | — | — |

### Frontier assessment

Reference values (float-verified, ≥15 digits): 2^(p₀) = **1.307031907702599** (the PPSZ /
Hertli-general limiting base); 2^(p₀ − 1/15218) = 1.306972376565153 (= JC's quoted Scheder
unique base, digit-exact); JC's lifted values 2^(p₀ − 3.465837065e−7) = 1.307031593709762 and
2^(p₀ − 3.640269421e−7) = 1.307031577906797 (both digit-exact vs. JC's table); HKZZ's unique
bonus p₀ − log₂(1.306995) ≈ 0.0000407 < 1/15218 ≈ 0.0000657 (so even its never-published
lift would be weaker than lifted-Scheder).

**No fetched source claims any explicit general-3-SAT base at or below 1.307031578.** The
only explicit general-3-SAT decimal in the entire corpus is Hertli's 1.30704 (underlying
1.3070319077…), which is strictly above both JC's 1.307031578 and JC's stated previous-best
1.307031594. All other sources claim only "PPSZ-base minus an unquantified ε" for general
3-SAT. **JC's frontier claim is consistent with all fetched primary sources.**

**Framing caveat (not a mismatch):** the "previous best" 1.307031594 that JC beat is *itself
JC's own instantiation* of the SS lifting applied to Scheder's published unique bonus 1/15218
— no source prints that number. JC state this honestly ("Applying the same lifting
calculation to the old and new unique-case bonuses gives the following limiting values"), but
any downstream claim "previous best published general bound = 1.307031594" should be
attributed to JC's computation, not to Scheder/SS. The best *previously printed* general
3-SAT decimal is Hertli's 1.30704.

Adjacent-literature note (outside the task's source list, checked because it could threaten
the frontier claim): Qin–Watanabe, "An Improvement of the Biased-PPSZ Algorithm for the 3SAT
Problem", IEICE Trans. Inf. & Syst. E105-D(3), 2022 — abstract confirms it improves HKZZ "for
**Unique 3SAT**" by numerical analysis; no general-3-SAT claim. Does not affect the frontier
claim.

**Verdict: UNCHANGED / frontier claim SUPPORTED** (with the framing caveat above).

---

## L7. Well-posedness of JC's own Lemmas C.1 and C.2 against SS's definitions

**SS definitions the lemmas rely on** (verbatim, SS-J):

- **Frozen/liquid (p. 8):** "We write F ⊨ T as a shorthand of 'F implies T', i.e., every
  satisfying assignment of F satisfies T. If F ⊨ (x = 0) or F ⊨ (x = 1) we say that x is
  frozen in F. Equivalently, all satisfying assignments of F agree on x. Otherwise, we say
  that x is liquid."
  ⟹ For satisfiable F: **x is liquid ⟺ both values of x extend to satisfying assignments**
  of F. (Hertli's Definition 5, p. 4, "non-frozen", is the same notion.)
- **I_x (pp. 8–9):** "Note that C_x(π,α) can be 1 for two reasons. First, it could be that in
  Line 4 of Encode, x is liquid in F|β and thus every correct proof heuristic P must answer
  P(F|β, x) = ?. In this case we set I_x(π,α) = 1. Second, it could be that x is frozen in
  F|β and P(F|β,x) answers '?' only due to its incompleteness. In this case we set
  J_x(π,α) = 1. Thus, C_x(π,α) = I_x(π,α) + J_x(π,α)." (β = α restricted to the variables
  processed before x under π.)
- **Guessed ⟺ liquid under the complete heuristic:** Observation 1.16's proof (p. 12): "Now
  observe that P^(∞) is complete, thus J(π,α) = 0 and C(π,α) = I(π,α)." Since C_x = 1 exactly
  when Encode/Decode consumes a bit for x ("guessed"), under P^(∞) **a variable is guessed iff
  it is liquid at the moment it is processed**. ✔ (This is what JC's phrase "the number of
  variables that are liquid when processed" and Lemma C.1's set L presuppose.)
- **Q's support:** Q(π,α) = (1/n!)·2^(−I(π,α)) > 0 on all of Sym(V) × sat(F), so
  E_Q[I] ≤ δn ⟹ ∃(π,α) with I(π,α) ≤ δn ("I(π,α) ≤ δn for some permutation π and satisfying
  assignment α", SS-J p. 29). JC's "some pair (π,α) in the support of Q" (App. C) matches.

**JC Lemma C.1 verbatim** (Appendix C): "Suppose I(π,α) ≤ r for a permutation π and a
satisfying assignment α of F. Let L be the set of variables that are liquid at the moment
they are processed along (π, α), and let ρ = α|_L. Then |L| = I(π,α) ≤ r and F|ρ has the
unique satisfying assignment α|_{V∖L}."

*Check against SS's definitions:* L = {x : I_x(π,α) = 1}, so |L| = I(π,α) by SS's I = Σ_x I_x
— definitionally exact. Proof logic (first π-position where a hypothetical second satisfying
assignment β ⊇ ρ deviates from α: the residual formulas coincide there, both values of that
variable extend to satisfying assignments, hence the variable is liquid-when-processed, hence
in L, contradicting β ⊇ ρ = α|_L) uses exactly SS's liquid notion for the *satisfiable*
residual F|β — valid. Existence side (α|_{V∖L} satisfies F|ρ) is immediate. **Sound; supplies
the proof SS omitted for their p. 29 assertion, in sharpened form ("at most", "consistent
with a satisfying assignment").**

**JC Lemma C.2 verbatim** (statement): "Let F be a satisfiable CNF formula on variable set V,
let α ∈ sat(F), and let R ⊆ V have size r. Assume that F|_{α|_R} has the unique satisfying
assignment α|_{V∖R}. Then, for every finite implication strength w,
P[PPSZ_w(F) = α] ≥ (n choose r)^(−1) · 2^(−r) · P[PPSZ_w(F|_{α|_R}) = α|_{V∖R}]."

*Check:* C.2 is self-contained (it does not use liquid/Q/I); its ingredients — uniform random
permutation, soundness of P^(w) (SS's "correctness": any value inferred along an α-consistent
prefix must equal α's value), independent unbiased guess bits, and the exchangeability facts
Pr[first-r-set = R] = (n choose r)^(−1) and uniform suffix order given the prefix — all match
SS's RandomDecode (Algorithm 3) / JC's PPSZ_w conventions. The independence claim ("every
forcing decision in the prefix is determined before the suffix order is consulted") is
correct because P^(w) reads only the residual formula. The padding step ("extend its domain
to an arbitrary r-set by assigning additional variables according to the unique satisfying
assignment of F|ρ. The further restricted formula remains uniquely satisfiable") is sound.
No conflict with any SS definition. (SS's own p. 29 sketch of the same step — "with
probability (n choose ≤δn)^(−1)·2^(−δn) the first δn steps produce exactly ρ, and the
remaining (1−δ)n steps are like running RandomDecode(F|ρ, P)" — is the assertion JC's C.2
proves; SS give it one sentence.)

Also re-verified for JC's Appendix C: the large-I branch algebra −p_w·n + q_w·δn =
−p₀n + (q₀δ − ε_w(1−δ))n is an identity ✔, and the unique-residual branch exponent equals
u_γ(δ_n)·n with JC's u_γ(δ) = γ(1−δ) − (1−p₀)δ − h₂(δ) ✔ (this is a *tighter* form than SS's
own weakened display (3.10), which drops a (1−δ) factor — JC prove their version themselves,
so no import issue).

**Verdict: CONSISTENT / definitions imported UNCHANGED** (Lemmas C.1–C.2 are JC's own; both
are well-posed and sound relative to SS's liquid/Q/I/RandomDecode definitions as fetched).

---

## Summary of verdicts

| item | subject | verdict |
|---|---|---|
| L1 | SS Main Theorem 1.17 vs JC Imported theorem 4.1, sentence 1 | **UNCHANGED** (JC add hypotheses — safe direction; see D1) |
| L2 | restriction claim / "Lifting Theorem 1.18" | **PARTIAL** (content in SS's p. 12 prose + p. 29 proof step, asserted without proof; not the numbered statement of 1.18; JC prove it themselves — D2, D3) |
| L3 | finite-strength error, SS Theorem 1.10, P^(w), bridging argument | **UNCHANGED** (import exact; ε_w ≥ 0 normalization D4 harmless; bridging sound) |
| L4 | monotone definition and P^(w) monotonicity | **UNCHANGED** |
| L5 | p∗, complete heuristic, Q | **UNCHANGED** (p∗ = 0.278652479555518…; all closed forms agree) |
| L6 | baseline running-time bounds | **UNCHANGED / frontier claim SUPPORTED** (no source claims general 3-SAT ≤ 1.307031578; framing caveat recorded) |
| L7 | JC Lemmas C.1/C.2 vs SS definitions | **CONSISTENT** (definitions UNCHANGED; JC's own proofs sound) |

## Enumerated deviations (all flagged, none mathematical errors)

- **D1 (L1, quantifier/hypothesis set):** JC's Imported theorem 4.1 adds "monotone" and
  "formula class closed under restrictions" to SS Main Theorem 1.17, which states neither.
  Safe direction (JC assume more, conclude the same); notably SS's *own proof* of 1.17 uses
  both (via Lemma 3.3, p. 30), so SS's statement under-declares its hypotheses and JC's
  version is the honest hypothesis set. JC's p ≥ p∗ matches the journal statement (the
  conference Theorem 10 lacks it).
- **D2 (L2, attribution granularity):** the "Moreover…" sentence of Imported theorem 4.1 is
  not the statement of Lifting Theorem 1.18; in SS it is an unproved in-proof assertion. JC
  reprove it (Lemma C.1). Mathematically clean, citation loose.
- **D3 (L2, trivial):** SS "fixing δn variables"/"fewer than δn" vs JC "at most δn" — JC's
  is the correct derivable form.
- **D4 (L3, trivial):** "ε_w ≥ 0" is JC's normalization, not asserted by SS Theorem 1.10;
  harmless because error bounds are upward-closed.
- **D5 (bookkeeping, task-prompt level):** the finite-strength equation p_w = p₀ + ε_w is
  eq. **(3)** in the compiled arXiv v1 PDF (the audit brief referred to it as "eq. (4)";
  eq. (4) is the change-of-measure inequality).
- **D6 (source quirk, not JC):** SS-J's visible page-1 DOI prints "…00259-1" vs. metadata/
  citation "…00259-y"; and SS's conference/journal versions swap the meaning of s_k
  (conference s_k = journal c_k) — JC consistently use the journal's c₃ = p₀ convention.
- **D7 (context caveat, not JC):** HKZZ's Unique-3-SAT numbers (Thm 7.8, 1.306995) lean on a
  "full version" that appears never to have been published; no erratum found either. Affects
  the strength of HKZZ's own claims, not JC's imports (JC never rely on HKZZ).

## Overall verdict on the lifting-import layer

**CLEAN** — no mathematical mismatch found between JC's LIFTING-layer imports and the fetched
primary sources: every imported inequality, constant (p₀ = c₃ = 2 ln 2 − 1,
p∗ = 0.278652479555518…, q₀ = 0.107641881564372…), quantifier, success event, base-2
exponent, heuristic definition (P^(w)), and structural notion (liquid, Q, I, monotone,
closed-under-restrictions, error) matches SS-J's journal statements verbatim or with
safe-direction strengthening only. The seven deviations above (D1–D7) are attribution-
granularity, normalization, or source-side quirks — every one enumerated, none affects
soundness or the numerics. The baseline check confirms **no fetched source claims a general
3-SAT randomized base at or below 1.307031578**, so JC's frontier claim stands relative to
Hertli, HKZZ, and both SS versions, with the recorded caveat that the previous-best figure
1.307031594 is JC's own instantiation of the SS lifting rather than a number printed in any
source.

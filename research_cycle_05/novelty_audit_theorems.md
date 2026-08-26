# Cycle 5 novelty audit: switch-structure and dense-circle theorems

**Date:** 2026-08-21; final cross-model amendment 2026-08-26.
**Scope:** priority/novelty ONLY, per Phase 8 of `INITIAL_RESEARCH_MISSION.md`.
No correctness assessment of N1–N5 is made or implied.  The SEG addendum
quotes the final proof-audit status solely to distinguish proof provenance
from novelty.  Targets N1–N5 as tasked.
Builds on (does not redo) `research_cycle_05/common_interval_literature.md`
("the Cycle-5 survey") and the Cycle-4 `literature_novelty_audit.md`.

**Final-amendment note.**  The independent Sol cross-model validation
expanded the terminology and equivalent-object search beyond the original
balanced-chain vocabulary.  It located material primary prior art in arc
permutations, regular set systems, greedoids/antimatroids, and literal unions
of relabelled set systems.  The N1, N4, N5, and SEG classifications below are
the corrected canonical classifications; inconsistent conclusions from the
2026-08-21 pass are superseded.

**Verdict scale:** KNOWN > LIKELY KNOWN > UNCLEAR > POTENTIALLY NOVEL >
NOVELTY STRONGLY SUPPORTED.  Verdicts are about located public prior art,
never about mathematical truth, and are deliberately not upgraded beyond
what the searches performed here support.  No Cycle-5 item receives the
final category after the cross-model amendment.

**Method note.**  The original pass used web search plus direct reads of the
two 2026 sources using the exact `balanced-chain` terminology (both PDFs
downloaded and read page-by-page that session):

- **[FLSY26]** T. Borém Fabris, N. Limaye, S. Srinivasan, A. Yehudayoff,
  *Multilinear Algebraic Branching Programs and the Min-Partition Rank
  Method*, [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/)
  (posted 2026-01-01), also CCC 2026, LIPIcs 383, Article 22,
  [DOI 10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22).
  Read this session: title/abstract, contents, §1 (Definition 1.2,
  Theorem 1.3, Definition 1.4, Lemma 1.5, Theorems 1.6–1.7,
  Corollary 1.8), §5.5 (interval-mABPs, Theorem 5.14), §5.6, §6
  (Further questions), references.
- **[Kush26]** D. Kush, *An Unconditional Barrier for Proving Multilinear
  Algebraic Branching Program Lower Bounds*, ECCC TR26-043 (posted
  2026-04-01) = arXiv:2604.00746.  Read this session: abstract, contents,
  §§1–4 (two-block steering, steered path, block deviation, forced
  probability), §8.3/§9 (failure probability, comparison with FLSY,
  open questions), Appendix A, references.
  **Status re-verified today:** ECCC revision #1 (2026-05-11) and arXiv v2
  (2026-05-11, marked *withdrawn*) both record an anonymous-referee gap in
  Lemma 4.1 ("the bound on the forced probability holds unconditionally
  but not conditionally on the filtration F_t"); "all the results in the
  paper crucially rely on the correctness of this lemma."  No public
  repair, erratum-fix, or successor paper was located through 2026-08-21
  (ECCC year-2026 listing scanned; arXiv/scholar sweeps below).  This
  matches the standing O01 note in `literature/novelty_log.md`.

A full scan of the ECCC 2026 listing for reports touching multilinear
ABPs / balanced chains / interval set systems returned: TR26-001,
TR26-043, and three unrelated multilinear reports (TR26-002 IPS
separations; TR26-035 read-once determinants; TR26-090 multilinear
formula lower bounds for sparse determinants).  This establishes only that
the exact `balanced-chain` phrase had a two-paper public footprint in that
catalogue.  It is not an enumeration of the broader feasible-word, regular-
set-system, greedoid/antimatroid, learning-space, common-interval, or
permutation literature.

---

## N1. Lemma A.1 (difference-`a` APs of size `2..q-2` are never cyclic intervals, `a ≠ ±1`)

**Searches run** (beyond the survey's §5.4, which already reported
NOT FOUND for the general "common intervals of multiplication
permutations" question):

1. `"arithmetic progression" "cyclic interval" modulo q never an interval multiplication`
2. `three-distance theorem corollary arithmetic progression consecutive residues interval Z_q`
3. `multiplication map x -> ax mod q maps interval to interval only a = ±1`
4. `Cilleruelo Garaev dilation of intervals modulo p concentration points`
5. `mathoverflow when is arithmetic progression mod p a set of consecutive residues interval`
6. `permutation of Z_n mapping every cyclic interval to cyclic interval rotations reflections dihedral folklore`
7. `"Bohr set" "interval" Z_p "arithmetic progression" structure rank one contained in interval`
8. `Cooper quasirandom permutations multiplication mod n discrepancy intervals`
9. `"simple permutation" no nontrivial blocks "multiplication" modular example "ax mod n"`
10. `three-gap theorem when is {a, 2a, ..., ka mod n} a set of consecutive integers block`
11. `"dilate"/"dilation" of an interval mod p "is not an interval" additive combinatorics`
12. `multiples mod n form consecutive residues problem prove only a=1 or a=n-1` (competition/folklore angle)

Plus a direct page-by-page read of the closest-community paper,
J. N. Cooper, *Quasirandom Arithmetic Permutations* (arXiv:math/0310384;
J. Number Theory 2005), §§1–3.1.

**Closest prior art and why it does not subsume:**

- *Three-distance / three-gap theorem* (Sós, Surányi, Świerczkowski 1958;
  van Ravenstein, J. Austral. Math. Soc. 1988; Alessandri–Berthé,
  Enseign. Math. 1998; Berthé–Reutenauer, Math. Intelligencer).  The gap
  multiset of `{c, c+a, …, c+(s-1)a}` mod `q` is classical, and Lemma A.1
  is a short corollary of exactly this kind of gap/adjacency counting
  (the lemma's own proof counts adjacencies as
  `max(0, s-h) + max(0, s-(q-h))`, `h = a^{-1}`).  No source was found
  that states the corollary (an AP with difference `a ∉ {±1}` and size
  `2..q-2` is never a cyclic interval / dilates of nontrivial intervals
  are never intervals).  The machinery subsumes the *proof method*, not
  the *statement*.
- *J. N. Cooper, Quasirandom Arithmetic Permutations* (math/0310384) and
  *Quasirandom Permutations* (math/0211001; JCTA 2004).  The only located
  community that studies `ψ_a : x ↦ ax mod n` against interval structure.
  Results are quantitative interval-discrepancy bounds, in expectation
  over `a` (`E[D(ψ_k)] = O(log² n log log n)`) plus an interval-overlap
  proposition (`σ(I) ∩ J ≠ ∅` for `|I|,|J| > √(nD)`).  Statistical, for
  typical `a`; contains no exact interval-image dichotomy and nothing for
  every fixed `a ≠ ±1`.
- *Rank-1 Bohr sets are 2-dimensional GAPs via continued fractions*
  (Tao–Vu, Additive Combinatorics §4.4; cf. Chow–Technau,
  arXiv:1810.04558).  The inverse-image of an interval under `x ↦ ax` is
  a rank-2 generalized AP; Lemma A.1 is the degenerate "never actually an
  interval" case of this picture.  The GAP structure theory does not
  state the dichotomy.
- *Dihedral folklore* (permutations preserving the full cyclic-interval
  system are exactly the `2q` rotations/reflections).  Strictly weaker:
  Lemma A.1 forbids a *single* nontrivial interval from mapping to an
  interval, not just all of them simultaneously.
- Cilleruelo–Garaev (GAFA 2011) and the modular-hyperbola concentration
  literature: products/dilates of intervals mod p, but always counting
  bounds, never the exact combinatorial statement.
- Survey §5.2's Sós/Kronecker-permutation papers
  (Bockting-Conrad–Kashina–Petersen–Tenner 2020; Clément 2025) explicitly
  do not treat interval images.

**Verdict: UNCLEAR.**  No exact source was located, but this is an elementary
special case adjacent to mature simple/common-interval and arithmetic-
permutation theory.  The proof is short adjacency counting and the folklore
risk (an exercise in lecture notes or a problem collection) is high.  It
should be presented only as "elementary; we could not locate this exact
statement", with the classical three-distance machinery cited as a neighbor.

---

## N2. Theorem A's shape (unions of affinely related cyclic interval systems admit no hybrid chains)

**Searches run** (in addition to the survey's §6.2–6.3 corpus:
Booth–Lueker 1976; Hsu–McConnell PC-trees 2003; Bläsius–Rutter
simultaneous PQ-ordering, ACM TALG 2016; Chauve–Maňuch–Patterson gapped
k-C1P NP-completeness; Meidanis–Porto–Telles PQR-trees):

1. `"union of two" interval systems permutations "no new" common intervals chains closed family`
2. `disjunction OR union of consecutive-ones constraints PQ-tree "either order" NP-hard boolean combination`
3. FLSY26 §6 (Further questions) read directly — poses only (i) the
   `N(n)` gap and (ii) derandomizing Lemma 2.3; it does **not** pose any
   union-of-interval-systems / switching-chain question.

**Closest prior art and why it does not subsume:**

- The consecutive-ones world composes constraints **conjunctively**
  (PQ-tree REDUCE = intersection of realizable order sets); "union"
  appears only as (a) k-block relaxations *within one order* (gapped
  k-C1P, NP-complete for k ≥ 2) and (b) coupling of several trees by
  order extension (simultaneous PQ-ordering, NP-complete in general).
  Neither concerns nested chains through the union of two interval
  families, and no rigidity statement of the form "the union of two
  consecutive-arrangement families supports no chains beyond the pure
  ones" was found anywhere.
- The "AND"-chain notion (nested *common* intervals: Blin–Faye–Stoye
  2010; de Montgolfier–Raffinot–Rusu 2014; Rusu 2014) is the studied
  interval-specific neighbor.  The final expanded search did locate the
  broad OR/extra-chain phenomenon outside interval terminology: Algaba,
  van den Brink, and Dietz, *Power Measures and Solutions for Games under
  Precedence Constraints*, TI Discussion Paper 15-007/II (2015),
  [Example 4.7, p. 23](https://papers.tinbergen.nl/15007.pdf), exhibits a
  full chain in a union of prefix-state chains that is not one of the
  listed input chains.  Regular-set-system and antimatroid/basic-word
  machinery are therefore material neighbors, although they do not imply
  Theorem A.
- Pure cyclic-interval growth words already have a standard name: arc
  permutations.  See S. Elizalde and Y. Roichman, *Arc permutations*,
  J. Algebraic Combin. 39 (2014),
  [DOI 10.1007/s10801-013-0449-6](https://doi.org/10.1007/s10801-013-0449-6).
- Component-wise, the affine case rests on Lemma A.1 (see N1), whose
  folklore risk is the only realistic route by which a disguised
  precedent could exist; the *chain* conclusion (middle purity + boundary
  conversion) has no located analogue.

**Verdict: POTENTIALLY NOVEL, narrowly scoped.**  No source located states
the repaired affine, balance-sensitive literal-union rigidity theorem.
This classification applies to that exact theorem shape, not to the broad
hybrid/switching-chain framework, whose feasible-word and extra-chain
antecedents are acknowledged above.  Residual risk remains because the
affine core decomposes into the elementary N1 component plus bookkeeping.

---

## N3. Theorem E's mechanism (bounded-defect hull approximation transferring the interval balanced-chain bound to near-interval families)

**Searches run:**

1. `"balanced-chain set system" OR "chain-balance" mABP 2026 arXiv`
2. `"min-partition rank" multilinear branching 2026 Fabris Limaye Srinivasan Yehudayoff follow-up`
3. `discrepancy set system "close to intervals" OR "almost intervals" robustness perturbation transfer lower bound`
4. `"union of two intervals" set system chain balanced random walk discrepancy lower bound`
5. `approximate set by interval hull "defect" OR "symmetric difference" transfer discrepancy bound combinatorics`
6. ECCC TR26-001 page + full-PDF section read; ECCC TR26-043 page (twice,
   incl. revisions) + full-PDF section read; arXiv abs/2604.00746 version
   history; ECCC year-2026 listing scan; CCC'26 accepted papers surfaced
   in search.

**Findings:**

- **[FLSY26]** proves the interval obstruction (Theorem 1.7 = the
  Theorem 4.4 the repository imports) for the *exact* single-order
  interval system only, and applies it to multi-order objects solely via
  per-summand rank subadditivity (§5.5, Theorem 5.14: a Σ_π mABP is
  split, one summand is almost-full-rank, and that summand's *single*
  order is analyzed).  No robustness/perturbation statement, no hull or
  defect notion, no near-interval families anywhere in the paper
  (contents + §§1, 5.5, 5.6, 6 checked directly).
- **[Kush26]** (the only located follow-up citing TR26-001) works in the
  opposite direction (upper bound) with two-block prefix-pair sets — sets
  at defect Θ(n) from every single circle — and contains no hull/defect
  machinery.  Two priority-relevant facts: (i) it is **withdrawn**
  (2026-05-11, Lemma 4.1 filtration gap) with no repair located through
  2026-08-21, so it subsumes nothing; (ii) *if* its claim is ever
  repaired, a polynomial-size 1-balanced-chain system of two-block sets
  would show that no bounded-defect-style transfer can extend to defect
  Θ(n) — making Theorem E's `d = o(n^{1/5})` regime the natural
  complementary territory, not a subsumed one.
- General combinatorial-discrepancy literature: no "hull approximation" /
  "almost interval" transfer principle located (searches 3–5; hits were
  unrelated: directional discrepancy, Brunn–Minkowski stability,
  discrepancy rounding).
- Approximate/gapped common intervals are established neighboring objects,
  including Corteel–Louchard–Pemantle, *Common Intervals in Permutations*,
  DMTCS (2006),
  [DOI 10.46298/dmtcs.362](https://doi.org/10.46298/dmtcs.362), and
  Amir–Gąsieniec–Shalom, *Improved approximate common interval*, IPL
  (2007),
  [DOI 10.1016/j.ipl.2007.03.006](https://doi.org/10.1016/j.ipl.2007.03.006).
  They do not supply the Cycle-5 hull/refinement/FLSY transfer.
- No other 2026 follow-up to FLSY exists on ECCC, and no arXiv cs.CC
  "balanced-chain" paper besides arXiv:2604.00746 was found.

**Closest prior art:** FLSY26 Theorem 1.7/4.4 itself (the imported input;
exact intervals only, one order) and [Kush26] (withdrawn; different
regime, no mechanism overlap).

**Verdict: POTENTIALLY NOVEL, narrowly scoped** — the exact transfer
mechanism (unique-hull +
nested-hull lemmas, stepwise refinement, defect-budgeted completion,
rooted complement reduction to the published interval theorem) was not
located in FLSY, the withdrawn follow-up, general discrepancy sources, or
the approximate-common-interval neighbors.  The classification does not
claim that hull defect or approximate intervals themselves are new.

---

## N4. "Switch depth" and the run-sandwich argument (bounded alternation between two interval systems forcing hull density)

**Searches run:**

1. `nested set chain alternating between two orderings "number of alternations" OR "switches" bounded forces structure`
2. Reuse of the N2/N3 sweeps (switching chains, union systems, hull
   transfer), which would have surfaced any quantitative variant.
3. FLSY26 and Kush26 read directly for any occurrence of the concepts
   (alternation counting between orders; run-length dichotomies;
   density/defect of chain states): none present.  FLSY's multi-order
   handling (§5.5) never lets a chain change order; Kush's chains live in
   one two-block grid family; neither defines anything like `D_mid`, pure
   runs, or a run-length ↔ defect trade-off.

**Findings:** no exact interval-system definition of `D_mid`, nor the exact
run-sandwich inequality `defect ≤ run-length + 2` for `t = 2`, was located.
But the qualitative framework cannot be called unstudied.  Algaba–van den
Brink–Dietz Example 4.7 gives an explicit extra maximal chain created by a
union of input prefix chains; greedoid/antimatroid basic words and
Eppstein's learning-space/chain-antimatroid alternative paths provide
general feasible-route machinery; and arc permutations name the one-order
cyclic words.  These do not contain Cycle 5's quantitative inequality, but
they invalidate an aggregate no-prior-framework conclusion.

**Closest prior art:** regular set systems and feasible orders (Algaba et
al. 2015); greedoid/antimatroid basic words (Björner–Ziegler,
[DOI 10.1017/CBO9780511662041.009](https://doi.org/10.1017/CBO9780511662041.009);
Korte–Lovász–Schrader,
[DOI 10.1007/978-3-642-58191-5](https://doi.org/10.1007/978-3-642-58191-5));
and Eppstein, *Upright-Quad Drawing of st-Planar Learning Spaces* (2008),
[DOI 10.7155/jgaa.00159](https://doi.org/10.7155/jgaa.00159).

**Verdict: UNCLEAR for the aggregate switching framework.**  The narrow
quantitative `D_mid` parameter and run-sandwich inequality may be
`POTENTIALLY NOVEL`, but absence from this bounded search cannot promote
the broader framework to that status.

---

## N5. Literal unions of relabelled RR-type/interval families as balanced-chain systems

**Searches run:** the N3 sweep (exact-term balanced-chain catalogue search:
ECCC 2026 listing, arXiv, CCC'26), plus direct reads of the two located
papers using that terminology, plus the survey's §6 corpus.  Boundary-object
checks: FLSY26 Lemma 1.5/§2 (worst-to-average unions), FLSY26 §5.5
(Σ_π mABP), Kush26 Theorem 2.4 (quoting FLSY's Lemma 2.3 mechanism:
"take O(n/ε) random permutations, apply each to every set, take the
union"), and the CKSS24 / DMPY12 / NNN12 neighbors.

**Findings:**

- **FLSY already publishes the literal-union construction and semantics.**
  Full-version Definition 1.2 takes all full Boolean chains contained in a
  set system.  Full-version Lemma 2.3 (conference Lemma 1.5), for even `n`,
  `|X|=n`, `ell ∈ [n]`, `p ∈ (0,1]`, and a `(p,ell)`-balanced-chain set
  system `𝓧` of size `s`, constructs an `ell`-balanced-chain set system of
  size `O(sn/p)`.  Its proof takes `r = ceil(n/(p lg e))` and literally sets
  `𝓨 = 𝓧 ∪ ⋃_{i=1}^r σ_i(𝓧)`, where
  `σ_i(𝓧) = {σ_i(S) : S ∈ 𝓧}`.  The proof witnesses
  balance using a pure chain inside one copy, but Definition 1.2 still
  includes every hybrid full chain contained in `𝓨`.  Instantiating `𝓧`
  with an RR/interval family gives the Cycle-5 host object.
- FLSY §5.5 + Corollary
  1.8 treat sums of interval-mABPs over different orderings π_i — the
  multi-order object in ABP form — but by rank subadditivity each
  analysis collapses to a single order; a chain never mixes orders.
- **An abstract extra-chain example predates FLSY.**  E. Algaba, R. van den
  Brink, and C. Dietz, *Power Measures and Solutions for Games under
  Precedence Constraints*, Tinbergen Institute Discussion Paper 15-007/II
  (2015), [stable record](https://hdl.handle.net/10419/107876),
  [open PDF](https://papers.tinbergen.nl/15007.pdf), Example 4.7, printed
  p. 23, starts from
  `Π={(1,2,3),(2,3,1),(3,1,2)}` and observes that
  `(∅,{3},{2,3},{1,2,3})` is also a chain in the union, although its
  order `(3,2,1)` was not listed.  This is not interval- or balance-
  specific, but it is direct prior art for "a literal union creates an
  extra/hybrid full chain."  The peer-reviewed article with the same title
  omits this example, so the working paper and page are the supporting
  source.
- Other neighboring objects remain relevant without subsuming the RR-
  specific structural results:
  - **CKSS24** (P. Chatterjee, D. Kush, S. Saraf, A. Shpilka, *Lower
    bounds for set-multilinear branching programs*, CCC 2024, LIPIcs 300,
    20:1–20:20): the predecessor multi-order model (sums of *ordered*
    smABPs, each summand with its own variable order).  Per-summand
    again; the underlying combinatorial object is the single maximal
    prefix chain per order (FLSY's `I_0` remark), not a union set system
    with switching.  This is an ABP-specific neighbor; it does not subsume.
  - **DMPY12** (Dvir–Malod–Perifel–Yehudayoff, STOC 2012): arc-partition
    families on the round-robin wheel — prior art for the *single*
    RR-type cyclic family, no unions, no balanced-chain formalism (which
    postdates it by 14 years).
  - **NNN12** (Newman–Neiman–Nikolov, FOCS 2012, Beck's three-permutations
    counterexample; cited by FLSY themselves): coloring discrepancy of
    the union of the prefix families of 3 permutations — the classical
    interval-union neighbor in *shape* (union of relabelled interval families),
    but with the opposite quantifier structure (max over sets of one
    coloring's discrepancy; no chains, no balance-along-a-chain), so it
    does not subsume.
  - **Kush26**: not a union of relabelled interval families (two-block
    prefix pairs in one order), and withdrawn besides.

**Verdict: KNOWN for the literal-union balanced-chain object.**  FLSY
Definition 1.2 and Lemma 2.3 are decisive.  This does not subsume Cycle 5's
RR-specific minimality, certificates, affine rigidity, or quantitative
switch-depth analysis; those narrower results retain their separate
classifications, at most `POTENTIALLY NOVEL` where stated above.

---

## SEG provenance and novelty addendum

The exact segment-localized statement SEG does not appear verbatim in
FLSY.  FLSY publishes the underlying random-walk/Fréchet machinery; the
offset, rounding, first-leg, tail-arithmetic, and cyclic-full adaptations
are proved in this repository and were checked by the deep, arms-length,
and final Sol audits.  Its mathematical status is **ADVERSARIALLY REVIEWED
PROOF CANDIDATE; UNFORMALIZED**, with verdict **SOUND WITH REPAIRS**.  Its
provenance is **NEW BUT PROVED IN THIS REPOSITORY**, not "published
verbatim".  Its novelty classification is **UNCLEAR**: the exact
localization was not located, but the probabilistic engine is published
FLSY machinery and no novelty certification has been completed for the
adaptation.

---

## Cross-cutting status note (priority-relevant, no verdict)

The O01-status line in `literature/novelty_log.md` was re-verified today:
FLSY's CCC 2026 version leaves `N(n)` open; TR26-043 = arXiv:2604.00746
remains withdrawn (v2, 2026-05-11, Lemma 4.1 filtration gap acknowledged
by the author); no public repair or successor exists as of 2026-08-21.
The Cycle-5 negative theorems therefore retain their program value.  The
bounded searches did not locate the exact N2/N3 statements or the narrow
`D_mid`/run-sandwich quantitative forms; they did locate prior art for the
literal-union object, pure cyclic words, feasible/basic words, and broad
extra-chain/alternative-route mechanisms.  No absence-from-search statement
here is a claim of novelty.

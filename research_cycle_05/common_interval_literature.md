# Literature Reconstruction: Common Intervals of Permutations and Related Structures

**Research cycle 05 — literature survey.**
Date: 2026-08-21. Compiled for the P-vs-NP research program's study of common cyclic intervals of
two cyclic orders C1, C2 on a q-element set (q odd) and of "cross pairs" (A, A∪{y}) with A a
C1-interval and A∪{y} a C2-interval.

**Labeling convention.**
- **[VERIFIED-ONLINE — source]**: claim checked during this survey against the cited document
  (paper PDF read directly, publisher/dblp/arXiv page, or a lecture-notes secondary source; the
  label states which).
- **[KNOWN-UNVERIFIED — citation given]**: classical result stated from background knowledge with a
  checkable citation that was *not* independently confirmed online in this session.
- **[NOT FOUND]**: searched for and not located; honest report of absence.

Primary PDFs read in full or in part during this survey: Bergeron–Chauve–de Montgolfier–Raffinot
(SIAM JDM 2008 version), Heber–Mayr–Stoye (Algorithmica 2011), Albert–Atkinson–Klazar (JIS 2003),
Corteel–Louchard–Pemantle (DMTCS 2006), and the Bielefeld comparative-genomics lecture notes
chapter 8 (Stoye's group, 2018/19).

---

## 1. Common intervals of two (linear) permutations

### 1.1 Definition and basic counts

**Definition.** For a family P = {P_1, …, P_K} of permutations of {1,…,n}, a *common interval* is a
set of integers that is an interval (a set of consecutive elements) in each permutation of the
family. WLOG P_1 = Id_n, so a common interval is a set that is simultaneously a range of values
and, in each other permutation, a range of positions.
**[VERIFIED-ONLINE — read directly from A. Bergeron, C. Chauve, F. de Montgolfier, M. Raffinot,
"Computing common intervals of K permutations, with applications to modular decomposition of
graphs", SIAM J. Discrete Math. 22(3):1022–1039, 2008 (Definition 1); conference version ESA 2005,
LNCS 3669, 779–790.]**
Equivalent formulation used by probabilists: I ⊆ [n] is an interval of the permutation G if
G^{-1}(I) is a set of consecutive positions; counting pairs of intervals (I,J) with G_A(I) = G_B(J)
for two permutations G_A, G_B is equivalent to counting intervals of the single permutation
G_B^{-1} G_A. **[VERIFIED-ONLINE — read from Corteel–Louchard–Pemantle, DMTCS 8(1):189–214, 2006,
Def. 1.1 and intro.]** This is exactly the reduction we use: the common-interval structure of
(C1, C2) depends only on the relative permutation rho = C2 ∘ C1^{-1}.

**Trivial intervals.** The n singletons and the full set [n] are always common intervals ("trivial
intervals"). **[VERIFIED-ONLINE — BCMR 2008, after Def. 1.]**

**Extremes.**
- Maximum: if all permutations are equal (say Id), every interval (i..j) is common, giving
  n(n+1)/2 = C(n+1,2) common intervals (counting singletons and the whole set). This is the maximum
  possible, since common intervals are in particular intervals of Id. **[Elementary arithmetic;
  the C(n,2)-interval count of one permutation and the fact that π = σ attains it is stated in the
  Bielefeld lecture notes, VERIFIED-ONLINE — gi.cebitec.uni-bielefeld.de skript_08.pdf, §8.2.]**
- Minimum: n+1, attained exactly by the *simple* permutations — those mapping no non-trivial
  interval onto an interval (no non-trivial "block"). Smallest examples: 2413 and 3142 (length 4);
  there are no simple permutations of length 3. **[VERIFIED-ONLINE — read from M.H. Albert,
  M.D. Atkinson, M. Klazar, "The enumeration of simple permutations", J. Integer Sequences 6
  (2003), Article 03.4.4 (abstract, and table of simple permutations of length ≤ 5).]**

### 1.2 Efficient algorithms

- T. Uno, M. Yagiura, "Fast algorithms to enumerate all common intervals of two permutations",
  *Algorithmica* 26(2):290–309, 2000. Three algorithms: two simple O(n²)-time algorithms and one
  enumerating all K common intervals of 2 permutations in optimal O(n+K) time and O(n) space.
  **[VERIFIED-ONLINE — dblp rec journals/algorithmica/UnoY00 + Springer article page
  s004539910014; the "three algorithms" breakdown confirmed from the Heber–Mayr–Stoye intro.]**
- S. Heber, J. Stoye, "Finding all common intervals of k permutations", CPM 2001, LNCS 2089,
  207–218: introduces *irreducible intervals*, a generating subset of size O(n); all z common
  intervals of k permutations in optimal O(kn+z) time. **[VERIFIED-ONLINE — Springer chapter
  10.1007/3-540-48194-X_19; journal treatment in Heber–Mayr–Stoye below.]**
- S. Heber, R. Mayr, J. Stoye, "Common intervals of multiple permutations", *Algorithmica*
  60(2):175–206, 2011 (received Jan 2009, online June 2009). Optimal O(kn+z) time, O(n) extra
  space for k permutations; extensions to multichromosomal and circular permutations (see §2).
  Every common interval is a *chain of overlapping irreducible intervals*; there are always fewer
  than n irreducible intervals (the count lies in [1, n−1]). **[VERIFIED-ONLINE — PDF read
  directly (title page, abstract, §§6–8, appendix); the [1,n−1] bound for irreducible intervals is
  Theorem 8 of the Bielefeld notes presentation of this material.]**
- B.-M. Bui-Xuan, M. Habib, C. Paul, "Revisiting T. Uno and M. Yagiura's algorithm", ISAAC 2005,
  LNCS 3827, 146–155: reinterprets the Uno–Yagiura machinery, connecting the family of common
  intervals to (weakly) partitive family theory; companion journal work: "Competitive graph
  searches", *Theoret. Comput. Sci.* 393(1–3):72–80, 2008. **[VERIFIED-ONLINE — Springer chapter
  10.1007/11602613_16 and ScienceDirect S030439750700850X.]**
- A. Bergeron, C. Chauve, F. de Montgolfier, M. Raffinot (BCMR), SIAM JDM 2008 (full citation
  above): the *generator* framework. A generator is a pair of vectors (R, L) with R[i] ≥ i,
  L[j] ≤ j such that (i..j) is a common interval iff L[j] ≤ i ≤ j ≤ R[i]. Generators of a union of
  permutation families combine by (min(R_1,R_2), max(L_1,L_2)) (Prop. 1); the (Sup, Inf) generator
  is computable in O(n) per permutation via stack algorithms (Props. 2–4, Thm. 1: O(Kn) for K
  permutations); a *commuting* generator yields all N common intervals in O(n+N) (Thm. 2); every
  *closed family* has a unique canonical commuting generator (Prop. 7, Thm. 3).
  **[VERIFIED-ONLINE — all read directly from the paper PDF.]**
- I. Belghiti, M. Habib, "A general method for common intervals", arXiv:1309.7141 (2013): generic
  algorithm merging the "potential beginning" technique with generators. **[VERIFIED-ONLINE —
  arXiv abstract.]**

### 1.3 The canonical tree structure: strong intervals, PQ-trees, linear vs prime nodes

**Closed families.** The common intervals of a set of permutations (containing Id) form a *closed
family*: a family of intervals of Id containing all singletons and (1..n), closed under taking
unions, intersections, and differences of *overlapping* members (if (i..k) and (j..l) belong to
the family with i ≤ j ≤ k ≤ l, so do (i..j), (j..k), (k..l), (i..l)). **[VERIFIED-ONLINE — BCMR
§4, read directly.]** In the language of set-family decomposition theory this says the family is
*weakly partitive*; the abstract theory of partitive families is due to M. Chein, M. Habib,
M.C. Maurer, "Partitive hypergraphs", *Discrete Math.* 37(1):35–50, 1981. **[VERIFIED-ONLINE —
ScienceDirect 0012365X81901382 + Semantic Scholar; the "weakly partitive" phrasing for common
intervals is from Bui-Xuan–Habib–Paul and from the Bergeron et al. line of work, VERIFIED-ONLINE
via search snippets of the SIAM paper.]**

**Strong intervals.** A common interval is *strong* if it *commutes* with (i.e., does not overlap:
is disjoint from or nested with) every common interval. The strong intervals, ordered by
inclusion, form a tree (the *inclusion tree* / *strong interval tree*): its root is [n], its
leaves the singletons, each node the union of its children. The number of strong intervals lies
between n+1 and 2n−1. **[VERIFIED-ONLINE — BCMR §5.1, Lemmas 1–4, Prop. 8, read directly,
including the "between n+1 and 2n−1" remark; strong intervals computable in O(n) from the
canonical generator via a stack over the sorted 4n interval bounds (Algorithm 6).]**

**PQ-tree form of the structure theorem (precise statement).** Define a *PQ-tree* as a tree with
leaves labeled 1..n whose internal nodes are P-nodes (at least 2 children) or Q-nodes (at least 3
children, children totally ordered). An *extended frontier* is: the frontier (leaf set) of a
P-node, or the union of frontiers of *consecutive children of a Q-node*, or a singleton. Then:

> **Proposition (BCMR Prop. 9, attributed to the classical PQ-tree literature).** For every closed
> family F there exists a PQ-tree such that the intervals of F are **exactly the extended
> frontiers** of the tree; the **strong intervals of F are exactly the frontiers of the nodes**;
> and the PQ-tree is **unique up to reversal of Q-nodes**.

**[VERIFIED-ONLINE — read directly from BCMR §5.2, Def. 6 and Prop. 9; the bijection between
PQ-trees and closed families is credited there to the classical PQ-tree literature (Booth–Lueker,
see §6).]** BCMR also give the O(1)-per-node labeling test: a node with ≥3 children is a Q-node
iff the union of its first two children is in the family, else a P-node; every node with exactly 2
children is labeled P. Conversions PQ-tree ↔ canonical generator run in O(n) (Prop. 10,
Algorithm 8). **[VERIFIED-ONLINE — read directly.]**

**Strong interval tree / "linear vs prime" dictionary.** In the comparative-genomics phrasing
(strong interval tree of a permutation σ): each internal node of the inclusion tree of strong
intervals carries a *quotient permutation* (the pattern of its children); a node is **linear**
(increasing or decreasing) if its quotient is Id or its reverse, and **prime** otherwise, in which
case the quotient is a *simple* permutation of length ≥ 4. The structure theorem then reads:

> Every common interval of {Id, σ} is either a node of the strong interval tree, or the union of
> consecutive children of a **linear** node; conversely all such unions are common intervals. At a
> prime node, no proper union of ≥2 (but not all) children is a common interval.

This is the same statement as Prop. 9 above under the dictionary {Q-node ↔ linear node with ≥3
children; P-node with 2 children ↔ linear node with quotient 12 or 21; P-node with ≥4 children ↔
prime node with simple quotient} — noting that P-nodes with exactly 3 children cannot occur for
common-interval families since there is no simple permutation of length 3.
**[The equivalence and dictionary are elementary given BCMR Prop. 9 (VERIFIED-ONLINE) and the
nonexistence of length-3 simples (VERIFIED-ONLINE, AAK table). The "linear/prime" terminology is
standard from S. Bérard, A. Bergeron, C. Chauve, C. Paul, "Perfect sorting by reversals is not
always difficult", IEEE/ACM Trans. Comput. Biol. Bioinform. 4(1):4–16, 2007 (conference version
LNCS, "Perfect Sorting by Reversals Is Not Always Difficult", Springer chapter 10.1007/11557067_19)
— journal details KNOWN-UNVERIFIED, chapter existence VERIFIED-ONLINE via Springer link.]**

**Relation to modular decomposition.** A *module* of a graph behaves like a single vertex; strong
modules form the modular decomposition tree, which "is indeed the PQ-tree of the family of
modules". For a *factorizing permutation* of a graph G (a permutation in which every strong module
is an interval — always exists, computable in linear time), the interval-modules form a closed
family whose strong intervals are exactly the strong modules of G (BCMR Prop. 11); this yields
linear-time modular decomposition from common-interval technology. **[VERIFIED-ONLINE — BCMR §6
read directly. Factorizing permutations: C. Capelle, M. Habib, F. de Montgolfier, "Graph
decompositions and factorizing permutations", Discrete Math. Theor. Comput. Sci. 5(1):55–70, 2002
— KNOWN-UNVERIFIED. Survey: M. Habib, C. Paul, "A survey of the algorithmic aspects of modular
decomposition", Computer Science Review 4(1):41–59, 2010; arXiv:0912.1457 — arXiv VERIFIED-ONLINE.]**
For two permutations specifically: common intervals of {Id, σ} = modules of the permutation graph
G_σ; hence the strong interval tree of σ is the modular decomposition tree of G_σ, with linear
nodes ↔ series/parallel (complete/edgeless quotient) modules and prime nodes ↔ prime modules.
**[Standard; follows from BCMR §6 (VERIFIED-ONLINE) plus the classical correspondence between
permutation-graph modules and common intervals — as background see the Habib–Paul survey above.]**

---

## 2. Circular / cyclic common intervals

### 2.1 Complement closure — the basic cyclic phenomenon

**Definition (HMS §7).** Arrange N = {1,…,n} along a circle ("circular permutation"). Given k
circular permutations, c ⊆ N is a *common interval* iff the elements of c occur uninterruptedly
(consecutively on the circle) in each. **[VERIFIED-ONLINE — read directly from Heber–Mayr–Stoye,
Algorithmica 60(2):175–206, §7.]**

**Lemma (HMS Lemma 8).** If c is a common interval of a family of circular permutations, then its
complement N∖c is also a common interval. ("This follows immediately from the definition.")
**[VERIFIED-ONLINE — read directly, statement and proof.]**
This is exactly the complement-closure the research program exploits (for q odd, complementation is
a fixed-point-free involution on the common cyclic intervals with 1 ≤ |c| ≤ q−1, so their number is
even — elementary consequence, no citation needed).
Important caveat verified there: complement-closure holds for the *common intervals* but **not**
for the irreducible-interval basis (explicit counterexample in HMS after Lemma 8), and it **fails**
for *mixed* families in which some chromosomes are linear and some circular (HMS Example 4).
**[VERIFIED-ONLINE — read directly.]**

### 2.2 Algorithms and counts in the circular case

- **Theorem (HMS Thm. 6).** Given k circular permutations of {1,…,n}, all z common intervals can
  be found in optimal O(kn+z) time and O(n) additional space. Method: compute the irreducible
  intervals of size ≤ ⌊n/2⌋ by running the linear-case machinery on **four linearizations** of each
  circular permutation (cutting between positions n and 1, and between ⌊n/2⌋ and ⌊n/2⌋+1),
  suppressing intervals of size > ⌊n/2⌋; generate all common intervals of size ≤ ⌊n/2⌋; then add
  the set of complements. **[VERIFIED-ONLINE — read directly (Algorithm 6, Thm. 6).]**
- Multichromosomal permutations: same optimal complexity (HMS Thm. 5); mixed linear/circular
  chromosomes: same complexity after inserting artificial breakpoints (HMS Thm. 7).
  **[VERIFIED-ONLINE — read directly.]**
- Earlier circular adaptation: S. Heber, J. Stoye, "Algorithms for finding gene clusters",
  WABI 2001, LNCS 2149, 252–263. **[VERIFIED-ONLINE — Springer chapter 10.1007/3-540-44696-6_20
  (title/venue); page numbers KNOWN-UNVERIFIED.]**
- Count remark (elementary): a single circular order on n points has n(n−1) proper nonempty cyclic
  intervals plus n singletons counted therein — i.e., n intervals of each length 1..n−1, plus N
  itself; two identical circular orders attain this maximum. No published extremal theory specific
  to the circular case was found beyond this trivial observation and the linear-case transfer.
  **[NOT FOUND — no dedicated "extremal count of circular common intervals" paper located.]**

### 2.3 Conserved intervals (the signed/genomic variant)

- A. Bergeron, J. Stoye, "On the similarity of sets of permutations and its applications to genome
  comparison", COCOON 2003, LNCS 2697, 79–89; journal version *J. Comput. Biol.* 13(7):1340–1354,
  2006. Introduces *conserved intervals* of sets of signed permutations; shows sets of conserved
  intervals have "elegant nesting and chaining properties" enabling compact graphic representations
  and linear-time algorithms; defines a conserved-interval distance. **[VERIFIED-ONLINE — Springer
  chapter 10.1007/3-540-45071-8_9 and JCB DOI 10.1089/cmb.2006.13.1340 (title/venue/abstract);
  the precise definition below is stated from knowledge: KNOWN-UNVERIFIED in its exact wording.]**
  Definition (standard form): for signed permutations, an interval with endpoints (a, b) is
  *conserved* if in every permutation of the family either a…b appears with the same set of
  elements in between, or −b…−a does. Conserved intervals are the common intervals that are
  additionally "framed" by the same endpoints up to global reversal — a subfamily of the common
  intervals closed under the same nesting/chaining calculus.
- Bergeron's generator technique extends to signed permutations, yielding enumeration of conserved
  intervals. **[VERIFIED-ONLINE — search-level confirmation via the COCOON/JCB abstracts and
  follow-up literature ("New applications of interval generators to genome comparison",
  ScienceDirect S1570866711001018).]**
- A. Bergeron, M. Blanchette, A. Chateau, C. Chauve, "Reconstructing ancestral gene orders using
  conserved intervals", WABI 2004, LNCS 3240, 14–25. Applies conserved-interval structure
  (including to circular genomes) for ancestral reconstruction. **[VERIFIED-ONLINE — Springer
  chapter 10.1007/978-3-540-30219-3_2 (title/venue); page numbers KNOWN-UNVERIFIED.]**
- Unifying frameworks: I. Rusu, "MinMax-profiles: a unifying view of common intervals, nested
  common intervals and conserved intervals of K permutations", *Theoret. Comput. Sci.*
  543:90–111, 2014 (arXiv:1304.5140). **[VERIFIED-ONLINE — cited with full details in the
  Bielefeld notes literature list (image read) + arXiv page.]**

### 2.4 Complement closure vs strong-interval-tree theory — the gap

How does the complement-closure of cyclic common intervals interact with the (rooted) strong
interval tree? Finding: **the literature handles the circular case by linearization, not by a
native cyclic structure theorem.** HMS reduce circular common intervals to four linearizations
plus complementation (VERIFIED-ONLINE, §2.2 above); no paper was found that develops a "cyclic
strong interval tree" or proves a circular analogue of BCMR Prop. 9 in which the tree is unrooted
and complement-invariant. **[NOT FOUND — searched "circular strong intervals", "cyclic strong
interval tree", "PC-tree common intervals".]**

The natural candidate structure exists in the adjacent consecutive-ones literature: **PC-trees**.
W.-L. Hsu, R.M. McConnell, "PC trees and circular-ones arrangements", *Theoret. Comput. Sci.*
296(1):99–116, 2003: an **unrooted** tree with P-nodes (children freely permutable) and C-nodes
(cyclic order fixed up to reversal) representing **all circular orders** of a ground set in which
every row of a circular-ones matrix is a circular arc; circular-ones orderings are exactly the
embeddings obtained by flipping C-nodes. **[VERIFIED-ONLINE — ScienceDirect S0304397502004358 +
author PDF at cs.colostate.edu/~rmm/pctrees.pdf.]** A 0/1 matrix has the *circular-ones property*
iff columns can be ordered so each row's ones or zeros are consecutive — note this definition is
already complement-symmetric row-wise, matching HMS Lemma 8. A. Tucker showed circular-ones
testing reduces to consecutive-ones testing by complementing suitable rows (A. Tucker, "Matrix
characterizations of circular-arc graphs", *Pacific J. Math.* 39(2):535–545, 1971).
**[Reduction VERIFIED-ONLINE as restated in Hsu–McConnell; Tucker's exact bibliographic data
KNOWN-UNVERIFIED.]**
Assessment: the PC-tree is the correct "PQ-tree of a cyclic order", and specializing it to the
family of common cyclic intervals of two cyclic orders (with C-nodes ↔ cyclically-linear nodes,
P-nodes ↔ prime) would give the natural cyclic structure theorem — but **we found no publication
that states this specialization explicitly**. This appears to be genuinely folklore-level open
writing space. **[NOT FOUND]**

---

## 3. Counts and randomness

### 3.1 Random permutations: expected O(1) beyond trivial, Poisson limit

- Uno–Yagiura computed, for a uniform random permutation of [n] (equivalently a uniform random
  pair), E(X_2) = 2(n−1)/n, E(X_3) = 6(n−2)/(n(n−1)), and E(X_k) ≤ 24/n² for k ≥ 4, where X_k is
  the number of common intervals of size k. **[VERIFIED-ONLINE — restated with formulas in
  Corteel–Louchard–Pemantle §2, read directly, crediting Uno et al.]**
- **Poisson limit.** S. Corteel, G. Louchard, R. Pemantle, "Common intervals in permutations",
  *Discrete Math. Theor. Comput. Sci.* 8(1):189–214, 2006 (preliminary version in *Mathematics and
  Computer Science III*, Trends in Mathematics, Birkhäuser 2004): as n → ∞ the number X of proper
  intervals (sizes 2..n−1) of a uniform random permutation converges in distribution to
  **Poisson(2)** (Prop. 2.1); nearly all mass comes from intervals of size 2. **[VERIFIED-ONLINE —
  PDF read directly (title page, Prop. 2.1 and displayed expectations).]**
- For k ≥ 2 independent uniform permutations, the expected number of common intervals of size ≥ 2
  (including [n] itself) is E(X^k) = 3 + O(n^{-1}) if k = 2 and 1 + O(n^{-1}) if k > 2.
  **[VERIFIED-ONLINE — Heber–Mayr–Stoye, Appendix A.1, read directly, including the proof sketch
  E(X^k_{n-1}) = 2^k/n^{k-1} etc.]** So beyond the n+1 trivial intervals a random pair has ≈ 2
  extra common intervals in expectation, and a random triple essentially none.
- Consequence used everywhere in the algorithmics: expected running time O(kn) for the optimal
  enumerators on random inputs. **[VERIFIED-ONLINE — HMS conclusion + appendix.]**
- Richer statistics (δ-intervals / gene teams): CLP also study "δ-intervals" (gaps ≤ δ−1 allowed);
  for δ = 2 the count is exponentially large but tightly concentrated (quenched = annealed means,
  Thm. 4.1 there; no Gaussian limit, Thm. 7.1). **[VERIFIED-ONLINE — read directly from CLP
  pp. 189–191.]** (Relevant to us only as a warning: relaxations of consecutivity change the count
  regime from O(1) to exponential.)

### 3.2 Density and asymptotics of simple permutations

- Let s_n be the number of simple permutations of length n; s_1..s_12 =
  1, 2, 0, 2, 6, 46, 338, 2926, 28146, 298526, 3454434, 43286526 (OEIS A111111).
  **[VERIFIED-ONLINE — AAK paper read directly; OEIS A111111.]**
- **Correct constant: e^{-2}, not e^{-2} of something else.** Main term: s_n / n! = e^{-2} + O(1/n)
  (AAK Observation 8), and the refined expansion proved in AAK §3:
  **s_n = (n!/e²) · (1 − 4/n + 2/(n(n−1)) + O(n^{-3}))**.
  **[VERIFIED-ONLINE — read directly from AAK pages 10–12, including the final display and the
  worked bootstrap; the paper notes the relative error at n = 20 is ≈ 3.89·10^{-3}.]**
- Provenance of the method: Kaplansky's 1940s analysis of permutations with no block of length 2
  gives n!/e² · (1 − 2/(n(n−1)) + O(n^{-3})) for that easier class; the probabilistic argument
  "implicitly given by Uno and Yagiura, made explicit by Corteel, Louchard and Pemantle"; the
  underlying technique goes back to Kaplansky and Wolfowitz on runs.
  **[VERIFIED-ONLINE — AAK page 8 read directly + the search-level summary of the AAK/JIS paper;
  I. Kaplansky, "The asymptotic distribution of runs of consecutive elements", Ann. Math.
  Statist. 16:200–203, 1945, and J. Wolfowitz's runs papers: KNOWN-UNVERIFIED exact data.]**
- Also in AAK: (s_n) is **not P-recursive**; the generating function S(x) relates to the
  functional inverse of F(x) = Σ k! x^k (coefficients differing alternately by ±2); congruence
  properties of the coefficients. **[VERIFIED-ONLINE — read directly from AAK pages 2 and 13.]**
- Distributional shape of the whole tree for a random permutation: M. Bouvel, C. Chauve,
  M. Mishna, D. Rossin, "Average-case analysis of perfect sorting by reversals", CPM 2009, LNCS
  5577, 314–325; journal version *Discrete Math. Algorithms Appl.* (arXiv:1201.0940; earlier
  arXiv:0901.2847). Uses expected values of strong-interval-tree parameters of random (signed)
  permutations; the average strong interval tree is dominated by a prime root with the trivial
  intervals below it (consistent with the Poisson(2) picture). Related enumerative study of the
  trees themselves: M. Bouvel et al., "Some families of trees arising in permutation analysis",
  *Electron. J. Combin.* 27(2), #P2.20 (2020). **[VERIFIED-ONLINE — Springer chapter
  10.1007/978-3-642-02441-2_28, arXiv pages, and combinatorics.org PDF (first-author page);
  full author list of the EJC paper not confirmed in this session — KNOWN-UNVERIFIED beyond
  M. Bouvel.]**

---

## 4. Permutations with rich common-interval structure

### 4.1 Substitution decomposition / inflation (wreath) notation

**Inflation.** σ[α_1,…,α_k] is obtained from σ (length k) by replacing its i-th entry by an
interval order-isomorphic to α_i ("wreath product for permutations"; the pattern of the block
decomposition is σ). Example from the source: 67183524 = (3142)[12, 1, 1, 2413].
**[VERIFIED-ONLINE — AAK pages 3–4 read directly.]**

**Decomposition theorem (AAK Theorem 1).** For every non-singleton permutation π there is a
**unique simple non-singleton** σ and permutations α_1,…,α_k with π = σ[α_1,…,α_k]. If σ ∉ {12,21}
the α_i are also uniquely determined; if σ = 12 (resp. 21), uniqueness holds under the extra
condition that α_1 be plus- (resp. minus-) indecomposable. **[VERIFIED-ONLINE — statement and
proof read directly from AAK.]** The same theorem underlies M.H. Albert, M.D. Atkinson, "Simple
permutations and pattern restricted permutations", *Discrete Math.* 300(1–3):1–15, 2005: a pattern
class with finitely many simple permutations is finitely based and has an algebraic generating
function. **[VERIFIED-ONLINE — search-level confirmation of venue/volume/result.]**
Survey of the whole area: R. Brignall, "A survey of simple permutations", in *Permutation
Patterns*, LMS Lecture Note Series 376, CUP 2010, 41–65; arXiv:0801.0963. **[VERIFIED-ONLINE —
arXiv + Cambridge chapter page; page range KNOWN-UNVERIFIED.]**

**How common intervals of an inflation decompose.** From the uniqueness proof (maximal proper
blocks either pairwise disjoint or of 12/21 type): every block (interval mapped to an interval) of
π = σ[α_1,…,α_k] with σ simple, k ≥ 4, is either contained in a single inflated block α_i or is a
union of *all* of them; for σ = 12…k / k…21 (linear case), blocks are unions of consecutive α_i as
well. Iterating gives exactly the strong-interval-tree picture of §1.3: the substitution
decomposition tree = strong interval tree; linear nodes contribute C(d+1,2)-type counts over their
d children, prime nodes contribute only themselves. **[VERIFIED-ONLINE at the level of AAK's
Theorem 1 and BCMR Prop. 9, which jointly imply this; no separate citation needed.]**

### 4.2 Separable permutations = all-linear strong interval trees

- Separable permutations: the closure of {1} under direct sums ⊕ and skew sums ⊖; equivalently
  the class Av(2413, 3142); equivalently the permutations whose substitution decomposition
  (strong interval tree) has **only linear nodes**. Introduced algorithmically by P. Bose,
  J.F. Buss, A. Lubiw, "Pattern matching for permutations", *Inform. Process. Lett.* 65(5):277–283,
  1998: permutation pattern matching is NP-complete in general, polynomial when the pattern is
  separable. **[VERIFIED-ONLINE — ScienceDirect S0020019097002093 + search summary confirming
  volume/pages/results; the ⊕/⊖ characterization VERIFIED-ONLINE via the "Unsplittable classes of
  separable permutations" arXiv search snippet.]**
- Enumeration: separable permutations of length n are counted by the large Schröder numbers.
  **[KNOWN-UNVERIFIED — standard; see J. West, "Generating trees and the Catalan and Schröder
  numbers", Discrete Math. 146:247–262, 1995.]**
- These are the natural "maximally rich" family for common intervals: every node linear means
  every internal edge of the tree spawns quadratically many overlapping common intervals in its
  scope, and **deep** strong interval trees (long root–leaf chains of nested strong intervals) are
  exactly long chains of nested common intervals. The extreme is the identity/monotone case
  (a single linear node / left comb, all C(n+1,2) intervals common). **[Interpretation; follows
  from §1.3, no separate citation.]**

### 4.3 Families {rho^j} of iterates sharing interval structure

**[NOT FOUND.]** Searches for "common intervals of powers of a permutation", "iterates of a
permutation sharing interval structure", and variants located nothing: the literature computes
common intervals of *given* families (typically genomes), never of the cyclic group generated by a
single permutation. Two adjacent facts worth recording:
- If B is a block system (partition into blocks of imprimitivity) for the cyclic group ⟨rho⟩ and
  the blocks are intervals of the reference order, then every rho^j maps each block to a block —
  but common-interval theory does not require invariance, only interval-to-interval, so the
  imprimitivity literature does not answer the question. **[Interpretation, no citation.]**
- Automorphism/consistency questions for PQ-trees (which orders does a given tree admit) are
  classical (Booth–Lueker, §6), but "which permutations rho have all powers consistent with a
  common PQ-tree" appears unstudied. **[NOT FOUND]**

---

## 5. Multiplication maps x ↦ a·x mod q and cyclic intervals

### 5.1 The three-distance theorem and its arithmetic

- **Three-distance (three-gap) theorem, Steinhaus conjecture.** Placing the points
  {α, 2α, …, Nα} (mod 1) on the circle partitions it into arcs of at most **three** distinct
  lengths, the largest being the sum of the other two; the lengths and multiplicities are governed
  by the continued fraction expansion of α (best approximations / Farey convergents). Conjectured
  by Steinhaus; proved in the late 1950s by V.T. Sós, J. Surányi, and S. Świerczkowski
  (independently, various forms). **[VERIFIED-ONLINE — Wikipedia "Three-gap theorem"; T. van
  Ravenstein, "The three gap theorem (Steinhaus conjecture)", J. Austral. Math. Soc. Ser. A
  45:360–370, 1988 (Cambridge Core page VERIFIED for title/venue; pages KNOWN-UNVERIFIED);
  V. Berthé, C. Reutenauer, "On the three-distance theorem", Math. Intelligencer (Springer article
  s00283-023-10316-z) VERIFIED-ONLINE.]**
  Classical original citations **[KNOWN-UNVERIFIED]**: V.T. Sós, "On the distribution mod 1 of the
  sequence nα", Ann. Univ. Sci. Budapest. Eötvös Sect. Math. 1:127–134, 1958; J. Surányi, "Über
  die Anordnung der Vielfachen einer reellen Zahl mod 1", ibid. 1:107–111, 1958;
  S. Świerczkowski, "On successive settings of an arc on the circumference of a circle",
  Fund. Math. 46:187–189, 1958.
- Survey connecting three-distance theorems to Sturmian/mechanical words and generalizations
  (three-distance for chunks, N-distance variants): P. Alessandri, V. Berthé, "Three distance
  theorems and combinatorics on words", *Enseign. Math.* 44:103–132, 1998. **[VERIFIED-ONLINE —
  multiple confirming sources in search results.]**
- The rational case α = a/q with the points {ja mod q : 0 ≤ j < m} is the exact statement needed
  for multiplication maps on Z_q: the gaps of {0, a, 2a, …, (m−1)a} mod q take at most three
  values determined by the Ostrowski/continued-fraction data of a/q. **[Standard specialization;
  covered by the general theorem (van Ravenstein treats rational α explicitly —
  KNOWN-UNVERIFIED detail).]**
- **Ostrowski representation** (numeration system from the continued fraction of α, governing
  which prefixes {1..m} produce which gap patterns): A. Ostrowski, "Bemerkungen zur Theorie der
  Diophantischen Approximationen", Abh. Math. Sem. Univ. Hamburg 1:77–98, 1922.
  **[KNOWN-UNVERIFIED — standard citation; modern treatments in Allouche–Shallit, *Automatic
  Sequences*, CUP 2003, and in Berthé's surveys.]**
- Algorithmic-flavored appearance of three-distance: Fibonacci hashing analysis, D.E. Knuth,
  *TAOCP* vol. 3, §6.4. **[KNOWN-UNVERIFIED.]**

### 5.2 Permutations induced by rotations ("Sós/Kronecker permutations")

- S. Bockting-Conrad, Y. Kashina, T.K. Petersen, B.E. Tenner, "Sós permutations", arXiv:2007.01132
  (2020): for f(x) = αx + β mod 1, the *Sós permutation* sorts f(0), …, f(n); bijection between
  Sós permutations and regions of a parameter-space partition; a "three areas" theorem (within a
  Farey strip at most three region areas occur, one the sum of the other two).
  **[VERIFIED-ONLINE — arXiv abstract.]**
- Follow-up: "Monotone subsets in lattices and the Schensted shape of a Sós permutation",
  arXiv:2107.11515 (2021): the RSK shape of a Sós permutation is piecewise linear with at most two
  slopes, described by the continued fraction of α (builds on Boyd–Steele's work on monotone
  subsequences of {iα}). **[VERIFIED-ONLINE — arXiv listing/snippet.]**
- F. Clément, "Regular structures in Kronecker permutations", arXiv:2509.03782 (2025): permutations
  induced by finite Kronecker sequences (kα mod 1); regularity results (e.g., for quadratic
  irrationals infinitely many n give permutations with all cycles of length ≤ 4). Does **not**
  treat intervals/common intervals. **[VERIFIED-ONLINE — arXiv abstract.]**
These give the state of the art on "structure of the permutation induced by a rotation". The
multiplication permutation π_a: x ↦ ax mod q is the *inverse-transpose* situation: it is
piecewise-order-preserving with exactly a increasing runs (for 1 ≤ a < q), and its interval
structure is governed by the same continued-fraction data of a/q. **[Elementary/standard framing;
the "a ascending runs" fact is elementary.]**

### 5.3 Disorder statistics of π_a(x) = ax mod q: Dedekind sums and Zolotarev

- **Inversions.** I(a,b) := inv(π_{a,b}) for π: x ↦ ax mod b on {0,…,b−1} satisfies **Meyer's
  theorem**: I(a,b) = −3b·s(a,b) + (b−1)(b−2)/4, where s(a,b) is the Dedekind sum; reciprocity for
  Dedekind sums transfers to 4a·I(a,b) + 4b·I(b,a) = (a−1)(b−1)(a+b−1). **[VERIFIED-ONLINE —
  search-level confirmation via K. Girstmair, "Dedekind sums s(a,b) and inversions modulo b",
  Int. J. Number Theory (World Scientific DOI 10.1142/S1793042115501067) and related arXiv papers;
  attribution to C. Meyer KNOWN-UNVERIFIED in detail.]**
- **Sign.** Zolotarev's lemma: for odd b, sgn(π_{a,b}) = (−1)^{I(a,b)} equals the Jacobi symbol
  (a|b). **[VERIFIED-ONLINE — same sources; original: G. Zolotarev, 1872, Nouvelles Ann. Math. —
  KNOWN-UNVERIFIED exact data.]**
- Dedekind sums are computable from the continued fraction of a/b (Barkan; Hickerson, 1977) —
  the same arithmetic object that controls the three-distance structure. **[KNOWN-UNVERIFIED —
  P. Barkan, C. R. Acad. Sci. Paris 284 (1977); D. Hickerson, "Continued fractions and density
  results for Dedekind sums", J. Reine Angew. Math. 290:113–116, 1977.]**

### 5.4 Common intervals of multiplication permutations specifically

**[NOT FOUND.]** No publication was located that explicitly studies (i) which cyclic intervals of
Z_q map to cyclic intervals under x ↦ ax mod q, (ii) the common (cyclic) intervals of the pair
(standard cyclic order, multiplication-by-a order), or (iii) block/interval structure of π_a in the
sense of §1. Searches tried: "common intervals multiplication permutation", "ax mod n interval
image interval", "multiplication modulo intervals three-distance", "Kronecker/Sós permutation
common intervals". The community that studies π_a (number theorists: Dedekind sums, Zolotarev,
lattice tests for linear congruential generators) measures *global disorder* (inversions, sign,
discrepancy), not *interval preservation*; the community that studies common intervals
(comparative genomics) never takes arithmetic permutations as input. The three-distance /
Ostrowski toolkit (§5.1) is clearly the right instrument — a size-m cyclic interval I has image aI
= an arithmetic progression with difference a, and whether an AP with difference a is a cyclic
interval is exactly a three-distance/gap question for {0, a, …, (m−1)a} mod q — but this
translation appears to be unwritten. **[Assessment; the mathematical statement in the last clause
is our framing, not a citation.]**

---

## 6. Switching / hybrid chains, unions and intersections of interval systems

This section reports on the caller's central speculative notion: chains ∅ ⊂ A_1 ⊂ A_2 ⊂ … growing
one element at a time, each A_i an interval in **at least one** of t given orders; and "cross
pairs" (A, A∪{y}) with A a C1-interval and A∪{y} a C2-interval.

### 6.1 Nested common intervals — the "interval in BOTH orders at every level" chain

The closest studied notion requires every set of the chain to be an interval in **both/all**
orders:
- G. Blin, D. Faye, J. Stoye, "Finding nested common intervals efficiently", *J. Comput. Biol.*
  17(9):1183–1194, 2010 (conference version RECOMB-CG 2009, LNCS 5817). Formalizes *nested common
  intervals* between two genomes; O(n³) for all, O(n²) irredundant output, **linear time for
  maximal nested common intervals**; approximate/gapped variants FPT. **[VERIFIED-ONLINE — Liebert
  DOI 10.1089/cmb.2010.0089 + Springer chapter 10.1007/978-3-642-04744-2_6; exact page range
  KNOWN-UNVERIFIED.]**
- F. de Montgolfier, M. Raffinot, I. Rusu, "Easy identification of generalized common and
  conserved nested intervals", *J. Comput. Biol.* 21(7):520–533, 2014. **[VERIFIED-ONLINE —
  DOI 10.1089/cmb.2013.0146 (title/venue/authors); volume/pages KNOWN-UNVERIFIED.]**
- I. Rusu, "MinMax-profiles" (full citation §2.3): uniform treatment of common, nested common, and
  conserved intervals of K permutations. **[VERIFIED-ONLINE.]**
Within one order, maximal chains of nested common intervals are root-leaf paths in the strong
interval tree augmented by the linear-node unions (§1.3) — so "nested chains of common intervals"
is well-understood machinery in the both-orders regime. **[Interpretation of §1.3.]**

### 6.2 Consecutive-ones machinery: PQ-trees, PC-trees, and their combinations

- K.S. Booth, G.S. Lueker, "Testing for the consecutive ones property, interval graphs, and graph
  planarity using PQ-tree algorithms", *J. Comput. Syst. Sci.* 13(3):335–379, 1976. PQ-trees
  represent **all** column orders realizing the consecutive-ones property (C1P); built
  incrementally by REDUCE steps — which is precisely "PQ-tree intersection": imposing the
  constraints of a second interval system onto the tree of a first is done row by row, so the
  *intersection* of two C1P-realizable order sets is again PQ-tree-representable and computable in
  linear time. Common intervals of K permutations is the inverse problem ("consecutive
  arrangement"). **[VERIFIED-ONLINE — dblp (exact volume/pages) + the consecutive-arrangement
  framing read directly in HMS intro; the intersection-by-reduction reading is standard.]**
- PQR-trees — the extension that survives *failure* of C1P (records the obstruction): J. Meidanis,
  O. Porto, G.P. Telles, "On the consecutive ones property", *Discrete Appl. Math.* 88:325–354,
  1998. **[VERIFIED-ONLINE — ScienceDirect S0166218X9800078X + Meidanis' PQR project page;
  page range KNOWN-UNVERIFIED.]**
- **Circular-ones property and PC-trees**: see §2.4 (Hsu–McConnell 2003, Tucker 1971)
  **[VERIFIED-ONLINE / KNOWN-UNVERIFIED as noted there]**. Experimental comparison:
  "Experimental comparison of PC-trees and PQ-trees", ACM J. Exp. Algorithmics (2023)
  (arXiv:2106.14805). **[VERIFIED-ONLINE — ACM DOI 10.1145/3611653.]**
- **Simultaneous PQ-ordering.** T. Bläsius, I. Rutter, "Simultaneous PQ-ordering with applications
  to constrained embedding problems", *ACM Trans. Algorithms* 12(2):16:1–16:46, 2016 (SODA 2013;
  arXiv:1112.0245). Input: several PQ-trees plus child–parent relations on shared leaf sets;
  question: can leaf orders be chosen for all trees simultaneously so each parent order extends
  each child order? **NP-complete in general; polynomial for "2-fixed" instances**, which cover
  partially PQ-constrained planarity etc. This is the only developed framework we found for
  "coupling several interval systems through shared ground sets", and is the natural home for
  questions like "does there exist one order consistent with prescribed interval families on
  overlapping subsets". **[VERIFIED-ONLINE — dblp journals/talg/BlasiusR16 + arXiv + ACM page.]**
- **Unions of interval systems / k-block relaxations.** A matrix has the *k-consecutive-ones
  property* if columns can be ordered so each row's ones split into ≤ k blocks (i.e., each set is
  a union of ≤ k intervals of ONE order — note: one order with k blocks, not k orders with one
  block). Deciding it is **NP-complete for k ≥ 2**; with bounded gaps, the gapped (k,δ)-C1P is
  NP-complete for all k ≥ 2, δ ≥ 1, (k,δ) ≠ (2,1). C. Chauve, J. Maňuch, M. Patterson, "On the
  gapped consecutive-ones property", EuroComb 2009, ENDM 34:121–125; M. Patterson, J. Maňuch et
  al., "Hardness results for the gapped consecutive-ones property", arXiv:0912.0309.
  **[VERIFIED-ONLINE — EuroComb PDF on Chauve's SFU page + arXiv abstract; ENDM volume/pages
  KNOWN-UNVERIFIED. Caution: author order for the arXiv version not re-checked.]**
  Adjacent: *d-track interval* graphs (sets that are unions of one interval on each of d disjoint
  linear orders) — recognition is NP-complete already for d = 2 (D.B. West, D.B. Shmoys,
  "Recognizing graphs with fixed interval number is NP-complete", Discrete Appl. Math. 8:295–305,
  1984). **[KNOWN-UNVERIFIED — standard citation, not re-checked online.]**

### 6.3 The switching-chain notion itself

**[FINAL CROSS-MODEL CORRECTION.]** The original searches ("each prefix is an interval in one of
two permutations", "chains of sets interval in at least one order", "simultaneous consecutive
ones two orders", "growing set one element at a time interval", plus the §6.2 corpus) found no
publication under the exact interval-system phrasing studying:
1. chains of nested sets, each a member of the **union** of two (or t) interval systems
   ("interval in C1 **or** C2 at each level"),
2. cross pairs (A, A∪{y}) with A an interval of C1 and A∪{y} an interval of C2, or the reachability
   /connectivity structure they generate,
3. one-element-growth processes alternating between the interval systems of several orders.
That non-detection is limited to the **exact interval-specific and quantitative specialization**.
The broader feasible-word and extra-chain phenomenon has direct prior art:

- S. Elizalde and Y. Roichman, "Arc permutations", *J. Algebraic Combin.* 39 (2014), 301–334,
  DOI [10.1007/s10801-013-0449-6](https://doi.org/10.1007/s10801-013-0449-6): the defining
  condition that every prefix is a cyclic interval gives the standard name for a pure one-circle
  growth word.
- T. Borém Fabris, N. Limaye, S. Srinivasan, A. Yehudayoff, "Multilinear Algebraic Branching
  Programs and the Min-Partition Rank Method", ECCC TR26-001 / CCC 2026,
  [DOI 10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22): Definition 1.2
  evaluates all full Boolean chains contained in a set system, and full-version Lemma 2.3
  constructs the literal union `𝓨 = 𝓧 ∪ ⋃_i σ_i(𝓧)` of relabelled copies. The proof uses pure
  witness chains, but the literal union semantically contains any hybrid chains too.
- E. Algaba, R. van den Brink, C. Dietz, "Power Measures and Solutions for Games under Precedence
  Constraints", Tinbergen Institute Discussion Paper 15-007/II (2015),
  [stable record](https://hdl.handle.net/10419/107876), [open PDF](https://papers.tinbergen.nl/15007.pdf),
  Example 4.7, printed p. 23: the union of prefix-state chains for
  `Π={(1,2,3),(2,3,1),(3,1,2)}` also contains the full chain for `(3,2,1)`, which was not an
  input order. This is an explicit abstract extra/hybrid chain. The later journal article omits
  this example, so the working paper is the supporting primary source.
- Feasible/basic words and alternative maximal paths are standard neighborhoods in
  greedoids/antimatroids and learning spaces: A. Björner and G. Ziegler, "Introduction to
  Greedoids" (1992), [DOI 10.1017/CBO9780511662041.009](https://doi.org/10.1017/CBO9780511662041.009);
  B. Korte, L. Lovász, R. Schrader, *Greedoids* (1991),
  [DOI 10.1007/978-3-642-58191-5](https://doi.org/10.1007/978-3-642-58191-5); and D. Eppstein,
  "Upright-Quad Drawing of st-Planar Learning Spaces" (2008),
  [DOI 10.7155/jgaa.00159](https://doi.org/10.7155/jgaa.00159). A rooted connected-set family of a
  graph is a standard node-search-antimatroid neighbor of the rooted cyclic family.

Nested **common** intervals (§6.1), simultaneous PQ-ordering (§6.2), and k-block C1P (§6.2) remain
the closest interval-order-specific neighbors. The exact cross-pair characterization, affine
no-hybrid theorem, `D_mid` parameter, and run-sandwich inequality were not located. Their absence
from this bounded search does not make the aggregate switching framework new.

---

## Assessment (requested conclusion)

**Is "common cyclic intervals of two cyclic orders + cross pairs (A, A∪{y})" standard, partially
standard, or unstudied?**

**Partially standard; the broad switching phenomenon has prior art, while the exact
interval-specific quantitative theory was not located.** In detail:

1. **Common intervals of two linear orders: fully standard.** Definition, optimal O(n+K)
   enumeration (Uno–Yagiura 2000), the closed-family/weakly-partitive axiomatics, generators, and
   the exact structure theorem — strong intervals form a tree, PQ-tree with P/Q (prime/linear)
   nodes, common intervals = nodes plus unions of consecutive children of linear nodes, tree unique
   up to Q-reversals (BCMR 2008) — plus the modular-decomposition dictionary, are all textbook-level
   settled, and the random-case count is sharp (Poisson(2) beyond trivial; simple permutations have
   density e^{-2} with s_n = (n!/e²)(1 − 4/n + 2/(n(n−1)) + O(n^{-3}))).
2. **Common cyclic intervals of cyclic orders: standard algorithmically, thin structurally.** The
   definition, the complement-closure lemma (interval iff complement interval), and optimal
   O(kn+z) enumeration are published (Heber–Mayr–Stoye), and conserved intervals give a signed
   variant with its own calculus (Bergeron–Stoye). But the literature handles circles by
   linearization; a native cyclic structure theorem (an unrooted, complement-invariant
   "PC-tree of strong cyclic intervals" analogous to BCMR's theorem) appears never to have been
   written down, even though the PC-tree technology for it exists.
3. **Common intervals of the multiplication permutation x ↦ ax mod q: exact source not located.**
   The exact question "which cyclic intervals have interval images under multiplication" was not
   found anywhere; the obviously relevant toolkit (three-distance theorem, Ostrowski numeration,
   continued fractions, and — for disorder statistics — Dedekind sums/Zolotarev) is classical and
   ready, but no statement of the translation to common-interval structure was located in this
   search.
4. **Switching/hybrid chains and cross pairs: aggregate status UNCLEAR.** Literal unions of
   relabelled set systems under full-chain semantics are published in FLSY Lemma 2.3, and Algaba
   et al. Example 4.7 explicitly shows a union creating an additional full chain. Arc
   permutations, regular set systems, and greedoid/antimatroid basic words supply further standard
   vocabulary. The exact interval-OR cross-pair theory, affine rigidity, switch-depth parameter,
   and run-sandwich inequality were not located; those narrower forms are not subsumed by the
   broad antecedents.

Net: the program can cite a mature foundation for items 1–2; it should describe item 3 only as an
exact formulation not located, with three-distance/Ostrowski and arithmetic-permutation theory as
classical neighbors. It must not call the broad item-4 object new. The defensible bounded-search
claim is only that the exact interval-specific cross-pair and quantitative switching results were
not located, with FLSY literal unions, Algaba's extra chain, arc permutations, regular systems,
antimatroids, nested common intervals, and simultaneous PQ-ordering all cited as material prior
art.

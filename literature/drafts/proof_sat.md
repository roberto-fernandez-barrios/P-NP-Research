# Phase 0/1 reconstruction: proof complexity and SAT algorithms

**Scope.** Independent reconstruction for the first research cycle, restricted to (i) proof
complexity and its proof-search / bounded-arithmetic interfaces and (ii) exact exponential SAT
algorithms and circuit-SAT-to-lower-bound bridges. This is a draft input to the repository-wide
Phase 0/1 synthesis. It does not attempt a separation of P from NP.

**Search date.** 2026-08-13. Sources are primary papers or author/venue copies wherever one was
found. Recent 2025--2026 claims are identified as preprints when they have not appeared in a
refereed venue. An unsuccessful web search is evidence about discoverability, not a proof that a
problem is open.

**Epistemic labels used here.**

- **KNOWN**: a cited theorem, with its model and qualifications stated.
- **OPEN**: explicitly posed as open in a primary/current source and not closed by the follow-up
  searches recorded below.
- **CONJECTURED**: stated as a conjecture by its authors.
- **FALSE-AS-WRITTEN (proof candidate)**: an explicit counterexample was derived in this cycle;
  it has an elementary proof and finite checks, but has not yet received external review.
- **UNKNOWN-STATUS**: the search did not support a confident open/closed classification.

## 1. Ground truth in one page

1. A polynomially bounded Cook--Reckhow proof system for TAUT exists iff
   \(\mathsf{NP}=\mathsf{coNP}\). This is not the same as \(\mathsf P=\mathsf{NP}\), and the
   original paper's webpage notes a correction to a corollary that had used the latter wording.
2. Resolution has sharp and reusable size--width machinery and exponential lower bounds for many
   explicit formulas. Nevertheless, *finding* near-shortest resolution refutations is NP-hard.
   This does not settle **weak** automatizability, which allows proof search in a stronger system.
3. No superpolynomial lower bound is known for unrestricted Frege or Extended Frege proofs of a
   polynomial-size family of propositional tautologies. Fixed-depth Frege is very different:
   exponential lower bounds are known. Adding MOD gates, already \(\mathrm{AC}^0[p]\)-Frege,
   remains a major frontier.
4. General cutting planes has exponential length lower bounds, but it also has a universal
   inequality-space-5 upper bound using large coefficients. With coefficients bounded by a fixed
   constant, the best explicit inequality-space lower bound found is only
   \(\Omega(\log\log\log n)\).
5. Polynomial calculus has robust degree and size--degree lower-bound technology. Space is much
   less understood. For Tseitin formulas on simple fixed-degree expanders of degree below six, the
   current generic lower bound is \(\Omega(\sqrt n)\), while linear space is known after an XOR
   substitution / doubled-edge construction and \(\Omega(n/\log n)\) is known for sufficiently
   large constant degree.
6. Feasible interpolation converts some proof lower bounds to circuit lower bounds. It works for
   Resolution and Cutting Planes, but conditional negative results show that one should not assume
   it for Frege or bounded-depth threshold Frege. Weak automatizability of Resolution is equivalent
   to feasible interpolation for \(\mathrm{Res}(2)\).
7. CDCL with restarts can polynomially simulate Resolution under precise learning and branching
   models. Width-\(k\) Resolution can be found by a randomized clause-learning procedure in
   \(n^{O(k)}\) conflicts. Standard learning has a real cost: merge-based systems can require a
   quadratic proof where Resolution has a linear one.
8. For worst-case 3-SAT on \(n\) variables, the verified deterministic benchmark located is
   \(O(1.32793^n)\) (Liu 2018). A July 2026 preprint claims randomized
   \(O^*(1.307031578^n)\) for general 3-SAT by a tighter analysis of the unchanged PPSZ algorithm.
   These are exponential-time results; they do not imply polynomial-time SAT.
9. The Williams algorithm-to-lower-bound bridge requires a nontrivial SAT algorithm for the
   *same circuit class*, for every polynomial size exponent (plus exact closure/constructibility
   hypotheses in restricted-class versions). A faster \(k\)-CNF algorithm alone is not a general
   circuit lower bound.
10. The Alekseev--Gaevoy 2026 affine-union robustness conjecture used for their conditional
    polynomial-depth \(\mathrm{Res}(\oplus)\) result appears **false as written**. Coordinate
    subspaces indexed by the middle layer of a Boolean cube give an elementary asymptotic
    counterexample for every \(q>1\), including \(q=3\), and every fixed \(r>0\). Independently,
    the printed application has codimension and error-parameter gaps. They look amenable to
    reparameterization for a coarser conclusion, but this audit does not certify the claimed
    conditional theorem as written.

## 2. Proof systems: definitions, theorems, and limits

### 2.1 Cook--Reckhow systems and the baseline implication

**KNOWN (Cook--Reckhow 1979).** A propositional proof system for a language \(L\) is a
polynomial-time computable onto map \(f:\Sigma^*\to L\); \(x\) is a proof of \(f(x)\). It is
polynomially bounded if every \(y\in L\) has a preimage of length polynomial in \(|y|\). For any
nonempty \(L\), a polynomially bounded proof system exists iff \(L\in\mathsf{NP}\). Therefore TAUT
has a polynomially bounded proof system iff \(\mathsf{NP}=\mathsf{coNP}\). All Frege systems are
p-equivalent, and all Extended Frege systems are p-equivalent (where p-simulation includes an
efficient proof translation).

- Model/uniformity: the verifier/map is uniform polynomial time; proof families themselves may be
  nonuniform witnesses.
- Technique: encode NP witnesses as proofs in one direction; use the proof string as an NP witness
  in the other.
- Limitation: a lower bound for one weak proof system does not imply \(\mathsf{NP}\ne\mathsf{coNP}\).
  One needs a lower bound against every proof system, or against a system known to be
  polynomially bounded if one exists.
- Source: [Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44
  (1979), author PDF](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf). The
  [author webpage](https://www.cs.toronto.edu/~sacook/homepage/recentpubs.html) records that
  Corollary 4.7 should read \(\mathsf{coNP}\ne\mathsf{NP}\), not \(\mathsf P\ne\mathsf{NP}\).

### 2.2 Resolution: length, width, and proof search

For an unsatisfiable CNF \(F\), Resolution derives clauses using
\[
  \frac{A\lor x\qquad B\lor\neg x}{A\lor B}
\]
(with weakening conventions varying slightly by paper) until the empty clause is obtained. Proof
size below means number of clauses/lines unless stated otherwise.

**KNOWN (Haken 1985).** The standard pigeonhole CNF \(\mathrm{PHP}^{n+1}_n\) requires
Resolution length \(2^{\Omega(n)}\), although Extended Resolution has polynomial-length proofs.

- Technique: bottleneck counting/random restrictions.
- Limit: the formula has \(\Theta(n^2)\) variables and \(\Theta(n^3)\) literal-scale encoding size;
  parameter conversions must be stated. This is a lower bound for Resolution, not Frege.
- Source: [Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI
  10.1016/0304-3975(85)90144-6](https://doi.org/10.1016/0304-3975(85)90144-6).

**KNOWN (Ben-Sasson--Wigderson 2001).** Let \(F\) be an unsatisfiable CNF over \(n\) variables,
let \(w_0\) be its maximum initial-clause width, and let \(W(F)\) be minimum refutation width. If
\(S(F)\) is minimum Resolution length, then
\[
  S(F) \ge \exp\!\left(\Omega\!\left((W(F)-w_0)^2/n\right)\right).
\]
Equivalently, a length-\(S\) refutation can be transformed into one of width
\(w_0+O(\sqrt{n\log S})\). Enumerating all bounded-width clauses gives an
\(n^{O(w)}\)-time proof-search procedure.

- Technique: random restrictions plus a progress measure reducing size to width.
- Dependencies: a formula-specific width lower bound; Atserias--Dalmau later characterized width
  by a pebble game.
- Limit: the square-root loss can make the generic search algorithm subexponential rather than
  polynomial even when a polynomial proof exists. Width lower bounds do not automatically extend
  to Frege or cutting planes.
- Source: [Ben-Sasson and Wigderson, *Short Proofs Are Narrow--Resolution Made Simple*, JACM
  48 (2001), author PDF](https://www.math.ias.edu/~avi/PUBLICATIONS/ABSTRACT/bw02.pdf),
  [DOI](https://doi.org/10.1145/375827.375835).

**KNOWN (Atserias--Müller 2020).** There is a polynomial-time reduction from 3-SAT to formulas
\(G(F)\) with a gap: in one case the shortest Resolution proof has polynomial length and in the
other it has length \(2^{r^{\Omega(1)}}\), where \(r=|G(F)|\). Consequently:

- polynomial-time automatizability of Resolution implies \(\mathsf P=\mathsf{NP}\);
- quasi-polynomial automatizability implies \(\mathsf{NP}\subseteq\mathsf{QP}\);
- subexponential automatizability implies \(\mathsf{NP}\subseteq\mathsf{SUBEXP}\).

Here automatizability means outputting a Resolution refutation in time polynomial (or the stated
time class) in the input size plus the shortest Resolution proof length.

- Technique: reflection-principle encodings and a length gap reduction.
- Limit: this is **strong** automatizability. It does not settle weak automatizability, in which the
  output may be a proof in a stronger system.
- Source: [Atserias and Müller, *Automating Resolution Is NP-Hard*, JACM 67 (2020), author
  PDF](https://www.cs.upc.edu/~atserias/papers/automating-resolution-np-hard/automating-resolution-np-hard.pdf),
  [arXiv:1904.02991](https://arxiv.org/abs/1904.02991).

### 2.3 Weak automatizability and feasible interpolation

**KNOWN (Atserias--Bonet 2004).** A proof system \(P\) is weakly automatizable if some system
\(Q\) simulating \(P\) has a proof-search algorithm polynomial in the input size and the shortest
\(P\)-proof size. For Resolution the following are equivalent:

1. Resolution is weakly automatizable.
2. \(\mathrm{Res}(k)\) is weakly automatizable (for each fixed \(k\ge2\)).
3. \(\mathrm{Res}(2)\) has feasible interpolation (and equivalent canonical-NP-pair separation
   formulations).

- Status: **OPEN** in the current sources; the 2020 NP-hardness of strong automatization does not
  close it.
- Source: [Atserias and Bonet, *On the Automatizability of Resolution and Related Propositional
  Proof Systems*, Information and Computation 189 (2004), author PDF](https://www.cs.upc.edu/~atserias/papers/autom/infocomp.pdf),
  [ECCC TR02-010](https://eccc.weizmann.ac.il/report/2002/010/).

**KNOWN (feasible interpolation).** Given an unsatisfiable conjunction
\(A(p,q)\wedge B(p,r)\), an interpolating proof system efficiently extracts a Boolean circuit
\(I(p)\) separating common-variable assignments extendible to the \(A\)-side from those
extendible to the \(B\)-side. Krajíček's proof gives circuit size polynomial/linear in the relevant
proof measure for systems such as Resolution, Cutting Planes, and suitable linear-equation
calculi; under a sign condition the interpolant is monotone. Clique--coloring contradictions plus
monotone circuit lower bounds then imply proof lower bounds.

- Technique: inductively attach a circuit gate to each proof line.
- Limit: feasible interpolation is a property to prove, not a generic property of strong systems.
  Cryptographic conditional results show Frege and \(\mathrm{TC}^0\)-Frege do not have feasible
  interpolation unless factoring Blum integers is easy; the same hypothesis yields their
  non-automatizability.
- Sources: [Krajíček, *Interpolation Theorems, Lower Bounds for Proof Systems, and Independence
  Results for Bounded Arithmetic*, JSL 62 (1997)](https://doi.org/10.2307/2275541);
  [Bonet, Pitassi, and Raz, *On Interpolation and Automatization for Frege Systems*, SICOMP 29
  (2000)](https://doi.org/10.1137/S0097539798353230).

### 2.4 Frege and bounded-depth Frege

**KNOWN / OPEN boundary.** Frege lines are arbitrary propositional formulas over a fixed complete
basis and finitely many sound, complete inference schemata. Extended Frege additionally permits
extension variables abbreviating formulas. Cook--Reckhow proves robustness under the choice of
basis/rules. As of this search:

- no superpolynomial proof-size lower bound is known for unrestricted Frege;
- no superpolynomial proof-size lower bound is known for Extended Frege;
- fixed-depth Frege has exponential lower bounds for explicit contradictions;
- superpolynomial lower bounds for \(\mathrm{AC}^0[p]\)-Frege remain open.

**KNOWN (bounded depth).** For every fixed proof depth \(d\), pigeonhole/Tseitin families require
size \(\exp(n^{\varepsilon_d})\) for some \(\varepsilon_d>0\) in depth-\(d\) Frege. The classical
PHP proof uses random restrictions/switching lemmas. It also implies a depth lower bound for
polynomial-size proofs; later expander switching lemmas improve this to
\(\Omega(\sqrt{\log n})\) depth for a linear-size 3-CNF Tseitin family.

- Model: proof depth counts formula depth of proof lines; \(d\) is fixed before \(n\to\infty\).
- Limit: \(\varepsilon_d\) deteriorates with \(d\); this does not approach unrestricted Frege.
- Sources: [Beame, Impagliazzo, Krajíček, Pitassi, Pudlák, and Woods, *Exponential Lower Bounds
  for the Pigeonhole Principle*, Computational Complexity 3 (1993), author PDF](https://homes.cs.washington.edu/~beame/papers/php.pdf),
  [DOI](https://doi.org/10.1007/BF01200117); [Pitassi, Rossman, Servedio, and Tan,
  *Poly-logarithmic Frege Depth Lower Bounds via an Expander Switching Lemma*, STOC
  2016](https://www.cs.columbia.edu/~rocco/papers/stoc16frege.html); [Håstad and Risse,
  bounded-depth Tseitin follow-up](https://doi.org/10.1016/j.apal.2022.103166).

**Negative status check.** The 2025 preprint on \(\mathrm{AC}^0[p]\)-Frege found in the search
constructs formulas with no polynomial proofs infinitely often while the tautology status of the
family is itself unresolved. It must not be cited as a lower bound for an explicit family of known
tautologies. Source: [arXiv:2509.16824](https://arxiv.org/abs/2509.16824).

### 2.5 Cutting Planes

Cutting Planes (CP) refutes an unsatisfiable system of integral linear inequalities over Boolean
variables. Lines are integer inequalities; rules include positive integral linear combination and
division with rounding. A refutation derives an impossible inequality such as \(0\ge1\).

**KNOWN.** General dag-like CP has exponential length lower bounds on explicit clique--coloring
families. The proof translates short CP proofs to small monotone real circuits/interpolants and
applies monotone lower bounds. CP with polynomially bounded coefficients (often denoted
\(\mathrm{CP}^*\)) also has exponential length lower bounds. Tree-like CP lower bounds follow
from communication complexity and have since been sharpened for concise pigeonhole formulas.

- Limitation: these are carefully engineered interpolation instances; they do not imply lower
  bounds for arbitrary integer programming or Frege. Coefficient size, line count, bit size, and
  blackboard space are different resources.
- Sources: [Cook, Coullard, and Turán, original CP proof system, Discrete Applied Mathematics 18
  (1987)](https://doi.org/10.1016/0166-218X(87)90039-4); [Pudlák, *Lower Bounds for Resolution
  and Cutting Plane Proofs and Monotone Computations*, JSL 62 (1997)](https://doi.org/10.2307/2275583);
  [Bonet, Pitassi, and Raz, *Lower Bounds for Cutting Planes Proofs with Small Coefficients*, JSL
  62 (1997)](https://doi.org/10.2307/2275569); [Impagliazzo, Pitassi, and Urquhart, tree-like CP,
  LICS 1994](https://doi.org/10.1109/LICS.1994.316056).

**KNOWN (space collapse with large coefficients).** Every unsatisfiable set of integral
inequalities has a CP refutation in inequality space at most 5. The construction may use
coefficients of exponential magnitude. For \(\mathrm{CP}_k\), defined in the cited paper by
requiring every coefficient in every line to have absolute value at most a fixed \(k\), the complete
tree contradiction \(\mathrm{CT}_n\) needs inequality space
\(\Omega(\log\log\log n)\). Already \(\mathrm{CP}_2\) simulates Resolution and has
space-5 proofs of PHP.

- Open in that paper: constant inequality space with polynomially bounded coefficients; stronger
  \(\mathrm{CP}_2\) inequality-space lower bounds; linear total-space bounds.
- Source: [Galesi, Pudlák, and Thapen, *The Space Complexity of Cutting Planes Refutations*,
  author PDF](https://users.math.cas.cz/~thapen/CP_constant_space.pdf).
- Follow-up check: the 2020 lifting separation gives a joint length/space separation between
  unbounded CP and polynomial-coefficient CP, but does not improve the fixed-\(k\) inequality-space
  lower bound. [Göös et al., arXiv:2001.02144](https://arxiv.org/abs/2001.02144).

**KNOWN (search hardness).** Automating CP is NP-hard. Tree-like CP has a conditional hardness
result under Gap-Hitting-Set assumptions. Source: [Göös, Koroth, Mertz, and Pitassi,
*Automating Cutting Planes Is NP-Hard*, arXiv:2004.08037](https://arxiv.org/abs/2004.08037).

### 2.6 Polynomial Calculus and Polynomial Calculus Resolution

Fix a field \(\mathbb F\). A clause is translated to a polynomial equation, Boolean axioms
\(x^2-x=0\) are available, and Polynomial Calculus (PC) derives linear combinations and variable
multiples until deriving \(1=0\). PCR adds a formal complementary variable for each literal.
Conventions matter: size can mean lines, monomials with repetition, or bit size; degree is maximum
total degree; monomial space is the maximum number of monomials simultaneously on the
blackboard.

**KNOWN (size--degree).** For an unsatisfiable \(k\)-CNF on \(n\) variables, a PCR refutation of
monomial size \(S\) can be transformed to degree
\[
  k+O(\sqrt{n\log S}).
\]
Hence a degree lower bound \(D\) gives
\(S\ge\exp(\Omega((D-k)^2/n))\). Degree at most \(d\) can be searched by linear algebra in
\(n^{O(d)}\) time.

- Technique: algebraic analogue of size--width plus linear-algebraic proof search.
- Limit: the field and Boolean encoding are part of the theorem. Degree lower bounds do not by
  themselves settle weak automatizability or space.
- Sources: [Clegg, Edmonds, and Impagliazzo, *Using the Groebner Basis Algorithm to Find
  Proofs of Unsatisfiability*, STOC 1996](https://doi.org/10.1145/237814.237860);
  [Impagliazzo, Pudlák, and Sgall, *Lower Bounds for the Polynomial Calculus and the Groebner
  Basis Algorithm*, Computational Complexity 8 (1999)](https://doi.org/10.1007/s000370050024).

**Negative status check.** A proposed target “prove a size--degree tradeoff for PC” is already
known, including tradeoffs applying to a single proof rather than merely to the minimum measures.
See [Galesi and Lauria, TOCT 2010](https://doi.org/10.1145/1838552.1838556) and [Lagarde et al.,
ITCS 2020](https://doi.org/10.4230/LIPIcs.ITCS.2020.72).

**KNOWN (space frontier, 2025 synthesis).** Filmus--Lauria--Mikša--Nordström--Vinyals prove,
over any field, that for a \(k\)-CNF \(F\) and a non-authoritarian constant-arity substitution
\(f\),
\[
  \operatorname{Sp}_{\mathrm{PCR}}(F[f])
    \ge (W_{\mathrm{Res}}(F)-k+1)/4.
\]
Consequences include linear PCR space for XOR-substituted Tseitin formulas (equivalently a
doubled-edge multigraph), even though they have tree-like PC refutations of size
\(O(n\log n)\) and degree \(O(1)\) over the matching characteristic. Without substitution,
subsequent width-to-space work gives \(\Omega(\sqrt n)\) on expander Tseitin, ordering, and FPHP
families. Austrin--Risse improve Tseitin to \(\Omega(n/\log n)\) only for sufficiently large
constant degree. For graphs of degree below 6, \(\Omega(\sqrt n)\) remains the best reported
bound; a 6-regular doubled-edge multigraph has \(\Omega(n)\).

- Open: eliminate the square-root loss; prove near-linear/linear space for simple low-degree
  expanders; characterize degree versus space; separate PCR space from Resolution space.
- Negative finding: the open random-3-CNF PCR-space problem in the conference version is closed;
  Bennett et al. obtain linear monomial space.
- Source: [Filmus, Lauria, Mikša, Nordström, and Vinyals, *Towards an Understanding of Polynomial
  Calculus: New Separations and Lower Bounds*, Theory of Computing 21 (2025), PDF](https://theoryofcomputing.org/articles/v021a004/v021a004.pdf).

**KNOWN (automation hardness).** It is NP-hard to automate Nullstellensatz, PC, and
Sherali--Adams, uniformly over the usual finite/real field variants and with/without twin
variables. More precisely, one reduction produces formulas with polynomial proofs in the yes
case and \(2^{n^{\Omega(1)}}\) proof size in the no case. Sum-of-Squares automatability is not
covered and was explicitly left open.

- Source: [de Rezende, Göös, Nordström, Pitassi, Robere, and Sokolov, *Automating Algebraic Proof
  Systems Is NP-Hard*, STOC 2021, author PDF](https://jakobnordstrom.se/docs/publications/AutomatingAlgebraic_STOC.pdf).

**KNOWN but non-transferable (Alekseev 2026).** Extended PC with a square-root rule over
\(\mathbb Q\), allowing extension variables for arbitrary-depth algebraic circuits, p-simulates
Extended Frege. Nevertheless the proved \(2^{\Omega(n)}\) bit-size lower bound is for the binary
value polynomial system
\(1+x_1+2x_2+\cdots+2^{n-1}x_n=0\), which has no polynomial-size CNF translation. The paper
explicitly notes that this does **not** imply a Frege or EF lower bound. It is also a bit-size lower
bound driven by integer divisibility, not a generic monomial/line lower bound.

- Source: [Alekseev, *A Lower Bound for Polynomial Calculus with Extension Rule*, Theory of
  Computing 22 (2026)](https://theoryofcomputing.org/articles/v022a004/index.html).

### 2.7 Bounded arithmetic links (safe formulation)

**KNOWN framework.** Paris--Wilkie translations turn bounded first-order formulas and proofs into
families of propositional formulas/proofs. The strength and uniformity depend on the exact theory,
formula class, and translation. Cook's equational theory PV has a close one-way simulation by
Extended Frege; fragments of Buss bounded arithmetic correspond to bounded-depth systems and
their reflection principles.

- Safe implication: an arithmetic proof in a fixed bounded theory normally yields a uniformly
  constructible family of short proofs in its associated propositional system.
- Unsafe inference: a proof lower bound for an arbitrary propositional family does not
  automatically give independence from a bounded arithmetic theory. One must show that the
  family is the correct translation and track uniformity/reflection.
- Source: [Buss, *Bounded Arithmetic and Propositional Proofs*, author notes](https://www.math.ucsd.edu/~sbuss/ResearchWeb/marktoberdorf95/paper.pdf);
  Cook--Reckhow's PDF above states the PV-to-EF simulation.

**KNOWN conditional barrier.** Razborov showed, under strong pseudorandom-generator hypotheses,
unprovability of certain circuit lower-bound statements in bounded arithmetic such as
\(S^2_2(\alpha)\), with weaker PRG assumptions for \(S^1_2(\alpha)\). This is a conditional
limitation on formalizing a class of arguments, not an unconditional circuit lower bound or an
oracle barrier. Source: [Razborov, *Unprovability of Lower Bounds on Circuit Size in Certain
Fragments of Bounded Arithmetic*, 1995](https://www.mathnet.ru/eng/im9).

### 2.8 Resolution and concrete SAT solving

**KNOWN correspondences.** DPLL without clause learning corresponds to tree-like Resolution
(with details depending on unit propagation and branching conventions). CDCL without
preprocessing outputs a Resolution refutation. Conversely, CDCL with restarts and suitable
learning/branching choices polynomially simulates general Resolution.

**KNOWN width simulation (Atserias--Fichte--Thurley).** If \(F\) on \(n\) variables has a
width-\(k\), length-\(m\) Resolution refutation, their randomized clause-learning algorithm with
restarts learns the empty clause with probability at least \(1/2\) after at most
\[
  4m\ln(4m)n^k
\]
conflicts/restarts. Eliminating \(m\) using the number of width-\(k\) clauses gives at most
\(8k\ln(8n)n^{2k}\). The proof uses clause absorption rather than literally learning every clause
in the given proof.

- Limitation: this is a deliberately randomized theoretical branching model and does not predict
  the runtime of every fixed production solver or heuristic.
- Source: [Atserias, Fichte, and Thurley, *Clause-Learning Algorithms with Many Restarts and
  Bounded-Width Resolution*, JAI 2011, author PDF](https://www.cs.upc.edu/~atserias/papers/clauselearning/aft_sat_paper.pdf).

**KNOWN learning-scheme overhead.** Resolution with Merge Ancestors (RMA) contains proofs
generated by standard 1-empowering/asserting learning schemes. RMA simulates Resolution with at
most linear multiplicative overhead, and there are formula families with linear Resolution proofs
but quadratic RMA proofs. Thus “CDCL is Resolution” is only a polynomial-equivalence slogan; the
precise learning model matters.

- Source: [Vinyals, Li, Fleming, Kolokolova, and Ganesh, *Limits of CDCL Learning via Merge
  Resolution*, arXiv:2304.09422](https://arxiv.org/abs/2304.09422).
- Remaining explicit question: restart-free 1-UIP CDCL versus general Resolution is still listed as
  open in the [Handbook of Satisfiability proof-complexity chapter](https://mathweb.ucsd.edu/~sbuss/ResearchWeb/ProofComplexitySAT/FinalGalleys.pdf).

## 3. Exact and exponential SAT algorithms

Throughout, \(O^*(\cdot)\) suppresses polynomial factors. Bounds are in the number \(n\) of
variables unless explicitly parameterized otherwise.

### 3.1 Local search, covering codes, and PPSZ

**KNOWN (Schöning).** Randomized local search for satisfiable \(k\)-CNF succeeds in expected
time
\[
  O^*\!\left(\left(2\frac{k-1}{k}\right)^n\right)
  =O^*((2-2/k)^n).
\]
For \(k=3\) this is \(O^*((4/3)^n)\). A random start lies close to a fixed satisfying assignment
with sufficient probability, and an unsatisfied-clause random walk has positive drift toward it.

- Derandomization: for every fixed \(k\) and \(\varepsilon>0\), Moser--Scheder give deterministic
  \(O^*((2(k-1)/k+\varepsilon)^n)\) via covering codes.
- Sources: [Schöning, *A Probabilistic Algorithm for k-SAT Based on Limited Local Search*,
  Algorithmica 32 (2002), author copy](https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/schoning2002.pdf);
  [Moser and Scheder, *A Full Derandomization of Schöning's k-SAT Algorithm*,
  arXiv:1008.4067](https://arxiv.org/abs/1008.4067).

**KNOWN (deterministic benchmark).** Liu combines branching with generalized covering codes over
“chains” of overlapping clauses. For 3-SAT the proved bound is
\[
  O(1.32793^n).
\]
For general fixed \(k\), the paper gives an explicit recurrence improving the prior deterministic
\((2-2/k)^{n+o(n)}\) benchmark.

- Source: [Liu, *Chain, Generalization of Covering Code, and Deterministic Algorithm for k-SAT*,
  ICALP 2018](https://doi.org/10.4230/LIPIcs.ICALP.2018.88).
- Current-status caveat: targeted 2024--2026 searches found no smaller published deterministic
  general-3-SAT base, but “current best” is vulnerable to terminology (3-SAT vs unique-3-SAT,
  randomized vs deterministic, variables vs clauses, polynomial vs exponential space).

**KNOWN (PPSZ framework).** PPSZ first closes under bounded-width Resolution, samples a random
variable ordering, assigns forced variables by unit implications, and guesses the rest. Its
success probability is controlled by the number of forced variables. The classical unique-3-SAT
exponent is \(2\ln2-1\approx0.38629\), giving a base near 1.307.

- Original source: [Paturi, Pudlák, Saks, and Zane, *An Improved Exponential-Time Algorithm for
  k-SAT*, JACM 52 (2005), author PDF](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/PaturiPudlakSaksZane_2005_jacm.pdf).
- Unique-to-general progress: [Hertli, *3-SAT Faster and Simpler--Unique-SAT Bounds for PPSZ Hold
  in General*, arXiv:1103.2165](https://arxiv.org/abs/1103.2165).
- Later analysis: [Scheder, *PPSZ Is Better Than You Think*, arXiv:2207.11071](https://arxiv.org/abs/2207.11071).

**RECENT PREPRINT, not yet treated as settled benchmark.** Jiang--Cai (July 2026) keep PPSZ and
the Scheder--Steinberger unique-to-general lift unchanged and replace the final recombination by an
exact rational LP dual certificate. They claim
\[
 \begin{array}{c|c}
 \text{problem}&\text{randomized time}\ \\ \hline
 \text{Unique-3-SAT}&O^*(1.306969598^n)\\
 \text{general 3-SAT}&O^*(1.307031578^n).
 \end{array}
\]
Source: [Jiang and Cai, *A Better Analysis for PPSZ for 3-SAT*,
arXiv:2607.10697](https://arxiv.org/abs/2607.10697). The exact-rational certificate makes this
unusually amenable to independent machine checking, but peer review and independent replication
were not located.

### 3.2 ETH, SETH, and sparsification: what the exponential bases do not prove

Let \(s_k\) be the infimum exponent \(c\) such that \(k\)-SAT is solvable in
\(2^{cn}\operatorname{poly}(|F|)\).

- **ETH** asserts \(s_3>0\) (equivalently, fixed-width SAT has no subexponential algorithm after
  sparsification).
- **SETH** asserts \(\lim_{k\to\infty}s_k=1\), equivalently: for every \(\varepsilon>0\) there is a
  \(k\) for which \(k\)-SAT has no \(2^{(1-\varepsilon)n}\) algorithm.

These are conjectures, not unconditional lower bounds.

**KNOWN (sparsification lemma).** For each fixed \(k\) and \(\varepsilon>0\), every \(n\)-variable
\(k\)-CNF is a disjunction of at most \(2^{\varepsilon n}\) \(k\)-CNFs in which each variable has
at most \(C(k,\varepsilon)\) occurrences; the decomposition is computable in
\(O^*(2^{\varepsilon n})\) time. This is why clause density can often be normalized in fine-grained
reductions, but \(C(k,\varepsilon)\) is not harmless when exact constants matter.

- Sources: [Impagliazzo and Paturi, *On the Complexity of k-SAT*, JCSS 62 (2001)](https://doi.org/10.1006/jcss.2000.1727);
  [Impagliazzo, Paturi, and Zane, *Which Problems Have Strongly Exponential Complexity?*, JCSS 63
  (2001), author PDF](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiZane_1998_focs.pdf).

### 3.3 Restricted circuit SAT and the algorithm-to-lower-bound bridge

**KNOWN (Williams 2010/2013).** Suppose there is a superpolynomial function \(s(n)\) such that,
for **every fixed** \(k\), Circuit-SAT on \(n\)-input circuits with \(n^k\) gates is solvable by a
(co-)nondeterministic algorithm in
\[
  2^n\operatorname{poly}(n^k)/s(n).
\]
Then \(\mathsf{NEXP}\not\subseteq\mathsf{P/poly}\). A constant-factor exponential saving
\(O(2^{(1-\delta)n}\operatorname{poly}(m))\) yields a language in \(\mathsf E^{\mathsf{NP}}\)
requiring \(2^{\varepsilon n}\)-size circuits for some \(\varepsilon>0\).

- Technique: assume small circuits, use succinct witnesses/local checkability to turn a faster SAT
  algorithm into a nondeterministic time-hierarchy contradiction.
- Quantifier warning: an algorithm for one size exponent \(k\), or for only \(k\)-CNF, is not the
  premise. The saving must dominate polynomial overhead for all fixed polynomial circuit sizes.
- Uniformity warning: the SAT algorithm is uniform; the contradicted circuit upper bound is
  nonuniform.
- Source: [Williams, *Improving Exhaustive Search Implies Superpolynomial Lower Bounds*, SICOMP
  42 (2013), author PDF](https://www.cs.cmu.edu/~ryanw/improved-algs-lbs2.pdf).

**KNOWN (ACC instantiation).** ACC consists of constant-depth, unbounded-fan-in
AND/OR/NOT/MOD\(_m\) circuits for fixed \(m>1\). Williams gives a faster ACC-SAT algorithm and
deduces
\[
  \mathsf{NTIME}[2^n]\not\subseteq\text{nonuniform polynomial-size ACC}.
\]
For every fixed depth \(d\) and modulus \(m\), some language in \(\mathsf E^{\mathsf{NP}}\)
requires ACC size \(2^{n^{\delta(d,m)}}\). The algorithm uses structural polynomial/symmetric
representations, fast matrix multiplication, and split-and-list evaluation.

- Source: [Williams, *Non-Uniform ACC Circuit Lower Bounds*, CCC 2011/JACM 2014, author
  PDF](https://people.csail.mit.edu/rrw/acc-lbs-ccc.pdf).

**KNOWN extension.** For \(\mathrm{ACC}\circ\mathrm{THR}\), \#SAT for subexponential-size
circuits is computable in \(2^{n-n^\varepsilon}\), yielding NEXP lower bounds against
quasi-polynomial-size \(\mathrm{ACC}\circ\mathrm{THR}\) and
\(\mathrm{ACC}\circ\mathrm{SYM}\). The same paper evaluates all assignments of
\(\mathrm{THR}\circ\mathrm{THR}\) circuits with up to \(2^{n/24}\) gates in
\(2^n\operatorname{poly}(n)\), but this all-input evaluation gives no SAT saving.

- Important closure caveat: the paper explicitly notes that a large OR of
  \(\mathrm{THR}\circ\mathrm{THR}\) circuits is not known to remain in the class. Therefore the
  clean restricted-class Williams implication cannot be quoted without checking closure.
- Source: [Williams, *New Algorithms and Lower Bounds for Circuits with Linear Threshold Gates*,
  Theory of Computing 14 (2018)](https://theoryofcomputing.org/articles/v014a017/).

### 3.4 Threshold-circuit SAT frontier

**KNOWN.** For depth-two threshold circuits with \(cn\) wires, Impagliazzo--Paturi--Schneider
give randomized time \(2^{(1-s)n}\) with \(s=c^{-O(c^2)}\). Chen--Santhanam improve the
dependence to \(c^{-O(c)}\). For each fixed depth \(d>1\), Chen--Santhanam--Srinivasan give a
randomized algorithm beating brute force for circuits with \(n^{1+\varepsilon_d}\) wires,
\(\varepsilon_d=2^{-O(d)}\), together with average-case lower bounds.

- Sources: [Impagliazzo, Paturi, and Schneider, *A Satisfiability Algorithm for Sparse Depth Two
  Threshold Circuits*, arXiv:1212.4548](https://arxiv.org/abs/1212.4548);
  [Chen and Santhanam, *Improved Algorithms for Sparse MAX-SAT and MAX-k-CSP*, ECCC
  TR15-112](https://eccc.weizmann.ac.il/report/2015/112/);
  [Chen, Santhanam, and Srinivasan, *Average-Case Lower Bounds and Satisfiability Algorithms for
  Small Threshold Circuits*, Theory of Computing 14 (2018)](https://www.theoryofcomputing.org/articles/v014a009/).

**KNOWN (near-quadratic gate frontier).** Tamaki gives deterministic \#SAT for a depth-two circuit
of \(m\) SYM/THR gates on \(n\) variables in
\[
  2^{,n-\Omega((n/(\sqrt m\,\operatorname{polylog}n))^a)}
\]
for an absolute constant \(a>0\). This is superpolynomially faster than exhaustive search when
\(m=O(n^2/\log^b n)\) for a sufficiently large constant \(b\). The search found no result crossing
the genuinely quadratic-gate boundary, and a 2026 ECCC frontier description still calls
subquadratic the best regime.

- Source: [Tamaki, *A Satisfiability Algorithm for Depth Two Circuits with a Sub-Quadratic Number
  of Symmetric and Threshold Gates*, ECCC TR16-100](https://eccc.weizmann.ac.il/report/2016/100/).
- Related but not a closure of this target: [Alman, Chan, and Williams, *Polynomial
  Representations of Threshold Functions and Algorithmic Applications*,
  arXiv:1608.04355](https://arxiv.org/abs/1608.04355) handles richer compositions with a
  subquadratic bottom layer.

## 4. Independent audit: Alekseev--Gaevoy Conjecture 1.4 / 4.2

### 4.1 Exact statement and claimed consequence

Let logs be base 2, as in the paper. The paper states the following.

**CONJECTURED in TR26-007.** For fixed constants \(r,q>0\), let
\(\Phi_1,\ldots,\Phi_m\subseteq\mathbb F_2^n\) be affine subspaces of codimension at most
\((\log n)^q\), with
\[
 \left|\bigcup_{j=1}^m\Phi_j\right|\ge2^{n-1}.
\]
For arbitrary subsets \(\Phi'_j\subseteq\Phi_j\) satisfying
\[
 |\Phi'_j|\ge(1-n^{-r})|\Phi_j|\quad\text{for every }j,
\]
there should exist a constant \(c(q)>0\), depending only on \(q\), such that
\[
 \left|\bigcup_j\Phi'_j\right|
 \ge (1-n^{-r c(q)})\left|\bigcup_j\Phi_j\right|.
\]
The quantification over \(m\) and the affine subspaces is unrestricted; the retained subsets are
arbitrary. Section 4 confirms this interpretation: sets of nice assignments are partitioned into
affine solution spaces \(\Phi_j^\rho\), and the retained sets \(\Psi_j^\rho\) are not asserted to be
affine.

**Conditional consequence (Theorem 1.1 / 4.3).** If the conjecture holds for \(q>1\) and
\(r=k-2\), a \(\mathrm{Res}(\oplus)\) refutation of the constrained bit pigeonhole formula
\(\mathrm{CBPHP}^{N,M}_{k,f}\) of size at most
\(2^{(\log N)^{q/2}}\) has depth at least \(\Omega(N^{(k-2)c})\), where \(c>0\) depends only on
\(q\). The more detailed theorem gives
\[
 d\ge\Omega\!\left(
   \left(\frac{N^{k-1-\varepsilon}}
   {(\log N)^{2kq+O(1)}}\right)^c
 \right).
\]
Choosing \(q=3\) would make the excluded proof size
\(2^{(\log N)^{3/2}}\), which is superpolynomial. If the premise held for all fixed
\(r=k-2\), then choosing \(k\) as a function of a desired fixed depth exponent would give
superpolynomial lower bounds for any fixed polynomial proof depth.

- Source: [Alekseev and Gaevoy, *New Polynomial-Depth Res(+) Lower Bounds*, ECCC
  TR26-007](https://eccc.weizmann.ac.il/report/2026/007/).

### 4.2 Coordinate-flat counterexample

**Status: FALSE-AS-WRITTEN (proof candidate; elementary internal check, not external review).**

Fix any \(q>1\), any fixed \(r>0\), and sufficiently large \(n\). Put
\[
 L=\lfloor(\log_2 n)^q\rfloor,
\]
so that \(2L\le n\). For every \(L\)-element subset \(S\subseteq[2L]\), define the coordinate
affine subspace
\[
 A_S=\{x\in\mathbb F_2^n:x_i=0\text{ for all }i\in S\}.
\]
Then \(\operatorname{codim}(A_S)=L\le(\log n)^q\). Its union is
\[
 U=\bigcup_{|S|=L}A_S
   =\{x:\text{at least }L\text{ of the first }2L\text{ coordinates are zero}\}.
\]
By symmetry of the binomial distribution,
\[
 |U|=2^{n-2L}\frac{4^L+\binom{2L}{L}}2\ge2^{n-1}.
\]

For each \(S\), let
\[
 D_S=\{x:\{i\in[2L]:x_i=0\}=S\},\qquad A'_S=A_S\setminus D_S.
\]
The last \(n-2L\) coordinates are free, so
\[
 |D_S|=2^{n-2L},\qquad |A_S|=2^{n-L},\qquad
 \frac{|D_S|}{|A_S|}=2^{-L}.
\]
Since \(q>1\), \(2^{-L}\le n^{-r}\) for every fixed \(r\) and all sufficiently large \(n\).
Thus every deletion obeys the conjecture's local budget.

Each point of \(D_S\) belongs to no \(A_T\) with \(T\ne S\): an \(L\)-set \(T\) is contained in
its zero coordinates \(S\) iff \(T=S\). Hence all these points disappear from the retained union,
while every point with more than \(L\) zero coordinates remains. Therefore
\[
 U\setminus\bigcup_{|S|=L}A'_S
   =D:=\bigcup_{|S|=L}D_S
\]
and
\[
 \frac{|D|}{|U|}
 =\frac{2\binom{2L}{L}}{4^L+\binom{2L}{L}}
 =\Theta(L^{-1/2})
 =\Theta((\log n)^{-q/2}),
\]
using the central-binomial-coefficient estimate
\(\binom{2L}{L}=\Theta(4^L/\sqrt L)\). This is larger than
\(n^{-r c}\) for every constant \(c>0\). No proposed \(c(q)>0\) can satisfy the conclusion.

This construction also falsifies the \(q=1,r=1\) instance (take
\(L=\lfloor\log_2 n\rfloor\), up to harmless rounding). For \(q>1\), it works for **all** fixed
\(r\). Thus “prove \(q=3\) for all fixed \(r\)” is not an open target; it is false as written.

### 4.3 Finite sanity check

With no unused coordinates and \(L=3\), there are \(\binom63=20\) flats in \(\mathbb F_2^6\).
Each flat has 8 points and loses one private point (fraction \(1/8\)). The original union has 42
points; the retained union has 22; 20 points, or \(20/42\), are lost. Direct enumeration for
\(L=1,\ldots,8\) gave:

| \(L\) | \(|U|\) in \(\mathbb F_2^{2L}\) | lost \(|D|\) | lost fraction | per-flat deletion |
|---:|---:|---:|---:|---:|
| 1 | 3 | 2 | 0.6667 | 0.5 |
| 2 | 11 | 6 | 0.5455 | 0.25 |
| 3 | 42 | 20 | 0.4762 | 0.125 |
| 4 | 163 | 70 | 0.4294 | 0.0625 |
| 6 | 2510 | 924 | 0.3681 | 0.015625 |
| 8 | 39203 | 12870 | 0.3283 | 0.00390625 |

The finite computation is only a check; the displayed counting proof is the asymptotic argument.

### 4.4 Exact form of the sets trimmed in the Res\((\oplus)\) application

This is the application-specific structure that the unrestricted conjecture throws away.  Put
\(b=\log_2 M\) and identify a full assignment
\(\gamma\in\mathbb F_2^{N b}\) with \((\gamma_1,\ldots,\gamma_N)\in[M]^N\).  For a pigeon set
\(P\subseteq[N]\), define the common collision-free predicate
\[
 \operatorname{Good}_f(P)=\left\{\gamma:
 \begin{array}{l}
  \gamma_p\ne\gamma_{p'}\text{ for all distinct }p,p'\in P,\\
  f(\gamma_{p_1},\ldots,\gamma_{p_k})\ne\gamma_{p_{k+1}}
  \text{ for all distinct }p_1,\ldots,p_{k+1}\in P
 \end{array}\right\}.
\]
The fixed function \(f:[M]^k\to[M]\) is chosen so that \(\mathrm{CBPHP}_{k,f}^{N,M}\) is
unsatisfiable and its symmetrized graph has the fibre bound
\[
 \bigl|\{y:(h_1,\ldots,h_k,y)\in\operatorname{Sym}_f\}\bigr|
 \le (\log M)^k
\]
for every fixed \(h_1,\ldots,h_k\).  Only this second property is used in the local trimming
estimate.

For a layer system \(L_j\), let \(C_j=\operatorname{Cl}(L_j)\), where closure is defined from
the *linear parts* of the equations.  In the paper's terminology,
\[
 \Phi_j=\operatorname{Sol}(L_j)\cap\operatorname{Good}_f(C_j)
\]
is its set of nice full assignments.  For every collision-free bit assignment \(\rho\) to **all
bits in all blocks in \(C_j\)** for which the cell is nonempty,
\[
 \boxed{\quad
 \Phi_j^\rho
   =\operatorname{Sol}(L_j)\cap\{\gamma:\gamma|_{C_j}=\rho\}.
 \quad}                                                     \tag{4.1}
\]
The cells in (4.1) are disjoint and their union is \(\Phi_j\).  Each is affine; after conditioning
on \(\rho\), the residual system is safe.

Suppose \(L_j\) is split between consecutive layers by querying the affine form \(\ell_j\).  Its
two children are
\(L_{j,0}=L_j\cup\{\ell_j=0\}\) and
\(L_{j,1}=L_j\cup\{\ell_j=1\}\).  Since closure depends only on linear parts,
\[
 P_j:=\operatorname{Cl}(L_{j,0})=
      \operatorname{Cl}(L_{j,1}).
\]
The union of the assignments that remain nice in the two children is therefore obtained by the
following *exact structured deletion* in each cell:
\[
 \boxed{\quad
 \Psi_j^\rho=\Phi_j^\rho\cap\operatorname{Good}_f(P_j).
 \quad}                                                     \tag{4.2}
\]
Indeed, each \(\gamma\in\Phi_j^\rho\) satisfies exactly the child selected by
\(\beta=\ell_j(\gamma)\), and it is nice there exactly when it is collision-free on the common
closure \(P_j\).  If \(L_j\) is not split on that layer, the paper sets
\(\Psi_j^\rho=\Phi_j^\rho\).

There is a typographical/type ambiguity in the primary source that should not be silently copied:
Section 4.3 literally describes \(\Psi_j^\rho\) as assignments having no collisions “on
\(L_j\cup\{\ell_j=\beta\}\).”  Collisions were defined on sets of pigeons, not on equation
systems, and \(\beta\) is not quantified there.  Equations (4.1)--(4.2) are the interpretation
forced by Definition 4.5, Lemma 4.6, and the explicit split analysis in Section 4.2.  The equality
of the two closures also makes the value of \(\beta\) immaterial.

The relevant structural facts are as follows.  A set of independent linear forms is dangerous
when it has more forms than blocks in its support; a system is safe when its span contains no
dangerous set.  The closure \(\operatorname{Cl}(L)\) is the unique inclusion-minimal block set
whose zero-restriction makes the linear part safe.  The cited closure lemmas give
\[
 |\operatorname{Cl}(L)|\le\operatorname{rk}(L),\qquad
 |P_j|\le\operatorname{rk}(L_{j,\beta})\le\operatorname{rk}(L_j)+1.
\]
Conditioned on \(\rho\), safety supplies distinct pivot blocks and at most one pivot bit per such
block.  All nonpivot bits are independent uniform bits; before setting a pivot, each new block has
two possible \([M]\)-values.  The fibre bound for \(\operatorname{Sym}_f\), followed by a union
bound over equality and \((k+1)\)-ary collisions, is exactly what proves Lemma 4.6.  With
\(W_j\ge\max\{\operatorname{rk}(L_j),|P_j|\}\) (one may safely take
\(W_j=\operatorname{rk}(L_j)+1\)), it yields cell by cell
\[
 |\Psi_j^\rho|\ge |\Phi_j^\rho|
 \left(1-\frac{(3W_j)^{k+1}(\log N)^{O(1)}}{N^{k-1-\varepsilon}}\right).       \tag{4.3}
\]
The paper writes \(W_j=\operatorname{rk}(L_j)\) in one application even though adding the query
can increase rank by one; replacing it by \(\operatorname{rk}(L_j)+1\) is an asymptotically
harmless correction.

Thus the weakest literal extra hypothesis supplied by the application is **not** an overlap or
independence property.  It is this:

> Every deletion is the intersection with the same global, hereditary, blockwise
> collision-free predicate, evaluated on a small closure \(P_j\) obtained from the old closure by
> one affine query: \(\Phi'_i=\Phi_i\cap\operatorname{Good}_f(P_i)\).

Moreover, each affine cell comes from a collision-free closure fixing of a system whose residual
part is safe, and \(f\) has the displayed bounded-fibre property.  The application does **not**
supply bounded overlap between different cells, independence of their bad events, a bound on the
number of closure fixings, or a lower bound on point multiplicity.  None of those may be inserted
into a repaired lemma without a separate proof.

### 4.5 Two further parameter gaps in the printed application

**Status of this subsection: ERRORS/GAPS IN THE PRINTED ARGUMENT, with plausible
reparameterizations; not claimed here as counterexamples to the coarser conditional theorem.**
The false-as-written Conjecture 4.2 is a separate issue.  If one replaces it by a true structured
lemma, the following bookkeeping still has to be repaired explicitly.

**Cell codimension.**  Section 4.3 asserts that the cells \(\Phi_j^\rho\) have codimension at
most \(\operatorname{rk}(L_j)\) in \(\mathbb F_2^{N\log M}\).  On the literal definition (4.1),
this is false: fixing \(\rho\) fixes every bit of every closure block.  The valid elementary bound
is
\[
 \operatorname{codim}(\Phi_j^\rho)
 \le \operatorname{rk}(L_j)+|C_j|\log M
 \le (1+\log M)\operatorname{rk}(L_j).                       \tag{4.4}
\]
For a concrete witness, take a block of length \(b>2\) and the two independent equations
\(x_{1,1}=0,x_{1,2}=0\).  Their closure is the first block.  A consistent \(\rho\)-cell fixes that
whole block and has codimension \(b\), whereas the system has rank two.  No quotient-ambient
version of Conjecture 4.2 is stated in the paper.

For \(q=3\), \(S\le2^{(\log N)^{3/2}}\), and the paper's low-rank cutoff
\((\log S+\log N)^2\), (4.4) gives codimension \(O((\log N)^4)\), not
\(O((\log N)^3)\).  A generic-conjecture argument would therefore at least need a shifted
codimension parameter (for example, a \(q=4\) premise in this case).  A direct structured lemma
for (4.1)--(4.2) avoids this bookkeeping error.  Hence the invocation with the *same* \(q\) is not
validated by the printed proof; this observation alone does not rule out a repaired conditional
depth lower bound with shifted parameters.

**Error parameter.**  The actual local deletion fraction used in Section 4.3 is
\[
 \delta_N=\frac{(\log N)^{2kq+O(1)}}{N^{k-1-\varepsilon}}.
\]
Conjecture 4.2 instantiated only at \(r=k-2\) yields a global loss bounded by
\((N\log M)^{-(k-2)c(q)}\), because \(\delta_N\le(N\log M)^{-(k-2)}\) for suitable fixed
\(\varepsilon<1\) and large \(N\).  It does not literally yield the stronger
\(\delta_N^{c(q)}\) displayed in Theorem 4.3.  That stronger display would require the conjecture
at a larger fixed \(r<k-1-\varepsilon\) (and then an arbitrarily small exponent slack), or a
version parameterized directly by \(\delta\).  The coarser \(r=k-2\) conclusion is the exponent
used in Theorem 1.1, so this quantifier mismatch does not by itself refute that coarser
consequence; it shows that the displayed stronger Theorem 4.3 step is not justified by its stated
single-\(r\) hypothesis.

There is also a minor threshold mismatch: after high-rank systems are discarded, the remaining
union is shown to have density \(1/2-o(1)\), not necessarily at least exactly \(1/2\), while the
conjecture assumes the latter.  A selector-bit padding argument can repair a constant-density
threshold in a reformulation, but the printed proof does not state it.

### 4.6 Prior-equivalence and follow-up search

Searches for the exact conjecture number/title, “per-subspace deletion,” affine-union robustness,
subspace-covering multiplicity, robust sunflowers, and coordinate-subcube/private-point
formulations found:

- no 2026 paper proving or explicitly refuting Conjecture 1.4/4.2;
- TR26-018 cites TR26-007 for its unconditional bounded-depth results, not for a proof of the
  conjecture;
- adjacent literature on robust sunflowers and Boolean-cube affine covers, but no exact statement
  that needs to be invoked for the construction above.

The counterexample is essentially the middle layer of the Boolean lattice expressed as private
points of coordinate flats. It does not need a finite-geometry incidence theorem.

### 4.7 What could be repaired

The unrestricted conjecture cannot be a research target. Potentially meaningful replacements are:

1. Prove the layer-preservation inequality only for the **structured** affine solution spaces and
   collision-deletion sets \((\Phi_j^\rho,\Psi_j^\rho)\) in (4.1)--(4.2). The coordinate
   construction shows that affine geometry plus a local density bound is insufficient; the
   one-query closure, safe residual system, shared collision predicate, and bounded fibres of
   \(\operatorname{Sym}_f\) must do real work.
2. Add a bound on the number/overlap multiplicity of flats. A trivial incidence union bound already
   works when \(m\) is small relative to \(n^r\), so the useful regime must be stated carefully.
3. Study fixed codimension (or \((\log n)^q\) with \(q<1\)). This avoids the middle-layer
   counterexample's tiny private cells, but by itself would not supply Theorem 1.1, whose proof
   needs codimension about a power of \(\log n\) with exponent above one.

A fixed-constant-codimension theorem could be mathematically clean, but it has weak immediate
proof-complexity consequence.  The following is a conservative statement actually sufficient for
the first nontrivial application, rather than an attractive extra regularity assumption.

**STRUCTURED ONE-QUERY ROBUSTNESS, \(k=3\) (candidate; open/not novelty-audited/may be
false).** Fix \(0<\varepsilon<1\), take a power of two
\(M=N^{2-\varepsilon}\) (or the paper's rounded version), and fix an \(f:[M]^3\to[M]\) having
the two Section 3.1 properties.  Let
\[
 S\le2^{(\log N)^{3/2}},\qquad R=(\log S+\log N)^2,qquad W=R+1,qquad
 \alpha_N=\frac{2(3W)^4(\log M)^3}{M}.
\]
At one parity-decision-DAG layer, take at most \(S\) affine systems \(L_j\) of rank at most \(R\).
For every collision-free full assignment \(\rho\) on \(C_j=\operatorname{Cl}(L_j)\), include the
nonempty cell \(\Phi_j^\rho\) from (4.1).  If \(L_j\) is split by its one query \(\ell_j\), set
\(P_j=\operatorname{Cl}(L_j\cup\{\ell_j=0\})) and trim by (4.2); if it is not split, leave its
cells unchanged.  Write
\[
 U=\bigcup_{j,\rho}\Phi_j^\rho,qquad
 U'=\bigcup_{j,\rho}\Psi_j^\rho.
\]
Prove that some constant \(c>0\), independent of \(N,S\), satisfies
\[
 |U|\ge M^N/3\quad\Longrightarrow\quad
 |U'|\ge(1-\alpha_N^c)|U|.                                  \tag{4.5}
\]
The factor in \(\alpha_N\) is a conservative explicit specialization of Lemma 4.6; changing a
universal constant would not change the target.  The \(1/3\) density allows the separately bounded
high-rank contribution to be removed from a layer that initially has density at least \(1/2\).
Together with that high-rank accounting, (4.5) is the one-step estimate needed for the \(k=3\),
\(S\le2^{(\log N)^{3/2}}\) Res\((\oplus)\) application.  It deliberately assumes no overlap,
multiplicity, or probabilistic independence not furnished by the DAG.

Before proof work, (4.5) should be attacked by trying to realize a private-middle-layer
construction using the shared predicates \(\operatorname{Good}_f(P_j)\).  Proving (4.5) only for
some additionally regular family would be interesting, but would not be sufficient until that
regularity is derived for every relevant proof layer.

## 5. Dependency graph for this track

The arrows mean “is a stated prerequisite/input to,” not logical equivalence unless marked.

```text
[KNOWN] Cook--Reckhow verifier definition
    -> [KNOWN] polynomially bounded TAUT system <=> NP=coNP
    -> [OPEN] lower bounds for successively stronger concrete systems

[KNOWN] formula-specific Resolution width lower bound
    -> [KNOWN] Ben-Sasson--Wigderson size lower bound
    -> [KNOWN] n^{O(width)} proof search / theoretical CDCL width simulation

[KNOWN] short proof + feasible interpolation
    -> [KNOWN] small (monotone, when signed) interpolant circuit
    -> [KNOWN] monotone circuit lower bound
    -> [KNOWN] proof lower bound for Resolution/CP instances

[OPEN] Res(2) feasible interpolation
    <=> [OPEN] weak automatizability of Resolution
    -- distinct from --> [KNOWN FALSE unless P=NP] strong automatizability of Resolution

[KNOWN] fixed-depth switching/restriction arguments
    -> [KNOWN] exponential bounded-depth Frege lower bounds
    -/-> [OPEN] AC0[p]-Frege lower bounds
    -/-> [OPEN] unrestricted Frege lower bounds

[KNOWN] bounded CP coefficients
    -> [KNOWN] CT_n needs Omega(log log log n) inequality space
[KNOWN] unbounded CP coefficients
    -> [KNOWN] universal inequality-space-5 refutation

[KNOWN] PC/PCR degree lower bound
    -> [KNOWN] exponential monomial-size lower bound
    -> [KNOWN] n^{O(degree)} degree search
[KNOWN] Resolution width + XOR substitution
    -> [KNOWN] PCR monomial-space lower bound
    -> [OPEN] remove substitution/square-root loss on low-degree expanders

[KNOWN] Resolution proof
    -> [KNOWN] CDCL-with-restarts simulation (model dependent)
    -> [OPEN] restart-free 1-UIP simulation/separation

[KNOWN] Schoning / PPSZ structural success analysis
    -> [OPEN] improve exact 3-SAT exponent or derandomize PPSZ
    -/-> polynomial-time SAT

[KNOWN] uniform nontrivial C-SAT for all polynomial sizes
    + [REQUIRED] closure/constructibility of C
    -> [KNOWN] nonuniform C-circuit lower bound via time hierarchy

[CONJECTURED] Alekseev--Gaevoy arbitrary affine-union robustness
    -> [CLAIMED CONDITIONAL; APPLICATION GAPS RECORDED] polynomial-depth Res(oplus) size lower bound
[FALSE-AS-WRITTEN proof candidate] coordinate middle-layer construction
    -| blocks the conjectured premise
    -> [OPEN] structured CBPHP collision-set robustness repair
```

## 6. Concrete unresolved intermediate targets

The scores are deliberately coarse integers 1--5. Product is
**novelty potential × tractability × connection × falsifiability × formalizability**. “Novelty”
means room for a genuinely new result after the searches below, not a claim of novelty.

| Rank | ID | Precise first increment | N | T | C | F | V | Product |
|---:|---|---|---:|---:|---:|---:|---:|---:|
| 1 | PS-1 | Improve \(\mathrm{CP}_2\) inequality-space for \(\mathrm{CT}_n\) from \(\Omega(\log\log\log n)\) to any \(\omega(\log\log\log n)\) bound | 4 | 4 | 3 | 5 | 4 | 960 |
| 2 | PS-2 | Remove the size parameter from the Buss--Yolcu transformation: strict effective simulation of Resolution by regular Resolution | 4 | 4 | 3 | 5 | 4 | 960 |
| 3 | PS-3 | For Tseitin on one explicit family of simple 3- or 4-regular expanders, improve PCR monomial space from \(\Omega(\sqrt n)\) to \(\Omega(n^{1/2+\epsilon})\) over a fixed field | 4 | 3 | 3 | 5 | 3 | 540 |
| 4 | SAT-1 | Independently formalize the Jiang--Cai exact-rational LP certificate and strengthen one recombination inequality enough to beat \(1.307031578^n\) for randomized general 3-SAT | 4 | 3 | 2 | 5 | 5 | 600 |
| 5 | PS-4 | Prove or refute the explicit \(k=3\) Structured One-Query Robustness statement (4.5) for the actual CBPHP layer cells | 4 | 2 | 4 | 5 | 4 | 640 |
| 6 | SAT-2 | Improve deterministic general 3-SAT below \(1.32793^n\) by a certified branching/covering-code measure | 4 | 3 | 2 | 5 | 4 | 480 |
| 7 | SAT-3 | Extend Tamaki's deterministic SYM/THR \#SAT saving from \(m=O(n^2/\log^b n)\) to \(m=n^2/\log^{o(1)}n\), with a superpolynomial saving | 4 | 2 | 4 | 5 | 3 | 480 |
| 8 | PS-5 | Settle whether restart-free 1-UIP CDCL polynomially simulates Resolution, first on a bounded-width or bounded-incidence family | 4 | 2 | 3 | 5 | 3 | 360 |
| 9 | PS-6 | Prove \(n^{\Omega(k)}\) general-Resolution lower bounds for random-graph \(k\)-clique formulas in a nontrivial growing-\(k\) regime | 4 | 2 | 3 | 4 | 3 | 288 |
| 10 | PS-7 | Resolve weak automatizability of Resolution, equivalently feasible interpolation for \(\mathrm{Res}(2)\) | 5 | 1 | 5 | 4 | 2 | 200 |

The ordering uses judgment as well as the raw product (PS-4's product is high, but even its exact
application-sufficient formulation (4.5) may admit a structured private-point counterexample).

### PS-1: bounded-coefficient cutting-planes space

**KNOWN.** \(\mathrm{CP}_2\) is already exponentially stronger than Resolution in length and can
refute PHP in inequality space 5; \(\mathrm{CT}_n\) needs
\(\Omega(\log\log\log n)\) inequality space.

**TARGET.** Prove \(\omega(\log\log\log n)\), initially even along an explicit infinite
subsequence or for a more constrained normal form that can later be normalized without losing
space.

**Why small and meaningful.** It is a quantitative improvement in a fixed, explicit system/family,
not a disguised major separation. It tests whether coefficient restrictions genuinely restore a
space hierarchy.

**Already-known audit.** Exact-phrase searches for \(\mathrm{CP}_2\), complete tree
contradiction, and inequality space found the 2014 paper and later joint length/space results, but
no improved pure \(\mathrm{CP}_2\) inequality-space bound. The 2026 branch-and-cut paper studies a
different model. Confidence: medium-high.

**Falsification/computation.** Enumerate normalized coefficients in \(\{-2,-1,0,1,2\}\) for small
\(n\); encode existence of a space-\(s\) derivation as SAT/SMT after quotienting inequalities by
Boolean equivalence; search for constant-space patterns that invalidate a proposed invariant.

**Formalization.** Lean definitions of Boolean-valid inequalities, CP rules, configurations, and a
candidate invariant are realistic. Exhaustive certificates can be checked independently.

### PS-2: strict effective simulation by regular Resolution

**KNOWN.** Buss--Yolcu construct \(f(\Gamma,s)\), computable in
\(\operatorname{poly}(|\Gamma|+s)\), satisfiable iff \(\Gamma\) is, such that if \(s\) upper-bounds
the shortest Resolution proof then \(f(\Gamma,s)\) has a regular-Resolution proof polynomial in
\(|\Gamma|+s\). They explicitly ask whether \(s\) can be removed.

**TARGET.** Construct \(f(\Gamma)\) in polynomial time in \(|\Gamma|\), with regular proof size
polynomial in the minimum Resolution proof size, or exhibit an obstruction to every transformation
in a clearly delimited syntactic class.

**Source/open evidence.** [Buss and Yolcu, *Regular Resolution Effectively Simulates Resolution*,
IPL 2024, author PDF](https://emreyolcu.com/research/regular-effectively-general.pdf). Searches
through August 2026 returned the paper's explicit open question and no closure.

**Falsification.** Test candidate transformations against pebbling, guarded graph tautologies, and
known regular-vs-general separations; check whether an implicit \(s\) is merely encoded in padding.

**Formalization.** The transformation and local regularity argument are finite syntactic objects
and suitable for Lean once a candidate exists.

### PS-3: low-degree Tseitin PCR space

**KNOWN.** Simple degree-3/4 expander Tseitin formulas have \(\Omega(\sqrt n)\) PCR space via the
square-root width relation. Linear space is known for doubled-edge (degree-6 multi-)graphs;
\(\Omega(n/\log n)\) needs very large constant degree.

**TARGET.** A first \(\Omega(n^{1/2+\epsilon})\) lower bound for one explicit simple 3- or
4-regular expander family, over a fixed field stated in advance.

**Already-known audit.** The 2025 Theory of Computing paper explicitly says degree below 6 still
has only \(\Omega(\sqrt n)\). Searches for 2025--2026 Tseitin PCR space found no improvement.
Do not use doubled edges or high degree and call it this target.

**Falsification.** Compute minimum-space PCR configurations for small expanders using linear
algebra/SAT encodings; actively seek low-space elimination orders. A counterexample family with
\(O(\sqrt n)\) space would refute the intended invariant.

**Formalization.** Definitions and graph expansion lemmas are feasible; the likely combinatorial
space argument would be substantial.

### SAT-1 and SAT-2: certified exact-base improvements

**SAT-1 target.** First reproduce the July 2026 rational intervals exactly, then change one
inequality or add one valid structural statistic and obtain a strictly smaller general-3-SAT base.
The replication is validation, not itself a new theorem; the strict certified improvement is the
open target.

**SAT-2 target.** Improve Liu's deterministic \(1.32793\) base. A valid result must include a
complete worst-case recurrence, cover construction, polynomial overhead, and all boundary cases;
benchmarks are irrelevant to the asymptotic claim.

**Already-known audit.** Searches separated unique/general and randomized/deterministic records.
No later published deterministic general-3-SAT base was found. The randomized 2026 number is a
preprint and should not be mixed with deterministic work.

**Computation/formalization.** Exact rational LP duals and finite branching recurrences are ideal
for independent scripts and eventual Lean checking. Floating-point optimization is insufficient.

### PS-4: repair the false affine robustness premise

**KNOWN NEGATIVE.** Arbitrary affine spaces plus arbitrary per-flat deletions fail by Section 4.2.

**TARGET.** Prove or refute the explicit \(k=3\) Structured One-Query Robustness statement (4.5).
It uses exactly the cells, single-query closures, and shared collision deletions supplied by
Section 4.3 of TR26-007.  Unlike a generic affine-union statement, it does not need the paper's
incorrect codimension assertion.

**Risk.** The structured statement may also be false; its current formulation is not stable enough
to call a conjecture endorsed by the literature. It must first survive attempts to realize the
coordinate-flat construction as CBPHP solution spaces. A result obtained only after adding an
overlap or independence hypothesis is not sufficient unless that hypothesis is separately proved
for all proof layers. The original Conjecture 1.4 is not eligible as a target.

### SAT-3: cross the near-quadratic threshold-gate frontier

**KNOWN.** Tamaki handles \(m=O(n^2/\log^b n)\) SYM/THR gates with a superpolynomial saving.

**TARGET.** Reduce the required logarithmic gap, initially to
\(m=n^2/\exp(O(\sqrt{\log n}))\) or \(n^2/\log^{o(1)}n\), while retaining a proved
\(2^n/n^{\omega(1)}\) deterministic \#SAT algorithm.

**Already-known audit.** Alman--Chan--Williams and later PTF algorithms cover incomparable
composed/small-size regimes. The ECCC 2026 frontier still states that the best general
depth-two-THR lower/algorithmic reach is subquadratic. No quadratic-gate SAT saving was found.

**Bridge limitation.** A SAT algorithm for THR\(\circ\)THR does not automatically instantiate a
Williams lower-bound theorem because OR/composition closure is unresolved. The algorithmic result
would still be meaningful, but its lower-bound consequence must be reproved.

### PS-5: restart-free 1-UIP versus Resolution

**TARGET.** Either simulate any bounded-width Resolution proof by restart-free 1-UIP CDCL with
polynomial overhead, or give an explicit superpolynomial separation in a precisely specified
trail/learning model. Start with bounded variable occurrence or graph width.

**Already-known audit.** With restarts, polynomial simulation is known. RMA's exact worst-case
overhead is linear multiplicatively and a quadratic separation is known. The handbook explicitly
leaves the restart-free question open; searches through 2026 found new CDCL/Res\((\oplus)\)
preprints but no closure of the Boolean 1-UIP question.

### PS-6: average-case clique Resolution

**KNOWN NEGATIVE SEARCH.** “Prove \(n^{\Omega(k)}\) Resolution lower bounds for some clique
formulas” is no longer open: a January 2026 preprint proves the worst-case bound in a substantial
growing-\(k\) regime. [Atserias et al., *Hard Clique Formulas for Resolution*, author
PDF](https://www.cs.upc.edu/~atserias/papers/hard-clique-formulas-for-resolution/clique.pdf).

**TARGET.** Obtain \(n^{\Omega(k)}\) for the standard random-graph clique CNF with high
probability in a nontrivial growing-\(k\) regime. Prior work gives weaker general-Resolution
average-case exponents, while \(n^{\Omega(k)}\) is known for regular Resolution.

- Sources checked: [Pang, ECCC TR19-068](https://eccc.weizmann.ac.il/report/2019/068/);
  [regular-Resolution random clique, arXiv:2012.09476](https://arxiv.org/abs/2012.09476).
- Risk: high; the fresh 2026 worst-case construction may not transfer to the random distribution.

### PS-7: weak automatizability

**TARGET.** Decide whether Resolution is weakly automatizable / \(\mathrm{Res}(2)\) has feasible
interpolation.

**Why ranked last.** It is exceptionally well connected but has resisted direct attack for over two
decades. It is too large for the first research move unless a smaller structural lemma emerges.

## 7. Track-local recommendation

**Recommend PS-1: improve bounded-coefficient Cutting Planes inequality space for the complete
tree contradiction.** It is the smallest verified gap in this dossier with all of the following:

- an explicit family and fixed proof system;
- a concrete current lower bound and a meaningful arbitrarily small asymptotic improvement;
- finite instances that can be exhaustively searched for counterexamples to candidate invariants;
- proof objects and rules that can be formalized without first building a large analysis library;
- no dependence on an unverified 2026 conjecture or a floating-point optimization record.

The first attack should not begin by trying to prove a large bound. It should:

1. reproduce the \(\Omega(\log\log\log n)\) argument and identify exactly where the iterated-log
   loss arises;
2. enumerate minimum-space \(\mathrm{CP}_2\) refutations of \(\mathrm{CT}_n\) for the largest
   feasible \(n\), quotienting inequalities by their Boolean truth sets;
3. formulate one candidate monotone configuration invariant that would yield
   \(\Omega(\log\log n)\) or even a strict \(\omega(\log\log\log n)\) improvement;
4. attempt to falsify the invariant computationally before proving it;
5. formalize the normalization and invariant statement in Lean only after the finite tests survive.

This is a track-local recommendation. The repository-wide first target must be chosen only after
comparison with the circuit, meta-complexity, and barrier-track dossiers.

## 8. Negative findings and uncertainty ledger

1. **FALSE-AS-WRITTEN proof candidate:** Alekseev--Gaevoy Conjecture 1.4/4.2, including
   \(q=3\) for every fixed \(r\), has the coordinate middle-layer counterexample in Section 4.
   It should not be ranked as an open target. Independent human-level checking is still required
   before treating the counterexample as a publication claim.
2. **ERROR/GAP IN ARGUMENT, not a separate refutation of the coarse conditional conclusion:**
   fixing a full closure assignment makes the cells' binary codimension as large as
   \(\operatorname{rk}(L)+|\operatorname{Cl}(L)|\log M\), contrary to the rank-only assertion in
   Section 4.3. The same-\(q\) use of Conjecture 4.2 is therefore not justified as written.
3. **ERROR/GAP IN ARGUMENT, plausibly repairable:** Conjecture 4.2 at the single value
   \(r=k-2\) gives the coarse \((N\log M)^{-(k-2)c}\) loss, not the stronger
   \(\delta_N^c\) displayed in Theorem 4.3. The coarse loss is the one relevant to Theorem 1.1.
4. **Primary-source type ambiguity:** “no collisions on \(L_j\cup\{\ell_j=\beta\}\)” in Section
   4.3 must mean no collisions on its closure; collisions are only defined on pigeon sets. This
   interpretation is forced by Definition 4.5, Lemma 4.6, and Section 4.2, but a future citation
   should mention the typo.
5. **Already known:** Polynomial Calculus size--degree tradeoffs, including strong same-proof
   variants.
6. **Already known:** linear PCR space after XOR substitution/doubling edges; this does not close
   the simple degree-3/4 expander target.
7. **Already known:** linear PCR monomial space for random 3-CNF; do not retain the older open
   problem.
8. **Already known:** worst-case \(n^{\Omega(k)}\) hard clique formulas for Resolution in a 2026
   preprint; only the average-case version remains in the target list.
9. **Not settled by NP-hard automation:** weak automatizability of Resolution.
10. **Not a Frege lower bound:** Alekseev's 2026 Ext-PC square-root lower bound, because BVP has no
   polynomial-size CNF translation and the resource is coefficient bit size.
11. **Not an \(\mathrm{AC}^0[p]\)-Frege tautology lower bound:** the 2025 infinitely-often result
   whose formula truth status remains open.
12. **Not a circuit lower-bound bridge by itself:** a better 3-SAT exponential base, or a
   THR\(\circ\)THR algorithm without the closure hypotheses of the Williams framework.
13. **Record uncertainty:** the claim that Liu's \(1.32793^n\) remains the fastest published
    deterministic general-3-SAT bound is based on targeted searches, not an exhaustive database
    proof. Any use in a novelty claim needs a fresh bibliographic audit.
14. **Record uncertainty:** Jiang--Cai's July 2026 base is a recent preprint. Its exact rational
    certificate was not independently rerun in this cycle.
15. **Terminology collision:** \(\mathrm{CP}_k\) in the space paper means coefficients bounded by
    a constant. Other papers use similar subscripts/stars for different restrictions. Every future
    statement must repeat the coefficient convention.

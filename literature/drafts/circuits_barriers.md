# Phase 0/1 reconstruction: Boolean circuits and lower-bound barriers

**Audit date:** 2026-08-13
**Scope:** Boolean circuit complexity (general and restricted circuits), uniform versus nonuniform consequences, and barriers relevant to lower bounds. A small algebraic-complexity appendix is included because a fresh withdrawn barrier claim creates an unusually concrete first-target candidate.
**Epistemic rule:** `KNOWN` below means that a cited source states and proves the result. `OPEN` means that primary/recent sources explicitly pose it or identify the cited bound as the current frontier and that targeted searches found no later resolution. `UNKNOWN-STATUS` means that the available text plausibly contains more than its formal theorem states, but a complete uniform parameter audit or independent proof is missing. No claim here is a novelty claim.

## 1. Model and notation ledger

- `B_2` is the complete basis of all two-input Boolean functions. Circuits have unrestricted depth and fan-out; size is the number of non-input gates. This is the model for the current explicit general-circuit record.
- `U_2 = B_2 \setminus {XOR, XNOR}`. A lower bound in `U_2` is not a lower bound in the full `B_2` model.
- `AC^0` has fixed depth, polynomial size, unbounded-fan-in AND/OR and negations (negations can be pushed to inputs). `AC^0[p]` additionally has unbounded-fan-in `MOD_p`; `ACC^0` permits `MOD_m` for an arbitrary fixed modulus (or a fixed finite collection of moduli). These names are nonuniform unless uniformity is stated.
- `TC^0` has fixed depth and polynomial size with linear-threshold gates. `THR o THR` is depth two. Threshold weights are arbitrary reals unless a source normalizes them to bounded integers without changing the represented gate.
- A De Morgan formula is a fan-out-one binary AND/OR tree with literals at the leaves; its size convention must be checked (leaves versus gates) before comparing constants.
- `P/poly` denotes nonuniform polynomial-size Boolean circuits. A *uniform* circuit theorem is never silently transferred to the nonuniform model.
- `E^NP` means deterministic time `2^{O(n)}` with an NP oracle. A lower bound for a language in `E^NP` is not an explicit-P or explicit-NP lower bound.
- Correlation is with respect to the uniform distribution unless stated otherwise. `CAPP_delta` asks for acceptance probability to additive error at most `delta`.

## 2. Ground truth: general Boolean circuits

### 2.1 Counting gives existential, not explicit, lower bounds

**KNOWN — Shannon counting bound.** For fan-in-two circuits over a fixed finite complete basis, almost every Boolean function on `n` inputs requires size `Omega(2^n/n)`. The proof counts circuit descriptions and compares them with the `2^{2^n}` truth tables. It is fully nonuniform and says nothing about a named function in P or NP. Source: Claude Shannon, “The Synthesis of Two-Terminal Switching Circuits” (1949), [primary copy](https://deeplearning.cs.cmu.edu/F24/document/readings/Shannon49.pdf), [DOI](https://doi.org/10.1002/J.1538-7305.1949.TB03624.X).

**KNOWN — matching universal upper bound up to basis conventions.** Lupanov showed that every `n`-variable Boolean function has circuit size `O(2^n/n)` over a standard complete basis; together with counting this gives worst-case `Theta(2^n/n)`. Exact leading constants depend on the allowed basis and cost convention, so this report does not transfer a leading constant between models. Source: O. B. Lupanov (1958), [MathNet primary record/copy](https://www.mathnet.ru/eng/dan22802).

**Limitation and dependency.** Counting works because a random truth table is overwhelmingly complex, but the property “has circuit complexity above s” is not thereby made efficiently recognizable or attached to an explicit low-complexity family. This explicitness gap is the central discontinuity between Shannon’s theorem and `NP not subseteq P/poly`.

### 2.2 The explicit full-basis record is only linear

**KNOWN — Li–Yang.** There are affine dispersers, constructible in polynomial time, whose unrestricted `B_2` circuit size is at least `3.1n-o(n)`. The model is nonuniform, arbitrary depth and fan-out, all binary Boolean gates, with gate count as size. The proof strengthens weighted gate elimination through a detailed analysis of bottleneck configurations. Source: Jiatu Li and Tianqi Yang, “`3.1n-o(n)` Circuit Lower Bounds for Explicit Functions,” STOC 2022, [ECCC TR21-023](https://eccc.weizmann.ac.il/report/2021/023/), [primary PDF](https://eccc.weizmann.ac.il/report/2021/023/download), [DOI](https://doi.org/10.1145/3519935.3519976).

**Later-status check.** A 2026 paper on constructive refuters still calls Li–Yang the state-of-the-art `3.1n-o(n)` bound, while adding an algorithm that extracts an error from undersized circuits rather than improving the numerical lower bound. Source: Carmosino, Dang, and Jackman, “Constructive Separations from Gate Elimination” (2026), [arXiv:2604.23958](https://arxiv.org/abs/2604.23958).

**KNOWN — quadratic-disperser implication.** An `(n,k,s)` quadratic disperser is nonconstant on every subset of `F_2^n` of size at least `s` that is the common zero set of at most `k` quadratic polynomials. If `f` is an `(n,1.83n,2^{g(n)})` quadratic disperser for any `g(n)=o(n)`, then its `B_2` circuit size is at least `3.11n`. The technique is weighted gate elimination whose induction measure is the size of a quadratic variety, not merely the number of live variables. No explicit/NP construction with these parameters is supplied. Source: Golovnev and Kulikov, “Weighted gate elimination: Boolean dispersers for quadratic varieties imply improved circuit lower bounds,” [ECCC TR15-170](https://eccc.weizmann.ac.il/report/2015/170/), [primary PDF](https://www.golovnev.org/papers/weighted.pdf).

**Negative finding — model confusion.** The often-quoted `5n-o(n)` explicit lower bound is for `U_2`, which excludes XOR and XNOR, not for full `B_2`. It therefore does not supersede `3.1n-o(n)`. Source: Iwama and Morizumi, [author/archival PDF](https://danchik.ru/biblio/articles/5nsu2.pdf), [DOI](https://doi.org/10.1007/3-540-45687-2_29).

**Current gap.** Li–Yang explicitly note that it is unknown whether an explicit function (for example one in NP) requires even `10n` full-basis gates. Thus current explicit and Shannon bounds differ exponentially.

## 3. Uniform versus nonuniform: exact consequences and non-consequences

### 3.1 Basic equivalences

**KNOWN.** A language is in `P/poly` iff it is decidable in polynomial time with polynomial-length advice, equivalently by a polynomial-size (not necessarily constructible) circuit family. A standard P-uniform polynomial-size circuit family characterizes P, but the precise uniformity convention (direct connection language, logspace uniformity, or polynomial-time generation) must be named for finer classes.

**Sanity check.** Every tally language is in `P/poly`: at each input length there is only one potentially accepted unary string, so one advice bit/circuit constant suffices. Hence `P/poly` contains undecidable languages. Circuit existence is not an algorithm for finding or evaluating a succinctly specified circuit family.

### 3.2 Consequences of an NP nonuniform upper bound

**KNOWN — Karp–Lipton.** If `NP subseteq P/poly`, then the polynomial hierarchy collapses to its second level (`PH = Sigma_2^P`, with the standard equivalent formulations). The proof guesses a small circuit for SAT and universally checks its self-reducibility-based consistency. It does *not* prove `NP not subseteq P/poly`. Source: Karp and Lipton, “Some Connections Between Nonuniform and Uniform Complexity Classes,” STOC 1980, [DOI](https://doi.org/10.1145/800141.804678).

**KNOWN — Kannan, with quantifier warning.** For every fixed integer `k >= 0`, there is a language `L_k in Sigma_2^P intersect Pi_2^P` that has no `O(n^k)` circuit family. The language can depend on `k`; the theorem does not provide one language in that intersection outside all polynomial circuit sizes. Source: Ravi Kannan, “Circuit-size lower bounds and non-reducibility to sparse sets,” Information and Control 55 (1982), [publisher page](https://www.sciencedirect.com/science/article/pii/S0019995882903825), [DOI](https://doi.org/10.1016/S0019-9958(82)90382-5).

**Logical direction.** `NP not subseteq P/poly` would imply `P != NP`, since `P subseteq P/poly`. The converse is not known and is substantially weaker. A restricted-class lower bound such as `PARITY notin AC^0` or `NEXP notin ACC^0` does not by itself imply `P != NP`.

### 3.3 Uniform lower bounds can be much stronger

**KNOWN — Allender.** The permanent, and more generally problems hard for `C_=P` (hence appropriate PP/#P-hard problems), cannot be computed by *uniform* constant-depth threshold circuits of size `T(n)` whenever every fixed iterate `T^{(k)}(n)=o(2^n)`. The proof uses uniform complexity-class simulations/diagonalization; uniformity is essential. Source: Eric Allender, “The Permanent Requires Large Uniform Threshold Circuits,” CJTCS 1999(7), [primary PDF](https://cjtcs.cs.uchicago.edu/articles/1999/7/cj99-07.pdf), [DOI](https://doi.org/10.4086/cjtcs.1999.007).

**Limitation.** This theorem gives no analogous nonuniform `TC^0` lower bound for permanent. Removing uniformity is therefore a real open target, not a routine restatement.

## 4. Restricted Boolean circuit lower bounds

### 4.1 `AC^0`

**KNOWN — Furst–Saxe–Sipser/Yao/Hastad line.** Fixed-depth polynomial-size `AC^0` circuits cannot compute parity. In the standard convention with `d` alternating unbounded-fan-in AND/OR layers, parity requires size `exp(Omega_d(n^{1/(d-1)}))`, essentially matching upper bounds at fixed depth. The decisive technique is a random restriction plus the switching lemma: restricted small-depth circuits simplify to shallow decision trees while parity retains complexity. Sources: Furst, Saxe, and Sipser, [primary copy](https://wiki.epfl.ch/edicpublic/documents/Candidacy%20exam/Furst%20Saxe%20Sipser%20-%201984%20-%20Parity%20circuits%20and%20the%20polynomial-time%20hierarchy.pdf), [DOI](https://doi.org/10.1007/BF01744431); Johan Hastad, “Almost Optimal Lower Bounds for Small Depth Circuits,” [author PDF](https://www.csc.kth.se/~johanh/largesmalldepth.pdf), [DOI](https://doi.org/10.1145/12130.12132).

**KNOWN — correlation strengthening.** Later switching-lemma analyses imply that a depth-`d`, size-`S` `AC^0` circuit has correlation at most `2^{-Omega(n/(log S)^{d-1})}` with parity, in the relevant parameter range. Source: Hastad, [SIAM J. Comput. DOI](https://doi.org/10.1137/120897432).

**Limitations.** These are nonuniform lower bounds, but only for circuits without modular or threshold gates. A 2026 `2^{n^{1/3-o(1)}}` lower bound for depth-four circuits computing majority is still an AND/OR depth-four theorem, not an `ACC^0` theorem. Source: Wu and Li, [arXiv:2608.09070](https://arxiv.org/abs/2608.09070).

### 4.2 `AC^0[p]`

**KNOWN — Razborov–Smolensky.** For distinct prime-power characteristics (in particular, `MOD_r` against fixed-depth circuits with `MOD_p` where `r` is not a power of prime `p`), exponential lower bounds hold; Smolensky's original depth-`k` statement gives a bound of the form `exp(Omega(n^{1/(2k)}))` on the number of AND/OR gates under its convention. Majority lower bounds also follow in the model. The proof approximates circuits by low-degree polynomials over `F_p` and then proves that the target cannot be so approximated. Source: Roman Smolensky, “Algebraic Methods in the Theory of Lower Bounds for Boolean Circuit Complexity,” STOC 1987, [primary copy](https://www.cs.bu.edu/faculty/gacs/courses/cs535/papers/p77-smolensky.pdf), [DOI](https://doi.org/10.1145/28395.28404).

**Limitation.** The field characteristic is the engine of the proof. It does not handle circuits mixing incompatible moduli and hence does not settle general `ACC^0`; this is a method/model boundary, not a theorem that mixed-modulus lower bounds are impossible.

### 4.3 `ACC^0`

**KNOWN — Williams.** `NEXP` is not contained in nonuniform polynomial-size `ACC^0`. More quantitatively, `E^NP` is not contained in nonuniform `ACC^0` of size `2^{n^{o(1)}}`; for every fixed depth `d` and modulus `m`, some `delta>0` and a language in `E^NP` require depth-`d` `ACC[m]` size `2^{n^delta}`. The route is algorithmic: reduce `ACC` circuits to a symmetric-gate representation, obtain SAT faster than exhaustive search, and combine this with easy witnesses and a time hierarchy. Source: Ryan Williams, “Nonuniform ACC Circuit Lower Bounds,” JACM 61(1), [author-course mirror of primary paper](https://people.engr.tamu.edu/j-chen3/courses/637/2020/reading/p3.pdf), [DOI](https://doi.org/10.1145/2559903).

**Limitations.** The hard language lies high above P/NP, and the theorem does not show that a standard explicit P function such as majority is outside `ACC^0`. It does not extend to unrestricted `TC^0`. The SAT-to-lower-bound implication requires an algorithm for the right closure of the circuit class, not merely a heuristic SAT speedup.

### 4.4 Threshold circuits

**KNOWN — fixed-depth wire/gate lower bounds.** Impagliazzo, Paturi, and Saks prove that parity computed by depth-`d` arbitrary-weight threshold circuits needs at least `n^{1+c*theta^{-d}}` wires (for an absolute constant and the paper's `theta <= 3` parameterization), and give a gate lower bound `(n/2)^{1/(2(d-1))}`. The method is random restriction. These are nonuniform, fixed-depth, polynomial lower bounds, not superpolynomial `TC^0` lower bounds. Source: [IPS primary PDF](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiSaks_1997_siamjc.pdf), [DOI](https://doi.org/10.1137/S0097539792282965).

**KNOWN — depth-two explicit-P record.** Kane and Williams construct a linear-time computable Andreev-type function such that, for `epsilon` above their stated `sqrt(log n/n)` regime, every depth-two arbitrary-weight LTF circuit agreeing on a `1/2+epsilon` fraction needs `Omega(epsilon^3 n^{3/2}/log^3 n)` gates or `Omega(epsilon^3 n^{5/2}/log^{7/2} n)` wires. The proof combines random restrictions and Littlewood–Offord/anti-concentration. Source: Kane and Williams, [arXiv:1511.07860](https://arxiv.org/abs/1511.07860), [DOI](https://doi.org/10.1145/2897518.2897636).

**KNOWN — 2026 `E^NP` advance.** For every fixed constant `epsilon in (0,1)`, Chen, Tal, and Yichuan Wang give an `f in E^NP` requiring `n^{2.5-epsilon}`-size `THR o THR` (also `SYM o THR`). Their technical theorem is a deterministic additive-`o(1)` CAPP algorithm for `XOR_2 o THR_{O(n^{2.5-epsilon})} o THR` in time `2^{n-n^{Omega(epsilon)}}`; the explicit Theorem 6.1 uses size `O(n^{2.5-2epsilon})` and time `O(2^{n-n^{epsilon/100}})`. Arbitrary real weights are normalized to bounded integers, and size is gate count in the paper's model. Source: Chen, Tal, and Wang, “Super-quadratic Lower Bounds for Depth-2 Linear Threshold Circuits,” [ECCC TR26-039 landing page](https://eccc.weizmann.ac.il/report/2026/039/), [primary PDF](https://eccc.weizmann.ac.il/report/2026/039/download/).

**Technique/dependency.** The algorithm applies random restrictions to bottom thresholds, uses low-degree probabilistic polynomials for symmetric/`1hotSUM` gates on most columns, batch evaluation, and Williams' CAPP-to-lower-bound lemma. The lower bound needs a deterministic CAPP running in `2^n/n^{omega(1)}` for an XOR of two circuits, not merely CAPP for a single circuit.

**Limitations.** This improves the `E^NP` exponent but not the explicit-P `n^{3/2}` gate frontier, proves no superpolynomial depth-two threshold lower bound, and does not settle `NEXP not subseteq THR o THR`.

### 4.5 De Morgan formulas

**KNOWN.** Hastad's shrinkage theorem controls expected formula size under a random restriction and yields an explicit-P `n^{3-o(1)}` lower bound. Tal later obtained an explicit construction with lower bound `Omega(n^3/(log n (log log n)^2))` via quantum query/adversary ideas and composition. Sources: Hastad, [DOI](https://doi.org/10.1137/S0097539794261556); Avishay Tal, “Formula Lower Bounds via the Quantum Method,” [primary PDF](https://www.ias.edu/sites/default/files/math/csdm/16-17/TalSTOC2017.pdf), [DOI](https://doi.org/10.1145/3055399.3055472).

**Current gap.** An `n^{3+delta}` lower bound for an explicit P function remains open; later work still treats the cubic exponent as a barrier/frontier. Corroborating primary venue: [ITCS 2024 paper](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2024.10).

### 4.6 Monotone circuits

**KNOWN — classical and fresh frontiers.** Razborov's approximation method gave a superpolynomial monotone lower bound for clique and a quasipolynomial bound for perfect matching. Source: Razborov, “Lower bounds on the monotone complexity of some Boolean functions” (1985), [MathNet](https://www.mathnet.ru/eng/mzm/v37/i6/p887), [DOI](https://doi.org/10.1007/BF01157687).

**KNOWN — 2025/2026 strengthening.** Perfect matching on an `n+n` bipartite graph requires monotone circuit size `2^{n^{1/3-o(1)}}`, via the approximation method plus a new matching-sunflower lemma. The same paper records a `2^{n^{1/2-o(1)}}` explicit clique frontier. Source: [ECCC TR25-102 primary PDF](https://eccc.weizmann.ac.il/report/2025/102/download), [arXiv:2507.16105](https://arxiv.org/abs/2507.16105), [STOC 2026 DOI](https://doi.org/10.1145/3798129.3800824).

**Negative finding.** “Prove a `2^{n^{Omega(1)}}` monotone lower bound for perfect matching” is already known and must be rejected as a target. A truly exponential `2^{Omega(n)}` bound remains open. Monotone lower bounds do not transfer automatically to ordinary circuits with negations.

## 5. Barrier catalogue

### 5.1 Relativization

**KNOWN — Baker–Gill–Solovay.** There are recursive oracles `A,B` such that `P^A=NP^A` while `P^B != NP^B`. Therefore a proof whose every step remains valid relative to every oracle cannot resolve unrelativized P versus NP. Source: Baker, Gill, and Solovay, “Relativizations of the P=?NP Question,” [primary copy](https://cse.ucdenver.edu/~cscialtman/complexity/Relativizations%20of%20the%20P%3DNP%20Question%20%28Original%29.pdf), [DOI](https://doi.org/10.1137/0204037).

**What it does not say.** It does not ban diagonalization, simulation, or oracle arguments as components of a proof. It rules out only a fully relativizing route to a statement that has contradictory relativizations.

### 5.2 Natural proofs

**KNOWN — definitions.** A property of `n`-variable truth tables is P-constructive if membership can be decided in time polynomial in the `2^n`-bit truth table, large if its density is at least `2^{-O(n)}`, and useful against `P/poly` if every function sequence possessing it infinitely often escapes polynomial-size circuits. Source: Razborov and Rudich, “Natural Proofs,” [primary journal PDF](https://www.cs.toronto.edu/tss/files/papers/1-s2.0-S002200009791494X-main.pdf), [DOI](https://doi.org/10.1006/jcss.1997.1494).

**KNOWN — conditional barrier.** Under the existence of sufficiently hard pseudorandom generators/functions in `P/poly` (the paper formulates stretch-2 generators with `2^{n^{Omega(1)}}`-type hardness), there is no P-natural property useful against `P/poly`. The reduction uses a large constructive useful property as a statistical distinguisher for generator outputs. The barrier is conditional on cryptographic hardness.

**KNOWN — unconditional restricted analogue.** The paper also proves that no `AC^0`-natural property can be useful against `AC^0[2]`, explaining why the naturalized `AC^0` parity methods cannot simply yield Razborov–Smolensky-type bounds.

**What it does not say.** It does not rule out a property that is nonconstructive, not large, or not useful in the formal sense; it does not apply straightforwardly to monotone lower bounds because there is no comparable random-monotone-function largeness setup. Counting itself is not made natural merely by being simple.

### 5.3 Algebrization

**KNOWN — Aaronson–Wigderson.** Algebrization strengthens relativization by granting access to low-degree extensions of an oracle. Inclusion and separation statements use asymmetric oracle/extension access. The paper constructs algebraic oracle worlds giving opposite behavior for P versus NP and shows that major goals including `NEXP not subseteq P/poly` and superlinear NP circuit lower bounds require nonalgebrizing techniques under its definitions. Source: Aaronson and Wigderson, “Algebrization: A New Barrier in Complexity Theory,” [primary PDF](https://www.scottaaronson.com/papers/alg.pdf), [DOI](https://doi.org/10.1145/1490270.1490272).

**What it does not say.** “Uses algebra” is not synonymous with “algebrizes,” and the theorem does not invalidate algebraic mathematics. One must test the exact oracle-extension invariance of a proposed argument.

### 5.4 Gate-elimination barriers

**KNOWN — local substitution limits.** Golovnev, Hirsch, Knop, and Kulikov formalize broad fixed-`m` gate-elimination schemas based on substituting a bounded number of inputs and a standard/subadditive complexity measure. They construct functions/circuits for which the measure drops by only `O_m(1)`, limiting the constant obtainable by that local induction schema and preventing a superlinear conclusion from the most naive form. Source: “On the Limits of Gate Elimination,” [primary PDF](https://golovnev.org/papers/limits.pdf), [DOI](https://doi.org/10.4230/LIPIcs.MFCS.2016.46).

**Scope.** This is a barrier to a specified local proof template, not to every argument called gate elimination. Function-specific global amortization, weighted/nonstandard measures, growing substitutions, and structural information can lie outside it; indeed Li–Yang improve constants within a more elaborate analysis.

### 5.5 Approximation-method barriers

**KNOWN — Razborov.** For a formal class of circuit-approximation lower-bound arguments without auxiliary variables, the achievable lower bound is bounded in terms of the number of essential variables (roughly `O(n n_0)`, and `O(n_0)` in the probabilistic variant, in the source's measure). With sufficiently many auxiliary variables the formalism can simulate much more, so the result is a method-class limitation rather than a universal circuit barrier. Source: Razborov, “Unprovability of Lower Bounds on Circuit Size in Certain Fragments of Bounded Arithmetic,” [author PDF](https://people.cs.uchicago.edu/~razborov/files/approx.pdf).

### 5.6 Hardness-magnification locality

**KNOWN.** Many hardness-magnification targets have efficient circuits augmented with a small number of low-fan-in arbitrary oracle gates. A lower-bound technique that *localizes*—continues to work despite these gates—would contradict those upper bounds before reaching the magnification threshold. This blocks direct reuse of several weak-model techniques for certain magnification routes. Source: Chen et al., “Beyond Natural Proofs: Hardness Magnification and Locality,” [ITCS 2020 primary proceedings](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70).

**Scope.** Locality is relative to a target and a proof method. It is not a theorem that magnification cannot work, and barriers do not automatically stack: a route can be nonrelativizing yet natural, or evade natural proofs while still localizing.

## 6. Fresh 2026 theorem-status audits

### 6.1 Can CTW's fixed `epsilon` be made `epsilon(n)=Theta(log log n/log n)`?

**Question.** Is there already a deterministic additive-`o(1)`, `2^n/n^{omega(1)}` CAPP for `XOR_2 o THR o THR` of size `n^{5/2}/polylog(n)` by substituting a shrinking `epsilon(n)` into ECCC TR26-039?

**Verdict: `UNKNOWN-STATUS`, not `KNOWN`.** The paper states every main theorem for a *fixed constant* `epsilon`; at the start of Section 4 it explicitly declares `epsilon` a global constant. Targeted searches through 2026-08-13 for the title, CAPP terminology, `n^{5/2}/polylog(n)`, and threshold-circuit variants found no follow-up that states the nonconstant-parameter theorem. Absence alone is not the reason for the status: the proof contains `O(1)` quantities and sufficiently-large-`n` thresholds whose dependence on `epsilon` is not uniformly bounded in the text.

**Why a reparameterization is plausible.** Put the Theorem 6.1 size target in the form

`n^{2.5}/log^K n = n^{2.5-2 epsilon(n)}`,

so `epsilon(n)=K log log n/(2 log n)`. Then the explicitly displayed terms behave as follows:

- the bad-column contribution `n^{-epsilon/3}` becomes `log^{-K/6} n=o(1)`;
- the advertised saving `n^{epsilon/100}` becomes `log^{K/200} n`, which beats `log n` when `K>200` before hidden overheads;
- independence `n^{epsilon/200}` and the seed budget `n^{epsilon/100}` become polylogarithmic; merely fitting the usual `k log n` seed description suggests `K>400` under these normalizations;
- Appendix A.1 hides a number/degree of `1hotSUM` components depending on `epsilon` (for fixed polynomial wire exponent it is on the order of `1/epsilon`). Advice enumeration can then cost `2^{O((log n)^3/log log n)}`. The explicit savings in the relevant batch-evaluation sublemmas dominate this only once `K` is a sufficiently large constant (a rough line-by-line estimate is in the `360–400+` range, not a verified threshold);
- errors of the form `t 2^{-n^{epsilon/500}}` still tend to zero for every fixed `K>0`, because `n^{epsilon/500}` is a positive power of `log n` while `t=O(log n/log log n)`.

**Unresolved proof obligation.** Every hidden constant in the threshold normalization, structural reductions, probabilistic-polynomial construction, deterministic seed enumeration, and “for sufficiently large n depending on epsilon” statement must be made uniform simultaneously. The displayed algebra is encouraging but does not establish that. Therefore it would be scientifically incorrect to cite TR26-039 as already proving the polylog-denominator result.

**Research classification.** This is a high-value *verification target*, but it is not included among the genuinely open targets below until the proof is uniformly audited or the authors state the parameter dependence. If the audit succeeds for some explicit `K_0`, it is `KNOWN-IMPLICIT`; if it fails at a particular dependency, the smallest repair becomes an open target.

### 6.2 Balanced-chain set systems: withdrawn polynomial barrier claim

For even `n`, a balanced coloring is `f:[n]->{+1,-1}` with `sum_i f(i)=0`. A set system `X subseteq P([n])` is **1-balanced-chain** if for every balanced coloring there is a maximal chain

`emptyset=C_0 subset C_1 subset ... subset C_n=[n]`, with every `C_i in X`,

such that `|sum_{j in C_i} f(j)|<=1` for all `i`. Let `N(n)` be the minimum `|X|`.

**KNOWN — public bounds.** Fabris, Limaye, Srinivasan, and Yehudayoff prove

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`.

Their upper bound is an existence construction: a random balanced walk has sufficiently frequent zeros with noticeable probability, a recursive gap filler gives the recurrence `N(n)<=n^d N(n/log n)`, and a worst-case-to-average symmetrization costs only a polynomial factor. They also relate balanced-chain systems to min-partition-rank lower bounds for multilinear ABPs, with a balance-parameter asymmetry in the general multilinear case and a tighter correspondence in the set-multilinear case. Source: Fabris et al., “Multilinear Algebraic Branching Programs and the Min-Partition Rank Method,” [ECCC TR26-001 landing page](https://eccc.weizmann.ac.il/report/2026/001/), [primary PDF](https://eccc.weizmann.ac.il/report/2026/001/download/), especially Theorems 1.3 and 1.6.

**WITHDRAWN/NOT KNOWN — `N(n)=n^{O(1)}`.** ECCC TR26-043 originally claimed a polynomial construction and the resulting unconditional min-partition-rank barrier. Revision 1, dated 2026-05-11, states that an anonymous referee found a gap in Lemma 4.1: the forced-probability bound is valid unconditionally but not conditional on the filtration `F_t`, which the supermartingale argument needs; the notice says all results crucially rely on the lemma. The arXiv record is explicitly withdrawn and provides the same reason. Sources: [ECCC TR26-043 revision notice](https://eccc.weizmann.ac.il/report/2026/043/), [withdrawn arXiv:2604.00746](https://arxiv.org/abs/2604.00746).

**Independent gap check.** The proof defines

`p_t = Pr[|H(t+1)|=|H(t)|+1 | F_t]`

and needs `p_t<=1/4` for every live history so that `3^{|H(t)|}` is a supermartingale. The global identity `f(Pool_t)=-H(t)` only shows that same-sign elements are a minority in the whole remaining pool. The next frontier elements were selected through an adaptive path whose history is part of `F_t`; after conditioning, those frontier values need not be exchangeable with the entire pool. An unconditional average bound cannot be inserted into the conditional expectation. Thus the referee notice identifies a substantive quantifier/conditioning error, not a cosmetic omission. The maximum-imbalance, excursion-length, and multiscale estimates downstream all use the conditional drift.

**Search for an independent resolution.** Exact-phrase, author, arXiv-identifier, min-partition-rank, balanced-chain, and `N(n)` searches through 2026-08-13 found no revised proof or independent paper establishing the polynomial bound. Search results that still repeat the v1 abstract (paper aggregators, mirrors, ResearchGate copies) predate or ignore the withdrawal and are not evidence. The earlier Dvir–Malod–Perifel–Yehudayoff polynomial-mABP separation does not imply a 1-balanced-chain system: it uses full rank only for a restricted family of arc partitions, and the FLSY correspondence has a balance-parameter direction that cannot be reversed for free.

**Verdict: `OPEN` (high confidence in the public literature).** The strongest currently supportable upper bound is the FLSY quasipolynomial bound. `N(n)=n^{O(1)}` should not be listed as a theorem or as an established barrier. As always, “open” describes the audited public literature, not a proof that no unpublished argument exists.

## 7. Dependency graph

The graph is written as an adjacency ledger so that hypotheses and one-way implications remain visible. An arrow means “is an input to,” not logical equivalence.

### 7.1 Known nodes

| ID | Status | Node |
|---|---|---|
| K-GEN-COUNT | KNOWN | Almost all functions need `Omega(2^n/n)` fan-in-two gates. |
| K-GEN-EXPL | KNOWN | P-constructible affine dispersers need `3.1n-o(n)` full-`B_2` gates. |
| K-QD-IMP | KNOWN | `(n,1.83n,2^{o(n)})` quadratic disperser implies a `3.11n` lower bound. |
| K-PPOLY | KNOWN | `P/poly` equals polynomial advice; `NP subseteq P/poly` collapses PH. |
| K-AC0 | KNOWN | Parity has exponential fixed-depth `AC^0` lower bounds and strong correlation bounds. |
| K-AC0P | KNOWN | Modulus-mismatch lower bounds hold for `AC^0[p]`. |
| K-ACC | KNOWN | `NEXP not subseteq ACC^0`; quantitative `E^NP` lower bounds follow from faster ACC-SAT. |
| K-THR-P | KNOWN | An explicit P function has about `n^{3/2}` depth-two threshold gate lower bound (polylog losses). |
| K-THR-ENP | KNOWN | For every fixed `epsilon>0`, an `E^NP` function needs `n^{2.5-epsilon}` `THR o THR` gates. |
| K-FORM | KNOWN | Explicit P functions need `n^{3-o(1)}` De Morgan formula size. |
| K-MONO | KNOWN | Perfect matching needs monotone size `2^{n^{1/3-o(1)}}`; clique reaches `2^{n^{1/2-o(1)}}`. |
| K-BC-QP | KNOWN | `Omega(n^2)<=N(n)<=n^{O(log n/log log n)}` for 1-balanced-chain systems. |
| K-BARR-R | KNOWN | Opposite relativized worlds block fully relativizing resolutions. |
| K-BARR-N | KNOWN/CONDITIONAL | Natural proofs are blocked by strong PRGs; an `AC^0`-natural restricted barrier is unconditional. |
| K-BARR-A | KNOWN | Opposite algebrized worlds block fully algebrizing routes for named goals. |
| K-BARR-L | KNOWN | Fixed local gate elimination, formal approximation schemas, and localizing magnification methods have stated method-class limits. |

### 7.2 Open, false, and uncertain nodes

| ID | Status | Node |
|---|---|---|
| O-BC-POLY | OPEN | `N(n)=n^{O(1)}` for 1-balanced-chain set systems. |
| O-QD | OPEN | Construct an explicit/P quadratic disperser with the K-QD-IMP parameters. |
| O-B2 | OPEN | Improve `3.1n-o(n)` for full `B_2` by any fixed linear amount (with `10n` a famous stretch target). |
| O-FORM | OPEN | Explicit P `n^{3+delta}` De Morgan formula lower bound for some fixed `delta>0`. |
| O-THR-P | OPEN | Explicit P `n^{3/2+delta}` gate lower bound for `THR o THR`. |
| O-CAPP-25 | OPEN | Nontrivial additive-`o(1)` CAPP for `XOR_2 o THR o THR` of size `n^{2.5+delta}`. |
| O-THR-SP | OPEN | `NEXP not subseteq` polynomial-size `THR o THR`. |
| O-MAJ-ACC | OPEN | `MAJORITY notin` nonuniform `ACC^0`. |
| O-PERM-NTC | OPEN | Remove uniformity from a permanent/nonuniform `TC^0` lower bound. |
| O-MONO-EXP | OPEN | A `2^{Omega(n)}` monotone lower bound for clique or bipartite perfect matching. |
| U-CTW-PL | UNKNOWN-STATUS | Uniformize CTW to size `n^{2.5}/polylog(n)` by shrinking `epsilon`. |
| F-BC-PAPER | FALSE AS A CURRENT THEOREM | TR26-043's polynomial balanced-chain theorem; the proof is withdrawn and all results depend on the gap. |
| F-B2-5N | FALSE MODEL TRANSFER | The `5n-o(n)` `U_2` bound is not a full-`B_2` bound. |
| F-MONO-POLYEXP | FALSE/ALREADY KNOWN | `2^{n^{Omega(1)}}` for monotone perfect matching is no longer open. |
| F-REST-PNP | FALSE INFERENCE | A lower bound against a restricted circuit class does not by itself separate P and NP. |
| F-UNI-NONUNI | FALSE INFERENCE | A uniform circuit lower bound does not automatically imply a nonuniform one. |
| F-KANNAN | FALSE QUANTIFIER SWAP | Kannan's per-`k` languages do not yield one `Sigma_2^P intersect Pi_2^P` language outside `P/poly`. |

### 7.3 Edges and bottlenecks

1. `O-QD -> K-QD-IMP -> O-B2`. The first edge is a concrete combinatorial construction route to a numerical full-basis improvement. Direct attacks on O-B2 need not pass through quadratic dispersers.
2. `K-THR-P -> O-THR-P`. CTW's `K-THR-ENP` is a separate high-uniform-complexity branch; it does not advance the P-function exponent.
3. `K-THR-ENP + Williams CAPP-to-LB lemma -> O-CAPP-25 -> stronger E^NP threshold lower bound`. A family of algorithms covering every polynomial size would feed toward `O-THR-SP`, but one fixed `delta` does not by itself give a superpolynomial lower bound.
4. `K-AC0 + K-AC0P + K-ACC -> O-MAJ-ACC`. Switching/low-degree-polynomial arguments collide with modular gates, while Williams' algorithmic method currently places the hard language in a much larger time class.
5. `K-FORM -> O-FORM`; random-restriction shrinkage and quantum/adversary composition reach the cubic frontier but no known combination crosses it.
6. `K-MONO -> O-MONO-EXP`. The new matching-sunflower argument changes the baseline, but an exponent linear in `n` is still missing. The result remains confined to monotone circuits.
7. `K-BC-QP -> O-BC-POLY -> polynomial-size full-rank mABP -> min-partition-rank barrier for mABPs`. The last two arrows are the FLSY construction. Because TR26-043 is withdrawn, the barrier endpoint is not currently established by this route.
8. `K-BARR-R`, `K-BARR-N`, and `K-BARR-A` constrain different proof invariances; none follows from another. `K-BARR-L` constrains named local schemas. No edge should be read as “all lower-bound proofs are impossible.”
9. `U-CTW-PL` sits between K-THR-ENP and O-CAPP-25. Resolving its status is prerequisite hygiene: an implicit polylog-denominator theorem would narrow the genuine next delta.

## 8. Ten genuinely unresolved intermediate targets

Scores use the mission's five multiplicative axes, each on a 1–5 scale: novelty potential (`N`), tractability (`T`), connection to stronger lower bounds (`C`), falsifiability (`F`), and formalizability (`V`). “Distance” and “difficulty” are independent 1–5 estimates where 1 is near/easy and 5 is far/very hard. The numbers are triage judgments, not mathematical facts.

| Rank | Target | N/T/C/F/V | Product | Distance / difficulty | Barrier contact | Computation / formalization |
|---:|---|---|---:|---|---|---|
| 1 | **CB-1:** Prove `N(n)<=n^C` for some absolute constant `C` for 1-balanced-chain set systems. The first diagnostic milestone is to decide whether the withdrawn two-block construction is repairable. | 5/4/4/5/5 | **2000** | 1 / 3 | Would establish a barrier for min-partition rank; the failed proof has an adaptive-conditioning obstruction, not a classical natural-proof barrier. | Small `n` is exactly enumerable/SAT-encodable; finite definitions and deterministic reductions are Lean-friendly. |
| 2 | **CB-2:** Construct in P (or NP-explicitly) an `(n,1.83n,2^{o(n)})` quadratic disperser. | 4/3/4/5/4 | **960** | 2 / 4 | Feeds weighted gate elimination; may collide with local-elimination constants only after construction. | Search small quadratic varieties and functions with SAT/ILP; definitions and implication lemmas formalizable. |
| 3 | **CB-3:** Prove an explicit-P `n^{3+delta}` De Morgan formula lower bound for some fixed `delta>0`. | 4/2/4/4/4 | **512** | 3 / 5 | Crosses the shrinkage/quantum cubic frontier; naturalness must be audited only if extrapolated toward general circuits. | Exact small formula minimization is possible but weak asymptotic evidence; restriction identities formalizable. |
| 4 | **CB-4:** Improve the full-`B_2` record to `(3.1+delta)n-o(n)` for any fixed `delta>0`; keep `10n` as a stretch milestone. | 4/2/5/4/3 | **480** | 2 / 5 | Directly contacts gate-elimination local-configuration barriers. | Exhaustive optimal circuits only at very small `n`; local case tables can be machine checked. |
| 5 | **CB-5:** Give an explicit P function requiring `n^{3/2+delta}` depth-two arbitrary-weight threshold gates. | 4/2/4/4/3 | **384** | 3 / 5 | Anti-concentration/restriction frontier; arbitrary real weights complicate finite search. | Integer-normalized bounded cases can be SMT-tested; full real-weight quantification needs real algebra/duality. |
| 6 | **CB-6:** Deterministic additive-`o(1)`, `2^n/n^{omega(1)}` CAPP for `XOR_2 o THR o THR` of size `n^{2.5+delta}` for any fixed `delta>0`. | 4/2/5/3/2 | **240** | 2 / 5 | Directly extends Williams' algorithmic method; no relativization shortcut. | Benchmark structural subroutines, but asymptotic savings dominate; formalization of probability/error budgets is substantial. |
| 7 | **CB-7:** Prove `2^{Omega(n)}` monotone circuit size for clique or bipartite perfect matching. | 3/2/3/4/3 | **216** | 3 / 5 | Approximation method has formal limitations; new global/sunflower structure may escape old instantiations. | Small monotone synthesis/cover LPs possible; combinatorial core potentially formalizable. |
| 8 | **CB-8:** Prove `MAJORITY notin` nonuniform `ACC^0`. | 5/1/5/4/2 | **200** | 5 / 5 | Must handle mixed moduli; straightforward Razborov–Smolensky transfer fails. Natural-proof and algebrization audits become important. | Low-degree/torus approximations can be tested at small `n`, but finite evidence is very weak. |
| 9 | **CB-9:** Prove `NEXP not subseteq` polynomial-size `THR o THR`. | 5/1/5/2/2 | **100** | 5 / 5 | Would require CAPP/SAT progress for every polynomial size or a new nonalgorithmic method; naturalness/locality concerns are severe. | Little meaningful direct finite testing; formalization practical only after a concrete lemma exists. |
| 10 | **CB-10:** Extend the permanent lower bound from uniform to nonuniform polynomial-size `TC^0` (using the same output/encoding convention as the cited uniform theorem). | 4/1/4/2/2 | **64** | 5 / 5 | Uniformity is precisely what the current proof exploits; removing it approaches the general `TC^0` frontier. | Small threshold synthesis is possible but not diagnostic; exact encoding and reduction must be formalized first. |

### 8.1 Active “already known?” audit for every target

**CB-1.** FLSY prove only `n^{O(log n/log log n)}` and describe the polynomial question as unresolved. The only exact polynomial claim found is TR26-043; both ECCC and arXiv flag the conditional-probability gap, and arXiv marks it withdrawn. No revision/follow-up was found through the audit date. Old polynomial mABP/formula separations use restricted partitions and do not imply `N(n)=poly(n)`. **Classification: OPEN, high confidence.**

**CB-2.** The Golovnev–Kulikov source phrases the disperser as a sufficient hypothetical construction. Li–Yang instead obtain `3.1n-o(n)` from affine dispersers, and the April 2026 gate-elimination paper still identifies `3.1n-o(n)` as the record. Searches for the exact parameter triple and “quadratic variety disperser” found no P/NP construction. **Classification: OPEN, high confidence.**

**CB-3.** Tal's theorem is `n^3` divided by polylogarithmic factors, and the ITCS 2024 source continues to frame surpassing cubic as open. Searches for `n^{3+epsilon}`/supercubic De Morgan formula lower bounds found no explicit-P theorem. **Classification: OPEN, high confidence.**

**CB-4.** Li–Yang explicitly state that even `10n` for an explicit/NP function is unknown. The 2026 constructive-refuter paper calls `3.1n-o(n)` state of the art. The `5n-o(n)` result was checked and is only `U_2`. **Classification: OPEN, high confidence.**

**CB-5.** CTW's 2026 introduction identifies Kane–Williams' roughly `n^{1.5}` P-function result as the P baseline and obtains `n^{2.5-epsilon}` only by moving the hard function to `E^NP`. No P-function exponent improvement was found. **Classification: OPEN, high confidence.**

**CB-6.** CTW is the newest located result and stops below exponent `2.5` for fixed epsilon. The separate `n^{2.5}/polylog` question is only `UNKNOWN-STATUS`; choosing `2.5+delta` keeps CB-6 strictly beyond even a successful uniformization. No 2026 follow-up was found. **Classification: OPEN, high confidence.**

**CB-7.** The 2025 ECCC/STOC 2026 paper already proves `2^{n^{1/3-o(1)}}` for matching and reports `2^{n^{1/2-o(1)}}` for clique, but explicitly leaves true exponential bounds open. This target was tightened after rejecting the already-known `2^{n^{Omega(1)}}` version. **Classification: OPEN, high confidence.**

**CB-8.** Williams proves a high-class language outside ACC, not majority. The torus-polynomial program explicitly describes its symmetric result as a step toward majority-versus-ACC, and the August 2026 majority lower bound found in the freshness search is for depth-four AND/OR circuits only. **Classification: OPEN, high confidence.** Source for the torus formulation: [ECCC TR18-076](https://eccc.weizmann.ac.il/report/2018/076/).

**CB-9.** Chen's 2018 paper states that it is consistent with then-current knowledge that NEXP has polynomial-size `THR o THR`; CTW 2026 supplies only each fixed exponent below `2.5` for an `E^NP` function, not a superpolynomial lower bound. Source: Lijie Chen, “Toward Super-Polynomial Size Lower Bounds for Depth-Two Threshold Circuits,” [arXiv:1805.10698](https://arxiv.org/abs/1805.10698). **Classification: OPEN, high confidence.**

**CB-10.** Allender's theorem and later weak-uniformity work emphasize that the strong lower bound hinges on uniformity. No nonuniform permanent-`TC^0` theorem was located; such a theorem would subsume a central unproved nonuniform threshold lower bound. **Classification: OPEN, high confidence, but the exact Boolean/multi-output encoding must be frozen before work starts.**

## 9. Exactly one recommended first target

### Recommendation: CB-1 — polynomial-size 1-balanced-chain set systems

**Precise target.** For even `n`, prove that there is an absolute constant `C` such that every `[n]` admits a 1-balanced-chain set system of size at most `n^C`.

This is the first target to attack. It outranks the quadratic-disperser route because it is newly exposed, finitely stated, has a nearly complete but invalid construction to dissect, and a positive solution would rigorously settle the claimed min-partition-rank barrier. It is not a direct P-versus-NP attack and must not be presented as one.

The target is the **general existence statement**, not “repair TR26-043.” Repairing or refuting the posted steering argument is only the most informative first subproblem. A counterexample to its conditional-drift lemma, or even a proof that every construction of that restricted form fails, leaves `N(n)=n^{O(1)}` open and must be recorded only as a negative method result.

**Why it is genuinely unresolved.** The exact claim appeared in one April 2026 preprint. On 2026-05-11 that preprint was withdrawn; the official ECCC notice says its central conditional forced-probability lemma is unsupported and every result relies on it. The prior primary paper proves only a quasipolynomial upper bound. Searches through 2026-08-13 found no repaired version or independent proof. This is stronger evidence than merely failing to find a citation.

**Falsification-first plan.** Before trying to prove the polynomial theorem:

1. Reconstruct the TR26-043 two-block stochastic process exactly, including the filtration and every revealed variable.
2. Enumerate balanced colorings, tie-breaking coins, and reachable histories for small even `n`; find the smallest history for which the claimed conditional `p_t<=1/4` fails. This tests understanding of the gap, not the asymptotic theorem.
3. Encode minimal 1-balanced-chain systems as set cover/SAT/ILP. For each candidate family, each balanced coloring must be covered by at least one all-prefix-balanced maximal chain. Compute exact `N(n)` for the largest feasible small `n`, retaining certificates and symmetry reductions.
4. Test natural repairs—fresh random permutations at each scale, nonadaptive candidate frontiers, three or more blocks, or state-dependent potentials—against the same exhaustive history engine. Reject a repair immediately when conditional drift or set-system-size accounting fails.
5. Search for colorings that force any proposed restricted construction (two intervals, bounded-block steering, fixed recursion templates) to use superpolynomially many states. Such a negative result would not prove `N(n)` superpolynomial, but it would prevent rediscovery of a structurally failed scheme.

**Proof program if it survives.** The most plausible positive routes are:

- replace the false pointwise drift claim by a potential that includes the conditional composition of the two frontier blocks, and prove a supermartingale for that enlarged state;
- make exposure genuinely exchangeable by choosing the relevant block permutations independently of the adaptively revealed values, then pay explicitly for including all possible nonadaptive choices in the fixed set system;
- prove a likelihood-ratio or hypergeometric domination theorem for the adaptive process strong enough to bound entire excursions, rather than each step;
- abandon stochastic steering and give a deterministic recursive covering construction with a polynomial number of chain states.

Every route must simultaneously prove (i) success for a noticeable fraction of uniformly balanced colorings, (ii) a fixed set system independent of the coloring, and (iii) polynomial total size after worst-case symmetrization. An adaptive algorithm that sees `f` but whose possible outputs occupy a superpolynomial family is not enough.

**Lean/computational verification plan.** Formalize the finite core first:

- balanced colorings, maximal chains, chain imbalance, 1-balanced-chain systems, and `N(n)`;
- the worst-case-to-average symmetrization lemma of FLSY, separated from its probabilistic existence step;
- the two-block transition system and a finite counterexample to the withdrawn conditional lemma, if found;
- certificates from exact small-`n` search, checked by a small independent verifier.

Mathlib's finite probability and martingale libraries should be assessed before formalizing asymptotics. If the repaired proof uses a new supermartingale, formalize its one-step conditional inequality and stopping-time conditions before the multiscale recurrence. A machine-checked finite counterexample refutes only the proposed lemma/construction, not the polynomial `N(n)` conjecture.

**Stopping rule for the next cycle.** Do not branch into P versus NP. First decide one of: (a) an explicit smallest counterhistory to Lemma 4.1 plus a proved restricted-construction obstruction; (b) a corrected conditional potential with all constants and set-system accounting; or (c) evidence that the process can be made nonadaptive without losing polynomial size. Only then reassess the target.

## 10. Research hygiene and caveats to carry forward

- The CTW `n^{2.5}/polylog` extension is not safely citeable until all epsilon-dependence is uniformized. Its displayed exponents are evidence for plausibility, not a theorem.
- TR26-043 aggregators frequently display the withdrawn v1 abstract without the gap notice. Always cite the current ECCC landing page/arXiv status, not a stale mirror.
- The balanced-chain problem is algebraic-complexity barrier work. A positive result would show a limitation of min-partition rank for mABPs; it would not prove a Boolean lower bound or P versus NP.
- “Explicit” varies among truth-table constructibility, P-uniformity, NP-explicitness, and coefficient access. Each target must freeze its convention.
- Threshold gate count and wire count are different measures. Kane–Williams' exponents cannot be interchanged.
- The strongest lower bound for a restricted model is not evidence of a lower bound for a superclass unless an explicit reduction is proved.
- Failed approaches and smallest counterexamples should be retained in the repository; they are structural research data.

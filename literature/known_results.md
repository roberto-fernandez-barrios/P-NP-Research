# Known-results map for research cycle 1

**Audit date:** 2026-08-13.  **Scope:** Phase 0 ground truth, not a survey of
all of complexity theory.  `KNOWN` means that the cited source contains a
proof of the stated result in the stated model.  Conditional theorems retain
their hypotheses.  A preprint is identified as such.  The detailed source
checks are retained in
[`drafts/circuits_barriers.md`](drafts/circuits_barriers.md),
[`drafts/proof_sat.md`](drafts/proof_sat.md), and
[`drafts/meta_magnification.md`](drafts/meta_magnification.md).

## Conventions that prevent invalid transfers

* `n` normally denotes input variables; for truth-table problems `N=2^n` is
  the input length.  A bound in `n` is never silently reported as a bound in
  `N`.
* `P/poly` is nonuniform polynomial-size Boolean circuits.  Circuit existence
  does not supply an algorithm for constructing the circuit family.
* `B_2` allows every binary Boolean gate; `U_2` omits XOR/XNOR.  `AC^0[p]`,
  `ACC^0`, and `TC^0` are nonuniform unless uniformity is stated.
* A gate lower bound, wire lower bound, formula-leaf lower bound, branching-
  program-node lower bound, and proof-line/space lower bound are different
  measures.
* Exact SAT/#SAT, additive approximate counting (CAPP), and average-case
  correlation are different tasks.
* MCSP, Gap-MCSP, MKTP (`KT`), and MKtP (Levin `Kt`) are different problems.
  Parameter-preserving reductions are required before transferring a theorem.

## 1. General Boolean circuits and nonuniformity

### Counting and explicitness

**KNOWN — existential optimum.** Almost every Boolean function on `n` inputs
requires `Omega(2^n/n)` fan-in-two gates over a fixed finite complete basis;
every function has `O(2^n/n)` circuits up to basis/cost conventions.  The
lower bound counts circuit descriptions, is fully nonuniform, and names no
function in P or NP.  Sources: Shannon,
[*The Synthesis of Two-Terminal Switching Circuits*](https://doi.org/10.1002/J.1538-7305.1949.TB03624.X)
(1949); Lupanov, [primary MathNet record](https://www.mathnet.ru/eng/dan22802)
(1958).

**KNOWN — explicit unrestricted record.** Polynomial-time constructible
affine dispersers require `3.1n-o(n)` gates over the full `B_2` basis.  The
proof is weighted gate elimination with global bottleneck analysis.  The
often quoted `5n-o(n)` theorem is only for `U_2` and does not strengthen this
record.  Source: Li and Yang,
[*3.1n-o(n) Circuit Lower Bounds for Explicit Functions*](https://eccc.weizmann.ac.il/report/2021/023/)
(STOC 2022).  A 2026 constructive-refuter paper still identifies this as the
record: Carmosino--Dang--Jackman,
[arXiv:2604.23958](https://arxiv.org/abs/2604.23958).

**KNOWN — quadratic-disperser bridge.** An explicit
`(n,1.83n,2^{o(n)})` quadratic disperser would yield a `3.11n` full-`B_2`
lower bound.  The construction is not supplied by the theorem.  Source:
Golovnev and Kulikov,
[*Weighted gate elimination*](https://eccc.weizmann.ac.il/report/2015/170/).

### Uniform versus nonuniform

**KNOWN — advice characterization and its limits.** `P/poly` equals
polynomial-time computation with polynomial advice.  It contains every tally
language, including undecidable ones, so a nonuniform upper bound need not be
algorithmic.  If `NP subseteq P/poly`, then `PH=Sigma_2^P` (Karp--Lipton,
[*Some Connections Between Nonuniform and Uniform Complexity Classes*](https://doi.org/10.1145/800141.804678)).
For every fixed `k`, Kannan gives a language (which may depend on `k`) in
`Sigma_2^P intersect Pi_2^P` without `O(n^k)` circuits; this is not one
language outside all of `P/poly` (Kannan,
[*Circuit-size lower bounds and non-reducibility to sparse sets*](https://doi.org/10.1016/S0019-9958(82)90382-5)).

**KNOWN — uniform threshold lower bound.** Permanent and suitable
`C_=P`-hard functions require large *uniform* constant-depth threshold
circuits under Allender's iterated-size condition.  Uniformity is an essential
hypothesis; the theorem gives no nonuniform `TC^0` lower bound.  Source:
Allender,
[*The Permanent Requires Large Uniform Threshold Circuits*](https://cjtcs.cs.uchicago.edu/articles/1999/7/cj99-07.pdf)
(1999).

## 2. Restricted Boolean circuit lower bounds

**KNOWN — `AC^0`.** At every fixed depth, parity requires exponential-size
`AC^0` circuits; in the usual depth convention the exponent is essentially
`n^{1/(d-1)}`.  Random restrictions and the switching lemma simplify the
circuit but preserve parity's difficulty.  Sources: Furst--Saxe--Sipser,
[*Parity, circuits, and the polynomial-time hierarchy*](https://doi.org/10.1007/BF01744431);
Hastad,
[*Almost Optimal Lower Bounds for Small Depth Circuits*](https://doi.org/10.1145/12130.12132).
The theorem does not handle modular or threshold gates.

**KNOWN — `AC^0[p]`.** Razborov--Smolensky polynomial approximation over
`F_p` gives exponential lower bounds for incompatible modular functions and
for majority in fixed-depth `AC^0[p]`.  The characteristic is part of the
argument, so it does not settle mixed-modulus `ACC^0`.  Source: Smolensky,
[*Algebraic Methods in the Theory of Lower Bounds for Boolean Circuit Complexity*](https://doi.org/10.1145/28395.28404)
(STOC 1987).

**KNOWN — `ACC^0`.** `NEXP` is not contained in nonuniform polynomial-size
`ACC^0`; quantitatively, for fixed depth and modulus some language in
`E^NP` needs size `2^{n^delta}`.  Williams obtains a faster uniform ACC-SAT
algorithm and converts it to the nonuniform lower bound using easy witnesses
and a time hierarchy.  Source: Williams,
[*Nonuniform ACC Circuit Lower Bounds*](https://doi.org/10.1145/2559903).
The hard language is not majority or a standard language in P/NP.

**KNOWN — depth-two threshold baselines.** Kane--Williams give a linear-time
computable function requiring, up to polylogarithms, `n^{3/2}` gates and
`n^{5/2}` wires in `THR o THR`, including correlation bounds.  Source:
[*Super-Linear Gate and Super-Quadratic Wire Lower Bounds for Depth-Two and Depth-Three Threshold Circuits*](https://arxiv.org/abs/1511.07860).
Chen--Tal--Wang (2026) prove that for every fixed `epsilon>0` some function in
`E^NP` needs more than `n^{2.5-epsilon}` gates in `THR o THR` and
`SYM o THR`; their engine is deterministic additive-`o(1)` CAPP for the XOR
of two such circuits in `2^{n-n^{Omega(epsilon)}}` time.  Source:
[ECCC TR26-039](https://eccc.weizmann.ac.il/report/2026/039/).  This does not
improve the explicit-P exponent or give a superpolynomial lower bound.

**KNOWN — De Morgan formulas.** Explicit P functions have
`n^{3-o(1)}` formula lower bounds; Tal's quantitative result is
`Omega(n^3/(log n (log log n)^2))`.  Shrinkage/random restrictions and the
quantum adversary/composition method reach, but do not cross, the cubic
frontier.  Sources: Hastad,
[*The shrinkage exponent of de Morgan formulas is 2*](https://doi.org/10.1137/S0097539794261556);
Tal,
[*Formula Lower Bounds via the Quantum Method*](https://doi.org/10.1145/3055399.3055472).

**KNOWN — monotone circuits.** Classical approximation methods give strong
monotone lower bounds without implying ordinary-circuit lower bounds.  The
current located frontiers are `2^{n^{1/3-o(1)}}` for bipartite perfect
matching and `2^{n^{1/2-o(1)}}` for clique.  Sources: Razborov,
[*Lower bounds on the monotone complexity of some Boolean functions*](https://www.mathnet.ru/eng/mzm/v37/i6/p887);
[ECCC TR25-102](https://eccc.weizmann.ac.il/report/2025/102/) (STOC 2026).

## 3. SAT algorithms and lower-bound bridges

**KNOWN — exact `k`-SAT algorithms.** Schoning's randomized one-sided-error
Monte Carlo decision algorithm runs in `O^*((2-2/k)^n)` time (equivalently,
the witness search has the corresponding expected-time formulation on
satisfiable inputs); Moser--Scheder derandomize it up to an arbitrarily small
constant in the base.  Sources:
[Schoning](https://mathweb.ucsd.edu/~sbuss/CourseWeb/Math268_2007WS/schoning2002.pdf),
[Moser--Scheder](https://arxiv.org/abs/1008.4067).  Liu's deterministic
general 3-SAT bound is `O^*(1.32793^n)`
([ICALP 2018](https://doi.org/10.4230/LIPIcs.ICALP.2018.88)).  PPSZ and its
analyses give a randomized base near `1.307`; a July 2026 preprint claims
`1.307031578^n` for general 3-SAT using an exact rational LP certificate, but
independent peer validation was not found
([Jiang--Cai](https://arxiv.org/abs/2607.10697)).  None is polynomial time.

**CONJECTURED, not known.** ETH asserts a positive exponential exponent for
3-SAT.  SETH asserts that the optimal `k`-SAT exponent approaches one as
`k` grows.  The sparsification lemma converts a fixed-width CNF to at most
`2^{epsilon n}` bounded-occurrence CNFs, with constants depending on
`k,epsilon`; it does not prove ETH or SETH.  Sources:
[Impagliazzo--Paturi](https://doi.org/10.1006/jcss.2000.1727) and
[Impagliazzo--Paturi--Zane](https://cseweb.ucsd.edu/~paturi/myPapers/pubs/ImpagliazzoPaturiZane_1998_focs.pdf).

**KNOWN — algorithms to lower bounds.** A uniform SAT algorithm with a
superpolynomial saving for circuits of every fixed polynomial size, with the
needed closure and constructibility, implies `NEXP not subseteq P/poly`;
constant-factor exponential savings yield exponential circuit lower bounds
for an `E^NP` language.  The quantifier over every fixed size exponent is
essential.  Source: Williams,
[*Improving Exhaustive Search Implies Superpolynomial Lower Bounds*](https://www.cs.cmu.edu/~ryanw/improved-algs-lbs2.pdf).
The ACC theorem is an instantiation; an isolated speedup for `k`-CNF or one
circuit-size exponent is not.

**KNOWN — threshold SAT boundaries.** Sparse depth-two threshold circuits
admit nontrivial SAT algorithms; Tamaki gives deterministic #SAT with a
superpolynomial saving for `m=O(n^2/log^b n)` SYM/THR gates for sufficiently
large fixed `b`.  Source:
[ECCC TR16-100](https://eccc.weizmann.ac.il/report/2016/100/).  Exact #SAT for
a single degree-`k` PTF is also known in
`poly(n,M)2^{n-tilde Omega(n^{1/(k+1)})}` time; therefore “nontrivial SAT for
one quadratic PTF” is a stale open problem.  Source: Bajpai et al.,
[*A #SAT Algorithm for Small Constant-Depth Circuits with PTF Gates*](https://vaibhkrishan.github.io/files/pdf/ptf-journal.pdf).

## 4. Hardness, randomness, and algebraic bridges

**KNOWN — hardness versus randomness.** If some language in
`E=DTIME(2^{O(n)})` has circuit complexity `2^{Omega(n)}`, then `P=BPP`.
The construction converts worst-case hardness to a pseudorandom generator;
the hypothesis is an explicit uniform language with exponential nonuniform
hardness, not Shannon counting.  Source: Impagliazzo--Wigderson,
[*P=BPP if E Requires Exponential Circuits*](https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/IW97/proc.pdf).

**KNOWN — PIT derandomization bridge.** Deterministic polynomial-time PIT for
integer arithmetic circuits (indeed the weaker infinitely-often
nondeterministic subexponential hypothesis in the paper) implies either
`NEXP not subseteq P/poly` or that permanent has no polynomial-size
arithmetic circuits.  Source: Kabanets--Impagliazzo,
[*Derandomizing Polynomial Identity Tests Means Proving Circuit Lower Bounds*](https://www.cs.sfu.ca/~kabanets/Research/poly.html).
This is a disjunction and is about arithmetic PIT.

**KNOWN — restricted algebraic lower bounds.** Nisan proves exponential
noncommutative formula/ABP lower bounds by coefficient-matrix rank
([STOC 1991](https://doi.org/10.1145/103418.103462)).  Raz proves
`n^{Omega(log n)}` multilinear-formula lower bounds for both permanent and
determinant
([ECCC TR03-067](https://eccc.weizmann.ac.il/report/2003/067/)).  Since
determinant is in VP, the multilinear restriction is indispensable and the
result does not separate VP from VNP.

**KNOWN — IPS bridge.** A superpolynomial Ideal Proof System lower bound for
any family of Boolean tautologies implies `VP != VNP`; a superpolynomial
lower bound on Polynomial Calculus lines implies the
Permanent-versus-Determinant conjecture.  Source: Grochow--Pitassi,
[*Circuit Complexity, Proof Complexity, and Polynomial Identity Testing: The Ideal Proof System*](https://www.cs.toronto.edu/~toni/Papers/jacm-gp.pdf).
These implications make general IPS/PC lower bounds at least as hard as major
algebraic lower bounds.

**KNOWN — balanced-chain frontier.** For even `n`, let `N(n)` be the minimum
size of a set system containing, for every balanced `+/-1` coloring, a
maximal chain whose every prefix has imbalance at most one.  Fabris--Limaye--
Srinivasan--Yehudayoff prove

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`

and connect balanced-chain systems to full-rank multilinear ABPs and the
min-partition-rank method.  More exactly, their Theorem 5.6 says that an
`l`-balanced system `X` yields, over every infinite field, a nonuniform
`n`-variate full-rank multilinear polynomial computed by an mABP of size at
most `|X|*binom(n,<=l)`.  Thus a size-`n^C` 1-balanced system would give size
`O(n^{C+1})`; this is a limitation of full min-partition rank, not an mABP
separation.  The correspondence is tight in the set-multilinear setting and
has a balance-parameter asymmetry for general mABPs.  The official
proceedings source is Fabris--Limaye--Srinivasan--Yehudayoff, CCC 2026,
LIPIcs 383, Article 22,
[DOI 10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22).
The fuller source is
[ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/), especially
Theorems 1.3 and 5.4--5.6.
A claimed polynomial upper bound in TR26-043 was withdrawn after a fatal
conditional-probability gap; it is not a known theorem
([official notice](https://eccc.weizmann.ac.il/report/2026/043/)).

**KNOWN — interval-family average-case upper bound.**  FLSY Definition 2.1
lets `I_(N,1)` contain the empty set and every ordinary interval of `[N]`.
Their Theorem 4.4 (Theorem 1.7) gives a universal `c>0` such that, for all
sufficiently large even `N`, its probability of containing a 1-balanced
maximal chain for a uniformly random balanced coloring is at most
`2^(-cN^(1/5))`.  The same paper's Lemma 2.3 (Lemma 1.5) is the
worst-case-to-average-case random-relabeling lemma.  Cycle 4 derives, via an
independently checked rooted complement/reversal bijection, the restricted
corollary

`A_n(RR_n) <= (n/2)2^(-c(n-2)^(1/5))`.

The FLSY interval estimate and symmetrization are known; the RR corollary is
an internal derived connection with no novelty claim.  It obstructs only
individual-copy RR acceptance and does not control hybrid chains in literal
unions of several copies.  See
[`research_cycle_04/literature_novelty_audit.md`](../research_cycle_04/literature_novelty_audit.md).

## 5. Proof complexity

**KNOWN — Cook--Reckhow baseline.** A propositional proof system is a
polynomial-time computable onto map to TAUT.  TAUT has a polynomially bounded
proof system iff `NP=coNP`.  A lower bound for one restricted proof system is
therefore not enough.  Source: Cook--Reckhow,
[*The Relative Efficiency of Propositional Proof Systems*](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf).

**KNOWN — Resolution.** Pigeonhole formulas require exponential Resolution
length (Haken,
[*The Intractability of Resolution*](https://doi.org/10.1016/0304-3975(85)90144-6)).
For an unsatisfiable CNF on `n` variables with initial width `w_0`, minimum
refutation width `W` implies length
`exp(Omega((W-w_0)^2/n))`; conversely a length-`S` proof can be narrowed to
`w_0+O(sqrt(n log S))`.  Enumerating width-`w` clauses gives
`n^{O(w)}` proof search.  Source: Ben-Sasson--Wigderson,
[*Short Proofs Are Narrow*](https://doi.org/10.1145/375827.375835).
Strong automatization of Resolution is NP-hard; weak automatizability remains
open and is equivalent to feasible interpolation for `Res(2)`.  Sources:
[Atserias--Muller](https://arxiv.org/abs/1904.02991),
[Atserias--Bonet](https://eccc.weizmann.ac.il/report/2002/010/).

**KNOWN/OPEN — Frege boundary.** Fixed-depth Frege has exponential lower
bounds for explicit pigeonhole/Tseitin families using switching restrictions.
No superpolynomial lower bound is known for unrestricted Frege or Extended
Frege, and no such bound is known for `AC^0[p]`-Frege for any fixed prime
`p`.  Recent
primary confirmation: [ECCC TR26-018](https://eccc.weizmann.ac.il/report/2026/018/).

**KNOWN — Cutting Planes space.** General Cutting Planes has inequality-
space-five refutations of every unsatisfiable system of integral linear
inequalities over Boolean variables, with the Boolean axioms, using very
large coefficients.  In `CP_k`, every variable coefficient (not the right-
hand constant) in every proof line has absolute value at most fixed `k`.
The complete-tree contradiction `CT_n` needs
`Omega(log log log n)` inequality space.  `CP_2` nevertheless has space-five
proofs of PHP.  Source: Galesi--Pudlak--Thapen,
[*The Space Complexity of Cutting Planes Refutations*](https://users.math.cas.cz/~thapen/CP_constant_space.pdf).

**KNOWN — Polynomial Calculus.** A PCR proof of monomial size `S` for a
`k`-CNF on `n` variables can be transformed to degree
`k+O(sqrt(n log S))`; degree-`d` search is linear algebra in `n^{O(d)}`
time.  Sources:
[Clegg--Edmonds--Impagliazzo](https://doi.org/10.1145/237814.237860),
[Impagliazzo--Pudlak--Sgall](https://doi.org/10.1007/s000370050024).
For suitable expander Tseitin formulas after two-variable XOR substitution,
Resolution width yields linear PCR monomial space; for simple low-vertex-
degree expanders the best located direct bound is only `Omega(sqrt n)`, while
sufficiently large constant vertex degree reaches `Omega(n/log n)`.  Source:
Filmus et al.,
[*Towards an Understanding of Polynomial Calculus*](https://theoryofcomputing.org/articles/v021a004/v021a004.pdf)
(2025).

**KNOWN — Res(`oplus`) boundary.** Exponential size lower bounds are known for
tree-like and regular restrictions.  For general DAG proofs, recent work gives
a depth tradeoff, an unconditional `Omega(w^2)` size bound in its parameters,
and superpolynomial lower bounds through a stated
`o(n^2/log^4 n)`-depth regime; it does not give exponential bounds throughout
the nearly quadratic range.  No superpolynomial lower bound is known for
unrestricted dag-like Res(`oplus`), the weakest currently identified fragment
of `AC^0[2]`-Frege with this status.  Sources:
[ECCC TR24-128](https://eccc.weizmann.ac.il/report/2024/128/),
[ECCC TR25-106](https://eccc.weizmann.ac.il/report/2025/106/), and
[ECCC TR26-018](https://eccc.weizmann.ac.il/report/2026/018/).

## 6. Meta-complexity and hardness magnification

**KNOWN — exact hypotheses magnify.** Slight lower bounds for precisely
parameterized approximate/gap MCSP or MKtP variants magnify to NP/EXP formula,
circuit, branching-program, or low-depth lower bounds.  The promise gap,
threshold, model, exponent, and quantifier “for all sufficiently small beta”
are part of each theorem.  Sources: Oliveira--Santhanam,
[*Hardness Magnification for Natural Problems*](https://eccc.weizmann.ac.il/report/2018/139/);
Oliveira--Pich--Santhanam,
[*Hardness Magnification near State-of-the-Art Lower Bounds*](https://www.theoryofcomputing.org/articles/v017a011/v017a011.pdf).
Unconditional bounds for wider gaps or different thresholds do not instantiate
these premises.

**KNOWN — locality barrier.** Search-MCSP has small circuits and streaming
algorithms augmented with short SAT-like oracle gates.  Many magnification
targets likewise have upper bounds with a few low-fan-in arbitrary oracle
gates, so a lower-bound method that remains valid after those gates are added
cannot prove the desired premise.  This is a method/target-specific locality
barrier, not an impossibility theorem for magnification.  Sources:
[McKay--Murray--Williams](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf),
[Chen et al.](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70).

**KNOWN — unconditional all-threshold MCSP bounds.** Let
`MCSP={(x,theta): CC(x)<=theta}`, where `x` is an `N`-bit truth table and the
threshold is part of the input.  This total language requires De Morgan
formula size
`N^3/2^{O(log^{2/3}N)}` and arbitrary-basis formula and deterministic
branching-program size `N^2/2^{O(sqrt(log N))}`.  The method uses local PRGs
whose outputs are truth tables of small circuits.  Source: Cheraghchi et al.,
[*Circuit Lower Bounds for MCSP from Local Pseudorandom Generators*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.39/LIPIcs.ICALP.2019.39.pdf).

**KNOWN — MKTP is not MCSP.** MKTP has deterministic branching-program lower
bound `Omega(N^2/log^2 N)`.  For standard MCSP the same paper proves only
`N^{3/2-o(1)}` for nondeterministic, co-nondeterministic, and parity branching
programs and explicitly says the Nechiporuk argument does not transfer to
deterministic MCSP because the circuit-size/`KT` relation loses too much.
Source: Cheraghchi et al.,
[*One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf).

**KNOWN/OPEN — hardness and cryptography.** Standard total MCSP and MKTP are
in NP; unconditional ordinary NP-completeness was not established by the
sources checked.  Results for partial/implicit variants or randomized/Turing
reductions do not change that status.  One-way functions are characterized by
average-case hardness of particular time-bounded Kolmogorov problems, and by
gapped MCSP under an existential locally samplable distribution; neither is a
uniform-random-total-MCSP theorem.  Sources:
[Liu--Pass](https://arxiv.org/pdf/2009.11514),
[Ren--Santhanam](https://drops.dagstuhl.de/opus/volltexte/2021/14309/pdf/LIPIcs-CCC-2021-35.pdf),
[Ilango--Ren--Santhanam](https://hanlin-ren.github.io/files/pdf/stoc22_robustness.pdf).

## 7. Freshness and negative-result ledger

1. **Single quadratic PTF SAT:** already known; rejected as an open target.
2. **`n^{2.001}` `THR o THR` lower bound for an `E^NP` function:** already
   subsumed by CTW 2026; rejected.
3. **`n^{5/2}/polylog n` CTW reparameterization:** `UNKNOWN-STATUS`.
   Displayed terms look compatible for a sufficiently large logarithmic
   exponent, but the theorem fixes constant `epsilon` and hidden dependence
   has not been uniformized.
4. **`N(n)=poly(n)` balanced chains:** OPEN.  The only exact claimed theorem
   was withdrawn; stale mirrors of its abstract are not evidence.
5. **`2^{n^{Omega(1)}}` monotone perfect-matching lower bound:** already
   known; the unresolved target must ask for `2^{Omega(n)}`.
6. **`Omega(N^2/log^2 N)` deterministic BP lower bound for MCSP:** not known
   from the matching MKTP theorem; the source expressly records the failed
   transfer.
7. **Alekseev--Gaevoy affine-union robustness conjecture:** false as written
   according to an internally adversarially reviewed parametric proof and
   blinded re-derivation.  The result is `UNFORMALIZED`, not externally peer
   reviewed or novelty-audited.  It does not refute the paper's unconditional
   proof-complexity results.

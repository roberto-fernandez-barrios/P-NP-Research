# Integration notes for research cycle 1

Date checked: 2026-08-13.

This is a working evidence ledger for Phase 0/1.  It is retained because stale
open-problem statements and failed target classifications are research data.

## Freshness corrections and negative findings

### A single degree-2 PTF does **not** remain an open nontrivial-SAT target

Kabanets and Lu (2018) explicitly called a nontrivial SAT algorithm for even one
degree-2 polynomial threshold function (PTF) open.  That statement is now stale.
Bajpai, Krishan, Kush, Limaye, and Srinivasan give:

* a deterministic exact #SAT algorithm for a single degree-`k` PTF in
  `poly(n,M) 2^{n-\widetilde{\Omega}(n^{1/(k+1)})}` time; and
* a zero-error randomized exact #SAT algorithm with saving
  `\widetilde{\Omega}(n^{1/k})`, as well as an algorithm for slightly
  superlinear-size, constant-depth `k`-PTF circuits.

For `k=2`, their journal version also records that Williams's earlier results
imply deterministic `2^{n-\Omega(\sqrt n)}`-time satisfiability.  Therefore the
unqualified target "beat brute force for a single quadratic PTF" is **KNOWN**,
not open.

Primary sources:

* Valentine Kabanets and Zhenjian Lu, *Satisfiability and Derandomization for
  Small Polynomial Threshold Circuits*, ECCC TR18-115 (2018), open-problem
  statement: <https://eccc.weizmann.ac.il/report/2018/115/>.
* Swapnam Bajpai, Vaibhav Krishan, Deepanshu Kush, Nutan Limaye, and Srikanth
  Srinivasan, *A #SAT Algorithm for Small Constant-Depth Circuits with PTF
  Gates*, Algorithmica 84 (2022), 1132--1162:
  <https://vaibhkrishan.github.io/files/pdf/ptf-journal.pdf>.

### The pre-2026 subquadratic THR o THR frontier is stale

Chen, Tal, and Wang prove that for every constant `epsilon in (0,1)` there is a
function in `E^NP` requiring more than `n^{2.5-epsilon}` gates in depth-two
`THR o THR` circuits (also `SYM o THR`).  Their engine is a deterministic
`2^{n-n^{Omega(epsilon)}}`-time, additive-`o(1)` CAPP algorithm for the XOR of
two such circuits.  Thus targets asking merely for an `n^{2.001}` lower bound or
nontrivial analysis of superquadratic `THR o THR` circuits are **KNOWN**.

Primary source:

* Lijie Chen, Avishay Tal, and Yichuan Wang, *Super-quadratic Lower Bounds for
  Depth-2 Linear Threshold Circuits*, ECCC TR26-039 (15 March 2026), Theorems
  1.1 and 1.2: <https://eccc.weizmann.ac.il/report/2026/039/>.

### Additive approximate counting is not exact SAT

De, Diakonikolas, and Servedio deterministically approximate the acceptance
probability of a degree-2 PTF to additive error `epsilon` in
`poly(n,2^{poly(1/epsilon)})` time.  Since deciding whether the acceptance
probability is nonzero is already NP-hard, this does not settle exact SAT or
multiplicative counting.  Any frontier statement must keep these tasks apart.

Primary source:

* Anindya De, Ilias Diakonikolas, and Rocco A. Servedio, *Deterministic
  Approximate Counting for Degree-2 Polynomial Threshold Functions*, ECCC
  TR13-172: <https://eccc.weizmann.ac.il/report/2013/172/>.

## Verified bridge results for later integration

* **Hardness to BPP derandomization.** If some language in
  `E = DTIME(2^{O(n)})` has Boolean circuit complexity `2^{Omega(n)}`, then
  `P=BPP`.  Source: Russell Impagliazzo and Avi Wigderson, *P=BPP if E Requires
  Exponential Circuits*, STOC 1997, pp. 220--229:
  <https://www.math.ias.edu/~avi/PUBLICATIONS/MYPAPERS/IW97/proc.pdf>.
* **PIT derandomization to lower bounds.** If integer arithmetic-circuit PIT is
  in P (indeed under the weaker infinitely-often nondeterministic
  subexponential hypothesis in the paper), then either `NEXP` is not contained
  in `P/poly` or the permanent has no polynomial-size arithmetic circuits.
  Source: Valentine Kabanets and Russell Impagliazzo, *Derandomizing
  Polynomial Identity Tests Means Proving Circuit Lower Bounds*, Computational
  Complexity 13 (2004), 1--46:
  <https://www.cs.sfu.ca/~kabanets/Research/poly.html>.
* **IPS bridge.** A superpolynomial IPS lower bound for any family of Boolean
  tautologies implies `VP != VNP`; a superpolynomial lower bound on the number
  of Polynomial Calculus lines implies the Permanent-versus-Determinant
  conjecture.  Source: Joshua A. Grochow and Toniann Pitassi, *Circuit
  Complexity, Proof Complexity, and Polynomial Identity Testing: The Ideal
  Proof System*, JACM 65(6), 2018:
  <https://www.cs.toronto.edu/~toni/Papers/jacm-gp.pdf>.
* **Restricted algebraic lower bounds do not separate VP from VNP.** Raz proved
  `n^{Omega(log n)}` lower bounds for multilinear formulas computing both the
  permanent and determinant.  Because determinant is in VP, the restriction is
  essential.  Source: Ran Raz, *Multi-Linear Formulas for Permanent and
  Determinant Are of Super-Polynomial Size*, JACM 56(2), 2009; ECCC TR03-067:
  <https://eccc.weizmann.ac.il/report/2003/067/>.

## Candidate fresh boundary after independent verification

A quantitatively minimal extension of the March 2026 threshold result is:

> For some constant `C`, give a deterministic `2^n/n^{omega(1)}`-time
> additive-`o(1)` CAPP algorithm for
> `XOR_2 o THR o THR` circuits with at most
> `n^{5/2}/(log n)^C` gates (with explicitly encoded polynomial-bit integer
> weights).

The checked theorem covers `n^{2.5-epsilon}` for every fixed positive epsilon,
not the near-critical `n^{2.5}/polylog(n)` regime.  An independent line-by-line
parameter audit found that the displayed terms plausibly tolerate
`epsilon(n)=Theta(log log n/log n)` for a sufficiently large constant in the
polylogarithmic denominator.  However, the paper declares `epsilon` a global
constant, contains hidden `epsilon`-dependent constants and sufficiently-large-
`n` thresholds, and no follow-up states the uniform theorem.  Therefore the
correct classification is **UNKNOWN-STATUS**, not OPEN and not KNOWN.  It was
excluded from the 25 ranked open targets.  See
[`circuits_barriers.md`](circuits_barriers.md#61-can-ctws-fixed-epsilon-be-made-epsilonn-theta-log-log-nlog-n).

## Withdrawn balanced-chain claim

Fabris--Limaye--Srinivasan--Yehudayoff prove only
`Omega(n^2)<=N(n)<=n^{O(log n/log log n)}` for 1-balanced-chain set systems.
TR26-043's claimed polynomial upper bound is withdrawn: its official notice
says the forced-probability estimate is not valid conditional on the needed
filtration and every result relies on it.  An independent internal audit
additionally finds a positive-probability `n=10` history with `p_t=2/7>1/4`
and shows that the separate block-deviation martingale also fails.  This is
an adversarially reviewed exact check but remains `UNFORMALIZED` and is not an
external publication claim.  The general polynomial existence statement
remains **OPEN** and is the selected first target; the withdrawn construction
is only the first repair-or-obstruction diagnostic.

Sources and audits:

* FLSY, [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/);
* [official TR26-043 withdrawal/gap notice](https://eccc.weizmann.ac.il/report/2026/043/);
* [`../../audits/cross_validation_proof_sat.md`](../../audits/cross_validation_proof_sat.md).

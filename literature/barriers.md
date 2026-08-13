# Barrier catalogue

**Audit date:** 2026-08-13.  A barrier below limits a specified proof
invariance or method class.  It is not a claim that the underlying lower bound
is false or unprovable by every method.

## 1. Relativization

**Theorem (Baker--Gill--Solovay, KNOWN).** There are recursive oracles `A`
and `B` with `P^A=NP^A` and `P^B != NP^B`.  A proof that remains valid
relative to every oracle therefore cannot settle unrelativized P versus NP.
Source: [*Relativizations of the P=?NP Question*](https://doi.org/10.1137/0204037).

**Exact scope.** The theorem rules out a wholly relativizing resolution of a
claim having opposite oracle worlds.  It does not ban diagonalization,
simulation, or oracle arguments as ingredients.  An argument is not shown to
relativize merely because it resembles a classical relativizing proof.

**Audit question.** Identify every semantic step and ask whether the claimed
simulation, counting, or reduction still holds with a common arbitrary oracle.

## 2. Natural proofs

**Definitions (Razborov--Rudich, KNOWN).** A property of `n`-variable truth
tables is:

* constructive if membership is decidable in time polynomial in the
  `2^n`-bit truth table;
* large if it holds on at least a `2^{-O(n)}` fraction of functions; and
* useful against `P/poly` if no polynomial-size circuit family possesses it
  infinitely often.

Under the paper's strong pseudorandom-function/generator hypothesis, no
P-constructive, large property is useful against `P/poly`.  The property
would distinguish pseudorandom truth tables from random ones.  The same paper
gives an unconditional restricted statement: no `AC^0`-natural property is
useful against `AC^0[2]`.  Source: Razborov--Rudich,
[*Natural Proofs*](https://doi.org/10.1006/jcss.1997.1494).

**Exact scope.** The main barrier is conditional.  It does not rule out a
property that is nonconstructive, not large, or not useful in the formal
sense.  It is not a direct barrier to monotone lower bounds, and “uses a
simple combinatorial property” is not a substitute for checking all three
conditions.

**Audit question.** State the truth-table algorithm, density, and usefulness
quantifiers.  If all hold, state exactly which pseudorandomness assumption is
contradicted.

## 3. Algebrization

**Theorem (Aaronson--Wigderson, KNOWN).** Algebrization gives machines access
to an oracle and to its low-degree extension.  The paper constructs algebraic
oracle worlds with opposite behavior for P versus NP and shows that several
major lower-bound goals, including the relevant formulations of
`NEXP not subseteq P/poly`, need nonalgebrizing techniques.  Source:
[*Algebrization: A New Barrier in Complexity Theory*](https://doi.org/10.1145/1490270.1490272).

**Exact scope.** “Algebraic” does not mean “algebrizing.”  Polynomial
identity testing, arithmetization, or algebraic geometry may participate in a
nonalgebrizing proof.  The exact asymmetric access to the oracle extension
must be checked.

## 4. Explicitness and nonuniformity

**Counting gap.** Shannon counting proves that almost all functions require
`Theta(2^n/n)` circuits but gives no named function in P or NP.  Turning an
existential truth table into a uniform family is the missing step; advice may
encode an uncomputable choice.

**`P/poly` gap.** Nonuniform circuit existence does not provide a uniform
algorithm, and `P/poly` contains undecidable tally languages.  Conversely, a
uniform lower bound (for example permanent versus uniform threshold circuits)
does not automatically hold nonuniformly.  Karp--Lipton gives a conditional
PH collapse from `NP subseteq P/poly`, not a proof that the containment fails.

**Quantifier gap.** Kannan's result is `for every k, there exists L_k`; it is
not `there exists L, for every k`.  The latter swap would manufacture a
lower bound outside `P/poly`.

## 5. Restricted-model transfer

Lower bounds are monotone in the *wrong* direction for many informal
arguments: hardness for a restricted model says nothing about a stronger
model unless a simulation/reduction is proved.  Current recurring hazards are:

* `U_2` versus full `B_2` gates;
* monotone versus ordinary circuits with negations;
* uniform versus nonuniform `TC^0`;
* `AC^0[p]` with one characteristic versus mixed-modulus `ACC^0`;
* multilinear formulas versus general arithmetic formulas/ABPs;
* tree-like, regular, or depth-bounded Res(`oplus`) versus unrestricted
  dag-like Res(`oplus`);
* formula, Formula-XOR, probabilistic formula, circuit, wire, and
  branching-program measures;
* total MCSP versus promise/partial/implicit MCSP, MKTP, or MKtP.

Every edge of this kind is absent by default.  It must be supplied by a cited
simulation with matching parameters.

## 6. Local gate-elimination limits

Golovnev--Hirsch--Knop--Kulikov formalize broad fixed-`m` gate-elimination
schemes based on assigning a bounded number of inputs and using a standard
subadditive complexity measure.  They construct functions/circuits for which
the measure drops by only `O_m(1)`, preventing a superlinear result from that
local template.  Source:
[*On the Limits of Gate Elimination*](https://doi.org/10.4230/LIPIcs.MFCS.2016.46).

**Escape routes not excluded:** function-specific global amortization,
weighted or nonstandard measures, growing restrictions, and structural
information.  Li--Yang's improved linear constant is consistent with this
scope.

## 7. Approximation-method limits

Razborov proves limitations for a formal class of circuit-approximation
arguments without auxiliary variables; in the source's measure the bound is
controlled by the number of essential variables.  Adding sufficiently many
auxiliary variables changes the formal power.  Source:
[*Unprovability of Lower Bounds on Circuit Size in Certain Fragments of Bounded Arithmetic*](https://people.cs.uchicago.edu/~razborov/files/approx.pdf).

This is not a theorem that all approximation arguments fail.  The
approximator class, auxiliary information, and conclusion must match the
formal barrier.

## 8. Hardness-magnification locality

Many magnification problems have efficient circuits when augmented with a
small number of low-fan-in arbitrary oracle gates.  A proof method that
*localizes*—continues to prove the same lower bound after these gates are
added—would contradict the upper bound before reaching the magnification
threshold.  Search-MCSP also has small uniform circuits and streaming
algorithms with short SAT-like oracle queries.  Sources:

* Chen et al.,
  [*Beyond Natural Proofs: Hardness Magnification and Locality*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITCS.2020.70);
* McKay--Murray--Williams,
  [*Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations*](https://people.csail.mit.edu/~rrw/MCSP-MKTP-stoc19.pdf).

**Exact scope.** Locality is relative to the target syntax, oracle fan-in,
number/adaptivity of queries, and proof method.  It does not show the target
statement is false.  A nonlocal measure may remain viable.

## 9. Magnification parameter mismatch

Hardness magnification is a theorem only at its exact interface.  The
following changes can destroy the implication:

* replacing a narrow promise gap by a wider known gap;
* changing the circuit-complexity threshold;
* replacing worst-case by average-case or changing the distribution;
* replacing MCSP by `KT`/`Kt` minimization;
* changing deterministic to probabilistic, formula to circuit, or gate to
  wire complexity;
* dropping “for all sufficiently small beta,” uniformity, or infinitely-/
  almost-everywhere qualifiers.

The Oliveira--Santhanam and Oliveira--Pich--Santhanam theorems are therefore
recorded as typed implications, not slogans.  Present unconditional bounds
usually miss their premises along at least one of these axes.

## 10. Algorithm-to-lower-bound interface

Williams-type implications require a **uniform** nontrivial SAT/CAPP algorithm
for every fixed polynomial size in a constructible class with the specified
closure (often an XOR/OR closure).  Common invalid substitutions are:

* an algorithm for only one size exponent;
* a heuristic or average-case speedup;
* additive approximate counting when exact satisfiability is needed;
* all-input evaluation with no saving over `2^n`;
* a class not closed under the combination used by the hierarchy proof; or
* a nonuniform existence assertion in place of an algorithm.

The ACC lower bound succeeds because its algorithm and representation meet
the full interface.  Threshold-circuit results must be checked individually.

## 11. Proof-complexity implication limits

* A lower bound for one Cook--Reckhow system does not imply `NP != coNP`.
* Proof size, degree/width, monomial space, inequality space, bit size, and
  automatizability are different resources.  Known tradeoffs include losses.
* Strong Resolution automatizability is NP-hard, while weak automatizability
  remains open; they cannot be conflated.
* Feasible interpolation yields circuit lower bounds only for systems and
  formula partitions satisfying its hypotheses.
* General IPS/Polynomial-Calculus lower bounds encounter algebraic circuit
  barriers: the cited IPS implications reach `VP != VNP` or
  Permanent-versus-Determinant.
* Bounded-depth Frege lower bounds do not converge automatically to
  unrestricted Frege as depth grows; the constants and restrictions depend
  on fixed depth.

## 12. Fresh method barriers and failed claims

### Balanced-chain min-partition rank claim

TR26-043 claimed polynomial-size 1-balanced-chain systems and hence an
unconditional min-partition-rank barrier for multilinear ABPs.  It was
withdrawn.  The official notice says the needed conditional forced-
probability estimate was only shown unconditionally and every main result
depends on it.  An independent internal audit found an explicit positive-probability
`n=10` history with conditional upward probability `2/7>1/4`; the same
history falsifies the separate block-deviation martingale claim.  This exact
counterhistory is adversarially reviewed within this cycle but
`UNFORMALIZED`, not an external publication claim.  Sources:
[official ECCC notice](https://eccc.weizmann.ac.il/report/2026/043/),
[`../audits/cross_validation_proof_sat.md`](../audits/cross_validation_proof_sat.md).

**Status:** the two proof lemmas are false as stated; the general polynomial
existence question remains OPEN.  There is currently no established
min-partition-rank barrier of the claimed strength.

### Affine-union robustness claim

Alekseev--Gaevoy Conjecture 1.4/4.2 allows arbitrary dense subsets of many
low-codimension affine subspaces and asserts that their union remains nearly
as large.  Internal coordinate-middle-layer/private-fiber constructions
refute the quantified statement for every fixed `q>1,r>0`, even with
polynomially many subspaces.  The two independently derived internal proofs
and finite checks are adversarially reviewed but `UNFORMALIZED`, not
externally peer reviewed or novelty-audited.  They are retained in:

* [`../theory/conjectures/falsified/ag26_affine_union_robustness.md`](../theory/conjectures/falsified/ag26_affine_union_robustness.md);
* [`../audits/eccc_tr26_007_conjecture_audit_meta.md`](../audits/eccc_tr26_007_conjecture_audit_meta.md).

This refutes the conjecture as written, not the paper's unconditional
Res(`oplus`) theorems or every possible structured repair.

## 13. Barrier checklist for future targets

Before promoting a candidate, record:

1. exact model, uniformity, size measure, and asymptotic variable;
2. whether the reasoning relativizes and whether contradictory oracle worlds
   apply;
3. natural-proof constructivity, largeness, and usefulness separately;
4. whether the argument algebrizes under the formal definition;
5. every restricted-to-stronger-model transfer;
6. whether a named local/approximation/rank method barrier matches the method;
7. every promise, threshold, accuracy, distribution, and quantifier in a
   magnification theorem;
8. closure and uniformity prerequisites of an algorithmic lower-bound bridge;
9. whether a hidden lemma is equivalent to or stronger than the desired
   conclusion; and
10. whether the result is only a lower bound for a restricted model.

Passing this checklist is not proof.  It only removes identified invalid
inferences.

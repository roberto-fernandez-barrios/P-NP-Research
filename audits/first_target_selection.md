# First-target selection audit: polynomial balanced-chain systems

**Decision date:** 2026-08-13
**Selected target:** O01, and no other target.
**Current status:** OPEN in the audited public literature.
**Work boundary:** selection and planning only; no Phase 2/3 proof attack has
begun.

## 1. Exact statement

Let `n` be a positive even integer.  A **balanced coloring** is a map
`f:[n]->{+1,-1}` with `sum_x f(x)=0`.  For a set system
`X subseteq P([n])`, a maximal chain is

`emptyset=C_0 subset C_1 subset ... subset C_n=[n]`, with `|C_i|=i`

and every `C_i in X`.  The chain's imbalance under `f` is
`max_i |sum_{x in C_i}f(x)|`.  `X` is **1-balanced-chain** if every balanced
`f` has a maximal chain in `X` of imbalance at most one.  Let `N(n)` be the
minimum size of such an `X`.

> **O01.** Prove that there is an absolute constant `C` such that
> `N(n)<=n^C` for every positive even `n`.

The evenness restriction is part of the statement: a `+/-1` balanced coloring
does not exist for odd `n` under this definition.

## 2. What is known

Fabris, Limaye, Srinivasan, and Yehudayoff (FLSY) prove

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`.

Their upper bound uses returns of a random balanced walk, a recursive gap
filler, and a worst-case-from-average symmetrization.  Their Theorem 1.3
connects balanced-chain systems to full-rank multilinear algebraic branching
programs:

* a constant-balanced system of size `s` yields a full-rank polynomial with
  an mABP of size `s*poly(n)`; and
* a lower bound for systems with a logarithmically larger balance parameter
  yields a full-rank mABP lower bound.

The parameter gap disappears in the set-multilinear version.  These directions
must not be reversed without proof.  Primary source:
[FLSY, ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/),
especially Theorems 1.3 and 1.6, Lemma 1.5, and the further-questions section.

## 3. Why the polynomial claim is not already known

### The only exact claimed solution was withdrawn

TR26-043 v1 claimed `N(n)=n^{O(1)}` using adaptive two-block steering.  On
2026-05-11 the author withdrew it.  The current ECCC record states that the
forced-probability estimate in Lemma 4.1 is valid only unconditionally, not
conditional on the filtration needed by the supermartingale, and that every
result in the paper depends on that lemma.  The arXiv record is explicitly
withdrawn for the same reason:

* [official ECCC revision/gap notice](https://eccc.weizmann.ac.il/report/2026/043/);
* [withdrawn arXiv record](https://arxiv.org/abs/2604.00746).

Metadata sites that repeat the April abstract are stale and were not counted
as independent proofs.

### Independent adversarial check of the withdrawal

A separate internal validator who did not propose the target reconstructed the actual
filtration and found a positive-probability counterhistory at `n=10`.
Split the points into ordered blocks
`A=(a_1,...,a_5)` and `B=(b_1,...,b_5)`.  Condition on

`f(a_1)=f(a_2)=f(b_1)=+1`

and on two tie coins consuming `a_1` and then `a_2`.  At time two the signed
imbalance is two and the unconsumed frontier `b_1` is known to be `+1`.  Of
the other seven positions exactly two are positive.  Hence the conditional
probability that both frontiers increase absolute imbalance is

`p_2=Pr[f(a_3)=+1 | F_2]=2/7>1/4`,

directly falsifying Lemma 4.1.  The same history gives block-deviation
increment probabilities `6/7` and `1/7`, so the separate martingale claim in
Lemma 3.3 also fails.  This counterhistory is adversarially reviewed within
this cycle and exactly checked but remains `UNFORMALIZED`; it is not an
external publication claim.  Repairing only the height potential would leave the
residual-size/Azuma analysis unsupported.  Full independent derivation:
[`cross_validation_proof_sat.md`](cross_validation_proof_sat.md).

### Attempts to reduce the target to older solved results

The audits checked and rejected the following shortcuts:

1. A fixed maximal chain works for exactly `2^(n/2)` signed balanced
   colorings: signs must be opposite within consecutive pairs of its
   permutation, while the orientation of each pair is independent.  Since
   `binom(n,n/2)/2^(n/2)` is still exponential, a polynomial explicit list of
   chains is impossible.  A small set system can share subsets among
   exponentially many chains, so the observation neither proves nor refutes
   O01.
2. Steinitz/rearrangement orders can depend on `f`; taking every possible
   prefix set can be exponential.  O01 requires one fixed small set system
   before `f` is known.
3. A sorting/permutation network state need not encode one particular subset
   of `[n]`; a polynomial network does not automatically give a polynomial
   set system.
4. Dvir--Malod--Perifel--Yehudayoff's polynomial mABPs use full rank for a
   restricted family of arc partitions.  FLSY do not provide a converse that
   turns this into a 1-balanced-chain system.
5. An adaptive algorithm is insufficient unless the union of every subset it
   can output is polynomially bounded.

Exact-title, arXiv-ID, author, `balanced-chain`, `N(n)`, discrepancy,
min-partition-rank, and citing-paper searches through 2026-08-13 found no
corrected version or independent polynomial construction.  Two independent
validators repeated the status audit.  See
[`cross_validation_circuits.md`](cross_validation_circuits.md) and
[`cross_validation_proof_sat.md`](cross_validation_proof_sat.md).

**Conclusion:** O01 is OPEN with high confidence in the public record.  This
is not a claim that no unpublished solution exists.

## 4. Why this target ranks first

O01 is not selected because the withdrawn proof is “almost complete”; it is
not.  It is selected because:

* the exact frontier and the reason the apparent closure fails are unusually
  well documented;
* it is a self-contained finite combinatorial statement with exact
  certificates and small instances;
* positive and negative work both diagnose the power of min-partition rank,
  the only general technique currently producing multilinear lower bounds;
* FLSY provide a valid quasipolynomial construction to dissect;
* discrepancy, adaptive exposure, posterior-state potentials, and recursive
  covering are reusable beyond this one statement; and
* it has no identified collision with relativization, natural proofs, or
  algebrization at the combinatorial level.

The tradeoff is explicit: the target is a polynomial-versus-quasipolynomial
collapse, not a tiny quantitative increment.  Therefore the next cycle is
bounded to a repair-or-obstruction diagnostic before committing to the full
existence proof.

Comparison with the nearest alternatives:

| Alternative | Why not first |
|---|---|
| O03 quadratic disperser | Clean and consequential, but no near construction is known and its asymptotic incidence property is harder to diagnose from small cases. |
| O02 `CP_2` space | More incremental, but `CT_n` has exponentially many clauses and successive iterated logarithms are invisible at feasible sizes; outward connection is weaker. |
| O18 PPSZ improvement | Closest and most formalizable, but likely yields a narrow algorithmic constant rather than a reusable lower-bound technique. |
| O05 strict regular-Resolution simulation | Syntactically clean and reusable, but existing regular-versus-general separations make the missing parameter removal less diagnostically local. |
| O04 MCSP branching programs (first target outside the shortlist) | The desired denominator is close to the best known bound for any explicit function in unrestricted BPs; the MKTP analogy is not a routine transfer. |

## 5. Exact consequence if O01 is true

Combining O01 with FLSY Theorem 5.6 gives the following exact consequence:
over every infinite field there is a nonuniform family of `n`-variate
full-rank multilinear polynomials computed by mABPs of size `O(n^{C+1})`.
It would show that full min-partition rank alone cannot prove
superpolynomial general-mABP lower bounds over those fields.

It would **not** prove:

* `mVBP=mVP`;
* an mABP lower bound;
* a Boolean circuit lower bound;
* `P != NP`; or
* that every rank-based method fails.

It is a lower-bound-method diagnosis, not a complexity separation.

## 6. Falsification-first plan for the next cycle

The first objective is not “prove O01.”  It is:

> Determine whether the withdrawn two-block/multiscale construction admits a
> corrected polynomial-state analysis, or prove a precisely delimited
> obstruction for that construction family.

Work packages, in order:

1. **Exact process model.** Encode the full filtration: revealed values,
   inspected-but-unconsumed frontiers, tie coins, scale transitions, and the
   fixed set system containing every reachable subset.
2. **Smallest counterhistories.** Exhaust balanced colorings and coin histories
   for small even `n`; independently verify whether `n=10` is the smallest
   violation of each posted martingale inequality.  Retain certificates.
3. **Exact small `N(n)`.** Formulate a set-cover/SAT/ILP model.  A candidate
   set family covers a coloring when it contains all prefixes of at least one
   alternating permutation for that coloring.  Use complement/permutation
   symmetry and column generation; verify every claimed optimum with a small
   independent checker.
4. **Attack repair proposals.** Test enlarged posterior-state potentials,
   fresh/nonadaptive exposures, `d>2` blocks, and deterministic recursion.
   Reject a proposal as soon as conditional drift, frequent-return tails, or
   total set-system size fails.
5. **Restricted obstruction.** Try to construct colorings forcing every
   fixed two-block/bounded-block recursion template to expose
   superpolynomially many distinct subsets.  Such a theorem is useful but
   must be labeled a method obstruction, not a lower bound on unrestricted
   `N(n)`.

Survival of finite search is not evidence of the asymptotic theorem.

## 7. Proof program if the diagnostic survives

Four plausible routes remain, none currently a proof candidate:

1. **Posterior-state supermartingale.** Track not only absolute imbalance but
   the conditional composition/status of every inspected frontier.  Prove the
   one-step inequality on the actual filtration, then stopping-time and
   excursion bounds.
2. **Nonadaptive exchangeability.** Draw all block permutations independently
   of revealed values and restrict adaptive choices so the next candidates
   remain conditionally exchangeable.  Prove separately that the fixed union
   of all possible output subsets stays polynomial.
3. **Long-horizon domination.** Allow locally positive drift but prove an
   excursion-level likelihood-ratio or hypergeometric domination theorem.
   This must also control block deviation/residual size; fixing only height is
   insufficient.
4. **Deterministic recursive cover.** Abandon stochastic steering and build a
   polynomial family of chain states with a deterministic discrepancy
   guarantee.

Every positive route has three simultaneous proof obligations:

* success for a noticeable fraction of random balanced colorings;
* one fixed set system independent of the coloring; and
* polynomial total size after the FLSY worst-case symmetrization.

An adaptive algorithm with superpolynomially many possible intermediate sets
does not meet O01.

## 8. Computational and Lean verification plan

### Computational artifacts

* A canonical JSON/text certificate for a balanced coloring, coin history,
  reached states, and conditional transition counts.
* An independent checker that never calls the search routine.
* Exact rational arithmetic for probabilities; no floating-point threshold
  decisions.
* A SAT/ILP certificate format for a candidate set system and a separate
  exhaustive verifier for every coloring/chain.
* Symmetry reductions proved before use and cross-checked on unsymmetrized
  tiny instances.

### Lean 4 order of work

1. finite sets, balanced colorings, maximal chains, imbalance, and `N(n)`;
2. validity of positive/negative finite certificates;
3. the FLSY worst-case-from-average symmetrization lemma, with its
   probabilistic existence step clearly isolated;
4. the exact two-block transition system and the finite `n=10`
   counterhistory;
5. only then, any new conditional-expectation inequality, stopping-time
   theorem, and multiscale recurrence.

Formalizing the finite core does not formally verify FLSY or O01.  Coverage is
tracked in [`../formal/coverage.md`](../formal/coverage.md).

## 9. Barrier audit

* **Relativization:** not directly applicable to the finite combinatorial
  existence statement; any claimed downstream complexity consequence must be
  audited separately.
* **Natural proofs:** O01 is an upper-bound construction/method-barrier
  question, not a large constructive property useful against `P/poly`.
* **Algebrization:** no oracle low-degree-extension invariance is being used.
* **Locality:** the immediate obstruction is adaptive conditioning, not the
  MCSP locality barrier.
* **Hidden strength:** a proof must not assume a polynomial list of chains,
  a polynomial number of adaptive states, or a derandomized family of
  permutations; each is essentially part of the desired construction.
* **Restricted model:** even a positive result diagnoses min-partition rank
  for multilinear ABPs.  It is not a general arithmetic/Boolean lower bound.

## 10. Next-cycle stopping rule

Stop and reassess after achieving one of:

1. a checked smallest counterhistory plus a proved obstruction for a precise
   two-/bounded-block construction class;
2. a corrected conditional potential with all stopping-time and polynomial-
   state accounting proved; or
3. a nonadaptive construction with a proved polynomial bound on every subset
   it can generate.

Do not branch into P versus NP, do not call a construction repair a proof of
O01, and do not call a restricted obstruction a lower bound on `N(n)`.

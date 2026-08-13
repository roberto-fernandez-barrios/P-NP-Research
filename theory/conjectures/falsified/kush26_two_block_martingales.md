# Counterhistory to the withdrawn two-block martingale claims

## External claims

Version 1 of Deepanshu Kush, *An Unconditional Barrier for Proving
Multilinear Algebraic Branching Program Lower Bounds* (ECCC TR26-043, 2026),
claimed in Lemma 4.1 that the conditional probability of increasing the
absolute imbalance in its adaptive two-block process is at most `1/4`.  Lemma
3.3 claimed that the difference between the numbers consumed from the two
blocks is a martingale.  The author withdrew the paper after a referee found
the first conditional-probability gap; the official notice says all main
results rely on it.

Primary status sources:

* [ECCC revision notice](https://eccc.weizmann.ac.il/report/2026/043/);
* [withdrawn arXiv record](https://arxiv.org/abs/2604.00746).

## Classification

**Both lemmas are FALSE AS STATED for the actual adaptive filtration.**  This
does not refute the general polynomial balanced-chain existence question.

Epistemic history (2026-08-13): `IDEA -> CONJECTURE` (the assertion that an
explicit counterhistory exists) `-> COMPUTATIONALLY TESTED -> PROOF CANDIDATE
-> ADVERSARIALLY REVIEWED`.  The history was derived independently during a
cross-track audit, checked algebraically by the root integrator, and verified
by exact enumeration.  No novelty claim is made; the paper was already
officially withdrawn for the principal conditioning issue.  The result
remains `UNFORMALIZED` and is not an external publication claim.

## Exact positive-probability history

Take `n=10`, with ordered blocks

`A=(a_1,...,a_5)` and `B=(b_1,...,b_5)`.

Condition a uniformly random balanced coloring on

`f(a_1)=f(a_2)=f(b_1)=+1`

and condition the first two fair tie coins to consume `a_1` and then `a_2`.
This event has positive probability.  At time two the signed imbalance is two
and the unconsumed frontier `b_1` is already known to be positive.  Among the
other seven positions exactly two are positive.  Therefore

`Pr[absolute imbalance increases | F_2]=Pr[f(a_3)=+1 | F_2]=2/7>1/4`.

This directly contradicts Lemma 4.1.

Let `D` be the number consumed from `A` minus the number consumed from `B`.
If `a_3` is negative (probability `5/7`), the greedy rule consumes it and
increments `D` by one.  If `a_3` is positive (probability `2/7`), the two
positive frontiers tie and a fair coin chooses the block.  Hence

`Pr[Delta D=+1 | F_2]=5/7+(2/7)(1/2)=6/7`

and

`Pr[Delta D=-1 | F_2]=(2/7)(1/2)=1/7`.

Thus `D` is not a martingale, contradicting Lemma 3.3's asserted conditional
increment symmetry.

## Reproduction

Run:

```powershell
python experiments/verify_balanced_chain_counterhistory.py
```

The script enumerates all `binom(7,2)=21` balanced completions and uses exact
rational arithmetic.

## Scope

The history shows that inspected-but-unconsumed frontier values destroy the
exchangeability used by both proofs.  Forgetting that information in a
coarser filtration does not fix the argument because the adaptive state and
choice are then no longer measurable in the required way.  A repaired
construction needs an enlarged posterior state, a genuinely nonadaptive
exposure rule, or a longer-horizon analysis.  Failure of this construction is
not a lower bound on unrestricted `N(n)`.

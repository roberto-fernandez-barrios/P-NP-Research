# Barrier audit: Cycle-4 rooted `RR_n` / ordinary-interval obstruction

**Date:** 2026-08-21
**Result audited:** the rooted complement/reversal reduction and its
single-copy acceptance consequence
**Overall disposition:** **PASS FOR THE STATED RESTRICTED COMBINATORIAL
OBSTRUCTION; NO COMPLEXITY-SEPARATION CONSEQUENCE**

This is the Phase-7 audit required by
[`INITIAL_RESEARCH_MISSION.md`](../../INITIAL_RESEARCH_MISSION.md).  A pass
here means only that none of the checked complexity-theoretic barriers
invalidates the theorem at its stated scope.  It is not an additional proof
of the theorem, a novelty finding, or evidence for a complexity separation.

## 1. Claim whose scope is being audited

For even `n=2m`, let `A_n` be the balanced-coloring acceptance probability
of the full induced subset DAG of the corrected one-cycle family `RR_n`.
Let `p_N` be the corresponding acceptance probability for the ordinary
one-interval family `I_(N,1)`.  The Cycle-4 proof establishes

```text
A_n <= m p_(n-2).
```

The exact rooted equivalence is elementary: after normalizing infinity to
have sign minus and fixing the finite rank-one root `r`, complementing and
reversing the nested cyclic intervals gives a 1-balanced maximal chain of
ordinary intervals on the other `n-2` points, and conversely.  The known
FLSY interval theorem then gives an absolute `c>0` such that

```text
A_n <= (n/2) 2^(-c (n-2)^(1/5))
    <= 2^(-c' n^(1/5))
```

for all sufficiently large even `n`, after changing the absolute constant.
Only this one-sided upper bound is claimed.  Its consequences are:

1. the proposed premise `A_n >= n^(-O(1))` is false for this exact family;
2. no inverse-polynomial-measure subclass of balanced words can be contained
   in the single-copy accepted class; and
3. any cover in which every witness lies wholly inside one constituent
   relabelled copy needs `2^(Omega(n^(1/5)))` copies.

The audited claim expressly does **not** control hybrid chains created in
the literal subset union of several copies.  It is not a lower bound on
`N(n)`, not an obstruction to arbitrary balanced-chain families, and not a
Boolean or algebraic complexity lower bound.  The proof and independent
logical audit are in
[`rooted_interval_obstruction.md`](../../research_cycle_04/rooted_interval_obstruction.md),
[`rr_probability_attack.md`](../../research_cycle_04/rr_probability_attack.md),
and
[`cycle04_rr_obstruction_adversarial.md`](../cycle04_rr_obstruction_adversarial.md).

## 2. Barrier disposition table

| Mission question | Disposition | Reason |
|---|---|---|
| Does the argument relativize? | **NOT APPLICABLE in the Baker--Gill--Solovay sense** | The claim is a finite set-system/probability statement. It mentions no oracle Turing machine or oracle complexity class. Its set bijection, conditioning, and union bound are unchanged by adjoining an irrelevant oracle, but calling that “a relativizing P-versus-NP proof” would misclassify the result. |
| Would relativization prevent the claimed consequence? | **NO, within the stated scope** | Opposite `P` versus `NP` oracle worlds do not contradict a theorem about the acceptance density of one fixed family. No `P`-versus-`NP` consequence is claimed. Any future complexity consequence would require a separately proved bridge and a fresh relativization audit. |
| Is this a Razborov--Rudich natural proof? | **NOT APPLICABLE** | The theorem does not define a useful property separating high-circuit-complexity truth tables from low-circuit-complexity ones and proves no circuit lower bound. A more detailed criterion check appears below. |
| Which constructivity/largeness/usefulness conditions apply? | **LIMITATION: constructivity alone is present; the triad is absent** | Single-word RR acceptance is decidable by polynomial-size induced-DAG reachability. The accepted class is stretched-exponentially sparse under the balanced distribution. The complementary rejected class is large there, but no usefulness-against-circuits statement exists. Thus the natural-proofs barrier is not triggered. |
| Does the argument algebrize? | **NOT APPLICABLE in the Aaronson--Wigderson sense** | No oracle and low-degree extension, arithmetized machine computation, or algebraic-oracle simulation occurs. Sums of signs and the FLSY combinatorial theorem do not by themselves make a proof “algebrizing.” |
| Does an oracle, black-box, or magnification barrier apply? | **NOT APPLICABLE** | There is no oracle reduction, black-box lower-bound method, MCSP-style target, or weak-to-strong hardness-magnification implication. FLSY is used as a cited theorem with its parameters checked, not as an oracle. |
| Is a hidden assumption equivalent to or stronger than the desired conclusion? | **PASS** | The exact reduction imports a known interval-family probability upper bound; it does not assume O01, a lower bound on `N(n)`, or a complexity separation. The main model and quantifier hazards have been checked explicitly below. |
| Is the result merely about a restricted computational model? | **LIMITATION: YES, in an even narrower construction-family sense** | It obstructs one fixed `RR_n` family and covers by individual-copy witnesses. No transfer to arbitrary set families, literal unions with hybrid paths, circuits, ABPs, or Turing-machine classes is proved. |

## 3. Relativization

The Baker--Gill--Solovay barrier concerns arguments purporting to separate
classes such as `P` and `NP` while remaining valid relative to every common
oracle.  The present theorem has no machine model and no oracle parameter.
It is a statement about permutations, signed finite sets, interval chains,
and a probability distribution.  Its proof consists of a literal
complement/reversal bijection, a fixed-root conditioning calculation, a
union bound over roots, and an application of a published interval-family
theorem.

Those steps are insensitive to an auxiliary oracle only in the vacuous
sense that the oracle is never queried.  This neither invalidates the
combinatorial result nor supplies a nonrelativizing technique.  The
relativization barrier would become relevant only if a future argument
attached a complexity-class consequence.  No such bridge is present here,
and none may be inferred from this audit.  See the repository
[`barrier catalogue`](../../literature/barriers.md#1-relativization) and
Baker--Gill--Solovay,
[*Relativizations of the P=?NP Question*](https://doi.org/10.1137/0204037).

## 4. Natural-proofs criteria

The Razborov--Rudich test must be applied to a property of Boolean-function
truth tables, with constructivity, largeness, and usefulness checked
separately.  The audited theorem instead classifies balanced sign words
relative to one labelled cyclic set family.

### Constructivity

Given a length-`n` coloring, whether `RR_n` accepts it can be decided by
constructing the `O(n^2)` literal family and performing compatibility-filtered
reachability in its adjacent-rank inclusion DAG.  Thus this word property is
constructive in time polynomial in the word length.  This observation is not
a circuit lower bound.

### Largeness

Under the uniform balanced-word distribution, the accepted class has measure
at most `2^(-Omega(n^(1/5)))`, while the rejected class has measure at least
`1-2^(-Omega(n^(1/5)))` for sufficiently large even `n`.

Even an artificial truth-table encoding does not produce the missing natural
property.  If `n=2^r` is treated as the truth-table length and the acceptance
property is declared false on unbalanced tables, its density among all
`r`-variable functions is at most
`2^(-Omega(2^(r/5)))`, below the natural-proofs largeness threshold
`2^(-O(r))`.  The complementary rejection property can be large, but
largeness alone is insufficient.

### Usefulness

No statement relates RR acceptance or rejection to the circuit complexity of
the encoded truth table.  In particular, the proof does not show that all
polynomial-size circuit families avoid either property infinitely often.
Usefulness against `P/poly`, or against any named circuit class, is absent.
Therefore the three Razborov--Rudich conditions never occur together, and
the natural-proofs barrier does not apply.  This is **not** evidence that the
method bypasses that barrier; the method simply does not attempt the kind of
lower bound to which it applies.  See
[`literature/barriers.md`](../../literature/barriers.md#2-natural-proofs) and
Razborov--Rudich, [*Natural Proofs*](https://doi.org/10.1006/jcss.1997.1494).

## 5. Algebrization

Aaronson--Wigderson algebrization concerns simulations in which machines
receive oracle access together with appropriate access to a low-degree
extension.  Nothing of that form appears here.  The imbalance
`sum_{x in S} f(x)`, cyclic-interval complementation, and the imported FLSY
probability estimate are finite combinatorics, not an algebraic-oracle
argument.  Accordingly the correct disposition is **not applicable**, not
“nonalgebrizing.”  A later arithmetization or algebraic-complexity bridge
would need its own audit.  See
[`literature/barriers.md`](../../literature/barriers.md#3-algebrization) and
Aaronson--Wigderson,
[*Algebrization: A New Barrier in Complexity Theory*](https://doi.org/10.1145/1490270.1490272).

## 6. Oracle, black-box, and magnification checks

No algorithm or hard function is treated as an oracle, and no black-box
simulation or lower-bound transfer is asserted.  Applying FLSY Theorem 4.4
to `N=n-2` is ordinary theorem reuse: the family, distribution, parity,
strict `epsilon` inequality, and `k=1<N^(1/5)` condition were matched
explicitly.  Its primary source is Fabris--Limaye--Srinivasan--Yehudayoff,
[*Multilinear Algebraic Branching Programs and the Min-Partition Rank
Method*](https://eccc.weizmann.ac.il/report/2026/001/), Theorem 4.4
(Theorem 1.7).

There is also no hardness-magnification statement.  The theorem does not
start from a weak circuit lower bound, does not target MCSP or a related
meta-complexity problem, and does not infer a strong separation.  Therefore
the locality and parameter-interface barriers catalogued for magnification
do not match this result.  In particular, the title and broader context of
the FLSY paper do not license an mABP, Boolean-circuit, or `P`-versus-`NP`
consequence here; no such consequence is used or claimed.

## 7. Hidden-assumption audit

The proof is not secretly as strong as O01.  Its substantive external input
is the known FLSY interval-family upper bound, which is strictly narrower
than either constructing a polynomial balanced-chain family or lower-bounding
all such families.  The following common hidden assumptions were checked in
the Cycle-4 proof and independent adversarial reconstruction:

* **Literal family and all ranks:** `RR_n` is the `(n-1)^2+2`-subset family,
  and the equivalence uses the full induced subset DAG, including rank one,
  rank two, every odd intermediary, and the endpoints.  It is not a
  seed-path-only calculation.
* **Normalization:** global sign reversal preserves acceptance and chooses
  exactly one infinity-negative representative from each sign pair.
* **Root quantifiers:** the restriction is uniform only after fixing `r` and
  conditioning on `f(r)=+1`.  The possibly coloring-dependent witness root
  is handled afterward by a union bound; no independence among root events
  is assumed.
* **FLSY parameters:** `n-2` is even, `k=1` satisfies the strict threshold
  for sufficiently large `n`, and the strict condition on `epsilon` still
  yields the stated non-strict upper bound by choosing an intermediate
  `epsilon`.
* **Asymptotics:** absorbing the polynomial prefactor changes the absolute
  constant and sufficiently-large threshold.  The result is only
  `A_n <= 2^(-Omega(n^(1/5)))`; no matching lower bound is claimed.
* **Coverage semantics:** the lower bound on the number of relabelings is
  proved only when the accepted-coloring sets of the individual copies must
  cover all colors.  It is not transferred to the full DAG of their literal
  union, where genuinely new hybrid paths may exist.
* **Uniformity and explicitness:** no efficient construction of a relabeling
  list is assumed or concluded.  The S4-D theorem is an upper bound on one
  fixed family's acceptance probability.

No step assumes O01, `P != NP`, a circuit lower bound, or an assertion
equivalent to them.  There is therefore no detected circularity.  This
barrier finding relies on, but does not replace, the separate proof audit.

## 8. Restricted-family boundary

The restricted-model question is the decisive limitation.  The theorem is
not even a hardness theorem for a standard computational model; it is an
obstruction for a particular combinatorial construction:

```text
one corrected cyclic RR family
    -> acceptance by one relabelled copy
    -> individual-copy symmetrization / cover.
```

It leaves open all of the following:

* an explicit polynomial-size literal union of relabelled `RR_n` copies
  whose coverage relies on hybrid chains;
* a different polynomial-size balanced-chain family;
* the primary target `N(n) <= n^C`;
* any transfer to multilinear ABPs, general ABPs, Boolean circuits, or
  Turing-machine complexity classes; and
* `P` versus `NP`.

Hardness for, or failure of, this restricted construction cannot be moved to
any stronger model without a separately proved simulation or reduction.  No
such edge is present.  The finite multi-`RR` certificates in Cycle 4 are
consistent with this boundary: they concern literal unions and carry no
asymptotic conclusion.

## 9. Final barrier verdict

The rooted `RR_n` / ordinary-interval obstruction receives a **PASS** as the
stated S4-D construction-family theorem.  Relativization, natural proofs,
algebrization, oracle/black-box limitations, and hardness magnification do
not invalidate it because it asserts no corresponding complexity lower bound
or separation.  This is primarily a not-applicable finding, not a claimed
barrier bypass.

The essential limitation is explicit and non-removable by wording: the
theorem obstructs individual-copy RR symmetrization only.  It says nothing
about hybrid multi-copy unions or arbitrary balanced-chain families.  It
therefore supplies no resolution of O01 and no complexity-theoretic
separation.

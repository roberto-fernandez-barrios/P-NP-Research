# Cross-validation audit: balanced chains, meta-complexity, and Cutting Planes

Audit date: 2026-08-13. This is an independent Phase 0/1 check of candidate first
targets proposed in the circuit/barrier and meta-complexity tracks. It does not claim a
complexity separation. Status words below mean status in the audited public literature.

## 1. Balanced-chain target: exact statement and current status

Let `n` be a positive **even** integer. A balanced coloring is a map
`f:[n] -> {+1,-1}` with `sum_x f(x)=0`. For a set system
`X subseteq P([n])`, Fabris--Limaye--Srinivasan--Yehudayoff (FLSY) define

```
cbal(X) = max_{balanced f} min_{maximal chains (C_0,...,C_n) in X}
          max_{0 <= i <= n} |sum_{x in C_i} f(x)|,
```

where a maximal chain has `|C_i|=i` and
`C_0 subset C_1 subset ... subset C_n`. A system is `k`-balanced-chain when
`cbal(X)<=k`, and `N(n)` is the minimum size of a 1-balanced-chain system.
The candidate is therefore the following unambiguous existence statement:

> **BC-POLY.** There is an absolute constant `C` such that, for every positive
> even `n`, `N(n)<=n^C` (enlarging the constant to absorb finitely many small
> cases if necessary).

The evenness qualifier is essential. If the definition is copied verbatim to odd
`n`, the maximum ranges over no balanced `+-1` coloring and is either undefined or
vacuous depending on convention. The target is well-posed after restricting to even
`n`; this is not a substantive obstruction.

### 1.1 What TR26-001 actually proves

**KNOWN.** FLSY prove

```
Omega(n^2) <= N(n) <= n^{O(log n / log log n)}.
```

The lower bound is stated more generally as `Omega(n^2/k)` for a
`k`-balanced-chain system. Their Theorem 1.6 gives the quasipolynomial upper
bound, and their further-questions section explicitly leaves closing this gap open.
Their Lemma 1.5 (also restated as Theorem 2.4 in the later withdrawn preprint)
is a worst-case-from-average reduction: an `(epsilon,k)`-balanced-chain system of
size `s` yields a worst-case `k`-balanced-chain system of size `O(sn/epsilon)`.

The algebraic consequence has a parameter asymmetry that matters. In the general
multilinear-ABP setting, FLSY Theorem 1.3 says, in the paper's notation:

- if every `(log s)`-balanced-chain system has size at least `s`, then every
  full-rank multilinear ABP has size at least `s^{Omega(1)}`;
- a constant-balanced-chain system of size `s` gives a full-rank multilinear
  polynomial over every infinite field computed by an mABP of size `s poly(n)`.

The characterization is tighter in the set-multilinear setting. Consequently, the
older polynomial-size mABP separation of Dvir--Malod--Perifel--Yehudayoff, whose
rank guarantee is for a restricted family of arc partitions, cannot simply be run
backwards to prove BC-POLY. No such converse is supplied by FLSY.

Primary source: T. Fabris, N. Limaye, S. Srinivasan, and A. Yehudayoff,
[*Multilinear Algebraic Branching Programs and the Min-Partition Rank
Method*](https://eccc.weizmann.ac.il/report/2026/001/) (ECCC TR26-001),
especially Definition 1.2, Theorems 1.3 and 1.6, Lemma 1.5, and Section 1.4;
[primary PDF](https://eccc.weizmann.ac.il/report/2026/001/download/).

### 1.2 What TR26-043 does not currently prove

**WITHDRAWN / NOT A KNOWN THEOREM.** Version 1 of TR26-043 claimed
`N(n)=n^{O(1)}`. The current ECCC record has a revision notice dated 2026-05-11:
an anonymous referee found that Lemma 4.1's forced-probability bound was proved
only unconditionally, whereas its use requires conditioning on the filtration; the
notice says every result in the paper crucially depends on that lemma. The current
arXiv record says that the author withdrew the paper and gives the same reason.

The ECCC page still displays the old affirmative abstract below the revision notice,
and its download/mirrors can expose version 1. Those artifacts are not evidence that
the theorem survived. The status-bearing sources are the
[ECCC revision record](https://eccc.weizmann.ac.il/report/2026/043/) and the
[withdrawn arXiv record](https://arxiv.org/abs/2604.00746). The invalidated argument
can be inspected in the
[version-1 PDF](https://arxiv.org/pdf/2604.00746v1), but should be cited as a
withdrawn proof candidate.

Exact-title, exact-arXiv-ID, author/title, `balanced-chain`, `N(n)`, and
`min-partition rank` searches through the audit date found no corrected version,
published repair, or independent proof. Hits repeating the April abstract were stale
mirrors or metadata pages. **Public-literature classification: OPEN, high
confidence.** This is not a claim about unpublished work.

## 2. Independent audit of the withdrawn two-block proof

The v1 construction splits a segment into two ordered blocks. At a grid state it
inspects the next element of both blocks, consumes an element that minimizes the
absolute running imbalance, and uses a fair coin on a tie. Write `H(t)` for signed
imbalance and `h(t)=|H(t)|`. When `h(t)>=1`, an upward step occurs exactly when
both frontier values have sign `sgn(H(t))`.

Lemma 4.1 defines

```
p_t = Pr[h(t+1)=h(t)+1 | F_t]
```

and claims `p_t<=1/4` at every live state. Its proof counts the sign agreeing with
`H(t)` among all `R` unconsumed elements and inserts the without-replacement
formula `P/R * (P-1)/(R-1)`. This substitution requires the two frontier elements
to remain an exchangeable pair conditional on `F_t`. They do not: earlier choices
carry information about a frontier element that was inspected but not consumed.

### 2.1 Explicit positive-probability counterhistory

This failure is visible without asymptotics. Take `n=10`, with ordered blocks

```
A=(a_1,...,a_5),   B=(b_1,...,b_5).
```

Condition on the positive-probability history

```
f(a_1)=f(a_2)=f(b_1)=+1,
the first tie coin consumes a_1, and the second tie coin consumes a_2.
```

At time zero, `H=0`, so the first choice is a tie and consumes `a_1`. At the next
step both candidates `a_2,b_1` are `+1`; the second tie consumes `a_2`. Hence at
time two, `H=2`, while the unconsumed frontier `b_1` is already known (or is
logically inferable from the adaptive choice) to be `+1`.

A balanced coloring on ten points has five plus signs. Of the eight unconsumed
elements, three are plus, but one of those three is the known `b_1`. Exactly two of
the other seven, still symmetric positions are plus. Therefore

```
p_2 = Pr[f(a_3)=+1 | F_2] = 2/7 > 1/4,
```

because the other frontier `b_1` is certainly plus. Balanced completions exist
(`choose(7,2)` of them before accounting for the remaining labels), so this is not
a zero-probability conditioning event.

This is a direct falsification of v1 Lemma 4.1 as stated, not merely a complaint
that a displayed calculation omitted detail. It validates the official withdrawal;
it does **not** refute BC-POLY.

### 2.2 A second affected lemma

The same history also invalidates the proof's assertion in Lemma 3.3 that the block
deviation `D(t)=a_t-b_t` is a martingale because both next values are unrevealed and
exchangeable. At time two above, if `a_3=-1` (conditional probability `5/7`), the
rule must consume `a_3`, increasing `D`; if `a_3=+1` (probability `2/7`), a fair tie
coin increases or decreases `D`. Thus

```
Pr[D(3)-D(2)=+1 | F_2] = 5/7 + (2/7)(1/2) = 6/7,
Pr[D(3)-D(2)=-1 | F_2] = 1/7.
```

So `D` is not a martingale under the information required to describe the adaptive
process. Defining a coarser sigma-algebra that deliberately forgets the inspected
frontier does not repair the proof: then the adaptive chain state/choice is not
properly represented, while conditioning on the observable selected path again
reveals the information. This second issue attacks the Azuma-based block-deviation
bound independently of the advertised Lemma 4.1 gap.

### 2.3 Consequences for a repair attempt

The one-step potential `3^{h(t)}` is not a supermartingale on the actual filtration,
and the downstream maximum-height, excursion-length, and multiscale estimates cannot
be retained by citing the v1 argument. A plausible repair would need at least one of:

- an enlarged state/potential that tracks the signs or posterior law of all exposed,
  unconsumed frontiers;
- a genuinely fresh/nonadaptive exposure rule, together with proof that the union of
  all possible output sets remains polynomial;
- a longer-horizon domination theorem that tolerates locally positive conditional
  drift and still gives the required frequent-return and residual-size tails.

Merely replacing `<1/4` by an unconditional average bound is insufficient for the
stopping-time arguments. The additional failure of the `D(t)` martingale means that
repairing the height potential alone would still leave a separate proof obligation.

## 3. Attempts to collapse BC-POLY to known combinatorics

The following checks did not prove the target known, but eliminate several tempting
shortcuts.

1. **A fixed chain covers `2^(n/2)` colorings.** A maximal chain is a
   permutation ordering of `[n]`. Requiring every prefix sum to have absolute
   value at most one forces opposite signs within the consecutive pairs
   `(1,2),(3,4),...`, but does not constrain the sign across a pair boundary.
   The orientation of every pair is independent, so exactly `2^(n/2)` signed
   balanced colorings are compatible with the chain. Hence any method that
   explicitly lists universal chains needs at least
   `binom(n,n/2)/2^(n/2)` chains, which is still exponential. A small set
   system can encode exponentially many chains through shared subsets, so
   this observation does not lower-bound `N(n)` beyond what is already known;
   it rules out the naive polynomial-list-of-permutations interpretation.

2. **Steinitz/rearrangement does not swap the quantifiers.** For each individual
   balanced `f`, one can order plus and minus elements alternately. The union of the
   resulting prefix sets over all `f` is generally exponential. BC-POLY asks for one
   fixed polynomial-size family before the coloring is chosen.

3. **Sorting or permutation networks do not immediately give a set system.** A
   polynomial-size network may compactly route many permutations, but a merged
   network vertex can be reached with different prefix subsets. An element of `X`
   must be a particular subset of `[n]`, not merely a control state. A construction
   needs a separate bound on the number of distinct subsets represented.

4. **An adaptive algorithm is not itself the object.** The builder may depend on
   `f`, but the set system containing every intermediate set must not. FLSY's
   worst-case-to-average lemma applies to one fixed small average-case system; it
   does not turn an algorithm with superpolynomially many possible states into a
   polynomial family.

5. **The old mABP separation is one-way evidence.** Restricted arc-partition full
   rank does not give full rank for every balanced partition and therefore does not
   instantiate the FLSY construction in reverse.

No primary source found in the audit identifies BC-POLY with a standard solved
universal-traversal, discrepancy, sorting-network, or Steinitz theorem. The problem
is therefore neither known nor ill-posed on the available evidence.

## 4. Comparison with the track-local Cutting Planes target

The proof-complexity dossier's target is:

> **CP-SPACE.** For the complete-tree contradictions `CT_n`, improve the known
> `CP_2` inequality-space lower bound from `Omega(log log log n)` to any
> `omega(log log log n)` bound, initially even in a clearly stated normal form or
> along an explicit infinite subsequence whose restriction can later be removed.

The primary CCC 2015 paper supports both the status and an important tractability
caveat. Its Theorem 6.5 proves that, if a `CT_n` refutation has inequality space
`c` and each line uses at most `b` distinct coefficients, then
`b^c >= sqrt(log log n)`; Theorem 6.6 specializes this to
`c=Omega(log log log n)` for every fixed `CP_k`. Section 7, Problem 3 explicitly
asks for a better space lower bound for `CP_2`. Source: N. Galesi, P. Pudlak, and
N. Thapen, [*The Space Complexity of Cutting Planes Refutations*](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2015.433),
Theorems 6.5--6.6 and Problem 3; [primary proceedings
PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol033-ccc2015/LIPIcs.CCC.2015.433/LIPIcs.CCC.2015.433.pdf).

The proof converts a space-`c` configuration into a `b^c`-symmetric set of
assignments and counts the possible cardinalities of such sets. This reveals that
the proposed `omega(log log log n)` increment is not automatically a tiny sharpening
of a numerical estimate. Even optimizing the paper's orbit-counting inequality can,
at best, raise the intermediate symmetry lower bound from the displayed
`sqrt(log log n)` toward roughly `log log n/log log log n`; taking a logarithm base
constant still yields only `Theta(log log log n)`. To obtain an `omega` space bound
through the same reduction, one would need a symmetry lower bound
`s=(log log n)^{omega(1)}`, or a qualitatively stronger invariant. This makes
CP-SPACE scientifically clean but less obviously tractable than the raw gap size
suggests.

Two formulation cautions further lower its first-target score. First, a better bound
on an infinite subsequence is a legitimate weaker result but does **not** establish
`omega(log log log n)`, whose ratio must diverge for all sufficiently large `n`.
Second, `CT_n` contains the clause falsified by each of the `2^n` assignments. In
terms of explicit formula length `M`, the current lower bound is only at the scale of
a fourth iterated logarithm (up to encoding factors). Small-instance proof search is
valuable for killing invariants, but cannot empirically resolve that asymptotic scale.

The two targets have different research profiles.

| Criterion | BC-POLY | CP-SPACE |
|---|---|---|
| Current theorem frontier | quasipolynomial upper bound versus polynomial conjecture | triple-iterated-log lower bound versus any strict asymptotic improvement |
| First falsification object | explicit finite adaptive histories; exact `N(n)` via set cover/SAT/ILP | small-space `CP_2` proof search; counterexamples to configuration invariants |
| Increment size | potentially large collapse from quasipolynomial to polynomial | deliberately incremental lower-bound improvement |
| Immediate significance | proves a limitation/barrier for min-partition rank against mABPs | advances a lower bound in a concrete proof system |
| Relation to P versus NP | indirect algebraic-method diagnosis | direct proof-complexity progress, still far from a separation |
| Present lead | withdrawn construction with now at least two filtration failures | a valid published lower bound whose loss points can be reconstructed |
| Main risk | invalid near-proof may be far from repair; positive theorem is all-or-nothing unless restricted-process results are isolated | tiny instances may not reveal iterated-log asymptotics; normal-form restriction may fail to lift |

**Assessment before the meta-track comparison.** BC-POLY is more immediately
falsifiable and experimentally accessible, and auditing the withdrawn proof already
produces useful negative structural information. CP-SPACE is the safer choice for a
small meaningful theorem: the requested advance is incremental, and success would
be a genuine lower bound rather than a barrier to one method. BC-POLY should outrank
CP-SPACE only if the first cycle is explicitly scoped as a **repair-or-obstruction
diagnostic** for the two-block/multiscale family, not because version 1 is considered
"nearly complete." The explicit histories show that it is not nearly complete under
its present filtration.

## 5. Meta-complexity candidate

The strongest fixed candidate supplied by the meta-complexity track is:

> **META-BP.** Let `N=2^n`. For standard total MCSP, whose input is a truth table
> `tt(f)` together with a binary circuit-size threshold, prove that every
> deterministic unrestricted branching program has size
> `Omega(N^2/log^C N)` for one fixed absolute `C`; the concrete sharp goal is
> `C=2`.

The model should be frozen as the standard acyclic deterministic binary branching
program with arbitrary repeated variable queries. Size may be counted by query nodes
or labelled edges, but one convention must be used; these differ by at most a constant
for the standard model. “Polylog” must mean one stated constant exponent, not an
input-dependent exponent. The full `(tt(f),theta)` language has `N+O(log N)` input
bits. This convention also avoids silently moving between a total all-threshold problem,
a fixed-threshold slice, and a gap promise problem.

### 5.1 Current theorem and quantitative gap

**KNOWN.** Cheraghchi--Kabanets--Lu--Myrisiotis prove that any arbitrary-basis
formula or general deterministic branching program computing MCSP on truth tables of
length `N` has size

```
N^2 / 2^{O(sqrt(log N))}.
```

This is Theorem 2 of their ICALP 2019 paper. Their proof constructs a strongly local
PRG for size-`s` general branching programs whose local circuit complexity is
`s^{1/2} 2^{O(sqrt(log s))}` (Lemma 24), then applies the local-PRG-to-MCSP
framework (Theorem 13). The framework begins with a device for total MCSP and fixes
the threshold to the PRG's local complexity. Thus the cited theorem supports the
all-threshold formulation above; it should not be misreported as a lower bound for
every independently chosen fixed-threshold slice.

Primary source: M. Cheraghchi, V. Kabanets, Z. Lu, and D. Myrisiotis,
[*Circuit Lower Bounds for MCSP from Local Pseudorandom
Generators*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.39/LIPIcs.ICALP.2019.39.pdf),
Theorems 2 and 13 and Lemma 24; [ECCC full-version
record](https://eccc.weizmann.ac.il/report/2019/022/).

The desired denominator is a genuine improvement: for every fixed `C`,
`2^{Theta(sqrt(log N))}` eventually exceeds `log^C N`. The known theorem can be
summarized as `N^{2-o(1)}`, but that notation does not imply a quadratic-over-polylog
bound.

### 5.2 The exact-looking theorem is for MKTP

**KNOWN BUT NON-TRANSFERRING.** Cheraghchi--Hirahara--Myrisiotis--Yoshida
Theorem 4 proves

```
BPsize(MKTP_N) = Omega(N^2/log^2 N).
```

MKTP asks about time-bounded Kolmogorov complexity, not minimum Boolean-circuit
size. The same source explicitly says that its Nechiporuk argument fails to apply to
MCSP: although KT complexity and circuit complexity are polynomially related, the
relation is not tight enough for the subfunction-counting proof. It separately proves
only `N^{1.5-o(1)}` for nondeterministic, co-nondeterministic, and parity branching
programs computing MCSP; those are different conclusions and do not settle META-BP.

Primary source: M. Cheraghchi, S. Hirahara, D. Myrisiotis, and Y. Yoshida,
[*One-Tape Turing Machine and Branching Program Lower Bounds for
MCSP*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf),
Theorems 4--5 and the discussion immediately following Theorem 4.

Exact theorem-string, model-variant, MCSP/branching-program, author-follow-up,
ECCC, and 2024--2026 searches found no later result giving META-BP. Recent hits for
partial minimum branching-program size, read-once nondeterministic branching
programs, and one-tape time lower bounds alter the function or model and do not imply
the target. **Public-literature classification: OPEN, medium confidence.** Confidence
is lower than for BC-POLY because the exact sharpening was not located as a numbered
open problem and general branching-program literature is broad.

### 5.3 Significance and tractability

META-BP is a strong local-PRG/lower-bound target, not a routine denominator cleanup.
The MKTP source says `Omega(N^2/log^2 N)` matches the state-of-the-art general
branching-program lower-bound frontier for an explicit function up to constants and
is optimal for the Nechiporuk method used there. Reaching that frontier for MCSP would
therefore require either a substantially sharper strongly local PRG than the 2019 one
or a new mechanism that overcomes the stated MCSP subfunction-counting obstruction.

The target is adjacent to hardness magnification but is **not itself** one of the
standard magnification hypotheses found in the primary literature. The branching-
program item in Oliveira--Pich--Santhanam's magnification theorem concerns
`Gap-MKtP` in a small-complexity regime and a lower bound beyond `N^{2+epsilon}`;
their MCSP theorem concerns `Gap-MCSP` and general circuits, with carefully separated
thresholds. A quadratic-over-polylog lower bound for total MCSP must not be claimed to
imply `P!=NP` without an additional exact reduction. Source: I. Oliveira, J. Pich,
and R. Santhanam, [*Hardness Magnification near State-Of-The-Art Lower
Bounds*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol137-ccc2019/LIPIcs.CCC.2019.27/LIPIcs.CCC.2019.27.pdf),
Theorems 1 and 4.

Finite branching-program synthesis can reject proposed reductions on tiny instances,
but it gives little evidence about replacing a `2^{O(sqrt(log N))}` loss by a polylog.
Formal verification would require a substantial PRG/extractor or subfunction-counting
library. META-BP is consequently the most technically significant of these three
targets if solved, but the least suitable first-cycle attack.

## 6. Final cross-track ranking and recommendation

| Rank | Target | Audit verdict |
|---:|---|---|
| 1 | **BC-POLY**, attacked first through a bounded repair-or-obstruction audit of the two-block/multiscale construction | Best finite falsifiability and freshest concrete lead. The general statement is open, but the withdrawn proof has two independent filtration failures and must not be called nearly complete. |
| 2 | **CP-SPACE** | Clean direct lower-bound problem and explicit original open question. However, `CT_n` has exponentially many clauses, feasible instances cannot exhibit the iterated-log regime, and the existing symmetry count cannot yield little-omega space merely by tightening constants. |
| 3 | **META-BP** | Clean after fixing conventions and potentially very significant, but asks MCSP to reach essentially the general BP frontier; the most obvious Nechiporuk transfer is explicitly known to fail and finite tests are weak evidence. |

**Recommend exactly one first target: BC-POLY**, stated only for even `n` as in
Section 1. This recommendation is comparative, not an estimate that the v1 proof is
close. The first attack should be the following falsifiable subprogram inside that
target:

1. formally encode the exact filtration, including inspected-but-unconsumed frontier
   signs, and machine-check the `n=10` counterhistory above;
2. enumerate the smallest failing histories for both the forced-probability and block-
   deviation claims;
3. test whether any potential on the enlarged finite state gives the height and
   residual-size tails simultaneously;
4. stop the repair route if the number of necessary frontier/posterior states destroys
   polynomial set-system accounting.

A proved obstruction to this restricted process is a useful negative result but does
not complete BC-POLY. The target remains the general polynomial set-system existence
statement; the process audit is the first bounded attack. If it yields neither a valid
potential nor a reusable restriction theorem, switch to CP-SPACE rather than silently
expanding into a general mABP or P-versus-NP attack.

### Uncertainty ledger

Uncertainties to retain:

- Search failure cannot exclude unpublished repairs or work too recent to be indexed.
- The `n=10` history is an explicit counterexample, but no claim is made that it is
  globally the smallest counterhistory; exhaustive enumeration would be needed.
- Local positive drift does not rule out a different long-horizon potential or the
  polynomial existence theorem.
- A restricted-construction impossibility theorem would be a legitimate negative
  result, but must never be described as a lower bound on unrestricted `N(n)`.
- META-BP's status is medium-confidence because no search establishes novelty and
  model terminology is broad; freeze total-vs-slice and node-vs-edge conventions.
- The MKTP theorem cannot be cited as an MCSP theorem, and the total-MCSP target is
  not automatically a hardness-magnification premise.

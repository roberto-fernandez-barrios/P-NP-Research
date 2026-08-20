# Adversarial audit: Cycle-2 repair and cached-frontier obstruction

## Audit status and independence

**Objects audited:** `research_cycle_02/proof_sat_repair_track.md`, especially Propositions 4.1, 5.1, and 6.1 and Candidate DR-1; and `research_cycle_02/construction_family_obstruction.md`, especially CF-O1 and its Stop-A classification.

**Status of this audit:** independent re-derivation and adversarial review completed; exact finite arithmetic rerun; `UNFORMALIZED`; no novelty claim and no external peer review.

I first derived the relevant probability and counting formulas directly from the stated processes and the primary sources, then compared them with the proposer report and its executable certificates. I did not edit the proposer report or any canonical state file.

Primary sources checked:

- Deepanshu Kush, *An Unconditional Barrier for Proving Multilinear Algebraic Branching Program Lower Bounds*, [ECCC TR26-043 v0](https://eccc.weizmann.ac.il/report/2026/043/download), April 1, 2026. Download SHA-256: `b72a0eedb80aea50dd3b9ed5c1e69cfd3a717fab7225ec69f46cfa6c15ecda0f`.
- Théo Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir Yehudayoff, *Multilinear Algebraic Branching Programs and the Min-Partition Rank Method*, [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/download), especially Lemma 2.3 and Lemma 3.2. Download SHA-256: `56f91e2c658dc689da9f543acbaf8dd9e127d551cb1f915c76b49001fba92a4a`.

The current ECCC record for TR26-043 itself states that Lemma 4.1 has a conditional-filtration gap and that the paper's results rely on it. That notice is corroborating context, not a substitute for the derivations below.

Verification rerun on 2026-08-21:

- `python -B research_cycle_02/experiments/check_proof_sat_repairs.py` — PASS, including every stored rational diagnostic;
- `python -B experiments/test_tr26_043_true_filtration.py -v` — PASS, 8/8 exact-enumerator tests; and
- a separate inline exhaustive coloring/process enumerator — PASS on the policy-robustness cases recorded in Section 2.

## Executive disposition

| Item | Verdict | Required qualification |
|---|---|---|
| Proposition 4.1, finite formula | **PASS** | Add `k>=1`; define `E_d` as the sign event, not as a particular tie outcome. |
| Proposition 4.1, asymptotic | **PASS** | `k=o(sqrt(M))`; uniform for every admissible `2<=d(M)<=D` with fixed `D`; room condition eventually holds. |
| Proposition 4.1, tie policy | **STRONGER THAN STATED** | Uniform ties are unnecessary for the Catalan lower bound; any nonanticipating one-frontier tie rule works. Uniformity is needed for the separate load-drift formula (3.2). |
| Proposition 4.1, construction consequence | **QUALIFIED PASS** | It falsifies the posted `O(log m)` gap with `O(1/m)` failure for a precise cached-frontier/direct-fill template. It does not rule out every polynomial use of the trajectories. |
| CF-O1 in `construction_family_obstruction.md` | **PASS, NARROWLY** | The theorem is uniform over `2<=d(M)<=D` and arbitrary nonanticipating tie policies. State `C,K>0`, `k>=1`, and retain every process/tail qualifier. Rename the identifier to avoid confusion with O01. |
| Proposition 5.1 | **ARITHMETIC PASS; TRANSITION INCOMPLETE** | It repairs the reserve inequality only. A full recursion still needs parity/splitting, next-scale closure, endpoint compatibility, and a larger local gap budget. |
| Proposition 6.1 | **PASS WITH GLOBALITY CLARIFICATION** | The polynomial description/local-family bounds must hold globally over all colorings, tie histories, and executions, and must include segment identity. |
| DR-1 | **PASS FOR THE STATED RESTRICTED CLASS** | Freeze a common constant gap factor, fixed `0<alpha<1`, and a polynomial list chosen independently of the coloring. It does not cover shared-state DAGs or adaptive splicing. |
| Executable certificates | **PASS AS FINITE DIAGNOSTICS** | The script does not prove the asymptotic propositions; its threshold and accounting checks are representative numerical checks. The written proofs carry those claims. |

### Cycle-2 stop condition A

**Qualified YES.** Proposition 4.1, together with a checked smallest counterhistory, reaches the first Cycle-2 stopping alternative for the following precisely frozen **high-confidence** family:

> Fix an integer `D>=2` and constants `C,K>0`. For each scale size `2M`, choose any `d(M)` with `2<=d(M)<=D` and `d(M)` dividing `2M`. Split into `d(M)` equal ordered blocks; expose the active frontiers; consume exactly one frontier minimizing global absolute imbalance; and use any nonanticipating tie rule. Demand, as a necessary part of the posted all-gaps guarantee, that the probability that the first subsequent balanced-band return gap exceeds `C log M` be at most `K/M`, so that direct gap filling and the advertised high-confidence multiscale union bound apply.

Uniformly over this family, even the first excursion has probability `Omega_D((log M)^(-3/2))` of exceeding `C log M`, which is eventually greater than `K/M`. Therefore that specific logarithmic high-confidence direct-gap template is obstructed, not merely its published potential proof.

This matches the literal first stopping alternative in `audits/first_target_selection.md`: “a checked smallest counterhistory plus a proved obstruction for a precise two-/bounded-block construction class.” For the eager-reveal process frozen here, the exact true-filtration enumerator finds the smallest Lemma-4.1 conditional-probability counterexample at `n=8` (atom probability `3/28`, conditional upward probability `1/3>1/4`) and exhaustively checks `n=2,4,6`. Under the separate query-minimal convention the minimum is `n=10`. I reran the eight-test exact suite successfully during this audit. Thus the smallest-history component and the asymptotic construction-family component use compatible eager semantics.

This is **not** an obstruction to:

- all fixed-`d` steering constructions;
- a quantitatively weaker return theorem;
- a compressed handler for longer gaps;
- a process that reconciles or consumes all inspected frontiers; or
- unrestricted `N(n)`.

If “stop condition A” is interpreted as requiring an impossibility theorem for every polynomial set system obtainable from any fixed-`d` trajectory, Proposition 4.1 does **not** meet that stronger reading. Its lower bound on one long-gap event tends to zero. In particular, it does not prove that success is non-noticeable, that every weaker return tail fails, that the probability all gaps are logarithmic is below every inverse polynomial, or that the union of all useful states is superpolynomial. The defensible canonical wording is therefore: **Stop A reached for the posted `1-O(1/M)` logarithmic cached-frontier/direct-fill guarantee only; no claim is made against noticeable success, weaker tails, other fixed-`d` constructions, or unrestricted `N(n)`.**

## 1. Reconstruction of the true cached-frontier law

Fix `d` active ordered blocks. Suppose the global imbalance is `H=h>0`, the unconsumed pool has size `R`, and `d-1` inspected but unconsumed frontiers are known pluses. The pool contains `(R-h)/2` pluses in total. Removing the `d-1` cached pluses leaves

\[
\frac{R-h}{2}-(d-1)
\]

uninspected pluses among `R-d+1` genuinely uninspected points. Only the block advanced on the previous step supplies a fresh frontier. Consequently

\[
p_d(R,h)
=\Pr(|H|\text{ increases at the next step}\mid\mathcal G)
=\frac{R-h-2d+2}{2(R-d+1)}.
\]

For fixed `d,h` this tends to `1/2`, not `2^{-d}`. The formula is valid when the displayed counts are nonnegative and parity-compatible. The negative-`H` case is symmetric.

If complete ties are uniform and block `j` supplies the fresh frontier, then

\[
\mathbb E[\Delta L_j\mid\mathcal G]=1-p_d+p_d/d,
\qquad
\mathbb E[\Delta L_i\mid\mathcal G]=p_d/d\quad(i\ne j).
\]

This load formula correctly gives expected two-block difference increment `1-p_d`. At `R=8,h=2,d=2`, `p_d=2/7`, so the increment distribution is `+1` with probability `6/7` and `-1` with probability `1/7`, with mean `5/7`.

The proposer formulas (3.1) and (3.2) are correct. The important scope distinction is that (3.1) does not use uniform tie breaking, while (3.2) does.

## 2. Proposition 4.1: independent derivation

Let the ambient balanced coloring have `M` pluses and `M` minuses. There are `d` equal blocks, each of length `2M/d`, and the process exposes all active frontiers and consumes one minimizing `|H|`.

Let `E_d` be only the event that the initial `d` frontiers have one common sign. Then

\[
\Pr(E_d)=2\frac{(M)_d}{(2M)_d}.
\]

The tie rule always consumes one of those frontiers, so no additional `1/d` factor belongs in `E_d`. Condition on the all-plus branch; the all-minus branch is symmetric. Immediately after the first consume:

- `H=1`;
- `d-1` plus frontiers remain inspected and cached;
- the uninspected population has `M-d` pluses and `M` minuses.

Until `|H|` returns to at most one, exactly one new color is exposed per step. A fresh minus is the unique correcting sign and is consumed. A fresh plus makes every frontier plus; whichever tied frontier is consumed, `d-1` pluses remain cached. Hence the sequence of consumed signs equals the adaptively sampled sequence of fresh signs.

Conditional on the past, the index of the next fresh point is measurable and uninspected. Uniform balanced coloring therefore makes its colors an ordered sample without replacement from the remaining counts. This remains true even though the block identity is adaptive.

Choose a word of length `2k` with `k` pluses and `k` minuses whose signed partial sums are strictly positive at every proper time and zero at the end. There are exactly

\[
\operatorname{Cat}_{k-1}
\]

such primitive Dyck words. Every fixed word has ordered-hypergeometric probability

\[
\frac{(M-d)_k(M)_k}{(2M-d)_{2k}}.
\]

Starting from `H=1`, every proper partial sum keeps `H>=2`, and the final zero sum returns to `H=1`. Thus the first subsequent balanced-band visit is exactly at time `2k`. The conditions

\[
k\le M-d,\qquad 2k+1<2M/d
\]

ensure the required colors exist and no block can exhaust even if all `1+2k` consumptions fall in one block. Therefore

\[
\Pr(T_{\rm bal}=2k\mid E_d)
\ge
\operatorname{Cat}_{k-1}
\frac{(M-d)_k(M)_k}{(2M-d)_{2k}}.
\]

This reproduces Proposition 4.1. The only missing formal side condition in its statement is `k>=1`.

In fact, under the displayed room condition the right side is the **exact** conditional probability, not only a lower bound: after leaving height one, every first return at even time `2k` corresponds bijectively to a primitive positive Dyck word of length `2k`. Keeping the weaker inequality is harmless and avoids requiring this strengthening downstream.

### Exact finite checks

I reran the proposer checker and separately recomputed the word counts and fractions without importing its functions.

- Primitive positive-return word counts for `k=1,...,7` were `1,1,2,5,14,42,132`, exactly `Cat_(k-1)`.
- For `M=10,d=2,k=4`, the conditional probability is `175/7293`; `Pr(E_2)=9/19`; their product is `525/46189`.
- For `M=60,d=3,k=4`, the conditional probability is `50445/2500238`.
- The room checks are strict: `2k+1=9<10` in the first instance and `9<40` in the second.

All certificate fractions in `proof_sat_repair_diagnostics.json` are correct.

As a separate policy-robustness check, I exhaustively enumerated all balanced colorings for five small `(M,d)` instances and simulated five deterministic nonanticipating tie rules (least block, greatest block, always fresh when tied, always cached when possible, and time-alternating). In every admissible case the exact conditional probability was policy-independent and equaled the formula:

| `(M,d,k)` | exact conditional probability |
|---|---:|
| `(5,2,1)` | `15/56` |
| `(6,2,1)` | `4/15` |
| `(6,2,2)` | `1/14` |
| `(8,2,1)` | `24/91` |
| `(8,2,2)` | `10/143` |
| `(8,2,3)` | `16/429` |
| `(6,3,1)` | `1/4` |
| `(8,4,1)` | `8/33` |

These finite enumerations are consistency checks only; policy-uniformity for all sizes follows from the filtration/exchangeability argument.

### Asymptotic check

For fixed `d` and `k=o(sqrt(M))`, expanding logarithms of the falling factorials gives

\[
\frac{(M-d)_k(M)_k}{(2M-d)_{2k}}
=4^{-k}\exp\!\left(O_d\!\left(\frac{k+k^2}{M}\right)\right)
=(1+o(1))4^{-k}.
\]

Also

\[
\operatorname{Cat}_{k-1}
\sim\frac{4^{k-1}}{\sqrt\pi\,k^{3/2}}.
\]

Thus the displayed conditional probability is `Theta(k^(-3/2))`. Taking `k` to be a sufficiently large constant multiple of `log M` makes `2k` exceed any prescribed `C log M`, while the unconditional event retains a constant factor `Pr(E_d)=Theta_d(1)`. Therefore the probability that even this first gap violates the cutoff is

\[
\Omega_d((\log M)^{-3/2})\gg M^{-1}.
\]

This implication is correct. It refutes the posted per-scale `O(1/M)` long-gap probability, not merely the claimed supermartingale.

### Uniformity for bounded variable `d(M)`

The preceding asymptotic is uniform when `d` may vary with `M` but remains in a fixed finite range `2<=d(M)<=D`. Indeed,

\[
\log\!\left(
4^k\frac{(M-d)_k(M)_k}{(2M-d)_{2k}}
\right)
=O_D\!\left(\frac{k+k^2}{M}\right),
\]

uniformly over all such `d`. Also

\[
2\frac{(M)_d}{(2M)_d}\longrightarrow 2^{1-d}
\]

uniformly over the finite set `d in {2,...,D}`; in particular it is bounded below by a positive constant depending only on `D` for all sufficiently large `M`. With

\[
k=\left\lceil\frac{C\log M}{2}\right\rceil+1,
\]

we have `k=o(sqrt(M))`, `2k>C log M`, `k<=M-d`, and, uniformly because `d<=D`,

\[
2k+1<2M/D\le 2M/d
\]

for all sufficiently large `M`. Consequently there is a constant `c_D>0` such that, for every admissible function `d(M)` and every sufficiently large admissible `M`,

\[
\Pr[T_{\rm bal}>C\log M]
\ge c_D(\log M)^{-3/2}.
\]

This is eventually larger than `K/M` for every fixed `K`. The conclusion is therefore genuinely uniform over `d(M)<=D`; it is not merely a separate pointwise statement for each fixed `d`.

The constant can be chosen independently of `C`: a universal Catalan lower constant, a fixed lower bound on `Pr(E_d)` over the finite set `2<=d<=D`, and (say) a factor `1/2` lower bound on the falling-factorial error suffice. Only the threshold from which the estimate holds depends on `C,D` (and the final comparison threshold also on `K`). This validates the `c_D` quantifier in CF-O1 as written.

## 3. Tie and reveal-policy scope

### Uniform ties are not needed for Proposition 4.1

On the selected event, a fresh correcting sign is the unique minimizer. A fresh bad sign makes all `d` active frontiers have that same sign. Any tie rule that consumes one frontier using only the revealed past leaves `d-1` bad cached frontiers. The next selected index remains measurable before its unseen color is exposed, so the ordered-hypergeometric law survives.

Accordingly, Proposition 4.1 extends verbatim from uniform ties to deterministic or randomized **nonanticipating** tie policies. It does not cover policies that inspect additional, deeper points or consume more than one frontier per step.

Here “nonanticipating” must mean that the chosen tied frontier is measurable with respect to the complete revealed-state filtration plus private randomness independent of the coloring, before the color of the next uninspected point is exposed. The policy may depend on `M`, `d`, block labels, load history, all cached colors, and all earlier private coins. It need not be stationary, symmetric, or uniform. Conditional on any such policy's past, the next selected uninspected index is fixed before its color is known; exchangeability of the uniformly random balanced coloring then gives exactly the same ordered-hypergeometric word probability. Thus the bounded-`d(M)` lower bound above is uniform over this entire policy class. A rule using information about an unexposed color, or revealing extra points before selecting, lies outside the proved class.

### Initial `H=0` reveal ambiguity

At `H=0`, every candidate gives absolute imbalance one. A query-minimal implementation can toss the certain-tie coin before inspecting unchosen candidates. Proposition 4.1 explicitly says to inspect all active frontiers, so it is correct for its stated eager process, but its initial event does not literally occur in this query-minimal variant.

The heavy-tail obstruction nevertheless has a direct query-minimal analogue. Consume the first selected point, with sign `s`. At the next, nonzero-height step, condition on all `d` required frontiers having sign `s`, and consume one. Let this event be `E'_d`. Then

\[
\Pr(E'_d)=\frac{(M-1)_d}{(2M-1)_d}=\Theta_d(1).
\]

After `E'_d`, `|H|=2`, there are `d-1` cached bad frontiers, and the unseen population has `M-d-1` bad signs and `M` correcting signs. A first-passage word of length `2k+1`, containing `k` bad and `k+1` correcting signs and staying nonnegative before its final step, returns from height two to the balanced band for the first time. There are `Cat_k` such words, giving

\[
\Pr(T_{\rm bal}=2k+1\mid E'_d)
\ge
\operatorname{Cat}_k
\frac{(M-d-1)_k(M)_{k+1}}{(2M-d-1)_{2k+1}},
\]

provided `k<=M-d-1` and `2k+3<2M/d`. For fixed `d` and `k=o(sqrt(M))`, this is again `Theta(k^(-3/2))`.

This independently derived extension is a proof candidate recorded here to clarify robustness; it is not present in the proposer report, not formalized, and not novelty-audited. The original Proposition 4.1 does not need this extension for correctness because it explicitly freezes eager exposure.

## 4. Does Proposition 4.1 rule out the construction family?

It rules out exactly the following claimed contract:

\[
\Pr[\text{every probe gap is at most }C\log m]
\ge 1-O(1/m)
\]

for the fixed-`d`, one-frontier-consumed cached process. The first-gap lower bound already contradicts that inequality. It also rules out any valid potential or fixed-bias stochastic domination that would imply the same false tail.

It does **not** prove that

\[
\Pr[\text{every gap is at most }C\log m]
\]

is negligible or below every inverse polynomial, because the certified probability of one long first gap tends to zero. Nor does it count the distinct subsets required by a hypothetical compressed long-gap handler. The report is correct to leave a “quantitatively weaker return theorem plus compressed cover” open.

The A/B/C matrix should therefore read “the posted logarithmic high-confidence A target is false” rather than the unqualified phrase “all actual-filtration control fails.”

### Direct audit of CF-O1

The theorem in `construction_family_obstruction.md` is a **PASS** after reading its quantifiers as `D>=2` integral and `C,K>0` fixed independently of `M`. Its unconditional claim follows by multiplying the conditional Catalan probability by

\[
\Pr(E_d)=2(M)_d/(2M)_d,
\]

which is uniformly bounded below for `2<=d<=D`. The room condition is uniform as well, and the exchangeability proof is valid after conditioning on any private-coin realization of any nonanticipating policy. Thus one may choose a common `c_D>0` and a sufficiently-large threshold depending on `C,D,K`, but not on the policy or on the particular admissible function `d(M)`.

Three presentation corrections are still required. First, Section 1's phrase “one positive-probability boundary event” is too weak in isolation: a merely positive event could have probability `o(1/M)`; the proof uses the stronger uniform constant lower bound for `E_d`. Second, write `C,K>0` and `k>=1` explicitly. Third, the label `CF-O1` is dangerously close to the main target `O01`; an identifier such as `CF-LOGGAP` better preserves the theorem's restricted meaning. None of these defects invalidates the theorem.

## 5. Proposition 5.1: variable residual threshold

Assume `g(m),d(m),b>=0`. If `r<2(d(m)+b)`, then a tail of size at most `g(m)` plus the entire residual has size strictly less than

\[
g(m)+2d(m)+2b.
\]

If `r>=2(d(m)+b)`, and a descent consumes at most `d(m)` residual points, then

\[
r-d(m)\ge r/2,
\qquad
r-d(m)\ge d(m)+2b\ge b.
\]

The segment identity remains the residual of size `r<=m^alpha`. These three arithmetic conclusions are correct. I checked them independently over a grid of integer `r,d,b`, in addition to rerunning the proposer script.

### What the proposition actually repairs

It repairs the false inference from an upper residual bound to a lower residual bound. For example, `m'=10^12` and `r=700` obey `r<=(m')^(2/3)` and enter the original fixed-`M0` recursive case, but

\[
\log m' > \tfrac32\log r+1.
\]

Nothing about the upper bound alone prevents this.

The variable threshold ensures sufficient **numerical reserve after a granted descent**. It does not establish a full valid scale transition unless the following are added:

1. the tail begins and the descent ends at balanced-band sets, so the claimed union really is a gap-fillable transition;
2. the descent is operationally defined and succeeds before exhausting the residual structure;
3. odd residual sizes have a defined block split or padding rule;
4. the next-scale A/B good event is uniform over the partially consumed start state, whose effective population lies only in `[r/2,r]`;
5. the distinction between segment size `r` and effective unconsumed size is maintained in every subsequent hypothesis; and
6. the local pattern budget is enlarged to cover the new absorption threshold.

The last item changes the posted constants. Plugging the withdrawn manuscript's displayed bounds

\[
g(m)=28\log m,\qquad d(m)=8+32\log m,\qquad b=350
\]

gives an absorption-gap budget below

\[
92\log m+716,
\]

not the original `60 log m+700`. This remains polynomial accounting, but the local system and its exponent must be changed.

**Disposition:** Proposition 5.1 is a sound reserve-arithmetic lemma and a useful bounded B diagnostic. Calling it a complete “transition repair” without the six closure conditions would overstate it. The proposer report mostly respects this limit but should make the budget change and closure assumptions explicit at integration.

The executable `verify_threshold_repair()` tests one numerical choice of `m`, `b`, `g`, and `d`. It is not a proof of the quantified proposition; the two-line algebra above is the proof.

As a finite regression check independent of that function, I exhaustively tested all `44,541` integer triples `0<=d,b<=20` and `0<=r<=100`; every triple satisfied the appropriate absorption or recursion inequalities. This is not used as an asymptotic proof.

## 6. Proposition 6.1: distinct-subset accounting

Suppose the hypotheses are global: conditional on each current segment, there are at most `m_j^b` possible next residual/nesting descriptions across **all** colorings and random histories, and for each such description there is one fixed, coloring-independent family of at most `m_j^c` possible local subsets covering all executions.

For one fixed depth `J`, the number of description/local-pattern tuples is at most

\[
\prod_{j=0}^Jm_j^{b+c}.
\]

Since `m_{j+1}<=m_j^alpha`,

\[
\log m_j\le\alpha^j\log n,
\qquad
\sum_{j=0}^J\log m_j\le\frac{\log n}{1-\alpha}.
\]

Therefore every fixed-depth tuple count is at most

\[
n^{(b+c)/(1-\alpha)}.
\]

If recursion stops upon reaching a fixed threshold, the recurrence forces `J_max=O(log log n)`. Summing over the possible current depths gives

\[
|S_n|\le(J_{\max}+1)n^{(b+c)/(1-\alpha)}=n^{O(1)}.
\]

Mapping tuples to composite unions cannot increase cardinality, so collisions are harmless. This proof is correct.

### Necessary wording correction

The local `m_j^c` family must be one global family after the residual object is fixed, not a different size-`m_j^c` family selected separately for each coloring. A per-execution reading is false: every coloring could select one subset, while the union over colorings contains exponentially many subsets. Likewise the `m_j^b` residual description count must include the segment's identity, not merely its length.

With those explicit globality conditions, Proposition 6.1 is a complete C-accounting lemma conditional on power shrink and local polynomial families. FLSY Lemma 2.3 then adds the stated `O(n/epsilon)` factor to a fixed average-case set system, so inverse-polynomial `epsilon` preserves polynomial size. This does not supply average success.

The report's sentence extending the lemma to “a fixed number of residual intervals” needs one more hypothesis. A fixed branching factor by itself is not enough: if every segment recursively spawns `s>1` children, the log-count can involve

\[
\sum_j s^j\alpha^j\log n,
\]

which is not bounded by the one-path geometric series when `s\alpha>=1`. The extension is valid if the multiple intervals form one jointly described next-scale object already covered by the stated `m_j^b,m_j^c` bounds and there remains only one nested scale path, or if a stronger aggregate contraction/counting condition (for example, a uniform contraction of total logarithmic size) is proved. Proposition 6.1 itself is a PASS for its singular nested execution; the multi-residual aside is **UNPROVED AS WRITTEN** under a branching-recursion reading.

The proposer's floating-point check for one synthetic logarithmic sequence is only a regression check. The geometric-series derivation is the exact proof.

## 7. DR-1: polynomially many fixed orders

Freeze constants `C,K>0` and `0<alpha<1`. Let `T(n)<=n^C` permutations be chosen independently of the coloring. Call one order good if the associated uniform bridge of length `n=2q` has every zero-to-zero excursion of length at most `K n^alpha`.

FLSY Lemma 3.2 says, for `a>=q^(2/3)`,

\[
\Pr[\lambda(B)\le2a]
=C(q,a)\min\{(q+1)^{-1/2},a^{-1/2}\}
\exp(-\beta q/a),
\]

with universal positive constants bounding `C(q,a)`.

To account exactly for the hidden constant in `K n^alpha`, take

\[
a_q=\max\{q^{2/3},(K/2)(2q)^\alpha\}.
\]

The desired event is contained in `{lambda(B)<=2a_q}`. Hence

\[
\Pr[\text{one fixed order is good}]
\le C_2\exp(-c q^\delta),
\qquad
\delta=\min\{1/3,1-\alpha\}>0,
\]

for a constant `c=c(K,alpha)>0`. At `alpha=2/3`, this max construction also handles either side of the source lemma's threshold. Thus

\[
T(n)\Pr[\text{one order good}]
\le n^C C_2\exp(-c(n/2)^\delta)<1
\]

for all sufficiently large even `n`. By the union bound, some balanced coloring defeats every order in the fixed polynomial list.

The report's conclusion is correct. Its shorthand “apply with `a=q^alpha`” suppresses the factor `K`, the conversion `n=2q`, and the threshold issue at `alpha=2/3`; these are harmless asymptotically but should be replaced by the `a_q` expression above in a fully frozen statement.

### Exact scope

DR-1 obstructs only a scheme in which one top-level order from a polynomial list must itself have all zero-to-zero gaps bounded by `K n^alpha`. It does not apply if a construction:

- splices choices from several orders before a whole top-level order is selected;
- represents exponentially many chains through a polynomial shared-state DAG;
- uses visits to `|H|=1` rather than the frozen zero-to-zero gaps;
- uses an `n`-dependent `alpha` tending to one; or
- uses an unrelated balanced-chain set system.

The report correctly warns that exponentially many required order descriptions do not imply exponentially many **distinct subsets**, because different chains can share states. Therefore DR-1 is a restricted fixed-order coverage obstruction, not a lower bound on arbitrary set systems or on `N(n)`.

For quantitative precision, “exponentially many order descriptions” should be written as `exp(Omega(n^delta))` with `delta=min{1/3,1-alpha}`. This is superpolynomial and exponential in a positive power of `n`, but for `delta<1` it is not a `2^{Omega(n)}` lower bound.

## 8. Additional formula and classification checks

1. **Long-horizon drift (10.1): pass.** With `d-1` cached pluses, the unseen population has size `R-d+1` and signed sum `-(h+d-1)`. Before a possible sign crossing, the sum of `L` consumed signs equals an ordered sample of `L` fresh signs, so its expectation is exactly `-L(h+d-1)/(R-d+1)`. The guard `h>L` is sufficient.
2. **NA-1 posterior example: pass.** The revealed consumed signs `+,-,+`, deferred signs `-,-,-`, and unseen signs `+,+,+,-` total zero. At `H=1`, a fresh pair is all bad with probability `binom(3,2)/binom(4,2)=1/2`.
3. **NA-2 batch expectation: pass.** A size-`d` sample from a pool of size `R` and sum `-H` has expected sum `-dH/R`, independent of internal ordering.
4. **Growing-`d` grid warning: pass for the full-grid template.** `(m/d+1)^d` has no fixed polynomial exponent when `d` is unbounded. This does not rule out a compressed non-grid representation.
5. **Epistemic labels:** the JSON certificate's `COMPUTATIONALLY_TESTED_FINITE_DIAGNOSTICS_ONLY` label is appropriate. Propositions 4.1, 5.1, and 6.1 are mathematical proof candidates supported by written derivations, not established merely by the script. Following this audit, Proposition 4.1 and DR-1 may be described as internally adversarially validated and unformalized, but not as novel or externally validated.

## 9. Concrete integration corrections

1. Replace the outcome sentence “the stopping rule is reached only at a bounded B/C diagnostic” with: **Stop A reached for the greedy, uniformly bounded-`d`, single-consumption cached-frontier process and its posted `1-O(1/M)` logarithmic direct-gap guarantee. Stop and reassess this construction family. No broader fixed-`d`, mABP, `N(n)`, or O01 obstruction is claimed.**
2. In Proposition 4.1 add `k>=1`, define `E_d` purely as the same-sign frontier event, and note that the Catalan obstruction works for arbitrary nonanticipating tie policies. Define nonanticipation against the full reveal filtration and require policy coins to be independent of the coloring.
3. Describe PS-1/DB-d as falsifying the **posted `O(log m)` / `O(1/m)` A conclusion**, not every conceivable actual-filtration theorem.
4. Rename Proposition 5.1 in summaries to “variable-threshold reserve lemma” unless parity, next-scale closure, endpoint assumptions, and enlarged local budgets are supplied.
5. In Proposition 6.1 explicitly quantify the residual and local families over all colorings, coins, and executions, and require their descriptions to include segment identity.
6. Do not invoke the fixed-number-of-residuals extension of Proposition 6.1 for a branching recursion without an aggregate contraction/counting hypothesis.
7. In DR-1 freeze `K,C,alpha` and use `a_q=max(q^(2/3),(K/2)(2q)^alpha)` to handle constants and the source theorem's threshold exactly; state its order lower bound as `exp(Omega(n^delta))`, not ambiguously as fully exponential.
8. In `construction_family_obstruction.md`, replace “one positive-probability boundary event” by the quantitatively sufficient fact that `E_d` has probability bounded below uniformly for `d<=D`; state `C,K>0`; and retain the unconditional multiplication by `Pr(E_d)`.
9. Rename `CF-O1` to `CF-LOGGAP` (or similarly explicit notation) so it cannot be mistaken for target O01. Once integrated, update its metadata from “pending independent adversarial audit” to “internally adversarially validated; unformalized”; do not make a novelty or external-validation claim.
10. Continue to state prominently that none of these results proves or refutes unrestricted `N(n)` or O01.

## Final verdict

The proposer report's central negative mathematics is sound. Proposition 4.1 and CF-O1 pass for the frozen eager cached-frontier family, uniformly over bounded `d(M)` and all nonanticipating tie policies; DR-1 is a valid fixed-order union-bound obstruction. Proposition 5.1 and the singular-path form of Proposition 6.1 are correct at their intended arithmetic/accounting level, but their hypotheses must be made operationally global before they are used as construction components. The multi-residual branching aside following Proposition 6.1 does not follow from the displayed one-path proof without an additional aggregate contraction condition.

The strongest warranted Cycle-2 conclusion is a **restricted method obstruction**: the unchanged fixed/bounded-`d`, one-frontier-consumed process cannot support the posted logarithmic direct-gap estimate with `O(1/m)` failure. Nothing here decides O01 or unrestricted `N(n)`.

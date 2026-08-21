# Research Cycle 4: independent symmetrization audit

**Base commit audited:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Date:** 2026-08-21
**Role:** independent Phase 4A prover / adversarial checker
**Overall disposition:** **PASS**
**Epistemic status:** the qualitative reduction is a direct instance of a
published FLSY lemma, not a new theorem.  The exact integer thresholds and
rankwise literal-union bound below are elementary derived refinements;
`INDEPENDENTLY RECONSTRUCTED; UNFORMALIZED`.

This report does not assume that the Cycle-3 conclusions are correct.  It
reconstructs from the literal definitions every fact used by the reduction.
It does not prove a lower bound on the RR acceptance probability, and hence
does not prove O01.

## 1. Verdict

Let \(n=2m\) be positive and even, let \(\mathcal B_n\) be the set of all
balanced sign functions \(f:[n]\to\{-1,+1\}\), and put

\[
M_n=|\mathcal B_n|=\binom n{n/2}.
\]

Let \(\mathcal F\subseteq 2^{[n]}\) be any fixed literal set family, and let
\(A(\mathcal F)\) be the fraction of \(\mathcal B_n\) accepted by its full
induced subset DAG.  Then, for a fixed balanced \(f\) and a uniformly random
permutation \(\pi\in S_n\),

\[
\Pr_\pi[\pi(\mathcal F)\text{ accepts }f]=A(\mathcal F).
\]

For independent uniform \(\pi_1,\ldots,\pi_t\),

\[
\Pr[f\text{ is rejected by every }\pi_j(\mathcal F)]
=(1-A(\mathcal F))^t.
\]

Consequently,

\[
\Pr[\text{some balanced }f\text{ is rejected by all copies}]
\le M_n(1-A(\mathcal F))^t.                 \tag{1}
\]

Thus a single fixed list exists whenever the right side of (1) is **strictly
less than one**.  Applied to the corrected Cycle-3 family \(RR_n\), this proves
the proposed implication.  There is no orientation, odd-intermediary, or
fixed-family gap.  The only material qualification is that the list is
nonuniform and nonconstructive; that is sufficient for the existential
quantity \(N(n)\).

## 2. Literal definitions and the only RR fact needed

For \(S\subseteq[n]\), write

\[
d_f(S)=\sum_{x\in S}f(x).
\]

A family \(\mathcal F\) accepts \(f\) when it contains a maximal chain

\[
\varnothing=C_0\subset C_1\subset\cdots\subset C_n=[n]
\]

with \(|d_f(C_i)|\le1\) at every rank.  Equivalently, this is a source--sink
path through the full inclusion-by-one DAG induced by the **literal subsets**
of \(\mathcal F\).  This definition includes both even and odd ranks.

The symmetrization proof does not use the deque recurrence, the claimed
all-\(n\) RR countercolor, the canonical-support quotient, or any conclusion
about generating paths.  It uses only that \(RR_n\) is a fixed literal family
and its literal size/rank profile.

That profile can be rederived directly.  Put \(q=n-1\), identify the ground
set with \(\mathbb Z_q\cup\{\infty\}\), and for each \(r\in\mathbb Z_q\) take
the prefix sets of

\[
(r,\infty,r+1,r-1,r+2,r-2,\ldots,r+(m-1),r-(m-1)).
\]

The empty and full sets are common to all orders.  At rank one the sets are
the \(q\) distinct singletons \(\{r\}\).  At every rank
\(2\le k\le n-1\), the sets are \(\{\infty\}\) joined to the \(q\) cyclic
intervals of proper length \(k-1\) in \(\mathbb Z_q\); different starting
points give different proper cyclic intervals.  Hence

\[
|RR_n\cap\tbinom{[n]}k|=
\begin{cases}
1,&k=0,n,\\
n-1,&1\le k\le n-1,
\end{cases}
\qquad
|RR_n|=(n-1)^2+2.                             \tag{2}
\]

This argument also covers \(n=2\): there is one order and three prefixes.

## 3. Exact equivariance

For a permutation \(\pi\), define

\[
\pi(\mathcal F)=\{\pi(S):S\in\mathcal F\},
\qquad
\pi(S)=\{\pi(x):x\in S\}.
\]

The map \(S\mapsto\pi(S)\) is a rank- and inclusion-preserving isomorphism
between the two full induced subset DAGs.  Moreover, for every \(S\),

\[
d_f(\pi(S))
=\sum_{y\in\pi(S)}f(y)
=\sum_{x\in S}f(\pi(x))
=d_{f\circ\pi}(S).                            \tag{3}
\]

Mapping every member of a witness chain by \(\pi\), and applying the inverse
map in the other direction, proves the exact biconditional

\[
\pi(\mathcal F)\text{ accepts }f
\quad\Longleftrightarrow\quad
\mathcal F\text{ accepts }f\circ\pi.          \tag{4}
\]

This proves more than preservation of the listed RR seed paths: it preserves
every hybrid path in the full induced subset DAG.

## 4. Why the pulled-back coloring is uniform

Fix \(f\in\mathcal B_n\).  For any \(h\in\mathcal B_n\), the condition
\(f\circ\pi=h\) says that \(\pi\) maps the \(m\) positive points of \(h\)
bijectively to the \(m\) positive points of \(f\), and likewise maps the
negative points bijectively.  Exactly

\[
m!\,m!
\]

permutations do this, independently of \(h\).  Therefore \(f\circ\pi\) is
uniform on \(\mathcal B_n\).  Combining this fiber count with (4) gives

\[
\Pr_\pi[\pi(\mathcal F)\text{ accepts }f]
=\frac{|\{h\in\mathcal B_n:\mathcal F\text{ accepts }h\}|}{M_n}
=A(\mathcal F).                                \tag{5}
\]

No transitivity assertion about RR automorphisms is being used.  Uniformity
comes from sampling the full symmetric group.

## 5. Independence and the exact union-bound threshold

For fixed \(f\), the event that \(\pi_j(\mathcal F)\) rejects \(f\) is a
function only of \(\pi_j\).  The permutations are independent, so the events
are independent.  Equation (5) therefore gives

\[
\Pr[\forall j,\ \pi_j(\mathcal F)\text{ rejects }f]
=(1-A)^t.                                      \tag{6}
\]

Taking the union over all \(M_n\) balanced colorings gives (1).  Events for
different colorings need not be independent; the union bound does not assume
that they are.

For \(0<A<1\), the least positive integer \(t\) for which the literal
all-coloring union bound is strictly below one is

\[
T_{\rm all}(n,A)
=\left\lfloor
  \frac{\ln M_n}{-\ln(1-A)}
 \right\rfloor+1.                              \tag{7}
\]

The floor-plus-one, rather than an unqualified ceiling, is necessary: if the
ratio in (7) is an integer, equality would leave the union-bound upper bound
equal to one and would not prove positive probability.  The endpoint cases
are

\[
T_{\rm all}(n,1)=1,
\qquad
T_{\rm all}(n,0)=\infty
\]

for this particular individual-copy coverage argument.  The latter does not
rule out a union becoming valid through new hybrid paths.

If exactly \(a\) of the \(M_n\) colorings are accepted, so \(A=a/M_n\), the
same strict condition has the exact integer form

\[
(M_n-a)^t<M_n^{\,t-1}.                         \tag{8}
\]

Equations (7)--(8) give the threshold certified by this union bound, not a
claim that fewer relabelings can never work.  Correlations between different
colorings, and hybrid paths in the final union, can only improve existence.

### Global-sign deduplication

For every literal family, acceptance of \(f\) is identical to acceptance of
\(-f\), because every discrepancy is negated and its absolute value is
unchanged.  The \(M_n\) conditions therefore occur in identical pairs.  If
one first unions over the \(M_n/2\) sign orbits, the sharper sufficient
condition is

\[
\frac{M_n}{2}(1-A)^t<1,                        \tag{9}
\]

and for \(0<A<1\) its exact threshold is

\[
T_{\pm}(n,A)
=\left\lfloor
  \frac{\ln(M_n/2)}{-\ln(1-A)}
 \right\rfloor+1.                              \tag{10}
\]

The requested union bound over all balanced colorings is (7).  Formula (10)
is a valid deterministic sharpening because the paired bad events are
literally the same event, not merely events of the same probability.

This also explains the normalized-word convention used by the Cycle-3 RR
search.  Fixing the color of \(\infty\) to be negative chooses exactly one
member of every \(\{f,-f\}\) pair.  Hence, if \(a^-\) of the normalized words
are accepted, then

\[
A_n=\frac{a^-}{\binom{n-1}{n/2}},              \tag{11}
\]

with no extra factor of two.

## 6. One fixed union and its distinct-subset count

Assume the strict inequality in (1), and choose a realization
\((\pi_1,\ldots,\pi_t)\) outside the bad event.  Define the literal family

\[
\mathcal Y=\bigcup_{j=1}^t\pi_j(RR_n).         \tag{12}
\]

This is one family fixed simultaneously for all colorings.  For every
balanced \(f\), at least one copy \(\pi_j(RR_n)\) accepts \(f\) in its full
induced DAG.  Its witness chain consists of literal members of that copy and
therefore lies in \(\mathcal Y\).  Thus \(\mathcal Y\) is a
1-balanced-chain family.  New paths that splice different copies do not
invalidate anything and may accept additional colorings.

The exact accounting identity is by rank:

\[
|\mathcal Y|
=2+\sum_{k=1}^{n-1}
 \left|\bigcup_{j=1}^t
   \pi_j\!\left(RR_n\cap\binom{[n]}k\right)
 \right|.                                      \tag{13}
\]

Using (2), this gives the distinct-literal-subset bounds

\[
|\mathcal Y|
\le
2+\sum_{k=1}^{n-1}
  \min\left\{\binom nk,\ t(n-1)\right\}
\le 2+t(n-1)^2.                                \tag{14}
\]

These are cardinalities of set unions.  They do not count permutations,
descriptions, generating paths, matching factors, abstract states, or edges.
The first inequality allows every possible collision between copies; the
last is an upper bound, not generally an equality.  The two endpoint subsets
are counted once, and all odd ranks are already included.

## 7. The inverse-polynomial premise implies O01

Suppose that there are absolute constants \(c\) and \(n_0\) such that

\[
A_n\ge n^{-c}
\]

for every even \(n\ge n_0\).  We may take \(c\ge0\).  The explicit integer
choice

\[
t_c(n)=\left\lfloor
 n^c\ln\binom n{n/2}
\right\rfloor+1                              \tag{15}
\]

is sufficient.  Indeed, \(t_c(n)>n^c\ln M_n\), so

\[
A_nt_c(n)>\ln M_n,
\qquad
M_n(1-A_n)^{t_c(n)}
\le M_ne^{-A_nt_c(n)}<1.                       \tag{16}
\]

Equations (14)--(16) give

\[
N(n)
\le 2+(n-1)^2
 \left(\left\lfloor n^c\ln\binom n{n/2}\right\rfloor+1\right)
=O(n^{c+3})                                   \tag{17}
\]

for all sufficiently large even \(n\).  In particular,
\(\ln M_n<n\) and, for \(n\ge2\),

\[
t_c(n)\le2n^{c+1},
\qquad
N(n)\le n^{\lceil c\rceil+5}.                 \tag{18}
\]

There is no asymptotic-to-all-\(n\) gap.  For each of the finitely many
positive even \(n<n_0\), the full Boolean lattice is a valid family, so
\(N(n)\le2^n\le n^n\).  For example, after replacing \(n_0\) by an integer
at least two, the single absolute exponent

\[
C=\max\{\lceil c\rceil+5,n_0\}
\]

works for every positive even \(n\).  This establishes the conditional
implication to O01, not its unproved premise.

## 8. Primary-source attribution: this is FLSY symmetrization

The qualitative implication is already known and must not be claimed as a
new theorem.

Fabris, Limaye, Srinivasan, and Yehudayoff define average-case
balanced-chain systems in Definition 5 and state their worst/average
conversion as Lemma 6, restated formally as Lemma 14, in the published
[CCC 2026 proceedings article](https://doi.org/10.4230/LIPIcs.CCC.2026.22).
It says that an \((\varepsilon,k)\)-balanced-chain family of size \(s\) yields
a worst-case \(k\)-balanced-chain family of size \(O(sn/\varepsilon)\).
The complete proof is Lemma 2.3 (also identified there as Lemma 1.5) of the
[ECCC TR26-001 full version](https://eccc.weizmann.ac.il/report/2026/001/download/).
That proof takes independent random permutations, pulls a fixed coloring
back to a uniform balanced coloring, and applies a union bound.  In the full
version's notation it chooses
\(r=\lceil n/(p\,\lg e)\rceil\), adjoins the original family as well as the
\(r\) permuted copies, bounds the coloring universe by \(2^n\), and obtains
size \((r+1)s=O(sn/p)\).

Set \(k=1\), \(\varepsilon=A_n\), \(s=(n-1)^2+2\), and
\(\mathcal F=RR_n\).  This is exactly Phase 4A.  Equations (7), (13), and
(14) only sharpen the constants by using the exact number of balanced
colorings, the exact rejection probability, shared endpoints, rank bounds,
and no unnecessary additional identity copy.  No novelty is claimed for
these elementary refinements.

## 9. Hidden-hypothesis audit

| Possible issue | Disposition |
|---|---|
| **Uniformity / constructivity** | The proof is a nonuniform probabilistic-existence argument for one family at each \(n\).  It does not efficiently find or explicitly describe the permutation list.  This is sufficient for the definition of \(N(n)\), but not for an explicit/uniform construction claim. |
| **Fixed family** | \(RR_n\) is fixed before the random permutation and before the adversarial coloring.  Positive probability in (1) selects one list that works for all colorings simultaneously.  A coloring-dependent base family would not justify this step. |
| **Orientation** | Relabeling maps the oriented RR prefix chains and every hybrid induced-DAG chain isomorphically.  Equation (3) fixes the potentially confusing \(\pi\) versus \(\pi^{-1}\) convention.  No cyclic orientation must be preserved. |
| **Odd intermediaries** | Every relabeled copy is an all-rank literal subset family.  Bound (13) counts odd ranks.  No contraction to even supports, and hence no later intermediary expansion or edge-to-subset conversion, is used. |
| **Hybrid paths** | \(A_n\) must be computed using the full induced DAG, as stipulated.  Hybrid paths inside one copy are preserved.  Hybrid paths between different copies only enlarge the accepted set and are not needed for the sufficiency proof. |
| **Independence** | Independence is required only across the sampled permutations for a fixed coloring.  No false independence assumption is made across different colorings.  Sampling with replacement is allowed; duplicate copies can later be removed. |
| **Global sign** | Full-color and sign-normalized acceptance fractions agree by (11).  Counting normalized words as though they were all signed colorings would introduce a factor-of-two error in raw counts, though not in \(A_n\). |
| **Odd ground-set size** | The proof is only for positive even \(n\).  For odd \(n\), balanced sign functions do not exist under this definition and the universal property would become vacuous; no odd case is used. |
| **Strictness** | The union-bound upper bound must be \(<1\), not \(\le1\).  Formula (7) handles the integer equality case correctly. |
| **Size measure** | Bound (14) counts distinct literal subsets.  A polynomial number of permutation descriptions alone would not suffice without this union bound on their literal members. |

No invalidating hidden hypothesis was found.

## 10. Edge cases and finite sanity checks

### \(n=2\)

Here \(RR_2=\{\varnothing,\{0\},\{0,1\}\}\), up to naming the two points.
Every balanced coloring gives opposite signs to the two points, so this sole
maximal chain is 1-balanced.  Thus

\[
A_2=1,\qquad T_{\rm all}(2,A_2)=1,
\qquad |RR_2|=3=N(2).
\]

A permutation swapping the two labels produces the other three-set maximal
chain, which is also valid.  There is no \(0^0\) convention in the proof:
the \(A=1\) case is handled separately.

### \(n=22\) checker sanity test (finite only)

The two independent Cycle-3 RR checkers, rerun below, both find 21 rejected
normalized words among
\(\binom{21}{11}=352716\).  If that finite exhaustive result is accepted,
then

\[
1-A_{22}=\frac{21}{352716}=\frac1{16796}.
\]

The all-coloring union bound is 42 for one copy and less than 0.003 for two
copies, so (7) returns \(t=2\).  This is only a finite consistency check; it
has no asymptotic implication and is not used in the proof above.

## 11. Independent verification record

The following commands were run from the repository root at the audited
commit:

```powershell
python -B experiments/cycle03_verify_foundation.py
python -B experiments/cycle03_check_cp_m_matching.py
python -B audits/check_cycle03_cp_m_adversarial.py
```

All exited with status zero.  Relevant outputs were:

- the foundation checker independently matched literal and contracted path
  acceptance and handled the even/odd domain boundary;
- the proposer checker confirmed \(|RR_n|=(n-1)^2+2\), full induced-DAG/deque
  agreement through its finite range, coverage through \(n=20\), and the
  first finite failure at \(n=22\);
- the separately implemented adversarial checker confirmed the exact RR
  rank profile through \(n=22\), independently propagated reachable cyclic
  intervals, compared them with a literal induced-DAG search through
  \(n=12\), and again obtained exactly 21 normalized failures at \(n=22\).

These computations corroborate the literal RR dependency and the finite
sanity check.  The symmetrization proof itself is exact and does not depend on
finite experimentation.

## 12. Final epistemic disposition

- **FLSY average-to-worst-case symmetrization:** `KNOWN`, published; the
  present reduction is an immediate specialization.
- **Equivariance, exact product probability, strict threshold (7), and
  distinct-subset bounds (13)--(14):** `INDEPENDENTLY RECONSTRUCTED;
  UNFORMALIZED` elementary consequences.
- **Implication \(A_n\ge n^{-O(1)}\Rightarrow\) O01:** `RIGOROUS CONDITIONAL
  COROLLARY`; its premise remains open in this audit.
- **O01:** `OPEN`.  No experimental acceptance rate is promoted to an
  asymptotic theorem.

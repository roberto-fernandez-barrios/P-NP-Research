# Cycle 4 adversarial audit: rooted `RR_n` interval obstruction

**Date:** 2026-08-21
**Base state audited:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
plus the Cycle-4 proof candidate and certificates
**Role:** independent Phase 4C/4F falsifier and theorem validator
**Verdict:** **PASS, with a one-sided-notation correction recorded below**
**Epistemic status:** mathematical proof independently reconstructed and
finite-checked; FLSY input is a published known theorem; Lean formalization
was not part of this audit

## 1. Verdict and exact scope

The following implication is correct for the literal corrected one-cycle
family `RR_n`.  If `n=2m` and `p_N` is the acceptance probability of the
ordinary one-interval family `I_(N,1)` under a uniform balanced coloring, then

```text
A_n <= m p_(n-2).                                      (1)
```

Fabris--Limaye--Srinivasan--Yehudayoff (FLSY) prove that a universal
constant `c>0` exists for which

```text
p_N <= 2^(-c N^(1/5))                                  (2)
```

for every sufficiently large even `N`.  Therefore, after changing the
absolute constant if needed,

```text
A_n <= (n/2) 2^(-c (n-2)^(1/5))
    <= 2^(-c' n^(1/5))                                 (3)
```

for every sufficiently large even `n`.  In particular, no subclass contained
in the accepted colorings can have inverse-polynomial measure under the
uniform balanced-coloring distribution for all sufficiently large `n`.
This reaches the requested S4-D obstruction for the proposed lower bound on
`A_n` and the individual-copy random-relabeling route.

This verdict does **not** show any of the following:

* that a polynomial literal union of relabeled copies is rejected by some
  coloring;
* that hybrid chains formed from subsets belonging to different copies are
  rare;
* a lower bound on arbitrary 1-balanced-chain families or on `N(n)`; or
* any Boolean, algebraic, or P-versus-NP separation.

The separate finite multi-`RR` attack therefore remains logically outside
this obstruction.

## 2. Dependencies checked independently

I treated the Cycle-3 and Cycle-4 documents as claims, not as premises.  I
reconstructed the literal family from the corrected seed orders in
`research_cycle_03/cp_m_matching_equivalence.md`, inspected the independently
implemented literal family and recurrence in
`experiments/cycle04_rr_verify_counts.py`, and then rebuilt both induced DAGs
in a separate one-off checker.

The external dependency was checked in both primary versions:

* Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir Yehudayoff,
  *Multilinear Algebraic Branching Programs and the Min-Partition Rank
  Method*, [ECCC TR26-001 full version](https://eccc.weizmann.ac.il/report/2026/001/),
  especially Definitions 1.2, 1.4, and 2.1 and Theorem 4.4 (Theorem 1.7).
* The published [CCC 2026 paper](https://doi.org/10.4230/LIPIcs.CCC.2026.22),
  especially Definitions 5 and 11 and Theorem 23 (Theorem 8).

The full version proves the probability estimate rather than merely stating
it; the proceedings version omits part of the technical proof but states the
same theorem.  No secondary source is needed for (2).

## 3. Literal-family reconstruction

Put `q=n-1` and identify the ground set with

```text
U = Z_q union {infinity}.
```

The corrected seed starting at `r` is

```text
r, infinity, r+1, r-1, r+2, r-2, ... .
```

Its rank-one prefix is `{r}`.  At every rank `k` with `2<=k<=n-1`, its
finite prefix is one cyclic interval of length `k-1`, joined with infinity.
Varying `r` gives every start position of every proper interval length.  The
empty and full sets give the endpoints.  Thus the literal prefix union is
exactly

```text
rank 0:                  emptyset;
rank 1:                  all finite singletons;
rank k, 2<=k<=n-1:       {infinity} union I,
                         I a length-(k-1) cyclic interval in Z_q;
rank n:                  U.
```

This derivation gives `(n-1)^2+2` distinct subsets.  More importantly for the
obstruction, it confirms that every full induced-DAG chain, including a
hybrid chain not equal to a seed path, has the interval form used below.

## 4. Rooted equivalence reconstructed in both directions

Normalize a balanced coloring by global sign reversal so that
`f(infinity)=-1`.  This is measure-preserving on global-sign pairs and does
not change acceptance.  The finite cycle then has total sign `f(Z_q)=+1`.

Fix `r in Z_q`, and let `E_r` be the event that an accepted chain has
rank-one state `{r}`.  Any such chain is forced to have

```text
C_0 = emptyset,
C_1 = {r},
C_(j+1) = {infinity} union I_j       (1<=j<=q),
```

where

```text
I_1={r} subset I_2 subset ... subset I_q=Z_q,
|I_j|=j,
```

and every `I_j` is a cyclic interval.  In particular, rank two is
`{infinity,r}`.  Its discrepancy is an even integer of absolute value at
most one, hence is zero, so `f(r)=+1`.

Cut the cycle at `r` and linearly order

```text
V_r = Z_q \ {r}
```

as `r+1,r+2,...,r-1`.  Define, for `0<=s<=q-1`,

```text
J_s = Z_q \ I_(q-s).
```

The complement of a cyclic interval containing the cut point is an ordinary
interval in this line.  Reversing the inclusions gives

```text
emptyset=J_0 subset J_1 subset ... subset J_(q-1)=V_r,
|J_s|=s.
```

This is a maximal chain in the complete ordinary one-interval family, not a
selected generating path.  Its discrepancies satisfy the exact identity

```text
f(J_s)
  = f(Z_q)-f(I_(q-s))
  = 1-f(I_(q-s))
  = -f(C_(q-s+1)).                                   (4)
```

Also `f(V_r)=1-f(r)=0`.  Hence an `E_r` witness gives a balanced restriction
and an accepted ordinary interval chain.

Conversely, assume `f(r)=+1` and start with any accepted maximal ordinary
interval chain `J_0,...,J_(q-1)` on `V_r`.  Set

```text
I_j = Z_q \ J_(q-j),          1<=j<=q.
```

The complement of an ordinary interval in the cut line is a cyclic interval
containing `r`.  These `I_j` have the required sizes and inclusions, so the
displayed `C` sequence consists entirely of literal `RR_n` subsets.
Identity (4), read backwards, proves compatibility at every rank.  Thus

```text
E_r
iff
f(r)=+1 and I_(n-2,1) accepts f restricted to V_r.    (5)
```

### Endpoint, parity, and orientation audit

No rank is lost in this correspondence:

| ordinary state | corresponding `RR_n` state |
|---|---|
| `J_0=emptyset` | `C_n=U` |
| `J_s`, `1<=s<=q-2` | `C_(q-s+1)` |
| `J_(q-1)=V_r` | `C_2={infinity,r}` |
| separate initial condition | `C_1={r}` |
| separate endpoint | `C_0=emptyset` |

Consequently all odd intermediaries as well as all even ranks are checked
directly.  The proof does not contract two steps, choose a near-endpoint
orientation, or assume that the chain follows one original seed.  Empty and
full ordinary intervals are present: `I_(N,1)` allows a union of zero
intervals, and `[N]` is one interval.  The converse also rules out a hidden
necessary-only reduction.

## 5. Conditioning and the adaptive-root issue

There are `binom(q,m)` normalized colorings: the finite cycle has `m` pluses
and `m-1` minuses.  For a fixed root,

```text
Pr[f(r)=+1] = m/q.
```

Conditioning on this event leaves `m-1` pluses and `m-1` minuses uniformly
distributed on the fixed ordered set `V_r`.  Equivalently, the exact ratio
of sample-space sizes is

```text
binom(2m-2,m-1) / binom(2m-1,m) = m/(2m-1)=m/q.
```

If `p_(n-2)` denotes ordinary interval acceptance under that uniform
balanced law, (5) therefore gives the equality

```text
Pr[E_r] = (m/q) p_(n-2).                              (6)
```

The root used by a witness may depend on the coloring.  This causes no
quantifier swap: acceptance is exactly `union_r E_r`, and the ordinary union
bound, with no independence assumption, gives

```text
A_n <= sum_r Pr[E_r] = q (m/q) p_(n-2) = m p_(n-2).
```

Thus normalization, fixed-root conditioning, and adaptive witness choice do
not create a gap.

## 6. FLSY parameter and strict-inequality audit

FLSY Definition 2.1 in the full version (Definition 11 in the proceedings)
defines `I_(N,1)` as unions of at most one ordinary interval of `[N]`.  This
is precisely the family in (5), including the empty set.  Their Definition
1.4 (Definition 5 in the proceedings) says that a family is
`(epsilon,k)`-balanced-chain exactly when

```text
Pr_balanced[chain-balance <= k] >= epsilon.
```

Full-version Theorem 4.4 (Theorem 1.7), published as Theorem 23 (Theorem 8),
states that for a universal constant and every sufficiently large even `N`,
`I_(N,1)` is not `(epsilon,k)`-balanced-chain whenever

```text
epsilon > 2^(-c N^(1/5))  and  k < N^(1/5).
```

Set `k=1`, which satisfies the strict second inequality for sufficiently
large `N`.  If the actual success probability `p_N` were strictly larger
than the displayed threshold, an `epsilon` strictly between them would
contradict the theorem.  Therefore `p_N` is at most the threshold.  The
strict `epsilon` in FLSY does not weaken this conclusion.  Here `N=n-2` is
even and tends to infinity.  Changing between base `2` and `exp` only changes
the universal constant.

Combining with (1) and absorbing the polynomial factor proves (3).  Since
`n^(1/5)` eventually dominates every constant multiple of `log n`, (3) is
eventually smaller than `n^{-C}` for every fixed `C`.

## 7. Consequences that do and do not follow

If a condition `C(word)` implies `RR_n` acceptance, its balanced-word
probability is at most `A_n`; hence no such condition can have
inverse-polynomial measure for all sufficiently large even `n`.  This
rigorously closes Phase 4C for this exact family.

The result is even enough to show that a deterministic list covering colors
only through **individual-copy acceptance** needs at least `1/A_n` copies:
each relabeling accepts exactly `A_n binom(n,n/2)` balanced colorings, so the
cardinality of the union of `t` individual acceptance sets is at most `t`
times that number.  Thus this restricted cover number is
`2^(Omega(n^(1/5)))`.

This counting statement must not be transferred to the full induced subset
DAG of the literal union.  That DAG can have hybrid paths using subsets from
different copies, and such a path need not be an individually accepted path
of any copy.  No conclusion about those hybrid paths was used or proved.

## 8. Independent finite checks

I independently built the literal cyclic-interval family and the ordinary
interval family, searched every inclusion-by-one edge, and compared (5) for
every normalized coloring and every possible root through `n=14`.  The
numbers of rooted instances tested were:

```text
n=2:      1
n=4:      9
n=6:     50
n=8:    245
n=10: 1,134
n=12: 5,082
n=14: 22,308
```

There were no mismatches, and full `RR_n` acceptance equalled the union of
the rooted events in every case.  I separately ran the committed checker

```powershell
python -B research_cycle_04/cycle04_probability_interval_reduction.py
```

which reconstructs witnesses in both directions and checks the exact
negated-discrepancy identity through `n=14`; it passed all 15,591 fixed-plus-
root instances in its parameterization.  These finite checks corroborate the
all-`n` bijection but are not the asymptotic proof.

I also ran

```powershell
python -B experiments/cycle04_rr_verify_counts.py
```

which passed the literal induced-DAG/recurrence comparison through `n=12`
and all stored acceptance certificates through `n=34`.

### Maximum-run counterexample

The stored `n=30` representative

```text
00001001110000100111011110111
```

has 15 pluses on the 29 finite points (with infinity minus), cyclic run
lengths

```text
4,1,2,3,4,1,2,3,1,4,1,3,
```

and maximum monochromatic run length four.  A separate literal induced-DAG
search over all 843 subsets of `RR_30` rejected it; the independently coded
interval recurrence also rejected it.  The representative occurs in
`certificates/cycle04_rr_acceptance/cycle04_rr_failures_n30.txt` (SHA-256
`2ba88e2417b3d9adbfb98bc30bdd70e3d589837641ea9f8f2437a62aaf973094`).

This is a certified finite counterexample to the unqualified statement
"maximum cyclic run length at most four implies acceptance."  It does not by
itself refute a condition asserted only beyond some threshold greater than
30, nor does it establish any asymptotic failure density.

## 9. Adversarial checklist

| Potential failure | Finding |
|---|---|
| Wrong or seed-only `RR_n` family | Not present; the proof uses the literal prefix union and all its induced-DAG paths. |
| Infinity as a possible root | Not present; rank-one `RR_n` subsets are exactly finite singletons. |
| Rank-two endpoint omitted | Not present; inclusion forces `{infinity,r}` and forces `f(r)=+1`. |
| Odd intermediary discarded | Not present; every rank maps through (4). |
| Complement has wrong orientation | Not present after cutting at `r`; cyclic intervals containing `r` and ordinary intervals in `V_r` are exact complements. |
| Only one direction proved | Not present; the complement/reversal construction is explicit in both directions. |
| Normalization changes the measure | Not present; each global-sign pair contributes exactly one infinity-negative representative. |
| Conditioned restriction nonuniform | Not present; the binomial ratio above gives the exact uniform law. |
| Adaptively selected root treated as fixed | Not present; fixed-root equality is followed by a union bound over all roots. |
| FLSY uses a different family | Not present; its `I_(N,1)` is the complete ordinary one-interval family. |
| FLSY parity or `k` threshold fails | Not present for sufficiently large even `N=n-2`; then `1<N^(1/5)`. |
| Strict `epsilon` gives only a weaker result | Not present; choose an intermediate `epsilon` if `p_N` exceeds the threshold. |
| Individual-copy cover confused with literal-union cover | This would be a gap, but the audited theorem expressly excludes the latter. |

## 10. Required wording correction

The proven asymptotic statement is one-sided:

```text
A_n <= 2^(-Omega(n^(1/5))).
```

It should not be abbreviated as `A_n = 2^(-Omega(n^(1/5)))`, because no
matching lower bound is proved.  The proof-candidate file
`research_cycle_04/rooted_interval_obstruction.md` already uses the correct
inequality.  Any integrated result should retain that form.

Subject to this notation and the scope boundary above, the S4-D obstruction
receives a **PASS** verdict.

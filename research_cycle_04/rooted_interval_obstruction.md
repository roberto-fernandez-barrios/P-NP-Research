# Cycle 4: rooted `RR_n` reduction to the ordinary interval family

**Base commit:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Date:** 2026-08-21
**Role:** Phase 4F obstruction theorem
**Status:** `LITERATURE AUDITED; INDEPENDENTLY RECONSTRUCTED; FINITE-CHECKED;
ADVERSARIAL PASS`; final integration audit passed
**Boundary:** this obstructs the simple acceptance-probability
symmetrization route for the corrected one-cycle family `RR_n`.  It is not a
lower bound on `N(n)` and does not rule out hybrid paths in unions of several
relabelled copies.

## 1. Statement

Let `n=2m`, let `q=n-1`, and let `A_n` be the fraction of balanced sign
colorings accepted by the full induced subset DAG of the corrected cyclic
interval family `RR_n`.

For an even integer `N`, let

```text
p_N = Pr[the ordinary one-interval family I_(N,1)
         contains a 1-balanced maximal chain]
```

under a uniformly random balanced coloring of its `N` linearly ordered
points.  Then

```text
A_n <= m p_(n-2).                                      (1)
```

Fabris--Limaye--Srinivasan--Yehudayoff (FLSY), full
version Theorem 4.4 (Theorem 1.7), prove that there is a universal `c>0`
such that, for all sufficiently large even `N`,

```text
p_N <= 2^(-c N^(1/5)).                                 (2)
```

Consequently, for all sufficiently large even `n`,

```text
A_n <= (n/2) 2^(-c (n-2)^(1/5))
    = exp(-Omega(n^(1/5))).                            (3)
```

Thus the premise `A_n >= n^(-O(1))` is false for this exact `RR_n` family.
The FLSY random-relabeling lemma applied only to individual-copy acceptance
would need stretched-exponentially many copies, rather than polynomially
many.  This is the requested S4-D type of construction-family obstruction.
Two independent reconstructions, a separate adversarial audit, and the final
repository-level integration audit all passed.

## 2. Literal `RR_n` model used

Identify the ground set with

```text
U = Z_q union {infinity}.
```

The literal members of `RR_n` are:

* the empty and full sets;
* every finite singleton at rank one; and
* at rank `k`, for `2<=k<=n-1`, every set
  `{infinity} union I`, where `I` is a finite cyclic interval of length
  `k-1` in `Z_q`.

This is the independently reconstructed literal description in
`cycle04_rr_exact_count.md`.  In particular, the argument below concerns all
hybrid chains in the induced inclusion DAG, not only the round-robin seed
orders.

Normalize a balanced coloring `f:U->{-1,+1}` by global sign reversal so that

```text
f(infinity)=-1.
```

The finite cycle then has total sign

```text
f(Z_q)=+1.                                             (4)
```

This normalization chooses exactly one coloring from each global-sign pair
and does not change acceptance.

## 3. Exact rooted equivalence

Fix `r in Z_q`.  Say that `f` is **RR-accepted with root `r`** when an
accepted maximal chain has rank-one member `{r}`.

Let

```text
V_r = Z_q \ {r},
```

linearly ordered by cutting the finite cycle at `r`, for example

```text
r+1, r+2, ..., r-1                                  (mod q).
```

### Lemma

For a normalized balanced coloring `f`, the following are equivalent.

1. `f` is RR-accepted with root `r`.
2. `f(r)=+1`, and the ordinary interval family on the linearly ordered set
   `V_r` contains a 1-balanced maximal chain for `f|V_r`.

### Forward direction

Let

```text
empty=C_0 subset C_1 subset ... subset C_n=U
```

be an accepted chain with `C_1={r}`.  Its rank-two member must be
`{infinity,r}`.  Every compatible even-rank set has discrepancy zero, so

```text
f(r)+f(infinity)=0,
```

and the normalization gives `f(r)=+1`.

For `1<=j<=q`, the literal form and inclusion force unique nested cyclic
intervals

```text
I_1={r} subset I_2 subset ... subset I_q=Z_q,
|I_j|=j,
C_(j+1)={infinity} union I_j.                         (5)
```

For `0<=s<=q-1`, define

```text
J_s = Z_q \ I_(q-s).                                  (6)
```

The complement of a cyclic interval containing the cut point `r` is an
ordinary interval of `V_r`; the empty set is allowed.  Equations (5)--(6)
therefore give a maximal ordinary-interval chain

```text
empty=J_0 subset J_1 subset ... subset J_(q-1)=V_r.
```

Using (4) and (5),

```text
f(J_s)
  = f(Z_q)-f(I_(q-s))
  = 1-f(I_(q-s))
  = -f(C_(q-s+1)).                                    (7)
```

Every `J_s` consequently has discrepancy at most one.  Finally,
`f(V_r)=f(Z_q)-f(r)=0`, so the restricted coloring is balanced on the even
set `V_r` of size `q-1=n-2`.

### Reverse direction

Assume `f(r)=+1` and let

```text
empty=J_0 subset J_1 subset ... subset J_(q-1)=V_r
```

be a 1-balanced maximal chain of ordinary intervals.  Put

```text
I_j = Z_q \ J_(q-j),          1<=j<=q.
```

The complement of an ordinary interval in the cut order is a cyclic
interval containing `r`.  Hence the `I_j` are nested cyclic intervals of
the required sizes.  Define `C_0=empty`, `C_1={r}`, and

```text
C_(j+1)={infinity} union I_j.
```

These are literal members of `RR_n` at every rank.  Equation (7) applies in
reverse, so ranks two through `n` have discrepancy at most one; rank one has
absolute discrepancy one.  Thus this is an accepted RR chain rooted at
`r`.

This proves the lemma.  It also proves the deque version directly: after
the surviving plus root is removed, opposite-sign boundary-pair deletion is
exactly reversal/complementation of an ordinary interval-growth chain.

## 4. Probability and conditioning

Sample a normalized coloring uniformly.  Equivalently, choose `m` plus
positions uniformly among the `q=2m-1` finite points and set infinity minus.
For a fixed root `r`,

```text
Pr[f(r)=+1] = m/q.                                    (8)
```

Conditional on `f(r)=+1`, the restriction to `V_r` has exactly `m-1` plus
and `m-1` minus signs and is uniform among all balanced colorings of this
fixed linearly ordered set.  The rooted-equivalence lemma and (8) give

```text
Pr[f is RR-accepted with root r] = (m/q) p_(n-2).     (9)
```

Every RR witness has some finite rank-one root.  A union bound over all
`q` choices gives

```text
A_n <= q (m/q) p_(n-2) = m p_(n-2),
```

which is (1).  No independence among root events is asserted or needed.

## 5. Imported FLSY theorem and parameter check

FLSY Definition 2.1 defines

```text
I_(N,1) = {ordinary intervals of [N]} union {empty}.
```

Their full-version Theorem 4.4 (Theorem 1.7) states that a universal
constant `c>0` exists such that, for every sufficiently large even `N`, this
family is not an `(epsilon,k)`-balanced-chain system when

```text
epsilon > 2^(-c N^(1/5))  and  k < N^(1/5).
```

By the definition of an `(epsilon,k)`-balanced-chain system, putting `k=1`
shows that its actual success probability `p_N` satisfies (2) once `N` is
sufficiently large.  The parity and threshold conditions apply here because
`N=n-2` is even and tends to infinity.

The primary sources are:

* Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir
  Yehudayoff, *Multilinear Algebraic Branching Programs and the
  Min-Partition Rank Method*, ECCC TR26-001, 2026,
  <https://eccc.weizmann.ac.il/report/2026/001/>; Definition 2.1 and
  Theorem 4.4 (Theorem 1.7).
* The published version is in *41st Computational Complexity Conference
  (CCC 2026)*, LIPIcs 383, Article 22,
  <https://doi.org/10.4230/LIPIcs.CCC.2026.22>.

The stretched-exponential interval estimate is a known theorem.  The rooted
complement equivalence above is an elementary derived connection; novelty is
not asserted and is being checked separately.

## 6. Consequence for the relabeling route

Let `M_n=binom(n,n/2)`.  The exact Phase-4A all-color union-bound threshold
for `0<A_n<1` is

```text
floor(ln(M_n)/(-ln(1-A_n)))+1.
```

For sufficiently large `n`, (3) gives `A_n<=1/2` and hence

```text
-ln(1-A_n) <= 2A_n.
```

The number of copies certified by that union-bound method is therefore at
least

```text
ln(M_n)/(2A_n) = exp(Omega(n^(1/5))).
```

Equivalently, the direct FLSY symmetrization lemma incurs size proportional
to `1/A_n`, which is stretched exponential here.  Polynomially many random
copies cannot be justified by this individual-copy acceptance estimate.

This conclusion has strict scope:

* it does not show that every polynomial list of relabelings fails;
* it does not bound the acceptance created by hybrid paths between copies;
* it does not refute an explicit algebraic multi-`RR` construction; and
* it says nothing negative about arbitrary 1-balanced-chain families or
  `N(n)`.

## 7. Audit obligations before promotion

The following validation obligations were imposed before promotion:

1. **PASS:** independent reconstruction of the rooted equivalence, including
   ranks zero, one, two, odd intermediaries, and full;
2. **PASS:** direct finite comparison of rooted RR acceptance with ordinary
   interval acceptance through `n=14`;
3. **PASS:** primary-source verification of the FLSY quantifiers and
   exponent in both the full and proceedings versions;
4. **PASS:** independent binomial-fiber audit of uniform normalized
   conditioning; and
5. **PASS:** an adversarial scope audit separating individual-copy
   symmetrization from hybrid multi-copy unions.

Evidence is in `rr_probability_attack.md`, `literature_novelty_audit.md`,
`../audits/cycle04_rr_obstruction_adversarial.md`, and
`cycle04_probability_interval_reduction.py`.

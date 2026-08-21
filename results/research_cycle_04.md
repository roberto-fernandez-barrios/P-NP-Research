# Research Cycle 4: randomized relabeling / RR-cover attack

**Base commit:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Date:** 2026-08-21
**Stopping condition:** **S4-D**
**Primary target:** O01 remains **OPEN**

## 1. Outcome

Cycle 4 rigorously obstructs the proposed route

```text
inverse-polynomial one-copy RR acceptance
    -> polynomially many random relabelings
    -> O01.
```

The implication itself is valid and is an immediate specialization of the
published FLSY worst-case-to-average-case lemma.  Its premise is false for
the corrected one-cycle family `RR_n`.

Let `A_n` be the fraction of balanced colorings accepted by the full induced
subset DAG of `RR_n`.  There is an absolute `c>0` such that, for all
sufficiently large even `n`,

```text
A_n <= (n/2) 2^(-c (n-2)^(1/5))
    = exp(-Omega(n^(1/5))).                    (1)
```

The proof first fixes the finite rank-one root of an RR witness, then
complements and reverses its nested cyclic intervals.  This gives an exact
bijection with a balanced maximal chain in FLSY's ordinary one-interval
family on `n-2` points.  FLSY's known stretched-exponential interval theorem
then yields (1).

Equation (1) rules out every inverse-polynomial-measure accepted subclass of
this `RR_n`, the Phase-4A random-cover argument with polynomially many
individual copies, and even an arbitrary deterministic cover by polynomially
many witnesses each contained in one copy.  It does not control hybrid paths
created only after taking the literal subset union of several relabelings.
It is a restricted construction-family obstruction, not a lower bound on
`N(n)`.

## 2. Phase 4A: exact symmetrization

For any fixed literal family `F`, balanced coloring `f`, and uniform
permutation `pi`, relabeling transports the full induced subset DAG and gives

```text
pi(F) accepts f  iff  F accepts f o pi.
```

Every balanced target coloring has exactly `(n/2)!^2` permutation fibers, so
`f o pi` is uniform among the `M=binom(n,n/2)` balanced colorings.  If `A` is
the acceptance fraction of `F`, then

```text
Pr[pi(F) accepts f] = A.
```

For independent `pi_1,...,pi_t`, the fixed-color rejection events are
independent and

```text
Pr[all t copies reject f] = (1-A)^t.
```

The all-color union bound is strictly successful when

```text
M(1-A)^t < 1.
```

For `0<A<1`, its exact least certified positive integer is

```text
floor(ln M / -ln(1-A)) + 1.                  (2)
```

The strict floor-plus-one matters when the quotient is integral.  Global
sign invariance permits the sharper replacement of `M` by `M/2`.  The
endpoint cases are `t=1` for `A=1` and no finite `t` from this argument for
`A=0`.

For `F=RR_n`, a successful realization produces one fixed literal family

```text
Y = union_j pi_j(RR_n).
```

Its exact rankwise cardinality is

```text
|Y| = 2 + sum_(k=1)^(n-1)
            |union_j pi_j(RR_n intersect rank k)|,
```

and therefore, counting **distinct literal subsets**,

```text
|Y| <= 2 + sum_(k=1)^(n-1) min{binom(n,k),t(n-1)}
     <= 2+t(n-1)^2.                           (3)
```

Thus the hypothetical bound `A_n>=n^(-c)` would imply
`N(n)=O(n^(c+3))` for large even `n`; finitely many smaller even cases can be
absorbed into one absolute exponent.  The argument is nonuniform but that is
sufficient for the existential definition of `N(n)`.  Relabeling every rank
eliminates orientation and odd-intermediary issues, and hybrid paths can only
help.

This is not a new symmetrization theorem.  It specializes FLSY's
worst-case-to-average-case Lemma 2.3 (Lemma 1.5) in the ECCC full version,
published as Lemma 14 (Lemma 6) at CCC 2026.  Formulae (2)--(3) are elementary
rounding and literal-count refinements.

## 3. Exact rooted reduction and S4-D obstruction

Write `n=2m`, `q=n-1`, and identify the ground set as
`Z_q union {infinity}`.  Normalize by global sign reversal so that infinity
has sign `-1`; the finite cycle then has total sign `+1`.

Fix a finite root `r`.  Every RR chain rooted at `{r}` is forced to have

```text
empty, {r}, {infinity} union I_1, ...,
{infinity} union I_q,
```

where `I_1={r}`, `I_q=Z_q`, and the `I_j` are nested cyclic intervals of
size `j`.  The rank-two discrepancy forces `f(r)=+1`.

Cut the cycle at `r`, linearly order

```text
V_r = Z_q \ {r} = (r+1,r+2,...,r-1),
```

and put

```text
J_s = Z_q \ I_(q-s),       0<=s<=q-1.
```

The `J_s` form a maximal chain of ordinary intervals on `V_r`.  Conversely,
complementing and reversing any such interval chain reconstructs a literal
RR chain rooted at `r`.  The discrepancy identity is exact:

```text
f(J_s) = 1-f(I_(q-s))
       = -f({infinity} union I_(q-s)).         (4)
```

This proves both directions, including empty, singleton, rank-two, odd, and
full ranks.

Let `p_N` be the success probability of the ordinary one-interval family
`I_(N,1)` on a uniform balanced coloring.  For a fixed root,

```text
Pr[root-r RR witness]
  = (m/q) p_(n-2),
```

because `Pr[f(r)=+1]=m/q` and the conditional restriction to `V_r` is uniform
balanced.  Union-bounding over the `q` roots gives

```text
A_n <= m p_(n-2) = (n/2)p_(n-2).              (5)
```

FLSY Definition 2.1 defines the ordinary interval family.  Their full
Theorem 4.4 (Theorem 1.7), published as Theorem 23 (Theorem 8), supplies a
universal `c>0` such that, for every sufficiently large even `N`,

```text
p_N <= 2^(-c N^(1/5)).                         (6)
```

Equations (5)--(6) prove (1).  The polynomial prefactor is absorbed only
after increasing the sufficiently-large threshold.  No independence among
root events is assumed.

Since each relabelled copy individually accepts exactly an `A_n` fraction,
any cover by within-copy witnesses needs at least `1/A_n`, which is
`2^(Omega(n^(1/5)))`.  The exact Phase-4A union-bound prescription is likewise
stretched exponential.  Neither statement rules out hybrid multi-copy
chains.

The rooted equivalence was independently reconstructed twice and exhaustively
checked in both directions for every balanced restriction and every root
through `n=14` (15,591 rooted instances).  The FLSY theorem statement,
numbering, and threshold quantifiers were checked against the primary full
and proceedings versions.  The connection is not claimed as novel; the
recorded search result is only `PRIOR-ART-NOT-FOUND` for the exact RR/deque
wording and finite sequence.

## 4. Phase 4B: exact acceptance data

An independent reconstruction gives the literal family

```text
rank 0,n: one endpoint set;
rank 1: every finite singleton;
rank k, 2<=k<=n-1:
        infinity joined to every finite cyclic interval of length k-1.
```

Hence `|RR_n|=(n-1)^2+2`.  The full induced-DAG acceptance predicate is the
exact cyclic-interval/deque recurrence, not merely coverage by the generating
round-robin orders.

The computation uses fixed-weight necklace enumeration.  With
`q=n-1` and normalized weight `m=n/2`, `gcd(q,m)=1`, so every rotation orbit
has full size `q`.  A packed reachability recurrence evaluates all starts
simultaneously.  A separately written Python implementation fully recounts
through `n=30`; all stored representatives and aggregate statistics are
independently checked through `n=34`.

| `n` | normalized words | accepted | rejected | rejection fraction | rejected rotation orbits |
|---:|---:|---:|---:|---:|---:|
| 22 | 352,716 | 352,695 | 21 | 0.0000595379852346 | 1 |
| 24 | 1,352,078 | 1,351,664 | 414 | 0.000306195352635 | 18 |
| 26 | 5,200,300 | 5,195,600 | 4,700 | 0.000903794011884 | 188 |
| 28 | 20,058,300 | 20,017,908 | 40,392 | 0.00201372997712 | 1,496 |
| 30 | 77,558,760 | 77,266,353 | 292,407 | 0.00377013505631 | 10,083 |
| 32 | 300,540,195 | 298,654,992 | 1,885,203 | 0.00627271503567 | 60,813 |
| 34 | 1,166,803,110 | 1,155,611,853 | 11,191,257 | 0.00959138427391 | 339,129 |

The corresponding rejected dihedral-orbit counts are
`1,10,100,760,5088,30500,169862`.  Exact cyclic-run and maximum-run
histograms are stored in the certificates.  Already at `n=30` there are
failures of maximum cyclic monochromatic run length four, refuting the simple
finite condition “maximum run at most four implies acceptance.”

These data are exact finite evidence only.  No asymptotic conclusion is
drawn from the visible trend.

## 5. Phase 4E: finite multi-RR certificates

Define `t_RR(n)` as the minimum number of relabelled copies whose **literal
subset union**, under its full induced DAG, accepts every balanced coloring.
Exact certificates prove

```text
t_RR(22)=t_RR(24)=t_RR(26)=t_RR(28)=t_RR(30)=2.       (7)
```

One copy fails in each case.  For the upper bound, the first copy is the
identity and the second fixes infinity and multiplies finite labels modulo
`q=n-1` by `a=2,2,2,4,5`, respectively.  The individual rejection sets are
disjoint, so these particular successes need no hybrid-only witness.  The
independent verifier nonetheless reconstructs and deduplicates all literal
subsets and all induced inclusion edges.

| `n` | multiplier `a` | one-copy rejects | two-copy literal subsets | full-union rejects |
|---:|---:|---:|---:|---:|
| 22 | 2 | 21 | 821 | 0 |
| 24 | 2 | 414 | 991 | 0 |
| 26 | 2 | 4,700 | 1,177 | 0 |
| 28 | 4 | 40,392 | 1,379 | 0 |
| 30 | 5 | 292,407 | 1,597 | 0 |

For these stored permutations the exact literal rank profile gives

```text
2+(n-1)(2n-5)
```

distinct subsets.  This counts neither permutations nor paths.  A second
direct check traversed the full `n=22` union DAG on all 352,716 normalized
colorings and found no rejection.

Equation (7) is not extrapolated to larger `n`.  In particular, it neither
contradicts the single-copy asymptotic obstruction nor proves an explicit
all-`n` family.

## 6. Formalization and validation status

The existing Lean development was extended to protect the deterministic
Cycle-4 symmetrization core.  `acceptsColoring_relabel_iff` proves exact
full-family acceptance equivariance; `isOneBalancedChain_relabel_iff` proves
worst-case invariance; and
`iUnion_isOneBalancedChain_of_pointwise_accepts` plus
`union_relabelings_isOneBalancedChain` prove the literal-union step.  The
pinned Lean 4.32.1/mathlib 4.32.1 build passes all 8,656 jobs at trust level
zero with no `sorryAx`; source scans find no standalone `sorry`, `axiom`,
`admit`, `unsafe`, or `opaque`.

Phase 4A is only `PARTIALLY FORMALIZED`: random-permutation fiber counting,
independence, the union bound, exact `t`, and distinct-subset cardinality are
not in Lean.  The literal RR/deque/rooted equivalence, imported FLSY theorem,
exact finite enumerations, and O01 are also unformalized.  The exact boundary
is recorded in `research_cycle_04/lean_formalization.md` and
`formal/coverage.md`.

Independent validation comprised:

* a separate Phase-4A proof and exact fiber/rank accounting;
* two independent all-`n` reconstructions of the rooted interval bijection;
* exhaustive two-way witness checking through `n=14`;
* primary-source verification of every imported FLSY quantifier and theorem
  number;
* a dedicated barrier audit, whose relativization/natural-proofs/
  algebrization findings are correctly `NOT APPLICABLE` at this restricted
  combinatorial scope rather than claimed barrier bypasses;
* independent exact recounting through `n=30` and certificate validation
  through `n=34`;
* an independent full multi-RR certificate checker through `n=30`; and
* a final repository-level mathematical, computational, formal, and scope
  audit.

The exact reproduction commands and final audit output are preserved in the
Cycle-4 reports and certificate indexes.

## 7. Epistemic ledger and stopping boundary

| Claim | Status |
|---|---|
| FLSY worst-case-to-average-case symmetrization | **KNOWN, PUBLISHED** |
| Exact Phase-4A threshold and literal-union count | **INDEPENDENTLY RECONSTRUCTED**; formal coverage recorded separately |
| Rooted RR / ordinary-interval equivalence | **INDEPENDENTLY RECONSTRUCTED; FINITE-CHECKED**; formal coverage recorded separately |
| FLSY ordinary one-interval probability upper bound | **KNOWN, PUBLISHED** |
| `A_n <= (n/2)2^(-c(n-2)^(1/5))` | **RIGOROUS COROLLARY; INDEPENDENTLY ADVERSARIALLY REVIEWED** |
| Exact `A_n` data through `n=34` | **EXHAUSTIVE FINITE COMPUTATION; INDEPENDENTLY CHECKED** |
| `t_RR(n)=2` for `n=22,24,26,28,30` | **EXHAUSTIVE FINITE COMPUTATION; INDEPENDENTLY CHECKED** |
| Any fixed `t` or polynomial multi-RR theorem for all `n` | **OPEN** |
| O01 | **OPEN** |

Cycle 4 stops under S4-D.  It does not begin Research Cycle 5.  No mABP,
Boolean, algebraic, or P-versus-NP consequence is claimed.

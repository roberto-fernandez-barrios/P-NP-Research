# Cycle 4 RR probability attack: rooted interval obstruction

**Cycle:** Research Cycle 4
**Role:** independent Phases 4C, 4D, and 4F attack
**Pinned repository state read first:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Date:** 2026-08-21
**Main disposition:** **S4-D is reached for the single-copy-acceptance / random-cover route.**
**Epistemic status:** the reduction below is `ADVERSARIALLY RECONSTRUCTED;
FINITE-CHECKED; UNFORMALIZED`; its asymptotic input is the published FLSY
Theorem 4.4 (Theorem 1.7), not a new probability theorem. Novelty is not
claimed.

This report does not edit or rely on the Cycle-4 state/result/failure logs.
It does not claim O01, a lower bound on `N(n)`, or any algebraic or Boolean
complexity consequence.

## 1. Outcome first

Let `n=2m`, put `q=n-1`, and let `RR_n` be the corrected Cycle-3 literal
family. Let `A_n` be its acceptance fraction among balanced signed
colorings. There is an absolute constant `c>0` such that, for all sufficiently
large even `n`,

```text
A_n <= (n/2) 2^{-c (n-2)^{1/5}} = 2^{-Omega(n^{1/5})}.
```

The reason is an exact reduction, including a converse:

> Once infinity is fixed negative and the first positive finite point `r` of
> an RR witness is fixed, complementing and reversing the nested cyclic
> intervals gives exactly a 1-balanced maximal chain in the ordinary
> one-interval family on the other `n-2` finite points.

Fabris--Limaye--Srinivasan--Yehudayoff prove that the probability that the
ordinary one-interval family accepts a uniform balanced coloring on `N`
points is at most `2^{-cN^{1/5}}` for all sufficiently large even `N`.

Consequences within the exact scope are:

1. Phase 4C cannot succeed for this `RR_n`: no accepted subclass can have
   inverse-polynomial balanced measure, because the whole accepted class has
   stretched-exponentially small measure.
2. Polynomially many independent relabelings cannot work through the Phase
   4A event "one copy individually accepts the color." Indeed, even for one
   fixed color the probability that any of `t` independent copies accepts it
   is at most `t A_n`.
3. More strongly, any deterministic list whose **individual acceptance
   sets** cover all balanced colors needs at least `1/A_n`, and hence at
   least `2^{Omega(n^{1/5})}` copies, by counting.
4. This says nothing against hybrid chains appearing only after taking the
   literal subset union of several relabeled RR families. Such a hybrid
   multi-RR construction is a different Phase 4E route.

The finite fact that `A_n` is close to one through the currently accessible
range is compatible with this theorem: the FLSY threshold and constant are
asymptotic and not numerically effective here. No finite trend is used in the
proof.

## 2. Dependencies independently rechecked

The following repository material was read as claims rather than authority:

* `AGENTS.md`, `INITIAL_RESEARCH_MISSION.md`, and `RESEARCH_STATE.md`;
* `research_cycle_03/cp_m_matching_equivalence.md`;
* `experiments/cycle03_check_cp_m_matching.py`;
* `audits/check_cycle03_cp_m_adversarial.py`;
* the RR/deque portions of `audits/cycle03_final_integration_adversarial.md`
  and `results/research_cycle_03.md`; and
* the relevant entries of `failure_knowledge.jsonl`.

The primary external source was checked directly:

* Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir
  Yehudayoff, *Multilinear Algebraic Branching Programs and the
  Min-Partition Rank Method*, ECCC TR26-001 (2026), especially Definitions
  1.2, 1.4, and 2.1 and Theorem 4.4 (Theorem 1.7),
  <https://eccc.weizmann.ac.il/report/2026/001/>. The conference version is
  CCC 2026, LIPIcs 383, Article 22,
  <https://doi.org/10.4230/LIPIcs.CCC.2026.22>.

The asymptotic probability estimate below is exactly an application of that
known theorem. The rooted complement equivalence was not assumed from FLSY
or Cycle 3; it was reconstructed in both directions and checked against the
literal induced subset DAG.

## 3. Exact objects and normalization

Write the ground set as

```text
U = F union {infinity},       F = Z_q,       q=2m-1.
```

The literal corrected RR family consists of:

* `emptyset` and `U`;
* every finite singleton `{r}`; and
* at rank `k`, for `2<=k<=n-1`, every set
  `{infinity} union I`, where `I` is a cyclic interval in `F` of length
  `k-1`.

This is the exact Cycle-3 family of `(n-1)^2+2` distinct subsets. A chain is
searched in the full inclusion-by-one DAG induced by these subsets; it is
not restricted to the generating round-robin seed paths.

Acceptance is invariant under globally replacing `f` by `-f`. Every balanced
coloring pair `{f,-f}` has exactly one member with
`f(infinity)=-1`. Therefore `A_n` is exactly the acceptance probability under
the normalized uniform distribution

```text
f(infinity)=-1,
f|F has m pluses and m-1 minuses.
```

There is no factor of two left over from this normalization:

```text
(1/2) binom(2m,m) = binom(2m-1,m).
```

## 4. Rooted RR is exactly the ordinary interval family

Fix a normalized coloring `f` and a finite point `r`.

### Lemma RC4-RI (exact rooted equivalence)

The following are equivalent.

1. `RR_n` has a 1-balanced maximal chain for `f` whose rank-one state is
   `{r}`.
2. `f(r)=+1`, and, after ordering
   `V=F\{r}` as

   ```text
   r+1, r+2, ..., r-1                 (cyclic arithmetic),
   ```

   the ordinary one-interval family on `V` has a 1-balanced maximal chain
   for `g=f|V`.

Here `|V|=n-2` is even and `g` is balanced.

### Forward direction

Let

```text
C_0, C_1, ..., C_n
```

be a rooted RR witness. The literal rank profiles force

```text
C_0 = emptyset,
C_1 = {r},
C_{j+1} = {infinity} union I_j       for 1<=j<=q,
```

where

```text
I_1={r} subset I_2 subset ... subset I_q=F
```

and every `I_j` is a cyclic interval of size `j`. In particular, rank two
is `{r,infinity}`. Since `f(infinity)=-1` and this even-rank state must have
discrepancy zero, `f(r)=+1`.

It follows that

```text
f(F)=1,
f(V)=f(F)-f(r)=0.
```

For `0<=t<=q-1`, define

```text
K_t = F \ I_{q-t}.
```

Because every `I_j` is a cyclic interval containing the cut point `r`, its
complement is an ordinary interval in the displayed linear order on `V`.
The complements reverse inclusions and sizes, so

```text
K_0=emptyset subset K_1 subset ... subset K_{q-1}=V
```

is a maximal chain of ordinary intervals.

Discrepancies agree up to an exact minus sign. For every `t`,

```text
g(K_t)
  = f(F \ I_{q-t})
  = 1 - f(I_{q-t})
  = - f({infinity} union I_{q-t})
  = - f(C_{q-t+1}).
```

Thus every `K_t` has absolute discrepancy at most one.

### Converse direction

Assume `f(r)=+1` and let

```text
K_0=emptyset subset K_1 subset ... subset K_{q-1}=V
```

be a 1-balanced maximal chain of ordinary intervals. Define, for
`1<=j<=q`,

```text
I_j = F \ K_{q-j}.
```

The complement in the cycle of an ordinary interval avoiding the cut point
`r` is a cyclic interval containing `r`. Reversing a maximal interval chain
makes these intervals grow by one endpoint at every step. Hence the sets

```text
C_0=emptyset,
C_1={r},
C_{j+1}={infinity} union I_j          (1<=j<=q)
```

form a maximal chain entirely inside the literal `RR_n` family.

Since `f(F)=1`, the same calculation gives

```text
f(C_{j+1}) = -g(K_{q-j}).
```

The two exceptional initial ranks have discrepancies zero and one. Therefore
the constructed chain is 1-balanced. This proves the converse.

### Endpoint and model audit

The proof explicitly covers all potential boundary mismatches:

* `K_0=emptyset` corresponds to the full RR state;
* `K_{q-1}=V` corresponds to `I_1={r}` and the rank-two RR state;
* the separate rank-one RR state is `{r}`;
* infinity is never a rank-one RR state;
* every odd as well as every even intermediary is present, so this proof
  uses no contracted-pair orientation assumption; and
* an arbitrary ordinary interval chain maps into literal cyclic-interval
  subsets already in RR, proving the converse rather than only a necessary
  condition.

## 5. Probability calculation

Let `N=n-2` and define

```text
p_N = Pr_g[the ordinary one-interval family I_{N,1}
           has a 1-balanced maximal chain for g],
```

where `g` is uniform over balanced colorings of `[N]`.

Under the normalized RR distribution, let `E_r` be the event that a witness
starts at finite root `r`. For a fixed `r`,

```text
Pr[f(r)=+1] = m/q.
```

Conditioned on this event, `f|V` is exactly uniform among balanced colorings
of the `N=2m-2` remaining points. Lemma RC4-RI therefore gives the equality

```text
Pr[E_r] = (m/q) p_{n-2}.
```

Every RR witness has some rank-one root, so acceptance is `union_r E_r`.
No independence between roots is assumed or needed. A union bound gives

```text
A_n = Pr[union_{r in F} E_r]
    <= sum_{r in F} Pr[E_r]
     = q (m/q) p_{n-2}
     = (n/2) p_{n-2}.                         (1)
```

This calculation also checks the fixed-family and uniformity issues: `r` is
not chosen adaptively in the probability distribution, and conditioning on
one fixed `r` produces the uniform balanced law required by FLSY.

## 6. Applying the published FLSY theorem

FLSY Definition 1.4 calls a family `(epsilon,k)`-balanced-chain when a
uniform balanced coloring has chain-balance at most `k` with probability at
least `epsilon`. Their Theorem 4.4 (Theorem 1.7) states that there is a
universal `c>0` such that, for all sufficiently large even `N`, the ordinary
one-interval family `I_{N,1}` is not `(epsilon,k)`-balanced-chain whenever

```text
epsilon > 2^{-c N^{1/5}}     and     k < N^{1/5}.
```

Take `k=1`. If `p_N` were strictly larger than the displayed threshold,
choosing `epsilon` between the threshold and `p_N` would make the interval
family `(epsilon,1)`-balanced-chain, contradicting the theorem. Thus

```text
p_N <= 2^{-cN^{1/5}}.
```

Substituting this into (1) proves

```text
A_n <= (n/2) 2^{-c(n-2)^{1/5}}
    = 2^{-Omega(n^{1/5})}.
```

The polynomial prefactor is absorbed into the exponent only after increasing
the sufficiently-large threshold. The theorem supplies an absolute constant;
there is no hidden `n`-dependent choice.

## 7. Implications for relabeling and the exact boundary

Every relabeling of RR accepts the same number `A_n M_n` of balanced
colorings, where `M_n=binom(n,n/2)`. Consequently, if a list of `t`
relabelings is required to cover colors by **individual-copy acceptance**, its
covered set has cardinality at most

```text
t A_n M_n.
```

Such a cover needs

```text
t >= 1/A_n >= 2^{Omega(n^{1/5})}.
```

For independent random relabelings and one fixed color,

```text
Pr[some copy individually accepts] = 1-(1-A_n)^t <= tA_n.
```

Thus every polynomial `t` has success probability `o(1)` even before trying
to cover all colors. This rigorously kills the proposed inverse-polynomial
acceptance premise and its simple random-cover consequence.

It does **not** prove that the literal subset union of polynomially many
relabelings fails. The induced DAG of that union can splice states from
different copies into hybrid chains. Counting only the union of the
individual acceptance sets would ignore exactly the Cycle-3 hybrid-path
warning. Phase 4E remains logically separate.

## 8. Probabilistic-process discipline and falsification record

The exact reduction also explains why a local branching heuristic is not a
safe source of a lower bound. For a fixed root, the reverse RR deletion
process is the ordinary interval-chain process on a uniform random bridge of
length `n-2`. FLSY's stretched-exponential upper bound applies to the
existence of **any** complete adaptive endpoint-deletion sequence, not merely
to one greedy rule.

For an attempted direct stochastic proof, the actual filtration after `t`
deletions must contain the identities and signs of all exposed/deleted
boundary points and the remaining plus/minus inventory. Under the uniform
balanced law the next signs are sampling-without-replacement variables; they
are not fresh independent fair bits. Conditioning retrospectively on a
successful deletion history is an even stronger change of law. No
independence, martingale, or branching domination is asserted in this report.

The independent finite scanner
`cycle04_probability_scan.cpp` was used only for falsification and checker
stress. It reproduces the Cycle-3 first failure and additionally finds:

```text
n=22: rejected 21 / 352716
n=24: rejected 414 / 1352078
n=26: rejected 4700 / 5200300
n=28: rejected 40392 / 20058300
n=30: rejected 292407 / 77558760
```

These are finite exact enumerations by a bit-parallel implementation of the
same interval recurrence, not asymptotic evidence. At `n=30` there are failed
words with maximum cyclic run length four, falsifying the tempting finite
guess that bounded runs force acceptance. The words

```text
1^8 0^5 1^3 (01)^k 0^5
```

were also checked and rejected for every `0<=k<=100`; this is a finite
counterexample search only, not an all-`k` theorem. It shows that increasing
the number of runs and keeping the maximum run length bounded do not supply a
credible unqualified sufficient condition. The FLSY corollary is the
rigorous asymptotic obstruction; none of these computations is used in it.

## 9. Independent checker and reproduction

Run the exact bijection checker:

```powershell
python -B research_cycle_04/cycle04_probability_interval_reduction.py
```

It independently builds the literal RR family and the ordinary interval
family, searches their full induced subset DAGs, constructs witnesses in both
directions, and checks the exact negated-discrepancy identity. The recorded
output is:

```text
n=2:  ordinary interval accepted 1/1;       root instances 1
n=4:  ordinary interval accepted 2/2;       root instances 6
n=6:  ordinary interval accepted 6/6;       root instances 30
n=8:  ordinary interval accepted 20/20;     root instances 140
n=10: ordinary interval accepted 68/70;     root instances 630
n=12: ordinary interval accepted 236/252;   root instances 2772
n=14: ordinary interval accepted 834/924;   root instances 12012
PASS exact rooted RR <-> ordinary one-interval chain bijection
```

Compile the optional finite scanner outside the repository tree:

```powershell
$scanExe = Join-Path $env:TEMP 'cycle04_probability_scan.exe'
g++ -O3 -std=c++20 research_cycle_04/cycle04_probability_scan.cpp -o $scanExe
& $scanExe 21 5
Remove-Item -LiteralPath $scanExe
```

The Python checker uses only the standard library. The C++ scanner is not a
certificate of the asymptotic theorem and is not required for the proof.

## 10. Final epistemic ledger

| Claim | Status |
|---|---|
| Literal definition and size `(n-1)^2+2` of corrected `RR_n` | Cycle-3 result independently re-read; finite checker reconstructs the literal family |
| Rooted RR acceptance iff ordinary one-interval acceptance on `n-2` points | `ADVERSARIALLY RECONSTRUCTED; FINITE-CHECKED; UNFORMALIZED` |
| `A_n <= (n/2)p_{n-2}` | `PROVED FROM THE ROOTED EQUIVALENCE; UNFORMALIZED` |
| `p_N <= 2^{-cN^{1/5}}` for large even `N` | `KNOWN`, FLSY Theorem 4.4 / 1.7 |
| `A_n <= 2^{-Omega(n^{1/5})}` upper bound | `KNOWN-THEOREM COROLLARY; INDEPENDENTLY AUDITED; UNFORMALIZED` |
| Inverse-polynomial accepted RR subclass | `REFUTED ASYMPTOTICALLY` by the upper bound |
| Polynomial individual-copy RR cover | `REFUTED`; needs `2^{Omega(n^{1/5})}` copies |
| Polynomial literal multi-RR union using hybrid paths | `OPEN`; not addressed by this obstruction |
| O01 | `OPEN` |

This reaches Cycle-4 stopping condition S4-D for the acceptance-probability
symmetrization route. It does not start or recommend a Cycle 5.

# Research Cycle 4: literature and novelty audit

**Audit date:** 2026-08-21
**Repository base:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Role:** independent literature/attribution audit
**Status:** `S4-D CONFIRMED FOR THE INDIVIDUAL-COPY RR SYMMETRIZATION ROUTE`

This audit does not establish a lower bound on `N(n)`, does not rule out
hybrid chains created by a union of several relabelled families, and makes no
novelty claim from a negative search.

## 1. Executive disposition

| Cycle-4 item | Disposition | Audit conclusion |
|---|---|---|
| Random-relabeling reduction | **KNOWN** | It is an immediate instance of the Fabris--Limaye--Srinivasan--Yehudayoff (FLSY) random-permutation covering lemma. The exact binomial threshold in Cycle 4 is a harmless sharpening of their `O(n/p)` choice, not a new qualitative theorem. |
| Rooted `RR_n` witness | **EXACT DERIVED EQUIVALENCE, independently checked** | Fixing the finite rank-one root turns `RR_n` acceptance, by complementing and reversing the nested intervals, into acceptance by the ordinary one-interval family `I_(n-2,1)`. |
| RR acceptance probability | **RIGOROUSLY OBSTRUCTED** | FLSY's interval theorem and the rooted equivalence imply `A_n <= (n/2) 2^(-c (n-2)^(1/5)) = exp(-Omega(n^(1/5)))` for all sufficiently large even `n`. Thus `A_n >= n^(-O(1))` is false for this `RR_n`. |
| Scope of S4-D | **STRICTLY LIMITED** | Polynomially many copies cannot cover all colorings by witnesses lying wholly inside individual copies. The theorem does not control new hybrid chains in the literal subset union of several copies. |
| Rooted count sequence in the prompt | **IDENTIFIED** | `1,2,6,20,68,...,25390056` is exactly the numerator sequence for balanced words accepted by `I_(N,1)`, for even `N=0,2,...,28`. FLSY bounds its asymptotic proportion but does not enumerate these finite numerators. |
| Exact enumeration / RR terminology | **PRIOR-ART-NOT-FOUND** | No source was found listing that sequence or naming the same restricted boundary-pair reduction. This is only a bounded search result, not evidence of novelty. |

The decisive result is therefore not a new acceptance-asymptotic theorem. It
is a short, exact reduction to a family for which FLSY already proved the
needed stretched-exponential upper bound.

## 2. Exact FLSY attribution and numbering

The primary sources are:

- Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir
  Yehudayoff, “Multilinear Algebraic Branching Programs and the
  Min-Partition Rank Method,” *41st Computational Complexity Conference
  (CCC 2026)*, LIPIcs 383, Article 22, 22:1--22:20. [Official record and
  BibTeX](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.22),
  [proceedings PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol383-ccc2026/LIPIcs.CCC.2026.22/LIPIcs.CCC.2026.22.pdf),
  [DOI 10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22).
- The longer version is [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/),
  2026.

The numbering is as follows.

| Content | CCC 2026 proceedings | ECCC full version |
|---|---:|---:|
| `(epsilon,k)`-balanced-chain definition | Definition 5 | Definition 1.4 |
| Random-permutation covering lemma, introductory statement | Lemma 6 | Lemma 1.5 |
| Same lemma, formal section statement | Lemma 14 (Lemma 6) | Lemma 2.3 (Lemma 1.5) |
| `m`-interval family `I_(n,m)` | Definition 11 | Definition 2.1 |
| Intervals-versus-random-partitions theorem, introductory statement | Theorem 8 | Theorem 1.7 |
| Same theorem, formal statement | Theorem 23 (Theorem 8) | Theorem 4.4 (Theorem 1.7) |

The official title of Lemma 6/Lemma 1.5 is **“Worst-case to average-case
reduction.”** Its mathematical direction is the one needed here: average-case
success of one fixed family is amplified, using random relabelings, into a
fixed family working for every balanced coloring.

The full-version proof of Lemma 2.3 takes

```text
r = ceil(n/(p lg e))
```

independent uniform permutations and unions the original set system with
their images. It union-bounds the failure probability over at most `2^n`
balanced colorings and obtains size `(r+1)s = O(sn/p)`. Thus Phase 4A is a
direct application of FLSY. Counting distinct subsets only makes FLSY's
upper bound smaller: the literal union has at most the sum of the copy sizes,
with coincident subsets counted once.

For the interval result, Definition 2.1/Definition 11 defines `I_(N,m)` as
all unions of at most `m` ordinary intervals of `[N]`; in particular,
`I_(N,1)` includes the empty set and every ordinary interval. The exact
formal statement, Theorem 4.4/Theorem 23, says that a universal `c>0` exists
such that, for every sufficiently large even `N`, `I_(N,1)` is not an
`(epsilon,k)`-balanced-chain set system whenever

```text
epsilon > 2^(-c N^(1/5))    and    k < N^(1/5).
```

The proceedings introductory Theorem 8 states the equivalent asymptotic
form `epsilon > 2^(-Omega(N^(1/5)))`, `k<N^(1/5)`. The ECCC introductory
Theorem 1.7 uses a coarser universal-power formulation; the explicit `1/5`
quantifiers are in its formal Theorem 4.4. Setting `k=1` is legitimate for
all sufficiently large `N`. If `p_N` denotes the actual probability that
`I_(N,1)` accepts a uniform balanced coloring, the definition and theorem
give

```text
p_N <= 2^(-c N^(1/5)).
```

No endpoint ambiguity affects this inference: if `p_N` were strictly above
the displayed threshold, an `epsilon` strictly between them would contradict
the theorem.

## 3. Independent reconstruction of the rooted equivalence

Let `n=2m`, `q=n-1`, and normalize a balanced coloring of
`Z_q union {infinity}` so that `f(infinity)=-1`. The finite cycle then has
total sign `+1`. For a finite point `r`, let `E_r` be the event that an
accepted `RR_n` chain starts with the singleton `{r}`. Cut the remaining
finite points at `r` and linearly order

```text
V_r = Z_q \ {r} = (r+1,r+2,...,r-1).
```

An `RR_n` chain rooted at `r` necessarily has

```text
empty, {r}, {infinity} union I_1, ..., {infinity} union I_q,
```

where `I_1={r}`, `I_q=Z_q`, and each `I_j` is a cyclic interval containing
`r`, growing by one endpoint at a time. Put

```text
J_s = Z_q \ I_(q-s),    0 <= s <= q-1.
```

The `J_s`, in increasing `s`, form a maximal chain of ordinary intervals in
`V_r`. Conversely, complementing and reversing any maximal ordinary-interval
chain on `V_r` gives precisely such nested cyclic intervals containing `r`.
This is a bijection of chains, including the empty, singleton, rank-two, and
full-set states.

The discrepancy identity is exact:

```text
f(J_s) = f(Z_q)-f(I_(q-s))
       = 1-f(I_(q-s))
       = -f({infinity} union I_(q-s)).
```

The rank-two state also forces `f(r)=+1`. Hence

```text
E_r  iff  f(r)=+1 and f|V_r is accepted by I_(n-2,1).
```

This proof was reconstructed independently of the Cycle-4 proposer. The
separate exhaustive checker `cycle04_probability_interval_reduction.py`
then compared the full literal `RR_n` induced DAG with the interval DAG for
every rooted instance through `n=14`; all `15,591` rooted instances in the
run passed. More precisely, it checked respectively
`1, 6, 30, 140, 630, 2772, 12012` rooted instances for
`n=2,4,...,14`, and reproduced ordinary-interval accepted counts
`1,2,6,20,68,236,834`. The finite check corroborates, but is not a substitute
for, the all-`n` bijection above.

FLSY does not state this as an `RR_n` or deque lemma. However, its proof of
the interval theorem already represents an ordinary interval chain through
its first and last inserted elements, two endpoint-growth walks, and a
cyclic-interval cut. The underlying interval geometry is therefore close to
their proof, and no novelty should be claimed for the complement/reversal
observation without expert review.

## 4. Acceptance bound and exact scope

Conditional on `f(r)=+1`, the restriction to `V_r` is a uniform balanced
coloring of `n-2` linearly ordered points. Since

```text
Pr[f(r)=+1] = m/(n-1),
```

the rooted equivalence gives

```text
Pr[E_r] = (m/(n-1)) p_(n-2).
```

Every accepted RR chain has some finite rank-one root. A union bound over
the `n-1` roots yields

```text
A_n = Pr[union_r E_r]
    <= m p_(n-2)
    <= (n/2) 2^(-c (n-2)^(1/5))
     = exp(-Omega(n^(1/5))).
```

Thus, for every fixed `d`, eventually `A_n<n^(-d)`. This rigorously refutes
the inverse-polynomial premise proposed for the simple RR symmetrization
route.

There are two useful ways to state the resulting limitation.

1. FLSY's random-cover construction, or the exact Phase-4A union bound, uses
   witnesses contained in an individual relabelled copy. Its prescribed
   copy count is stretched exponential when supplied with this `A_n`.
2. More strongly, every relabelled copy individually accepts exactly an
   `A_n` fraction of balanced colorings. The union of the individual
   acceptance sets of `t` copies has measure at most `t A_n`; therefore any
   cover by within-copy witnesses requires `t >= 1/A_n`, also stretched
   exponential.

Neither statement applies to a coloring accepted only by a chain that
switches between subsets contributed by different copies. Such hybrid paths
are valid in the full induced subset DAG and can only increase acceptance.
Consequently this audit does **not** prove that every polynomial list of RR
relabelings fails, and it does not obstruct an explicit multi-RR construction
that exploits hybrids. It settles S4-D only for the acceptance-probability /
individual-copy symmetrization argument.

## 5. Exact Phase-4A relation to FLSY

For completeness, if `M=binom(n,n/2)` and `0<A_n<1`, then `t` independent
permutations miss a fixed balanced coloring with probability
`(1-A_n)^t`. The least integer certified by the strict union-bound condition

```text
M (1-A_n)^t < 1
```

is

```text
floor(ln(M)/(-ln(1-A_n))) + 1.
```

This exact threshold and the replacement of `2^n` by `M` refine constants
and rounding in FLSY Lemma 2.3; the symmetry principle and the literal-union
construction are already theirs. No hidden orientation problem occurs:
`f o pi` is uniform on balanced colorings, and applying `pi` to every
literal subset transports chains bijectively. There is no odd-intermediary
problem because whole maximal chains, not contracted pair paths, are
permuted. The family is fixed before the random permutations are sampled,
and the probabilistic method fixes one successful list afterward.

## 6. Sequence and adjacent-literature audit

Let

```text
b_N = number of balanced binary words of length N accepted by I_(N,1).
```

The rooted bijection identifies the prompt sequence exactly as

```text
b_0,b_2,...,b_28 =
1,2,6,20,68,236,834,2984,10760,38996,141834,517284,
1890742,6923424,25390056.
```

This identification is mathematical, not an OEIS inference. It also gives
the denominator `binom(N,N/2)` and hence the FLSY probability `p_N`.

The closest primary-source literatures located were:

- Crespi Reghizzi and San Pietro, “Deque Languages, Automata and Planar
  Graphs,” DLT 2018, [arXiv:1806.06562](https://arxiv.org/abs/1806.06562),
  [DOI 10.1007/978-3-319-98654-8_20](https://doi.org/10.1007/978-3-319-98654-8_20).
  Their characteristic deque language records typed front/tail insertion
  and extraction operations and corresponding cancellations. It supplies
  genuine deque terminology, but not the present two-color boundary-pair
  predicate, rooted interval counts, or acceptance probability.
- Kemp, Mahlburg, Rattan, and Smyth, “Enumeration of Non-Crossing Pairings
  on Bit Strings,” *Journal of Combinatorial Theory, Series A* 118 (2011),
  129--151, [arXiv:0906.2183](https://arxiv.org/abs/0906.2183),
  [DOI 10.1016/j.jcta.2010.07.002](https://doi.org/10.1016/j.jcta.2010.07.002).
  They enumerate all noncrossing complementary pairings of a fixed bit
  string. Existence of an arbitrary noncrossing complementary pairing is
  broader than the RR rule, which permits deletion only at the first two,
  last two, or first/last boundary positions of the current word.
- Brignall, “Permutations sortable by deques and by two stacks in parallel,”
  *European Journal of Combinatorics* 59 (2017), 71--95,
  [DOI 10.1016/j.ejc.2016.08.002](https://doi.org/10.1016/j.ejc.2016.08.002).
  Its objects and enumeration are sortable permutations/canonical operation
  sequences, not balanced binary words or interval-chain acceptance.

These papers are structural neighbors, not sources for the displayed
sequence or the FLSY probability bound. Searches for bichromatic noncrossing
matchings, plane-tree foldability, queue/deque graph layouts, and matching
pattern avoidance likewise returned broader geometric, graph-layout, or
unrestricted matching objects. No equivalence was found.

## 7. Search protocol and negative-result limits

The audit used the official FLSY proceedings PDF and full ECCC text, exact
phrase and formula searches, arXiv-facing searches, general scholarly/web
search, DOI/citation metadata, and an OEIS sequence check. Query families
included the following literal strings and close punctuation variants:

- the full numeric prefix and long fragments such as
  `"1, 2, 6, 20, 68, 236, 834, 2984"`,
  `"236, 834, 2984, 10760"`, and
  `"141834, 517284, 1890742"`;
- `"deque-reducible" word`, `"deque matching" binary word`, and
  `delete "first two" "last two" "first and last"`;
- `opposite symbols boundary deletion`, `connected bichromatic peeling`,
  `noncrossing matching recursive boundary`, and `foldable binary word`;
- `maximal chain intervals balanced binary word`, `interval-growth chain`,
  and `chain-balance interval set system`;
- `"random relabeling" interval set system`,
  `"union of permuted interval families"`, and cyclic-interval variants.

The current OEIS stripped-data snapshot was searched for several contiguous
subsequences of lengths three through eight, including the large-tail
fragments above; no match was found. OEIS is a secondary index, and absence
there has no novelty force. Exact web searches found unrelated numerical
sequences or no indexed result. The FLSY PDFs contain neither the displayed
finite sequence nor the terms `deque` or `round-robin`; their use of cyclic
intervals in the proof of the ordinary-interval theorem was inspected
separately as noted above.

Negative searches remain incomplete for several reasons:

1. The same recurrence may be encoded as an interval-growth path,
   two-ended elimination order, restricted noncrossing matching, deque
   language, lattice path, or permutation class without sharing keywords.
2. Sequence databases omit unsubmitted, shifted, transformed, or
   parameterized arrays; exact finite counts can also be buried in tables,
   theses, code, or supplements.
3. Citation and metadata indexes lag recent 2026 work and do not reliably
   cover ECCC-only reports, workshops, or non-English sources.
4. The rooted-equivalence observation is elementary enough to be folklore or
   implicit in endpoint-growth arguments even if not stated as a theorem.
5. The audit cutoff is 2026-08-21. Unindexed, private, or later work is not
   excluded.

Accordingly, “not found” above means only **PRIOR-ART-NOT-FOUND IN THIS
SEARCH**. It must not be promoted to a novelty claim.

## 8. Bottom line

FLSY's symmetrization lemma is the exact prior attribution for Phase 4A, and
their ordinary-interval theorem becomes decisive after the independently
verified rooted complement/reversal bijection. For all sufficiently large
even `n`,

```text
A_n <= (n/2) 2^(-c (n-2)^(1/5)) = exp(-Omega(n^(1/5))).
```

This is a rigorous S4-D obstruction to the proposed inverse-polynomial
acceptance / individual-copy relabeling route. It is not a matching
asymptotic formula for `A_n`, not a lower bound on `N(n)`, and not an
obstruction to hybrid paths in literal unions of multiple RR copies.

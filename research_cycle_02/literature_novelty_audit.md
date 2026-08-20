# Cycle 2 independent literature and novelty audit: balanced chains and the stale-frontier process

**Search cutoff:** 2026-08-13 (Europe/Madrid).  
**Role:** independent literature/novelty verifier.  
**Scope:** (i) a repair or follow-up establishing O01 after the withdrawal of TR26-043; (ii) prior exact values of `N(2), N(4), N(6), N(8)` or computations in the equivalent read-once alternating-pair DAG model; and (iii) prior analyses of the actual stale-frontier `d`-block process.  
**Independence:** I did not open or use the new Cycle-2 proof-complexity, meta-complexity, exact-value, or process-analysis reports. The elementary checks below were derived directly from the definitions and the primary papers. No repository computation is treated here as literature evidence.

## Status vocabulary used here

The labels in this audit have deliberately narrow meanings.

- `KNOWN`: supported by an identified primary source, or an elementary consequence whose complete derivation is given here.
- `PRIOR-ART-NOT-FOUND`: the stated searches did not locate a public source. This is a negative search result, **not** a claim of novelty, priority, or exhaustive nonexistence.
- `UNKNOWN-STATUS`: the proposed statement is not precise enough, or the available evidence is insufficient, to classify its mathematical truth. Failure to locate prior art does not change this label.

`OPEN` is used separately for the public mathematical status of O01. It is not being inferred merely from search-engine silence: the active foundational paper explicitly leaves the exact complexity open, and the only located polynomial claim was officially withdrawn because every result depends on a gap.

## Executive disposition

| Item audited | Classification | Evidence and qualification |
|---|---|---|
| FLSY upper bound `N(n) <= n^{O(log n / log log n)}` | `KNOWN` | Theorem 1.6/Theorem 3.3 of active [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/download/), for sufficiently large even `n`. |
| FLSY publication status | `KNOWN` | Active ECCC report dated 2026-01-01; also #22 on the [official CCC 2026 accepted-paper list](https://computationalcomplexity.org/Archive/2026/accepted_papers.html) and listed in the [official program](https://computationalcomplexity.org/Archive/2026/program.html) for 2026-08-06. No correction or withdrawal is posted on its ECCC record as of the cutoff. |
| TR26-043 status | `KNOWN` | [arXiv:2604.00746](https://arxiv.org/abs/2604.00746) explicitly says “withdrawn” in v2 (2026-05-11). The [ECCC record](https://eccc.weizmann.ac.il/report/2026/043/) retains the report but posts Revision #1 stating that Lemma 4.1 is not valid conditionally on the filtration and that all results rely on it. |
| A post-withdrawal proof of O01, `N(n)=n^{O(1)}` | `PRIOR-ART-NOT-FOUND` | No repair, replacement proof, follow-up, or citing paper establishing O01 was located. The public target therefore remains `OPEN` on the verified record. This is not a novelty conclusion. |
| `N(2)=3` | `KNOWN` | Immediate from the definition; proof below. No explicit prior table was located. |
| `N(4)=6` | `KNOWN` | Immediate small-case argument; proof below. No explicit prior table was located. It should not be advertised as substantive novelty. |
| Prior published exact values/computations for `N(6)` or `N(8)` | `PRIOR-ART-NOT-FOUND` | Exact-notation, terminology, numeric-sequence, SAT/ILP/exhaustive-search, and equivalent-DAG searches found no relevant record. This audit does not validate any repository value. |
| Prior exact alternating-pair/read-once DAG computation under a compatible size convention | `PRIOR-ART-NOT-FOUND` | FLSY introduces the equivalent model and says its exact complexity is open, but gives no finite table. Older-model terminology searches found no matching computation. |
| True-filtration all-same-frontier one-step identity `(n/2-d)/(n-d)` | `KNOWN` | Exact elementary hypergeometric calculation given below. |
| A prior source applying that identity to the TR26-043 stale-frontier process | `PRIOR-ART-NOT-FOUND` | Exact formula, filtration, queue-head, adaptive-interleaving, and withdrawal-follow-up searches found none. |
| Standard first-passage tails for a simple symmetric random walk | `KNOWN` | For example FLSY Lemma 4.5, citing Feller and Bhattacharya--Waymire, proves `Pr[F_delta >= z] = Theta(delta/sqrt(z))` in its stated range. |
| A fixed-`d` return-tail theorem for the **actual stale-frontier adaptive process** | `UNKNOWN-STATUS` | The one-step atom does not establish an excursion or return-time law; dependencies persist. No process-specific source was found, and exact quantifiers/coupling remain to be stated and proved. |
| Full `d`-prefix-grid state count `prod_i (m_i+1)` | `KNOWN` | Elementary injective counting for disjoint blocks; derivation below. |
| A general drift-versus-state-count impossibility theorem for all `d`-block repairs | `UNKNOWN-STATUS` | The fixed-`d` atom plus full-grid count is a valid warning for that particular materialized-grid scheme, not a no-go theorem for sparse DAGs, compressed states, or different adaptive constructions. No such general theorem was found. |

## 1. Official ground truth: FLSY and TR26-043

### 1.1 FLSY is active and gives the verified quasi-polynomial upper bound

The official [ECCC landing page for TR26-001](https://eccc.weizmann.ac.il/report/2026/001/) records:

- title: *Multilinear Algebraic Branching Programs and the Min-Partition Rank Method*;
- authors: Théo Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir Yehudayoff;
- publication date: 2026-01-01;
- no posted revision, gap notice, or withdrawal as of 2026-08-13.

In the [official paper](https://eccc.weizmann.ac.il/report/2026/001/download/), Definition 1.2 defines a `k`-balanced-chain set system. For even `n`, the proof of Theorem 3.3 defines `N(n)` to be the minimum size of a 1-balanced-chain set system over `[n]`. Theorem 1.6/Theorem 3.3 states, for every sufficiently large even `n`,

```text
N(n) <= n^{O(log n / log log n)}.
```

The paper explicitly calls the exact complexity of its equivalent nondeterministic read-once branching-program model an open question. It also notes that the construction, and hence the mABP obtained from it, is nonuniform. Nothing in the active FLSY version proves `N(n)=n^{O(1)}`.

The official [CCC 2026 accepted-paper list](https://computationalcomplexity.org/Archive/2026/accepted_papers.html) includes FLSY as paper #22. The [CCC 2026 program](https://computationalcomplexity.org/Archive/2026/program.html) lists its talk at 14:30 on 2026-08-06. These records establish acceptance and program listing; this audit does not infer any stronger bibliographic status that is not shown by an official proceedings record.

### 1.2 The polynomial claim is withdrawn; the surviving ECCC abstract is stale evidence

The official [arXiv record for 2604.00746](https://arxiv.org/abs/2604.00746) says:

- v1 submitted 2026-04-01;
- v2 posted 2026-05-11 and marked **withdrawn**;
- no PDF is available for v2;
- the comments report that Lemma 4.1 only bounds the forced probability unconditionally, not conditionally on the filtration required by the supermartingale argument, and that all results rely on the lemma.

The official [ECCC TR26-043 page](https://eccc.weizmann.ac.il/report/2026/043/) is slightly different administratively: it retains the original report and its theorem-claiming abstract, but Revision #1, dated 2026-05-11, posts the same fatal-gap notice. Thus the exact status is:

> The work is explicitly withdrawn on arXiv; ECCC retains the report page and v1 download with an official revision notice saying that the conditional lemma is unsupported and every result depends on it.

The still-visible ECCC abstract and downloadable v1 PDF are therefore **not** evidence that O01 is proved. Secondary pages that copied that abstract are likewise not repair evidence.

### 1.3 Repair/follow-up audit for O01

I searched exact title, author, report number, theorem terminology, gap language, likely repair terminology, citations, and current 2026 complexity-theory records. The strongest negative checks were:

- The arXiv API query `all:"balanced-chain"` returned four metadata hits. Only the withdrawn Kush preprint was relevant; the other three were terminology collisions. `all:"1-balanced-chain"` and `all:"min-partition rank"` each returned only the withdrawn preprint. FLSY is ECCC-only, illustrating why this query alone is not exhaustive.
- The current [author homepage](https://sites.google.com/view/deepkush/) still lists the same preprint with the arXiv and ECCC links, and lists no correction or replacement.
- The current ECCC author page and 2026 rank-method/balanced-chain searches exposed TR26-001 and TR26-043, but no later repair.
- The Semantic Scholar citations API for `ARXIV:2604.00746` returned an empty `data` array on the cutoff date. An OpenAlex search by the identifier string returned zero works. These are only lag-prone secondary-index checks.
- DBLP lists TR26-043 as an informal ECCC publication and lists no replacement on the author's record.
- Crossref title search returned no exact repaired article.
- Exact GitHub code searches for `"1-balanced-chain"`, `"balanced-chain set system"`, `"2604.00746"`, and `"min-partition rank" "N(n)"` returned no code hits.

**Disposition.** A valid post-withdrawal proof of O01 is `PRIOR-ART-NOT-FOUND` through 2026-08-13. The mathematical target remains `OPEN` on the verified public record. Unpublished work, a privately circulated repair, or an unindexed manuscript cannot be excluded by this audit.

## 2. Exact small values and the equivalent DAG model

### 2.1 Conventions matter

Under FLSY's convention a set system is a family `X subseteq P([n])`, its size is the number of distinct subsets, and it must contain, for every balanced coloring, an entire maximal chain

```text
emptyset = C_0 subset C_1 subset ... subset C_n = [n],  |C_i|=i,
```

with every prefix imbalance at most one.

For a 1-balanced chain, the two elements inserted between `C_{2j}` and `C_{2j+2}` have opposite colors. Compressing every two insertions gives the FLSY read-once DAG model: each source--sink path has `n/2` edges, an edge is labelled by a pair of variables, and it is open exactly when the pair is bichromatic. Conversely, an open pair path can be expanded by choosing orders for the two elements in every pair.

This is an equivalence of functionality, but **raw exact sizes are not automatically identical**. A set-system size counts odd and even prefix subsets; a DAG size may count vertices, edges, or only even-level states. Any claimed prior exact DAG value therefore needs an explicit normalization before it can be identified with `N(n)`.

### 2.2 Two routine base cases

These checks are included to prevent an absence-of-citation claim from turning trivial facts into novelty claims.

#### `N(2)=3`

Every maximal chain of `P([2])` has three sets, so `N(2)>=3`. The family

```text
{ emptyset, {1}, {1,2} }
```

is 1-balanced for either balanced coloring, so `N(2)=3`.

#### `N(4)=6`

A family of size five that contains a maximal chain consists exactly of that one chain. Color the first two elements in its permutation `+` and the last two `-`; its size-two prefix then has imbalance two. Hence `N(4)>=6`.

For the upper bound, use

```text
X = { emptyset, {1}, {1,2}, {1,3}, {1,2,3}, [4] }.
```

In any balanced coloring of four elements, at least one of elements `2,3` has color opposite to element `1`; otherwise the first three elements would have one sign, impossible in a two-plus/two-minus coloring. Choose the chain through `{1,2}` or `{1,3}` accordingly. Its even prefixes are balanced and its odd prefixes have imbalance one. Thus `N(4)<=6`, proving `N(4)=6`.

These values are `KNOWN` by direct argument even though no explicit prior table was found.

### 2.3 Searches for `N(6)`, `N(8)`, and finite DAG computations

The following families of searches produced no relevant primary source, paper, thesis, code repository, or database entry:

- exact notation: `"N(2)" "balanced-chain"`, `"N(4)" "balanced-chain"`, `"N(6)" "balanced-chain"`, and `"N(8)" "balanced-chain"`;
- method terms: `"balanced-chain set system" exact`, `computer search`, `SAT`, `ILP`, `set cover`, `optimizer`, and `exhaustive`;
- size language: `"minimum size" "balanced-chain set system"` and `"1-balanced-chain set system"`;
- FLSY-equivalent model language: `"nondeterministic read-once branching program" "Hamming weight" "n/2"`, `"Each edge" "labeled by two variables" "Hamming weight"`, `"open path" "xi + xj = 1" branching program`, and bichromatic-pair/perfect-matching variants;
- terminology variants: `"universal alternating chain"`, `"alternating-chain DAG"`, adaptive pairing, universal pairing, and read-once alternating-pair DAG;
- candidate-number check: `"3, 6, 12, 20" "balanced chain"` and the same sequence with branching-program/Hamming-weight terms. Hits were unrelated numeric collisions;
- public code: GitHub exact-code queries listed in Section 1.3.

Direct text searches in FLSY for `computer`, `small values`, `exact`, and finite `N(2)` tables found no computation. The paper says the equivalent program's exact complexity remains open.

**Disposition.** An explicit published/citable exact computation for `N(6)` or `N(8)`, or a normalized equivalent-DAG computation, is `PRIOR-ART-NOT-FOUND`. This does not establish that a repository computation is novel, and this audit has not checked its certificates. Exact `N(2)` and `N(4)` should be treated as routine `KNOWN` base cases.

## 3. The actual stale-frontier `d`-block process

### 3.1 Why the filtration is different from fresh sampling

In the block process, the rule inspects the current head of each unfinished block before choosing which head to consume. Unchosen heads persist. A faithful filtration therefore contains:

1. every consumed element and its sign;
2. every inspected frontier element and its sign, including unconsumed heads; and
3. the rule's random coins and previous choices.

Calling an unconsumed head “unrevealed” merely because it has not been appended to the chain loses information already used by the algorithm. Conditional exchangeability among all remaining positions is therefore unavailable.

### 3.2 Exact true-filtration atom

Consider the atom at which the `d` initially exposed, distinct block heads are all `+` under a uniformly random balanced coloring of `n` positions, with exactly `n/2` plus signs. The rule consumes one of these `+` heads. The other `d-1` heads remain known stale `+` values. Only the successor revealed behind the consumed head is fresh.

Among the `n-d` positions not exposed on this atom, exactly `n/2-d` are `+`. Therefore

```text
Pr[next frontier is again all + | true filtration, all d heads are +]
    = (n/2-d)/(n-d)
    = 1/2 - d/(2(n-d)).
```

The all-minus atom is symmetric. More generally, at later histories the numerator and denominator must be updated using all signs already exposed, not just elements already consumed.

This identity is `KNOWN`: it is a one-draw hypergeometric conditional probability, and the derivation above is complete. For fixed `d` it tends to `1/2`, not to a fresh-sampling value of order `2^{-d}`. What is `PRIOR-ART-NOT-FOUND` is an earlier public source identifying and exploiting this exact atom for the TR26-043 process.

### 3.3 What standard random-walk theory does and does not supply

For an ordinary simple symmetric walk, first-passage and return tails are classical. In particular, [FLSY Lemma 4.5](https://eccc.weizmann.ac.il/report/2026/001/download/) states that if `F_delta` is the first passage time to `delta` and `Omega(delta^2) <= z <= n/2`, then

```text
Pr[F_delta >= z] = Theta(delta/sqrt(z)).
```

FLSY cites Feller and Bhattacharya--Waymire for the exact first-passage distribution. It also uses the Csáki--Erdős--Révész longest-excursion result for a random bridge.

Those facts do **not** automatically transfer to the stale-frontier process. The next selected sign is influenced by known persistent heads and by the adaptive choice history. The exact one-step atom shows near-unbiased persistence for fixed `d` on a particular history, but it does not alone give a Markov chain, a coupling over whole excursions, or a return-time lower bound.

Accordingly:

- standard symmetric-walk tails are `KNOWN`;
- a prior process-specific analysis is `PRIOR-ART-NOT-FOUND`;
- a theorem asserting fixed-`d` near-unbiased return tails for the actual process is `UNKNOWN-STATUS` until its state space, stopping time, conditioning, quantifiers, and comparison walk are stated precisely and proved.

### 3.4 Full-prefix-grid state count and its limitation

Let the `d` disjoint blocks have lengths `m_1,...,m_d`. If a construction materializes every possible union of a prefix from each block, its states are indexed by

```text
(k_1,...,k_d),  0 <= k_i <= m_i.
```

Distinct vectors give distinct subsets because the blocks are disjoint. Hence the number of states is exactly

```text
prod_{i=1}^d (m_i+1).
```

For nearly equal blocks this is about `(n/d+1)^d`. It is polynomial for fixed `d`. If `d=d(n)` is unbounded, it is superpolynomial: when `d<=sqrt(n)` it is at least `n^{d/2}` (up to harmless floor effects), while when `d>sqrt(n)` it is at least `2^d`.

This counting statement is `KNOWN`. Combined with the atom above it gives a concrete design tension:

- fixed `d` permits a polynomial full grid, but the all-same frontier persists with one-step probability approaching `1/2`;
- growing `d` may offer more heads away from the stale atom, but the fully materialized prefix grid is superpolynomial.

It is **not** a lower bound for every repair. A sparse DAG might omit most grid states, merge histories, use a different posterior statistic, or abandon the block scheme. The general claim that drift and state count rule out every polynomial construction is therefore `UNKNOWN-STATUS`. The process-specific articulation was `PRIOR-ART-NOT-FOUND` in the searched record.

### 3.5 Adjacent literature checked and why it does not subsume the process

The closest located primary works use materially different randomness or control models:

1. Agelos Georgakopoulos, John Haslegrave, Thomas Sauerwald, and John Sylvester, [*The Power of Two Choices for Random Walks*](https://arxiv.org/abs/1911.05170), *Combinatorics, Probability and Computing* 31(1):73--100 (2022), DOI [10.1017/S0963548321000183](https://doi.org/10.1017/S0963548321000183). At every step the controller receives two **independent fresh** uniformly sampled neighbors. There are no persistent inspected queue heads.
2. Emilio De Santis and Mauro Piccioni, [*Infinite paths on a random environment of Z^2 with bounded and recurrent sums*](https://arxiv.org/abs/1906.02048), *Journal of Statistical Physics* 176 (2019), DOI [10.1007/s10955-019-02333-0](https://doi.org/10.1007/s10955-019-02333-0). Edge labels live in an i.i.d. two-dimensional random environment; this is not a balanced finite coloring split into persistent one-dimensional queues.
3. Nikhil Bansal and Joel H. Spencer, [*On-Line Balancing of Random Inputs*](https://arxiv.org/abs/1903.06898), *Random Structures & Algorithms* 57(4):879--891 (2020), DOI [10.1002/rsa.20955](https://doi.org/10.1002/rsa.20955). Random vectors arrive and the algorithm chooses a sign; the action and revealed-information structure differ from choosing among stale signed heads.
4. Alantha Newman, Ofer Neiman, and Aleksandar Nikolov, [*Beck's Three Permutations Conjecture: A Counterexample and Some Consequences*](https://dimacs.rutgers.edu/~alantha/papers2/beck-focs12.pdf), FOCS 2012, pp. 253--262, DOI [10.1109/FOCS.2012.84](https://doi.org/10.1109/FOCS.2012.84). This fixes permutations and chooses a coloring to force prefix discrepancy; FLSY explicitly notes that balanced-chain systems reverse the central quantifiers and may represent many chains implicitly.

These works are useful neighbors, but none proves the requested atom, tail theorem, or drift-grid obstruction for the actual stale-frontier process.

## 4. Search log

All searches in this table were run on 2026-08-13. Search-engine results were followed to primary papers or official records when a relevant-looking hit appeared.

| Question | Sources | Exact strings / API queries | Result |
|---|---|---|---|
| Official status | ECCC, arXiv, CCC 2026 | `TR26-001`, `TR26-043`, `2604.00746`; official accepted-paper and program pages | FLSY active/accepted/listed; arXiv work withdrawn; ECCC fatal-gap revision posted. |
| O01 repair | Web search, ECCC, arXiv API, author homepage, DBLP, Crossref | `"An Unconditional Barrier for Proving Multilinear Algebraic Branching Program Lower Bounds" -arxiv`; `"2604.00746" repair correction`; `"Deepanshu Kush" "balanced-chain"`; `"Deepanshu Kush" "min-partition rank"`; `"TR26-043"`; `"polynomial-size 1-balanced-chain"`; `"Fabris" "Kush" "balanced-chain"` | No repair or replacement proof found. Stale mirrors repeated the withdrawn abstract. |
| arXiv exact-term sweep | arXiv export API | `all:"balanced-chain"`; `all:"1-balanced-chain"`; `all:"min-partition rank"` | 4, 1, and 1 metadata hits respectively; only relevant hit was withdrawn TR26-043. |
| Citation/follow-up indices | Semantic Scholar API, OpenAlex API, DBLP, Crossref | citations of `ARXIV:2604.00746`; identifier/title queries | Semantic Scholar citations array empty; OpenAlex identifier search zero; DBLP only the original ECCC item; Crossref no exact repair. These indices can lag. |
| Exact finite values | Web search, FLSY full text | `"N(2)" "balanced-chain"`, likewise `N(4),N(6),N(8)`; `"balanced-chain set system" exact`; `computer search`; `SAT`; `ILP`; `exhaustive`; `"minimum size"` | No prior exact table/computation found. FLSY has no small-value table. |
| Candidate sequence | Web search | `"3, 6, 12, 20" "balanced chain"`; `"3,6,12,20" branching program Hamming weight`; exact pair-value variants | Only unrelated numeric collisions. This is not validation of the numbers. |
| Equivalent DAG | Web search, arXiv, DBLP | `"nondeterministic read-once branching program" "Hamming weight" "n/2"`; `"open path" "xi + xj = 1"`; `bichromatic perfect matching read-once branching program`; `universal alternating chain`; `alternating-chain DAG` | FLSY or irrelevant results only; no normalized finite computation. |
| Public code | GitHub code search via `gh search code` | `"1-balanced-chain"`; `"balanced-chain set system"`; `"2604.00746"`; `"min-partition rank" "N(n)"` | Empty result arrays for all four exact queries. |
| True-filtration atom | Web search, arXiv, general scholarly search | `"(n/2-d)/(n-d)"`; `"n/2-d" "n-d" probability`; `"forced probability" "balanced coloring" filtration`; `stale frontier random walk`; `queue heads partial sums random signs` | No process-specific source. Formula collisions/irrelevant probability pages omitted. |
| Adaptive interleaving process | Web/arXiv search | `random signed queues choose among queue heads discrepancy partial sums`; `adaptive interleaving random permutations minimize partial sums`; `online interleaving d sequences random signs bounded partial sum`; `monotone path random sign grid bounded partial sums`; `two-block steering random walk coloring` | Only adjacent random-environment, online discrepancy, or queueing papers; none has the same filtration. |
| Grid obstruction | Web/arXiv search | `prefix grid discrepancy set system`; `d-dimensional prefix grid set system`; `all prefixes d permutations discrepancy`; `prefixes of d permutations discrepancy`; `drift state count adaptive interleaving` | General prefix-discrepancy work, no stale-frontier drift-versus-full-grid result. |

## 5. Negative findings and limitations

1. **No novelty inference.** `PRIOR-ART-NOT-FOUND` reports the outcome of specified public searches. It does not exclude unpublished notes, private correspondence, non-English sources, unindexed theses, or a paper using terminology too remote to retrieve.
2. **Very recent-paper index lag.** TR26-043 is only four months old at the cutoff. Semantic Scholar, OpenAlex, Crossref, and DBLP are discovery aids, not authoritative proof registries. Their empty or sparse results are weak negative evidence.
3. **Stale abstract hazard.** ECCC and several secondary sites still display the original theorem-claiming abstract. The official revision/gap notice and arXiv withdrawal control the evidentiary status.
4. **Terminology collisions.** “Balanced chain” also names scheduling task sets, stochastic-matrix chains, matroid contention-resolution chains, poset notions, and physics models. These false positives were inspected when plausibly relevant and rejected.
5. **Equivalent-model normalization.** A set-system vertex count, a read-once DAG vertex count, and an edge count need not agree exactly. A numerical match without an explicit conversion is not prior art for `N(n)`.
6. **Atom versus path law.** The exact `(n/2-d)/(n-d)` atom refutes a fresh-resampling intuition on that history, but it neither proves a return-tail theorem nor refutes polynomial balanced-chain existence.
7. **Full grid versus all constructions.** `prod_i(m_i+1)` is exact only when every prefix combination is materialized. It is not a lower bound against sparse or compressed representations.

## 6. Citation metadata

### Central sources

- Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir Yehudayoff. *Multilinear Algebraic Branching Programs and the Min-Partition Rank Method*. Electronic Colloquium on Computational Complexity, [TR26-001](https://eccc.weizmann.ac.il/report/2026/001/), 2026. ISSN 1433-8092. Official [PDF](https://eccc.weizmann.ac.il/report/2026/001/download/). Accepted at CCC 2026 according to the official conference list.
- Deepanshu Kush. *An Unconditional Barrier for Proving Multilinear Algebraic Branching Program Lower Bounds*. Electronic Colloquium on Computational Complexity, [TR26-043](https://eccc.weizmann.ac.il/report/2026/043/), 2026; [arXiv:2604.00746](https://arxiv.org/abs/2604.00746), v1 2026-04-01, v2 withdrawn 2026-05-11. DataCite DOI [10.48550/arXiv.2604.00746](https://doi.org/10.48550/arXiv.2604.00746).
- Endre Csáki, Paul Erdős, and Pál Révész. *On the Length of the Longest Excursion*. *Zeitschrift für Wahrscheinlichkeitstheorie und Verwandte Gebiete* 68(3):365--382, 1985. DOI [10.1007/BF00532646](https://doi.org/10.1007/BF00532646). Author-hosted [paper](https://www.renyi.hu/~p_erdos/1985-19.pdf).
- Rabi Bhattacharya and Edward C. Waymire. *Random Walk, Brownian Motion, and Martingales*. Graduate Texts in Mathematics 292, Springer, 2021. DOI [10.1007/978-3-030-78939-8](https://doi.org/10.1007/978-3-030-78939-8).
- William Feller. *An Introduction to Probability Theory and Its Applications*, Volume I, third edition. Wiley, 1968. FLSY cites Theorem 2 on p. 89 for the simple-walk first-passage distribution.

### Machine-readable negative-query endpoints

- arXiv API: [`all:"balanced-chain"`](https://export.arxiv.org/api/query?search_query=all:%22balanced-chain%22&start=0&max_results=100), [`all:"1-balanced-chain"`](https://export.arxiv.org/api/query?search_query=all:%221-balanced-chain%22&start=0&max_results=100), and [`all:"min-partition rank"`](https://export.arxiv.org/api/query?search_query=all:%22min-partition%20rank%22&start=0&max_results=100).
- Semantic Scholar citations API: [`ARXIV:2604.00746`](https://api.semanticscholar.org/graph/v1/paper/ARXIV:2604.00746/citations?limit=100&fields=title,authors,year,url,externalIds). Returned `{"offset":0,"data":[]}` on 2026-08-13.
- OpenAlex identifier search: [`2604.00746`](https://api.openalex.org/works?search=2604.00746&per-page=20). Returned count zero on 2026-08-13; this is an index-coverage fact, not evidence about mathematical truth.

## Bottom line

The verified current baseline is still FLSY's quasi-polynomial upper bound. The only located polynomial proof is withdrawn on arXiv and carries an official fatal-gap notice at ECCC; no public repair was found. Exact `N(2)` and `N(4)` are routine facts, while prior exact `N(6)`/`N(8)` or normalized equivalent-DAG computations were not found. The stale-frontier all-same-head atom has exact next-step probability `(n/2-d)/(n-d)`, but converting that one-step fact into fixed-`d` return tails or a general impossibility theorem remains `UNKNOWN-STATUS`. The full-prefix-grid count is exact for that construction and explains a genuine design tension, not an obstruction to O01 itself.

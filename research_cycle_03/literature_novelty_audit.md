# Cycle 3 literature and novelty/equivalence audit: structural subset DAGs

**Search cutoff:** 2026-08-21 (Europe/Madrid).
**Role:** independent primary-source literature and terminology audit.
**Scope:** exact published values of the balanced-chain minimum at \(n=6,8\); universal/shared subset DAGs; cut-crossing perfect-matching DAGs; universal alternating-chain constructions; and adjacent work on switching/routing networks, branching programs, matching routing, separating systems, covering designs, universal cycles, and Boolean-lattice path covers.
**Independence:** repository claims about the Cycle-2 finite computations are not treated as literature evidence. I read the governance/state files and the Cycle-2 structural report to identify the mathematical object and size convention, then reconstructed the model comparisons below directly from the definitions and primary sources.

## Epistemic labels

- **KNOWN:** stated by an identified primary source, or an elementary implication for which a complete argument is supplied here.
- **DERIVED CONNECTION:** an exact reduction or comparison independently checked here. This label is about correctness, not novelty.
- **PRIOR-ART-NOT-FOUND:** the documented searches did not locate a public source. It is not a novelty, priority, or exhaustive-nonexistence claim.
- **NOVELTY UNCLEAR:** no source making the same formulation was located, but the search cannot exclude unpublished, differently named, or unindexed work.
- **OPEN:** the verified public status of O01. Search silence is not its basis: the active foundational paper leaves the exact complexity open, while the only located polynomial claim is officially withdrawn because its results depend on a stated proof gap.

## Executive disposition

| Question | Disposition | Precise qualification |
|---|---|---|
| Current foundational source | **KNOWN** | Fabris--Limaye--Srinivasan--Yehudayoff now has an official CCC 2026 proceedings version, DOI [10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22), plus the fuller [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/). |
| Polynomial O01 claim in Kush TR26-043 | **withdrawn; not evidence** | [arXiv:2604.00746](https://arxiv.org/abs/2604.00746) is marked withdrawn. The [ECCC record](https://eccc.weizmann.ac.il/report/2026/043/) says the needed bound is unconditional rather than conditional on the filtration and that all results rely on that lemma. No repair was located. |
| Published exact \(N(6)\), \(N(8)\), or \(N(10)\) | **PRIOR-ART-NOT-FOUND** | Exact-notation, finite-value, optimization, certificate, sequence, and equivalent-model searches found no relevant primary source. A narrow post-computation search for `N(10)=35` and equivalent pair-program language was also negative. This does not validate or establish novelty of the repository computations. |
| Published formula \(N(2m)=m(m+1)\) | **PRIOR-ART-NOT-FOUND** | No source was located. The values at \(n=4,6,8\), even if independently certified, remain only finite observations. |
| Pair-labelled open-path program | **KNOWN** | FLSY explicitly introduces the directed acyclic nondeterministic read-once program whose edges query pairs, are open exactly on bichromatic pairs, and whose source--sink paths have length \(n/2\). It says the exact complexity remains open. |
| Exact even-subset path-DAG reformulation | **DERIVED CONNECTION; NOVELTY UNCLEAR as a separately named theorem** | It is an elementary contraction/expansion of 1-balanced maximal chains. FLSY gives the same pair-labelled computational skeleton, but does not identify its raw vertex count with the all-level distinct-subset minimum \(N(n)\). |
| Relation to monotone switching networks | **DERIVED CONNECTION; strict qualification required** | The contracted object is a directed layered acyclic monotone open-path network over cut-edge predicates, restricted to balanced cuts, with every path a perfect matching. General monotone switching networks lack these subset-support and perfect-matching constraints and usually use an undirected state graph. |
| Beneš/Waksman networks, superconcentrators, sorting/routing networks | **KNOWN adjacent objects; no subsumption found** | They share hardware among many routes, but their size counts switches/vertices, not the union of all data-dependent subset-prefix states. A small routing network therefore does not by itself give a small balanced-chain set system. |
| Boolean-lattice “chain covers” \(N(n,r)\) | **KNOWN notation collision** | Nagy--Patkós, [arXiv:2606.29385](https://arxiv.org/abs/2606.29385), minimize the number of maximal chains needed to cover every strict \(r\)-term chain. Their \(N(n,r)\) counts chains/permutations, not distinct subset vertices and not coloring witnesses. |
| A standard object called a crossing-perfect-matching DAG or universal alternating-chain DAG | **PRIOR-ART-NOT-FOUND** | Exact and variant searches returned geometric crossing matchings, alternating paths in matching theory, and unrelated alternating-chain terminology, not the present cut-crossing subset DAG. |

## 1. Current primary-source ground truth

### 1.1 FLSY now has an official proceedings version

The official Dagstuhl record is:

- Théo Borém Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir Yehudayoff, “Multilinear Algebraic Branching Programs and the Min-Partition Rank Method,” *41st Computational Complexity Conference (CCC 2026)*, LIPIcs 383, Article 22, pages 22:1--22:20.
- Official record and BibTeX: [Dagstuhl document page](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.22).
- DOI: [10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22).
- Proceedings PDF: [LIPIcs.CCC.2026.22.pdf](https://drops.dagstuhl.de/storage/00lipics/lipics-vol383-ccc2026/LIPIcs.CCC.2026.22/LIPIcs.CCC.2026.22.pdf).
- Full version: [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/).

Definition 2 of the proceedings paper defines balanced colorings, maximal chains contained in a set system, and \(k\)-balanced-chain set systems. Theorem 7/18 gives

\[
N(n)\le n^{O(\log n/\log\log n)}
\]

for sufficiently large even \(n\). Observation 13 derives the known layer-by-layer lower bound from Alon--Kumar--Volk. The paper does not give exact values at \(n=6\) or \(n=8\).

Most importantly for Cycle 3, pages 5--6 explicitly introduce the following computational model:

- a directed acyclic graph with a source and sink;
- every edge labelled by a pair \((x_i,x_j)\);
- every variable used at most once on any directed path;
- every source--sink path has exactly \(n/2\) edges;
- an edge is open iff \(x_i+x_j=1\);
- acceptance iff there is an open source--sink path;
- the target language is precisely the strings of Hamming weight \(n/2\).

FLSY then asks for the smallest such program and says its exact complexity remains open. Thus the central “shared matching-state” computational viewpoint is direct prior art. What still needs separate accounting is the repository objective: \(N(n)\) counts all distinct odd and even subset states, not only program vertices or descriptions.

### 1.2 The polynomial paper remains withdrawn

The current [arXiv record for 2604.00746](https://arxiv.org/abs/2604.00746) says that the paper was withdrawn in version 2 on 2026-05-11. Its comments identify the problem: the forced-probability estimate used by the supermartingale holds unconditionally but not conditionally on the required filtration.

The [ECCC TR26-043 revision record](https://eccc.weizmann.ac.il/report/2026/043/) independently states that an anonymous referee found this gap in Lemma 4.1 and that all results in the paper crucially rely on the lemma. The theorem-claiming abstract still displayed on mirrors and on the retained v1 report is stale and cannot be used as evidence.

No post-withdrawal repair, replacement, or independent proof was found in the searches described below. Therefore O01 remains **OPEN** on the verified record. This audit makes no mABP separation claim.

### 1.3 New 2026 nearby records checked

Two records published after the foundational ECCC report deserve explicit disambiguation:

1. Zoltán Lóránt Nagy and Balázs Patkós, “Chain Covers in the Boolean Lattice,” [arXiv:2606.29385](https://arxiv.org/abs/2606.29385). They define \(N(n,r)\) as the minimum number of maximal chains whose union, as a collection of chains, covers every strict \(r\)-term chain. A maximal chain is identified with a permutation. This is not the balanced-chain \(N(n)\): it counts covering permutations rather than distinct subset states and has no adversarial coloring or imbalance constraint.
2. Ben Lee Volk, “A Lower Bound for Read-Once Parity Branching Programs,” [arXiv:2607.05944](https://arxiv.org/abs/2607.05944), DOI [10.48550/arXiv.2607.05944](https://doi.org/10.48550/arXiv.2607.05944). It studies branching programs whose queries are parities and cites FLSY in its complexity context. Text and citation inspection found no exact balanced-chain values or construction for the pair-open-path object.

Neither record changes O01 or supplies \(N(6)\) or \(N(8)\).

## 2. Exact \(N(6)\), \(N(8)\), \(N(10)\), and the finite quadratic lead

### 2.1 Search protocol

The update used primary-source landing pages and full texts where available, plus negative searches in arXiv, ECCC, Dagstuhl, Crossref, DBLP, Semantic Scholar citation metadata, general scholarly/web search, and exact title/phrase searches. Query families included:

- “balanced-chain” with \(N(6)\), \(N(8)\), exact value, minimum size, small cases, computer search, SAT, ILP, MILP, CP-SAT, exhaustive search, certificate, and optimizer;
- the exact candidate sequence \(3,6,12,20\), and \(6,12,20,30\), combined with balanced chain, Hamming weight, read-once program, pair-labelled DAG, or Boolean lattice;
- “nondeterministic read-once branching program” with Hamming weight \(n/2\), pair variables, bichromatic pair, and open path;
- universal alternating chain, universal bichromatic pairing, universal perfect-matching DAG, cut-crossing matching DAG, shared subset DAG, subset-state routing, and Boolean-lattice path cover;
- citing/cited-by checks for DOI 10.4230/LIPIcs.CCC.2026.22 and the withdrawn arXiv/ECCC report.

After the Cycle-3 computation produced the internally certified finite value
`N(10)=35`, a separate narrow search added exact combinations of
“balanced-chain”, `N(10)`, `N(10)=35`, size 35, ten variables, Hamming weight
five, bichromatic-pair open path, and pair-labelled/read-once program.  It also
rechecked the FLSY proceedings/full text, ECCC, and arXiv-facing results.  The
hits were the foundational source, the stale theorem-claiming metadata of the
withdrawn report, and terminology collisions; no primary source stating the
finite value or an equivalent size-normalized computation was located.

The arXiv API exact-phrase query

<https://export.arxiv.org/api/query?search_query=all:%22balanced-chain%22&start=0&max_results=100>

returned four metadata records when checked on 2026-08-21. Only the withdrawn Kush paper concerned this object; the remaining hits were terminology collisions. This query also misses ECCC-only records, which is why it is merely one check. Crossref title queries found no exact finite-value paper. The citation trail from the FLSY DOI exposed the withdrawn Kush record and Volk’s parity-BP paper, not a small-value computation.

### 2.2 Disposition

No public primary source was found that states or machine-certifies exact balanced-chain values at \(n=6\), \(n=8\), or \(n=10\). No source was found computing the equivalent pair-labelled program under a size normalization that could be translated to the repository’s “number of distinct subsets” convention.

Accordingly:

- prior published \(N(6)\): **PRIOR-ART-NOT-FOUND**;
- prior published \(N(8)\): **PRIOR-ART-NOT-FOUND**;
- prior published \(N(10)=35\): **PRIOR-ART-NOT-FOUND**;
- prior published formula \(N(2m)=m(m+1)\): **PRIOR-ART-NOT-FOUND**;
- novelty or priority of the repository computations: **not established by this search**.

The finite values in repository state remain computational claims to be checked through their certificates. Literature silence supplies no evidence that the quadratic identity continues at \(n=10\) or asymptotically.

## 3. Exact path-DAG and branching-program comparison

This section separates three objects that are easy to conflate:

1. an all-level set family, whose size is \(N(n)\);
2. a canonical even-subset DAG, whose vertices are subsets of even cardinality;
3. FLSY’s abstract pair-labelled read-once program, whose size convention is program vertices.

### 3.1 Consecutive pairs

Let \(f:[n]\to\{-1,+1\}\) be balanced and

\[
\varnothing=C_0\subset C_1\subset\cdots\subset C_n=[n]
\]

be a maximal chain with \(|f(C_i)|\le1\) for every \(i\). At an even rank \(2j\), the sum \(f(C_{2j})\) is an even integer of absolute value at most one, hence is zero. Therefore

\[
f(C_{2j+2}\setminus C_{2j})
=f(C_{2j+2})-f(C_{2j})=0,
\]

so the two newly added elements are bichromatic. Conversely, if every consecutive pair is bichromatic, every even prefix has sum zero and every odd prefix has sum \(\pm1\). This proves the consecutive-pair characterization without a literature assumption.

### 3.2 Exact contraction and expansion

Given a set family \(\mathcal X\), retain its even-cardinality members as vertices. Put an edge

\[
S\longrightarrow S\cup\{a,b\}
\]

when \(\mathcal X\) contains \(S\), the endpoint, and at least one odd intermediary \(S\cup\{a\}\) or \(S\cup\{b\}\). Label the edge by \(\{a,b\}\).

By the preceding characterization, \(\mathcal X\) is 1-balanced-chain iff, for every balanced coloring, this DAG has a source--sink path all of whose pair labels cross the color cut. Expansion chooses the stored odd intermediary for every traversed edge. This is the exact Cycle-2 path-DAG reformulation.

Its raw size is

\[
|\mathcal X|
= |\text{distinct even states}|
  + |\text{distinct odd states}|,
\]

not the number of described paths and not automatically the number of DAG vertices.

### 3.3 Canonical support lemma for the FLSY program

There is a useful normalization that appears implicit in the FLSY model but was not located as a separately stated lemma.

Delete every vertex and edge not lying on a source--sink path. For a live program vertex \(v\), consider two source-to-\(v\) paths with variable-support sets \(A\) and \(B\). Fix any \(v\)-to-sink suffix with support \(D\). Concatenating either prefix with this suffix gives a source--sink path. Every such path has \(n/2\) pair edges and is syntactically read-once, so it uses exactly \(n\) distinct variables. Hence

\[
A\cup D=[n]=B\cup D,\qquad A\cap D=B\cap D=\varnothing,
\]

and therefore \(A=B=[n]\setminus D\). Thus every live vertex has a canonical used-variable subset \(S_v\). For an edge \(u\to v\) labelled \(\{a,b\}\),

\[
S_v=S_u\cup\{a,b\}.
\]

Vertices with the same support can be merged: any incoming prefix uses exactly \(S\), while any outgoing suffix uses exactly its complement, so merging does not introduce repeated variables. Every resulting full path still labels a perfect matching. The quotient is therefore a canonical even-subset DAG.

Conversely, a canonical even-subset DAG is immediately an FLSY pair program. Thus, under the vertex-count convention and after live-vertex quotienting, the FLSY program and the canonical even-state DAG have the same minimum vertex complexity. This is a **DERIVED CONNECTION**. The exact normalization was not found stated in the literature, so its novelty status is **UNCLEAR**.

### 3.4 Polynomial but not exact equivalence of size measures

Let \(Q(n)\) be the minimum number of distinct even vertices in a canonical pair-DAG satisfying the balanced-cut path condition. Contracting a set family gives

\[
Q(n)\le N(n).
\]

If a canonical DAG \(D\) has \(V\) vertices and \(E\) edges, choose one odd intermediary for each edge and take the union with the even states. This gives

\[
N(n)\le V+E.
\]

After deleting duplicate edges, \(E\le V^2\), so

\[
Q(n)\le N(n)\le Q(n)+Q(n)^2.
\]

Consequently, polynomial-size existence is equivalent between the canonical even-state DAG and the all-level set family up to polynomial blow-up. Exact finite minima need not agree: odd intermediaries can be shared across edges, and \(N(n)\) charges them while the even-state program does not. This is why a branching-program vertex result cannot be reported as exact \(N(6)\) or \(N(8)\) without an odd-state accounting argument.

### 3.5 Cut and matching interpretation

For each unordered pair define the cut predicate

\[
y_{\{a,b\}}(f)=1\quad\Longleftrightarrow\quad f(a)\ne f(b).
\]

Every source--sink path in the canonical DAG partitions \([n]\) into \(n/2\) disjoint pair labels. It is open under \(f\) exactly when those pairs form a perfect matching across the balanced cut \(f^{-1}(+1)\mid f^{-1}(-1)\). Coverage asks that every balanced complete bipartite cut contain at least one routed path-matching.

Equivalently, as a monotone function of arbitrary edge bits \(y\), the DAG accepts when \(y\) contains one of its represented perfect matchings; Cycle 3 only requires completeness on balanced cut vectors. This restricted-domain formulation is important. The predicates \(y_{\{a,b\}}\) are not independent Boolean variables on coloring inputs, and the state vertices must be literal partial supports.

This gives an exact and potentially useful phrase for CP-M:

> a support-consistent, layered, directed acyclic monotone switching network whose accepting paths are perfect matchings and which accepts every balanced cut graph.

No primary source using this full formulation was located. It should be described as a derived reduction with **NOVELTY UNCLEAR**, not as a new object.

## 4. Adjacent literatures and non-equivalences

### 4.1 Switching networks

Aaron Potechin, “Bounds on Monotone Switching Networks for Directed Connectivity,” [arXiv:0911.0664](https://arxiv.org/abs/0911.0664), [ECCC TR09-142](https://eccc.weizmann.ac.il/report/2009/142/), defines a switching network as an undirected state multigraph whose edges are labelled by input literals; an input is accepted when the open labelled subgraph connects the distinguished states. The paper studies directed-connectivity inputs and proves lower bounds for monotone networks. It also analyzes functions on cuts.

The open-path semantics is genuinely close. The balanced-chain DAG is nevertheless a much narrower object:

- its state graph is directed, layered, and acyclic;
- every state has a canonical subset support;
- every transition adds exactly two unused ground elements;
- every full path is a perfect matching;
- completeness is required on balanced complete-bipartite cut graphs, not on all positive instances of directed connectivity.

Potechin’s lower bounds therefore do not transfer directly. His cut-space/Fourier techniques are a plausible toolbox to inspect, but importing them requires a new theorem respecting the support and restricted-input constraints.

### 4.2 Standard read-once branching programs and ZDDs

Allan Borodin, Alexander Razborov, and Roman Smolensky, “On Lower Bounds for Read-\(k\)-Times Branching Programs,” *Computational Complexity* 3 (1993), 1--18, DOI [10.1007/BF01200404](https://doi.org/10.1007/BF01200404), distinguishes the syntactic condition that no variable repeats on any path. This supports the terminology, but its standard Boolean branching programs query variables/literals rather than an XOR predicate on a pair at one edge. FLSY’s custom model is the direct source for the present pair query.

Shin-ichi Minato, “Zero-Suppressed BDDs for Set Manipulation in Combinatorial Problems,” DAC 1993, 272--277, DOI [10.1145/157485.164890](https://doi.org/10.1145/157485.164890), gives a canonical DAG representation that can share structure among large set families. ZDD size counts decision nodes in a fixed variable order. It does not count distinct prefix subsets in a Boolean-lattice inclusion DAG, and it supplies no balanced-cut source--sink coverage theorem. ZDD compression is therefore an implementation/representation analogy, not an O01 construction.

### 4.3 Universal permutation and routing networks

The classical primary sources are:

- V. E. Beneš, “Permutation Groups, Complexes, and Rearrangeable Connecting Networks,” *Bell System Technical Journal* 43 (1964), 1619--1640, DOI [10.1002/j.1538-7305.1964.tb04102.x](https://doi.org/10.1002/j.1538-7305.1964.tb04102.x).
- Abraham Waksman, “A Permutation Network,” *Journal of the ACM* 15(1) (1968), 159--163, DOI [10.1145/321439.321449](https://doi.org/10.1145/321439.321449).
- Nicholas Pippenger, “Superconcentrators,” *SIAM Journal on Computing* 6(2) (1977), 298--304, DOI [10.1137/0206022](https://doi.org/10.1137/0206022).

Beneš/Waksman networks share a small set of switches among all input-output permutations. Superconcentrators guarantee disjoint routes from every equal-size input/output pair. These are strong precedents for shared routing hardware, but neither size metric records all subsets of identities that have passed the first \(j\) routing decisions.

A sorting or permutation network can, after seeing a balanced bit coloring, route the two color classes and thereby describe a bichromatic matching. However, different switch settings can induce exponentially many label-subsets at an intermediate time. To obtain a balanced-chain family one must prove that the union of those partial identity sets is polynomial. Hardware size alone does not prove that accounting statement.

### 4.4 Cut-matching and matching routing

Rohit Khandekar, Satish Rao, and Umesh Vazirani, “Graph Partitioning Using Single Commodity Flows,” STOC 2006, 385--390, DOI [10.1145/1132516.1132574](https://doi.org/10.1145/1132516.1132574), primary author PDF [here](https://people.eecs.berkeley.edu/~vazirani/pubs/partitioning.pdf), introduced the cut-matching framework: a cut player supplies a bisection and a matching player supplies a perfect matching crossing it.

This is the closest established use of “a perfect matching across a cut,” but it is not a universal subset DAG. The matching is chosen adaptively in a multi-round graph-building game; it is not required to be one of the source--sink paths of a fixed support-labelled state graph.

Searches for “matching routing” also returned the distinct routing-via-matchings model in which pebbles are exchanged along a matching in each time step. Searches for “crossing perfect matching” predominantly returned geometric graph theory, where crossing refers to intersecting straight-line edges, for example Aichholzer et al., “Perfect Matchings with Crossings,” *Algorithmica* 86 (2024), DOI [10.1007/s00453-023-01147-7](https://doi.org/10.1007/s00453-023-01147-7). Neither meaning is the color-cut crossing used here.

### 4.5 Separating, bisecting, balancing, and covering families

The closest set-system sources separate coverage from connectivity:

- Gyula O. H. Katona, “On Separating Systems of a Finite Set,” *Journal of Combinatorial Theory* 1(2) (1966), 174--194, [author/archive copy](https://real.mtak.hu/21125/). A separating family distinguishes every pair by membership patterns; it imposes no inclusion-chain routing.
- Niranjan Balachandran, Rogers Mathew, Tapas Kumar Mishra, and Sudebkumar Prasant Pal, “Bisecting and \(D\)-secting Families for Set Systems,” [arXiv:1604.01482](https://arxiv.org/abs/1604.01482). A bisecting family guarantees an approximately half intersection for every target set. This resembles one-layer balance coverage but has no requirement that witnesses at consecutive ranks connect.
- Noga Alon, Mrinal Kumar, and Ben Lee Volk, “Unbalancing Sets and an Almost Quadratic Lower Bound for Syntactically Multilinear Arithmetic Circuits,” *Combinatorica* 40 (2020), 149--178, DOI [10.1007/s00493-019-4009-0](https://doi.org/10.1007/s00493-019-4009-0), preprint [arXiv:1708.02037](https://arxiv.org/abs/1708.02037), and conference version DOI [10.4230/LIPIcs.CCC.2018.11](https://doi.org/10.4230/LIPIcs.CCC.2018.11). FLSY explicitly reinterprets its balancing-set result as a lower bound of order \(\Omega(n/k)\) on each eligible layer, yielding an order-\(\Omega(n^2/k)\) total lower bound (up to the parameter normalization and endpoint layers stated there) for balanced-chain systems. It supplies coverage lower bounds, not gluing.
- Federico Montecalvo, “Some Constructions of General Covering Designs,” *Electronic Journal of Combinatorics* 19(3) (2012), P28, DOI [10.37236/2606](https://doi.org/10.37236/2606). General covering designs guarantee threshold intersections of blocks with every target set. They do not enforce exact half-intersection or connectivity through every rank.

These sources support a sharp methodological distinction for CP-G: proving that each level covers all colorings is not enough. A separate color-specific reachability/gluing theorem is indispensable.

### 4.6 Universal cycles and permutation families

Fan Chung, Persi Diaconis, and Ron Graham, “Universal Cycles for Combinatorial Structures,” *Discrete Mathematics* 110 (1992), 43--59, DOI [10.1016/0012-365X(92)90699-G](https://doi.org/10.1016/0012-365X(92)90699-G), constructs compact cyclic listings through overlap for families including subsets and permutations. A universal cycle is not an inclusion-monotone path DAG and its windows do not supply coloring-specific balanced prefixes.

António Girão, Lukas Michel, and Youri Tamitegama, “Small Families of Partially Shattering Permutations,” *Combinatorica* 46 (2026), Article 10, DOI [10.1007/s00493-026-00201-6](https://doi.org/10.1007/s00493-026-00201-6), preprint [arXiv:2407.05773](https://arxiv.org/abs/2407.05773), studies small permutation families realizing enough local order patterns on each fixed \(k\)-set. That is a family-of-permutations count with local shattering requirements, not a union-of-prefix-subsets count with global alternation for every equipartition.

Exact searches for “universal alternating chain” and “alternating-chain DAG” produced unrelated uses in semigroups, scheduling, matching augmentations, and physics. No standard term for the balanced-chain object was found.

### 4.7 Boolean-lattice path and chain covers

Nagy--Patkós [arXiv:2606.29385](https://arxiv.org/abs/2606.29385) is the most recent direct title collision. It covers every short chain by selected maximal chains; for fixed \(r\) it gives upper and lower bounds differing by a logarithmic factor, and for near-maximal chains it gives other exact/asymptotic results. Those statements cannot be transferred to balanced chains because:

- their cost is the number of selected maximal chains, not the number of distinct vertices in their union;
- the objects to be covered are pre-existing subchains, not balanced colorings;
- there is no discrepancy predicate.

D. Duffus, B. Sands, and P. Winkler, “Maximal Chains and Antichains in Boolean Lattices,” *SIAM Journal on Discrete Mathematics* 3(2) (1990), 197--205, DOI [10.1137/0403017](https://doi.org/10.1137/0403017), proves equivalent fiber/cutset/red-blue statements for colorings of the **vertices of the Boolean lattice**. In O01, the ground elements are colored and a subset inherits a discrepancy sum. The coloring domains and conclusions differ.

These papers are relevant Boolean-lattice context but do not subsume the path-DAG problem.

## 5. Consequences for the Cycle-3 candidate principles

The literature audit yields the following conservative routing:

- **CP-M (shared matching states):** the pair-labelled open-path program is already explicit in FLSY. The useful refinement is to enforce canonical subset support and charge odd intermediaries. The nearest broader language is a restricted monotone switching network on balanced cut graphs. Any claim stronger than this comparison needs a novelty audit.
- **CP-G (layer-cover gluing):** balancing/bisecting/covering families address individual levels. No located source turns simultaneous level coverage into a single color-specific source--sink chain at polynomial state cost. Connectivity remains the missing obligation.
- **CP-S and CP-P:** no source was found for the particular two-anchor spine or paired-leaf/laminar formulations in the Cycle-2 report. Classical laminar and routing constructions are too broad to count as the same class. This is **PRIOR-ART-NOT-FOUND**, not novelty.
- **Universal routing analogy:** Beneš/Waksman/superconcentrator constructions demonstrate that exponentially many routes can share polynomial hardware. The exact obstacle for O01 is that hardware nodes do not remember canonical processed-element subsets. A successful reduction must bound those induced subset states, not only switches.
- **Potential imported technique:** Potechin’s switching-network analysis works with functions on cuts. Because O01 inputs are balanced cuts of \(K_n\), this is a legitimate technical direction to inspect. No transfer theorem was found, and the support-perfect-matching restriction may radically change both upper and lower bounds.

No searched literature justifies \(N(10)=30\), the identity \(N(2m)=m(m+1)\), or any asymptotic extrapolation.

## 6. Negative-search limitations

The negative results above are deliberately narrow.

1. The terminology is unstable. “Balanced chain,” “alternating chain,” “crossing matching,” “matching routing,” and “chain cover” each have large unrelated literatures.
2. Exact phrase searches miss equivalent objects phrased as programs, switching networks, path families, decision diagrams, permutation systems, or discrepancy games.
3. arXiv does not index ECCC-only papers reliably; the FLSY full version itself demonstrates this limitation.
4. Crossref, Semantic Scholar, OpenAlex, DBLP, and citation graphs lag and can omit preprints, theses, workshops, code, and recent proceedings links.
5. Non-English, unpublished, privately circulated, or unindexed work cannot be excluded.
6. Size conventions vary sharply: number of paths, maximal chains, switches, program vertices, labelled edges, decision nodes, and distinct subset states are not interchangeable.
7. A paper may contain an unadvertised small computation or equivalent lemma that title/abstract/full-text keyword searches miss.
8. The search cutoff is only eight days after the Cycle-2 audit cutoff; database ingestion near CCC 2026 is still in motion.

Therefore every “not found” statement must remain **PRIOR-ART-NOT-FOUND**. It is not evidence of novelty and should not be used in a publication claim without a broader expert-led citation review.

## 7. Primary-source index

| Topic | Primary source |
|---|---|
| Balanced-chain systems and pair-open program | FLSY, CCC 2026, DOI [10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22); full [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/) |
| Withdrawn polynomial claim | Kush, [arXiv:2604.00746](https://arxiv.org/abs/2604.00746); [ECCC TR26-043](https://eccc.weizmann.ac.il/report/2026/043/) |
| Boolean-lattice chain covers | Nagy--Patkós, [arXiv:2606.29385](https://arxiv.org/abs/2606.29385) |
| Read-once parity BP, current adjacent record | Volk, [arXiv:2607.05944](https://arxiv.org/abs/2607.05944) |
| Monotone switching networks | Potechin, [arXiv:0911.0664](https://arxiv.org/abs/0911.0664), [ECCC TR09-142](https://eccc.weizmann.ac.il/report/2009/142/) |
| Syntactic read-\(k\) programs | Borodin--Razborov--Smolensky, DOI [10.1007/BF01200404](https://doi.org/10.1007/BF01200404) |
| ZDD set-family sharing | Minato, DOI [10.1145/157485.164890](https://doi.org/10.1145/157485.164890) |
| Rearrangeable routing | Beneš, DOI [10.1002/j.1538-7305.1964.tb04102.x](https://doi.org/10.1002/j.1538-7305.1964.tb04102.x); Waksman, DOI [10.1145/321439.321449](https://doi.org/10.1145/321439.321449) |
| Superconcentrators | Pippenger, DOI [10.1137/0206022](https://doi.org/10.1137/0206022) |
| Cut-matching framework | Khandekar--Rao--Vazirani, DOI [10.1145/1132516.1132574](https://doi.org/10.1145/1132516.1132574) |
| Separating systems | Katona, [archive copy/record](https://real.mtak.hu/21125/) |
| Bisecting families | Balachandran--Mathew--Mishra--Pal, [arXiv:1604.01482](https://arxiv.org/abs/1604.01482) |
| Balancing-set lower bounds | Alon--Kumar--Volk, DOI [10.1007/s00493-019-4009-0](https://doi.org/10.1007/s00493-019-4009-0), [arXiv:1708.02037](https://arxiv.org/abs/1708.02037) |
| General covering designs | Montecalvo, DOI [10.37236/2606](https://doi.org/10.37236/2606) |
| Universal cycles | Chung--Diaconis--Graham, DOI [10.1016/0012-365X(92)90699-G](https://doi.org/10.1016/0012-365X(92)90699-G) |
| Partially shattering permutations | Girão--Michel--Tamitegama, DOI [10.1007/s00493-026-00201-6](https://doi.org/10.1007/s00493-026-00201-6), [arXiv:2407.05773](https://arxiv.org/abs/2407.05773) |
| Boolean-lattice maximal chain/antichain statements | Duffus--Sands--Winkler, DOI [10.1137/0403017](https://doi.org/10.1137/0403017) |

## Bottom line

The strongest exact equivalence found is not a new routing-network theorem: it is FLSY’s own pair-labelled read-once open-path model, normalized into canonical subset supports. The normalization shows polynomial equivalence to \(N(n)\) but also exposes why exact finite values require separate odd-state accounting. Classical switching and routing networks explain how many paths can share a small graph, yet none of the located sources controls the number of distinct processed-element subsets induced by all color-dependent routes.

Published exact \(N(6)\), exact \(N(8)\), exact \(N(10)=35\), and the quadratic finite formula remain **PRIOR-ART-NOT-FOUND** through 2026-08-21. This is a search result only. O01 remains **OPEN**.

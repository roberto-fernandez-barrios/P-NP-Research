# Phase 1 research frontier

**Audit date:** 2026-08-13.  This file contains exactly **25** candidate
intermediate problems.  It does not include P versus NP itself as a candidate
attack.  `OPEN` means unresolved in the audited public literature; confidence
is stated because a negative search cannot prove novelty.

## 1. Ranking method

Each candidate receives five integer scores from 1 (low) to 5 (high):

* `N`: novelty potential after the active “already known?” search;
* `T`: tractability for this research engine;
* `C`: connection to stronger lower bounds or reusable methods;
* `F`: falsifiability by exact counterexamples/certificates; and
* `V`: practicality of formal verification.

The required score is the literal product `N*T*C*F*V`.  Ties are broken by
higher connection, then smaller mathematical distance, then candidate ID as
a stable final tie-breaker.  `D/H/S` are separate 1--5 estimates of distance
from known results, expected difficulty, and significance.  These are triage
judgments, not mathematical measurements.

## 2. Ranked list of 25 candidates

| Rank | ID | Precise unresolved increment | N/T/C/F/V | Product | D/H/S | Main prerequisite and barrier contact | Finite / formal route |
|---:|---|---|---|---:|---|---|---|
| 1 | **O01** | Prove that for every even `n` there exists a 1-balanced-chain system of size at most `n^C`, for one absolute `C`. | 5/3/4/5/5 | **1500** | 2/3/4 | FLSY recurrence/symmetrization; withdrawn adaptive proof has two filtration failures, not a classical P-vs-NP barrier. | Exact set-cover/SAT/ILP for `N(n)`; finite definitions and construction certificates are Lean-friendly. |
| 2 | **O03** | Construct a polynomial-time evaluable `(n,1.83n,2^{o(n)})` quadratic disperser. | 4/3/4/5/4 | **960** | 2/4/4 | Quadratic-variety incidence and weighted gate elimination; local-elimination constants matter only after construction. | Enumerate small quadratic varieties/functions; formalize disperser check and implication. |
| 3 | **O02** | Prove `Sp_CP2(CT_n)=Omega((log log log n)^2)` in the source's inequality-space model. | 4/3/3/5/4 | **720** | 2/3/3 | Must improve the symmetric-slice invariant; `CT_n` has `2^n` clauses and unrestricted CP has space 5. | SAT/SMT search for small normalized configurations; Lean rules/invariants feasible. |
| 4 | **O18** | Verify the July 2026 exact-rational PPSZ certificate and add one valid inequality/statistic giving randomized general 3-SAT base `<1.307031578`. | 3/4/2/5/5 | **600** | 1/2/2 | PPSZ/Scheder--Steinberger analysis and exact LP duality; replication alone is not novelty. | Exact rational checker and dual certificate; unusually suitable for Lean. |
| 5 | **O05** | Remove the proof-size parameter (which the current construction can weaken to proof height) from Buss--Yolcu's effective simulation of Resolution by regular Resolution. | 4/3/3/4/4 | **576** | 2/4/3 | Regular-vs-general separations and transformation uniformity; avoid hiding the parameter in padding. | Test on guarded/pebbling families; syntactic transformation can be formalized. |
| 6 | **O06** | Prove that there exist `epsilon>0`, a field `F`, a polynomial-time explicit connected simple 4-regular expander family `(G_t)`, and odd charges `chi_t` such that PCR over `F` refuting `Ts(G_t,chi_t)` needs monomial space `Omega(|V(G_t)|^{1/2+epsilon})`. | 4/3/3/5/3 | **540** | 2/4/3 | Must remove the width-to-space square-root loss without doubled edges or high vertex degree. | Compute small optimal configurations; formal graph/algebra proof is moderate-large. |
| 7 | **O08** | Prove an explicit-P De Morgan formula lower bound `n^{3+delta}` for some fixed `delta>0`. | 4/2/4/4/4 | **512** | 3/5/4 | Must cross shrinkage/quantum cubic frontier. | Small formula synthesis is weak evidence; restriction/composition lemmas formalizable. |
| 8 | **O07** | Improve full-`B_2` explicit-P size to `(3.1+delta)n-o(n)` for some fixed `delta>0`. | 4/2/5/4/3 | **480** | 2/5/5 | Local gate-elimination barrier; requires new global amortization or O03-like structure. | Exhaust local configurations; machine-check case tables. |
| 9 | **O13** | Prove or refute the repository-defined `k=3` Structured One-Query Robustness statement below for actual CBPHP parity-DAG cells. | 3/2/4/5/4 | **480** | 2/4/4 | Shared collision predicate, one-query closures, safe residual systems; generic affine geometry is refuted. | Search for structured private fibers; exact finite instances/Lean definitions feasible. |
| 10 | **O19** | For depth-two unbounded-fan-in circuits whose gates are arbitrary symmetric or linear-threshold functions and whose total gate count is `m(n)=n^2/exp(sqrt(log log n))`, give deterministic #SAT time `2^n/n^{omega(1)}`. | 4/2/4/5/3 | **480** | 2/5/4 | Tamaki decomposition; Williams closure and all-polynomial-size reach are separate obligations. | Benchmark exact subroutines and verify symbolic savings; full probability proof is large. |
| 11 | **O04** | For all-threshold `MCSP={(x,theta):CC(x)<=theta}`, with `|x|=N`, prove deterministic unrestricted BP size `Omega(N^2/log^C N)` for one fixed `C` (benchmark `C=2`); size counts nonterminal query nodes. | 4/2/3/5/4 | **480** | 2/5/4 | Sharpen the local PRG or replace the MKTP-specific Nechiporuk lemma; the input length `N+O(log N)` does not change the asymptotic. | Enumerate small threshold-input subfunctions; formalize a replacement subfunction lemma. |
| 12 | **O17** | Give a deterministic general 3-SAT algorithm on `n` variables running in `O^*((1.32793-delta)^n)` time for some fixed `delta>0`, with a complete exact branching/covering recurrence. | 4/3/2/5/4 | **480** | 1/3/2 | Liu chain/covering-code framework or new measure; empirical speed is irrelevant. | Exact recurrence/cover certificate; high formalizability. |
| 13 | **O22** | Fix a nondecreasing integer-valued `s` with `n<=s(n)<=n^2/log n` for all large `n`; prove every fan-in-two `B_2` circuit deciding `MCSP[s]` on `N=2^n` input bits has at least `2N-o(N)` **gates**. | 4/1/5/5/4 | **400** | 3/5/5 | Almost-universal hashing plus a direct-sum/gate invariant; naturalness/locality audit required. | Small circuit synthesis can kill invariants; formal cases feasible. |
| 14 | **O23** | For fixed `d>=1,epsilon>0`, prove `MCSP[(log N)^d]` needs probabilistic-formula size `N^{2+epsilon}`, where the model is a finite distribution over De Morgan formulas, pointwise correct with probability at least `2/3`, and size is maximum leaf count in the support. | 4/1/5/5/4 | **400** | 3/5/5 | Strengthen inconsistent-label/PCP-of-proximity machinery at sparse thresholds. | Enumerate obstruction lists; formalization large but certificate-oriented. |
| 15 | **O09** | Prove an explicit-P `n^{3/2+delta}` gate lower bound for arbitrary-weight `THR o THR`. | 4/2/4/4/3 | **384** | 3/5/4 | Anti-concentration/restriction frontier; real weights complicate enumeration. | SMT/duality for bounded integer normalizations; formal real algebra is harder. |
| 16 | **O21** | Prove an explicit-P function requires `n^{5/2+delta}` wires in arbitrary-weight `THR o THR` circuits for some fixed `delta>0`. | 4/2/4/4/3 | **384** | 3/5/4 | Crosses the Kane--Williams wire frontier; the CTW higher-class gate theorem does not imply it. | SMT/duality for bounded normalizations and restriction identities; finite synthesis is weak asymptotic evidence. |
| 17 | **O14** | Determine whether nondeterministic restart-free CDCL with unit propagation, arbitrary decisions, 1-UIP learning, permanent learned-clause retention, and size measured by conflicts polynomially simulates Resolution; otherwise give an explicit superpolynomial separation. | 4/2/3/5/3 | **360** | 3/4/3 | Exact trail/learning semantics and known restart simulations. | Exhaustive solver traces/certificates; semantics formalizable. |
| 18 | **O25** | Prove `Gap-MCSP[2^{n^{1/3}},2^{n^{2/3}}]` needs Formula-XOR size `N^{1.01}`, where Formula-XOR is a De Morgan formula with arbitrary parity leaves and size is leaf count, by a measure that fails under the known short-oracle upper bound. | 4/1/5/5/3 | **300** | 4/5/5 | Must be demonstrably nonlocal; ordinary-formula/IP variants do not transfer. | Mechanically test candidate measure against oracle circuits; large formal burden. |
| 19 | **O15** | For `k=floor(n^{1/10})` and `G~G(n,n^{-4/(k-1)})`, prove that for some absolute `c>0`, `Pr[L_Res(Clique_k(G))>=n^{ck}]=1-o(1)`. | 4/2/3/4/3 | **288** | 3/5/3 | Upgrade Pang's general-Resolution exponent; regular/a-irregular Resolution already reaches the desired scale. | Random small graphs/proof search offer falsification; asymptotic probability formalization hard. |
| 20 | **O10** | Additive-`o(1)`, `2^n/n^{omega(1)}` CAPP for XOR of two size-`n^{2.5+delta}` `THR o THR` circuits. | 4/2/5/3/2 | **240** | 3/5/5 | Extend CTW beyond 2.5; a separate all-size/closure theorem would be needed for a Williams consequence. | Symbolic error/runtime audit; direct finite evidence weak. |
| 21 | **O24** | For the universal constant `mu>0` in the STACS 2021 magnification theorem, prove `MCSP[2^{mu n}]` is not in `DTIME_1[N^{1.01}]` in its one-way-read-only-input/two-way-work-tape model. | 4/1/5/4/3 | **240** | 5/5/5 | Crossing sequences/information transfer must work at the small magnifying threshold; the known near-quadratic randomized bound is for `mu>1/2`. | Enumerate small machines to falsify invariants; crossing-sequence statements can be formalized. |
| 22 | **O11** | Prove monotone circuit size `2^{Omega(n)}` for bipartite perfect matching on `n+n` vertices. | 3/2/3/4/3 | **216** | 3/5/3 | Must strengthen matching-sunflower/approximation methods; remains monotone only. | Small cover LPs/synthesis; formal combinatorics possible. |
| 23 | **O12** | Prove majority outside nonuniform `ACC^0`. | 5/1/5/4/2 | **200** | 5/5/5 | Mixed moduli defeat direct Razborov--Smolensky transfer; naturalness/algebrization audits important. | Small torus/polynomial experiments are weak; formalization only after a lemma. |
| 24 | **O16** | Resolve weak automatizability of Resolution, equivalently feasible interpolation for `Res(2)`. | 5/1/5/4/2 | **200** | 5/5/5 | Two-decade central proof-complexity problem; strong automatization hardness does not settle it. | Finite candidates can be falsified, but existential target has little direct finite leverage. |
| 25 | **O20** | Prove `NEXP` is not contained in nonuniform polynomial-size `THR o THR`. | 5/1/5/2/2 | **100** | 5/5/5 | Requires all-polynomial-size CAPP/SAT reach with closure or a new nonalgorithmic method; naturalness/locality concerns are severe. | Direct finite evidence is non-diagnostic; formalization starts only after a concrete structural lemma. |

### Frozen model notes for repository-defined targets

For **O02**, `CP_2` means Cutting Planes in which every variable coefficient
in every line has absolute value at most two (the constant term is not so
bounded).  `Sp_CP2` is the maximum number of inequalities simultaneously on
the blackboard.  This is the convention of Galesi--Pudlak--Thapen.

For **O13**, put `b=log_2 M`, identify assignments with `[M]^N`, and let
`Good_f(P)` mean that the blocks indexed by `P` have neither equal values nor
an `f`-collision.  Fix `0<epsilon<1`, use the paper's power-of-two rounding
of `M=N^{2-epsilon}`, and fix `f:[M]^3->[M]` such that
`CBPHP_{3,f}^{N,M}` is unsatisfiable and
`|{y:(h_1,h_2,h_3,y) in Sym_f}|<=(log M)^3` for every fixed triple
`(h_1,h_2,h_3)`.  Let

`S<=2^{(log N)^{3/2}}`, `R=(log S+log N)^2`, `W=R+1`, and
`alpha_N=2(3W)^4(log M)^3/M`.

At one parity-DAG layer take at most `S` affine systems `L_j` of rank at most
`R`.  With `C_j=Cl(L_j)`, for every collision-free full block assignment
`rho` on `C_j` define the nonempty cell

`Phi_j^rho=Sol(L_j) intersect {gamma: gamma|_{C_j}=rho}`.

If `L_j` is split by its one affine query `ell_j`, set
`P_j=Cl(L_j union {ell_j=0})=Cl(L_j union {ell_j=1})` and
`Psi_j^rho=Phi_j^rho intersect Good_f(P_j)`; otherwise set
`Psi_j^rho=Phi_j^rho`.  For `U=union Phi_j^rho` and
`U'=union Psi_j^rho`, O13 asks whether a constant `c=c(epsilon)>0` satisfies

`|U|>=M^N/3  ==>  |U'|>=(1-alpha_N^c)|U|`,

where `c` does not depend on `N` or `S`.

This exact repair was formulated in this repository.  It is **OPEN AFTER
SEARCH, low-medium confidence, potentially false, and not novelty-audited**.
It assumes no overlap or independence beyond the displayed shared collision
predicate.  The unrestricted affine-union conjecture is false and is not an
eligible substitute.  Full definitions and the separate codimension/error
bookkeeping gaps are retained in
[`drafts/proof_sat.md`](drafts/proof_sat.md#ps-4-repair-the-false-affine-robustness-premise).

## 3. Active “already known?” audit

### Circuit and algebraic targets

* **O01:** FLSY prove only
  `Omega(n^2)<=N(n)<=n^{O(log n/log log n)}` and explicitly leave the gap
  open ([ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/)).
  The only exact polynomial claim, TR26-043, is withdrawn and its official
  record says all results rely on a conditional-probability gap
  ([ECCC notice](https://eccc.weizmann.ac.il/report/2026/043/)).  Two
  independent audits found no corrected proof and produced explicit
  counterhistories to two posted lemmas.  **OPEN, high confidence.**
* **O03/O07:** Golovnev--Kulikov state the quadratic-disperser construction
  only as a sufficient hypothesis; Li--Yang and a 2026 follow-up retain
  `3.1n-o(n)` as the full-`B_2` record.  The `5n-o(n)` hit is `U_2` only.
  **OPEN, high confidence.**
* **O08:** Tal's bound remains below cubic by polylogarithms; an ITCS 2024
  primary paper still identifies supercubic explicit-P formulas as open.
  **OPEN, high confidence.**
* **O09/O10/O21:** CTW 2026 improves only the `E^NP` function and only below
  exponent 2.5 for fixed `epsilon`; no P-function gate or wire exponent
  improvement or `2.5+delta` CAPP theorem was found.  Kane--Williams remains
  the explicit-P wire baseline
  ([primary paper](https://arxiv.org/abs/1511.07860)).  The possible `2.5/polylog` implicit
  reparameterization is `UNKNOWN-STATUS` and does not settle these targets.
  **OPEN, high confidence.**
* **O11/O12:** STOC 2026 already gives subexponential monotone matching
  bounds, so the target was tightened to true exponential.  Williams gives a
  high-class language outside ACC, not majority.  **OPEN, high confidence.**

### Proof-complexity and SAT targets

* **O02:** Galesi--Pudlak--Thapen prove `Omega(log log log n)` for every fixed
  `CP_k` and explicitly ask for a better `CP_2` space bound.  Later joint
  length/space and branch-and-cut work uses different resources/models; no
  pure-space improvement was located.  The earlier vague `omega` target was
  replaced by the concrete square in this file.  **OPEN, medium-high
  confidence.**
* **O05:** Buss--Yolcu explicitly ask whether their source-size parameter can
  be removed; no closure was found through the audit date
  ([primary manuscript](https://arxiv.org/abs/2402.15871)).
  **OPEN, high confidence.**
* **O06:** the 2025 synthesis reports only `Omega(sqrt n)` below vertex degree
  six; doubled edges and large vertex degree were explicitly excluded
  ([Theory of Computing 21](https://theoryofcomputing.org/articles/v021a004/v021a004.pdf)).
  **OPEN, high confidence.**
* **O13:** the unrestricted affine conjecture is false.  The candidate uses
  only the actual one-query closure/collision structure and is stated exactly
  in [`drafts/proof_sat.md`](drafts/proof_sat.md#ps-4-repair-the-false-affine-robustness-premise).
  Searches found no theorem or counterexample for this restricted statement.
  **OPEN AFTER SEARCH, low-medium confidence; repository-defined, potentially
  false, and not novelty-audited.**
* **O14/O16:** the proof-complexity handbook and the
  [SAT 2023 merge-resolution account](https://arxiv.org/abs/2304.09422)
  leave restart-free 1-UIP versus Resolution open; Atserias--Bonet's weak-automatizability
  equivalence remains unclosed.  Strong automatization NP-hardness is
  inapplicable.  **OPEN, high confidence.**
* **O15:** Pang proves only `exp(Omega(k^{1-epsilon}))` for general Resolution
  on the random distribution, while the `n^{Omega(k)}` theorem is regular/
  a-irregular or a fresh worst-case construction.  The target freezes one
  allowed random regime.  Sources: [ECCC TR19-068](https://eccc.weizmann.ac.il/report/2019/068/),
  [regular case](https://arxiv.org/abs/2012.09476), and
  [2026 worst case](https://arxiv.org/abs/2601.12503).
  **OPEN, medium-high confidence.**
* **O17/O18:** searches separated deterministic/randomized and general/unique
  3-SAT.  No deterministic base below `1.32793` was found.  The July 2026
  PPSZ number is a preprint claim, and no strict improvement or independent
  validation was located.  **OPEN, medium confidence.**
* **O19:** Tamaki stops at `n^2/log^b n` for sufficiently large fixed `b`.
  Since `exp(sqrt(log log n))=(log n)^{1/sqrt(log log n)}`, O19's denominator
  is unbounded but smaller than every fixed power of `log n`.  Richer PTF
  algorithms use incomparable size/composition regimes
  ([ECCC TR16-100](https://eccc.weizmann.ac.il/report/2016/100/)).  **OPEN,
  high confidence.**

### Meta-complexity targets

* **O04:** the best all-threshold total-MCSP deterministic BP bound is
  `N^2/2^{O(sqrt(log N))}`.  The apparent `Omega(N^2/log^2 N)` closure is for
  MKTP; its authors explicitly explain why Nechiporuk does not transfer to
  MCSP.  Two independent validators rechecked the model.  Sources:
  [ICALP 2019](https://doi.org/10.4230/LIPIcs.ICALP.2019.39) and
  [STACS 2021](https://doi.org/10.4230/LIPIcs.STACS.2021.23).  **OPEN, medium
  confidence.**
* **O20:** Chen's 2018 depth-two threshold paper states that polynomial-size
  `THR o THR` for `NEXP` is consistent with known lower bounds; CTW 2026 still
  proves only each fixed exponent below 2.5 for an `E^NP` function.  No
  superpolynomial result was found
  ([primary preprint](https://arxiv.org/abs/1805.10698)).  **OPEN, high
  confidence.**
* **O22:** Chen--Li--Yang define `B_2` size by gates and explicitly ask for an
  unconditional deterministic `2N-o(N)` MCSP circuit-size lower bound after
  proving a related probabilistic result.  The source's gate convention and
  threshold-function quantifier are frozen above
  ([ECCC TR22-086](https://eccc.weizmann.ac.il/report/2022/086/)).  **OPEN,
  high confidence.**
* **O23:** known sparse-threshold probabilistic-formula bounds are below the
  operative quadratic threshold; the `N^{2+alpha-epsilon}` result uses the
  different threshold `s=N^alpha`, and monotonicity does not transfer it
  ([ECCC TR20-065](https://eccc.weizmann.ac.il/report/2020/065/)).  **OPEN,
  high confidence.**
* **O24:** STACS 2021 supplies the exact one-tape implication for a universal
  small `mu>0`.  Its unconditional near-quadratic randomized lower bounds use
  `mu>1/2`, and its short-oracle analysis blocks a direct parameter transfer;
  no theorem matching the small magnifying `mu` was found
  ([primary source](https://doi.org/10.4230/LIPIcs.STACS.2021.23)).  **OPEN, high
  confidence, but it would already imply `P!=NP` and is only a benchmark.**
* **O25:** ITCS 2020 explicitly leaves Formula-XOR Frontier B unresolved.  Its
  ordinary-formula, interactive-proof, and oracle results are different
  models ([primary source](https://doi.org/10.4230/LIPIcs.ITCS.2020.70)).
  **OPEN, high confidence.**

## 4. Major endpoints, estimated but not ranked as candidates

These OPEN nodes occur in the DAG, so their required estimates are recorded.

| ID | Endpoint | D/H/S | Barrier collision | Prerequisites | Finite/formal outlook |
|---|---|---|---|---|---|
| G01 | P versus NP | 5/5/5 | Relativization, natural proofs, algebrization apply to broad routes. | A genuinely new general lower-bound/algorithmic method. | Direct finite cases are non-diagnostic; formalize only concrete intermediate lemmas. |
| G02 | `NP not subseteq P/poly` / general nonuniform lower bounds | 5/5/5 | Naturalness/algebrization; explicitness and nonuniformity gap. | Algorithms satisfying full Williams interface or another general technique. | No useful direct enumeration; high formal burden. |
| G03 | `VP != VNP` over a fixed characteristic-zero field | 5/5/5 | Algebraic naturalness/PIT issues; restricted rank results do not transfer. | General arithmetic circuit lower bound. | Symbolic small cases weak; formalization only after structural lemmas. |
| G04 | Unrestricted Frege/EF superpolynomial lower bound | 5/5/5 | Interpolation/cryptographic and bounded-arithmetic obstacles; fixed-depth methods do not scale. | New proof-complexity measure for strong systems. | Small proof search cannot establish asymptotics. |
| G05 | Unrestricted dag-like Res(`oplus`) superpolynomial lower bound | 4/5/4 | Lifting/affine geometry must survive arbitrary DAG reuse; F01 blocks one route. | True structured robustness or a different measure. | Finite proof search useful for candidate measures; formalization feasible but large. |
| G06 | General multilinear-ABP separation over a fixed infinite field | 5/5/4 | Current min-partition rank alone is insufficient if O01 holds; general-model gap. | New rank/non-rank measure. | Small ABP synthesis possible but asymptotically weak. |

## 5. Exactly five shortlisted targets

The shortlist is exactly:

1. **O01 — polynomial-size 1-balanced-chain systems.** Fresh, exact, finite,
   and linked to diagnosing the only general multilinear rank method; the
   failed proof supplies concrete falsification work.
2. **O03 — explicit quadratic disperser.** A crisp combinatorial object with
   a proved numerical circuit consequence and strong finite encodings.
3. **O02 — stronger `CP_2` space for `CT_n`.** The smallest direct lower-
   bound increment, though the family is exponentially large and iterated-log
   behavior is invisible experimentally.
4. **O18 — certified PPSZ improvement.** Nearest and most machine-checkable,
   but its connection to stronger lower bounds is weakest.
5. **O05 — strict effective regular-Resolution simulation.** Exact and
   syntactic, but known regular/general separations make the missing parameter
   less locally diagnosable than O01.

## 6. Exactly one first target

**Selected: O01 — polynomial-size 1-balanced-chain systems.**

For every positive even integer `n`, let `N(n)` be the minimum size of a set
system `X subseteq P([n])` such that for every balanced coloring
`f:[n]->{+1,-1}` there is a maximal chain

`emptyset=C_0 subset C_1 subset ... subset C_n=[n]`

inside `X` with `|sum_{x in C_i}f(x)|<=1` for every `i`.  The target is:

> There is an absolute constant `C` such that `N(n)<=n^C` for every even
> `n`.

This is the general existence statement, not “repair TR26-043.”  The next
cycle must begin with a strictly bounded repair-or-obstruction diagnostic for
the withdrawn construction.  A failure of that construction does not refute
O01; a positive O01 result would establish the associated min-partition-rank
limitation, not an mABP separation or P versus NP.

The full unresolved-status audit, comparison, falsification plan, proof
program, and Lean/computational plan are in
[`../audits/first_target_selection.md`](../audits/first_target_selection.md).

**Cycle-2 disposition (2026-08-21).** The bounded diagnostic is complete. It
reached Stop A only for the greedy, uniformly bounded-`d`, single-consumption
cached-frontier process and its posted `1-O(1/M)` logarithmic direct-gap
contract. O01 remains OPEN, and no broader fixed-`d`, `N(n)`, or mABP
obstruction is claimed. See
[`research_cycle_02.md`](../results/research_cycle_02.md).

# Final integration audit: circuits, algebra, barriers, and graph consistency

**Audit date:** 2026-08-13
**Scope:** read-only review of the seven canonical Phase 0/1 artifacts requested
by the integration task.  This file records corrections; it does not modify
the canonical files.

## Corrections required before the cycle is frozen

### 1. O04 mixes threshold-input MCSP with the fixed slice `MCSP[n^2]`

**Affected files:**
[`known_results.md`](../literature/known_results.md) (the unconditional MCSP
branching-program paragraph),
[`dependency_graph.md`](../literature/dependency_graph.md) (K18, O04, and the
K18/K19-to-O04 edge),
[`open_problems.md`](../literature/open_problems.md) (O04 and its knownness
audit), and
[`first_target_selection.md`](first_target_selection.md) (the O04 comparison).

The ICALP 2019 theorem cited for K18 is about MCSP with the threshold supplied
as part of the input.  Its local-PRG framework does not prove the same
near-quadratic bound for the fixed language `MCSP[n^2]`.  In Theorem 13 the
contradiction evaluates the alleged MCSP device at
`C(tt(f), lambda(N,S))`; the threshold is the PRG's local complexity and
depends on the assumed device size `S`.  At the near-quadratic branching-
program scale that threshold is not the fixed value `n^2=(log N)^2`.

Primary evidence: Cheraghchi--Kabanets--Lu--Myrisiotis,
[*Circuit Lower Bounds for MCSP from Local Pseudorandom Generators*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.39/LIPIcs.ICALP.2019.39.pdf),
Definition 12 and Theorem 13, especially the proof's use of
`C(tt(f),lambda(N,S))`.

**Correction:** choose one of the following and propagate it consistently.

1. Change O04 to the threshold-input MCSP problem and ask to improve
   `N^2/2^{O(sqrt(log N))}` to `Omega(N^2/log^C N)`.  Then K18 is the correct
   baseline.
2. Keep the fixed slice `MCSP[n^2]`, but remove K18 as its asserted baseline,
   perform a separate fixed-slice literature audit, and rescore O04's distance
   and confidence.  A lower bound for the full threshold-input problem cannot
   be restricted to a particular threshold in this direction.

The MKTP comparison K19 remains valid only as a comparison, not a reduction.

### 2. The O01-to-G06 arrow has the wrong polarity

**Affected file:**
[`dependency_graph.md`](../literature/dependency_graph.md), overview edge
`O01 -> G06` and ledger row `O01,K21 -> G06`.

O01 would yield a polynomial-size mABP computing a full min-partition-rank
polynomial.  This diagnoses a limitation of full min-partition rank; it does
not establish or strengthen the endpoint `mVBP != mVP`.  The ledger text says
this correctly, but the directed edge and the combined overview label for G06
say the opposite.  This also conflicts with Section 5 of
[`first_target_selection.md`](first_target_selection.md), which explicitly
says that O01 would not prove an mABP lower bound.

**Correction:** remove `O01 -> G06`.  If the consequence is to remain in the
DAG, create a separate typed known-implication/method-limitation node, for
example “O01 implies polynomial-size full-rank mABPs and hence a limitation of
full min-partition rank,” and point O01/K21 to that node.  Keep G06 solely for
the actual general mABP separation.

### 3. Three hardness/randomness edges are not correctly typed

**Affected file:**
[`dependency_graph.md`](../literature/dependency_graph.md), overview edges
from K22 and K23 and ledger rows for those nodes.

* `K22 -> G02` is false under the current labels.  K22 is the conditional
  theorem “exponential circuit hardness in E implies `P=BPP`”; G02 is an
  NP/nonuniform circuit-lower-bound endpoint.  The ledger instead points K22
  to an undefined “derandomization endpoint,” so the overview and ledger also
  disagree.
* K23 proves one **disjunction**: deterministic PIT implies
  `NEXP not subseteq P/poly` **or** a polynomial arithmetic-circuit lower bound
  for permanent.  Drawing independent ordinary arrows `K23 -> G02` and
  `K23 -> G03` asserts each disjunct separately.
* G02 currently conflates `NP not subseteq P/poly` with the different
  `NEXP not subseteq P/poly` disjunct.  The latter does not imply the former.

**Correction:** add a defined derandomization endpoint for K22 (or omit the
edge); split the NP and NEXP circuit endpoints; and represent K23 with an
explicit disjunction/hyperedge node.  Do not replace the disjunction with two
implications.  The prose statement in
[`known_results.md`](../literature/known_results.md) already preserves the
disjunction and can be used as the canonical wording.

### 4. O10 and O19 do not, as stated, feed G02

**Affected file:**
[`dependency_graph.md`](../literature/dependency_graph.md), `O10 -> G02`,
`O19 -> K10`, and the two ledger rows ending at G02.

O10 is a CAPP target for one depth-two threshold class at one polynomial size
exponent.  O19 is a #SAT target only through the near-quadratic gate regime.
Neither exact target supplies the K10 hypothesis of a uniform nontrivial
algorithm for every fixed polynomial size together with the required closure.
The ledger acknowledges these additional obligations, but an edge conditional
on an unrepresented further theorem is not a dependency of the stated O10 or
O19 node.  In particular, neither target by itself proves the general
`NP not subseteq P/poly` endpoint G02.

**Correction:** remove those G02 edges, or insert separate OPEN extension
nodes for all-polynomial-size reach and closure/uniformity, followed by the
proper K10 implication.  A class-specific threshold lower-bound endpoint can
record the direct consequence of O10/O19 without overstating it as a general
P/poly lower bound.

### 5. Algebraic endpoints and O01's consequence need explicit field/nonuniformity qualifications

**Affected files:**
[`dependency_graph.md`](../literature/dependency_graph.md) (G03, G06, K23,
K24, and K21) and
[`first_target_selection.md`](first_target_selection.md), Section 5.

`VP`, `VNP`, permanent completeness, IPS, and multilinear algebraic classes
are field-dependent.  G03 and G06 currently name no field, while the incoming
theorems do not all have a field-free formulation.

For O01 specifically, FLSY Theorem 5.6 gives the n-variate full-rank
polynomial and mABP over **every infinite field** `F`.  Over an arbitrary
field, Theorems 5.4--5.5 first give the construction over the rational-function
extension `F(W_X)`.  The specialization in Theorem 5.6 is existential, and the
paper expressly notes that its construction is nonuniform.  “Over the stated
fields” is therefore too implicit for the file that promises the exact
consequence.

Primary evidence: Fabris--Limaye--Srinivasan--Yehudayoff,
[*Multilinear Algebraic Branching Programs and the Min-Partition Rank Method*](https://eccc.weizmann.ac.il/report/2026/001/),
Theorems 5.4--5.6 and the nonuniformity discussion following Theorem 1.6.

**Correction:** fix a field (for example a characteristic-zero field where
that is the intended VP/VNP endpoint) on G03/G06 and all incoming algebraic
edges.  Replace the selection audit's parenthetical by the explicit
Theorem-5.6 qualification above.  Do not describe the resulting polynomial or
mABP family as uniform or explicit without an additional construction.

### 6. O20 and O24 are not yet concrete mathematical OPEN statements

**Affected files:**
[`open_problems.md`](../literature/open_problems.md) and
[`dependency_graph.md`](../literature/dependency_graph.md).

O20 asks first to “specify” a nonvacuous effective-sparse-language interface.
Before its enumeration, density, constructivity, self-reducibility, and
quantifiers are fixed, there is no single proposition whose OPEN status can
be checked.  Calling the current formulation an OPEN theorem node conflicts
with the file's own admission of formulation risk.

O24 similarly leaves “parameter-preserving reduction” and “the exact
approximate/gap regime” undefined: it does not state the reduction type,
truth-table length blow-up, completeness/soundness or approximation radius,
or the quantifier order on `c,gamma,epsilon`.  ITCS 2020 Theorem 1 has distinct
approximate and worst-case-gap items, and its discussion asks whether the
`MCSP[n^c,2^{n^gamma}]` regime refutes natural proofs; it does not by itself
supply the exact reduction statement now attributed to O24.

Primary evidence: Chen--Hirahara--Oliveira--Pich--Rajgopal--Santhanam,
[*Beyond Natural Proofs: Hardness Magnification and Locality*](https://drops.dagstuhl.de/storage/00lipics/lipics-vol151-itcs2020/LIPIcs.ITCS.2020.70/LIPIcs.ITCS.2020.70.pdf),
Theorem 1 and the subsequent “Towards a more robust theory” discussion.

**Correction:** either (i) classify each as a formulation/UNKNOWN-STATUS
research task until the interface is frozen, or (ii) write the missing
quantifiers and parameter ledger and then rerun the knownness audit.  O24 can
remain the fourth shortlist *direction*, but it should not be called a crisp,
high-confidence OPEN theorem before this repair.

### 7. The declared ranking rule leaves three ties unresolved

**Affected file:**
[`open_problems.md`](../literature/open_problems.md), ranking-method paragraph
and ranked table.

All 25 products are arithmetically correct and the product ordering is
correct.  However, the declared tie-breakers—higher connection, then smaller
distance—still leave these pairs tied:

* O13/O19: product 480, `C=4`, `D=2`;
* O22/O23: product 400, `C=5`, `D=3`; and
* O12/O16: product 200, `C=5`, `D=5`.

The table nevertheless assigns distinct ranks.

**Correction:** add a deterministic tertiary tie-breaker and state it, or use
tied ranks.  This does not change the five-item shortlist.

### 8. The cycle summary says only five targets were ranked

**Affected file:**
[`research_cycle_01.md`](../results/research_cycle_01.md), opening outcome
paragraph.

“Audited 25 intermediate targets; ranked exactly five” contradicts the
25-row ranked table.  Exactly five were *shortlisted*.

**Correction:** replace it with “audited and ranked 25 intermediate targets,
shortlisted exactly five, and selected exactly one.”

### 9. One primary-source title is incorrect

**Affected file:**
[`known_results.md`](../literature/known_results.md), the STACS 2021 MKTP/MCSP
citation.

The linked paper's title is **“One-Tape Turing Machine and Branching Program
Lower Bounds for MCSP,”** not “One-Tape Lower Bounds and the Complexity of
MCSP.”  The theorem statement and URL are otherwise the intended source.

### 10. `Verified results` is too strong for the recorded epistemic status

**Affected file:** [`RESEARCH_STATE.md`](../RESEARCH_STATE.md).

That section includes the affine-union counterexample while immediately
classifying it as `ADVERSARIALLY REVIEWED` and “not formally verified or
novelty-audited.”  The body is appropriately cautious, but the heading can be
read as promoting the result beyond its stated validation level.

**Correction:** rename the section to “Audited cycle findings” (or move the
item to an epistemic-status section) and preserve the existing qualification.

## Checks completed with no correction required

* The ranked table contains exactly 25 distinct IDs O01--O25 and ranks 1--25;
  all score products are correct.
* The shortlist is exactly O01, O03, O02, O24, O18 in both the frontier and
  cycle summary.  O01 alone is selected in the frontier, selection audit,
  research state, and cycle summary.
* The 30 explicit Mermaid arrows over 42 referenced nodes admit a complete
  topological ordering, so the drawn overview is structurally acyclic.  The
  corrections above concern semantic typing, not a directed cycle.
* All 21 local Markdown links in the seven audited canonical files resolve.
  The sole local fragment link,
  `drafts/proof_sat.md#ps-4-repair-the-false-affine-robustness-premise`,
  matches its heading.
* The canonical quantitative circuit statements checked against their
  primary sources—Li--Yang's `3.1n-o(n)` full-`B_2` record, the
  `3.11n` quadratic-disperser implication, CTW's fixed-`epsilon`
  `n^{2.5-epsilon}` threshold lower bound/CAPP theorem, and the 2026 monotone
  matching/clique exponents—need no numerical correction.

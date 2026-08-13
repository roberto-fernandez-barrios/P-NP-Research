# Final integration audit: meta-complexity and hardness magnification

**Audit date:** 2026-08-13
**Scope:** the canonical Phase 0/1 files only.  I checked the integrated
meta-complexity claims against the primary sources and the detailed track
dossier.  I did not edit any canonical file.

## Executive verdict

The high-level map is sound: the repository correctly separates MCSP, MKTP,
and MKtP; correctly treats magnification as parameter- and model-sensitive;
correctly records the locality barrier as a method barrier; and correctly
states that the near-quadratic deterministic branching-program theorem is for
MKTP, not MCSP.  All 25 displayed score products are arithmetically correct,
and the selected O01 consequence is safe once its field and nonuniformity
qualifications are made explicit.

There are, however, **two model errors that should be corrected before the
canonical files are treated as frozen**:

1. O04 mixes the all-threshold language MCSP with the fixed-threshold slice
   `MCSP[n^2]`; the cited lower bound is for the former.
2. O22 calls a `B_2` **gate-size** frontier a wire frontier.  At the exact
   constant `2N`, this is not a harmless convention change.

O20, O21, and O24 are source-motivated research directions but are not yet
fully quantified mathematical statements.  Consequently, the claim that all
25 entries are “precise unresolved increments” is too strong until these
three are frozen.

## 1. Required corrections

### C1 — O04 conflates two different total languages (high priority)

Current canonical statement:

> For total `MCSP[n^2]`, prove deterministic unrestricted BP size
> `Omega(N^2/log^C N)`.

There are two distinct total (non-promise) languages:

* the all-threshold language
  `MCSP = {(x,theta): CC(x) <= theta}`, where `|x|=N=2^n` and the threshold is
  encoded in `O(n)` bits; and
* the fixed-threshold slice
  `MCSP[s] = {x: CC(x) <= s(n)}`.

Cheraghchi--Kabanets--Lu--Myrisiotis Theorem 2 proves

`BPsize(MCSP) >= N^2/2^{O(sqrt(log N))}`

for the **all-threshold** language (and likewise for arbitrary-basis
formulas).  It does not state this bound for every independently chosen slice
`MCSP[s]`.  Their local-PRG framework fixes a threshold tied to the local
complexity when it passes through a parameterized slice; it does not imply the
bound for `s(n)=n^2` merely by notation.  Cheraghchi--Hirahara--Myrisiotis--
Yoshida Theorem 4 likewise states the `Omega(N^2/log^2 N)` result for the
all-threshold language MKTP, although its proof exhibits a particular hard
threshold slice.

**Concrete repair:** choose one of the following, preferably (A).

* **(A) Preserve the known-vs-target comparison:** redefine O04 as
  `BPsize(MCSP) = Omega(N^2/log^C N)` for the all-threshold input
  `(x,theta)`, with BP size equal to the number of nonterminal query nodes and
  `C` one fixed absolute constant.  Input length is `N+O(log N)`, which does
  not alter the displayed asymptotics.
* **(B) Preserve the slice:** keep `MCSP[n^2]`, but remove K18 as a proved
  baseline/edge until a primary theorem for that exact slice is supplied.
  Its open status may still be plausible, but the asserted quantitative gap
  from K18 has not been established.

This affects `literature/open_problems.md` O04 and its status paragraph,
`literature/dependency_graph.md` K18/O04 and edge ledger, and the comparison in
`audits/first_target_selection.md`.

Primary anchors:

* Cheraghchi--Kabanets--Lu--Myrisiotis, ICALP 2019, Theorems 2 and 13:
  https://doi.org/10.4230/LIPIcs.ICALP.2019.39
* Cheraghchi--Hirahara--Myrisiotis--Yoshida, STACS 2021, Definition 9 and
  Theorem 4: https://doi.org/10.4230/LIPIcs.STACS.2021.23

### C2 — O22 is gate complexity, not wire complexity (high priority)

The canonical O22 asks for `2N-o(N)` deterministic fan-in-two **wire** lower
bounds.  Chen--Li--Yang define a `B_2` circuit to have arbitrary fan-in-two
Boolean gates and explicitly define its size as the **number of gates**.
Their `CC^0[2]` and `AC^0[m]` measures use wires, but their general `B_2`
circuit statements do not.  Theorem 1.6 concerns probabilistic `B_2` gate
size, and the immediately following open question asks for an unconditional
`2n-o(n)` circuit-size lower bound for MCSP, even for deterministic circuits.
Translating their input length `n` to this repository's truth-table length
`N` gives a `2N-o(N)` **gate** lower bound.

A constant-factor gate/wire conversion is inadequate here: the leading
constant two is the entire frontier.

**Concrete repair:** replace O22 everywhere by, for example,

> Fix a nondecreasing size function `s` (or simply fix `s(n)=n`) satisfying
> the source's admissible threshold conditions.  Prove that deterministic
> `B_2` circuits deciding `MCSP[s]` require at least `2N-o(N)` gates.

Do not say “for a fixed `n<=s(n)<=...`”: `n` varies.  Say “for a fixed size
function `s` satisfying ...”.  If the intended target is genuinely a wire
bound, it needs a different source-state audit and should not be presented as
the CCC 2022 frontier.

Primary anchor: Chen--Li--Yang, ECCC TR22-086 / CCC 2022, Section 2.2 and
Theorem 1.6:
https://eccc.weizmann.ac.il/report/2022/086/download

### C3 — O20 is an open direction, not yet a theorem statement (medium priority)

Atserias--Muller Theorem 11 says exactly that if there are `epsilon>0` and
`sigma(ell)<=2^{o(ell)}` for which

`n^{-epsilon}-MCSP[sigma] notin P-uniform-SIZE[n^{1+epsilon+o(1)}]`,

then `P != NP^{oplus P}`.  The paper then asks whether one can obtain a
general uniform threshold by placing any `2^{n^{o(1)}}`-sparse problem in the
role of `MCSP[sigma]`.

The canonical target correctly notices that an arbitrary sparse undecidable
set makes an unqualified implication meaningless.  But “specify and prove a
nonvacuous effective-sparse-language interface” does not itself specify the
class, approximation promise, conclusion, or quantifiers.  It is therefore
not yet falsifiable as a mathematical statement.

**Concrete repair:** label O20 `OPEN DIRECTION / STATEMENT TBD`, or choose a
specific effectivity class `E` and state:

* whether `Q` is in P, NP, or `NTIME[2^{n^{o(1)}}]`;
* the exact YES/NO definition of `n^{-epsilon}-Q`;
* the sparsity quantifier;
* P-uniform circuit size and the meaning of the `o(1)` exponent; and
* the exact conclusion.

The audit should also distinguish this proposed **uniform approximate**
theorem from the already-known general nonuniform sparse-problem theorem in
Atserias--Muller Theorem 12.

Primary anchor: Atserias--Muller, arXiv:2503.24061v2, Theorems 11--12 and the
two questions immediately after Theorem 11:
https://arxiv.org/abs/2503.24061

### C4 — O21 uses two informal predicates (medium priority)

The source really does ask for a more constructive Santhanam--Williams proof
that exhibits an explicit hard P problem.  However, canonical O21 leaves
“constructively” and “named natural P problem” undefined and does not specify
the size exponent.  It should be classified as a source-stated research
direction, not as a precise OPEN theorem.

**Concrete repair:** fix a constant `c`, a named language `L in P`, the exact
claim `L notin P-uniform-SIZE[n^c]`, and a checkable definition of the desired
constructivity (for example a uniform counterexample/refuter algorithm).
Alternatively retain the prose but label it `OPEN DIRECTION` and omit a
formal novelty score until it is frozen.

Primary anchor: Atserias--Muller, discussion following Theorem 11,
https://arxiv.org/abs/2503.24061

### C5 — O24 needs the reduction interface and constants frozen (medium priority)

ITCS 2020 explicitly identifies reductions from worst-case
`MCSP[n^c,2^{n^gamma}]` to approximate MCSP as a route toward extending its
non-naturalization theorem.  It also already proves a **conditional**
error-correcting-code reduction for the concrete `1/3,2/3` exponents under
`QP subseteq P/poly` (Lemma 22 and Corollary 23).  Definition 37 gives a
formal `k`-reduction interface: easy functions map to functions of circuit
size at most `s^k`, and hard functions map to functions not
`(1-epsilon)`-approximable by circuits of size `t^{1/k}`.

Canonical O24 does not say whether the new reduction must be unconditional,
does not specify the constants on the target approximate problem, and does
not quantify its output-length/size loss.  “Retaining an `N^{1+epsilon}`
threshold” is a desired outcome, not a formal reduction statement.

**Concrete repair:** formulate O24 using Definition 37 verbatim, require an
unconditional polynomial-time truth-table map, fix `k,c,gamma,epsilon` (and
any output parameters), and state the output truth-table length.  Then append
the symbolic inequality showing that composition preserves one fixed
superlinear exponent.  Until then, label it `OPEN DIRECTION / STATEMENT TBD`.
This matters because O24 is shortlisted at rank four.

Primary anchor: Chen et al., ITCS 2020, Theorem 1, Lemma 22, Corollary 23,
Definition 37, and Proposition 38:
https://doi.org/10.4230/LIPIcs.ITCS.2020.70

### C6 — freeze the O23 and O25 model syntax (low priority)

Their statuses are otherwise supported.

* **O23:** state `d>=1`; a probabilistic formula is a finite distribution over
  De Morgan formulas, correct on every input with probability at least `2/3`;
  size is the maximum **number of leaves** of a formula in the support.  With
  these conventions,
  `MCSP[(log N)^d] notin ProbFormula[N^{2+epsilon}]` is OPEN with high
  confidence and would exceed Chen--Jin--Williams Theorem 1.4's sharp
  quadratic threshold.  Primary source:
  https://eccc.weizmann.ac.il/report/2020/065/download
* **O25:** say that Formula-XOR is a De Morgan formula whose leaves compute
  arbitrary parities, and size counts leaves.  The exact promise has YES
  circuit size at most `2^{n^{1/3}}` and NO circuit size greater than
  `2^{n^{2/3}}`.  ITCS 2020 Theorem 24 gives the safe consequence “either
  `QP notsubseteq P/poly` or `NP notsubseteq NC1`; in particular
  `NQP notsubseteq NC1`.”  Proposition 43's locality upper bound has
  `N^epsilon`-fanin arbitrary oracle gates immediately above XOR leaves.
  O25 is OPEN with high confidence.  Primary source:
  https://doi.org/10.4230/LIPIcs.ITCS.2020.70

### C7 — repair the O01 edge in the overview DAG (medium priority)

The detailed prose states the consequence safely, but the overview edge

`O01 -> G06 [mVBP vs mVP / rank-method diagnosis]`

conflates a method limitation with progress toward a separation.  O01 does
not feed a proof of `mVBP != mVP`; it supplies a small full-rank mABP and hence
blocks full-rankness alone as a lower-bound certificate.

**Concrete repair:** split the node into:

* `B_MPR`: polynomial-size full-rank mABPs / min-partition-rank limitation;
  and
* `G06`: the still-open general mABP separation.

Draw `O01 -> B_MPR` and, if desired, a dashed “forces new methods for” edge
from `B_MPR` to `G06`.  Do not draw an implication/progress edge from O01 to
the separation itself.

## 2. Selected O01 consequence: verified safe form

FLSY Theorem 5.6 gives the exact statement needed.  If `X` is an
`l`-balanced-chain system on an even `n`-element ground set, then for every
**infinite** field `F` there exists an `n`-variate full-rank multilinear
polynomial over `F` computed by an mABP of size at most

`|X| * binom(n, <=l)`.

Consequently, O01 with `l=1` and `|X|<=n^C` yields a nonuniform family of
full-rank polynomials with mABP size `O(n^{C+1})`.  This safely establishes
that the full min-partition-rank property alone cannot certify
superpolynomial general-mABP lower bounds over infinite fields.  The source
has a related construction over a rational-function extension for every
field (Theorem 5.5), but that is not identical to the specialized
`n`-variate statement.

Safe canonical wording:

> If O01 is true, then for every infinite field there is a nonuniform
> polynomial-size mABP family computing full-rank multilinear polynomials.
> Thus full min-partition rank alone cannot prove superpolynomial mABP lower
> bounds over those fields.

The existing exclusions are correct: O01 does not prove an mABP lower bound,
`mVBP=mVP`, `mVBP!=mVP`, a Boolean lower bound, or `P!=NP`.  It also does not
show that every rank-based argument fails.

Primary anchor: FLSY, ECCC TR26-001, Theorems 1.3, 5.5, and 5.6:
https://eccc.weizmann.ac.il/report/2026/001/download/

## 3. Model and notation audit

| Item | Verdict | Exact qualification |
|---|---|---|
| MCSP | PASS with C1 caveat | `MCSP` is the all-threshold `(x,theta)` language; `MCSP[s]` is a fixed-threshold slice.  Both are total, so “total” does not distinguish them. |
| Gap-MCSP | PASS | Promise problem; YES has circuit size `<=s_1`, NO has size `>s_2`.  Behavior in the gap is unrestricted. |
| MKTP | PASS | Random-access `KT(x)=min(|d|+t)`; the program returns each requested bit within `t`.  The near-quadratic BP theorem is for the all-threshold MKTP language. |
| MKtP | PASS | Levin `Kt`, using a whole-string printing program and cost `|p|+ceil(log t)`.  It is the EXP-like problem in the OPS/CJW magnification results. |
| Formula-XOR | PASS after C6 | De Morgan formula with arbitrary parity leaves; size is leaves. |
| Probabilistic formula | PASS after C6 | Distribution over De Morgan formulas; pointwise success at least `2/3`; size is maximum leaf size in the support. |
| `B_2` circuits in CCC 2022 | FAIL in O22 | Arbitrary fan-in-two Boolean gates; size is gates, not wires. |
| P-uniform size | PASS | The map from input length to the circuit description is computable in time polynomial in that input length. |

The canonical distinction among MCSP/MKTP/MKtP is therefore good; the only
substantive notation failure is the all-threshold/slice use in O04.

## 4. O04 and O20--O25 status ledger

| ID | Audited status | Correction/risk |
|---|---|---|
| O04 | OPEN, medium confidence, **after model is fixed** | Prefer all-threshold MCSP.  If `MCSP[n^2]` remains, K18 is not its verified baseline. |
| O20 | SOURCE-STATED OPEN DIRECTION; statement TBD | Must fix effective class and exact uniform approximate implication. |
| O21 | SOURCE-STATED OPEN DIRECTION; informal | Must define constructivity/naturalness and fix exponent/language. |
| O22 | OPEN, high confidence | Replace “wire” by `B_2` gate size and fix a size function `s`. |
| O23 | OPEN, high confidence | Add De Morgan/leaf/pointwise-error conventions and `d>=1`. |
| O24 | SOURCE-STATED OPEN DIRECTION; statement TBD | Require unconditional Definition-37 reduction and freeze all losses. |
| O25 | OPEN, high confidence | Add parity-leaf/leaf-size syntax; consequence and locality scope are otherwise correct. |

No primary source located in the final audit closes the corrected O04, O22,
O23, or O25 statements.  This is a literature-audit conclusion, not a proof
of novelty.

## 5. Known claims and barrier audit

The following integrated claims are supported and need no substantive change:

* total all-threshold MCSP has De Morgan-formula lower bound
  `N^3/2^{O(log^{2/3}N)}` and arbitrary-basis-formula/general-deterministic-BP
  lower bound `N^2/2^{O(sqrt(log N))}`;
* all-threshold MKTP has deterministic BP lower bound
  `Omega(N^2/log^2 N)`, and the source explicitly says the Nechiporuk proof
  does not transfer to MCSP because the circuit-size/KT relation is too
  lossy;
* the same STACS paper's `N^{3/2-o(1)}` MCSP results concern
  nondeterministic, co-nondeterministic, and parity BPs, not unrestricted
  deterministic BPs;
* standard total MCSP and MKTP are in NP, while unconditional ordinary
  NP-completeness remains unproved; conditional, partial, implicit, oracle,
  and randomized-reduction results do not change that status;
* the Oliveira--Santhanam and Oliveira--Pich--Santhanam implications require
  their exact promise gaps, thresholds, models, and “all sufficiently small
  beta” quantifier;
* locality is model-, oracle-fanin-, placement-, number-, and
  adaptivity-sensitive.  It rules out proof methods that survive the relevant
  oracle augmentation, not the target lower bounds;
* the naturalization equivalences are parameter-specific and do not say that
  every MCSP lower bound is a natural proof; and
* locally samplable-distribution Gap-MCSP/OWF equivalences do not imply
  hardness under uniform random truth tables.

The barrier catalogue's language is appropriately cautious.  C1 and C2 are
also good examples of why its restricted-model and parameter-mismatch rules
must be applied to the target table itself.

## 6. Ranking audit

I mechanically recomputed every displayed product.  All 25 are correct:

`1500, 960, 720, 600, 600, 576, 540, 512, 480, 480, 480, 480, 480, 450,
400, 400, 384, 360, 300, 288, 240, 225, 216, 200, 200`.

The top-five list agrees with the displayed ranking.  Two qualifications
remain:

1. The stated tie rule does not fully order O22/O23 (identical five scores and
   identical `D/H/S`) or O12/O16 (also identical).  Add a final stable
   tie-break such as candidate ID, or display tied ranks.
2. O24 is ranked fourth even though its mathematical statement is not frozen.
   Its `F=4` and novelty score should be treated as provisional.  O20 and O21
   have the same, though non-shortlisted, issue.  Re-score after C3--C5.

These corrections do not threaten the selection of O01: its product lead is
large, its statement is exact, and its immediate consequence is now
source-verified.  They do mean that “25 precise unresolved increments” should
be changed to “25 candidate directions” until O20/O21/O24 are formalized.

## 7. Citation completeness

The canonical files give primary citations for the principal known results,
but K30/O20/O21 and the O22/O23 status paragraphs rely too heavily on the
draft dossier.  Add direct canonical citations:

* O20/O21/K30: Atserias--Muller,
  https://arxiv.org/abs/2503.24061 (v2, 2025 preprint);
* O22: Chen--Li--Yang, https://eccc.weizmann.ac.il/report/2022/086/download;
* O23: Chen--Jin--Williams,
  https://eccc.weizmann.ac.il/report/2020/065/download;
* O24/O25: Chen et al., https://doi.org/10.4230/LIPIcs.ITCS.2020.70.

The arXiv title for 2503.24061 is **“Simple general magnification of circuit
lower bounds.”**  Its current public version is v2, revised 2025-06-21, and it
should remain labeled a preprint.

## Final disposition

**Do not alter the selected target.**  O01 remains a defensible first target,
and its consequence is safe in the exact form in Section 2.  Before declaring
the Phase 0/1 state fully frozen, correct C1 and C2, separate the O01 method-
barrier node from the mABP-separation endpoint, and either formalize or
downgrade O20/O21/O24 from precise OPEN statements to open directions.

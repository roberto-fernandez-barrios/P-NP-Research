# Final integration audit: proof complexity and SAT

**Audit date:** 2026-08-13
**Scope:** read-only audit of `literature/known_results.md`,
`literature/barriers.md`, `literature/dependency_graph.md`,
`literature/open_problems.md`, `audits/first_target_selection.md`,
`RESEARCH_STATE.md`, and `results/research_cycle_01.md`, with the linked
proof/SAT dossiers and formal-coverage ledger consulted when a canonical claim
depended on them. No canonical file was edited by this audit.

## 1. Executive verdict

The Phase 0/1 integration is structurally complete, and the selected target is
unambiguous. The proof-complexity and SAT reconstruction is mostly source-
accurate. Before the cycle is committed, however, the canonical files should
receive the following corrections.

1. **High priority -- repair O04's model.** “Total `MCSP[n^2]`” conflates the
   all-threshold total problem with the fixed-threshold slice `MCSP[n^2]`. The
   cited ICALP 2019 branching-program lower bound is for total MCSP, whose input
   includes the threshold. It does not, as cited, give the same baseline for the
   fixed `n^2` slice.
2. **High priority -- do not call O14 an exact OPEN target yet.** No formula
   family or CDCL transition/proof semantics is actually frozen. The global
   restart-free simulation question is open, but the restricted statement in
   the candidate table is not yet a proposition with truth conditions.
3. **High priority -- quantify O19.** `m=n^2/log^{o(1)} n` does not select a
   function or quantify the `o(1)`. Freeze one explicit subpolylogarithmic
   denominator and state Tamaki's exact depth-two mixed-gate model.
4. **Medium priority -- expose O13's epistemic status.** It is a new repository-
   formulated repair, not a source-stated public conjecture. Label it
   `OPEN AFTER SEARCH / NOT NOVELTY-AUDITED` (or conservatively
   `UNKNOWN-STATUS`) and make its exact cells and trims visible in a canonical
   file.
5. **Medium priority -- qualify original counterexamples everywhere.** The
   affine and balanced-chain counterexamples are `UNFORMALIZED` internal
   results that have been independently/adversarially checked within this
   cycle, not externally peer-reviewed theorems. `RESEARCH_STATE.md` partly
   says this for the affine result but not for the balanced-chain result; the
   graph and cycle report use bare `FALSE` wording.
6. **Mechanical -- replace one confirmed 404** for the 2026 hard-clique paper
   with its stable arXiv record.

These repairs do **not** affect the selection of O01.

## 2. Exact-count and consistency checks

### Passed

* `literature/open_problems.md` contains exactly **25** ranked candidate rows,
  with 25 distinct IDs and all IDs `O01` through `O25` present exactly once.
* Ranks are exactly 1 through 25, each used once.
* All 25 displayed five-factor products recompute correctly.
* The shortlist is exactly **five** distinct targets, in order:
  `O01`, `O03`, `O02`, `O24`, `O18`.
* Exactly **one** target is selected: `O01`. Both
  `audits/first_target_selection.md` and the cycle report say that no other
  target was selected.

### Concrete wording corrections

* `results/research_cycle_01.md:11` says “audited 25 intermediate targets;
  ranked exactly five.” The repository actually ranks all 25 and shortlists
  five. Replace this with **“ranked 25 intermediate targets; shortlisted
  exactly five.”**
* `audits/first_target_selection.md:140-148` compares O01 with the four other
  shortlisted targets and also with O04. This is not a numerical violation,
  but label O04 explicitly as **“first target outside the shortlist”** so the
  table cannot be read as a six-item shortlist.

## 3. Proof/SAT known-result precision

### 3.1 Cutting Planes

The quantitative claims behind O02 are correct. Galesi--Pudlak--Thapen define
`CP_k` by requiring every variable coefficient in every proof inequality to
have absolute value at most fixed `k`; this is not a bound on the right-hand
constant. Inequality space is the maximum number of inequalities simultaneously
kept on the blackboard. Their Theorem 6.6 proves
`Sp_CP_k(CT_n)=Omega(log log log n)` for every fixed `k`, and their Problem 3
explicitly asks for a better `CP_2` lower bound. Their Theorem 5.1 gives
space-five `CP_2` refutations of PHP.

Primary source: [Galesi--Pudlak--Thapen, CCC 2015](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2015.433).

Corrections:

* `literature/known_results.md:250-255` should say “every unsatisfiable system
  of integral linear inequalities **over Boolean variables, with the Boolean
  axioms**,” not the potentially broader “every unsatisfiable integral
  system.”
* Define `Sp_CP2` once in `open_problems.md` or spell out the blackboard
  measure. Also state that `CP_2` bounds variable coefficients, not the
  constant term. This prevents collision with other bounded-coefficient CP
  conventions.

### 3.2 Resolution, effective simulation, and automatizability

O05 is source-stated and remains open with high confidence. Buss--Yolcu's
Definition 1.1 uses a transformation `f(Gamma,s)` computable in
`poly(|Gamma|+s)`, equisatisfiable with `Gamma`, such that if `s` upper-bounds
the shortest Resolution proof size, the transformed formula has a regular-
Resolution proof of size `poly(|Gamma|+s)`. Their construction may use proof
height instead of size, and they explicitly ask whether the parameter can be
removed altogether.

Primary source: [Buss--Yolcu, arXiv:2402.15871](https://arxiv.org/abs/2402.15871).

Correction: replace “proof-size/height parameter” by the less ambiguous
**“proof-size parameter (which the current construction can weaken to proof
height)”** at the first full statement of O05.

O16 is also accurate. Atserias--Bonet prove that Resolution is weakly
automatizable iff `Res(2)` has feasible interpolation (and give the analogous
equivalence for constant `Res(k)`, `k>1`). Strong automatizability hardness does
not decide this question.

Primary sources:
[Atserias--Bonet, ECCC TR02-010](https://eccc.weizmann.ac.il/report/2002/010/),
[Atserias--Muller, arXiv:1904.02991](https://arxiv.org/abs/1904.02991).

### 3.3 PCR space

O06 survives the already-known audit. Filmus--Lauria--Miksa--Nordstrom--Vinyals
state that for graphs of vertex degree below six the best known Tseitin PCR
monomial-space lower bound is still `Omega(sqrt n)`; random `d`-regular graphs
for fixed `d>=4` attain that bound over any field. Linear space is obtained for
the degree-six **multigraph** created by doubling every expander edge, and the
`Omega(n/log n)` result needs very large constant degree. These do not close a
simple 3- or 4-regular target.

Primary source: [Filmus et al., Theory of Computing 21(4), 2025](https://theoryofcomputing.org/articles/v021a004/v021a004.pdf), especially Theorems 3.2, 3.4, and 3.5 and the subsequent-developments discussion.

Corrections:

* In `literature/open_problems.md:33`, write “3- or 4-regular,” not `3/4`.
* Freeze the actual unsatisfiable formulas. A precise version is:
  **fix a field `F`, an explicit connected simple 4-regular expander family
  `(G_t)`, and odd charge functions `chi_t`; prove
  `Sp_PCR_F(Ts(G_t,chi_t) |- bottom)=Omega(|V(G_t)|^{1/2+epsilon})`.**
* `literature/open_problems.md:93` should say “below **vertex** degree six” to
  avoid confusion with polynomial-calculus proof degree.
* `literature/known_results.md:264` should say “for suitable expander Tseitin
  formulas after two-variable XOR substitution,” rather than sounding as if
  every XOR-substituted Tseitin formula automatically has linear space.

### 3.4 Frege and Res(`oplus`)

Two small precision repairs are advisable.

* `literature/known_results.md:247` should quantify `AC^0[p]`-Frege for a
  **fixed prime `p`**, which is the convention in the cited literature.
* `literature/known_results.md:271-273` begins “Exponential size lower bounds
  are known for tree-like, regular, and bounded/nearly-quadratic-depth
  restrictions.” This can be read as claiming exponential bounds throughout
  the nearly-quadratic regime. Separate the claims. ECCC TR26-018 proves the
  depth tradeoff `depth=Omega(w^2/log S)`, a pure `Omega(w^2)` unrestricted
  size bound, and a **superpolynomial** consequence for a stated
  `o(n^2/log^4 n)` depth regime. Tree-like/regular exponential bounds should
  be stated independently. Primary source:
  [ECCC TR26-018](https://eccc.weizmann.ac.il/report/2026/018/).

### 3.5 Randomized SAT wording

`literature/known_results.md:133-135` calls Schoning's bound an “expected”
decision runtime. The clean model statement is a randomized one-sided-error
Monte Carlo `k`-SAT algorithm in `O^*((2-2/k)^n)` time; alternatively, expected
time applies to finding a witness on satisfiable inputs. It should not sound
like a Las Vegas decision algorithm that certifies UNSAT in that expected time.

## 4. Open-status audit for O02, O05, O06, O13--O19

| ID | Audit verdict | Exact issue or surviving statement |
|---|---|---|
| O02 | **OPEN, medium-high confidence** | Source Problem 3 asks for a better `CP_2` space bound; no later pure inequality-space improvement was located. The concrete square is safely beyond the known iterated-log bound. Define the model as in section 3.1. |
| O05 | **OPEN, high confidence** | The source explicitly asks to remove size/height access. No closure was located through the audit date. Use the exact effective-simulation quantifiers above. |
| O06 | **OPEN, high confidence after formulation repair** | No `Omega(n^{1/2+epsilon})` result was found for a fixed simple low-degree expander Tseitin family. Add the graph family, charge, field, and formula encoding. |
| O13 | **OPEN AFTER SEARCH, low-medium confidence; not novelty-audited** | This exact structured statement was created in this repository, so it is not a source-stated public open problem. A negative search found no equivalent theorem/counterexample, but that is not a novelty audit. Prefer `UNKNOWN-STATUS` in the typed DAG until the statement is canonicalized. |
| O14 | **FORMULATION NEEDED / UNKNOWN-STATUS as written** | The global no-restart CDCL-vs-Resolution problem remains open, including in the 2023 merge-resolution account. But “on a frozen bounded-width/incidence family” names neither a family nor a CDCL proof system. Freeze trail states, propagation/conflict rules, nondeterministic branching, 1-UIP learning, clause retention/deletion, restart prohibition, proof-size measure, and the formula family before assigning OPEN. Primary current source: [Vinyals et al., SAT 2023](https://arxiv.org/abs/2304.09422). |
| O15 | **OPEN, medium-high confidence** | Pang proves only `exp(Omega(k^{1-epsilon}))` for general Resolution on the random distribution and `n^{Omega(k)}` for `a`-irregular Resolution. The 2026 `n^{Omega(k)}` result is worst-case/explicit, not Pang's average case. |
| O16 | **OPEN, high confidence** | The Atserias--Bonet equivalence is correct and no unconditional decision was located. |
| O17 | **OPEN, medium confidence** | Targeted current-record searches found no deterministic general-3-SAT base below Liu's. State the benchmark as `O^*(1.32793^n)` (or the source's `2^{o(n)}`-suppressed convention), on `n` variables, to avoid a false exact-Big-O comparison. |
| O18 | **OPEN only in its strict-improvement part** | Jiang--Cai v1 (12 July 2026) claims worst-case randomized general-3-SAT time `O^*(1.307031578^n)`, via the existing unique-to-general lift and exact rational intervals. Re-running the certificate is validation, not an open theorem or novelty. Keep one candidate by explicitly making successful replication a prerequisite and a strict certified base improvement the OPEN deliverable. |
| O19 | **Plausibly OPEN, but not exact as written** | Tamaki handles depth-two unbounded-fan-in circuits in which each gate is either symmetric or linear threshold, with `m` total gates, and obtains deterministic #SAT time `2^{n-Omega((n/(sqrt(m) poly(log n)))^a)}`. The expression `log^{o(1)} n` needs an explicit positive function and quantifier. |

### Exact O13 cell structure that should be canonicalized

The linked draft gives the application-supplied structure as follows. For
`C_j=Cl(L_j)` and each collision-free full bit assignment `rho` on every block
of `C_j`, the nonempty cell is

`Phi_j^rho = Sol(L_j) intersect {gamma : gamma restricted to C_j = rho}`.

If node `j` is split by one affine query `ell_j`, then the two child closures
coincide,

`P_j = Cl(L_j union {ell_j=0}) = Cl(L_j union {ell_j=1})`,

and the actual trimmed cell is

`Psi_j^rho = Phi_j^rho intersect Good_f(P_j)`.

For an unsplit node, `Psi_j^rho=Phi_j^rho`. Thus every deletion comes from the
same hereditary collision-free predicate evaluated on the one-query closure;
no overlap or independence property is supplied by the application. This is
the weakest explicit extra structure currently justified.

The canonical graph is right to retain U03: the printed binary-codimension
identification and the stronger `delta_N^c` bookkeeping are **UNKNOWN / ERROR
IN ARGUMENT**, not a refutation of every correctly stated conditional theorem.
O13 should be described only as one potentially sufficient ingredient, subject
to the separate high-rank and parameter ledger.

### Exact O15 formulation

To remove “block-clique distribution” ambiguity, write the target as: for
`k=floor(n^{1/10})`, `G` sampled from
`G(n,n^{-4/(k-1)})`, prove that for some absolute `c>0`,

`Pr_G[L_Res(Clique_k(G)) >= n^{c k}] = 1-o(1)`.

This is inside Pang's `k=n^{c_0}`, `0<c_0<1/3`, `xi>1` regime. Primary source:
[Pang, ECCC TR19-068](https://eccc.weizmann.ac.il/report/2019/068/).
The distinct 2026 worst-case result is
[Hard Clique Formulas for Resolution, arXiv:2601.12503](https://arxiv.org/abs/2601.12503).

### Exact O19 repair

A simple frozen target beyond every fixed-polylog denominator is:

> For depth-two unbounded-fan-in circuits on `n` variables in which every gate
> is either an arbitrary symmetric gate or a linear threshold gate, with at
> most `m(n)=n^2/exp(sqrt(log log n))` gates in total, give deterministic #SAT
> time `2^n/n^{omega(1)}`.

Here `exp(sqrt(log log n))=(log n)^{1/sqrt(log log n)}` is unbounded but
subpolylogarithmic, so this is genuinely beyond Tamaki's fixed-`b` theorem.
Primary source: [Tamaki, ECCC TR16-100](https://eccc.weizmann.ac.il/report/2016/100/).

Do not use the linked draft's suggested
`m=n^2/exp(O(sqrt(log n)))` as an initial advance: for every fixed `b`, that
gate count is eventually `O(n^2/log^b n)` and is already inside Tamaki's
theorem.

## 5. Cross-track model error: O04

This is outside the assigned proof/SAT IDs but is a material integration error.

`literature/open_problems.md:38` and
`literature/dependency_graph.md:101` say “total `MCSP[n^2]`.” These are two
different conventions:

* **total/all-threshold MCSP:** input is `(tt(f),theta)` and asks whether the
  circuit complexity of `f` is at most `theta`;
* **fixed slice `MCSP[s]`:** input is only `tt(f)` and the threshold is the
  external function `s(n)`.

Cheraghchi--Kabanets--Lu--Myrisiotis Theorem 2 proves the
`N^2/2^{O(sqrt(log N))}` BP lower bound for the first problem. In their proof,
the threshold is fixed to the local complexity `lambda(N,S)` of the PRG, which
depends on the hypothesized device size. That argument does not establish the
same lower bound for the fixed `s(n)=n^2` slice.

Primary source: [ICALP 2019 paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.39/LIPIcs.ICALP.2019.39.pdf), Theorems 2 and 13.

Concrete repair: either

1. remove `[n^2]` and make O04 an improvement for the standard all-threshold
   total MCSP function, preserving the cited baseline; or
2. retain fixed `MCSP[n^2]`, remove the asserted K18 dependency, and first
   establish/cite a fixed-slice baseline.

The first option is the minimal correction. The `Omega(N^2/log^2 N)` theorem
for MKTP remains comparison only and does not transfer.

## 6. Counterexample epistemics

The object-level mathematics and the evidence level should be visible at every
canonical summary point.

### Affine-union counterexample

Current best repository status is:

* exact parametric proof written down;
* finite coordinate instances checked computationally;
* a blinded independent derivation and adversarial audit performed by separate
  agents in this cycle;
* **UNFORMALIZED**, not externally peer reviewed, and not novelty-audited.

`RESEARCH_STATE.md:18-21` records most of this correctly. Add the same short
qualification to F01 in the dependency graph and to the “false as written”
sentence in the cycle report. “Two independently derived constructions” should
say **“two independently derived internal constructions”** so it cannot be
mistaken for external validation.

### Balanced-chain counterhistory

The official withdrawal establishes that the conditional forced-probability
step was not proved. The exact `n=10` history and the additional Lemma 3.3
failure are internal results supported by exact arithmetic and a script. Add to
`RESEARCH_STATE.md:22-24`, F02/F03 in the dependency graph, and the cycle report:

> `ADVERSARIALLY REVIEWED WITHIN THIS CYCLE; UNFORMALIZED; not an external
> publication claim.`

The bare heading `RESEARCH_STATE.md:12` “Verified results” is too strong for a
section mixing literature synthesis with unformalized original
counterexamples. Rename it **“Audited results and completed state artifacts”**
or split source-verified results from internally checked claims.

Object-level `FALSE` may remain in the typed graph if the adjacent evidence
status is supplied. The official withdrawal and both counterhistories refute
the attempted construction only; all canonical files correctly leave O01
OPEN.

## 7. Link audit

I extracted 66 distinct external HTTP(S) targets from the seven canonical
files and resolved all local relative-file targets. The O13 heading anchor in
`drafts/proof_sat.md` exists.

### Confirmed broken

* `literature/open_problems.md:111` returns HTTP 404:
  `https://www.cs.upc.edu/~atserias/papers/hard-clique-formulas-for-resolution/clique.pdf`.
  Replace it with the primary stable record
  `https://arxiv.org/abs/2601.12503`.

### Reachability uncertain, stable replacements available

* `literature/open_problems.md:91`, the Yolcu author-hosted PDF, timed out in
  the audit. This is not evidence that it is dead. Prefer the stable primary
  arXiv record `https://arxiv.org/abs/2402.15871`.
* `literature/known_results.md:75`, the CJTCS PDF, failed the command-line TLS
  check but remained indexed and retrievable by the browser. Prefer the DOI
  `https://doi.org/10.4086/cjtcs.1999.007` or Allender's author copy if robust
  link-checking matters.

Publisher DOI endpoints that returned 403 to an automated HEAD request were
not classified as broken; this is common anti-bot behavior. The two DOI URLs
containing balanced parentheses in `known_results.md` are valid CommonMark link
destinations and require no syntax repair.

## 8. Formal-coverage ledger

`formal/coverage.md` correctly says that neither internal counterexample is
formally verified. One row uses `NOT A FORMAL THEOREM`, which is outside the
four formal-status labels mandated by `INITIAL_RESEARCH_MISSION.md`. Since the
dependency DAG and ranking are indeed not theorems, move that row to a short
“non-theorem artifacts” subsection rather than treating the phrase as a fifth
formalization status. No current theorem should be upgraded above
`UNFORMALIZED`.

## 9. Minimal pre-commit correction checklist

1. Repair O04's total-versus-fixed-threshold model.
2. Relabel/formulate O14 and freeze O19 as above.
3. Mark O13 as repository-defined and not novelty-audited; expose its exact
   `Phi/Psi` structure canonically.
4. Add the O06 charge/formula/field details and disambiguate graph degree.
5. Tighten the Schoning, CP, Frege, and Res(`oplus`) model wording.
6. Qualify both internal counterexamples at every high-level occurrence.
7. Replace the one confirmed 404 and, optionally, the two fragile links.
8. Change “ranked exactly five” to “ranked 25; shortlisted exactly five.”

After these repairs, the proof/SAT portion supports the Phase 0/1 conclusion:
25 ranked candidates, exactly five shortlisted targets, exactly one selected
target, and no attempted proof of P versus NP.

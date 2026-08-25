# Research Cycle 6: frontier reassessment and next-target selection

**Cycle date:** 2026-08-25
**Branch:** `cycle06-fable` (provisional; `master` and `cycle05-fable` untouched)
**Cycle type:** reassessment, not a proof cycle
**Status of this cycle:** **PROVISIONAL** — produced while the Cycle-5
theorems (A/E/SEG/C/F) await independent cross-model validation; nothing
below depends on any of them
**Primary outcome:** ranked reassessment of five candidates; exactly one
recommended next target: **O18 (certified PPSZ improvement)**

## 0. Executive conclusion

Five candidates were compared independently against the ten mandated
questions, with literature status re-verified against primary sources on
2026-08-25 and with bounded exploratory experiments where they could
change the decision.

Final ranking (best next target first):

1. **O18** — verify the Jiang–Cai exact-rational PPSZ certificate and add
   one valid inequality/statistic giving a certified randomized general
   3-SAT base strictly below `1.307031578`.  **SELECTED.**
2. **Cycle-3 all-defect-router obligation (DR-POLY)** — held in reserve.
   This cycle's new finite data and two small lemmas show it is a
   *strengthening* of O01, not a smaller sub-lemma: `DR-POLY` implies
   O01 (modulo the Cycle-3 `DEFECT-LIFT` proof candidate), O01 implies
   its width-4 relaxation, and the exact minimum router sizes strictly
   exceed `N(n)` at every computed size.
3. **O05** — Buss–Yolcu strict effective simulation.  A material status
   change was found during reassessment: published supercritical
   size–depth trade-offs (STOC 2025) block the canonical
   flatten-then-translate route.  Recorded; not selected.
4. **O03** — explicit `(n,1.83n,2^{o(n)})` quadratic disperser.  The
   entropy gap between the state of the art (`(1-c)n`) and the target
   (`o(n)`) is far larger than the Phase-1 triage assumed.
5. **O02** — `CP_2` inequality space for `CT_n`.  No experimental grip
   at any reachable scale; unchanged literature status; worst fit.

The selection is a deliberate diversification away from O01-adjacent
work while Cycle 5 awaits cross-model validation.  O01 remains **OPEN**
and unclaimed; no proof program was started in this cycle.

## 1. Ground rules and validation state

* **Cycle-5 quarantine.**  Theorems A, E, C, F and Lemma SEG are treated
  as `PENDING INDEPENDENT CROSS-MODEL VALIDATION` throughout.  No
  argument, score, or experiment in this cycle uses them.  The Cycle-5
  *stop disposition* (RR-family unions retired as the primary O01 route)
  is used only as a strategic fact about where effort has already gone,
  which holds under either validation outcome: if the obstruction
  theorems are validated the route is closed, and if they fall the route
  needs re-validation before further construction on top of it.
* **Literature verification.**  Every candidate's status was re-checked
  against primary sources on 2026-08-25 (web verification this session;
  previous repository audit 2026-08-21).  Negative searches cannot prove
  novelty or exhaustiveness; confidence levels are stated per candidate.
* **Bounded experiments.**  One experiment family was run (defect
  routers, Section 2), chosen because its outcome could change the
  ranking.  All code is standard-library Python, deterministic, and
  committed; results are single-implementation and labelled
  PROVISIONAL (cross-validated against previously audited balanced-side
  values where possible, but not independently adversarially reviewed in
  this cycle).
* **No promotions.**  No claim in this cycle is promoted beyond
  `PROOF CANDIDATE`/`PROVISIONAL`; no novelty claims are made.

## 2. Candidate A — the Cycle-3 all-defect-router obligation (DR-POLY)

### 2.1 Exact open statement

From `research_cycle_03/cp_s_recursion_attack.md` Section 5 (repository-
defined; frozen there and restated here exactly).

For even `n`, a **one-sided 2-defect router** is a family
`D subseteq P([n])` such that

* for every coloring `f:[n]->{+1,-1}` with total `+2`, `D` contains a
  maximal chain all of whose prefix imbalances lie in `[0,2]`; and
* for every coloring with total `-2`, a maximal chain with prefix
  imbalances in `[-2,0]`.

Let `R(n)` be the minimum size of such a `D`.

> **DR-POLY (OPEN, repository-defined).**  There is an absolute constant
> `c` with `R(n) <= n^c` for every even `n`.

The Cycle-3 obligation as recorded was "a non-escalating,
polynomial-state all-defect routing/compression lemma."  Clarification
established in Cycle 3 Section 5.3 and re-verified here: for the O01
recursion itself, per-`n` 2-defect routers suffice (`DEFECT-LIFT` only
ever consumes a 2-defect router at each step); defect escalation to
`4,6,...` arises only if one insists on building `D_{n+2}` *from* `D_n`
by the same lift.  DR-POLY quantifies over arbitrary constructions.

### 2.2 Literature status

Repository-defined object.  The Cycle-1–5 literature sweeps for
balanced-chain systems, band-restricted lattice-path covers, and the
common-interval/switching literature found no external match for
"band `[0,2]` chain covers of total-`+2` colorings"; the FLSY paper
(CCC 2026, LIPIcs 383 Art. 22 / ECCC TR26-001) studies only the balanced
band `[-1,1]`.  Status: `PRIOR-ART-NOT-FOUND (bounded search); NOT
NOVELTY-AUDITED`.  O01 context re-verified 2026-08-25: TR26-043 remains
flawed with no v3/successor (the ECCC record's revision #1 of 2026-05-11
concedes the forced-probability bound fails conditionally on the
filtration; the arXiv record is withdrawn); web search results that
repeat its April abstract as a "resolution" of the FLSY open problem are
stale and were discounted.

### 2.3 Strongest known bounds (including this cycle's data)

Exact values and brackets computed this cycle
(`experiments/cycle06_defect_router_exact.py`,
`experiments/cycle06_router_ub_deep.py`; single implementation;
`certificates/cycle06_router/`):

| `n` | `N(n)` (known) | `L(n)` (known) | `sum_k rho(n,k)` (exact LB) | `R(n)` |
|---:|---:|---:|---:|---|
| 2 | 3 | 3 | 3 | **3** (exact) |
| 4 | 6 | 6 | 7 | **7** (exact) |
| 6 | 12 | 12 | 15 | **15** (exact) |
| 8 | 20 | 19 | 24 | in `[24, 26]` |
| 10 | 35 | 33 | 41 | in `[41, 50]` |

`rho(n,k)` is the exact per-level compatibility-cover minimum for the
router band (branch-and-bound set cover with the same canonical-first
symmetry argument as Cycle 3 Section 3.1); the exact vectors are

```
rho(4)  = 1,2,1,2,1
rho(6)  = 1,3,2,3,2,3,1
rho(8)  = 1,4,2,4,2,4,2,4,1
rho(10) = 1,5,3,6,3,5,3,6,3,5,1
```

Upper witnesses are literal families verified on both the `+2` and `-2`
sides by an independent reachability pass.  Calibration: the same search
machinery, run on the balanced problem, reproduces the audited values
`N(4)=6`, `N(6)=12`, `tau(8)=(1,1,4,2,3,2,4,1,1)` with `L(8)=19`
exactly, and reaches 23 (not the known optimum 20) at `n=8` — so the
`R(8)`, `R(10)` upper ends are search artifacts, not tight.

Upper bound side: `R_{[-1,3]}(n) <= N(n+2) <= (n+2)^{O(log n/log log n)}`
by Lemma W4-RESTRICT below plus FLSY; no quasi-polynomial upper bound is
currently known for the width-2 quantity `R(n)` itself.

### 2.4 Small self-contained results proved and machine-checked this cycle

All four lemmas are elementary; they are recorded because they fix the
router problem's exact relationship to O01.  Status of each:
`PROVED (elementary); MACHINE-CROSS-CHECKED (finite); UNFORMALIZED;
PROVISIONAL (single-cycle, no independent adversarial review yet)`.

**Lemma R-SYM.**  A family satisfies the `-2`-side router condition iff
it satisfies the `+2`-side condition, with the same chains.
*Proof.*  For any coloring `f` and subset `S`, `d_{-f}(S) = -d_f(S)`,
and negation bijects total-`+2` with total-`-2` colorings; a chain has
prefix imbalances in `[-2,0]` under `-f` iff in `[0,2]` under `f`.
(Checked exhaustively for all orderings and colorings at `n=4,6`;
sampled at `n=8`.)  Hence `R(n)` is computed from the `+2` side alone.

**Lemma R-PARITY.**  For a total-`+2` coloring, a maximal chain has all
prefix imbalances in `[0,2]` iff every odd prefix has imbalance exactly
`1` and every even prefix has imbalance in `{0,2}`, iff the consecutive
ordered pairs `(pi_{2i-1}, pi_{2i})` follow the two-state walk: at state
`0` the pair is `(+,-)` (stay) or `(+,+)` (to state `2`); at state `2`
the pair is `(-,+)` (stay) or `(-,-)` (to state `0`); the walk starts at
`0` and ends at `2`.
*Proof.*  Prefix imbalance has the parity of prefix length; odd values
in `[0,2]` reduce to `{1}`, even to `{0,2}`; reading two steps at a time
gives the walk.  (Same finite checks.)
This is the router analogue of the Cycle-3 consecutive-pair
characterization, with one structural difference that measures the extra
cost: at state `0` only the *ordered* pair `(+,-)` is allowed where the
balanced problem allows both orders, and monochromatic pairs are legal
exactly at the state flips.

**Lemma R-DUAL.**  For a total-`+2` coloring, `d_P([n] \ S) = 2 - d_P(S)`,
so complementation preserves the band `[0,2]`; reversing and
complementing a band chain gives a band chain, and
`rho(n,k) = rho(n,n-k)`.  (Machine-confirmed for all computed vectors.)

**Lemma W4-RESTRICT.**  If `X` is 1-balanced-chain on `n+2` points and
`a,b` are two fixed points, then `X|ab = { S \ {a,b} : S in X }` has at
most `|X|` members and contains, for every total-`+2` coloring of the
remaining `n` points, a maximal chain with prefix imbalances in
`[-1,3]` (dually `[-3,1]` for `-2`).  Hence, defining `R_[a,b]` for
general bands, `R_{[-1,3]}(n) <= N(n+2)`.
*Proof.*  Extend the coloring by `f(a)=f(b)=-1` (total `0`); take a
1-balanced chain for the extension; delete `a,b` from every set; the two
duplicate steps collapse, leaving a maximal chain on `[n]`, and each
prefix imbalance equals the extension's imbalance plus
`|C_j cap {a,b}| in {0,1,2}`, hence lies in `[-1,1] + {0,1,2}`.
(Machine-checked by restricting verified balanced families on 6 and 8
points: `experiments/cycle06_band4_restrict_check.py`, PASS.)

**Observation DR2O01 (conditional).**  Granting the Cycle-3
`DEFECT-LIFT` proof candidate, `N(n+2) <= N(n) + R(n) + 2`; hence if
`R(n) <= n^c` for all even `n` then
`N(n) <= 3 + sum_{even k < n}(k^c + 2) = O(n^{c+1})`, i.e.
**DR-POLY implies O01**.  Status: `PROOF CANDIDATE (elementary summation
over the Cycle-3 lemma, which is itself PROOF CANDIDATE; PROVISIONAL)`.
Together with W4-RESTRICT: **the entire gap between DR-POLY and O01 is
band narrowing from width 4 to width 2.**  The Cycle-3 `DEFECT-LIFT`
lemma itself was re-checked finitely this cycle with optimal
ingredients: `|X_4|=6`, `|D_4|=7` lift to a verified 1-balanced-chain
family of exactly `6+7+2=15` subsets on six points.

### 2.5 Smallest plausible missing lemma

A *band-narrowing lemma*: convert width-4 band chains into width-2 band
chains with polynomial state overhead.  By W4-RESTRICT + DR2O01 this is
essentially the whole problem — a proof would give O01 itself (modulo
DEFECT-LIFT).  A weaker genuinely-smaller sub-question does exist:
adapt the FLSY random-walk hierarchy to the `[0,2]` band and decide
whether `R(n) <= n^{O(log n/log log n)}` (the width-2 quasi-polynomial
question), which W4-RESTRICT answers only for width 4.

### 2.6 Computational falsification

DR-POLY itself is not finitely falsifiable (an existence claim for all
`n`).  Candidate constructions are cheaply falsifiable with this
cycle's checker; exact `R(n)` is now known through `n=6` and bracketed
through `n=10`; `n=12` would need a Cycle-3-grade bespoke optimizer.

### 2.7 Formalizability

High: the definitions live in the same finite insertion-order framework
already partially formalized in `formal/BalancedChain.lean`; R-SYM,
R-PARITY, R-DUAL, W4-RESTRICT and DEFECT-LIFT are small finite lemmas.

### 2.8 Do Cycles 1–5 materially change its attractiveness?

Yes — downward, decisively, for *selection as the next target*:

1. DR2O01 shows it is a strengthening of O01, not a reduction: choosing
   it means choosing O01 again under another name.
2. The new finite data runs the wrong way for "routers are cheap":
   `R(n) > N(n)` at every computed size (`7>6`, `15>12`, `>=24>20`,
   `>=41>35`), and the lift's per-step cost `R(n)+2` exceeds the actual
   marginal growth `N(n+2)-N(n)` by a factor `~1.5–2.1` throughout
   (`5,9,17,>=26` versus `3,6,8,15`).  Optimal balanced families do not
   decompose as lift-of-router even approximately.
3. Five consecutive cycles attacked O01 and produced exact finite
   values and restricted obstructions, not a construction; the marginal
   value of an immediate sixth O01-adjacent cycle is low.
4. The Cycle-5 obstruction landscape is itself awaiting cross-model
   validation; resuming O01-adjacent work now would either build on
   unvalidated foundations or duplicate that validation.

The positive side of the ledger: the engine's O01-specific capital
(Lean layer, checkers, exact-value machinery) transfers fully, and this
cycle's lemmas make the route's status exact.  That argues for *reserve*
status, not selection.

### 2.9 Known barriers

No classical barrier (finite combinatorial construction target).
Internal barriers: the escalation phenomenon for recursive router
construction (Cycle 3); the band-narrowing gap being equivalent to the
open content of O01; and the Cycle-2 CF-LOGGAP-style tail obstructions
for greedy/cached constructions, which apply to natural router
constructions exactly as to balanced ones.

### 2.10 One concrete first attack (if it were chosen)

Attempt the width-2 quasi-polynomial question: rework the FLSY
hierarchy (returns of a random walk + recursive gap filler +
symmetrization) for the `[0,2]` band, where R-PARITY replaces the
crossing-pair characterization.  Success (`R(n) <= n^{polylog}`) would
put DR-POLY in the same epistemic position as O01; failure would
localize exactly which FLSY step needs the two-sided band.  Supporting
finite work: exact `R(8)` via a Cycle-3-grade optimizer.

### 2.11 Reasons NOT to choose it (actively sought)

All of Section 2.8; plus the anti-continuity mandate for this cycle
(the candidate is the O01 recursion route by another name); plus the
strategic value of having a genuinely independent result track while
O01's obstruction landscape is re-validated.  **Not selected; retained
as the canonical structural route to O01 with its status now exact.**

## 3. Candidate B — O03: explicit quadratic disperser

### 3.1 Exact open statement

Construct a polynomial-time evaluable family `f_n: F_2^n -> F_2` that is
an `(n, 1.83n, 2^{g(n)})`-quadratic disperser for some `g(n) = o(n)`:
`f_n` is non-constant on every `S subseteq F_2^n` with `|S| >= 2^{g(n)}`
expressible as the common zero set of at most `1.83n` polynomials of
degree at most 2 over `F_2`.  (Definition re-verified against the
Golovnev–Kulikov source this session.)  Known consequence (GK, ECCC
TR15-170): such an `f` requires `3.11n` gates over full `B_2`.

### 3.2 Literature status (verified 2026-08-25)

OPEN, high confidence.  GK state the disperser only as a sufficient
hypothesis; existence is easy non-constructively (counting); no explicit
construction with these parameters was found.  Li–Yang `3.1n-o(n)`
(affine dispersers) remains the explicit full-`B_2` record; the 2026
constructive-refuter paper (arXiv:2604.23958) still cites it as the
record.

### 3.3 Strongest known bound toward it

Explicit extractors/dispersers for **degree-2 varieties** exist only at
min-entropy `(1-c)n` for a small constant `c > 0` (Chattopadhyay et al.,
ITCS 2024; ECCC TR23-140 / arXiv:2309.11019), i.e. dispersion only for
varieties of size `>= 2^{(1-c)n}`.  Random low-degree polynomials
extract much better but are non-explicit (ECCC TR24-093).  O03 needs
non-constancy down to size `2^{o(n)}` against up to `1.83n` quadratics.

### 3.4 Smallest plausible missing lemma

An explicit degree-2-variety disperser at min-entropy `(1-c')n` for any
`c'` materially larger than the current constant — still far from
`o(n)`.  No candidate mechanism is on record.

### 3.5–3.7 Falsification, formalizability, cycle delta

Candidate constructions are only weakly testable (dispersion is
asymptotic; enumerating quadratic systems is infeasible beyond toy
sizes, `2^{1+n+binom(n,2)}` polynomials).  Definitions and the GK
implication are formalizable; any eventual proof would be
algebraic-combinatorial of unknown shape.  Cycles 1–5 add nothing that
helps here: the engine's demonstrated strengths (exact finite
certificates, adversarial audits of combinatorial claims) do not bite;
no pseudorandomness capability has been demonstrated.

### 3.8 Known barriers

No classical barrier blocks an explicit construction.  Adjacent
limitation results on gate elimination bound the *consequence* method's
reach, not the disperser.  The operative barrier is distance: the
entropy regime `o(n)` with `1.83n` polynomials is beyond every known
technique, including the 2024 breakthrough line.

### 3.9 One concrete first attack

Reconstruct the GK requirement analysis; determine whether the
ITCS 2024 extractor's entropy bottleneck is structural or optimizable;
attempt a reduction from quadratic-variety dispersion at moderate
entropy to affine dispersion via restriction (quadratics stay quadratic
under affine restriction, so a genuinely new degree-reduction idea is
required — this is the first thing to formalize or refute).

### 3.10 Reasons NOT to choose

The Phase-1 triage (`D/H = 2/4`) underestimated distance: the fresh
audit shows a chasm between `(1-c)n` and `o(n)` entropy.  The numerical
payoff (`3.1n -> 3.11n`) is marginal; the engine has no comparative
advantage; a cycle here would most likely end with a survey and no
falsifiable intermediate.  **Rank 4 of 5.**

## 4. Candidate C — O02: `CP_2` inequality space for `CT_n`

### 4.1 Exact open statement

In the Galesi–Pudlák–Thapen model (`CP_2`: every variable coefficient in
every proof line has absolute value at most 2; the constant term is
unbounded; inequality space = maximum number of inequalities
simultaneously on the blackboard), prove

`Sp_CP2(CT_n) = Omega((log log log n)^2)`

for the complete tree contradiction `CT_n` (which has `2^n` clauses).
The square was frozen in Phase 1 as the smallest decisive increment over
the known bound.

### 4.2 Literature status (verified 2026-08-25)

OPEN, medium-high confidence.  GPT prove `Omega(log log log n)` for
every fixed `CP_k` and explicitly ask for better `CP_2` bounds;
unrestricted CP has space-5 refutations of everything (with exponential
coefficients), and `CP_2` itself refutes PHP in space 5.  The
2020 lifting work (arXiv:2001.02144) concerns joint length/space of
polynomial-coefficient CP, a different resource; no pure-space
improvement was found in the fresh search.

### 4.3–4.7 Bounds, missing lemma, falsification, formalizability, delta

Strongest known: `Omega(log log log n)` (GPT).  The smallest missing
lemma cannot yet be isolated without a full reconstruction of the GPT
argument; the first analytical step of any attack is to locate which
compression step in their extraction produces the innermost logarithm
and whether one level can be avoided.  Computational falsification is
effectively unavailable: `CT_n` is exponential-size, only `n <= 4` is
enumerable, and iterated-logarithm behavior is invisible at any finite
scale (already recorded at Phase 1).  Lean formalization of CP rules and
configurations is feasible; the needed invariant is unknown.  Cycles 1–5
change nothing mathematically and confirm strategically that the
engine's advantage (exact finite falsification) is inert here.

### 4.8 Known barriers

No classical barrier.  Model-internal constraints are severe: any
candidate space invariant must die under unbounded coefficients (space
collapses to 5) and must not apply to PHP (space 5 in `CP_2`), which
kills most naive potential functions in advance.

### 4.9 One concrete first attack

Verbatim reconstruction of the GPT `CT_n` argument; formalize its
invariant; attempt one additional iteration of their slice/game
compression.  Purely analytical; no experimental component exists.

### 4.10 Reasons NOT to choose

Zero experimental grip, tiny significance (`S=3` at Phase 1), no
falsification channel, and the worst capability match of the five.
**Rank 5 of 5.**

## 5. Candidate D — O18: certified PPSZ improvement (SELECTED)

### 5.1 Exact open statement

Two mandatory stages, frozen from `literature/open_problems.md` and
sharpened by this cycle's source reconnaissance:

* **Stage V (validation; explicitly not novelty).**  Independently
  verify the Jiang–Cai claim [JC26]: randomized general 3-SAT in
  `O*(1.307031578^n)` (Unique-3-SAT `O*(1.306969598^n)`) via the
  unchanged PPSZ algorithm, Scheder's regular/irregular estimates, the
  Scheder–Steinberger-style unique-to-general lift, and a final
  linear-programming dual certificate checked in exact rational
  interval arithmetic.
* **Stage I (the open target).**  Add at least one *new, proved* valid
  inequality or structural statistic to the recombination and derive a
  certified randomized general 3-SAT base **strictly below
  `1.307031578`** (equivalently, strictly improve the certified bound,
  wherever the corrected frontier sits after Stage V).

### 5.2 Literature status (verified 2026-08-25)

OPEN, medium confidence (unchanged from the 2026-08-21 audit, now
directly re-verified):

* [JC26] = Jiang–Cai, *A Better Analysis For PPSZ For 3-SAT*,
  arXiv:2607.10697, **v1 only** (2026-07-12, 13 KB source); no v2, no
  errata, no independent validation, and no strictly better bound
  located in any later source.
* Public artifact repository confirmed:
  `github.com/jiangxioabai/A-Better-Analysis-For-PPSZ` containing
  `ppsz_certificate.json` (exact-rational parameters, root brackets,
  certificate version `2026-07-12-rational-v6`),
  `verify_ppsz_constants.py` (Python 3, `fractions.Fraction`, atanh
  series with rational remainder bounds, Taylor tails), and a
  verification transcript.
* Baseline chain (as reported by [JC26]; verbatim re-verification of
  the baselines is part of Stage V): PPSZ (Paturi–Pudlák–Saks–Zane,
  JACM 2005); Hertli (unique bounds hold in general, arXiv:1103.2165);
  Scheder, *PPSZ is better than you think* (arXiv:2207.11071):
  Unique `1.306972377`, general `1.307031594`; [JC26]:
  Unique `1.306969598`, general `1.307031578`.

### 5.3 Strongest known bound

Certified published frontier: Scheder's general-3-SAT bound
(`~1.3070316`).  Claimed frontier: [JC26]'s `1.307031578` (preprint,
unvalidated).  The deterministic record `O(1.32793^n)` (Liu, ICALP 2018)
is a different target (O17) and is not affected.

### 5.4 Smallest plausible missing lemma

Source reconnaissance this session (labelled reconnaissance-level; to be
re-derived verbatim at attack time): [JC26] express both of Scheder's
estimates as affine functions of three normalized statistics of the
critical-clause structure,

`i_0 = |ID_0|/n`, `i_1 = |ID_1|/n`, `tau = |TwoCC|/n`,

and certify `min max{L_reg, L_irr}` over `i_0, i_1, tau >= 0` by an LP
dual with multiplier `lambda = b_1/A`.  The certified optimum sits at
`i_1 = (A - P_reg)/(A + b_1)`, `i_0 = tau = 0`, with strictly positive
slack margins reported on the `i_0` and `tau` dual constraints
(approximately `0.00134` and `0.0139`).  The smallest plausible missing
lemma is therefore **one proved valid linear constraint on
`(i_0, i_1, tau)` that is violated at that optimum** — e.g. a
combinatorial lower bound showing extremal instances cannot concentrate
all weight on indegree-1 variables with no indegree-0 and no TwoCC
variables — or a strictly improved `b_1` coefficient.  Any such
constraint immediately moves the LP value and yields a strictly better
certified base.

### 5.5 Computational falsification

Excellent, in both directions.  Candidate structural inequalities are
falsifiable by enumerating critical-clause-tree/sibling-graph
configurations of small unique-3-SAT instances (exact finite
enumeration — the engine's core competence).  The certificate itself is
machine-checkable end-to-end in exact rationals; a flaw in [JC26] would
be *found*, not suspected.

### 5.6 Formalizability

Best of the five.  The final object is a finite exact-rational
certificate plus LP duality — directly Lean-checkable (rational
arithmetic, series tails with explicit remainder bounds).  The
probabilistic PPSZ semantics would initially remain unformalized
imports, exactly like the FLSY imports in Cycles 4–5, with the same
verbatim-verification discipline.

### 5.7 Do Cycles 1–5 materially change its attractiveness?

Yes — upward, materially.  The skills this target needs are precisely
the ones the engine has demonstrated and hardened over five cycles:
verbatim import verification against primary sources (FLSY, twice),
independent reimplementation of checkers, exact rational/integer
certificate discipline, adversarial review with repaired statements,
and Lean formalization of finite cores.  None of the Cycle-5 quarantined
theorems is involved.  The target is also robust to either outcome of
the pending Cycle-5 validation.

### 5.8 Known barriers

No classical barrier (randomized upper-bound analysis).  Real risks:
(i) [JC26] may be flawed — then Stage V produces a documented flaw and
the target reverts to improving Scheder's certified `1.307031594`, so
the work is not wasted; (ii) the heavy dependency is verbatim
verification of Scheder's estimates (a long, technical analysis) — the
FLSY-import discipline applies but the effort is nontrivial;
(iii) the LP optimum may be genuinely realizable, i.e. no valid
inequality separates it — the falsification-first plan detects this
early and converts the cycle into a realizability map; (iv) parallel
work: the area is six weeks old and the authors may improve their own
bound.

### 5.9 One concrete first attack

1. Mirror and hash-freeze the [JC26] artifacts; run their checker.
2. Write an independent exact-rational checker from
   `ppsz_certificate.json` alone (no code reuse), including independent
   series-tail bounds.
3. Re-derive the recombination LP and its three margin conditions from
   Scheder's published estimates, importing them verbatim with the
   FLSY-grade citation discipline.
4. Falsification-first search for the missing inequality: exhaustively
   enumerate critical-clause structures on small ground sets and map
   the realizable region of `(i_0, i_1, tau)` near the LP optimum
   `(0, i_1^*, 0)`.  If the optimum is approachable by real instances,
   record the obstruction and stop (S-C).
5. If a candidate constraint survives, prove it combinatorially, rerun
   the LP in exact rationals, and produce a new certificate; then run
   the full audit chain (independent reimplementation, adversarial
   review, novelty audit, Lean check of the final certificate).

Stop rules: **S-A** certificate fails → documented flaw (validation
result).  **S-B** Scheder imports cannot be verbatim-verified within
bounded effort → record the boundary, downgrade, stop.  **S-C** no
valid separating inequality after bounded search → realizability map,
stop.  **S-D** strict certified improvement → full validation chain.

### 5.10 Reasons NOT to choose it (actively sought)

* Weakest connection to lower bounds of all five (`C=2` at Phase 1;
  unchanged): a 3-SAT base improvement advances Track D, not the
  lower-bound tracks, and no complexity separation follows.
* The improvement magnitude is microscopic (the [JC26] step itself is
  `1.6e-8` in the general base); the headline value is the *certified
  frontier* and the reusable exact-analysis machinery, not the number.
* Dependence on an unrefereed preprint — mitigated by validation-first
  ordering, and the fallback target (improve over Scheder) survives a
  [JC26] collapse.
* Scheder-import verification may dominate the cycle's budget (stop
  rule S-B bounds this).
* Small but nonzero scoop risk.

None of these outweighs the fit; **selected**, with the mission rule
("smallest unresolved statement revealing a reusable technique; do not
optimize for prestige") applied explicitly.

## 6. Candidate E — O05: strict effective simulation by regular Resolution

### 6.1 Exact open statement

Buss–Yolcu (IPL 2024; arXiv:2402.15871) define: `P` *effectively
simulates* `Q` if there is `f(Gamma, s)`, computable in
`poly(|Gamma| + s)` time, satisfiable iff `Gamma` is, such that whenever
`s` is at least the smallest `Q`-proof size of `Gamma`, `f(Gamma, s)`
has a `P`-proof of size `poly(|Gamma| + s)`.  Their Theorem 3.1: regular
resolution effectively simulates resolution; the construction
`f(Gamma, h)` depends only on the *height* `h` of some resolution
refutation (leveled variables `W[x,j]`, `j in [h-1]`), and if `Gamma`
has a refutation of height `h` and size `s` then `f(Gamma, h)` has a
regular refutation of size at most `6hns`.

> **Question 3.2 (BY, verbatim).**  "Does regular resolution strictly
> effectively simulate resolution?" — i.e. can the parameter be removed,
> with `f(Gamma)` computable in `poly(|Gamma|)` alone and regular size
> polynomial in `|Gamma|` plus the minimum resolution size?

### 6.2 Literature status (verified 2026-08-25)

OPEN, high confidence; no closure found.  New context found during this
reassessment (both papers existed at the Phase-1 audit but had not been
connected to O05 in this repository):

* Göös–Maystre–Risse–Sokolov, *Supercritical Tradeoffs for Monotone
  Circuits* (arXiv:2411.14268, STOC 2025) introduce **bracket
  formulas**: unsatisfiable 3-CNFs with quasipolynomial-size resolution
  refutations such that **every refutation of polynomial depth requires
  exponential size**.
* de Rezende–Fleming–Janett–Nordström–Pang (arXiv:2411.14267,
  STOC 2025) prove *truly* supercritical size–depth trade-offs for
  resolution (bounds in formula size, not just variable count).

### 6.3 Derived observation (new this cycle)

**BY-ROUTE-BLOCK.**  The canonical route to strictness — flatten a
minimal refutation to height `poly(n)` and apply `f(., poly(n))` — is
unavailable: for bracket formulas, the minimum size among
height-`poly(n)` refutations is exponential while the unconstrained
minimum is quasipolynomial, so the `6hns` guarantee of
`f(Gamma, poly(n))` degenerates, and more generally *any* strict
simulation must handle formulas whose small refutations are necessarily
superpolynomially deep.  Depth flattening with polynomial size loss is
itself refuted by the same family.
Status: `DERIVED OBSERVATION FROM PUBLISHED THEOREMS; source parameters
(6hns, height-only dependence, Question 3.2 wording) verified against
the arXiv HTML this session; PROVISIONAL pending a verbatim re-read in
any future attack cycle`.

### 6.4–6.7 Bounds, missing lemma, falsification, formalizability, delta

Strongest known: the parameterized BY theorem itself, plus the classical
exponential regular/general separations (which make plain p-simulation
false and the effective notion necessary).  The smallest plausible
missing lemma now splits: (positive direction) a translation gadget that
compresses necessarily-deep narrow proofs regularly — no known
mechanism, and BY-ROUTE-BLOCK says leveling cannot supply it;
(negative direction) a regular lower bound for every translation in a
delimited syntactic class on bracket-style formulas — heavyweight
lifting machinery, and only closes a class.  Computational falsification
is moderate: candidate translations can be stress-tested on pebbling,
Stone, and small bracket instances by proof search.  Formalizability is
good for syntactic transformations, poor for the lifting route.
Cycles 1–5 delta: the engine's restricted-obstruction craft transfers,
but five cycles of experience say self-defined-class obstructions
accumulate without exporting; and the newly connected supercritical
results lower the positive route's tractability below the Phase-1
estimate.

### 6.8–6.9 Barriers; first attack

The supercritical trade-offs function as a direct internal barrier on
the natural route (Section 6.3); no classical barrier otherwise.  First
attack if chosen: implement bracket formulas at small scale; measure
`f(Gamma,h)` behavior; attempt "no level-monotone variable-leveling
translation is strict" as a delimited negative theorem.

### 6.10 Reasons NOT to choose

The positive direction now requires an unknown gadget against a proven
obstruction pattern; the negative direction needs lifting expertise and
closes only a class; expected outcome of a cycle is another restricted
obstruction — the pattern this reassessment is mandated to break.
**Rank 3 of 5** (the new connection and testbed give it residual value
above O03/O02).

## 7. Comparative ranking

Rescored on the Phase-1 axes (novelty potential, tractability for this
engine, connection, falsifiability, formalizability), with changes from
the 2026-08-13 ledger justified per candidate above.  Scores are triage
judgments, not measurements; the final order also uses the explicit
judgments recorded in the dossiers (as Phase 1 itself did).

| Rank | Candidate | 2026-08-13 product | 2026-08-25 rescore | Direction | Dominant new fact |
|---:|---|---:|---:|---|---|
| 1 | **O18** | 600 (3/4/2/5/5) | **750** (3/5/2/5/5) | up | Public exact-rational artifact chain; LP optimum + slack identified; perfect capability match |
| 2 | **DR-POLY router** | n/a (not in ledger) | **480** (3/2/4/4/5) | — | Implies O01 (DR2O01); `R(n) > N(n)` at every computed size; anti-continuity mandate |
| 3 | **O05** | 576 (4/3/3/4/4) | **384** (4/2/3/4/4) | down | Supercritical size–depth trade-offs block the canonical route (BY-ROUTE-BLOCK) |
| 4 | **O03** | 960 (4/3/4/5/4) | **288** (4/2/3/3/4) | down | Entropy chasm `(1-c)n` vs `o(n)`; falsifiability of the real statement is weak; consequence magnitude marginal |
| 5 | **O02** | 720 (4/3/3/5/4) | **192** (4/2/3/2/4) | down | Confirmed: no experimental channel at any reachable scale |

Note on the large O03/O02 drops: the Phase-1 `F=5` scores rated the
falsifiability of *small finite probes*, not of the actual open
statements at their operative scale; the fresh audit rates the latter.

## 8. Selection

**Selected next target: O18 — certified PPSZ improvement**, exactly one
target, with the two-stage statement of Section 5.1, the first attack of
Section 5.9, and the stop rules S-A–S-D.  The full selection audit,
anti-continuity check, risk register, and falsification/proof/Lean plans
are in [`../audits/cycle06_target_selection.md`](../audits/cycle06_target_selection.md).

The runner-up disposition is explicit: the router obligation remains the
canonical structural route to O01 and should be re-examined *after* the
Cycle-5 cross-model validation resolves, ideally beginning with the
width-2 quasi-polynomial question (Section 2.10).

## 9. Compliance and non-claims

* No result in this cycle depends on Cycle-5 Theorems A/E/C/F or Lemma
  SEG; their statuses are unchanged and remain pending independent
  cross-model validation.
* O01 is not claimed, not resolved, and its public status is unchanged
  (`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`, FLSY; TR26-043
  remains flawed/withdrawn with no successor as of 2026-08-25).
* No long proof program was started; the experiments were bounded and
  decision-relevant; every new lemma above is small, self-contained,
  elementary, and labelled `PROVISIONAL`.
* No novelty is claimed for anything in this cycle; the router finite
  values are repository-internal data.
* The selection was not made to preserve continuity: the chosen target
  shares no objects, techniques, or files with Cycles 1–5's O01 work.

## 10. Artifacts

* `results/research_cycle_06_reassessment.md` (this file)
* `audits/cycle06_target_selection.md`
* `experiments/cycle06_defect_router_exact.py`
* `experiments/cycle06_router_ub_deep.py`
* `experiments/cycle06_band4_restrict_check.py`
* `certificates/cycle06_router/README.md`
* `certificates/cycle06_router/cycle06_router_values.json`
* `certificates/cycle06_router/cycle06_router_values_deep.json`
* `failure_knowledge.jsonl` (entries RC6-DR-01, RC6-O05-01: route-block
  records, not falsifications)
* `RESEARCH_STATE.md` (PROVISIONAL Cycle-6 section, this branch only)

### Primary sources verified this session (2026-08-25)

* Jiang–Cai, arXiv:2607.10697 (v1, 2026-07-12);
  `github.com/jiangxioabai/A-Better-Analysis-For-PPSZ`
* Buss–Yolcu, arXiv:2402.15871 (IPL 2024), Theorem 3.1 / Question 3.2
* Göös–Maystre–Risse–Sokolov, arXiv:2411.14268 (STOC 2025)
* de Rezende–Fleming–Janett–Nordström–Pang, arXiv:2411.14267 (STOC 2025)
* Golovnev–Kulikov, ECCC TR15-170 (quadratic-disperser bridge)
* Chattopadhyay et al., ECCC TR23-140 / arXiv:2309.11019 (ITCS 2024)
* Galesi–Pudlák–Thapen (CP space; author PDF, unchanged)
* ECCC TR26-043 revision record (still flawed, no successor)
* Scheder, arXiv:2207.11071; Hertli, arXiv:1103.2165; Liu, ICALP 2018

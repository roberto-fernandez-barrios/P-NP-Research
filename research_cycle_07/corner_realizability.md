# Theorem CR: the Jiang–Cai LP corner is realizable

**Date:** 2026-08-26.  **Branch:** `cycle07-o18-fable`.
**Status:** PROOF CANDIDATE, **hostilely reviewed — verdict SOUND WITH
REPAIRS** (`audits/cycle07_corner_theorem_review.md`); all repairs
R-A–R-E are applied in this revision (the reviewer independently
replicated all 21 instances, re-derived the case analyses, and
supplied the corrected asymptotic arguments adopted below).  Full
machine verification of every finite claim by two independent
implementations (`experiments/cycle07_corner_family.py` and the
reviewer's `research_cycle_07/checkers/cr_review_independent.py`).
**Context:** Stage I of Cycle 7, executed falsification-first per the
mandate: before hunting for a "missing inequality" excluding the LP
corner `(i_0, i_1, tau) = (0, i_1^*, 0)`,
`i_1^* = (A−P_reg)/(A+b_1) = 0.060043244708778326…`, we tried to prove
the corner realizable.  It is.  Semantics and conventions:
`research_cycle_07/stage1_semantics.md` (in particular TwoCC is
Definition 31's closure-based set, per Stage-V repair R4).

---

## 1. Statement

**Theorem CR.**  There are constants `n_0` and `c > 0` such that for
every `n ≥ n_0` and every integer `0 ≤ m_1 ≤ n/10`, there exists a
3-CNF formula `F_{n,m_1}` on `n` variables such that:

1. `F_{n,m_1}` is uniquely satisfiable, with unique satisfying
   assignment `1^n`;
2. every variable has **exactly one** critical clause in the closure
   `F̃` (Definition 31, either reading of "3-clause": parents of width
   exactly 3 or width ≤ 3) — hence `TwoCC = ∅` and the canonical
   selection is unique (no selection freedom);
3. every canonical critical clause has width exactly 3 with distinct
   negated variables (the Scheder §6 regime; out-degree 2, `2n` arcs);
4. the critical-clause graph has no indegree-0 vertex, exactly `m_1`
   indegree-1 vertices, and the rest of indegree 2 or 3;

so the recombination statistics are exactly

    (i_0, i_1, tau) = (0, m_1/n, 0).

Two variants exist: clauses of width ≤ 3 ("pairs" variant) and clauses
of width exactly 3 throughout ("triples" variant).  **The triples
variant is the primary carrier of the no-go corollary** (repair R-E):
its closure is trivial — `F̃ = F` with ZERO width-≤3 resolvents, so
`TwoCC = ∅` under every reading of Definition 31, including an
iterated-resolution closure.  The pairs variant satisfies `TwoCC = ∅`
under Definition 31's textual one-round reading (both parent-width
conventions, machine-verified), but under a hypothetical iterated
closure its TwoCC becomes all of `V` (reviewer's fixpoint computation);
it is retained because Scheder's own convention is one-round and his
"k-CNF" means clauses of width ≤ k (frozen PDF p. 2, reviewer-pinned),
so width-2 clauses are inside the Theorem-6 instance class.

**Corollary CR-1 (density).**  The closure of the set of realizable
statistics vectors contains the segment `{(0, t, 0) : 0 ≤ t ≤ 1/10}`;
in particular the [JC26] LP optimum `(0, i_1^*, 0)` is a limit of
statistics of uniquely satisfiable instances (at `n = 50` and
`n = 100` the realized `i_1 = 0.06` differs from `i_1^*` by
`4.3·10⁻⁵`; the deviation is at most `1/(2n)` in general).

**Corollary CR-2 (no-go for the missing-inequality route).**  No
constraint `Q(i_0, i_1, tau) ≥ 0` — linear or not — that is valid for
every uniquely satisfiable 3-CNF (under any, hence in particular the
forced, canonical selection) can exclude the corner: `Q(0, m_1/n, 0) ≥ 0`
for all realizable `m_1/n`, and by continuity along the realized
sequence any `Q` excluding a neighborhood of `(0, i_1^*, 0)` is
falsified by `F_{n, round(i_1^* n)}`.  Consequently:

* the [JC26] recombination LP is **exactly optimal** over the statistic
  system `(i_0, i_1, tau)`: its value `γ* = 0.000068779380458836…`
  cannot be improved by adding any valid constraint in these variables;
* any certified improvement of the `1.307031578` frontier within
  Scheder's framework must change the *estimates* or introduce *new
  statistics* with new estimate dependence — not recombine the existing
  three statistics more cleverly.

Note the corner instances are algorithmically easy (they carry massive
auxiliary structure), which is precisely why they block only the
*statistics-level* route: the imported estimates `L_reg`, `L_irr` are
lower bounds valid for all instances, and on the corner family they are
simply very loose.  Realizability of the statistics says nothing about
PPSZ being slow there — and does not need to.

## 2. The construction

Fix `n` and `m_1`.  All indices are mod `n`.  Let

    base = ⌊n/3⌋ + 1,       jmax = ⌊(n−3)/2⌋,
    p_i  = ⌊i·n/m_1⌋            (i = 0,…,m_1−1;  the W-set),
    s_i  = p_i − base           (the special sources),
    δ    = the least d ∈ {2,…,min(⌊n/m_1⌋−2, jmax−base)} such that the
           set {q_i := p_i + d} is disjoint from {p_j} and from {s_j},
           and no q_i is adjacent (±1) to any s_j,
    g(x) = x + base  for x ∉ {s_i},     g(s_i) = q_i.

(Repair R-A: the earlier draft also demanded `{p_i} ∩ {s_i} = ∅`,
which is δ-independent, unnecessary — the reviewer's §3.1 re-derivation
shows the degree count never uses it — and actually false at several
verified sizes, e.g. `n = 50, m_1 = 3`; only the `q`-exclusions above
matter, and they are what the engine enforces.  Repair R-B: existence
of a valid `δ`: each of the three exclusion families forbids, per
wrap of the circle, at most a constant number of residues near
`p_j − p_i − d ≡ base (± 1)`-type coincidences; the reviewer's
corrected counting, machine-scanned over all `26 ≤ n ≤ 1200` and
`1 ≤ m_1 ≤ n/10`, shows a valid `δ` exists for every such pair except
`(n, m_1) = (27, 2)` — so `n_0 = 28` suffices on the scanned range,
with the corrected counting argument covering all larger `n`, and the
engine picks `δ` constructively in every verified case.)

**Critical clauses** (one per variable, width exactly 3):

    C_x = ( x ∨ ¬(x+1) ∨ ¬g(x) ),      x = 0,…,n−1.

The CCG arcs are `x → x+1` and `x → g(x)`.

**Auxiliary all-positive clauses** (the closed-set killers).  Let
`Adj = { {x, x+1}, {x, g(x)} : x }` (the sibling-adjacency pairs).

* pairs variant: all `( a ∨ b )` with `{a,b} ∉ Adj`;
* triples variant: all `( a ∨ b ∨ c )` with `{a,b}, {a,c}, {b,c} ∉ Adj`.

## 3. Proof

### 3.1 Degrees (claim 4)

`f(x) = x+1` is a bijection, contributing exactly one in-arc to every
vertex.  `g` contributes: `0` to each `p_i` (its unique `g`-preimage
under the default map, `s_i`, was redirected; no other source targets
`p_i` since the default `g` is a bijection and `q_j ≠ p_i` by the
choice of `δ`); `2` to each `q_i` (its default preimage `q_i − base`,
which is not special since `q_i − base = s_j` is excluded, plus `s_i`);
`1` to every other vertex.  Hence indegrees: `1` on `W = {p_i}`, `3` on
`W' = {q_i}`, `2` elsewhere; no indegree 0.  Widths: `x+1 ≠ g(x)`
(jumps ≥ base ≥ 2), `x ∉ {x+1, g(x)}`.  ∎

### 3.2 No 2-cycles or triangles; linearly growing girth (repaired, R-C)

Arc steps are `+1`, `+base`, `+(base+δ)`.  A directed cycle's steps sum
to `kn`, `k ≥ 1`; with `j` long steps and `a` unit steps its length is
`L = a + j`.

*No 2-cycles or triangles (`n ≥ 26`).*  For `L ≤ 3`: `j = 0` forces
`L = n`; `j ∈ {1, 2}`: the step sum is at most `2·jmax + 1 ≤ n − 2 < n`
and at least `base > 0`, so it is never `≡ 0 (mod n)`… precisely, for
`j = 1`: `a + jump ≤ 2 + jmax < n`; for `j = 2`: two long steps sum to
a value in `[2·base, 2·jmax] ⊆ [2n/3, n−3]`, plus `a ≤ 1` stays `< n`;
for `j = 3` (the case the earlier draft omitted): three long steps sum
to a value in `[3·base, 3·jmax] = [n+3, (3n−9)/2]`, strictly between
`n` and `2n`, so no triangle of three long steps exists either.  ∎

*Girth.*  The earlier draft claimed `girth ≥ n/3 − 3δ − 3`; the
reviewer REFUTED that bound (first violation `n = 78`; clean
counterexample `n = 200, m_1 = 11, δ = 2`: girth `52 < 57.67`, realized
by an 11-segment chain alternating special jumps with default-step
runs — the paper's own `n = 80` instance has girth `20`, a 5-special
chain, not the draft's predicted 24).  What is true and is used below:

* girth still grows linearly — reviewer-measured `≈ 0.2n–0.3n` on a
  scan to `n = 800`;
* certified replacement bound (reviewer's lemma, adopted):
  **`girth > 17` whenever `n > 96 + 51δ`** — which is what the triples
  variant's independent-triple argument needs (§3.3), with `δ ≤ n/m_1`
  bounded (constant for `m_1 = Θ(n)`);
* the pairs variant's uniqueness proof no longer uses girth at all
  (repair R-D, §3.3).

Machine-measured girths on the verified instances: 5–30.  ∎

### 3.3 Unique satisfiability (claim 1)

`1^n` satisfies every clause (each critical clause contains its
positive head; auxiliary clauses are all-positive).  Let `β ≠ 1^n`
satisfy `F` and let `S = {x : β(x) = 0} ≠ ∅`.

* If `|S| = 1`, say `S = {x}`: the clause `C_x` has `x = 0`,
  `x+1 = g(x) = 1`, so all three literals are false.  Contradiction.
* If `|S| ≥ 2`: every `x ∈ S` must satisfy `C_x` through `¬(x+1)` or
  `¬g(x)`, i.e. has an out-neighbor in `S` ("S is closed").  Following
  out-neighbors inside the finite set `S` yields a directed cycle
  contained in `S`.
  - pairs variant (repaired, R-D — girth-free and covering all
    `n ≥ 26`): if `S` contains any non-adjacent pair `{a,b}`, the
    clause `(a ∨ b)` is falsified, so `S` must be a clique of the
    adjacency graph `Adj` (edges `{x, x+1}` and `{x, g(x)}`).  **`Adj`
    is triangle-free for this construction** (reviewer's case analysis,
    machine-confirmed: a triangle would need one of `g(x) = x ± 2`, a
    two-jump sum `≡ ±1 (mod n)` — impossible since two long steps sum
    into `[2·base, 2·jmax] ⊆ [2n/3, n−3]` and `δ ≥ 2` — or
    `g(x) = g(x±1)`, excluded by construction).  Hence the clique `S`
    has `|S| ≤ 2`, so the directed cycle inside `S` is a 2-cycle —
    impossible by §3.2.  Contradiction.
  - triples variant: if `S` contains a pairwise-non-adjacent triple,
    its clause is falsified.  Any `|S| ≥ 3(Δ+1) = 18` vertices of a
    max-degree-5 graph contain an independent triple (greedy: pick,
    delete ≤ 6, repeat; the reviewer notes 13 is the sharp threshold —
    18 is used as the safe bound).  Since a closed `S` contains a
    directed cycle, `|S| ≥ girth > 17` for `n > 96 + 51δ` (§3.2).
    Contradiction.  For the two search-mode triples instances with
    girth 8–9 the asymptotic argument does not apply and uniqueness
    rests on the direct machine check below (as it does, redundantly,
    for every verified instance).  ∎

(For each concrete instance the machine additionally verifies
uniqueness *directly* — a complete DPLL shows `F ∧ (x = 0)` is UNSAT
for every variable `x` — so claim 1 does not rest on this proof for the
verified range.)

### 3.4 The closure adds no critical clause (claim 2)

`F̃` adds resolvents of width ≤ 3 from pairs of clauses of `F`
(Definition 31; under the strict reading only width-3 parents resolve —
a subcase of what follows).  A resolvent is a *critical clause* iff it
has exactly one positive literal.  Cases:

* **aux × aux:** all-positive clauses share no complementary pair — no
  resolvents.
* **critical × aux:** the only complementary pairs use a negative
  `¬u` of a critical clause `C_x = (x ∨ ¬y ∨ ¬z)` (with `u ∈ {y,z}`)
  against a positive `u` of an aux clause `A`.  The resolvent is
  `(x ∨ ¬v) ∪ (A ∖ {u})` where `v` is the other negative of `C_x`.
  Since `A`'s vertex set is pairwise non-adjacent while `x` is adjacent
  to `u` (arc `x → u`), `x ∉ A`; hence the resolvent contains `x` and
  all of `A ∖ {u}` positively — at least two positive literals — unless
  `A ∖ {u} ⊆ {x}`, impossible.  Also the tautology case `v ∈ A` gives
  no clause.  If `|A ∖ {u}| = 1` the resolvent `(x ∨ w ∨ ¬v)` has two
  positives; if 2 (triples), width is 4 unless a literal coincides —
  coincidences are `w = x` (excluded: `w ∈ A` non-adjacent to `u`,
  while `x` is adjacent to `u`; note `x = w` would put `x ∈ A`) or
  `w = v` (tautology).  **No critical resolvent.**
* **critical × critical:** `C_x = (x ∨ ¬(x+1) ∨ ¬g(x))` and `C_u` can
  resolve only via `x`'s positive against `¬x ∈ C_u` (i.e. `u → x`),
  giving `(u ∨ ¬v ∨ ¬(x+1) ∨ ¬g(x))` with `v` = the other negative of
  `C_u` — width 4, hence excluded from `F̃`, unless a coincidence
  reduces the width: `v = x+1` or `v = g(x)` (the *grandparent
  overlap*), or a tautology.  Overlap requires, for an arc `u → x`,
  that the other out-neighbor of `u` be an out-neighbor of `x`.  With
  `out(x) = {x+1, g(x)}`:
  - `u = x−1` (arc via `f`): other neighbor `g(x−1)`; overlap needs
    `g(x−1) ∈ {x+1, g(x)}` — excluded analytically below.
  - `u` with `g(u) = x` (arc via `g`): other neighbor `u+1`; overlap
    needs `u+1 ∈ {x+1, g(x)}`; `u+1 = x+1 ⟺ u = x` (no self-arc);
    `u+1 = g(x)` — excluded analytically below.
  Tautology cases (`v` complementary to a literal) produce no clause.
  **No critical resolvent** (machine-verified exhaustively: V4 computes
  every width-≤3 resolvent of every clause pair and finds, for every
  variable, exactly one critical clause in `F̃`, under both readings).

  The two overlap exclusions deferred to the machine in the earlier
  draft are discharged analytically (reviewer's derivation, adopted —
  repairing the garbled prose):
  - `g(x−1) = x+1` needs a jump of 2 `< base` — impossible;
    `g(x−1) = g(x)` needs, if both defaults, jumps differing by 1
    (impossible); if exactly one of `x−1, x` is special, it forces
    `δ = 1` or `δ = −1` (impossible, `δ ≥ 2`); if both special,
    `q_i = q_j` (impossible, the `q`'s are distinct);
  - `g(u) = x` and `u+1 = g(x)` need two long jumps summing to
    `1 (mod n)`, but two long jumps sum into
    `[2·base, 2·jmax] ⊆ [2n/3, n−3]`, never `≡ ±1 (mod n)`.
  (V6's `ovl = 0` on every instance corroborates.)

Hence every variable has exactly one `F̃`-critical clause: `TwoCC = ∅`,
and there is no canonical-selection freedom.  ∎

### 3.5 Statistics

By 3.1 and 3.4: `ID_0 = J_0 = ∅`, `ID_1 = J_1 = W` (`|W| = m_1`),
`tau = 0`.  ∎

## 4. Why this closes the narrow Stage-I route

The Stage-I plan was: find a valid constraint on `(i_0, i_1, tau)`
strictly violated at the LP optimum, add it to the LP, re-certify a
larger `Γ`.  Validity must hold for all uniquely satisfiable 3-CNFs
(the estimates hold for every instance and every canonical selection;
on the family the selection is forced).  By Theorem CR the point
`(0, m_1/n, 0)` is realized exactly, with `m_1/n → i_1^*`; so every
valid constraint set contains the corner in its closure, and the
re-optimized LP value over any valid constraint set equals `γ*`
(the LP objective `max{L_reg, L_irr}` is continuous, and its inf over
any set whose closure contains the corner is ≤ its value at the corner,
= `γ*`; conversely `Γ ≥ γ*` holds already without new constraints).
This is stop rule **S7-C** (corner realizable → realizability map,
stop the inequality route), with the sharpening that the map is not
merely "no obstruction found" but a constructive exact realization.
The reviewer additionally verified (B6) that constraints jointly using
`n` are equally blocked — the family exists at every `n ≥ n_0` with
statistics converging to the corner — and re-confirmed the LP-side
inputs (objective continuity, corner uniqueness by subdifferential
algebra, and the value argument, which in fact needs only attainment,
not uniqueness).

What survives for future work (recorded, not pursued):

1. improve the imported estimates themselves (Scheder's §7/§8 chains;
   his journal version states the constants are not tight);
2. new statistics: the corner family is clause-rich (Θ(n²)/Θ(n³) aux
   clauses) — statistics sensitive to auxiliary structure (e.g. counts
   of all-positive clauses, occurrence degrees) could separate it, but
   the imported estimates carry no dependence on such statistics, so
   new estimates would have to be proved first;
3. **the concrete candidate new estimate (next-cycle material):** the
   corner family lies in Hertli's "1C-Unique (≤3)-CNF" class
   (arXiv:1311.2513: every variable has at most one critical clause) —
   the exact regime for which Hertli 2014 proves his barrier-breaking
   Unique-3-SAT gain.  A verbatim-imported, coordinate-expressed
   version of a 1C-class estimate is precisely the kind of FOURTH
   affine bound that would be active near the corner (`tau = 0` is the
   1C-ish regime) and could strictly improve the recombination.  This
   is an "add a new estimate" route, explicitly outside the Stage-I
   scope closed by this theorem ("add a valid inequality over the
   existing three statistics"), and it would require importing and
   verifying Hertli-2014's substantially heavier analysis;
4. sparse-instance restrictions: for m = O(n) clauses the construction
   above does not apply as stated (the pairs/triples killers are
   dense); whether the corner is realizable with O(n) clauses is OPEN
   (recorded as a question, with no bearing on the validity claim —
   the analysis quantifies over all instances, dense ones included).

## 5. Machine verification (falsification-first record)

Engine: `experiments/cycle07_corner_family.py`
(SHA-256 `c00ae7235399ce43d61a54eaaf23cd5ffa0c86778b24701aa0f45c9e6f4f8c55`).
Transcript: `research_cycle_07/corner_family_verification_output.txt`
(SHA-256 `eac85d35581b697f625c6454aec7eb397b56732011b1ab02c62f82d19c93017b`).
Dataset: `certificates/cycle07_corner/instances.json`
(SHA-256 `1af8aff15117d948285bf32e82a87a8574195ea5c3266aeb4c1ccb42acac28cd`
— byte-identical to the dataset the hostile review replicated).
Post-review delta disclosure: after the review, the engine received
only the review's own minor doc fixes (docstring accuracy for V1/V6, an
added V5 indegree-range assertion) and was re-run — the reviewed
mathematics is unchanged, all 21 verdicts re-passed, and the dataset
hash is unchanged; the engine/transcript hashes above supersede the
pre-fix values recorded in the review file (which is preserved as a
historical record and not edited).  **21/21 instances PASS**:

* search-assisted construction: pairs at
  `n = 26, 30, 40, 50, 60, 80, 100` with `m_1 = round(i_1^* n)`;
  triples at `n = 60, 80`; breadth cases `i_1 ∈ {0, .04, .12, .24, .32}`
  at `n = 50`;
* explicit (search-free, = §2) construction: pairs at
  `n = 30, 50, 80, 100, 120`; triples at `n = 80, 100`.

Per instance the machine verifies: V1 exactly-one-critical-clause and
width/distinctness; V2 `1^n` satisfies; V3 uniqueness by complete DPLL
(`F ∧ (x=0)` UNSAT for every `x`); V4 the full resolvent closure and
`TwoCC = ∅` under both Definition-31 readings; V5 the exact indegree
profile (`J_0 = 0`, `J_1 = m_1`); V6 girth/2-cycles/overlap counts.

Bugs found and fixed by this discipline during development (recorded in
the honesty ledger): an early all-pairs variant created width-2
critical resolvents (`TwoCC = V`); a DPLL branching bug (branching on
an assigned literal) produced false SAT answers; wide repair windows
created 2-cycles; a `δ`-resonance (`q_i = s_{i+2}`) chained long jumps
into a directed 5-cycle at `n = 80`.  Each was caught by the verifier,
not by inspection.

Errors found by the HOSTILE REVIEW in the asymptotic proof text (all
repaired in this revision; none affected the instances, the engine's
verdicts, or the corollaries): R-A vacuous δ-condition
(`{p_i} ∩ {s_i} = ∅` demanded but false at verified sizes and
unnecessary); R-B incoherent δ-existence counting (corrected;
`n_0 = 28`, sole failure `(27,2)` in `26 ≤ n ≤ 1200`); R-C false girth
bound `≥ n/3 − 3δ − 3` (refuted at `n = 78` onward by special-jump
chains; replaced by the reviewer's certified `girth > 17` for
`n > 96 + 51δ`, with measured linear growth to `n = 800`); R-D the
pairs-uniqueness clique-vs-girth step needed `girth ≥ 7`, false at six
instances (replaced by the sharp triangle-free argument, girth-free,
all `n ≥ 26`); R-E Definition-31 reading sensitivity of the pairs
variant (triples variant promoted to primary carrier).

Independent replication (reviewer): all 21 instances reproduced from
the stored `g`-maps — clause counts, profiles, closure/TwoCC under both
readings, forced selection, girths, and uniqueness by a different
enumerator, including an exhaustive `|S| ≤ 8` sweep (8.66M subsets) at
`n = 30` and a complete closed-clique/cycle analysis; differential
tests of the engine's DPLL and resolvent computation against brute
force (1,350 + 800 cases, zero mismatches); no violated valid
constraint found (B9).  Reviewer artifacts:
`audits/cycle07_corner_theorem_review.md`,
`research_cycle_07/checkers/cr_review_independent.py` (+ outputs),
`cr_review_girth_scan.py`, `cr_review_engine_diff.py`.

## 6. Epistemic status and dependencies

* Theorem CR's proof is self-contained elementary combinatorics plus
  the frozen Definition-31 semantics; it does NOT depend on Cycle-5
  results, on the truth of [JC26], or on Scheder's estimates.
* The no-go corollary CR-2 additionally uses: the LP corner location
  and uniqueness (Stage V, independently proved in
  `lp_reconstruction.md` §5) and the exact value `i_1^*` (two
  independent exact-rational checkers).
* Status labels: construction and finite claims
  `MACHINE-VERIFIED BY TWO INDEPENDENT IMPLEMENTATIONS (21 instances,
  two construction modes, two aux variants, both Definition-31
  readings)`; asymptotic arguments `ADVERSARIALLY REVIEWED — SOUND
  WITH REPAIRS; repairs applied (R-A–R-E)`; CR-2 `ADVERSARIALLY
  REVIEWED (B6 airtight given Stage-V inputs); primary carrier: the
  triples variant`.  UNFORMALIZED (no Lean layer for this cycle's
  combinatorics; candidate for future formalization alongside the
  rational-certificate core).
* Novelty: [JC26] explicitly wrote "We do not assert that this point is
  realized by a formula"; the novelty audit (V-d) found no prior work
  on realizability of PPSZ-recombination statistics.  Final pre-promotion
  search (2026-08-26): the structural CLASS of the family is known —
  Hertli's "1C-Unique (≤3)-CNF" (arXiv:1311.2513), the recognized hard
  regime for PPSZ (tight instances for the full PPSZ analysis are not
  known; Scheder, TR21-069 §1.2: "we do not even fully understand the
  true success probability of PPSZ") — but no prior explicit
  construction with
  prescribed CCG indegree profiles and closure-TwoCC-emptiness, and no
  prior statement of recombination-statistics realizability/optimality,
  was found.  What is claimed as potentially new: the constructions
  with prescribed `(i_0, i_1, tau)` and the exact-optimality no-go for
  the [JC26] recombination; what is NOT claimed: novelty of the 1C
  class itself, or any statement about tightness of the full PPSZ
  analysis (the family is algorithmically easy).

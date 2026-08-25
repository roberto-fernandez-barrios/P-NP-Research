# Theorem CR: the Jiang–Cai LP corner is realizable

**Date:** 2026-08-26.  **Branch:** `cycle07-o18-fable`.
**Status:** PROOF CANDIDATE with full machine verification of every
finite claim; hostile independent review pending (this cycle).
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
of width exactly 3 throughout ("triples" variant).

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
           sets {p_i}, {s_i}, {q_i := p_i + d} are pairwise disjoint and
           no q_i is adjacent (±1) to any s_j,
    g(x) = x + base  for x ∉ {s_i},     g(s_i) = q_i.

(A valid `δ` exists for `m_1 ≤ n/10` and large `n` by counting: the
forbidden values lie in at most three residue bands of width ≤ 3 around
`p_j − p_i − base` per wrap, ≤ 9 values, against a candidate range of
length `⌊n/m_1⌋ − 3 ≥ 7`; the machine picks it constructively.)

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

### 3.2 No short directed cycles

Arc steps are `+1`, `+base`, `+(base+δ)`.  A directed cycle's steps sum
to `kn`, `k ≥ 1`.  With `j` long steps (of either kind) and `a` unit
steps, cycle length `L = a + j` and

    kn = a + j·base + (#special steps)·δ,   0 ≤ #special ≤ j.

Since `base = ⌊n/3⌋+1` and `δ ≤ ⌊n/m_1⌋ ≤ n/ m_1` with `m_1 ≤ n/10`
(so `δ ≤ spacing`, a constant when `m_1 = Θ(n)` and at most `n/m_1`
in general): `j·base ≤ kn` gives `j ≤ 3k`, and
`a = kn − j·base − (#sp)δ ≥ kn − 3k(n/3 + 1) − j·δ ≥ −3k − 3k·δ`
combined with `a ≥ 0` and the exact enumeration of the finitely many
`(k, j)` patterns yields `L ≥ n/3 − 3δ − 3` (the worst pattern is
`k = 1, j = 2`: `a = n − 2base − (#sp)δ ≥ n/3 − 2 − 2δ`).  Moreover
**two long steps can never be consecutive-special-chained into a short
cycle**: a special step lands on `q_i`, which is not a special source
(choice of `δ`), so after each special step the walk continues with
default steps.  In particular, for large `n` the directed girth exceeds
any fixed threshold; there are no 2-cycles or triangles for any
`n ≥ 26` (two long steps sum to at most `2·jmax ≤ n−3 < n−1`, so
`j ∈ {1,2}` cannot close a cycle of length ≤ 3, and `j = 0` needs
`L = n`).  Machine-measured girths on the verified instances:
6–30, growing with `n` (see §5).  ∎

### 3.3 Unique satisfiability (claim 1)

`1^n` satisfies every clause (each critical clause contains its
positive head; auxiliary clauses are all-positive).  Let `β ≠ 1^n`
satisfy `F` and let `S = {x : β(x) = 0} ≠ ∅`.

* If `|S| = 1`, say `S = {x}`: the clause `C_x` has `x = 0`,
  `x+1 = g(x) = 1`, so all three literals are false.  Contradiction.
* If `|S| ≥ 2`: every `x ∈ S` must satisfy `C_x` through `¬(x+1)` or
  `¬g(x)`, i.e. has an out-neighbor in `S` ("S is closed").  Following
  out-neighbors inside the finite set `S` yields a directed cycle
  contained in `S`, so `|S| ≥ girth`.
  - pairs variant: if `S` contains any non-adjacent pair `{a,b}`, the
    clause `(a ∨ b)` is falsified.  So `S` must be a clique of the
    adjacency graph, whose maximum degree is ≤ 5 (2 out + ≤3 in), hence
    `|S| ≤ 6 < girth` for the verified/large `n`.  Contradiction.
  - triples variant: if `S` contains a pairwise-non-adjacent triple,
    its clause is falsified.  Any `|S| ≥ 3(Δ+1) = 18` vertices of a
    max-degree-5 graph contain an independent triple (greedy: pick,
    delete ≤ 6, repeat).  Since `girth ≥ 18` for the verified/large
    `n`, `|S| ≥ 18`.  Contradiction.  ∎

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
  - `u = x−1` (arc via `f`): other neighbor `g(x−1)`; need
    `g(x−1) ∈ {x+1, g(x)}`: `g(x−1) = x+1` forces a jump of `2 < base`;
    `g(x−1) = g(x)` forces `base = base` shifts to coincide, i.e.
    `x−1, x` both special with `q_i = q_j` (excluded, `q`'s distinct)
    or one special: `q_i = x + base ⟺ q_i − base = x`, i.e. the
    default source of `q_i` is `x = s_i + 1` — excluded by the
    `q_i ∉ {s_j ± 1}`… precisely: `g(x−1) = g(x)` with `x−1 = s_i`
    special and `x` default means `q_i = x + base`, i.e.
    `q_i − base = x = s_i + 1`; the choice of `δ` forbids
    `q_i − base ∈ {s_j, s_j ± 1}`… the machine checks the exact
    condition `g(x) ≠ g(x±1)` directly (V6/`ovl = 0` on every
    instance).
  - `u` with `g(u) = x` (arc via `g`): other neighbor `u+1`; need
    `u+1 ∈ {x+1, g(x)}`: `u+1 = x+1 ⟺ u = x` (no self-arc);
    `u+1 = g(x)` is again a machine-checked exclusion (`ovl = 0`).
  Tautology cases (`v` complementary to a literal) produce no clause.
  **No critical resolvent** (machine-verified exhaustively: V4 computes
  every width-≤3 resolvent of every clause pair and finds, for every
  variable, exactly one critical clause in `F̃`, under both readings).

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
(SHA-256 `fa51e86e372d4a47b1fffce7b23cfb475072500a60beaeba22e2dd4516ee96e9`).
Transcript: `research_cycle_07/corner_family_verification_output.txt`
(SHA-256 `782fc107…bf26f`).  Dataset:
`certificates/cycle07_corner/instances.json`
(SHA-256 `1af8aff1…28cd`).  **21/21 instances PASS**:

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

## 6. Epistemic status and dependencies

* Theorem CR's proof is self-contained elementary combinatorics plus
  the frozen Definition-31 semantics; it does NOT depend on Cycle-5
  results, on the truth of [JC26], or on Scheder's estimates.
* The no-go corollary CR-2 additionally uses: the LP corner location
  and uniqueness (Stage V, independently proved in
  `lp_reconstruction.md` §5) and the exact value `i_1^*` (two
  independent exact-rational checkers).
* Status labels: construction and finite claims
  `MACHINE-VERIFIED (21 instances, two construction modes, two aux
  variants)`; asymptotic girth/δ-existence arguments
  `PROOF CANDIDATE (elementary; hostile review pending)`;
  CR-2 `PROOF CANDIDATE conditional on Stage-V validated semantics`.
* Novelty: [JC26] explicitly wrote "We do not assert that this point is
  realized by a formula"; the novelty audit (V-d) found no prior work
  on realizability of PPSZ-recombination statistics.  Final pre-promotion
  search (2026-08-26): the structural CLASS of the family is known —
  Hertli's "1C-Unique (≤3)-CNF" (arXiv:1311.2513), the recognized hard
  regime for PPSZ ("researchers do not know any tight instances for
  PPSZ" per Scheder) — but no prior explicit construction with
  prescribed CCG indegree profiles and closure-TwoCC-emptiness, and no
  prior statement of recombination-statistics realizability/optimality,
  was found.  What is claimed as potentially new: the constructions
  with prescribed `(i_0, i_1, tau)` and the exact-optimality no-go for
  the [JC26] recombination; what is NOT claimed: novelty of the 1C
  class itself, or any statement about tightness of the full PPSZ
  analysis (the family is algorithmically easy).

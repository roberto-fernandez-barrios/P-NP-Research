# Stage I — combinatorial semantics of (i_0, i_1, tau) from first principles

**Date:** 2026-08-25.  **Prerequisite:** Stage-V verdict
JC-SOUND-WITH-REPAIRS (`audits/cycle07_jc_validation.md`); frontier
`1.307031578`; repairs R1–R5 in force — in particular **R4: TwoCC is
Definition 31's closure-based set**.

This document reconstructs, from the frozen sources (not from the LP),
what the recombination coordinates mean, what an "instance" of the
realizability problem is, and the exact question Stage I must answer
before any inequality is conjectured.  All conventions below are pinned
to ECCC TR21-069 rev 1 (frozen, SHA `e4d634c4…`), as imported by [JC26].

## 1. Objects

* **Instance.**  A 3-CNF `F` (clauses of width ≤ 3) on variable set `V`,
  `|V| = n`, uniquely satisfiable, normalized so the unique satisfying
  assignment is all-ones (`α = 1^n`).
* **Critical clause of `x`.**  A clause in which `x` occurs positively
  and every other literal is negative — i.e., under `α`, `x` is the only
  true literal (form `(x ∨ ¬y ∨ ¬z)`, `(x ∨ ¬y)`, or `(x)`).
  Unique satisfiability forces **every variable to own at least one
  critical clause** (flipping `x` alone must falsify some clause, and
  only clauses where `x` is the sole true literal can be falsified by
  that flip).
* **Canonical selection.**  Each variable selects exactly ONE of its
  critical clauses ("we ask x to select one", src p. 7).  The imported
  estimates hold for EVERY selection; the analysis may use the most
  favorable one (see §4).
* **Critical clause graph (CCG).**  For canonical clause
  `(x ∨ ¬y ∨ ¬z)`: arcs `x→y`, `x→z`.  The k = 3 sections of the source
  operate in the regime where every canonical critical clause has width
  exactly 3 ("Each vertex has out-degree 2, giving a total of 2n arcs",
  src p. 20); the width-<3 boundary convention is a pinned-open import
  detail (§6, D1) and Stage-I enumeration restricts to
  width-exactly-3 canonical clauses with `y ≠ z` accordingly.
* **Sibling graph SG.**  Undirected MULTIgraph on `V`; one edge `{y,z}`
  per variable's canonical clause; `|E| = n` with multiplicity;
  `deg_SG(v) = indeg_CCG(v)`.
* **TwoCC (Definition 31 — closure-based; repair R4).**  Let `F̃` be `F`
  plus all 3-clauses inferable from PAIRS of 3-clauses of `F`
  (single resolution round producing width-≤3 resolvents; src example:
  `(x∨¬y∨¬z), (a∨¬x∨¬y) ⊢ (a∨¬y∨¬z)`).  `TwoCC` = variables with at
  least two critical clauses **in `F̃`**.
* **Classes.**  `J_i` = variables of CCG-indegree `i` (all variables);
  `ID_i = J_i \ TwoCC` for `i ∈ {0,1}`.  Coordinates:

      i_0 = |ID_0|/n,   i_1 = |ID_1|/n,   tau = |TwoCC|/n.

* **Degree identity.**  With all canonical clauses width-3:
  `Σ_v indeg(v) = 2n`, so writing `n_k = |J_k|`:
  `Σ_k n_k = n`, `Σ_k k·n_k = 2n`, hence `2n_0 + n_1 = Σ_{k≥3}(k−2)n_k`.
  The corner profile `(i_0, i_1, tau) = (0, 0.0600432…, 0)` is
  degree-feasible, e.g. `n_1 = n_3 = 0.06n`, `n_2 = 0.88n` — **no
  degree-counting obstruction exists**; any obstruction must come from
  unique satisfiability + the closure.

## 2. Unique satisfiability = the closed-set condition

Write `S = zero-set of an assignment β` (`β = 1^n ⟺ S = ∅`).  For a
clause set `F`, `β` satisfies `F` iff:

* every critical-form clause `(x ∨ ¬y ∨ ¬z)` with `x ∈ S` has `y ∈ S`
  or `z ∈ S`;
* every 2-positive clause `(x ∨ y ∨ ¬z)` forbids (`x,y ∈ S`, `z ∉ S`);
* every 3-positive clause `(x ∨ y ∨ z)` forbids `{x,y,z} ⊆ S`;
* (0-positive clauses cannot occur: `α` must satisfy them.)

So: **`F` is uniquely satisfiable iff no nonempty `S ⊆ V` is
"closed"**, where closed means: every `x ∈ S` has an out-neighbor
(in its OWN critical clauses' negative variables — for the canonical
clause, its CCG out-neighbors; for additional critical clauses, theirs)
inside `S`, and no auxiliary (≥2-positive) clause is violated by `S`.

**Proposition S1 (critical-clauses-only formulas are never uniquely
satisfiable, absent unit clauses).**  If every clause of `F` contains at
least one negative literal — in particular if `F` consists solely of
critical-form clauses of width ≥ 2 — then `0^n` satisfies `F`, so `F`
is not uniquely satisfiable with `α = 1^n`.  *Proof.*  Under the
all-zeros assignment every negative literal is true, and each clause
contains one.  ∎  (In the width-exactly-3 canonical regime every
critical clause has two negative literals, so S1 applies.)

**Consequence.**  Every uniquely satisfiable width-3 instance MUST
contain auxiliary clauses with ≥ 2 positive literals, and those must
break every closed set — in particular `S = V`, so at least one
all-positive clause or a chain of 2-positive clauses eliminating `0^n`.
The Stage-I tension is exactly:

> auxiliary clauses are mandatory (to kill closed sets), but auxiliary
> clauses interact with critical clauses in the closure `F̃` and can
> create second critical clauses (TwoCC mass) — and the corner needs
> `tau → 0` AND `i_0 → 0` simultaneously with `i_1 ≈ 0.06 > 0`.

## 3. How second critical clauses arise in the closure

A resolvent of two width-3 clauses has width 3 iff the parents share a
literal besides the resolved pair.  Cases relevant to `F̃`-criticality
(new clause with exactly one positive literal, i.e. a critical clause):

* **critical × critical, overlap:**  `(x∨¬u∨¬y) , (u∨¬y∨¬z) ⊢
  (x∨¬y∨¬z)` — a new critical clause for `x` whenever `x`'s canonical
  clause points to `u` and `u`'s clause shares the other negation `¬y`.
  ("grandparent overlap": `x→u`, both clauses containing `¬y`.)
* **2-positive × critical:**  `(a∨x∨¬u) , (u∨¬y∨¬z)` resolving on `u`
  gives width 4 unless overlap; with overlap `(a∨x∨¬y) , (y∨¬a?…)` —
  resolvents with two positives are non-critical.  A 2-positive parent
  can produce a CRITICAL resolvent only by resolving away one of its
  positives: `(a∨x∨¬u)` resolved on `a` with `(…∨¬a∨…)` needs the other
  parent to contain `¬a`: `(¬a∨¬p∨q)`-type (a critical clause of `q`
  pointing to `a`): `(q∨¬a∨¬p) , (a∨x∨¬u) ⊢ (q∨x∨¬p∨¬u)` width 4
  unless overlap (`p ∈ {x,u}` or …): e.g. `(q∨¬a∨¬u) , (a∨x∨¬u) ⊢
  (q∨x∨¬u)` — TWO positives, not critical.  So 2-positive clauses spawn
  critical resolvents only via multi-step patterns outside one
  resolution round, EXCEPT the case `(q∨¬a∨¬x) , (a∨x∨¬u)`:
  resolve on `a`: `(q∨¬x∨x∨¬u)` tautology; resolve on x?? `x` positive
  in parent 2, `¬x` in parent 1: `(q∨¬a∨a∨¬u)` tautology.  (To be
  exhausted mechanically in the enumeration engine — the engine computes
  `F̃` by brute force, so no case analysis is load-bearing.)
* **Padding trap:**  a width-2 critical clause `(x∨¬y)` subsumes and
  behaves like `(x∨¬y∨¬z)` for every `z`; the width-exactly-3 regime
  avoids this (§1).

## 4. The exact realizability question (selection quantifier pinned)

The imported estimates hold for every canonical selection, so for a
given `F` the analysis gets

    Bound(F) = max over canonical selections sel of Γ(i_0, i_1, tau)(F, sel),

where `Γ` is the LP value function (`Γ ≥ γ*` everywhere; `Γ = γ*`
exactly at the corner `x* = (0, i_1*, 0)`, `i_1* = (A−P_reg)/(A+b_1) =
0.060043…`).  Hence:

* **The corner blocks improvement iff** there exist uniquely
  satisfiable instances (as `n → ∞`) for which EVERY canonical
  selection yields statistics with `Γ(stats) → γ*` — by uniqueness of
  the LP minimizer, equivalently stats(F, sel) → x* for every selection.
* **A candidate missing inequality** need only hold in the weak form:
  "for every uniquely satisfiable `F` there EXISTS a canonical
  selection with `Q(i_0, i_1, tau) ≥ 0`", for some constraint `Q`
  violated at `x*`.  (Proving it for all selections is stronger and
  also acceptable.)

Stage-I data collection must therefore record, per instance `F`:
`d_min(F) = min_sel dist(stats, x*)` and `d_max(F) = max_sel …`, and the
Pareto set of attainable stats vectors; the falsification target is a
family with `d_max(F) → 0` (every selection near the corner), and the
inequality-hunting target is a proved lower bound on quantities like
`α·i_0 + β·tau` (best selection) as a function of `i_1`.

## 5. First structural observations to test (NOT yet conjectures)

Recorded as directions for the falsification-first program; none is
asserted:

* O-A: With `tau = 0` (no closure-TwoCC), auxiliary ≥2-positive clauses
  must break all closed sets; do the auxiliary clauses force
  `Ω(·)`-many... (quantify: how few auxiliary clauses suffice, and do
  they force indegree-0 or TwoCC mass?)  Note `0^n`-breaking needs an
  all-positive clause or 2-positive chains; a single `(u∨v∨w)` clause
  kills all `S ⊇ {u,v,w}` only.
* O-B: grandparent-overlap-freeness (no `x→u` with shared second
  negation) is necessary for `tau = 0` at one resolution round;
  overlap-freeness is a local girth-type condition on the CCG+labels —
  is it compatible with 94% of vertices having indegree ≥ 2 and unique
  satisfiability?
* O-C: the corner's `i_1 ≈ 6%` is NOT structurally special (any
  `i_1 ∈ [0, ~0.94]`-ish is degree-feasible); the LP corner's exact
  `i_1*` is an artifact of the coefficient values.  So a "corner
  exclusion" inequality must exclude a NEIGHBORHOOD, not a point —
  i.e., a genuine constraint surface `Q(i_0, i_1, tau) ≥ 0` with
  `Q(x*) < 0`.

## 6. Pinned-open import details for the enumeration engine

* D1: the source's convention for width-<3 canonical critical clauses
  (assumed width-exactly-3 in §6's out-degree-2 statement; where the
  reduction/justification lives in the source is not yet pinned).
  Engine policy: enumerate in the width-exactly-3 canonical regime;
  separately record instances where some variable's ONLY critical
  clauses have width < 3 (these fall outside the §6 regime and are
  quarantined from conclusions until D1 is pinned).
* D2: whether `y ≠ z` is required in `(x∨¬y∨¬z)` (loops in SG);
  engine policy: require distinct.
* D3: multigraph conventions (parallel SG edges allowed: two variables
  with the same sibling pair) — allowed in the engine, per "counting
  parallel edges by multiplicity".
* D4: `F̃` = ONE resolution round over pairs of 3-clauses of `F`
  producing width-≤3 resolvents (per Definition 31's wording); tautology
  resolvents discarded; the engine computes this by brute force.

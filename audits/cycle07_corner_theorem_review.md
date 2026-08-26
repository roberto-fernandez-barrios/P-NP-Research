# Hostile adversarial review — Theorem CR (corner realizability) and its verification engine

**Reviewer:** independent validator (arms-length; no code or prose reused from the
author's engine).  **Date:** 2026-08-26.
**Reviewed objects (SHA-256 recomputed by me, all match the doc's claims):**

* `research_cycle_07/corner_realizability.md` (Theorem CR + CR-1 + CR-2)
* `research_cycle_07/stage1_semantics.md` (pinned semantics)
* `experiments/cycle07_corner_family.py` = `fa51e86e372d4a47b1fffce7b23cfb475072500a60beaeba22e2dd4516ee96e9`
* `research_cycle_07/corner_family_verification_output.txt` = `782fc107…bf26f`
* `certificates/cycle07_corner/instances.json` = `1af8aff1…28cd`
* frozen source: `scheder_tr21069_rev1.pdf` — pp. 2, 6–8, 19–20 read directly from the PDF.

**My tools (new, written for this review, under `research_cycle_07/checkers/`):**

* `cr_review_independent.py` (+ `cr_review_independent_output.txt`,
  `cr_review_triples_rerun.txt`) — from-scratch re-verification of all 21
  instances: reconstruction from stored `g`, independent indegree profiles,
  independent closure/TwoCC (both Definition-31 readings **and** an
  iterated-closure probe), four independent uniqueness methods (own
  counter-based DPLL model enumerator; closed-set characterization
  differentially validated against direct clause evaluation; complete clique
  enumeration; short-cycle enumeration; exhaustive small-|S| sweeps), own
  girth BFS, max-clique, and a doc-formula reconstruction of `g`.
* `cr_review_girth_scan.py` (+ `_output.txt`) — δ-existence scan over 72,673
  (n, m1) pairs (26 ≤ n ≤ 1200, all m1 ≤ n/10) and girth-vs-claimed-bound scan
  to n = 800.
* `cr_review_engine_diff.py` — differential audit of the engine's `sat_dpll`
  (1,350 queries vs. exhaustive truth tables) and `resolvents` (800
  clause-set/reading comparisons vs. a naive quadratic implementation).

---

## Overall verdict: **SOUND WITH REPAIRS**

The theorem's substance survives a determined attempt to break it.  All 21
machine-verified instances replicate perfectly under independent methods; the
realized statistics `(0, m1/n, 0)` with `TwoCC = ∅` and forced canonical
selection are genuine; the no-go logic of CR-2 is airtight given the Stage-V
LP inputs; and the engine's two load-bearing primitives are bug-free under
differential testing.  **However, three of the four asymptotic proof steps in
the document contain real errors as written** — one of which makes the
document's own construction recipe vacuous at two of its verified sizes
(n = 50, 100) — and one semantics sensitivity deserves a prominent caveat.
Every error is repairable; repairs are specified below and were derived and
machine-checked as part of this review.  No counterexample to the theorem or
the corollary was found.

### Required repairs (all verified feasible by this review)

1. **R-A (§2, δ-condition).**  Delete "`{p_i}`, `{s_i}` … pairwise disjoint"
   from the δ-condition; keep only the `{q_i}`-conditions (Q∩P = ∅, Q∩S = ∅,
   q's not ±1-adjacent to specials), i.e. exactly what the engine enforces.
   As literally written the doc's condition is **unsatisfiable for every δ at
   n = 50, m1 = 3 (P∩S = {16, 33}) and n = 100, m1 = 6 (P∩S = {16, 66})** —
   two of the paper's own verified explicit instances — and at 15,601 of the
   72,673 scanned (n, m1) pairs (21%).  P∩S-disjointness is δ-independent, is
   never used by any verified claim, and my re-derivation of §3.1 confirms it
   is unnecessary.
2. **R-B (§2, δ-existence argument).**  The counting parenthetical is
   incoherent ("≤ 9 forbidden values against a candidate range of length
   … ≥ 7" concludes nothing) and ignores the `jmax − base` cap.  Real failure:
   **(n, m1) = (27, 2) has no valid δ** (the only candidate d = 2 puts
   q + 1 ∈ S).  Scan result: that is the *only* failure for
   26 ≤ n ≤ 1200, m1 ≤ n/10, so `n_0 = 28` suffices empirically.  Corrected
   argument (sketch, checked): P-differences never land in the candidate
   window (consecutive p-gaps ∈ {⌊n/m1⌋, ⌊n/m1⌋+1} > spacing − 2), so the
   forbidden d-values come only from the `s_j − p_i (mod n)` bands ±1 — at
   most one band of ≤ ~5 consecutive values per window of ≥ 7 (m1 ≥ 7) or a
   ≤ 5/spacing density (m1 ≤ 6, window ≈ n/6) — hence a valid δ = O(1)
   exists for all large n.
3. **R-C (§3.2, girth bound).**  The claimed bound `girth ≥ n/3 − 3δ − 3` is
   **false**: violated at **116 of 193 scanned n** (first at n = 78:
   girth 16 < 17.00; clean counterexample **n = 200, m1 = 11, δ = 2:
   girth = 52 < 57.67**, exactly realized by the 11-segment special-jump
   chain I predicted analytically: repeat [special step +69, then 3–4 unit
   steps to the next special source]).  The supporting claim "the worst
   pattern is k = 1, j = 2" is falsified by the paper's own n = 80 instance:
   its measured girth 20 is the k = 2, j = 5 all-special chain
   5 × (special + 3 units), not the k = 1 pattern (which gives 24).  "Special
   steps never chain" is literally true (q_i ∉ S) but toothless: chaining
   after two unit steps (q_i + 2 = s_j) is not excluded and is what produces
   the violations.  The parenthetical no-triangle argument also omits the
   j = 3 all-jump case (closable: 3 jumps ∈ [n+3, 1.5n−4.5] ∌ kn).
   **Replacement (proved here):** (i) no 2-cycles/triangles for n ≥ 26 —
   window arithmetic incl. the j = 3 case; (ii) any directed cycle of length
   L ≤ 17 forces j ≤ 3k − 1 long steps, whence
   L ≥ n/3 − 3k + 1 − s·δ ≥ n/3 − 15 − 17δ > 17 for n > 96 + 51δ; with
   δ = O(1) (R-B) this gives girth ≥ 18 for all large n.  Empirically girth
   grows like ~0.2n–0.3n (scan to n = 800; worst case over all m1 ≤ n/10:
   girth 10 at n = 60 rising to 43 at n = 400).
4. **R-D (§3.3, pairs uniqueness step).**  "max degree ≤ 5, hence
   |S| ≤ 6 < girth for the verified/large n" is **false at six of the
   verified instances** (girth 5–6 ≤ 6: pairs n = 26, 30, 30-explicit, 40,
   50-search, 50-m1=2); there the doc's closed-set argument does not close
   and uniqueness rests on the (sound) DPLL check V3, as the doc itself
   parenthetically concedes.  **Sharp repair (proved and machine-confirmed):**
   the sibling-adjacency graph Adj is **triangle-free** for this construction
   (requires only: jumps ∉ {1, 2}, g(x) ≠ g(x±1), 2-jump sums ∉ {±1 mod n},
   3-jump sums ≢ 0 mod n — all excluded by the jump window and δ ≥ 2), so a
   closed clique has ≤ 2 vertices, and a closed 2-set is a 2-cycle — excluded.
   This proves pairs-variant uniqueness for **all** n ≥ 26 with no girth
   assumption.  Measured max clique = 2 on all 21 instances.  (Triples: the
   18 = 3(Δ+1) threshold is valid but loose — 2(Δ+1)+1 = 13 suffices; the two
   triples-search instances, girth 8 and 9, are below both thresholds and
   rest on V3/my enumerator.)
5. **R-E (Definition-31 reading; prominence, not correctness).**  The pairs
   variant's `TwoCC = ∅` holds under Definition 31's one-round reading (both
   parent-width conventions, machine-verified) but **fails maximally under an
   iterated-resolution closure**: my fixpoint computation gives
   TwoCC = **all** variables (tau = 1.0) at n = 26 (19,201-clause closure) and
   n = 30-explicit (29,755).  The one-round reading is textually correct
   ("pairs of 3-clauses **of F**", and the pinned D4/R4), but the **triples
   variant is robust under every reading** — it has zero width-≤3 resolvents,
   so F̃ = F under one-round, iterated, and even the broadest
   semantic-implication reading of "inferred".  Recommend stating CR/CR-2
   with the triples variant as the primary carrier of the no-go and the pairs
   variant as the width-≤3-class witness.

None of R-A…R-E affects the machine-verified finite claims, the realized
statistics, or the corollaries; they affect the *asymptotic proof text* and
its robustness framing.

---

## Per-item findings

### B1. Semantics fidelity — **CONFIRMED** (with the width-convention question settled)

* **"3-CNF" convention:** PDF p. 2 (read directly): *"If every clause
  contains at most k literals, the formula is called a k-CNF formula."*
  So Scheder's Theorem-6 class is **width ≤ 3**, and the pairs variant
  (width-2 all-positive aux + width-3 critical clauses) **is inside the
  stated theorem class**.  The "exactly 3" reading is *not* the source
  convention.  Had it been, only the triples variant would carry the no-go —
  and the triples variant exists and is verified (n = 60, 80 search;
  n = 80, 100 explicit), so the no-go carries under either convention.
  The residual ambiguity is only in Definition 31's word "3-clauses" for the
  *parents* of the closure; the engine checks both readings (V4), and both
  yield TwoCC = ∅ on all 21 instances (replicated).
* **Critical clause** (PDF p. 7): clause of the form (x ∨ ȳ₂ ∨ … ∨ ȳ_k) —
  exactly one positive literal, owned by its positive variable.  Engine's
  `is_critical` (exactly one positive) matches; the head assignment matches.
* **Canonical selection** (p. 7): "we ask x to select one" — free selection
  among F's critical clauses.  The family has exactly one critical clause per
  variable in F (V1) and in F̃ (V4) — replicated — so the selection is forced;
  the ∃-selection and ∀-selection forms of any candidate constraint coincide
  on this family (this is what makes CR-2 cover stage1 §4's weak form).
* **Definition 31** (p. 19, read from the rendered page; matches the frozen
  extract glyph-for-glyph): F̃ = F plus all 3-clauses inferable from pairs of
  3-clauses **of F** — a single round.  Engine implements one round of
  resolution, width-≤3 non-tautological resolvents, both parent readings.
  Two conservative-direction notes: (i) the engine admits width-≤2 resolvents
  into the census — a superset of "3-clauses", which can only *create* TwoCC
  members, never hide them: sound.  (ii) Under the broadest reading of
  "inferred" (semantic implication from a pair = supersets of a parent or of
  a resolvent), no additional critical clause can arise in this family: every
  resolvent has ≥ 1 positive literal, clauses with ≥ 2 positives keep ≥ 2
  under weakening, width-3 critical clauses have no width-≤3 proper
  weakenings, and width-≤2 one-positive resolvents do not exist (B2).  So the
  engine's resolution-only F̃ is complete for TwoCC purposes under every
  reading of Definition 31 — *for one round*.  For the iterated reading see
  R-E: pairs breaks, triples survives.
* TwoCC = closure-based set per repair R4: matches Definition 31 and the
  corroborating Proposition-56 quote.  ID_i = J_i \ TwoCC (§6 vs §8
  convention) as pinned in stage1 §1: consistent with p. 20/p. 45.

### B2. Closure adds no critical clause (§3.4) — **CONFIRMED**; my independent re-derivation

Setup: negatives occur **only** in critical clauses (¬u ∈ C_x iff arc x→u);
positives occur as critical heads and throughout the all-positive aux clauses.
Every resolution therefore falls in exactly one case:

* **aux × aux.**  No complementary pair (all-positive).  No resolvents.  ∎
* **critical × aux.**  Forced shape: C_x = (x ∨ ¬v ∨ ¬w), v ∈ out(x), aux A ∋ v.
  Resolvent R = {x, ¬w} ∪ (A∖{v}).
  - x ∉ A: A's vertex set is pairwise non-adjacent, x is Adj-adjacent to v.
  - Hence positives(R) = {x} ⊔ (A∖{v}), **≥ 2 positives at any width** —
    never critical.  Tautology iff w ∈ A∖{v} (discarded).
  - Width-2 resolvents impossible: pairs give R = (x ∨ b ∨ ¬w) with b = x
    excluded and b = w a tautology, so width exactly 3 with 2 positives;
    triples give width 4 (same two coincidences excluded).
  - Resolving **on the head x** is impossible against an aux parent: it
    would need ¬x, and aux clauses carry no negatives.  Confirmed: no clause
    type other than critical clauses carries negative literals.
* **critical × critical.**  Only head-vs-negative: C_u ∋ ¬x (arc u→x) against
  C_x's head.  R = {u, ¬v, ¬f(x), ¬g(x)}, v = out(u)∖{x}.
  - Exactly **one** positive (u); u ≠ v (no self-arc); tautology iff
    u ∈ out(x), i.e. a 2-cycle — none exist (verified).
  - Width 4 unless the grandparent overlap v ∈ {f(x), g(x)}; a double
    coincidence is impossible (f(x) ≠ g(x)), so **width-2 resolvents cannot
    occur** here either.
  - Overlap enumeration over the two arc types (my derivation, discharging
    the doc's machine-deferred exclusions *analytically* for the explicit
    family): arc via f (u = x−1): g(x−1) = x+1 needs a jump of 2 < base;
    g(x−1) = g(x) needs δ = 1, or δ ≡ −1, or q_i = q_j, or consecutive
    specials — all excluded (δ ≥ 2, distinct q's, p-spacing ≥ 10).  Arc via
    g (x = g(u)): u+1 = g(u)+1 is a self-arc; u+1 = g(g(u)) needs a 2-jump
    sum ≡ 1 (mod n), impossible since 2-jump sums lie in [2·base, n−3].
    So overlap-freeness is a *theorem* for the explicit construction, not
    merely a machine observation.  The engine's `ovl` metric is exactly
    "∃ arc u→x with (out(u)∖{x}) ∩ out(x) ≠ ∅" (code equivalence checked) —
    equivalent to the doc's two exclusion conditions given the jump window.
    `ovl` is diagnostic-only, but nothing rests on it: V4's exhaustive
    resolvent census would catch any overlap-induced critical resolvent, and
    such a resolvent can never coincide with the canonical C_u (its third
    negative lies in out(x) ∌ x), so masking is impossible.
* **Zero-positive resolvents cannot arise** (each resolvent inherits the
  non-resolved parent's head or the aux remainder), so no weakening of a
  resolvent is ever critical — closing the last loophole of the broad
  "inferred" reading.

**No missed case.**  Machine cross-check (mine): pairs — strict-reading
resolvent set is empty, loose-reading sets have 1,012–18,691 elements, all
with ≥ 2 positives, zero critical; triples — zero resolvents under both
readings.  Every variable has exactly one critical clause in F̃ on all 21
instances.  TwoCC = ∅ replicated everywhere.

### B3. Unique satisfiability (§3.3) — mechanism **CONFIRMED**, doc's step **defective at small n** (R-D)

My re-derivation of the closed-set characterization: β with zero-set S ≠ ∅
satisfies F iff (i) every x ∈ S has an out-neighbor in S (else C_x is
falsified: x = 0 and both negated vars = 1), and (ii) no all-positive killer
lies inside S (pairs: S contains no non-adjacent pair = S is an Adj-clique;
triples: S contains no pairwise-non-adjacent triple).  Machine-validated
against direct clause evaluation (4,000 random assignments + all |S| ≤ 3 per
instance; 21/21 exact agreement).  |S| = 1 dies by (i) (no self-arcs).
Closedness ⇒ S contains a directed cycle ⇒ |S| ≥ girth.

* **Δ(Adj) ≤ 5 is correct** (ring ±1, own jump target, ≤ 2 jump preimages;
  parallel edges collapse in the *set* Adj and can only reduce the count, so
  they cannot break the bound), hence clique ≤ 6.  **But** the doc's
  conclusion "|S| ≤ 6 < girth for the verified/large n" fails at girth ≤ 6,
  which is the case for six verified instances (see R-D).  The theorem's
  asymptotic form survives (girth → ∞), and my triangle-free repair removes
  the girth dependence entirely and covers all n ≥ 26.
* **Triples:** the greedy bound is valid — any |S| ≥ 3(Δ+1) = 18 contains an
  independent triple (pick, delete ≤ Δ+1 = 6, repeat) — though 2(Δ+1)+1 = 13
  is the sharp version of the same argument.  Girth ≥ 18 holds for the
  explicit verified instances (20, 30) but not the search ones (8, 9), which
  rest on V3/my enumerator; asymptotically girth ≥ 18 holds for large n by
  R-C's repaired bound and empirically from n ≈ 80 (corner m1) / n ≈ 160–200
  (worst m1 ≤ n/10).

### B4. Degrees (§3.1) — **CONFIRMED**

f = +1 is a bijection (1 in-arc each).  Default g = +base is a bijection;
redirects s_i → q_i.  p_i: loses its unique default preimage s_i; no q_j = p_i
(Q∩P = ∅); ⇒ 0 g-preimages ⇒ indegree 1.  q_i: default preimage q_i − base
survives (it equals s_i + δ, which is special iff q_i = p_j — excluded) and
s_i is added; s_i ≠ q_i − base (δ ≠ 0); no third source (bijectivity +
distinct q's) ⇒ indegree 3.  All others: exactly one g-preimage ⇒ indegree 2.
Widths: jumps ∈ [base, jmax] ∌ {0, 1} and q_i ∉ {s_i, s_i ± 1}.  The
δ-exclusions actually used are **only** the Q-conditions — P∩S-disjointness
(doc's extra clause) is never needed (basis of repair R-A).  Independent
profiles on all 21 instances: {1: m1, 2: n−2m1, 3: m1}, J_0 = ∅ — exact match.

### B5. Girth (§3.2) — **BROKEN as stated** (R-C); measured values all reproduce

My own BFS reproduces the transcript girth on all 21 instances (5–30).  For
the explicit n = 80 instance I derived the girth-20 cycle exactly:
δ = 2, so specials jump +29; from q_i = p_i + 2, three unit steps reach
s_{i+2} = p_i + 5; five segments of (special + 3 units) = 20 steps, total
displacement 160 = 2·80.  This certified-correct 20 already refutes the doc's
"worst pattern k = 1, j = 2" (which gives 24 at n = 80); the doc's numeric
bound survives at n = 80 by luck (20 ≥ 17.67) and fails from n = 78 onward at
116 of 193 sampled sizes (scan to n = 800), including the analytically
predicted and BFS-confirmed girth = 52 < 57.67 at (n, m1, δ) = (200, 11, 2).
"Special steps never chain" is true only in the immediate-successor sense.
Girth growth is genuinely linear (~0.2n–0.3n), so every claim that only needs
girth → ∞ (or ≥ 18 eventually) survives with the corrected argument in R-C.

### B6. No-go corollary CR-2 — **CONFIRMED** (airtight given Stage-V inputs), with precise scope

* **(i)** The LP objective Φ = max{L_reg, L_irr} is a max of two affine
  functions — continuous.  `lp_reconstruction.md` §5's corner-uniqueness
  argument re-checked line by line: the subgradient convex combination at
  weights (λ, 1)/(1+λ), λ = b1/A is ((b0 − 2b1), 0, (bT + λS))/(1+λ) with
  certified-positive first and third components; the standard octant KKT
  condition and the strict-inequality uniqueness argument are correct.
  Note the *value* part of CR-2 does not even need uniqueness: for any valid
  constraint set C, Γ' = inf over Feasible∩C ≥ γ* (subset) and
  Γ' ≤ lim Φ(0, m1(n)/n, 0) = Φ(corner) = γ* (realized points lie in C;
  Φ continuous), hence Γ' = γ* exactly.
* **(ii)** Selection quantifier: engine V1 (exactly one critical clause in F)
  and V4 (exactly one in F̃) both replicated by my independent census on all
  21 instances — no selection freedom exists, so validity "for some
  selection" and "for every selection" coincide on the family; CR-2's
  parenthetical is exactly right.
* **(iii) What CR-2 does and does not rule out.**  Ruled out: any constraint
  Q(i_0, i_1, tau) ≥ 0 — of arbitrary form, no continuity needed — valid for
  all uniquely satisfiable 3-CNF (width ≤ 3; and by the triples variant, also
  the all-width-3 subclass and every plausible "regular" subclass, since the
  family has all critical clauses width 3 with distinct negatives) that
  excludes a *neighborhood* of the corner; equivalently, any addition to the
  LP that would raise its value.  **Also ruled out (worth adding to the doc,
  currently implicit):** n-joint constraints Q(i_0, i_1, tau, n) ≥ 0 cannot
  raise the *asymptotic* value either, because the family realizes
  |i_1 − i_1*| ≤ 1/(2n) at every n ≥ n_0, so any uniform-in-n neighborhood
  exclusion is falsified at finite n.  Not ruled out (doc states the first
  three): (a) new statistics with new estimate dependence (the corner family
  is Θ(n²)/Θ(n³)-dense and could be separated by aux-sensitive statistics);
  (b) improving the imported estimates; (c) restrictions of the instance
  class the analysis quantifies over — in particular sparse m = O(n)
  realizability is OPEN (correctly recorded); (d) trivially, constraints
  excluding only the measure-zero irrational point itself — these cannot
  change the LP value (objective continuity) and CR-2's neighborhood phrasing
  already handles them.  CR-2's dependency labeling (conditional on Stage-V
  LP reconstruction and the exact i_1*, γ*) is accurate; those inputs were
  not re-derived here beyond §5's algebra.

### B7. Engine audit — **CONFIRMED sound** (minor cosmetic gaps)

* `sat_dpll`: branching restricted to unassigned variables of the first
  active clause, both polarities tried — complete; unit propagation reaches a
  fixpoint and correctly detects conflicts; "no clauses left" = SAT is
  correct (remaining variables free); the forced literal is seeded into the
  initial assignment and can never be overwritten (the historical bug noted
  in the doc's ledger is indeed fixed).  **Differential test: 1,350 queries
  (450 random + family-style formulas × 3 forced literals) against exhaustive
  truth tables — zero mismatches.**
* `resolvents`: variable-indexed pairing over positive/negative occurrence
  lists is exhaustive; exact-literal removal, tautology filter, width-≤3
  filter, and both parent-width readings are correct.  Self-resolution is
  vacuously impossible (no clause contains complementary literals).
  **Differential test: 400 random clause-sets × 2 readings against a naive
  all-pairs implementation — zero mismatches.**
* V4 logic: any critical resolvent not identical to one of the n canonical
  clauses lands in the census; a critical clause's head is determined by its
  unique positive literal, so cross-variable masking is impossible; TwoCC ≠ ∅
  under either reading fails the case.  Correct.
* verify()/main(): every V-error fails the case; construction exceptions fail
  the run; exit code 0 iff all pass; the dataset is rebuilt deterministically
  (no randomness anywhere in the engine).  Correct.
* Minor (no load-bearing effect): the V1 docstring promises an
  aux-non-adjacency check that the code does not perform; the V6 docstring
  promises "max clique size vs girth" but no clique computation exists;
  V5 does not enforce claim 4's "rest of indegree 2 or 3" tail (profiles show
  it anyway); V6's girth/ovl/2cyc are printed diagnostics that do not gate
  pass/fail (V3/V4 carry the load, as the doc itself states).

### B8. Independent replication — **FULL AGREEMENT (21/21)**

From `instances.json` (only `g` + variant trusted; clauses rebuilt from the
doc's §2 spec by my own code):

| check | result |
|---|---|
| clause counts vs transcript | 21/21 exact (pairs m = n + C(n,2) − 2n; e.g. 299/405/1175/3080/4850/7020; triples 27,684/70,245/142,806) |
| indegree profiles | 21/21 = {1: m1, 2: n−2m1, 3: m1}, J_0 = ∅; Σindeg = 2n |
| closure/TwoCC, strict reading | 21/21: resolvent set **empty** ⇒ F̃ = F ⇒ TwoCC = ∅ |
| closure/TwoCC, loose reading | 21/21: pairs 1,012–18,691 resolvents, all ≥ 2 positives, TwoCC = ∅; triples 0 resolvents |
| exactly one critical clause per var in F and F̃ | 21/21 (forced selection confirmed) |
| iterated-closure probe | pairs n=26: 19,201 clauses, TwoCC = 26/26; pairs n=30-explicit: 29,755, TwoCC = 30/30 (⇒ R-E); triples: F̃ = F trivially (zero resolvents to iterate) |
| uniqueness, own DPLL enumerator (counter-based, cap 2) | 21/21: exactly one model, = 1^n (12–697 nodes; incl. triples n=100 with 142,806 clauses) |
| uniqueness, closed-clique route (pairs; complete) | 15/15 pairs instances: no closed clique among all cliques (max clique = 2 everywhere) |
| uniqueness, cycle route (triples explicit) | n=80/100: no simple directed cycle ≤ 12; girth 20/30 ≥ 13 ⇒ complete structural proof |
| uniqueness, exhaustive small-S sweep | n=30-explicit: all 8,656,936 subsets |S| ≤ 8 — none closed+killer-free; n=50-explicit: all 2,369,935 subsets |S| ≤ 5 — none |
| characterization vs direct clause evaluation | 21/21 agreement (4,000 random + all |S| ≤ 3 each) |
| girth (own BFS) | 21/21 match transcript (5…30) |
| g reconstruction from doc §2 formulas | engine-style condition: 7/7 explicit instances reproduced **exactly** (δ = 2 in all); doc-literal condition: **vacuous at n=50 and n=100** (R-A) |

Disagreements with the engine: **none**.  Disagreements with the *document*:
R-A, R-C, R-D above.

### B9. Counterexample hunt against genuinely valid constraints — **NONE FOUND**

Checked against every valid constraint I could prove: nonnegativity ✓;
i_0 + i_1 + tau ≤ 1 ✓ (0.06 ≪ 1); Σ indeg = 2n ✓ (m1 + 2(n−2m1) + 3m1);
SG handshake ✓; degree identity 2n_0 + n_1 = Σ_{k≥3}(k−2)n_k ✓ (0 + m1 =
1·m1); every variable owns ≥ 1 critical clause (forced by unique
satisfiability) ✓; Lemma-34 consistency (n − m1 ≤ |H| ≤ n) ✓; Observation-37
consistency ✓.  Parity hunts: n_1's parity is unconstrained by the arc-count
identity (n_1 + 3n_3 = 4m1 is even automatically); no parity obstruction
exists.  The m1 = 0 instance realizes (0, 0, 0), so no valid constraint
separates even the extreme corner of the segment.  Had any genuinely valid
constraint failed on the family, uniqueness or the statistics would have had
to be wrong — both replicate under four independent methods.

---

## Additional minor observations (no action strictly required)

1. §3.4's prose garbles the g(x−1) = g(x) exclusion ("q_i − base ∈
   {s_j, s_j ± 1}…") — the needed fact is simply δ ≠ 1 (and δ ≢ −1), which
   holds; the machine check and my derivation close it.  Cosmetic.
2. Theorem CR's "n_0" is genuinely needed: n = 27 (δ-nonexistence) and the
   sub-threshold girths at n ≤ ~76 mean n_0 cannot be 26; the statement
   already quantifies "there are constants n_0", so this is not an error —
   but §5's "verified/large n" phrasing blurs which instances the *asymptotic*
   argument covers versus which rest on V3/V4 (six pairs and two triples
   instances are V3-covered only).  The repaired §3.3 (triangle-freeness)
   makes all pairs instances proof-covered; the triples-search instances
   remain machine-covered only.
3. CR-1's numeric claim checked: |0.06 − i_1*| = 4.32·10⁻⁵ at n = 50, 100 ✓;
   rounding bound 1/(2n) ✓.
4. The engine's constructor comment "requires n ≥ 26" is accurate for the
   *search* variant it gates, but the explicit builder silently fails at
   n = 27 (assert) — consistent with R-B, worth a comment.

## Files written by this review

* `research_cycle_07/checkers/cr_review_independent.py`
* `research_cycle_07/checkers/cr_review_independent_output.txt` (full 21-instance log; exit 0)
* `research_cycle_07/checkers/cr_review_triples_rerun.txt`
* `research_cycle_07/checkers/cr_review_girth_scan.py`
* `research_cycle_07/checkers/cr_review_girth_scan_output.txt`
* `research_cycle_07/checkers/cr_review_engine_diff.py`
* this report: `audits/cycle07_corner_theorem_review.md`

No reviewed file was modified.  No git commands were run.

## Bottom line

* **Theorem CR (claims 1–4, both variants, verified range):** CONFIRMED by
  independent replication; nothing broke.
* **Theorem CR (asymptotic proof text):** SOUND WITH REPAIRS R-A…R-D — the
  written δ-condition is vacuous at two verified sizes, the written girth
  bound is false, and the written pairs-uniqueness step fails at six verified
  sizes; all repaired here with proofs that are simpler and stronger than the
  originals.
* **Corollary CR-1:** CONFIRMED (with n_0 per R-B/R-C).
* **Corollary CR-2 (no-go):** CONFIRMED and airtight given the Stage-V LP
  inputs; strengthened by noting n-joint constraints are also blocked; the
  triples variant should be its primary carrier for reading-robustness (R-E).
* **Engine:** CONFIRMED sound (differentials clean); cosmetic docstring gaps.

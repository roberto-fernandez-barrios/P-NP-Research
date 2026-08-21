# Research Cycle 3: structural DAG attack

**Cycle date:** 2026-08-21
**Primary target:** O01 — polynomial-size 1-balanced-chain set systems
**Stopping condition:** S3-D reached by an exact finite `n=10` result
**Primary status:** O01 remains **OPEN** and unclaimed

## Executive conclusion

Research Cycle 3 deliberately attacked the apparent small-value formula

`N(2m)=m(m+1)`.

It fails at the first mandated frontier.  Under the FLSY convention, counting
the empty and full sets,

`N(10)=35`,

whereas the finite formula predicts 30.  The determination is an exhaustive
finite computational result with standard-library recomputation and explicit
upper witnesses; it has no asymptotic implication.

The exact level-cover minima are

`tau(10,k) = 1,1,5,3,5,3,5,3,5,1,1`,

with sum 33.  A normalized color-reachability exhaustion proves that no
prefix with the minimum counts `1,1,5,3,5` reaches every balanced coloring
through rank four.  Complementation gives an upper-suffix obstruction.  The
two disjoint defects exclude sizes 33 and 34, while a 35-subset family works
for all 252 signed balanced colorings.

The structural attacks did not produce a general polynomial construction.
They instead killed precise star-spine, laminar-hierarchy, layer-gluing,
cyclic matching-state, and recursion rules, preserving their smallest
counterexamples and retry conditions.  The useful surviving statements are
restricted invariants and reductions, not O01:

- an adversarially reviewed but unformalized proof candidate shows that a
  unique-singleton family needs at least `ceil(n/4)` selected triples;
- the unformalized prefix-defect lemma forces level surplus in an affected
  rank band;
- a conditional, unformalized one-step additive lift reduces same-sign new
  points to a separate
  one-sided defect-router family, whose polynomial construction remains open;
- recursively laminar frontiers exhibit an exact state-accounting versus
  routing-flexibility tradeoff; and
- the canonical even-subset DAG is polynomially equivalent to the FLSY
  pair-open read-once program only after support normalization and explicit
  odd-intermediary accounting; and
- a concrete cyclic-interval family has exactly `(n-1)^2+2` literal states,
  is exhaustively valid through `n=20`, but fails first at `n=22` within that
  class.

None of these statements proves a polynomial bound, an mABP separation, an
algebraic or Boolean complexity separation, or P versus NP.

## 1. Hardened foundation

The Cycle-2 claims needed here were treated as untrusted and independently
reconstructed.

### Consecutive pairs and the exact path DAG

A maximal chain with insertion order `pi_1,...,pi_n` is 1-balanced for a
coloring exactly when every consecutive pair

`{pi_1,pi_2}, {pi_3,pi_4}, ..., {pi_(n-1),pi_n}`

is bichromatic.  Even prefix imbalances are even integers of absolute value
at most one, hence zero; the converse follows by summing crossing pairs.

Consequently a fixed chain covers `2^(n/2)` signed balanced colorings, not
two.  Two stale Cycle-1 passages were corrected.  The explicit-list lower
bound becomes `binom(n,n/2)/2^(n/2)`, which remains exponential but says
nothing against shared subset states.

Contracting every two steps gives an exact functionality-preserving DAG:
vertices are selected even subsets, an arc `S -> S union {a,b}` exists only
when a selected odd intermediary backs it, and the arc is open exactly when
`{a,b}` crosses the coloring.  Expanding an open path through its stored odd
intermediaries recovers a selected balanced maximal chain.

Raw even-DAG vertex count is not exactly `N(n)`, because `N(n)` also charges
odd subsets.  Polynomial existence is preserved: a `q`-vertex canonical
subset DAG has at most `q*binom(n,2)` inclusion-by-two arcs, so choosing one
odd intermediary per arc yields at most `q(1+binom(n,2))` distinct subsets.

An independent standard-library checker compared the contracted and
uncontracted definitions for all 16 families on two points and all 65,536
families on four points, for every signed coloring.  It also rechecked the
stored systems through `n=8`.

### S1, S2, and the surcharge

Lemma S1 survives independent review: if `{v}` is the unique selected
singleton on `n=2m` points, at least `m` selected pairs are incident with
`v`.  Otherwise color `v` and all its selected neighbors plus and fill to a
balanced positive set; every reachable pair is monochromatic.  Complementing
sets and reversing chains gives S2 for a unique co-singleton.

For each rank, `tau(n,k)` is the minimum size of a compatibility cover of all
balanced colorings.  Every valid family pays that minimum independently at
each rank, so

`L(n)=sum_k tau(n,k) <= N(n)`.

The connectivity surcharge

`sigma(n)=N(n)-L(n)`

is therefore a nonnegative aggregate excess.  It is not automatically the
size of a removable bridge set over an embedded collection of minimum
covers.  The exact values now give

| `n` | `L(n)` | `N(n)` | `sigma(n)` |
|---:|---:|---:|---:|
| 2 | 3 | 3 | 0 |
| 4 | 6 | 6 | 0 |
| 6 | 12 | 12 | 0 |
| 8 | 19 | 20 | 1 |
| 10 | 33 | 35 | 2 |

CF-LOGGAP was audited only for leakage.  It remains a restricted obstruction
to the unchanged greedy, bounded-block, single-consumption cached-frontier
process and its posted high-confidence logarithmic-gap contract.  No
conclusion from it is transferred to a deterministic subset DAG or to O01.

Full details and reproduction are in
[`foundation_independent_audit.md`](../research_cycle_03/foundation_independent_audit.md)
and [`cycle03_verify_foundation.py`](../experiments/cycle03_verify_foundation.py).

## 2. Literature and equivalent-object audit

The literature search was updated through 2026-08-21 using primary sources
and terminology variants.

Fabris--Limaye--Srinivasan--Yehudayoff is now published at CCC 2026,
LIPIcs 383, Article 22, DOI
[10.4230/LIPIcs.CCC.2026.22](https://doi.org/10.4230/LIPIcs.CCC.2026.22),
with [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/) as the
full version.  It supplies the pair-labelled open-path read-once program and
the public range

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`.

The polynomial claim in arXiv:2604.00746/ECCC TR26-043 remains withdrawn.
The current records say the required conditional-filtration estimate is not
proved and that all results depend on it.  Its stale theorem-claiming abstract
is not evidence.

No primary source was located for exact `N(6)`, `N(8)`, or `N(10)=35`, nor
for the now-falsified quadratic formula under the same distinct-subset size
normalization.  These dispositions are only
`PRIOR-ART-NOT-FOUND`; they are not novelty or priority claims.

The closest exact established model is FLSY's pair-open read-once program.
Classical monotone switching networks, Beneš/Waksman routing, superconcentrators,
cut-matching, ZDDs, separating/bisecting systems, covering designs, and
Boolean-lattice chain covers illuminate parts of the problem but do not
control the union of literal processed-element subsets.

See
[`literature_novelty_audit.md`](../research_cycle_03/literature_novelty_audit.md)
for sources, search protocol, terminology collisions, and negative-search
limitations.

## 3. Exact finite determination at `n=10`

### 3.1 Level-cover lower bound

For every rank `k`, an explicit cover of the claimed size is checked against
all 252 positive masks.  To rule out a cover one smaller, choose any member
of a hypothetical cover and relabel it to `{0,...,k-1}`; `S_10` is transitive
on rank-`k` subsets and balanced colorings.  Enumerate all choices of the
remaining members.  A smaller cover could be padded, so this is complete.
The hardest case fixes one rank-four member and checks
`binom(209,3)=1,499,784` branches.  Complementation supplies upper ranks.

This proves the exact vector above and `N(10)>=33`, already ruling out size
30 without a global MILP.

### 3.2 Prefix obstruction and size 34

In an exact-minimum prefix through rank four, normalize the unique singleton
to `{0}`.  All five selected pairs must be reachable; otherwise the remaining
four would contradict `tau(10,2)=5`.  They therefore form the normalized star
`{0,i}`, `1<=i<=5`.

Exact 252-bit reachability propagation gives 30 live triple candidates.
All 4,060 choices of three triples are checked; 90 reach every coloring at
rank three.  Across those branches, all 1,686,060 choices of five reachable
four-sets are checked.  None reaches all colors; the maximum is 250 of 252.
Globally unreachable selected states are not omitted unsafely: if one were
selected, the remaining fewer-than-`tau` live states would have to cover all
colors at that rank.

A size-34 family has exactly one unit of surplus over the level minima.  A
surplus at rank five or above leaves the forbidden lower prefix.  A surplus
at ranks one through four leaves an exact-minimum upper suffix, which becomes
the same forbidden prefix after complementation and path reversal.  End
ranks cannot have surplus.  Hence size 34 is impossible.

More generally, every size-35 optimum has one unit of excess in ranks
`1,...,4` and one in ranks `6,...,9`, and none at rank five.  The displayed
family places them at ranks four and six; those exact ranks are not forced.

### 3.3 Upper family

The certified family has 35 distinct masks and level counts

`1,1,5,3,6,3,6,3,5,1,1`.

Literal checking accepts a stored maximal-chain witness for every signed
balanced coloring.  Independently enumerating the induced Boolean-lattice
DAG finds 60 maximal chains, verifies coverage without trusting optimizer
flows, and shows every subset in this displayed family is essential under
single-vertex deletion.  The family has a unique singleton and co-singleton,
minimum terminal half-stars, and 22 signed colorings with a unique represented
path.  These properties are not asserted for every optimum.

Run:

```text
python -B experiments/check_balanced_chain_n10_exact.py
```

The checker uses only the Python standard library.  The full proof boundary,
SAT/cut-generation corroboration, masks, witnesses, and certificates are in
[`exact_n10.md`](../research_cycle_03/exact_n10.md) and
[`certificates/balanced_chain_n10/`](../certificates/balanced_chain_n10/README.md).

## 4. Structural construction classes

### CP-S: star spines

Two exact classes were tested.

- `CP-SD`, a literal two-rail diamond spine, has at most `6m-4` distinct
  subsets on `n=2m` points.
- `CP-SQ`, the broader quadratic width envelope, has `m` states at each
  internal even rank and two at each internal odd rank, for exactly
  `m(m+1)` distinct subsets.

The general terminal-fanout proof candidate says that a valid family with a
unique singleton needs at least `ceil(m/2)` selected triples: each triple can
continue at most two incident star pairs, and if fewer than `m` leaves
continue, the anchor and all continuing leaves can be colored alike.  Thus
both two-rail/two-triple classes fail for every `m>=5`, first at `n=10`.
All 7,140 local two-triple choices were also exhausted.

### CP-P: recursively laminar frontiers

For a rooted full binary leaf hierarchy `T=(A,B)`, define

`H(T)=H(A) union H(B) union (A+H(B)) union (B+H(A))`.

The exact distinct-state recurrence is

`h(T)=2h(A)+2h(B)-4`.

Complete balanced hierarchies on powers of two have the attractive quadratic
count `(2n^2+4)/3`, but coloring one root half plus and the other minus makes
every selected rank-two state monochromatic.  They fail first at `n=4`.

A sharper `n=6` example has 28 states and covers every balanced coloring at
every rank, yet plus set `{0,1,2}` has no full path: the hierarchy forces one
root block to be exhausted, and neither block order admits crossing pairs.

Every unlabelled rooted full binary shape was exhausted through `n=12`.  At
`n=10`, all 98 shapes have at least 76 states and the six valid shapes have at
least 448.  These are construction-class data only; no growth rate is
inferred.

### CP-G: layer-cover gluing

Four tempting rules fail under exact definitions.

- Exact minimum covers at all ranks first fail to glue at `n=8`.
- A total surcharge of one first fails at `n=10`.
- Allowing arbitrary extra states only at the middle rank works for the
  displayed `n=8` optimum but fails at `n=10`, because the lower prefix has
  already failed before the middle.
- Even requiring a compatible inclusion edge for every coloring across every
  adjacent interface does not make those edges composable.  Exhausting every
  endpoint-containing family through `n=4` finds the smallest counterexample
  `[0,1,3,5,10,11,15]`, of size seven.

The reusable prefix-defect proof candidate says: if ranks `0,...,r` cannot
reach all colors at their exact minima, every valid family has at least one
unit of excess in that rank interval.  Complementation gives the upper
interval; if `2r<n`, the intervals are disjoint and force two units.  This
proves the all-optimum band restriction at `n=10` from the finite prefix
certificate.

The displayed `n=8` and `n=10` surplus ranks contain no embedded
`tau`-sized cover subfamily.  Thus `sigma` cannot universally be read as a
number of removable bridge vertices.

### CP-M: shared matching states

The matching track first exposed an important validation error.  A union of
listed chain prefixes can contain maximal chains that were not among those
listed: inclusion edges splice prefixes from different seeds.  At `n=10`,
the plus set `{0,1,2,3,6}` crosses none of the nine round-robin seed
matchings, but the literal family contains the hybrid witness order

`3,9,4,2,5,6,7,1,8,0`.

Thus seed-menu noncoverage is not a construction counterexample.  All
coverage tests in the corrected track search the full induced subset DAG.

For a live, fixed-length, syntactically read-once pair-labelled program, an
unformalized normalization proof shows that every vertex has a unique used
support.  Merging equal supports is safe.  If `Q(n)` is the minimum number of
even support vertices in the resulting canonical subset DAG, explicit
odd-intermediary accounting gives

`Q(n) <= N(n) <= Q(n)+min(Q(n)^2,Q(n)*binom(n,2))`.

There is also an exact unformalized reduction: `N(n)` is the minimum size of
the literal all-prefix union of a cut-covering collection of oriented ordered
perfect matchings; `Q(n)` is the analogous even-prefix minimum.  These are
model equivalences, not upper bounds or novelty claims.

The sharpest concrete CP-M test is the cyclic interval family `RR_n`.  It is
the union of prefixes of the `n-1` round-robin factor orders.  Its selected
sets are the two endpoints, all finite singletons, and `infinity` joined to
every proper cyclic interval.  Hence it has exactly

`|RR_n|=(n-1)^2+2`

distinct subsets.  Hybrid paths are characterized exactly by a deque
recurrence on the cyclic sign word.  Exhausting every normalized balanced
word proves validity for every even `n<=20`.  At `n=22`, exactly the 21
rotations of `1^8 0^5 1^3 0^5` fail; their reachable interval states die at
length 13.  A separate unformalized recurrence proof candidate gives the
four-run countercolor

`1^(m-3) 0^5 1^3 0^(m-6)`

for this same family at every `n=2m>=22`.  This kills one quadratic family,
not shared matching-state compression in general.

Three further exact classes fail cleanly: full submatching closure already
has `2^(n/2)` supports for one matching; a stage-only selector becomes
invalid without used-support memory and has `2^(n-1)` states after the
literal lift; and compatibility-signature merging first splices repeated
supports at `n=4`.

Detailed class definitions, proofs, countercolors, and checkers are in
[`cp_s_recursion_attack.md`](../research_cycle_03/cp_s_recursion_attack.md),
[`cp_p_hierarchy_attack.md`](../research_cycle_03/cp_p_hierarchy_attack.md),
[`cp_g_gluing.md`](../research_cycle_03/cp_g_gluing.md), and
[`cp_m_matching_equivalence.md`](../research_cycle_03/cp_m_matching_equivalence.md).

## 5. Recursion attack and precise missing obligations

Simply appending two new points fails when they have the same sign, because
the old restriction then has total imbalance `+/-2`.

A one-sided 2-defect router `D` contains, for each total-`+2` coloring, a
chain whose prefix imbalances lie in `[0,2]`, and dually in `[-2,0]`.  If `X`
is balanced-chain and `D` is such a router, the explicit lift

`R(X,D)=X union ({a}+D) union {U+{b}, U+{a,b}}`

is balanced-chain on two more points and has the exact additive count

`|R(X,D)|=|X|+|D|+2`.

This is a conditional one-step lemma, not a recursion satisfying O01.
Polynomial routers `D_n` for all `n` would yield a polynomial family after
summation, but no such construction is proved.  Reusing `X` as its own router
loses the required defect property at `n=6`, and the next unsupported lift
loses balanced coverage at `n=8`.  The recurrence also doubles `|X|`.

The CP-P full insertion lift always preserves coverage, but clones four
marker copies of every old state: `|I(X)|=4|X|`.  A sparse additive top splice
works for one step under a two-defect terminal invariant, then loses that
invariant at `n=6`.  Preserving it exposes successively larger defects; the
literal union of all even residual frontiers has `2^(n-1)` states.

Accordingly no proposed transformation satisfies the required theorem
“property `P` is explicit, preserved, and adds only `poly(n)` distinct
subsets.”  The precise open obligation is a non-escalating, polynomial-state
all-defect routing/compression lemma.  Naming that obligation does not prove
it.

## 6. Formalization and independent validation

The reusable finite core was formalized in Lean 4.32.1 with a pinned mathlib
4.32.1 manifest.  The kernel accepts, without `sorry`, `axiom`, or `admit`:

- balanced coloring, imbalance, insertion-order maximal chains, and the
  fixed-family quantifiers;
- both directions of the consecutive-pair characterization;
- both directions of the contracted path-DAG reformulation for path
  functionality on an even ground set; and
- Lemma S1 and its direct final-pair dual S2.

These named declarations are `FORMALLY VERIFIED` within the encoded
insertion-order and contracted-path representations.  The order-theoretic
extensional characterization of maximal chains, a separate graph object,
distinct-state accounting, `tau`/`sigma`, all exact values of `N(n)`,
CF-LOGGAP, the Cycle-3 construction classes, and O01 remain unformalized.

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

An independent formal audit also directly elaborated the source at trust
level zero, inspected the exported theorem types, and found only Lean's
ordinary classical/mathlib axioms, with no `sorryAx`.  See
[`lean_formalization.md`](../research_cycle_03/lean_formalization.md),
[`formal/coverage.md`](../formal/coverage.md), and
[`formal_adversarial_audit.md`](../research_cycle_03/formal_adversarial_audit.md).

The stage-1 adversarial audit independently reimplemented the `n=10` lower
and upper checks, including all 1,686,060 prefix branches, and separately
implemented contracted reachability for CP-S/P/G.  It confirmed the finite
claims after narrow wording corrections.  The final stage independently
audits corrected CP-M semantics, the all-`m` countercolor proof candidate,
formal scope, this integration, and the canonical state update.  The two
reports are
[`cycle03_n10_structural_adversarial.md`](../audits/cycle03_n10_structural_adversarial.md)
and
[`cycle03_final_integration_adversarial.md`](../audits/cycle03_final_integration_adversarial.md).

## 7. Failure knowledge and stopping boundary

Every rejected construction class, its smallest counterexample, its exact
scope, and a retry condition is preserved in
[`failure_knowledge.jsonl`](../failure_knowledge.jsonl).  In particular, the
unchanged greedy single-consumption cached-frontier process was not retried or
silently generalized.

Cycle 3 stops under S3-D: the exact finite result `N(10)=35` decisively
falsifies the size-30 target and several structural candidates, while the
remaining classes fail for recorded reasons.  The formalization and
independent integration audits above are complete.  O01 remains **OPEN**.
Research Cycle 4 is not begun automatically.

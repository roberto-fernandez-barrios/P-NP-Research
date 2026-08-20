# Cycle 2 positive-repair track: balanced-chain steering

**Date:** 2026-08-13

**Track:** independent proof/SAT-side reconstruction and repair audit

**Target boundary:** this report does **not** prove or refute O01.

**Epistemic status:** exact derivations and finite certificates are internally
checked and `UNFORMALIZED`. The cached-frontier logarithmic-gap obstruction,
the fixed-order obstruction, and the two bounded positive diagnostics below
have received independent internal adversarial review. No external review or
novelty claim is made.

## 1. Outcome

None of the five required repair families currently meets all three proof
obligations:

* **A — actual-filtration control:** a conditional drift or return theorem for
  the process the builder really executes;
* **B — residual control:** a proved subpower residual/block-size bound and a
  feasible scale transition; and
* **C — total accounting:** a polynomial bound on the total number of
  **distinct subsets** in one coloring-independent set system, not merely a
  polynomial-time adaptive execution for each coloring.

The main negative finding is common to posterior-state, fixed-`d` steering,
and fixed/logarithmic-horizon domination.  Once an exposure leaves bad-sign
frontiers unconsumed, only one frontier is fresh at the next step.  Conditional
on the actual filtration, the supposed `2^{-d}` upward probability becomes
asymptotically `1/2`.  An exact Catalan subevent gives a polynomial lower tail
for the first return time, ruling out the logarithmic-gap estimate required by
the posted construction.

Two bounded diagnostics survive:

1. **B-RESERVE (conditional):** a variable absorb/recurse threshold repairs
   the numerical reserve inequality in a separate scale-transition error.
   This is not a complete transition and does not prove residual
   concentration or return control.
2. **C-ACCOUNTING:** power shrink plus polynomial local pattern and residual
   description counts implies polynomial **total distinct-subset** accounting.
   This isolates C cleanly but assumes A and B have already supplied the
   relevant good executions.

After independent validation, Cycle-2 Stop A is reached for the greedy,
uniformly bounded-`d`, single-consumption cached-frontier process and its
posted `1-O(1/M)` logarithmic direct-gap guarantee. This is not a broader
fixed-`d` obstruction, an mABP lower bound, a result about unrestricted
`N(n)`, or O01. The two bounded B/C diagnostics remain useful but do not form
a survivor construction.

## 2. Primary-source baseline and version control

I worked from the following primary sources, not from Cycle-2 reports by other
agents.

1. Théo Fabris, Nutan Limaye, Srikanth Srinivasan, and Amir Yehudayoff,
   *Multilinear Algebraic Branching Programs and the Min-Partition Rank
   Method*, [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/),
   especially Lemma 1.5/Lemma 2.3, Lemma 3.2, and Theorem 3.3.  The downloaded
   official PDF had SHA-256
   `56F91E2C658DC689DA9F543ACBAF8DD9E127D551CB1F915C76B49001FBA92A4A`.
2. Deepanshu Kush, *An Unconditional Barrier for Proving Multilinear
   Algebraic Branching Program Lower Bounds*, original posted manuscript of
   [ECCC TR26-043](https://eccc.weizmann.ac.il/report/2026/043/), especially
   Definition 3.1, Lemmas 3.3 and 4.1, and Sections 7--8.  The original PDF
   returned by the official download endpoint had SHA-256
   `B72A0EEDB80AEA50DD3B9ED5C1E69CFD3A717FAB7225EC69F46CFA6C15ECDA0F`.
   The current ECCC record explicitly says that the conditional bound in
   Lemma 4.1 has a gap and that all results depend on it.  The manuscript is
   therefore used only as a source of proposed constructions, never as a
   theorem.

The FLSY facts used below are exact:

* a random bridge of length `2q` satisfies, for `a >= q^(2/3)`,

  `Pr[longest zero-to-zero excursion <= 2a]
     = C(q,a) min{(q+1)^(-1/2),a^(-1/2)} exp(-beta q/a)`,

  where `C_1 <= C(q,a) <= C_2` and `beta>0` are universal (FLSY Lemma
  3.2, quoting Csáki--Erdős--Révész); and
* choosing a gap bound `m=Theta(n/log n)`, recursively filling every gap, and
  applying worst-case-from-average symmetrization yields
  `N(n) <= n^d N(n/log n)` and hence the quasipolynomial upper bound (FLSY
  Theorem 3.3).

## 3. The actual filtration

For the two-block process, a filtration containing only consumed/"assigned"
values is too coarse: the next choice is not measurable with respect to it.
The decision-time filtration `G_t` must include

* the identities and signs of all consumed points;
* the identity and sign of every inspected but unconsumed frontier;
* all previous tie outcomes; and
* the current block positions and scale state.

After an active step exactly one block advances.  Consequently, at the next
decision `d-1` frontiers are already known and only the frontier of the block
just advanced is fresh.  Conditional on `G_t`, the sign of that fresh point is
a draw without replacement from the uninspected population.  This is the
state on which every A claim below is evaluated.

Suppose `H>0`, the unconsumed pool has size `R`, and all `d-1` cached frontiers
have sign `+`, the sign that would increase `|H|`.  Global balance gives

`# plus signs in the whole pool = (R-H)/2`.

Therefore the exact actual-filtration upward probability is

`p_d(R,H) = (((R-H)/2)-(d-1))/(R-(d-1))
            = (R-H-2d+2)/(2(R-d+1)).`                   (3.1)

For fixed `d,H` and `R -> infinity`, this tends to `1/2`, not `2^{-d}`.
For the previously certified `n=10` history, `d=2,R=8,H=2`, and (3.1) gives
`p_2=2/7` exactly.

There is also an exact block-load drift.  Let block `j` be the one supplying
the fresh frontier.  If the fresh sign corrects `H` (probability `1-p_d`),
block `j` must advance.  If it is bad (probability `p_d`), all `d` frontiers
tie and a uniform tie advances each block with probability `1/d`.  Hence

`E[Delta load_j | G_t] = 1-p_d+p_d/d`,

`E[Delta load_i | G_t] = p_d/d` for every cached block `i != j`.   (3.2)

Relative to the uniform increment `1/d`, the drift vector has coordinate
`(d-1)(1-p_d)/d` at `j` and `-(1-p_d)/d` elsewhere.  In the `n=10` two-block
history this says

`E[Delta(a-b) | G_t] = 1-2/7 = 5/7`,

equivalently probabilities `6/7` and `1/7` for increments `+1` and `-1`.
Thus enlarging the posterior state repairs measurability but does not restore
the claimed load martingale.

## 4. Exact cached-frontier heavy tail

### Proposition 4.1 (finite Catalan subevent)

Let a uniform balanced coloring of `2M` points have `M` signs of each type.
Split the points into `d` ordered blocks of equal size `2M/d`, where fixed
`d>=2` divides `2M`. Run the natural `d`-frontier rule: inspect all active
frontiers, consume one minimizing absolute imbalance, and use any
nonanticipating tie rule. Here nonanticipating means that the tied frontier
is chosen from the full revealed history plus private randomness independent
of the coloring, before the next uninspected color is exposed. Uniformity is
needed for the separate load-drift formula (3.2), not for this proposition.

Let `E_d` be only the event that the initial `d` frontiers all have one
common sign; the tie policy then consumes one of them. This first consumed point is a balanced
visit because `|H|=1`.  Let `T_bal` be the number of subsequent steps until
the next visit to the balanced band `|H|<=1`.  If

`1 <= k <= M-d` and `2k+1 < 2M/d`,

then

`Pr[T_bal = 2k | E_d]
 >= Cat_(k-1) (M-d)_k (M)_k / (2M-d)_(2k)`,           (4.1)

where `Cat_j=binom(2j,j)/(j+1)` and `(x)_r` is a falling factorial.  Moreover

`Pr[E_d] = 2(M)_d/(2M)_d`.                            (4.2)

### Derivation

Assume the common initial sign is `+`.  After the first consumption, `H=1`,
`d-1` known `+` frontiers remain, and the uninspected population contains
`M-d` pluses and `M` minuses.  Until return to the balanced band:

* a newly exposed minus is consumed and decreases `H`; and
* a newly exposed plus makes all `d` frontiers plus, after which a tie consumes
  one frontier and leaves `d-1` plus frontiers cached.

Thus the newly exposed signs form an adaptive sample without replacement,
but their sign word has the ordinary ordered-hypergeometric law.  Select the
subevent in which the next `2k` signs contain `k` pluses and `k` minuses, every
proper partial signed sum is strictly positive, and the final sum is zero.
These are primitive Dyck excursions, and there are `Cat_(k-1)` such words.
Each has probability

`(M-d)_k (M)_k/(2M-d)_(2k)`.

On every selected word, `H=1+partial_sum` is at least two at all proper
intermediate times and returns to one at time `2k`.  Hence no intermediate
set is balanced, and the next balanced visit occurs exactly `2k` steps later.
The room condition ensures no block can exhaust even if every consumption
falls in one block.  This proves (4.1); (4.2) is direct sampling without
replacement.  The all-minus case is symmetric.

For fixed `d` and `k=o(sqrt(M))`, falling-factorial expansion and the Catalan
asymptotic give

`Cat_(k-1) (M-d)_k (M)_k/(2M-d)_(2k)
  = (1+o(1)) Cat_(k-1)/4^k
  = Theta(k^(-3/2)).`                                 (4.3)

Taking `k=Theta(log M)` yields a lower bound
`Omega_d((log M)^(-3/2))`, far larger than `1/M`.  In particular, no
posterior potential can validly imply the withdrawn `O(log m)` return bound
with per-scale failure `O(1/m)` for this unchanged process: the claimed
conclusion itself is false.

The estimate is uniform when `d=d(M)` ranges over `2<=d<=D` for a fixed
`D`: the falling-factorial error is `O_D((k+k^2)/M)`, the room condition
holds for logarithmic `k`, and `Pr[E_d]` is bounded below by a positive
constant depending only on `D`.

The exact checker supplies two finite witnesses:

* `d=2,n=20,k=4`: conditional probability `175/7293`; including the initial
  same-sign event, an eight-step first gap occurs with probability at least
  `525/46189`;
* `d=3,n=120,k=4`: conditional probability `50445/2500238`.

These are finite diagnostic certificates, not asymptotic evidence standing
in for the derivation.

## 5. A separate residual-transition error and a bounded repair

Even if the withdrawn A and block-concentration claims were granted, the
posted multiscale transition has a second mismatch.  Section 8 denotes the
current effective size by `m'_j` and the residual segment by `m_{j+1}`.  Its
block-deviation step supplies only an **upper** bound

`m_{j+1} <= 4 sqrt(m'_j log m'_j) <= (m'_j)^(2/3)`.

The subsequent H1 calculation uses

`log m'_j <= (3/2) log m_{j+1}+1`,

which would require a **lower** bound of the form
`m_{j+1} >= (m'_j)^(2/3)/2`.  Nothing preceding supplies it.  An upper bound
on `|D(T)|` permits a residual anywhere from zero upward.  Residuals satisfying
`M_0 <= m_{j+1} << (m'_j)^(2/3)` therefore fall into the recursive case while
the asserted descent budget can exceed what H1 justifies.

This is classified as `ERROR IN ARGUMENT`, not as a refutation of every
conditional multiscale theorem.

### Proposition 5.1 (variable-threshold reserve lemma)

At a scale of size `m`, suppose some independently proved good event gives:

* a tail after the last balanced visit of at most `g(m)` points;
* a residual segment of size `r <= m^alpha`, for fixed `alpha<1`; and
* a descent to a balanced visit after consuming at most `d(m)` residual
  points, whenever descent is attempted.

Fix a constant base reserve `b`.  Use the rule

* if `r < 2(d(m)+b)`, absorb the tail and the whole residual; and
* otherwise, descend and recurse.

Then:

1. the absorption gap has size less than
   `g(m)+2d(m)+2b`;
2. in the recursive case the unconsumed next-scale population is at least
   `r-d(m) >= r/2` and at least `b`; and
3. the next segment still has size `r <= m^alpha`.

The proof is the two displayed inequalities.  If `g(m),d(m)=O(log m)`, both
transition types require only `O(log m)` direct gap filling.  This repairs the
lower-bound mismatch without inventing one.

**Limits.** Proposition 5.1 assumes A and the residual upper bound; it proves
neither. It repairs only the numerical reserve inequality. A full transition
still requires balanced-band endpoints, an operational descent, a rule for
odd residuals, next-scale hypotheses uniform over partially consumed starts,
and consistent segment/effective-size bookkeeping. The local gap budget must
also be enlarged: substituting the withdrawn manuscript's displayed
`g(m)=28 log m`, `d(m)=8+32 log m`, and `b=350` gives a bound below
`92 log m+716`, not the original `60 log m+700`. For the unchanged steering
process, Proposition 4.1 prevents using the posted logarithmic `g,d` claims.
The proposition is therefore a bounded B diagnostic, not a survivor
construction or a complete transition repair.

## 6. Bounded polynomial total-accounting lemma

### Proposition 6.1 (geometric-log accounting)

Fix constants `0<alpha<1` and `b,c>=0`.  Consider recursive executions with
segment sizes

`m_0=n`, `m_{j+1} <= m_j^alpha`,

stopping at a fixed constant size. Suppose that, globally over all colorings,
tie histories, and executions at a scale of size `m_j`:

* the residual/nesting object, including the segment identity, has at most
  `m_j^b` possible descriptions; and
* after that object is fixed, every reachable local subset belongs to one
  fixed coloring-independent family of at most `m_j^c` distinct subsets.

Let the final set system contain the union of local subsets over **all** valid
executions.  Then, counting execution descriptions as an upper bound on
distinct unions,

`|S_n| <= (J_max+1) n^((b+c)/(1-alpha))`,              (6.1)

where `J_max=O(log log n)`.  In particular `|S_n|=n^O(1)`.

### Proof

For a fixed depth and nesting, the number of pattern/description tuples is at
most

`product_j m_j^(b+c)`.

Since `log m_j <= alpha^j log n`, this product is at most

`exp((b+c) sum_j log m_j)
 <= exp((b+c) log n sum_j alpha^j)
 = n^((b+c)/(1-alpha)).`

Summing over the `O(log log n)` possible depths gives (6.1), with the harmless
depth factor absorbable into one additional power of `n` if desired.  This
counts descriptions, so collisions between descriptions only reduce the
number of distinct subsets.

If this fixed family succeeds for an `epsilon>=n^{-q}` fraction of uniform
balanced colorings, FLSY Lemma 2.3 then adds at most `O(n/epsilon)` permuted
copies.  The **worst-case** family therefore still has at most

`O((n/epsilon)(J_max+1)n^((b+c)/(1-alpha))) = n^O(1)`

distinct subsets.  This last multiplication is conditional on noticeable
average success; Proposition 6.1 does not establish that probability.

For `alpha=2/3`, this recovers the sound accounting idea behind TR26-043
Lemma 7.5. A branching extension to several recursive residual intervals does
not follow from a fixed branching factor alone: it additionally needs the
children to form one jointly described next-scale object on a single nested
path, or a proved aggregate contraction such as contraction of total
logarithmic size. Without that condition, branching can destroy the geometric
series used here.

**Status and limit.** This is a reconstruction/generalization of known
bookkeeping, not a novelty claim.  It is a complete C endpoint conditional on
the stated local and shrink hypotheses.  It says nothing about the probability
that A/B-good executions exist. Per-execution polynomial descriptions would
not suffice: their union over colorings or histories could be exponential.

## 7. Repair family I: posterior-state potentials

### Candidate PS-1

Keep the two-block steering rule but augment the potential by pool counts,
frontier signs, and block orientation.

| Obligation | Verdict | Exact reason |
|---|---|---|
| A | **FAIL** | Equation (3.1) gives upward probability tending to `1/2`; Proposition 4.1 falsifies the needed exponential/logarithmic return tail. |
| B | **FAIL / no replacement proof** | Equation (3.2) falsifies the zero-drift load martingale.  A harmonic corrector may exist for a finite posterior Markov chain, but no bounded-increment concentration result controlling the exhaustion residual was derived. |
| C | **CONDITIONAL PASS** | For fixed `d`, prefix positions and `O(1)` cached signs give polynomially many state summaries.  If gaps were `O(log m)` and residuals power-shrank, Proposition 6.1 would give polynomial total subsets. |

The key distinction is between a potential being measurable and it proving the
desired event.  Posterior augmentation fixes the first issue only.  It cannot
prove a return tail contradicted by Proposition 4.1.

**Retry condition:** change the transition rule so a bad cached frontier does
not persist, or construct a polynomial universal gap cover that tolerates the
certified heavy tail.  A new actual-filtration residual concentration theorem
is independently required.

## 8. Repair family II: nonadaptive/fresh exposure

Two natural concrete versions fail for complementary reasons.

### Candidate NA-1: choose one fresh point, defer the rest

At each round expose a disjoint fresh `d`-tuple, consume a best point, and
permanently defer the other `d-1` points.

**A fails after conditioning.**  The first-round all-bad probability has the
desired hypergeometric form, but observed deferred signs alter the posterior
of the unseen reservoir.  There is a reachable `n=10,d=2` history:

* expose batch signs `(+,-),(-,-),(+,-)`;
* at heights `0,1,0`, consume signs `+,-,+`, each a legal minimizer; and
* defer `-,-,-`.

The current imbalance is `H=1`.  The four unseen signs are `+,+,+,-`, so the
next fresh pair is all bad with probability

`binom(3,2)/binom(4,2)=1/2>1/4`.

Thus deleting revealed values from the active reservoir does not preserve the
claimed conditional bias.

**B fails deterministically.** After `T` rounds, exactly `(d-1)T` exposed
points are deferred.  Linear progress creates a linear residual.

**C fails for the randomized-tie version.**  On a coloring whose first `T`
batches are monochromatic, every one of the `d` points is a tie choice in each
round.  Across tie histories, `d^T` different chosen subsets are reachable.
The coloring can be completed to a balanced coloring when the ambient set is
large enough.  For `d=3,T=8`, the finite counts are residual `16` and `6561`
chosen subsets.

**Retry condition:** give one explicit rule that consumes or recycles every
exposed point while preserving actual conditional exchangeability, a
sublinear residual, and polynomial reachable subsets.  Treating known signs
as if they were hidden is invalid.

### Candidate NA-2: consume every fixed batch

Partition a fixed order into batches of constant size `d`, inspect a batch,
and consume all of it in the best internal order.

| Obligation | Verdict | Exact reason |
|---|---|---|
| A | **constant-drift claim FALSE; return control UNKNOWN** | Batch-end imbalance is independent of the internal order.  Given current `H` and remaining pool size `R`, the expected batch sum is exactly `-dH/R`, only the weak bridge drift. |
| B | **PASS** | No points are deferred; the within-batch remainder is less than `d`. |
| C | **PASS for fixed d** | Complete-batch prefixes plus all within-batch subsets give at most `(ceil(n/d)+1)2^d` distinct sets. |

More precisely, the displayed identity **falsifies the proposed constant-
negative-drift repair**.  It does not by itself prove that no other return
theorem could ever be obtained for this batch process; no such replacement
return theorem is supplied here.  The candidate is rejected because A is not
established.  This cleanly demonstrates why B+C without A is insufficient:
internal reordering cannot change the sum at batch boundaries.

**Retry condition:** add a mechanism that changes batch-end sums without
deferral or exponential state branching; internal permutation alone cannot.

## 9. Repair family III: `d`-block steering for `d>2`

### Candidate DB-d

Use `d` ordered equal blocks, inspect every active frontier, consume one
minimizing absolute imbalance, and break complete ties uniformly.

| Obligation | Verdict | Exact reason |
|---|---|---|
| A | **FAIL for every fixed d** | Equations (3.1) and (4.1): after a same-sign exposure, `d-1` bad frontiers are cached and only one fresh sign remains.  The up probability tends to `1/2`, with a polynomial return tail. |
| B | **FAIL for the proposed martingale route** | Equation (3.2) gives a nonzero conditional load-deviation drift.  No substitute concentration theorem is supplied. |
| C | **TRADEOFF** | The full local prefix grid has `(m/d+1)^d` sets before gap filling.  It is polynomial for fixed `d`, and Proposition 6.1 would finish C under hypothetical A/B.  Any `d=d(m)->infinity` makes this full-grid template non-polynomial with no fixed exponent. |

The advertised reduction from roughly `1/4` to `1/2^d` is an unconditional
first-exposure calculation, not an iterated conditional statement.  More
blocks increase the number of cached bad frontiers but still expose only one
new sign after each single-element step.

**Retry condition:** either consume enough frontiers per round to eliminate
the cache while retaining steering at batch endpoints, or prove a genuinely
different actual-filtration process.  A load-concentration proof and, for
growing `d`, a compressed subset family are also mandatory.

## 10. Repair family IV: longer-horizon domination

### Candidate LH-1

Retain the cached-frontier process but compare `L`-step excursions with a
constant-negatively-biased birth-death chain.

**A fails.** Proposition 4.1 gives polynomial survival at low height, whereas
the return tail of every fixed-bias birth-death chain is exponential.  The
failure is not confined to one-step drift.  Away from the boundary, suppose
`d-1` bad frontiers are cached, the pool size is `R`, and `h>L`, so even `L`
correcting steps cannot hit zero.  The unseen population has size `R-d+1` and
signed sum `-(h+d-1)`.  Sampling without replacement gives the exact raw
`L`-step drift

`E[H_{t+L}-H_t | G_t]
   = -L(h+d-1)/(R-d+1).`                               (10.1)

For `h>L` with `L,h=O(log R)`, (10.1) is `o(1)`, not a constant negative
drift.  This exact formula is used only before a possible return; no
extrapolation across the stopping boundary is intended.

**B is not established.** Grouping steps into horizons does not change the
load drift (3.2), and no subpower exhaustion residual follows.

**C has a sharp direct-filling boundary.** Directly including all subsets of
an `L`-step gap costs `2^L`, hence is polynomial only for `L=O(log R)`.  At
that polynomial-accounting horizon A is already falsified by Proposition
4.1.  For a no-return window where (10.1) applies, obtaining constant raw
drift requires `L=Omega(R/(h+d))`; whenever this exceeds logarithmic size,
direct filling is superpolynomial.  Invoking an unknown polynomial
balanced-chain cover recursively for a long gap would be circular with O01.
This is not a proof that every conceivable compressed long-gap family fails;
it rejects the direct-subset implementation.

**Retry condition:** use a reference process with the correct
hypergeometric/bridge tail, not a fixed-bias chain, and independently give a
polynomial-size universal cover for its long excursions.

## 11. Repair family V: deterministic recursive covers

### Candidate DR-1: polynomially many fixed orders with power-size gaps

Fix constants `C,K>0` and `0<alpha<1`, and choose a list of at most `n^C`
permutations independently of the coloring. For each order, use its
zero-to-zero intervals and recursively fill them, aiming for every gap to
have size at most `K n^alpha`.

For a single fixed order and a uniformly random balanced coloring, the sign
sequence is a uniform bridge of length `n=2q`. Set

`a_q=max{q^(2/3),(K/2)(2q)^alpha}`.

The desired event is contained in the event that the longest excursion is at
most `2a_q`. FLSY Lemma 3.2 therefore bounds its probability by

`C_2 exp(-c q^delta)`, where `delta=min{1/3,1-alpha}>0`

and `c=c(K,alpha)>0`. This formulation retains the fixed gap constant and
the source lemma's `a>=q^(2/3)` threshold, including `alpha=2/3`. A union bound over
polynomially many fixed orders is still less than one for large `q`, so some
balanced coloring defeats all of them.

| Obligation | Verdict | Exact reason |
|---|---|---|
| A | **FAIL** | The primary-source random-bridge estimate makes power-size maximum gaps exponentially rare for each fixed order; polynomially many orders do not cover all colorings. |
| B | **PASS only on the rare good event** | Every recursive residual is at most `O(n^alpha)` by the event's definition. |
| C | **CONDITIONAL PASS for a polynomial list** | Raw prefixes number at most `T(n)(n+1)`; with polynomial local recursion data, Proposition 6.1 controls total sets.  This does not compensate for false A. |

Quantitatively, the union bound requires
`exp(Omega(n^delta))` order descriptions, where
`delta=min{1/3,1-alpha}`. It does **not** by
itself prove exponentially many distinct subsets: exponentially many chains
can share a small set system.  Any such shared-state compression must be
counted directly rather than charged per order; constructing it is precisely
the unresolved difficulty, so no stronger C obstruction is claimed here.

**Retry condition:** replace the polynomial fixed-order list with a shared
subset DAG whose coverage and distinct-set count are both proved.  The FLSY
estimate rules out only this fixed-order recursion template, not arbitrary
deterministic set systems and not O01.

## 12. Consolidated A/B/C matrix

| Candidate | A: actual filtration | B: residual/block | C: total subsets | Disposition |
|---|---:|---:|---:|---|
| PS-1 posterior potential, same process | **FAIL** | **FAIL / open substitute** | conditional pass | reject |
| NA-1 expose one/defer rest | **FAIL** | **FAIL** | **FAIL** | reject |
| NA-2 consume fixed batches | constant-drift repair fails; no return theorem | pass | pass | reject |
| DB-d, fixed `d>2` | **FAIL** | **FAIL / open substitute** | conditional pass | reject |
| LH-1 fixed/log horizon | **FAIL** | not established | fails at useful large horizon | reject |
| DR-1 polynomial fixed orders | **FAIL** | rare-event pass | conditional pass | reject |
| B-RESERVE variable threshold | assumed | **conditional reserve pass** | compatible | bounded diagnostic only; transition incomplete |
| C-ACCOUNTING geometric-log lemma | not supplied | assumed shrink | **pass** | bounded diagnostic only |

No A-only or A/B-only proposal is promoted.  In particular, polynomial state
counting does not rehabilitate a false return theorem, and an adaptive path
does not count as a construction until all possible subsets are bounded.

## 13. Reproducible artifacts

Run:

```powershell
python research_cycle_02/experiments/check_proof_sat_repairs.py
```

The checker uses exact rational arithmetic and independently brute-counts
Dyck words for `k<=7`.  It verifies the finite probabilities, the reachable
fresh-pair history, every integer branch of a representative variable-threshold
instance, and the geometric-log inequality.

Artifacts:

* `research_cycle_02/experiments/check_proof_sat_repairs.py`;
* `research_cycle_02/certificates/proof_sat_repair_diagnostics.json`; and
* `research_cycle_02/proof_sat_repair_failures.jsonl`.

The JSONL file is track-local and ready for root-level review/append.  It has
not been appended to any canonical global failure ledger.

## 14. Recommended next retry

Do not spend another cycle searching for a more elaborate potential whose
goal is the **posted `O(log m)` gap bound with `O(1/m)` failure** for the
unchanged single-consumption frontier process: Proposition 4.1 falsifies that
conclusion, not just the posted proof.  A quantitatively weaker return theorem
paired with a genuinely new compressed gap cover is not ruled out.

The narrowest legitimate positive retry is:

> Design a round that consumes/reconciles **all** revealed frontiers, changes
> the batch-end imbalance distribution (unlike NA-2), and has a fixed-
> polynomial family of within-round and cross-round subsets.  Before any tail
> analysis, freeze its actual filtration and prove A, B, and C separately.

If no such round is found, the most reusable negative next step is to formalize
Proposition 4.1 and the fixed-order obstruction.  Neither direction should be
described as progress on unrestricted `N(n)` without an additional theorem.

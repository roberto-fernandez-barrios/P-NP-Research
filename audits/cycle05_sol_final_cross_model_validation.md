# Research Cycle 5: final independent cross-model hostile validation

**Audit branch:** `cycle05-sol-final-audit`
**Candidate branch/commit audited:** `cycle05-fable` at
`18ba9cf4071f618113aa9657d847d44828c6da2d`
**Audit date:** 2026-08-26
**Scope:** Cycle 5 only; no continuation of the research program
**Validator posture:** every candidate claim was treated as false until
reconstructed

## 1. Executive disposition

The mathematical conclusions of Theorems A, E, SEG, C, and F survive this
audit.  The repaired precomposition version of Theorem A is sound as stated.
Theorem E is sound after three local quantifier/normalization corrections.
SEG is sound after exact local proof repairs, but the last arms-length report's
R3 is not a complete proof and its R4 argument is false in the case
`L = j^5 + 1`.  I give replacements below that preserve the frozen SEG
statement, `C = 6`, the advertised `c`, and the explicit `L_0`.  Theorems C
and F then follow after one floor correction in C and one scope correction in
Lemma RS.

The finite mathematical data are sound.  Independent exhaustive enumeration
places the first possible hybrid-only example at `n = 22`; all checked stored
witnesses have one switch.  The `n = 24` payload contains 14,864 stored
records but only 8,258 distinct `(permutation, word)` examples.  The excess
6,606 records are exactly duplicate `swap`/`xswap` labels.  Several current
summaries still call all 14,864 records examples or certificates and must be
corrected.

The Lean project builds cleanly and its coverage ledger correctly leaves the
literal `RR_n`, Theorems A/E/C/F, SEG, and all probability estimates outside
formal coverage.  The novelty ledger does not survive intact: FLSY Lemma 2.3
already uses literal unions of relabelled set systems, and standard
arc-permutation, greedoid/antimatroid, and regular-set-system vocabularies are
material prior-art neighborhoods omitted from the submitted search.  No
Cycle-5 item merits `NOVELTY-STRONGLY-SUPPORTED` on the present evidence.

No result here proves or suggests a resolution of P versus NP or O01.  O01
remains open.  Nothing was merged and no candidate theorem/proof file was
edited during this validation.

## 2. Independence and evidence protocol

I first reconstructed the definitions and theorem statements from the base
objects, then attacked the claims, and only afterward compared against the
submitted proofs and earlier verdicts.  The work was split into independent
proof, finite-computation, formal, and prior-art workstreams.  In particular:

- `enumerate_rr_failures.cpp` is a new literal implementation of the single
  `RR_n` interval recurrence and imports no Cycle-5 engine;
- `verify_finite_claims.py` independently reconstructs cyclic interval
  levels, relabelled failure sets, literal union reachability, witness
  nesting/balance, label-switch cost, and certificate hashes;
- the proof attacks independently recomputed the affine adjacency formula,
  the hull-chain reduction, all SEG constants, the two C/F substitutions,
  and the terminal cyclic split;
- the FLSY primary source was fetched from ECCC, hashed, and read directly;
- the Lean run began with `lake clean`, rebuilt the pinned dependency graph,
  ran the repository checker, and separately printed kernel axiom
  dependencies of every credited theorem family;
- the literature pass used alternative terminology, including feasible
  words, arc permutations, search antimatroids, regular set systems, and
  admissible permutations, rather than merely repeating the submitted
  queries.

The primary FLSY file used was the official ECCC full version, SHA-256
`56F91E2C658DC689DA9F543ACBAF8DD9E127D551CB1F915C76B49001FBA92A4A`:
[Fabris--Limaye--Srinivasan--Yehudayoff, ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/download/).
The proceedings version is
[LIPIcs CCC 2026, Article 22](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.CCC.2026.22).

## 3. Theorem A

### 3.1 Reconstruction before comparison

Let `n = 2m`, `q = n-1`, and
`U = Z_q union {infinity}`.  The literal family `RR_n` contains:

- `emptyset` and `U`;
- every finite singleton at rank 1;
- at rank `2 <= r <= n-1`, every set `{infinity} union I`, where `I` is a
  cyclic interval of `Z_q` of length `r-1`.

A relabelled copy is the literal image `pi(RR_n)`.  A list's family is the
deduplicated literal union, so copy provenance is not part of membership.
A balanced coloring is accepted exactly when the induced subset DAG contains
a maximal inclusion-by-one chain whose discrepancy has absolute value at
most one at every rank.  Pure acceptance means that one constituent contains
an entire accepting chain.  Hybrid-only acceptance means that the literal
union accepts while every constituent rejects.

For infinity-fixing copies, normalize `f(infinity) = -1`.  Removing
`infinity` converts a literal accepting chain to nested finite sets
`I_1 subset ... subset I_{q-1}`, one point added at each step, each a cyclic
interval in at least one copy.  Their finite sums are `1` at odd sizes and
`0` or `2` at even sizes.

The correct relative geometry follows without convention choices.  Pulling
the pair `(pi_i(RR_n), pi_j(RR_n))` back by `pi_i^{-1}` gives

```text
(RR_n, (pi_i^{-1} o pi_j)(RR_n)).
```

Thus the operative relative map is precomposition
`pi_i^{-1} o pi_j`.  The discarded postcomposition map
`pi_j o pi_i^{-1}` is a conjugate and need not preserve affine structure.
An affine map is `x |-> ax+b (mod q)` with `a` a unit.  Its cyclic intervals
are precisely arithmetic progressions with difference `a`; `b` only rotates
the image circle.

The frozen repaired theorem is therefore: for `q >= 7`, after merging
dihedrally identical circles, if every pairwise precomposition relative map
is affine with multiplier not `+1` or `-1`, every accepted coloring has a
pure accepting chain, and consequently `G(P)=0`.

### 3.2 Hostile proof check

Put `h = a^{-1} mod q`, represented in `{1,...,q-1}`.  A size-`s`
difference-`a` progression has exactly

```text
max(0, s-h) + max(0, s-(q-h))
```

ordinary cyclic adjacencies.  Equating this with the `s-1` adjacencies of a
proper ordinary interval proves that, for `2 <= s <= q-2`, a progression is
not also an ordinary interval unless `a = +/-1`.  This calculation does not
use primality of `q`.

For a cross pair `A subset A union {y}` in opposite circles, compare the
ordinary adjacency components with the step-`h` graph in progression-index
space.  In the ordinary-to-affine direction, the only noninterval shape
capable of losing one point is a component pair of sizes `(s-1,1)`; the
index-step equation forces the lower boundary `|A| <= 2`, and complementation
gives `|A| >= q-3`.  In the reverse direction, deleting one point from an
ordinary interval yields either one run or two runs.  Equating its adjacency
count with the progression formula again leaves only those boundary sizes,
including the `a = +/-(q+1)/2` boundary cases.  Hence:

- there are no nontrivial common intervals at sizes `2,...,q-2`;
- there are no cross steps starting at sizes `3,...,q-4`.

Any accepted chain therefore has one owner throughout sizes `3,...,q-3`.
The two boundary repairs are complete: a compatible three-point interval has
sign multiset `{+,+,-}` and contains an adjacent bichromatic pair, while the
complementary three-point interval at the upper end has a majority-sign
endpoint that extends the chain compatibly to a co-singleton.  Replacing the
two bottom and two top states creates a pure chain in the middle owner.

I found no missing common interval, cross pair, rank-boundary case, or
multi-copy interaction.  Pairwise uniqueness after dihedral duplicates are
merged is sufficient for an arbitrary list length `t`.

### 3.3 Falsification attempts

Independent exact checks covered every odd `q` from 7 through 51 and every
unit multiplier other than `+/-1`: 490 multiplier cases had no forbidden
common interval or middle cross step.  Nonvacuous coloring checks found zero
affine-union rescues at `q=21` and `q=23`; at `q=27,a=2`, 54 common rejected
words were found and none was rescued.  Offsets require no new case because
they do not change the image interval family.

The old postcomposition theorem is genuinely false.  A fresh `n=24`
conjugated-affine construction and the stored `n=22` word `0xae2b3` both
have affine `pi_2 o pi_1^{-1}`, nonaffine
`pi_1^{-1} o pi_2`, rejection by both copies, and literal-union acceptance.
The `n=22` case was rerun through a separately written literal subset DAG.
Both copies fix infinity, so this is exactly the composition defect rather
than an infinity-moving edge case.

The stated infinity-fixing scope is correct.  A common moved anchor can be
globally relabelled back to infinity, but lists with different moved anchors
remain outside the theorem.

**Theorem-A disposition:** the repaired precomposition theorem is sound as
stated.  The old postcomposition statement must remain recorded as false.

## 4. Theorem E

### 4.1 Reconstructed statement and reduction

For a reference cyclic order `O*`, an `O*`-hull of `S` is a smallest
`O*`-interval containing it, and the hull defect is
`|hull(S) setminus S|`.  A circle is `d`-dense relative to `O*` when every
one of its intervals has defect at most `d`.  Theorem E quantifies over all
sufficiently large even `n`, every finite list length `t`, and any
infinity-fixing list whose circles share one such reference, under

```text
6d + 8 < (n-2)^(1/5).
```

Its conclusion is

```text
H(P) <= (n/2) 2^(-c (n-2)^(1/5)).
```

Because defect is integer-valued, set `D=floor(d)` if the statement permits
real `d`; equivalently state the theorem for integer `d`.  Let
`j* = q-2D-2`.  For an accepting chain `I_j`, a minimum reference hull is
the complement of a largest gap.  Through `j*`, the largest gap is unique.
The elementary two-gap inequality also proves that successive unique hulls
are nested.  Thus the `H_j=hull(I_j)` form a nested rooted chain with
`j <= |H_j| <= j+D` and `|f(H_j)| <= D+2`.

Refining each hull jump one endpoint at a time costs at most `D+1` and gives
imbalance at most `2D+3`.  Completing the final at most `2D+2` points gives
a maximal rooted cyclic-interval chain with imbalance at most `3D+4`.
Complementing and cutting at its plus root yields a maximal ordinary
interval chain on `N=n-2` points with imbalance at most
`k=3D+5`.

Condition on the chosen root being plus.  Its complement coloring is
uniformly balanced on those `N` points.  The published FLSY Theorem 4.4,
applied with the actual integer `k<N^(1/5)`, bounds the bad event.  Summing
the root probability over all roots gives exactly the factor `n/2`.

### 4.2 Quantifiers and attacks

The argument never enumerates or union-bounds over copies.  It processes the
single accepting chain and uses only that whichever copy owns a state is
dense relative to the same `O*`.  The conclusion is therefore genuinely
independent of `t`, even for arbitrarily large finite lists.

The displayed density inequality is stronger than needed for the final
FLSY parameter: `6D+8<N^(1/5)` implies `3D+5<N^(1/5)` once the already
required sufficiently-large regime is reached.  The theorem explicitly
retains FLSY's sufficiently-large-`N` hypothesis; the numerical inequality
alone is not being used to erase that hypothesis.  `N=n-2` is even, as
required by FLSY.

An attempted counterfamily in which every accepted state has defect at most
`d`, with the number of available circles growing arbitrarily with `n`, is
still mapped deterministically into the same rooted FLSY bad event.  It
cannot violate the conclusion without violating the published theorem or
one of the checked elementary hull steps.  No such failure was found.

### 4.3 Required local repairs

- `dense_circle_obstruction.md:16` calls the imported parameter `k=O(1)`.
  Here `d` may grow, so it must say `k=3D+5<N^(1/5)` and cite the uniform
  `k<N^(1/5)` range of FLSY.
- `dense_circle_obstruction.md:22-23` says a global relabel makes
  `O*=O_1=id`.  A reference need not be one of the listed circles.  The
  correct normalization is only `O*=id`, unless membership in the list is
  separately assumed.
- `dense_circle_obstruction.md:34` must quantify `d` as a nonnegative
  integer or introduce `D=floor(d)` before `j*` and all chain indices.
- `flsy_reconstruction.md:79-81` should record a harmless strictness slip in
  the source proof display: retain the theorem's actual integer
  `k<N^(1/5)` instead of enlarging to `cbal<=N^(1/5)` at perfect fifth
  powers.  The published theorem statement and Theorem E are unchanged.

No repair changes the theorem's conclusion, exponent, uniformity in `t`, or
density threshold.

## 5. Lemma SEG and FLSY localization

### 5.1 Frozen statement

There are universal constants `c>0`, `C>0`, and `L_0` such that, for every
`N`; every admissible integer total `sigma` with `|sigma|<=1` and
`sigma congruent N (mod 2)`; a uniformly random sign function conditioned
on total `sigma`; fixed linear intervals
`emptyset != A subseteq B subseteq [N]`; `L=|B setminus A|>=L_0`; and every
integer `1<=k<L^(1/5)`,

```text
Pr[there is A=D_0 subset ... subset D_L=B,
   one point added at each step, every D_i an interval,
   and |f(D_i)|<=k for all i]
 <= C sqrt(N) exp(-c L^(1/5)).
```

For an unconditioned random coloring the `sqrt(N)` factor is absent.  If
`B` is not fixed but only its added length is fixed, the cost is at most
`L+1`.  A proper cyclic `B` reduces verbatim by cutting outside `B`; for
`B=Z_N`, `A` nonempty, another `L+1` factor suffices.  The relative form
`|f(D_i)-f(A)|<=k` has offset zero.  There is no large-`N` hypothesis beyond
existence of the intervals; the asymptotic regime is `L>=L_0`.

Valid explicit witnesses after the repairs are

```text
c = min(1/2, (1/6)^2 / (8*27648^2))
  = 4.542344518777...e-12,
C = 6,
L_0 = ceil(13824^(5/2)) = 22,469,029,418.
```

At this `L_0`, both `L^(2/5)>=13824` and
`L^(1/5)>=(2/3) ln L` hold and remain monotone in the needed direction.

### 5.2 What is and is not published

FLSY publishes the discrete Frechet definition, the global interval-chain
reduction, the zero-offset two-walk anti-concentration lemma, the
first-passage and milestone lemmas, and Theorem 4.4.  It does **not** state a
fixed `A`-to-`B` segment theorem, a nonzero-offset anti-concentration lemma,
the full cyclic endpoint case, or these explicit constants and rounding
conventions.

SEG is therefore not `PUBLISHED VERBATIM`.  It is a new repository
derivation using published probabilistic machinery.  Its grid normal form,
offset lemma, cyclic-full reduction, and exact bookkeeping require proof in
this repository.  The corrected proof below supplies that proof; citation
substitution alone would not.

### 5.3 Localization and independence audit

For fixed linear `A=[a_1,a_2] subseteq B=[b_1,b_2]`, every intermediate
interval is determined by how many points are added from the disjoint left
and right arcs of `B setminus A`.  A chain is a monotone grid staircase.  Its
running sum is `f(A)` plus two fresh partial-sum walks after global balance is
removed.

Global balance is used once, through the pointwise bound

```text
Pr[E | total=sigma] <= 3 sqrt(N) Pr[E].
```

Under the unconditioned measure, the coordinates in `A`, the left arc, and
the right arc are independent.  Conditioning on `f(A)=sigma'` changes only
one starting offset.  Milestones use only increments of the longer walk;
absolute position disappears by translation.  At each stopping time the
target direction is history-measurable, reflection makes the two directions
equidistributed, and strong Markov supplies independent identically
distributed first-passage legs.  Neither earlier nor future chain history,
nor `f(B)`, is conditioned upon.  Cyclic cutting is a deterministic
relabeling.  Parity is confined to the ambient conditioned measure and the
usual parity support of integer first-passage times.

No hidden dependence on the global starting value, total balance, past,
future, absolute location, chain endpoints, or an unpriced conditioning was
found.

### 5.4 R1 -- first offset leg

Let `d=L^(1/5)`, `Delta=3d`, `z_0=M(0)`, `h_0=H(0)`, and let `z_1` be the
first milestone of `M`.  The conditioned offset satisfies
`|z_0-h_0|=|sigma'|<=k<d` (the proof only needs `<=d`).  The milestone gap is
at least `ceil(3d)`.  Hence

```text
|z_1-h_0| >= ceil(3d)-|sigma'| >= 2d > d.
```

The chaser cannot already be within the `d`-ball at time zero, so the
extracted first chaser time `b_1` is at least one and the stopping time
`tau_1<=b_1` is legitimate.  Every later leg begins within `d` of the prior
milestone by the definition of `tau_{i-1}`, so the same invariant applies;
there is no second hidden base case.  With integer rounding as in R3, each
leg must traverse at least `ceil(d)`, so domination by the required
first-passage variable follows.  R1 is valid.

### 5.5 R2 -- tail arithmetic

Write `ell>=L/2`, `Delta=3d`, `c_3=256`, and

```text
K=floor(ell/(c_3 Delta^3)),  x=d^2/13824.
```

The correct upper bound is `K<=L/(6912d^3)`, not the submitted
`L/(13824d^3)`.  For the lower bound there are exactly two cases:

- if `13824<=d^2<27648`, then `K>=1`, so
  `Kd>=d>=d^3/27648`;
- if `d^2>=27648`, then `x>=2` and
  `K>=floor(x)>=x/2`, giving the same inequality.

There is no uncovered interval.  Therefore

```text
(Kd)^2/(16(L/2)) >= L^(1/5)/(8*27648^2).
```

R2's repaired conclusion and final exponent are valid.

### 5.6 R3 -- integrality

The arms-length R3 discussion is incomplete: the submitted proof continues
to write `F_d` although `d=L^(1/5)` is generally real, and its treatment of
the real Chernoff threshold relies partly on measured slack.  Exact constants
cannot be justified by simulation.

A complete replacement is as follows.

1. For integer `a>=1` and real `t>=4a^2`, reflection expresses
   `Pr[F_a>=t]` as exactly `a` parity-compatible binomial masses in
   `[-a,a)`, at time `ceil(t)-1`.  The central mode is at least
   `1/(2sqrt(n))`, and the relevant mass-to-mode product ratio is at least
   `7/8`.  The usual mode upper bound gives, uniformly,

   ```text
   a/(6sqrt(t)) <= Pr[F_a>=t] <= 1.85a/sqrt(t).
   ```

2. Keep real `Delta=3d`, define milestone exit at integer level
   `ceil(Delta)`, and use `floor(Delta)` independent blocks of
   `floor(256Delta^2)` steps.  Failure to exit implies that each fresh block
   misses `ceil(2Delta)`.  The upper first-passage bound makes each block's
   failure probability less than `0.30` for `Delta>=2`, and
   `0.30^floor(Delta)<=2^-Delta` for `Delta>=3`.  Every nonvacuous SEG
   instance is far inside this range.

3. In the offset lemma take the integer first-passage level
   `delta=ceil(d)`.  Since walk values are integral and the tracking radius
   is at most `floor(d)`,

   ```text
   ceil(3d)-2floor(d) >= ceil(d)=delta.
   ```

   This includes the first leg after R1.

4. Since `delta<=2d`,
   `K delta^2<=L/(1728d)<=L/2`.  Also `K delta>=Kd`, so R2's exponent is
   unchanged.  The real first-passage estimate applies directly to the real
   threshold `t*` in the Chernoff argument.

This is a proof, not an appeal to asymptotic `O(1)` loss.  It preserves the
advertised `1/6`, `27648`, `c`, and `L_0`.

### 5.7 R4 -- cyclic `B=Z_N`

R4 in the final arms-length report is false as written.  From integer
`k<L^(1/5)` one gets only `k<=(L-1)^(1/5)`.  Equality is possible when

```text
L-1=j^5, i.e. L=j^5+1,
```

not when `L=j^5`.  Non-strict offset control cannot turn a Frechet event at
distance `<=j` into the strict event `<j`.

The failed proof inclusion has a concrete witness: take cyclic `N=34`,
`A={0}`, `L=33=2^5+1`, `k=2`, and grow one-sided with increments

```text
+,-,-,(+,-)^15.
```

All chain sums lie in `{0,1,2}`, but after dropping the terminal point the
length-32 one-sided Frechet distance is exactly 2, not `<32^(1/5)`.

The SEG statement is nevertheless repaired locally.  For each terminal
split `u+v=L-1`, assign the final remaining point to the end of the left
extension sequence.  The two coordinate sequences are still disjoint and
now have total length `(u+1)+v=L`.  The actual cyclic chain supplies a
staircase that postpones that final left step to its endpoint.  Apply the
offset lemma at length `L`, then union over the `L` terminal splits.  This
uses the original strict `k<L^(1/5)` hypothesis and preserves the
`(L+1)` factor and every constant.  This replacement, not the submitted
perfect-fifth sentence, is required.

### 5.8 R5 -- final constant

The unconditioned offset estimate contributes
`2exp(-cL^(1/5))`; unconditioning contributes at most `3sqrt(N)`.  The
product is `6sqrt(N)exp(-cL^(1/5))`.  Thus `C=6`.  The declaration `C:=3` in
`cycle05_seg_deep_independent_validation.md:373` contradicts its own
displayed bound and must be changed.  R5 is valid.

**SEG disposition:** the frozen statement is sound with the exact R1--R5
repairs above.  It is an unformalized, adversarially reviewed repository
proof candidate, not a theorem published verbatim by FLSY.

## 6. Theorems C and F

### 6.1 Theorem C

There are `q-5` middle states.  If a chain has at most `D` middle switches,
put `h=D+1`.  One pure block has at least `ceil((q-5)/h)` states and hence at
least

```text
M = floor((q-7)/h)
```

additions.  The current proof's claim that it has at least the real number
`L*=(q-7)/h` additions is false when `L*` is nonintegral.  For `L*>=2`,
`M>=L*/2`, so replacing `c` by `c/2^(1/5)` preserves the displayed form.

The SEG substitution is otherwise exact:

- ambient length `N=q` and conditioned total `sigma=+1`, with matching odd
  parity;
- `k=2`, not the growing `k` used elsewhere in F;
- a proper cyclic endpoint because the run stays within sizes
  `3,...,q-3`;
- segment length `M`, eventually exceeding `L_0` and satisfying
  `2<M^(1/5)`;
- at most a polynomial endpoint/order budget.  The displayed
  `t q^4 O(sqrt(q))` prefactor has slack.

The theorem follows with the floor correction and with `D_mid` given the
precise arbitrary-`t` definition in section 8 below.

### 6.2 Theorem F

The two branches are distinct and were checked separately.  Set
`L=floor(n^(1/5)/7)`.

In the long-run branch, a pure run supplies a proper cyclic SEG segment with
`k=2` and added length at least `L`.  This gives
`poly(n) exp(-Omega(n^(1/25)))`.

In the short-run branch, Lemma RS must cover every finite chain state, not
only the stated middle states.  The same sandwich proves it.  A state in
copy 1 has zero copy-1 defect.  For a copy-2 state, take the first later
copy-1/common state or the universal co-singleton; the containing copy-1
interval is at most `L+2` additions away.  Prepend size 2 to the first
copy-2 middle run if necessary, use the co-singleton for size `q-2`, and
note that size 1 and size `q-1` are common.  Thus every finite state has
copy-1 defect at most `d=L+2`.

Apply the chain form of Theorem E, then the **published** FLSY Theorem 4.4
on `N=n-2` with

```text
k = 5+3d = 11+3 floor(n^(1/5)/7),
```

which is approximately `(3/7)n^(1/5)`.  This is not the `k=2` SEG
application.  For sufficiently large `n`, both
`6d+8<(n-2)^(1/5)` and `k<(n-2)^(1/5)` hold.  The density event is bounded
by `(n/2)2^(-c(n-2)^(1/5))`, which is stronger than the long-run rate.

After the SEG, floor, and RS repairs, C and F may move from “conditional on
an unproved SEG” to

```text
ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED
```

while retaining an explicit dependency on SEG.  They are not published or
formally verified theorems.

## 7. Hybrid-only minimality and finite certificates

### 7.1 Independent exhaustive enumeration

The new C++ enumerator visited every normalized balanced word and produced:

| `n` | words tested | `RR_n` rejects |
|---:|---:|---:|
| 2 | 1 | 0 |
| 4 | 3 | 0 |
| 6 | 10 | 0 |
| 8 | 35 | 0 |
| 10 | 126 | 0 |
| 12 | 462 | 0 |
| 14 | 1,716 | 0 |
| 16 | 6,435 | 0 |
| 18 | 24,310 | 0 |
| 20 | 92,378 | 0 |
| 22 | 352,716 | 21 |
| 24 | 1,352,078 | 414 |

For even `n<22`, one copy accepts every balanced coloring.  Acceptance is
equivariant under every ground-set relabeling, including relabelings that
move infinity.  Therefore no coloring can be rejected by all constituents
of any list, and hybrid-only acceptance is impossible.  This establishes
minimality without assuming a particular second copy or search class.

At `n=22`, the committed canonical example was checked literally:
finite transposition `(1 13)`, normalized word `0x1fe0e`, rejection by both
copies, acceptance by their union, and one-switch witness.  Existence at 22
and nonexistence below 22 are therefore both independently established.

### 7.2 Certificate audit

All five payloads named by `cycle05_hybrid_SHA256SUMS.txt` match their
committed hashes.  The independent verifier then obtained:

| payload | stored records | distinct `(permutation,word)` | duplicate excess | distinct permutations | distinct words |
|---|---:|---:|---:|---:|---:|
| `n=22` | 122 | 122 | 0 | 43 | 17 |
| `n=24` | 14,864 | 8,258 | 6,606 | 440 | 414 |

Every stored chain is nested, adds one point per step, belongs to at least
one stated circle at every level, and satisfies the exact parity-dependent
balance condition.  The stored pullback words and common-reject counts are
correct.  Every one of the 122 `n=22` records and all 14,864 `n=24` records
has a one-switch witness.  Since each is hybrid-only, a zero-switch witness
is impossible, so the minimum is exactly one.

At `n=24`, every duplicate key occurs twice and its two route labels are
exactly `swap` and `xswap`.  The distinct word projection is exactly the set
of all 414 independently enumerated `RR_24` failures.  Thus the corrected
claim is:

```text
14,864 verified stored records representing 8,258 distinct
(permutation, word) examples, with 6,606 duplicate swap/xswap records.
```

The infinity-moving probe records 550 tested candidates and 32 finds.  All
32 were rerun with a literal full-ground-set family and induced-subset-DAG
checker; each pair rejects individually and accepts in union.  This sample
proves existence outside the infinity-fixing setting but does not establish
an exhaustive count.

The complete `n=22` transposition profile was also rebuilt:

| cyclic distance `delta` | common rejects | rescued |
|---:|---:|---:|
| 1 | 17 | 0 |
| 2 | 13 | 0 |
| 3 | 9 | 0 |
| 4 | 7 | 0 |
| 5 | 5 | 0 |
| 6 | 7 | 0 |
| 7 | 9 | 0 |
| 8 | 11 | 0 |
| 9 | 11 | 2 |
| 10 | 11 | 4 |

The sharp observed threshold is 9, and the rescuing distances are exactly
`{9,10}`.  Current wording `delta>=8` is wrong.

### 7.3 Provenance limits

The `n=22` fields `min_switches` and `canonical` are correct, but the
committed search generator does not reproduce those annotations; the README
warns that rerunning it strips them.  Canonical provenance should either
include the annotation step or label it as a separately verified manual
postprocessing step.  The `n=24` file lacks those fields, so it is not the
“same schema.”  Independently recomputing the switch counts closes the
mathematical question, but not the reproducibility wording.

The structured `revB`, bit-reversal, and xor measurements in results section
6 do not have a committed construction driver.  They should be accompanied
by one or explicitly labelled as non-reproducible finite diagnostics.  This
does not affect A, E, SEG, C, F, minimality, or the stored certificates.

## 8. Switching chains and switch depth

The provenance-invariant label set `L(S)` is the correct basis.  A chain is
pure iff one label is available at every state.  Its switch count is the
minimum number of adjacent label changes over compatible label assignments;
zero switches is equivalent to purity.  A change occurs at a common state
or across a cross pair.  These facts are mathematically sound and the core
zero-switch equivalence is covered by Lean.

Two definition repairs are required:

1. `hybrid_definitions.md:55-67` first defines a partition into disjoint
   blocks and then discusses consecutive blocks “overlapping” at a state.
   Retain the unambiguous minimum-label-change definition, or use
   endpoint-sharing segments rather than a partition.
2. `switch_structure_theory.md:26-33` is ambiguous for `t>2`.  Define

   ```text
   r_mid(C) = min number of consecutive blocks partitioning [3,q-3]
              such that each block's states share at least one label,
   D_mid(P) = max_C (r_mid(C)-1).
   ```

   For two copies this is exactly alternation in the subsequence of
   singly-labelled middle states and exactly what the committed DP computes.
   It is also the quantity used by Theorem C's pigeonhole argument.

The finite DP data reproduce the advertised affine value zero and the
`q=13,17,21` transposition/pair-swap table.  Wider independent checks found
`D_mid<=1` for transpositions through odd `q=61` and pair-swap equality
through odd `q=101`; these are finite checks, not all-`q` proofs.

The all-`q` transposition `D_mid<=1` remains a proof candidate because the
submitted text gives only a case skeleton.  The pair-swap all-`q` lower bound
is proved, but its displayed witness omits its first alternation.  At
`switch_structure_theory.md:252-256`, prepend

```text
I_3={0,1,3}       (copy-2 only),
I_4={0,1,2,3}     (common),
```

before the four-step pattern.  This yields the claimed `(q-7)/2` lower
bound.  Equality remains certified only for the stated finite values; it is
not an all-`q` theorem.  The omission changes no lower-bound conclusion once
the two states are inserted.

## 9. Formal coverage

The formal project pins Lean `4.32.1`, mathlib tag `v4.32.1`, and resolved
mathlib commit `520045ab14e26149ee970e2e617ca04b09bde5d6`.  All inherited Lake
dependencies have resolved commits in `lake-manifest.json`.  A source scan
of `formal/BalancedChain.lean` found no `sorry`, `admit`, or user `axiom`.

A cold `lake clean` followed by `formal/check.ps1` used Lean `4.32.1`
(commit `f054605aea4b840552cca2e725580bffd1e1b704`) and Lake `5.0.0`, rebuilt
8,663 jobs successfully, and ended with the repository checker's `PASS`.
The build emitted only linter warnings.  A separate kernel audit compiled
`FormalAxiomAudit.lean` and printed the dependencies of all eleven credited
theorem families.  The union of those dependencies was exactly `propext`,
`Classical.choice`, and `Quot.sound`; there was no custom axiom.

The prose ledger in `formal/coverage.md` matches the source.  It credits the
generic deterministic balanced-chain definitions, relabeling and literal
union lemmas, consecutive-pair and contracted-path formulations, S1/S2, and
the generic multi-copy purity/switch layer.  It explicitly marks all of the
following unformalized:

- literal `RR_n` and the interval-walk reformulation;
- Theorems A, E, C, and F;
- SEG and RS/M;
- the hull/Frechet/random-walk probability estimates;
- finite optimum and certificate claims;
- O01.

No audited text implies that Lean proves any of those items.  The formal
coverage claim is therefore sound.

## 10. Independent novelty and prior-art sanity check

The submitted novelty statuses are search judgments, not mathematical
theorems.  The expanded terminology search changes them as follows:

| repository contribution | final classification | reason |
|---|---|---|
| N1, affine AP/cyclic-interval lemma | **UNCLEAR** | No exact source was found, but this is an elementary special case adjacent to mature simple/common-interval and arithmetic-permutation theory; folklore risk is high. |
| N2, repaired affine no-hybrid Theorem A | **POTENTIALLY-NOVEL** | Pure cyclic chains and feasible words are known, but no exact affine, balance-sensitive literal-union rigidity theorem was located. |
| N3, Theorem E hull-transfer mechanism | **POTENTIALLY-NOVEL** | Approximate/gapped common intervals are established, but no exact `t`-independent hull/refinement/rooted-FLSY transfer was located. |
| N4, switching framework as an aggregate | **UNCLEAR** | Extra maximal chains under a union and alternative feasible routes have direct prior art.  The narrow quantitative `D_mid` and run-sandwich inequality may be potentially novel. |
| N5, literal unions of relabelled interval/RR systems as balanced-chain objects | **KNOWN** | FLSY Definition 1.2 and Lemma 2.3 use literal unions of relabelled copies of an arbitrary set system.  Instantiating the base family with RR gives the object. |
| SEG localization | **UNCLEAR** | The probabilistic engine is known from FLSY; the exact localized statement was not found verbatim and is a proved repository adaptation, not a novelty-certified result. |

The decisive N5 source is FLSY Lemma 2.3.  It defines
`Y=X union union_i sigma_i(X)` and evaluates all maximal Boolean chains
contained in that literal set system.  Its proof chooses pure relabelled
chains and does not study hybrid provenance, so it does not subsume the
Cycle-5 structural results; it does make the underlying object and literal
union semantics published prior art.

There is also an explicit abstract extra-chain example in
[Algaba--van den Brink--Dietz, TI 15-007/II, Example 4.7, p. 23](https://papers.tinbergen.nl/15007.pdf):
the union of prefix states from three listed permutations contains a fourth
full chain not among the inputs.  It is not interval- or balance-specific,
but it is prior art for the broad “union creates a hybrid chain” mechanism.
The peer-reviewed article with the same title omits that example, so the
working paper, not merely its journal DOI, is the supporting source.

Other material primary/authoritative neighbors include:

- [Elizalde--Roichman, *Arc permutations*](https://doi.org/10.1007/s10801-013-0449-6),
  whose defining prefix condition names pure cyclic-interval growth words;
- [Bjorner--Ziegler, *Introduction to Greedoids*](https://doi.org/10.1017/CBO9780511662041.009)
  and [Korte--Lovasz--Schrader, *Greedoids*](https://doi.org/10.1007/978-3-642-58191-5),
  for feasible/basic-word and antimatroid machinery;
- [Eppstein, chain antimatroids and alternative learning-space paths](https://doi.org/10.7155/jgaa.00159);
- [Uno--Yagiura, common intervals](https://doi.org/10.1007/s004539910014),
  [Heber--Mayr--Stoye, multiple/circular permutations](https://doi.org/10.1007/s00453-009-9332-1),
  and [Hsu--McConnell, PC trees](https://doi.org/10.1016/S0304-3975(02)00435-8);
- [Bohus, discrepancy of intervals from several orders](https://doi.org/10.1002/rsa.3240010208)
  and [Newman--Neiman--Nikolov](https://doi.org/10.1109/FOCS.2012.84),
  which use different discrepancy quantifiers but establish the multi-order
  interval-union neighborhood;
- [Corteel--Louchard--Pemantle, delta-intervals](https://doi.org/10.46298/dmtcs.362)
  and [Amir--Gasieniec--Shalom, approximate common intervals](https://doi.org/10.1016/j.ipl.2007.03.006),
  as near-interval prior art relevant to N3.

The search was public-web/ECCC/arXiv/Dagstuhl/DOI/author-repository based,
mainly English, through 2026-08-26.  It did not exhaust MathSciNet, zbMATH
full text, non-English theses, private work, or complete citation graphs.
Negative search results therefore support at most `POTENTIALLY-NOVEL`, never
the submitted strong status.  All `NOVELTY-STRONGLY-SUPPORTED` wording for
Cycle 5 must be removed.

## 11. Final integration consistency and exact correction ledger

Commit `18ba9cf` is titled “Apply SEG arms-length referee repairs,” but its
diff adds only the referee report and its tooling/results.  It does not edit
the deep SEG proof, the theorem file, the results summary, or
`RESEARCH_STATE.md`.  Consequently a disposition table saying “fixed” is
not evidence that the operative artifacts contain the fix.

The following corrections are required before canonical integration.  “No”
in the last column means that the theorem/certificate conclusion survives;
it does not mean the wording may be left unchanged.

| file and location | current statement/problem | exact correction | mathematical conclusion changes? |
|---|---|---|---|
| `audits/cycle05_seg_deep_independent_validation.md:190-247,263-324` | W1/W2/W3 mix integer first-passage variables with real `d`, `Delta`, and `t*`; R1/R2 are absent | Insert the real-threshold W1, rounded W2, `delta=ceil(d)` S3 argument, R1 first-leg sentence, and R2 two-case arithmetic from sections 5.4--5.6 of this audit | No |
| `audits/cycle05_seg_deep_independent_validation.md:309-313` | Uses `13824` in an upper bound and an invalid one-line floor absorption | Use `K<=L/(6912d^3)` and split `d^2` into `[13824,27648)` and `[27648,infinity)` | No |
| `audits/cycle05_seg_deep_independent_validation.md:319-321` | Degenerate split explanation does not establish the first chaser time | Use R1: `b_1>=1`; for a zero-length chaser the event is empty once a milestone exists | No |
| `audits/cycle05_seg_deep_independent_validation.md:373-380` | Declares `C:=3` while displaying `6sqrt(N)` | Set the theorem constant to `C=6` | No |
| `audits/cycle05_seg_arms_length_referee.md:250-267` | R3 relies partly on computed margin and leaves real `F_d` in the proof | Replace it with the fully analytic rounded argument in section 5.6 | No |
| `audits/cycle05_seg_arms_length_referee.md:281-303` | R4 names perfect fifths `L=j^5`; the missed equality is at `L=j^5+1`, and the claimed strict inclusion is false | Parameterize each terminal split with the last point appended to one extension walk, keep total walk length `L`, and apply S3 before the `L`-way union bound | No |
| `research_cycle_05/flsy_reconstruction.md:115-135,202` | Calls the offset localization “verbatim,” “zero changes,” or “cosmetic” | Say `NEW BUT PROVED IN THIS REPOSITORY`; cite the grid, offset, rounding, first-leg, and cyclic-full proofs and this final audit | No |
| `research_cycle_05/flsy_reconstruction.md:79-81` | Repeats FLSY's proof-display enlargement from strict `<N^(1/5)` to non-strict `<=N^(1/5)` | Keep the theorem's actual integer `k<N^(1/5)` throughout; note that this repairs the perfect-fifth boundary | No |
| `research_cycle_05/switch_structure_theory.md:275-298` | SEG is tied only to the first skeptic report and repairs are called statement-level | Freeze the full theorem, cite the deep proof, arms-length report, and this audit; call R1--R5 proof repairs and record the corrected R3/R4 | No |
| `research_cycle_05/switch_structure_theory.md:308-317` | A pure run is claimed to have at least the real `L*` additions | Use `M=floor((q-7)/(D+1))>=L*/2` and absorb `2^(1/5)` into the constant | No |
| `research_cycle_05/switch_structure_theory.md:355-364` | Lemma RS covers only “middle states,” but E* consumes all finite states | Extend the sandwich explicitly to sizes 1, 2, `q-2`, and `q-1`, preserving defect `<=L+2` | No |
| `research_cycle_05/switch_structure_theory.md:26-33` | `D_mid` is ambiguous for arbitrary `t` | Use the minimum common-label block partition definition in section 8 | No |
| `research_cycle_05/hybrid_definitions.md:55-67` | Disjoint partition blocks are later said to overlap | Keep minimum adjacent label changes, or define endpoint-sharing segments | No |
| `research_cycle_05/switch_structure_theory.md:252-258` | The pair-swap witness starts at size 4 and yields one fewer visible alternation | Prepend `I_3={0,1,3}` and the common `I_4={0,1,2,3}`; retain only the all-`q` lower bound and finite equality claims | No |
| `research_cycle_05/README.md:12`; `results/research_cycle_05.md:207`; `RESEARCH_STATE.md:77-82` | Summary wording can read as all-`q` proofs of transposition depth and pair-swap equality | Transposition `D_mid<=1`: proof candidate, finite-DP checked. Pair-swap: all-`q` lower bound, equality only at certified finite `q` | No |
| `research_cycle_05/dense_circle_obstruction.md:16` | Says the FLSY parameter is `k=O(1)` | Write `k=3D+5<N^(1/5)`, allowing growing `D` in the theorem's range | No |
| `research_cycle_05/dense_circle_obstruction.md:22-23` | Assumes the common reference is listed as `O_1` | After global relabeling write only `O*=id`, unless list membership is separately assumed | No |
| `research_cycle_05/dense_circle_obstruction.md:34,110` | `d` is not typed, yet it is used in an integer chain index | Quantify integer `d>=0` or set `D=floor(d)` and use `D` in all indices/bounds | No |
| `results/research_cycle_05.md:22,161-164`; `RESEARCH_STATE.md:35-36`; `research_cycle_05/README.md:37`; `audits/cycle05_final_integration_adversarial.md:118,199-200` | Calls all 14,864 `n=24` records examples/certificates; README says “same schema” | State “14,864 records, 8,258 distinct `(permutation,word)` examples, 6,606 duplicate swap/xswap labels”; state that `n=24` lacks `min_switches`/`canonical` fields | No |
| `results/research_cycle_05.md:158-160`; `failure_knowledge.jsonl` entry `RC5-HY-04` | Gives or suggests a rescuing threshold at distance 8 / only records zero through 7 | Record zero rescue through 8 and exact rescuing distances `{9,10}` at `n=22` | No |
| `results/research_cycle_05.md:49-50`; `RESEARCH_STATE.md:59-60`; `failure_knowledge.jsonl` entry `RC5-HY-02` | Gives `85.7--87.9%` for `n=24..34`, but `n=34` is 85.6% | Use `85.6--87.9%` for `n=24..34` | No |
| `research_cycle_05/switch_structure_theory.md:260-263` | Gives `87.4--87.9%` for `n=24,26,28,30`, omitting the 85.7% endpoint | Use `85.7--87.9%` for those four sizes (87.4% is the aggregate, not the minimum) | No |
| `research_cycle_05/README.md:54-56` and the `n=22` generator | Annotation step is acknowledged but not reproducible | Commit a deterministic annotation/postprocessing step or label the fields as independently checked manual postprocessing | No |
| `results/research_cycle_05.md:248-254` | `revB`, bit-reversal, and xor diagnostics lack a committed generator | Add a reproducer or explicitly label these measurements non-reproducible diagnostics | No |
| `research_cycle_05/switch_structure_theory.md:275-280,299,344,366`; `results/research_cycle_05.md:53-65,288-305,355-356`; `RESEARCH_STATE.md:64-76,97-98,108-114`; `failure_knowledge.jsonl` entry `RC5-HY-03` | SEG remains “proof candidate” based only on the first audit; C/F remain conditional on an allegedly unproved lemma; repairs are called statement-level | After incorporating this audit's exact proof repairs, label SEG/C/F `ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED`, retain the dependency arrows, and state SEG is not published verbatim | No |
| `research_cycle_05/novelty_audit_theorems.md:44,109-114,152-154,206-213,245-253,295-303,318-319` | “Exactly two papers,” framework “established as unstudied,” N1/N4 potential, and N5 strong novelty | Apply the N1--N5 classifications in section 10; explicitly cite FLSY Lemma 2.3, arc permutations, regular systems/antimatroids, and the Algaba extra-chain example | No |
| `research_cycle_05/common_interval_literature.md:579-610` | Calls the broad switching/hybrid object apparently unstudied/new | Limit non-detection to the exact interval-specific quantitative theory and acknowledge the broader feasible-word/extra-chain literature | No |
| `research_cycle_05/README.md:15-16`; `results/research_cycle_05.md:126-138,359`; `RESEARCH_STATE.md:100-106`; `literature/novelty_log.md:29-33` | Propagates four potential-novel labels and `NOVELTY STRONGLY SUPPORTED` for the object | N1 `UNCLEAR`; N2/N3 narrowly `POTENTIALLY-NOVEL`; N4 aggregate `UNCLEAR`; N5 object `KNOWN`, RR-specific analysis at most `POTENTIALLY-NOVEL`; remove every strong label | No |
| `audits/cycle05_final_integration_adversarial.md:54-70`; `audits/cycle05_fable_independent_validation.md:325-333` | Historical audits endorse stale SEG/novelty statuses | Mark those portions superseded by the deep/arms-length/final cross-model proof and prior-art findings; preserve them as audit history | No |
| `results/research_cycle_05.md:69-70`; `RESEARCH_STATE.md:96-97` | Says all infinity-moving relabelings are outside scope | If precision is desired, say different-anchor/general infinity-moving lists are outside; a common moved anchor globally reduces to the infinity-fixing case | No |
| `results/research_cycle_05.md:130` | Credits approximately 40 searches although 20 numbered queries are documented | Say “20 documented query strings plus direct source/catalog scans,” or document the additional queries | No |

The corrected provenance hierarchy is:

1. FLSY's named results and probability ingredients are published.
2. Theorem A, Theorem E, SEG, C, and F are repository proofs, internally
   adversarially reviewed and unformalized; SEG is not a quoted FLSY theorem.
3. The finite claims are exhaustive or certificate-verified computations,
   not asymptotic proofs.
4. Lean proves only the generic deterministic core named in its coverage
   ledger.
5. Novelty labels are bounded-search assessments.  No strong novelty claim
   is justified.

## 12. Final statuses

THEOREM-A: SOUND-AS-STATED

THEOREM-E: SOUND-WITH-REPAIRS

SEG: SOUND-WITH-REPAIRS

THEOREM-C: SOUND-WITH-REPAIRS

THEOREM-F: SOUND-WITH-REPAIRS

HYBRID-MINIMALITY: SOUND-AS-STATED

CERTIFICATES: SOUND-WITH-REPAIRS

FORMAL-COVERAGE: SOUND-AS-STATED

The required repairs are local, explicit, and conclusion-preserving.  The
current candidate artifacts should not be copied verbatim into canonical
state; applying the ledger above is a condition of integration.  No merge
was performed.

MERGE-SAFE-WITH-MINOR-CORRECTIONS

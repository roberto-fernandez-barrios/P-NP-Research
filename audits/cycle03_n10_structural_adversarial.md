# Cycle 3 stage-1 adversarial audit: exact `n=10` and CP-S/P/G

**Audit date:** 2026-08-21
**Frozen base commit:** `e942729da8db176848354d8d0161e85bcee7c080`
**Role:** independent adversarial falsifier/integrator
**Scope:** exact `N(10)` certificate and the CP-S, CP-P, and CP-G reports as
they existed at the audit cutoff
**Excluded from this stage:** CP-M and Lean, which require a later audit after
their artifacts stabilize
**Status boundary:** finite claims are `ADVERSARIALLY REVIEWED;
UNFORMALIZED`.  O01 remains **OPEN**.  No asymptotic, mABP, or complexity
separation follows.

## 1. Disposition

| Claim | Disposition | Exact qualification |
|---|---|---|
| `N(10)=35` | **PASS** | Reconstructed from the literal definition in new code; the exhaustive lower searches, complement argument, size-34 split, and 35-mask upper family all pass. This is a finite computational result, not a formal theorem or asymptotic lead. |
| `tau(10,k)=(1,1,5,3,5,3,5,3,5,1,1)` | **PASS** | Every upper cover was checked and every normalized one-smaller cover was exhausted independently. The normalization and padding arguments are sound. |
| No prefix of profile `1,1,5,3,5` | **PASS** | All 4,060 triple choices and 1,686,060 relevant four-set choices were reconstructed. The pruning of globally dead selected states is complete because of the already established level minima. |
| Size-35 upper family | **PASS** | Forward color-bitset reachability accepts all 252 signed colorings without reading stored witness chains. All 60 paths and the structural metadata were then independently recomputed. |
| CP-S `TFO` | **PASS** | The terminal-fanout proof is correct; the `n=10` local boundary was separately exhausted. `ADVERSARIALLY REVIEWED; UNFORMALIZED`. |
| CP-SD / CP-SQ failures | **PASS WITH WORDING CORRECTION** | The state accounting and `n>=10` terminal bottleneck are correct. CP-SQ should explicitly be defined only for `n>=4`, and “first failure” should mean the first size with no valid member of the class, not the first invalid parameter choice. |
| `DEFECT-LIFT` | **PASS, CONDITIONAL ONLY** | Coverage and the exact `|X|+|D|+2` distinct-state count are correct. The missing polynomial-router statement is neither proved nor preserved by the recursion. |
| Self-router preservation failure | **PASS** | Independently reproduced: defect routing fails at `n=6`; continuing the unsupported lift loses balanced coverage at `n=8`. |
| CP-P hierarchy recurrence and block rule | **PASS** | The four-piece union has `h(T)=2h(A)+2h(B)-4`; mixed states exhaust one root child. An independent contracted-pair implementation reproduces the shape table through `n=12`. |
| CP-P layer-cover/no-path example | **PASS** | The 28-state `n=6` hierarchy covers every color at every rank but has no path for plus set `{0,1,2}`. |
| CP-P full and sparse lifts | **PASS WITH SCOPE** | Full insertion preserves coverage and costs exactly `4|X|`. The sparse splice lemma is correct under DTP, but DTP fails to be preserved at `n=6`. The `2^(n-1)` count applies only to the literal all-even-residual frontier union. |
| CP-G adjacent-interface predicate | **PASS** | A fresh exhaustion of all 16,384 endpoint-containing `n=4` families reproduces 556 counterexamples and the first seven-state example. |
| CP-G prefix-defect Lemma G4 | **PASS** | The proof and its complement dual are correct. At `n=10`, the disjoint prefix bands force the two units of surplus in every optimum. |
| CP-G reachability Lemma G2 | **QUALIFIED PASS** | Add the hypothesis `emptyset in X` (and treat the full set as selected when stating the terminal equivalence), or define the base reachability as empty when the endpoint is absent. Valid families already satisfy this. |
| `sigma` interpretation | **PASS** | It is aggregate level excess, not the number of removable bridge vertices in a fixed minimum-cover skeleton. The displayed surplus ranks contain no minimum-cover subfamily. |

No stage-1 claim was found that resolves O01 or supports an asymptotic
extrapolation.

## 2. Independent implementations

Two new standard-library checkers were written without importing proposer
modules:

* `audits/check_cycle03_n10_structural_adversarial.py` reconstructs all 252
  signed balanced colorings, all compatibility columns, the normalized level
  lower bounds, the prefix obstruction, complement duality, the surplus-level
  split, and the upper family.
* `audits/check_cycle03_structural_classes_adversarial.py` checks CP-S/P/G.
  Its hierarchy search uses the **contracted pair DAG** and propagates all
  balanced colors together, rather than reusing the proposer's uncontracted
  one-element path routine.

Their SHA-256 hashes at this audit cutoff are respectively

```text
80d285405af9f595e4060a9e7eaf87cdd5bb91b0fbe145fb95b56185a5fa89dc
0dd426924b274a1adc2f8f22245d8532d153f2cfef3755113bdc361fee8f16f3
```

Hexadecimal hashes are case-insensitive. The files may legitimately acquire
new stage-2 checks later; Git records the authoritative final versions.

## 3. Clean reconstruction of `N(10)=35`

### 3.1 Literal object

The audit did not begin from stored paths. It represented a balanced coloring
by a five-element plus mask `P` and used

`d_P(S)=2|S intersect P|-|S|`.

For a selected family `X`, it propagated the exact bitset of colorings having
a one-element selected path from the empty set to each state, intersecting at
each step with `|d_P(S)|<=1`. Thus acceptance at the full mask is precisely
the repository definition.

### 3.2 Level-cover normalization and padding

For each `k<=5`, the claimed cover itself covers all 252 signed balanced
colorings. To refute a cover of size `tau-1`, fix any member of a hypothetical
nonempty cover. The action of `S_10` is transitive on `k`-sets and permutes
the complete balanced-coloring universe, so that member may be relabeled to
`{0,...,k-1}`. Exhausting every choice of the remaining distinct `k`-sets is
therefore complete; it need not be an orbit-free enumeration.

Refuting exactly size `tau-1` also refutes every smaller cover. A smaller
cover can be padded with unused, distinct same-rank sets until it has
`tau-1` members, and coverage is monotone under adding sets. There are more
than enough rank-`k` sets in every case. For `tau=1`, the only smaller family
is the empty family and no symmetry normalization is needed.

The independent branch counts and maxima agree exactly:

| rank | claimed `tau` | normalized one-smaller branches | maximum coverage |
|---:|---:|---:|---:|
| 0 | 1 | 1 | 0/252 |
| 1 | 1 | 1 | 0/252 |
| 2 | 5 | 13,244 | 250/252 |
| 3 | 3 | 119 | 250/252 |
| 4 | 5 | 1,499,784 | 248/252 |
| 5 | 3 | 251 | 244/252 |

For every balanced `P`, `d_P([10] minus S)=-d_P(S)`. Exhausting this identity
over every state and color transfers both upper and lower bounds to ranks
six through ten. The level sum is 33, so size 30 is already impossible.

### 3.3 Completeness of the minimum-prefix exhaustion

Suppose levels zero through four have counts `1,1,5,3,5` in a valid family.
Relabel the unique singleton to `{0}`.

Every selected pair usable on a path must contain `0`. If one of the five
selected pairs were globally unreachable, the other four reachable pairs
would give every coloring a compatible rank-two state, contradicting
`tau(10,2)=5`. Hence all five are distinct star pairs and their leaves may be
relabelled to `1,...,5`.

The same reasoning justifies the later pruning:

* a globally unreachable selected triple would leave two reachable triples
  covering all colors, contradicting `tau(10,3)=3`; and
* a globally unreachable selected four-set would leave four reachable
  four-sets covering all colors, contradicting `tau(10,4)=5`.

This argument excludes only signatures equal to zero. A state reachable for
some but not all colors remains in the enumeration with its exact signature.
Therefore globally dead selected states are not a missing case.

The clean-room enumeration found:

* 30 reachable triple candidates;
* all `binom(30,3)=4,060` triple choices;
* 90 triple choices reaching every color at rank three;
* 1,686,060 choices of five reachable four-sets over those branches; and
* maximum terminal coverage 250/252, attained 15,120 times.

The full terminal histogram and the first ten maximum branches match the
stored certificate.

### 3.4 Size 34

Every valid family has at least `tau(10,k)` members at rank `k`. A size-34
family would therefore have exactly one unit of surplus above the level sum
33.

* Ranks zero and ten cannot receive it because each has only one subset.
* A surplus at a rank from five through nine leaves the forbidden exact
  minimum prefix at ranks zero through four.
* A surplus at a rank from one through four leaves ranks six through ten at
  their minima. Complementing all selected sets and reversing each path turns
  that suffix into the same forbidden prefix.

These cases are exhaustive. This establishes the finite lower bound 35 once
the two exhaustive computations above are accepted.

### 3.5 Upper family without stored witnesses

The 35 masks are distinct, include both endpoints, and have profile

`1,1,5,3,6,3,6,3,5,1,1`.

Fresh forward reachability reaches the full set for all 252 colors. Stored
chains were not read for that check. A separate enumeration then reproduced:

* 60 selected maximal chains;
* exactly 32 signed colorings per chain;
* coloring path multiplicities from one to 30;
* 22 signed colorings with a unique path;
* the complete stored multiplicity histogram;
* unique singleton mask 64 and unique co-singleton mask 1019;
* the lower and complemented upper half-stars; and
* positive coloring loss after every one-subset deletion (minimum loss four,
  maximum 252).

Thus the displayed family supplies the finite upper bound 35. These
structural observations concern this family; except for the two-band surplus
consequence of G4, they are not asserted for all optima.

### 3.6 Hash and artifact consistency

The branch statistics were computed before consulting producer code. The
audit then reconstructed the producer's byte stream and matched every stored
`enumeration_sha256`, including

```text
level 0/1  5b9814ed605608bc2ced605c40adb755bca96d613bce2ea70412a34cab35b144
level 2    77bec1e0e0d43e7d50c29df900e035392383b82d29b9df2c84d0d9a1a9bb8488
level 3    76d8b2874d18418201920f793de6308f2b960c518a481f5f7cac3e6c0de021a0
level 4    76811700f4a10dbcc195be976d8abcf8ce92e8d1bcd6dcdeba82ea4dd1ebb641
level 5    a8e9abfc49cf71a7776f21502ac75f02580449490c051de5281ea5d5438729ff
prefix     e39cb91a40104e40aa6f08b17d207c82b274baf08acd467ba5f49cf82446c849
```

The stored hash is an integrity summary, not a proof: its byte encoding is
currently specified by the checker source rather than by the JSON schema.
For archival portability, the certificate README should state that encoding.
The SAT `UNSAT` records have no checked proof and were deliberately not used.

## 4. CP-S and recursion audit

### 4.1 State accounting and terminal fanout

A literal two-rail diamond spine has at most `2m-2` distinct odd checkpoints,
at most `4(m-1)` even intermediates, and two endpoints, hence at most
`6m-4` distinct subsets. Collisions only decrease this number.

With a unique singleton `{v}`, let `Lambda` be the star leaves whose pair
`{v,u}` continues into at least one selected triple. Each triple contains at
most two such leaves, so `|Lambda|<=2q` for `q` triples. If `2q<=m-1`, choose
a balanced plus side containing `{v} union Lambda`. Every possible path then
uses a positive monochromatic rank-two pair. Therefore `2q>=m` and
`q>=ceil(m/2)`. The complement/reversal dual is equally valid.

At `n=10`, the audit exhausted all 7,140 pairs of selected triples after
normalizing the five-leaf star. No pair of triples continues more than four
leaves, and the constructive countercolor fails before rank three. This
validates both the two-rail failure and the two-odd-width CP-SQ failure.

Two wording changes are required:

1. CP-SQ's formula uses separate singleton and co-singleton ranks and a
   count of `m-2` internal odd ranks. State explicitly that its domain is
   `n=2m>=4`; the displayed formula is not a definition at `n=2`.
2. “The smallest failure is `n=10`” must mean the smallest `n>=4` for which
   **no valid member exists**. Some parameter choices can be invalid at
   smaller sizes even though the stored examples show the class is nonempty.

Whether CP-SQ requires distinct anchors should also be explicit. The
bottleneck proof does not depend on that choice.

### 4.2 Defect lift

The conditional lift is sound. For opposite new signs, use an old balanced
path, then the selected state `U union {b}`, then the full state. For equal
new signs `s`, the old total is `-2s`; a one-sided defect path lies in
`[-2,0]` or `[0,2]` as appropriate, and adjoining `{a}` shifts every value
into `[-1,1]` before the final `b` returns the total to zero.

The old, `{a}`-shifted, `b`-only top, and full pieces have disjoint marker
signatures, so the exact count is `|X|+|D|+2`. The audit exhaustively checked
all nine `(X,D)` antecedent pairs on a two-point old ground set.

This does not preserve a router. The independent computation reproduced
defect failures at `n=6` for plus masks 48 and 15 and balanced failures at
`n=8` for masks 15 and 240 after another unsupported iteration. Consequently
`DR-POLY` is only an open sufficient condition, not the explicit preserved
property required for a completed recursion and not a Cycle-3 S3-B result.

## 5. CP-P hierarchy audit

### 5.1 Recurrence and root rule

For root children with disjoint nonempty grounds `A,B`, the four defining
pieces intersect only at `emptyset`, `A`, `B`, and `A union B`. Inclusion-
exclusion gives

`h(T)=2h(A)+2h(B)-4`.

Complementation exchanges the unshifted and completed-opposite-child pieces,
so complement closure and the singleton/co-singleton claims follow by
induction. Every selected state meeting both root children contains all of
`A` or all of `B`. If both have size at least two, this forces every maximal
chain to exhaust one before entering the other. These arguments pass without
a hidden plane ordering or path-description restriction.

For equal complete children the recurrence solves to
`(2n^2+4)/3`. Coloring one entire root child plus and the other minus kills
rank two for every `n=2^q>=4`, so the quadratic balanced hierarchy is indeed
false at its first nontrivial case.

### 5.2 Independent finite shape sweep

The contracted-pair implementation reproduced:

| `n` | shapes | valid | minimum states, any | minimum states, valid |
|---:|---:|---:|---:|---:|
| 2 | 1 | 1 | 4 | 4 |
| 4 | 2 | 1 | 12 | 16 |
| 6 | 6 | 2 | 28 | 48 |
| 8 | 23 | 3 | 44 | 160 |
| 10 | 98 | 6 | 76 | 448 |
| 12 | 451 | 11 | 108 | 1152 |

Every valid shape in this finite sweep independently passed DTP. No growth
rate or unrestricted lower bound is inferred.

For `T=((0,1),((2,3),(4,5)))`, the audit reconstructed 28 states and profile
`1,6,3,8,3,6,1`. Every balanced coloring has a compatible state at every
rank. Plus set `{0,1,2}` nevertheless has no contracted path: taking the
two-leaf child first consumes a plus-plus pair; taking the four-leaf child
first would have to divide one plus and three minuses into two crossing
pairs. H4/H5 therefore pass exactly as scoped.

### 5.3 Lifts

The full marker product has four disjoint signatures and hence exactly
`4|X|` states. The same-sign proof is correct: flip one old minority-sign
element to make the old coloring balanced, take its mate in the resulting
witness, and replace that pair by two crossing pairs involving the new
same-sign elements. The audit checked the lift for every balanced family on
two old points, not only the displayed base.

For the sparse splice, DTP supplies a crossing-pair prefix leaving two old
majority-sign vertices; the four explicitly listed tail states complete the
path. The additive bound is correct. Independently, the iterates have sizes
14, 41, and 92; DTP first fails at `n=6` on plus mask 48, and the next
unsupported iterate first fails balanced coverage at `n=8` on mask 15.

The count `sum_r binom(n,2r)=2^(n-1)` is the exact number of literal even
residual bases. It is not a lower bound for every compressed all-defect DAG,
as the report correctly states.

## 6. CP-G audit

### 6.1 Exact reachability and the endpoint qualification

G1 and G3 are immediate and correct. G2 is the ordinary last-edge induction,
but its statement begins “for a family `X`” while assigning
`R_0(emptyset)=Omega_n` unconditionally. It should say `emptyset in X`, or
assign an empty base when the empty set is absent. Similarly, the terminal
equivalence presupposes that `[n]` is selected. This does not affect any valid
family or finite certificate, because every maximal selected chain contains
both endpoints.

### 6.2 Adjacent interfaces do not compose

A new exhaustive loop reproduced the exact `n=4` statistics:

* 8,874 of 16,384 endpoint-containing families pass all adjacent interfaces;
* 556 of those fail global reachability;
* the bad-size histogram is `7:24, 8:180, 9:264, 10:88`; and
* the lexicographically first minimum family is
  `{0,1,3,5,10,11,15}`, missing plus masks 3 and 12.

For plus mask 3, interface witnesses `1 -> 5` and `10 -> 11` do not compose,
because state 10 is unreachable from the only selected singleton. The
predicate has no counterexample at `n=2`, so `n=4` is the first positive even
failure.

### 6.3 Prefix defect and surcharge

The independent `n=8` prefix computation found 18 triple candidates, 153
triple choices, three all-color choices, 360 terminal choices, and maximum
64/70. The independent `n=10` computation is Section 3 above. Their
dead-state completeness uses the exact `tau` minima in precisely the same
sound way.

G4 follows because every excess summand is nonnegative; a zero prefix excess
would give the prohibited exact-minimum prefix. Complement/reversal gives the
upper inequality. When `2r<n`, the rank intervals are disjoint and the two
units add. Thus at `n=10`, every size-35 optimum has exactly one surplus unit
somewhere in ranks one through four, one somewhere in ranks six through nine,
and none at rank five. This does not determine the precise two surplus ranks
or the rest of an optimum's structure.

Finally, direct enumeration confirmed that the surplus rank of the displayed
`n=8` optimum contains zero minimum-cover subfamilies and that both surplus
ranks of the displayed `n=10` optimum do likewise. Therefore `sigma` cannot
be interpreted as deleting named bridge vertices from those fixed optima.

## 7. Required integration corrections

Before the reports receive their final integrated status:

1. restrict CP-SQ explicitly to `n>=4`, make the anchor convention explicit,
   and qualify “smallest failure” as an existence statement;
2. add the endpoint hypothesis/definition to CP-G Lemma G2;
3. keep `DR-POLY` and compressed all-defect routing labelled open, not as
   preserved recursion lemmas or S3-B survivors;
4. document the enumeration-hash byte encoding if the digests are intended
   as portable certificate fields; and
5. retain the explicit scope that the SAT `UNSAT` outputs are corroborating
   solver evidence only.

These are definitional or evidence-presentation corrections. They do not
change the finite result `N(10)=35` or the negative structural results audited
in this stage.

## 8. Reproduction

From the repository root:

```powershell
python -B audits/check_cycle03_n10_structural_adversarial.py
python -B audits/check_cycle03_structural_classes_adversarial.py
```

Both end in PASS. The second includes the complete 451-shape `n=12` sweep and
may take about a minute depending on the machine.

## 9. Final stage-1 boundary

The exact finite conclusion `N(10)=35` survives a genuinely independent
reconstruction. The proposed quadratic finite identity is therefore false at
`n=10`. TFO, the conditional defect lifts, the hierarchy recurrence/block
rule, the full/sparse lift analyses, the adjacent-interface counterexample,
and prefix-defect G4 survive this audit with the qualifications above.

None is a general polynomial construction. O01 remains **OPEN**. CP-M and
Lean still require the separately requested stage-2 adversarial audit.

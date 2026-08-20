# Adversarial audit of the Cycle-2 exact `N(n)` track

**Audit date:** 2026-08-13

**Verdict:** **PASS** for the mathematical/computational claims
`N(2)=3`, `N(4)=6`, `N(6)=12`, and `N(8)=20`.

**Status after this audit:** independently computationally reproduced and
adversarially reviewed inside the repository; still `UNFORMALIZED` and
`NOT NOVELTY-AUDITED`.  This audit makes no asymptotic claim and does not
address O01.

**Independence boundary:** I did not use or validate my own Cycle-2 repair
track.  I treated the exact-value report, optimizer, checker, and certificates
as untrusted inputs, reconstructed the model from the definition, reran both
provided paths, and wrote a third set-based enumeration that imports neither
proposer program.  No proposer artifact was edited and nothing was committed.

## 1. Inputs frozen for the audit

| Artifact | SHA-256 |
|---|---|
| `research_cycle_02/exact_balanced_chain_values.md` | `08B2C6D6589A32A1F1360574BCC9D886997C13E88420559A81AB19EA227C4233` |
| `experiments/balanced_chain_optimize.py` | `3FF99039431AF09424BAEB47EA907FD854AA963863BDA3EE662E88200FF034DE` |
| `experiments/check_balanced_chain_certificates.py` | `A47B98412D1726FFA31E1F35AA5EB038FFC69D703B1A751A8BB4400A49E78DF8` |
| `exact_n2.json` | `281C84531EC15D67B205F43C4E0DAD20E43EF90B488A98F8E6A37D0B08FBE0AF` |
| `exact_n4.json` | `9E24756A443E354DF1BB1DF7ACE9BCE0B5E70FEDCA7010782193977E0AA7CD1F` |
| `exact_n6.json` | `65B248730DCC838FD8D4C2282E9B45EF30E06A9D01B7177035ECA3A904183643` |
| `exact_n8.json` | `E8D2E2AB66CB3CE9E113E46673DC6ED32539D3F66EC25D430DFD3ECC48BED0D6` |
| `level_cover_lower_bounds.json` | `0C4A78D600E18D6D7425BDC22DC2701C5F550727E28F409806877119092067CD` |
| `n8_no_size19.json` | `17664A3B8E283AFBD2A2DA2149BF7CFEB15C6A0CC04E81092F46C3E2F4E55009` |

## 2. Reproduction results

### 2.1 Provided standard-library checker

Running

```text
python -B experiments/check_balanced_chain_certificates.py
```

completed successfully and printed:

```text
PASS n=2: upper witnesses exhaustive; lower bound=3
PASS n=4: upper witnesses exhaustive; lower bound=6
PASS n=6: upper witnesses exhaustive; lower bound=12
PASS n=8: upper witnesses exhaustive; lower bound=20
PASS n=8 no-size-19 enumeration: 100800 level-4 branches
ALL BALANCED-CHAIN CERTIFICATES PASS
```

### 2.2 Fresh HiGHS optimization

I reran all four optimizations into a newly created directory under the
system temporary directory, not into `certificates/`.  All runs returned
status optimal with equal objective and dual bound:

| `n` | objective | dual | B&B nodes | fresh family identical to stored family |
|---:|---:|---:|---:|---|
| 2 | 3 | 3 | 0 | yes |
| 4 | 6 | 6 | 1 | yes |
| 6 | 12 | 12 | 1 | yes |
| 8 | 20 | 20 | 9 | yes |

I then loaded only the standard-library witness verifier against the freshly
written families; it accepted every balanced coloring.  This rerun supports
reproducibility but is not used as the sole lower-bound argument.

### 2.3 Third implementation

I independently represented points and subsets by Python `set`/`frozenset`
objects, represented a coloring by its positive-element set, and used the
literal signed sum

`sum(1 if x in P else -1 for x in S)`.

It imported neither proposer script.  It independently:

1. reconstructed every maximal path contained in each displayed family;
2. computed a chain's colorings from independently oriented consecutive
   pairs rather than calling the compatibility predicate;
3. exhausted all smaller collections for every claimed layer minimum; and
4. redid the full `n=8`, size-19 lower-prefix enumeration without a color,
   complement, singleton, or permutation quotient.

This path also passed.

## 3. Model equivalence audit — PASS

For a positive set `P` of cardinality `n/2`, the imbalance of `S` is

`d_P(S)=2|S intersect P|-|S|`.

A maximal Boolean-lattice path visits exactly one set of each size, and its
successive vertices differ by one element.  Restricting the lattice to
vertices with `|d_P(S)|<=1` therefore gives a source-to-sink path exactly when
the selected family contains a maximal imbalance-at-most-one chain for `P`.
There is no relaxation in this translation.

The MILP has one binary selector per vertex and a continuous unit flow per
retained coloring.  Every flow edge is a compatible one-element extension and
is constrained by both endpoint selectors.  Flow conservation sends one unit
from `emptyset` to `[n]`.  Because all edges strictly increase cardinality,
the graph is acyclic; any positive unit flow decomposes into source-to-sink
paths, at least one of which uses only selected vertices.  Continuous flow
splitting cannot create a false feasible family.

The source and sink are compatible for every balanced coloring.  Skipping a
flow-conservation row only for a compatible vertex having no incident edge
does not omit a source/sink constraint and cannot create a path.

## 4. Consecutive-pair encoding and orientations — PASS

For an addition order `(pi_1,...,pi_n)`, every even compatible prefix must
have imbalance zero.  Hence each pair

`(pi_1,pi_2), (pi_3,pi_4), ..., (pi_(n-1),pi_n)`

must contain one positive and one negative point.  Conversely this condition
makes every even prefix zero and every odd prefix `+1` or `-1`.

Crucially, the positive endpoint of each pair is **not fixed by the pair's
order**.  It can be chosen independently in either orientation.  Thus one
chain covers exactly `2^(n/2)` signed balanced colorings.  Both proposer
encodings preserve these choices:

* the flow/compatibility model uses absolute imbalance and therefore accepts
  either orientation; and
* every stored witness was independently checked pair by pair, with XOR—not
  a fixed orientation—required.

The third implementation found:

| `n` | maximal chains in displayed family | colors per individual chain | union of covered signed colorings | distinct pair-orientation vectors occurring among stored witnesses |
|---:|---:|---:|---:|---:|
| 2 | 1 | 2 | 2 | 2 |
| 4 | 2 | 4 | 6 | 4 |
| 6 | 8 | 8 | 20 | 8 |
| 8 | 16 | 16 | 70 | 16 |

At every pair position and every `n`, both orientation bits occur among the
stored witnesses.  No branch is missing because pair orientations vary.

## 5. Symmetry audit — PASS

Only the following optimizer symmetries/reductions are present, and both are
valid.

### 5.1 Global sign quotient

For every subset `S`,

`d_(P complement)(S)=-d_P(S)`.

Thus `P` and its complement induce the identical compatible DAG.  Since
exactly one member of each complement pair contains element zero, the test
`mask & 1` retains exactly one of the `binom(n,n/2)/2` identical commodities.
The certificate checker and both independent enumerations use all signed
colorings.

### 5.2 Canonical-chain relabeling

Every feasible family contains a witness maximal chain for any one balanced
coloring.  Relabeling elements by their order on that chain maps its prefixes
to the canonical prefix chain, preserves the family cardinality, and
bijectively permutes the full set of balanced colorings.  Hence forcing the
canonical chain in the optimizer is without loss.

No complement closure of the selected family, no permutation invariance of
the family, and no fixed orientation of a chain pair is imposed.  The
decisive size-19 enumeration uses neither of the two reductions: it loops over
all eight singleton roots and all 70 signed balanced colorings.

## 6. Upper witnesses and mask encoding — PASS

For every certificate I independently checked:

* `family_elements` re-encodes to `family_masks` exactly;
* masks are unique and in `[0,2^n-1]`;
* the recorded level counts equal the mask cardinalities;
* there is exactly one witness for each of all `2,6,20,70` positive sets in
  lexicographic combination order;
* each recorded order is a permutation;
* its stored masks are precisely its successive prefix sets;
* every prefix lies in the displayed family; and
* every consecutive pair is bichromatic, with either orientation permitted.

Independently enumerating all maximal paths in each family, rather than using
the stored witnesses, gives the path and coverage counts in Section 4 and
covers every balanced coloring.

## 7. Layer minima — PASS

Let `tau(n,k)` be the minimum number of level-`k` subsets whose compatible-
coloring sets cover every signed balanced coloring.  Every valid chain family
must meet this cover at each level, so the disjointness of Boolean-lattice
levels gives

`N(n) >= sum_k tau(n,k)`.

The independent set-based enumeration tested every collection strictly
smaller than the claimed minimum and then verified the stored example.  The
number of smaller collections tested at each level (including the empty
collection) was:

| `n` | verified minima | smaller collections tested by level |
|---:|---|---|
| 2 | `1,1,1` | `1,1,1` |
| 4 | `1,1,2,1,1` | `1,1,7,1,1` |
| 6 | `1,1,3,2,3,1,1` | `1,1,121,21,121,1,1` |
| 8 | `1,1,4,2,3,2,4,1,1` | `1,1,3683,57,2486,57,3683,1,1` |

The sums `3,6,12` match the upper families for `n=2,4,6`.  At `n=8` the sum
is 19, leaving exactly the size-19 case treated next.

## 8. Unsymmetrized `n=8` no-size-19 enumeration — PASS

### 8.1 Why the branch space is complete

A size-19 family must attain every layer minimum and hence have counts

`1,1,4,2,3,2,4,1,1`.

For a fixed singleton, any globally unreachable selected pair can be removed
from the reachable prefix.  The remaining at most three reachable pairs
would have to cover all colorings at level two, contradicting
`tau(8,2)=4`.  The same argument applies to a globally unreachable selected
triple or four-set, using `tau(8,3)=2` and `tau(8,4)=3`.  It is therefore
complete to enumerate exactly four, two, and three globally reachable
vertices at levels two, three, and four.

The enumeration still retains a separate reachability bit for each coloring.
A vertex reachable for only some colorings is not discarded; it carries
exactly those colors forward.  At level four, a valid full family would have
to make every one of the 70 colors reachable.  A color missing there cannot
be repaired at a later level because every maximal chain has a level-four
prefix.  Thus the upper half need not be enumerated once all lower prefixes
fail.

### 8.2 Independent enumeration evidence

The third implementation used `frozenset` containment and literal signed
sums, not integer bit operations or the proposer reachability function.  It
reproduced exactly:

```text
level2_choices = 280
level2_live    = 280
level3_choices = 42840
level3_dead    = 42000
level3_live    = 840
level4_choices = 100800
coverage histogram = {60: 25200, 62: 25200, 64: 50400}
maximum covered = 64 of 70
```

It iterated all eight singleton roots and all signed colorings.  Its branch
records used a deliberately different textual set encoding and produced
SHA-256

`6BFFE7CB63EBFE011E5D0EA42D96F6585CF5C08ACDF4D0241586DBA50327ECC5`.

That hash is not expected to equal the proposer's byte encoding; the matching
branch totals and histogram are the cross-check.  Since every branch misses
at least six colors at level four, no size-19 family exists.  Together with
the displayed size-20 family, this proves the finite computational claim
`N(8)=20`.

## 9. Adversarial omission checklist

| Suspected defect | Result | Evidence |
|---|---|---|
| Pair orientations accidentally fixed | **PASS** | Compatibility uses absolute imbalance; third path uses XOR per pair; all `2^(n/2)` orientation vectors occur. |
| Global-sign quotient drops a distinct DAG | **PASS** | The two imbalance functions are exact negatives. |
| Canonical chain assumes an invariant family | **PASS** | It is obtained by relabeling one existing witness; universality over colorings is permutation invariant. |
| Continuous flows create feasibility without a chain | **PASS** | The flow graph is an acyclic, cardinality-increasing DAG. |
| Layer cover proves compatibility but not reachability | **PASS WITH SEPARATION** | It is used only for the generic per-level lower bound; the size-19 enumeration propagates per-color reachability separately. |
| Unreachable selected vertices omitted incompletely | **PASS** | Fewer globally reachable vertices would violate the independently proved layer minimum. |
| Upper half of size-19 family omitted | **PASS** | Missing reachability at mandatory level four is irreversible. |
| Hidden singleton/permutation quotient in no-19 search | **PASS** | Eight singleton roots produce `8*binom(7,4)=280` level-two branches. |
| Mask/element-list mismatch | **PASS** | All four lists re-encode exactly. |

## 10. Non-fatal corrections and hardening

These do not change any optimum.

1. **Documentation wording — FAIL, editorial only.**
   `research_cycle_02/exact_balanced_chain_values.md:109` says every exact
   certificate contains “all nine prefix masks.”  Only `n=8` has nine.  The
   correct statement is “all `n+1` prefix masks” (respectively 3, 5, 7, and
   9).  The JSON files and both verifiers use the correct lengths.
2. **Ambiguous wording — clarify.** At line 204, “all four reachable level-2
   choices” should be “all choices of four reachable level-2 sets.”  The
   following count 280 and the code are unambiguous.
3. **Checker hardening — non-mathematical omission.** The provided checker
   does not compare `family_elements` with `family_masks`, nor does it compare
   `n8_no_size19.json`'s `prerequisite_level_counts` field with the independently
   derived minima.  Both stored fields are correct and were checked in this
   audit.  Adding these assertions would make future certificate corruption
   fail earlier.

## 11. Final disposition

The adversarial search found no encoding omission, invalid quotient,
incomplete size-19 branch, invalid witness, or incorrect layer minimum.  The
four exact finite values and the stated connectivity surcharge at `n=8`
therefore **PASS** independent internal validation.  The result should remain
described as a finite, computationally certified, unformalized result until a
formal proof or external review changes that status.

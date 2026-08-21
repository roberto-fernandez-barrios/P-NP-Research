# Cycle 4: exact acceptance counting for the corrected `RR_n`

**Role:** independent exact-counting / dynamic-programming attack
**Date:** 2026-08-21
**Base commit read:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Status:** exact exhaustive necklace computation through `n=34`; full
independent recount through `n=30`; no asymptotic inference
**Boundary:** these data neither prove an inverse-polynomial lower bound on
`A_n` nor obstruct one.

## 1. Independent reconstruction of the literal family

Let `n=2m`, `q=n-1`, and write the ground set as
`Z_q union {infinity}`.  For each `r in Z_q`, the corrected round-robin seed
order is

```text
r, infinity, r+1, r-1, r+2, r-2, ..., r+(m-1), r-(m-1),
```

with finite arithmetic modulo `q`.  Direct prefix calculation, without using
the Cycle-3 conclusion as a premise, gives the literal union

```text
rank 0:       emptyset;
rank 1:       every finite singleton {r};
rank k, 2<=k<=n-1:
              {infinity} union I for every cyclic interval I in Z_q
              of length k-1;
rank n:       the full set.
```

For even seed rank `2j`, the finite prefix is
`{r-(j-1),...,r+(j-1)}`.  For odd seed rank `2j+1`, it is
`{r-(j-1),...,r+j}`.  As `r` varies, these give all starts of the stated
interval length.  Conversely every seed prefix has this form.  Distinct
proper cyclic intervals of a fixed length have distinct starts, and ranks
distinguish different lengths.  Hence the number of **distinct literal
subsets** is

```text
2 + q at each of n-1 internal ranks = 2+q(n-1) = (n-1)^2+2.
```

The independent checker constructs both the seed-prefix union and the
displayed interval family and checks their equality for every even `n<=34`.
This finite check corroborates the preceding all-`n` calculation; it is not
being substituted for it.

## 2. Rechecked full-induced-DAG/deque equivalence

Globally reverse every sign when necessary so that `infinity` has sign
minus.  A normalized finite cyclic word `w` then has length `q`, exactly `m`
ones and `m-1` zeroes.  Global reversal preserves every chain imbalance in
absolute value, so this loses no coloring.

In a compatible chain the rank-one state must be a plus finite singleton.
The only selected rank-two successor adds `infinity`.  At every later rank,
the finite part remains a cyclic interval and can grow only at its two
endpoints.  At each even rank the whole selected set is balanced, equivalently
the odd finite interval has sign sum `+1`.  Therefore each two-step interval
extension adds one plus and one minus.  Conversely, for any opposite-sign
two-point extension, the forced nearer-first order on one endpoint, or either
endpoint order for a split extension, has intermediate imbalance exactly
`+1` or `-1` and returns to zero.  Every state used is a literal interval
state above.

If `R_l` is the set of starts of reachable finite intervals of odd length
`l`, indices modulo `q`, then

```text
R_1 = {i : w_i=1},

R_(l+2) = {i-2 : i in R_l and w_(i-2) != w_(i-1)}
        union {i-1 : i in R_l and w_(i-1) != w_(i+l)}
        union {i   : i in R_l and w_(i+l) != w_(i+l+1)}.
```

The three terms add two points on the left, one at each endpoint, or two on
the right.  Thus `RR_n` accepts the coloring exactly when `R_q` is nonempty.
Reversing the construction deletes an opposite-sign pair from the first two,
the two ends, or the last two positions of the current deque.  This proves
both directions for the **full induced subset DAG**, including hybrid paths;
no seed-factor coverage assumption occurs.

As a separate computational check, the Python validator searches every
literal inclusion-by-one edge for every normalized balanced coloring through
`n=12` and obtains exactly the same predicate as the recurrence.

## 3. Exact symmetry-reduced counting method

The number of normalized words is

```text
B_n = binom(q,m) = binom(n,n/2)/2.
```

The accepted fraction among normalized words equals `A_n`: the balanced
colorings split into complement pairs, each pair has one representative with
`infinity` minus, and acceptance is complement invariant.

Acceptance is invariant under rotation of `Z_q`.  Moreover every normalized
word has full rotation period `q`.  Indeed, if its least period were `d|q`,
then the repetition count `q/d` would divide its number `m` of ones.  But
`gcd(q,m)=gcd(2m-1,m)=1`, so `q/d=1`.

It is therefore exact to enumerate one fixed-density binary necklace per
rotation orbit and give it weight `q`.  The C++ producer uses the standard
FKM necklace recursion with weight pruning.  It visits exactly

```text
binom(q,m)/q
```

leaves, a factor `q` fewer than naive balanced-word enumeration.  For each
leaf, one `q`-bit word holds all reachable starts, so one recurrence level is
three rotations, XORs, ANDs and ORs.  This simultaneously evaluates all
possible initial cuts/rotations; it does not call a linear-word reducer on
`q` rotations separately.  The arithmetic work is

```text
O((m-1) binom(q,m)/q)
```

fixed-width word operations for the committed range, plus output of rejected
representatives.  The storage used by the enumerator apart from certificates
is `O(q)`.

## 4. Exact counts

All rows are counts of sign-reversal-normalized balanced finite words.  The
counts for signed balanced colorings on all `n` points are exactly twice the
three integer word columns, while the fractions are unchanged.

| `n` | normalized words `B_n` | accepted | rejected | rejection fraction | rejected rotation orbits |
|---:|---:|---:|---:|---:|---:|
| 22 | 352,716 | 352,695 | 21 | 0.0000595379852346 | 1 |
| 24 | 1,352,078 | 1,351,664 | 414 | 0.000306195352635 | 18 |
| 26 | 5,200,300 | 5,195,600 | 4,700 | 0.000903794011884 | 188 |
| 28 | 20,058,300 | 20,017,908 | 40,392 | 0.00201372997712 | 1,496 |
| 30 | 77,558,760 | 77,266,353 | 292,407 | 0.00377013505631 | 10,083 |
| 32 | 300,540,195 | 298,654,992 | 1,885,203 | 0.00627271503567 | 60,813 |
| 34 | 1,166,803,110 | 1,155,611,853 | 11,191,257 | 0.00959138427391 | 339,129 |

The exact unreduced rational for every row is stored in its JSON certificate.
The monotone increase visible in the rejection column is finite evidence
only.  In particular, it supports neither `A_n >= n^(-O(1))` nor a
superpolynomially small upper bound on `A_n`.

## 5. Failure orbits and run statistics

Every rotation orbit has size `q`.  Reversal preserves failure and either
fixes one rotation orbit or pairs two of them.  The exact orbit decomposition
is:

| `n` | rejected rotation orbits | reflection-fixed rotation orbits | rejected dihedral orbits |
|---:|---:|---:|---:|
| 22 | 1 | 1 | 1 |
| 24 | 18 | 2 | 10 |
| 26 | 188 | 12 | 100 |
| 28 | 1,496 | 24 | 760 |
| 30 | 10,083 | 93 | 5,088 |
| 32 | 60,813 | 187 | 30,500 |
| 34 | 339,129 | 595 | 169,862 |

The cyclic-run histograms below count rejected **rotation orbits**, not
individual words.  Multiplication by `q` gives the corresponding word count.

| `n` | histogram `number of cyclic runs : rejected rotation orbits` |
|---:|---|
| 22 | `4:1` |
| 24 | `4:3, 6:15` |
| 26 | `4:6, 6:62, 8:120` |
| 28 | `4:10, 6:159, 8:647, 10:680` |
| 30 | `4:15, 6:331, 8:2069, 10:4608, 12:3060` |
| 32 | `4:21, 6:606, 8:5238, 10:17955, 12:25365, 14:11628` |
| 34 | `4:28, 6:1014, 8:11455, 10:54210, 12:118180, 14:115482, 16:38760` |

For every computed `n`, the occurring run counts are exactly the even values
from `4` through `n-18`.  The four-run orbit count is respectively
`1,3,6,10,15,21,28`, which equals `binom(m-9,2)` on this finite range.  These
are exact summaries of the certificates, but an all-`n` classification is
only a **conjecture-generation prompt**, not a theorem.

The certificate JSON also records exact histograms of maximum zero-run,
maximum one-run, maximum monochromatic run, and the joint profile

```text
(cyclic run count, maximum zero run, maximum one run).
```

The observed minimum possible maximum monochromatic run among failures drops
from `8` at `n=22` to `4` at `n=30,32,34`.  Thus the data already warn against
assuming that all failures must contain an extremely long monochromatic run.
At `n=34`, one rejected rotation orbit even has maximum zero-run `2` (its
maximum one-run is `8`).

## 6. Certificates and validation boundary

Artifacts:

* `experiments/cycle04_rr_necklace_count.cpp` is the exact producer;
* `experiments/cycle04_rr_verify_counts.py` is the separately written
  validator;
* `certificates/cycle04_rr_acceptance/cycle04_rr_acceptance_n*.json` stores
  counts and all aggregate orbit/run statistics;
* `certificates/cycle04_rr_acceptance/cycle04_rr_failures_n*.txt` stores one
  lexicographically least word per rejected rotation orbit; and
* `certificates/cycle04_rr_acceptance/SHA256SUMS.txt` freezes the payloads.

The validator establishes all of the following:

1. equality of the seed-prefix and literal cyclic-interval definitions;
2. equality of interval reachability and full literal-DAG reachability through
   `n=12` on every normalized balanced coloring;
3. exact binomial/orbit accounting and coprime full-period justification;
4. rejection of every stored representative;
5. canonicality, uniqueness, complement/rotation accounting, reversal
   pairing, and every recorded run histogram; and
6. a from-scratch exact Python necklace recount through `n=30`, reproducing
   all five failure lists and counts.

The `n=32,34` rows were rerun by the C++ producer and then subjected to all
certificate checks in items 1--5, but not to the much slower full Python
recount.  The computation stopped at `n=34` because the complete `n=34`
failure-representative certificate is already about 11.5 MB and the next
lists grow quickly; this is an engineering cutoff, not a mathematical one.

No asymptotic claim is inferred from these seven rows.

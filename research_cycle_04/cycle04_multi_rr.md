# Cycle 4: exact finite multi-RR literal-union attack

**Base commit:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Role:** independent multi-RR set-cover / full-induced-DAG search
**Status:** `EXHAUSTIVE FINITE COMPUTATION; INDEPENDENT CHECKER; UNFORMALIZED`
**Boundary:** no asymptotic conclusion and no claim about O01

## 1. Result

Define the finite optimization parameter

\[
t_{RR}(n)=\min\left\{t:\exists\pi_1,\ldots,\pi_t\in S_n\text{ such that }
\bigcup_{j=1}^t\pi_j(RR_n)
\text{ accepts every balanced coloring}\right\},
\]

where acceptance is through the **full inclusion-by-one DAG induced by the
literal subset union**.  It is not restricted to the generating RR paths.

Exact certificates give

\[
t_{RR}(22)=t_{RR}(24)=t_{RR}(26)=t_{RR}(28)=t_{RR}(30)=2.       \tag{1}
\]

For each `n`, one copy fails on at least one coloring, proving the lower bound
`t_RR(n)>=2`.  The stored two-copy list has disjoint individual rejection
sets, proving the upper bound.  Consequently no hybrid path is needed for the
successful lists, although the verifier reconstructs the full literal union
and is capable of checking hybrid-only coverage whenever the individual
rejection intersection is nonempty.

This is finite evidence only.  Equation (1) gives neither a fixed two-copy
theorem for all `n` nor any asymptotic upper bound.

## 2. Independently reconstructed objects

Put `q=n-1`, take finite labels `Z_q`, and use label `q` for infinity.  The
literal corrected RR family has rows

* rank zero: `emptyset`;
* rank one: every finite singleton;
* rank `k`, `2<=k<=n-1`: infinity joined to every cyclic interval of finite
  length `k-1`; and
* rank `n`: the full set.

Thus the base family has `q` subsets at every internal rank and
`q^2+2=(n-1)^2+2` distinct literal subsets.  The checker reconstructs these
rows directly; it does not use a list of generating paths as the family.

After fixing infinity negative up to global sign, a balanced coloring is a
finite cyclic binary word of length `q` and weight `n/2`.  The forward
interval recurrence tracks all reachable odd-length cyclic intervals.  A
separate scalar implementation and a direct induced-literal-DAG search agree
on every normalized coloring through `n=12`.  This guards the recurrence
semantics before it is used for the larger exhaustive counts.

The fixed-density FKM recursion generates one least-rotation word per binary
necklace.  Since

\[
\gcd(n-1,n/2)=1,
\]

every orbit has exactly `q` members.  Matching the generated orbit total to
`binom(q,n/2)/q` therefore provides an exact exhaustion rather than a sample.

## 3. Exact certificates and algebraic relabelings

The first copy is normalized to the identity.  Every successful second copy
fixes infinity and uses the finite-cycle multiplier

\[
\pi_a(x)=a x\pmod q.
\]

The complete finite results are:

| `n` | `q` | normalized colors | one-copy rejected | rejected rotation orbits | multiplier `a` | common individual rejects | hybrid-only accepts | literal union subsets |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 22 | 21 | 352,716 | 21 | 1 | 2 | 0 | 0 | 821 |
| 24 | 23 | 1,352,078 | 414 | 18 | 2 | 0 | 0 | 991 |
| 26 | 25 | 5,200,300 | 4,700 | 188 | 2 | 0 | 0 | 1,177 |
| 28 | 27 | 20,058,300 | 40,392 | 1,496 | 4 | 0 | 0 | 1,379 |
| 30 | 29 | 77,558,760 | 292,407 | 10,083 | 5 | 0 | 0 | 1,597 |

The full permutations, rather than only their multiplier descriptions, are
stored in the JSON certificates.  The search used master seed `20260821`;
the successful candidates were algebraic and occurred before random trials,
but the derived per-`n` seed is still recorded for reproducibility.

For these particular multipliers the exact rank profile is

* one subset at ranks zero and `n`;
* `q` subsets at ranks one, two, and `n-1`; and
* `2q` subsets at every rank from three through `n-2`.

Thus the literal count is

\[
2+3q+2q(n-4)=2+(n-1)(2n-5),                 \tag{2}
\]

matching every stored direct set-union count.  Equation (2) counts distinct
literal subsets.  It does not count permutations, interval descriptions,
paths, or abstract states.

## 4. Individual coverage versus hybrid coverage

For a relabelled copy `F_j=pi_j(RR_n)`, let `R_j` be its rejection set on
global-sign orbits and put `R=intersection_j R_j`.

If `f` is not in `R`, a complete witness chain lies inside at least one
individual copy and hence inside the literal union.  Only colors in `R` can
possibly require a hybrid path.  The exact verification procedure is
therefore:

1. exhaust the one-copy failure necklaces and expand their rotations;
2. pull colors back through each stored permutation and compute `R` exactly;
3. form the literal subset union rank by rank and deduplicate it;
4. construct every inclusion-by-one edge between adjacent literal ranks; and
5. run color-compatible reachability in this full induced DAG for every
   member of `R`.

This is an exact reduction in workload, not a seed-path approximation.  In
all five successful certificates `R` is empty.  Hence all colors are covered
by an individual copy, `hybrid-only accepts = 0`, and the full union has zero
rejections.  The certificate makes that distinction explicit rather than
crediting unstored paths or assuming that hybrid paths do not exist.

## 5. Independent verification and hashes

The proposer/search program is
[`cycle04_multi_rr_search.cpp`](../experiments/cycle04_multi_rr_search.cpp).
It uses bit-parallel interval reachability and searches algebraic, affine, and
seeded random relabelings.

The independent deterministic checker is
[`cycle04_multi_rr_verify.py`](../experiments/cycle04_multi_rr_verify.py).
It does not import or invoke the C++ program.  It freshly:

* regenerates all fixed-weight necklaces;
* recomputes the complete RR rejection-orbit list;
* compares a scalar start-set recurrence, the fast recurrence, and direct
  literal-DAG acceptance through `n=12`;
* expands all failed rotations and verifies the stored FNV checksum;
* recomputes the permutation pullbacks and rejection intersection;
* deduplicates the literal union; and
* reconstructs every induced inclusion edge and tests all remaining colors.

In addition to that exact intersection-based proof, the independent checker
was run with `--direct-full-dag-n22`.  It traversed the full two-copy induced
DAG separately for all 352,716 normalized `n=22` colorings and returned zero
rejections.  This direct run does not use the common-rejection shortcut.

The complete independent run finished successfully with:

```text
PASS n=22 ... minimum_t_exact=2 ... literal_subsets=821
PASS n=24 ... minimum_t_exact=2 ... literal_subsets=991
PASS n=26 ... minimum_t_exact=2 ... literal_subsets=1177
PASS n=28 ... minimum_t_exact=2 ... literal_subsets=1379
PASS n=30 ... minimum_t_exact=2 ... literal_subsets=1597
ALL CYCLE-4 MULTI-RR CERTIFICATES PASS
```

The certificate index and SHA-256 manifest are in
[`cycle04_multi_rr_README.md`](../certificates/cycle04_multi_rr/cycle04_multi_rr_README.md)
and
[`cycle04_multi_rr_SHA256SUMS.txt`](../certificates/cycle04_multi_rr/cycle04_multi_rr_SHA256SUMS.txt).
At the recorded verification cutoff, the source SHA-256 values are
`5cf24180d1cf659cf0d6e040801b9cb79614403c76234aacc081887e7acbed40`
for the C++ search and
`29a616e5caff0dfd218f49cd9f24637132ffd212b792ebc826426b8a456fa6a5`
for the Python verifier.

## 6. Scope after the Cycle-4 stopping result

The separate Cycle-4 S4-D analysis obstructs the simple asymptotic route that
would lower-bound one-copy acceptance and then use independent relabelings
plus a union bound.  That obstruction does **not** prove that multi-copy
literal unions fail: hybrid paths can join states from different copies, so a
union may accept a coloring rejected by every constituent copy.  The present
successful finite lists happen not to need that phenomenon because their
individual rejection sets are disjoint.

Conversely, these finite two-copy certificates do not weaken the S4-D
asymptotic conclusion.  No pattern in the multipliers `2,2,2,4,5` is promoted
to an all-`n` conjecture or theorem, and no behavior at `n<=30` is extrapolated.
O01 remains open.

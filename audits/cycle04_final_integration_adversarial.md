# Research Cycle 4 final integration adversarial audit

**Date:** 2026-08-21
**Base commit:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Role:** independent repository-level mathematical, computational, formal,
and scope audit
**Verdict:** **PASS — no blocking correction required**
**Stopping disposition:** **S4-D for the individual-copy `RR_n`
acceptance/symmetrization route; O01 remains OPEN**

This audit treated the Cycle-4 reports and certificates as claims.  It read
the governing instructions and state, every report in `research_cycle_04/`,
the integrated result, both certificate indexes and manifests, the failure
ledger additions, the Lean source and coverage ledger, the obstruction audit,
and the mandatory barrier audit.  It then reran the independent checkers and
reconstructed the central logical interfaces.  It did not edit any research
report, state file, certificate, experiment, formal source, or literature
record.

## 1. Final verdict and exact scope

The Cycle-4 stopping theorem is sound at its stated restricted scope.  For
the corrected literal one-cycle family `RR_n`, if `A_n` denotes the fraction
of balanced colorings accepted by its full induced subset DAG, then an
absolute constant `c>0` satisfies

```text
A_n <= (n/2) 2^(-c(n-2)^(1/5))
```

for every sufficiently large even `n`.  This is a one-sided upper bound.  No
matching lower bound, equality asymptotic, or estimate of the constant is
claimed.

It follows that the proposed inverse-polynomial premise for single-copy
acceptance is false and that a cover whose witness for each coloring lies
inside one constituent relabelled copy requires stretched-exponentially many
copies.  It does **not** follow that a polynomial literal union of relabelled
copies fails: its full induced DAG may have chains that splice subsets from
different copies.  It also gives no lower bound on arbitrary balanced-chain
families or `N(n)`.

The integrated result, state, barrier audit, literature ledger, and failure
ledger all preserve that distinction.  They make no mABP, Boolean, algebraic,
or P-versus-NP separation claim.  O01 is correctly recorded as **OPEN**.

## 2. Symmetrization reduction audit

For a permutation `pi`, literal relabeling is a rank- and
inclusion-preserving bijection and satisfies

```text
d_f(pi(S)) = d_(f o pi)(S).
```

Thus `pi(F)` accepts fixed `f` if and only if `F` accepts `f o pi`, including
every path in the full induced subset DAG.  For any fixed balanced target
coloring, each balanced pulled-back coloring has exactly
`(n/2)! (n/2)!` permutation fibers.  Hence the success probability is the
acceptance fraction `A` of `F`.  Independent permutations give fixed-color
rejection probability `(1-A)^t`; no independence between different
colorings is used.

For `M=binom(n,n/2)` and `0<A<1`, the strict all-color union bound succeeds
exactly when

```text
M(1-A)^t < 1,
```

and the least positive integer certified by it is

```text
floor(ln M / -ln(1-A)) + 1.
```

The floor-plus-one correctly handles an integral quotient.  The endpoint
cases `A=1` and `A=0`, the optional global-sign-orbit sharpening, and the
nonuniform nature of the selected list are all handled correctly.

For `RR_n`, the audited rank profile is one subset at ranks zero and `n` and
`n-1` subsets at every internal rank.  A literal union of `t` relabelings
therefore has

```text
2 + sum_(k=1)^(n-1)
      |union_j pi_j(RR_n intersect rank k)|
<= 2 + t(n-1)^2
```

distinct subsets.  This counts neither descriptions nor paths.  Consequently
the hypothetical bound `A_n>=n^(-O(1))` really would imply O01, including the
finite exceptional values of `n`; there is no orientation, odd-intermediary,
fixed-family, or uniformity gap.

This qualitative reduction is correctly attributed rather than claimed as
new.  The primary [ECCC TR26-001 full version](https://eccc.weizmann.ac.il/report/2026/001/)
states it as Lemma 2.3 (Lemma 1.5), and the published
[CCC 2026 paper](https://doi.org/10.4230/LIPIcs.CCC.2026.22) states it as
Lemma 14 (Lemma 6).  The exact binomial threshold and collision-aware literal
count are elementary refinements.

## 3. Rooted reduction and FLSY dependency

The central reduction was reconstructed in both directions.  Normalize
`f(infinity)=-1`, so the finite cycle `Z_q`, `q=n-1`, has total sign `+1`.
For a fixed finite rank-one root `r`, a literal RR chain is forced to use
nested cyclic intervals

```text
I_1={r} subset ... subset I_q=Z_q.
```

The rank-two state `{infinity,r}` forces `f(r)=+1`.  Cutting the cycle at `r`
and defining

```text
J_s = Z_q \ I_(q-s)
```

gives a maximal chain of ordinary intervals on the remaining `n-2` points.
Conversely, complementing and reversing any such ordinary-interval chain
gives literal RR states at every rank.  The exact discrepancy identity

```text
f(J_s) = -f({infinity} union I_(q-s))
```

proves compatibility both ways and explicitly covers the endpoints, rank
one, rank two, every odd intermediary, and the full set.

For a fixed root, `Pr[f(r)=+1]=(n/2)/(n-1)`, and after conditioning the
restriction is uniform balanced on the fixed ordered set of `n-2` points.
If `p_N` is ordinary one-interval acceptance probability, then

```text
Pr[root-r witness] = ((n/2)/(n-1)) p_(n-2).
```

Union-bounding over the `n-1` possible roots, without assuming independence,
gives `A_n <= (n/2)p_(n-2)`.

The external theorem was checked directly in the primary source.  FLSY
Definition 2.1 defines `I_(N,1)` as the empty set and ordinary intervals.
Theorem 4.4 (Theorem 1.7), published as Theorem 23 (Theorem 8), states that a
universal `c>0` exists such that for all sufficiently large even `N` the
family is not `(epsilon,k)`-balanced-chain when

```text
epsilon > 2^(-cN^(1/5))  and  k < N^(1/5).
```

Taking `k=1` is valid for sufficiently large `N`.  The theorem's strict
inequality in `epsilon` still implies `p_N<=2^(-cN^(1/5))`: if `p_N` were
larger, an intermediate `epsilon` would contradict the theorem.  Here
`N=n-2` is even and tends to infinity.  Absorbing the polynomial prefactor
requires only a changed absolute constant and a larger threshold.  These
quantifiers justify S4-D exactly as recorded.

## 4. Exact RR acceptance evidence

The literal RR definition, corrected seed-prefix union, cyclic-interval
recurrence, and direct full induced-DAG predicate were independently compared.
The exact normalized counts retained are:

| `n` | total | accepted | rejected | rejected rotation orbits |
|---:|---:|---:|---:|---:|
| 22 | 352,716 | 352,695 | 21 | 1 |
| 24 | 1,352,078 | 1,351,664 | 414 | 18 |
| 26 | 5,200,300 | 5,195,600 | 4,700 | 188 |
| 28 | 20,058,300 | 20,017,908 | 40,392 | 1,496 |
| 30 | 77,558,760 | 77,266,353 | 292,407 | 10,083 |
| 32 | 300,540,195 | 298,654,992 | 1,885,203 | 60,813 |
| 34 | 1,166,803,110 | 1,155,611,853 | 11,191,257 | 339,129 |

All hashes and aggregate orbit/run statistics match the stored payloads.
The independent Python implementation recounted every fixed-weight necklace
through `n=30`, reproducing all five failure lists exactly.  Through `n=34`,
it checked every stored failure representative, canonical rotation,
reflection pairing, and recorded histogram.  The stated trust boundary is
accurate: completeness at `n=32,34` rests on the separately inspected and
rerun exhaustive C++ producer rather than a second full Python recount.

No finite trend is used for the asymptotic theorem.  The stored `n=30`
maximum-run-four rejection correctly falsifies only the unqualified finite
run-length sufficient condition recorded in `RC4-RR-02`.

## 5. Multi-RR certificate audit

The five finite results

```text
t_RR(22)=t_RR(24)=t_RR(26)=t_RR(28)=t_RR(30)=2
```

pass.  In every case one copy has a nonempty rejection set, proving the lower
bound.  The second stored permutation fixes infinity and multiplies finite
labels modulo `n-1` by `2,2,2,4,5`; the verifier freshly exhausts the one-copy
failure necklaces and finds the two individual rejection sets disjoint.
Therefore every coloring has a witness wholly in one copy, which is already
an exact proof for the literal union; no seed-path assumption is involved.

The verifier nevertheless reconstructs and deduplicates every literal subset
and every adjacent-rank inclusion edge.  The distinct-subset counts are

```text
821, 991, 1177, 1379, 1597
```

and agree with `2+(n-1)(2n-5)`.  A separate direct traversal of the full
two-copy induced DAG on all 352,716 normalized `n=22` colorings found zero
rejections.  For `n=24,...,30`, the exact empty intersection of individual
rejection sets makes an all-color full-DAG traversal logically redundant;
the checker correctly records zero hybrid-only acceptances rather than
claiming that hybrid paths do not exist.

These are exact finite results only.  No constant-`t`, polynomial-`t`, or
all-`n` multi-RR statement follows from them.

## 6. Formal verification audit

The pinned Lean 4.32.1/mathlib 4.32.1 build completed all 8,656 jobs.  Direct
elaboration with trust level zero also exited successfully.  The source has
no `sorry`, `axiom`, `admit`, `unsafe`, or `opaque` declaration.

The named Cycle-4 declarations have the stated meanings:

* `acceptsColoring_relabel_iff` proves full-family acceptance equivariance;
* `isOneBalancedChain_relabel_iff` proves worst-case invariance;
* `iUnion_isOneBalancedChain_of_pointwise_accepts` embeds an individual
  witness into a literal indexed union; and
* `union_relabelings_isOneBalancedChain` specializes that step to relabelled
  copies.

The formal boundary is not overstated.  Random-permutation fibers,
independence, the union bound, exact `t`, distinct-subset cardinality, the
literal RR family, deque/rooted equivalence, the FLSY theorem, finite
enumerations, and O01 remain unformalized.  Phase 4A is correctly labelled
`PARTIALLY FORMALIZED`.

## 7. Reproduction record

The following independent commands exited successfully during this audit:

```powershell
python -B experiments/cycle03_verify_foundation.py
python -B experiments/cycle03_check_cp_m_matching.py
python -B audits/check_cycle03_cp_m_adversarial.py
python -B research_cycle_04/cycle04_probability_interval_reduction.py
python -B experiments/cycle04_rr_verify_counts.py
python -B experiments/cycle04_rr_verify_counts.py --skip-literal-equivalence --recount-through 30
python -B experiments/cycle04_multi_rr_verify.py
python -B experiments/cycle04_multi_rr_verify.py --skip-small-semantic-audit --direct-full-dag-n22 certificates/cycle04_multi_rr/cycle04_multi_rr_n22.json
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

The rooted checker tested 15,591 fixed-positive-root instances through
`n=14`.  The RR recount visited respectively
`16,796, 58,786, 208,012, 742,900, 2,674,440` necklaces for
`n=22,24,26,28,30`.  The direct multi-RR run tested all 352,716 normalized
`n=22` colorings.  Both certificate manifests passed SHA-256 verification;
all twelve Cycle-4 JSON files and all 34 failure-ledger JSONL records parsed,
with unique failure IDs.

The repository-level checker is
[`check_cycle04_integration_adversarial.py`](check_cycle04_integration_adversarial.py).
It verifies the frozen arithmetic, permutations, distinct-subset profiles,
manifests, source-hash claims, JSONL IDs, formal boundary, one-sided/scope
language, relative Markdown links, base commit, and absence of temporary
executables or Python caches.

## 8. Consistency, correction list, and stopping boundary

`README.md`, `RESEARCH_STATE.md`, the integrated result, the literature map,
novelty log, failure ledger, formal ledger, certificate reports, obstruction
audit, and barrier audit agree on all material statuses and numbers.  The
relative links resolve, the manifests match, and no generated `.exe`, Python
bytecode, or other temporary research artifact remains outside ignored build
caches.

**Required corrections:** none.

At audit time the working tree contains the intended uncommitted Cycle-4
research artifacts, so it is not yet Git-clean; it is clean-commit ready once
this audit and checker are included.  The final integrator must still run the
repository checker, commit the completed state, and verify an empty
`git status --short` afterward.

Cycle 4 must stop under S4-D after that commit.  This audit does not authorize
or begin Research Cycle 5.

## Post-audit integration note

After the initial PASS, the integrator removed a stale pre-Cycle-4 sentence
from `literature/open_problems.md` and added the correctly scoped S4-D
disposition, then changed `rooted_interval_obstruction.md` from
pending-integration metadata to the completed audit status.  A follow-up
found and prompted correction of one remaining “audit pending” sentence in
that report.  The two files are now mutually consistent: O01 remains open,
S4-D concerns only individual-copy acceptance, hybrid literal-union chains
remain outside the obstruction, and Cycle 5 has not begun.  The integration
checker was rerun after the correction and passed.

## Final staging reproducibility note

The staged `.gitattributes` rules were independently checked after the
post-audit update.  They set `text eol=lf` for `.gitattributes` itself, both
complete Cycle-4 certificate trees, and the two multi-RR source files whose
SHA-256 values are recorded in the report.  `git check-attr` confirms the
rule on all 31 protected paths.  For every protected path, the staged blob ID
equals `git hash-object --no-filters` on the current file, so the manifest
checks are testing the same bytes that will be committed.  Because the
explicit `eol=lf` attribute governs checkout conversion, those evidence bytes
remain LF-stable even when a Windows clone has `core.autocrlf=true`.

Both certificate manifests, the Cycle-4 integration checker,
`git diff --check`, and `git diff --cached --check` passed after the
attributes and Markdown whitespace normalization.  This final staging-only
fix preserves every mathematical result and closes the raw-byte
reproducibility issue.

## Committed-state checker note

After the initial Cycle-4 commit, the integrator found that the repository
checker still required `HEAD` to equal the pinned base commit.  That was the
correct pre-commit condition but would make the committed checker reject its
own intended descendant state.  The check now requires the pinned base to be
an ancestor of `HEAD`; it accepts both the pre-commit base state and the
committed Cycle-4 state while still rejecting unrelated histories.  The
checker was rerun successfully after this correction.

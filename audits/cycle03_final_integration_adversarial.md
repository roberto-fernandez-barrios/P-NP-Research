# Cycle 3 final adversarial audit: CP-M, Lean, and integration

**Audit date:** 2026-08-21
**Frozen base commit:** `e942729da8db176848354d8d0161e85bcee7c080`
**Role:** independent adversarial falsifier and final integrator
**Scope:** corrected CP-M report, Lean artifact and its separate formal audit,
the integrated Cycle-3 result/state/index files, the top-level README, and the
five CP-M failure-ledger records
**Status boundary:** the CP-M mathematical claims below are `INDEPENDENTLY
REPRODUCED/ADVERSARIALLY REVIEWED; UNFORMALIZED` unless a narrower finite
computational status is stated. Only the explicitly listed Lean statements are
`FORMALLY VERIFIED`, and only within their encoded model. O01 remains **OPEN**.

This is stage 2 of the independent Cycle-3 audit. Stage 1 is
[`cycle03_n10_structural_adversarial.md`](cycle03_n10_structural_adversarial.md).

## 1. Final disposition

| Claim or artifact | Disposition | Exact qualification |
|---|---|---|
| Canonical-support lemma for fixed-length syntactically read-once pair programs | **PASS** | The liveness, fixed-length, and syntactic read-once hypotheses are all necessary and are stated. The result is a normalization, not `Q(n)=N(n)`. |
| `Q(n) <= N(n) <= Q(n)+min(Q(n)^2,Q(n) binom(n,2))` | **PASS** | Distinct canonical even supports and distinct inclusion-by-two edges are counted correctly; odd intermediaries are charged by distinct subsets. This is a polynomial-existence equivalence only. |
| Exact ordered-matching prefix-union reductions for `N` and `Q` | **PASS** | Both directions survive hybrid paths. A seed collection need not list all paths induced by its literal prefix union. |
| Round-robin interval family `RR_n` has `(n-1)^2+2` distinct subsets | **PASS** | Exact literal subset accounting, not a path-description count. |
| Interval/deque characterization of `RR_n` connectivity | **PASS** | Independently compared with the full induced subset DAG, not just the generating factor paths. |
| Claimed `n=10` factor-menu obstruction | **RETRACTED, CORRECTLY RECORDED** | The listed factors do not cover the displayed cut, but the literal family does via a hybrid path. It is not an `RR_10` counterexample. |
| `RR_n` valid for every even `n<=20`, first fails at `n=22` | **PASS, FINITE EXHAUSTIVE** | After fixing the infinity sign, every balanced finite cyclic word was exhausted. At `n=22` the 21 failures are exactly one rotation orbit. |
| Four-run obstruction for every even `n>=22` | **PASS, UNFORMALIZED** | The recurrence and stable induction were checked independently, with the exceptional `m=11` and `m=12` transitions separated. It obstructs only this one-cycle interval family. |
| Full-submatching, stage-only, and color-signature quotients | **PASS AS FAILURES** | Their exponential accounting or unsafe-splicing examples do not imply lower bounds for arbitrary shared matching DAGs or for `N(n)`. |
| Lean build and theorem scope | **PASS** | Clean pinned build; central theorem axiom reports contain only standard classical/quotient axioms and no `sorryAx`. The order-theoretic maximal-chain equivalence and all exact `N`, `tau`, `sigma`, CP-class, and O01 claims remain outside Lean. |
| Final Cycle-3 integration | **PASS** | Required CP-S/G/n10 wording repairs are present; CP-M language is corrected throughout; epistemic status, S3-D stopping, links, ledger, and no-Cycle-4 boundary are consistent. |

No audited claim proves a polynomial O01 construction. No mABP separation or
complexity separation is claimed.

## 2. Independent CP-M checker and method

The new checker
[`check_cycle03_cp_m_adversarial.py`](check_cycle03_cp_m_adversarial.py) does
not import the proposer program. The proposer used memoized recursive deletion;
the audit instead propagates all reachable cyclic-interval starts **forward**.
For small sizes it separately searches every inclusion-by-one edge of the
literal subset family. This difference is important: restricting the search to
the generating factor paths would repeat the exact error under audit.

The checker independently verifies:

* the round-robin one-factorization and its literal prefix family;
* the family rank profile and exact distinct-subset count through `n=22`;
* the failed `n=10` seed menu and the successful hybrid witness;
* equality of the forward interval recurrence and literal-DAG acceptance for
  every normalized balanced coloring through `n=12`;
* exhaustive validity through `n=20` and the full failure set at `n=22`;
* the proposed four-run closed forms for every `11<=m<=300`, as corroboration
  of the symbolic induction below; and
* the three unsafe quotient/accounting examples.

Its SHA-256 at this audit cutoff is

```text
f7341d0d41870c4e6d14cc054da5b9eb15b5288511c35e0141b523c4b7086d26
```

The substantive terminal output was:

```text
PASS exact RR_n factorization, interval states, and size ... 22: 443
PASS n=10 seed-menu failure but literal hybrid success
PASS forward interval recurrence equals literal induced DAG ...
PASS exhaustive first RR_n failure at n=22 ... 20: 0, 22: 21
PASS four-run closed forms in broad finite audit ... 11 through 300
PASS unsafe matching-state quotient/accounting checks
ALL CYCLE-3 CP-M ADVERSARIAL CHECKS PASS (FINITE SCOPE)
```

The finite loop to `m=300` is not being used as an all-`m` proof. The proof is
the transition analysis in Section 6.

## 3. Canonical support and `Q` accounting

### 3.1 Unique support

Let `v` be a live vertex of a pair-labelled DAG in which every source-to-sink
path has exactly `m=n/2` edges and every such path has pairwise-disjoint edge
labels. If two source-to-`v` prefixes have supports `A` and `B`, choose one live
suffix from `v` to the sink and call its support `D`. Both concatenations are
full syntactically read-once paths, hence

`A intersect D = B intersect D = emptyset`

and each uses `m` disjoint pairs, hence all `n` ground elements. Therefore

`A union D = U = B union D`, so `A=B=U minus D`.

This also forces an edge labelled `e` from `u` to `v` to satisfy
`S_v=S_u union e`, with `S_u` disjoint from `e`. Merging vertices having the
same support is safe: every entering prefix uses exactly `S`, every outgoing
suffix uses `U minus S`, and any splice remains syntactically read-once.

The argument fails if dead vertices are retained without qualification, full
paths have different lengths, or read-once behavior is enforced by hidden path
history rather than graph syntax. The report states these hypotheses.

### 3.2 Relating `Q` and `N`

Contracting pairs of consecutive single-element steps in a
1-balanced-chain family produces a canonical even-support DAG, so `Q<=N`.
Conversely, for each distinct even-to-even edge choose either of its two odd
intermediary subsets. Adding all chosen odd subsets expands every open pair
path into an actual selected maximal chain, so `N<=V+E`.

After duplicate parallel edges are removed, an ordered support pair determines
at most one edge, giving `E<=V^2`. Each support also has at most `binom(n,2)`
inclusion-by-two successors, giving `E<=V binom(n,2)`. Applying this to an
optimum `V=Q` proves

`Q(n) <= N(n) <= Q(n)+min(Q(n)^2,Q(n)*binom(n,2)).`

This does not assert equality of the exact minima. Distinct edges can share an
odd intermediary subset, and `N` counts distinct odd states rather than an edge
description.

## 4. Exact prefix-union reductions and hybrid paths

For an oriented ordered perfect matching, concatenate its oriented pairs and
take all literal subset prefixes. A cut-covering collection of these objects
immediately supplies a valid family. Conversely, from any valid family choose
one witness chain for each balanced coloring. The chains induce a cut-covering
collection, and their prefix union is contained in the original family. This
proves the exact minimum identity for `N`.

The even-support identity for `Q` is analogous. A collection of ordered
unoriented perfect matchings produces its union-of-even-prefixes DAG. In the
reverse direction, delete dead material from an optimum canonical DAG and take
all its source-to-sink paths; every remaining support lies on one and therefore
appears in the resulting prefix union.

Hybrid paths do not invalidate either reverse direction. If a seed prefix
union accepts a coloring only through a hybrid chain, add that already selected
chain to the path collection. Its literal prefix union does not grow. What is
invalid is the stronger claim that every accepted color is crossed by one of
the originally listed seed matchings.

At `n=10`, plus set `{0,1,2,3,6}` has crossing-edge counts
`3,3,3,3,3,3,1,3,3` in the nine seed factors, so none is a perfect crossing
matching. Nevertheless the literal family contains every prefix of

`3,9,4,2,5,6,7,1,8,0`,

and each consecutive pair crosses. This independently confirms both the old
menu-only claim's retraction and the corrected semantics.

## 5. Exact `RR_n` accounting and deque equivalence

Put `q=n-1` finite points on `Z_q` and add `infinity`. The factor centered at
`r` is ordered

`r,infinity,r+1,r-1,...,r+(m-1),r-(m-1)`.

Rank one contains the `q` finite singletons. At each rank `2<=k<=n-1`, the
states are exactly `infinity` together with a cyclic interval of `k-1` finite
points. There are `q` distinct proper intervals of each length. The endpoints
are common to all paths, so the number of distinct subsets is

`2 + q(n-1) = 2+q^2 = 2+(n-1)^2`.

This also exposes all hybrid edges. After globally reversing signs if needed,
fix `infinity` minus. The finite cyclic word has `m` ones and `m-1` zeros. A
selected path begins at a plus singleton, adds infinity, and thereafter grows
one finite cyclic interval by one endpoint at each single-element step. Across
each pair of steps it must add one plus and one minus.

Equivalently, in reverse, a current linear interval may delete an
opposite-sign pair from its left end, right end, or two opposite ends. The last
pair of any selected path is necessarily one of these three boundary choices,
so the recurrence is complete, not only sufficient. Reversing accepted
deletions gives actual inclusion edges between literal `RR_n` states, proving
color-specific connectivity.

The audit compared this characterization to a direct literal-DAG search for
all normalized balanced colors at `n=2,4,6,8,10,12`. It did not constrain the
direct search to factor centers, and the two predicates agree everywhere.

## 6. First failure and the all-size obstruction

Fixing infinity minus is exhaustive up to global sign reversal: every balanced
signed coloring has exactly one normalized representative, whose finite word
has `m` ones. Exhausting all `binom(2m-1,m)` such words gives no failure for
even `n<=20`. At `n=22`, precisely 21 words fail, exactly the rotations of

`111111110000011100000 = 1^8 0^5 1^3 0^5`.

The SHA-256 of the sorted, newline-delimited failure words is
`ea61fa625c178336031605dcb22349e167b8e9ed3b42698b8ea383b507e44581`.
For the displayed rotation, reachable interval starts at lengths
`1,3,5,7,9,11,13` have cardinalities `11,4,5,2,2,4,0`, respectively. The
empty length-13 row is already a literal-DAG disconnection certificate.

For the general statement, let

`w_m=1^(m-3) 0^5 1^3 0^(m-6)` for `m>=11`,

and let `R_l` contain the starts of reachable cyclic intervals of odd length
`l`, modulo `q=2m-1`. The exact transition is

```text
R_(l+2) = {i-2 : i in R_l and w[i-2] != w[i-1]}
        union {i-1 : i in R_l and w[i-1] != w[i+l]}
        union {i   : i in R_l and w[i+l] != w[i+l+1]}.
```

Substitution at the four run boundaries gives

```text
R_3 = {m-5,m+1,m+3,2m-2}
R_5 = {m-6,m,m+1,m+2,2m-3}
R_7 = {m-7,2m-4}
R_9 = {m-8,2m-5}.
```

The exceptional tails are:

* `m=11`: `R_11={2,3,15,16}` and `R_13=emptyset`;
* `m=12`: `R_11={3,4,18}`, `R_13={16,17}`, and `R_15=emptyset`.

For `m>=13`, `R_11={m-9,m-8,2m-6}`. Inductively, for
`6<=t<=m-7`,

`R_(2t+1)={2m-t-1}`.

Until the last step the only active boundary is the wrap from the final zero
run to the initial one run, so the start decreases by one at each extension.
At the endpoint it branches to
`R_(2m-11)={m+4,m+5}`. Substitution of both starts into the three boundary
tests yields no child, hence `R_(2m-9)=emptyset`. This proves failure before a
full finite interval is reached for every `m>=11`.

The proof is a precise obstruction to `RR_(2m)`, not to other cyclic orders,
a polynomial union of orders, arbitrary shared matching-state DAGs, or O01.

## 7. Unsafe quotient checks

The negative accounting examples are correctly scoped:

* A fixed perfect matching has `2^m` distinct submatching unions, so closing
  that one matching under all pair orders is already exponential. This is not
  a lower bound for more selective shared states.
* A stage-only selector that permits every disjoint next pair generates every
  even subset, totaling `2^(n-1)` even supports. This refutes that literal
  construction, not arbitrary canonical DAGs.
* At `n=4`, supports `{0,1}` and `{2,3}` have the same balanced-color
  compatibility signature. Merging them can splice an incoming `{0,1}` edge
  to an outgoing edge with the same label, repeating variables rather than
  reaching the full support. Thus compatibility signatures alone are not a
  safe canonical quotient.

The failure ledger preserves these as retries with explicit scope rather than
converting them into general lower bounds.

## 8. Lean trust and scope audit

The pinned environment is Lean `v4.32.1` with the matching Mathlib revision.
Both

```powershell
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
lake env lean -t 0 BalancedChain.lean
```

completed successfully. Direct `#print axioms` checks for the central
consecutive-pair/path/S1/S2 results report only `propext`, `Classical.choice`,
and `Quot.sound`; no `sorryAx` is present. The hardened check script now scans
standalone `axiom`, `sorry`, and `admit` tokens rather than using the former
line-leading token regex. The separate
[`formal_adversarial_audit.md`](../research_cycle_03/formal_adversarial_audit.md)
correctly records that repair as resolved.

The accepted scope is intentionally narrower than the informal mathematical
development. `MaximalChain` is represented by an insertion order, and
`ContractedPath` is defined through that same order. Lean does not separately
prove equivalence with every order-theoretic maximal chain or construct an
independent graph object with subset-accounting semantics. Within the encoded
model it verifies balanced coloring, family witnessing, the consecutive-pair
characterization, path reformulation, and Lemmas S1/S2. It does not verify
exact `N(10)`, `tau`, `sigma`, CP-S/P/G/M, any recursion, O01, or an asymptotic
claim.

## 9. Final integration checks

The static checker
[`check_cycle03_integration_adversarial.py`](check_cycle03_integration_adversarial.py)
parses all repository Python and JSON outside build caches, resolves the local
links in the Cycle-3 artifacts and top-level README, validates the full JSONL
ledger schema and unique IDs, specifically checks CP-M records `01` through
`05`, and guards the O01/formal/CP-M/stopping-condition language. Its SHA-256
at this audit cutoff is

```text
1939ef194478161fa60173435118bd8897d9744d1a7203cbb92eab2bc33eb0a7
```

The integrated files
[`results/research_cycle_03.md`](../results/research_cycle_03.md),
[`RESEARCH_STATE.md`](../RESEARCH_STATE.md),
[`research_cycle_03/README.md`](../research_cycle_03/README.md), and
[`README.md`](../README.md) consistently state:

* exact finite `N(10)=35`, with the size-30 lead falsified;
* O01 remains **OPEN** and no finite-to-asymptotic inference is made;
* CP-M's seed-menu `n=10` claim was retracted, while literal `RR_n` succeeds
  through `n=20` and first fails at `n=22`;
* Lean status is limited to the encoded core;
* Cycle 3 stops under S3-D; and
* Research Cycle 4 has not begun and is not started automatically.

The five appended CP-M failure records are valid JSON, uniquely identified,
and preserve the needed boundaries: seed-menu necessity only; the exact
one-cycle interval family only; no lower bound from stage selectors; no safe
quotient from color signatures; and no general lower bound from full
submatching closure.

Stage 1 required narrow corrections to CP-SQ's domain/anchor scope, CP-S's
“first class failure” wording, CP-G endpoint hypotheses, and the `n=10`
certificate digest description. They are all present in the final files.
No stale statement treating the `n=10` seed-menu miss as a literal CP-M-family
failure remains.

## 10. Final boundary

**FINAL CYCLE-3 ADVERSARIAL INTEGRATION: PASS.**

This PASS establishes only the qualified finite, structural, and encoded
formal claims listed above. It does not establish a general polynomial-size
construction. The most informative surviving CP-M direction is the exact
prefix-union/canonical-support reduction; the tested quadratic one-cycle
family is decisively obstructed from `n=22` onward. O01 remains **OPEN**.

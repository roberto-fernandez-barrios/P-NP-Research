# Research Cycle 3: independent foundation and scope audit

**Audit date:** 2026-08-21
**Frozen base commit:** `e942729da8db176848354d8d0161e85bcee7c080`
**Role:** independent Phase 3A mathematical verifier / adversarial falsifier
**Scope:** definitions, consecutive-pair characterization, exact path-DAG
reformulation, Lemmas S1--S2, `tau`, `L`, `sigma`, exact-certificate
dependencies, and CF-LOGGAP scope only. No new construction is proposed.
**Formal status:** `UNFORMALIZED`; the checks below are finite computations,
not Lean proofs.
**Novelty status:** not assessed here.

## Executive disposition

| Item | Disposition | Precise status |
|---|---|---|
| FLSY/set-system definition used by Cycle 2 | **PASS** | Matches Definition 1.2 and the definition of `N(n)` in Theorem 3.3 of the active FLSY paper, for positive even `n`. |
| Consecutive-pair characterization | **PASS** | Complete elementary proof; independently checked for every permutation and balanced coloring through `n=8`; `ADVERSARIALLY REVIEWED; UNFORMALIZED`. |
| Contracted path-DAG reformulation | **QUALIFIED PASS** | Exact for path existence. Polynomial-size equivalence is correct for a **subset-labeled** DAG after accounting for odd intermediaries/edges. Raw DAG vertex count is not exactly `N(n)`. |
| Lemma S1 | **PASS** | Quantifiers and countercolor are correct, including `n=2`; `ADVERSARIALLY REVIEWED; UNFORMALIZED`. |
| Lemma S2 | **PASS** | Correct complement/reversal dual of S1; `ADVERSARIALLY REVIEWED; UNFORMALIZED`. |
| `tau(n,k)`, `L(n)`, and `sigma(n)` | **PASS WITH INTERPRETIVE CAVEAT** | The definitions, lower bound, and values through `n=8` are correct. `sigma` is an aggregate cross-level coherence surcharge, not automatically the size of a canonical bridge set. |
| Exact `n=2,4,6,8` dependencies | **PASS** | Existing checker reran successfully; a new independent formulation also accepted all upper families and recomputed every `tau` value. No claim is made for `n>=10`. |
| CF-LOGGAP isolation | **PASS** | No checked conclusion transfers to a general subset DAG, shared-state family, unrestricted `N(n)`, or O01. |
| Repository-wide consistency of the fixed-chain count | **FAIL (stale Cycle-1 text only)** | Two older audit files say one chain covers two colorings. The correct number is `2^(n/2)`. Current Cycle-2 structural files use the correct count. |

No counterexample was found to the path-DAG equivalence, S1, S2, or the
`tau`/`sigma` dependencies. This audit does not prove O01 and makes no
asymptotic inference from the finite systems.

## 1. Inputs and independent baseline

I read the repository instructions and research state before checking the
claims. The principal foundation inputs treated as untrusted were:

- `AGENTS.md`, `INITIAL_RESEARCH_MISSION.md`, and `RESEARCH_STATE.md`;
- `research_cycle_02/small_system_structure.md`;
- `research_cycle_02/exact_balanced_chain_values.md`;
- all files in `certificates/balanced_chain_exact/`;
- `experiments/balanced_chain_optimize.py` and
  `experiments/check_balanced_chain_certificates.py`;
- `audits/cycle02_exact_n_adversarial.md` and
  `audits/cycle02_exact_n_disposition.md`;
- `research_cycle_02/construction_family_obstruction.md` and the two CF-LOGGAP
  scope/disposition audits; and
- the Cycle-2 result, failure ledger, and formal-coverage ledger.

I also checked the definition against the current official primary source,
[Fabris--Limaye--Srinivasan--Yehudayoff, ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/download/),
especially Definition 1.2, the read-once branching-program description in the
introduction, and Theorem 3.3's definition of `N(n)`.

The independent finite implementation is
`experiments/cycle03_verify_foundation.py`. It imports neither Cycle-2
program. It uses the literal imbalance formula, a fresh Boolean-lattice path
search, a separately implemented contracted-pair search, exhaustive family
enumeration at `n<=4`, and fresh layer-cover enumeration through `n=8`.

## 2. Definition and boundary audit

Fix a positive even integer `n` and write `m=n/2`. A balanced coloring is
equivalently a plus set `P subseteq [n]` of size `m`. For `S subseteq [n]`,

`d_P(S)=2|S intersect P|-|S|`.

A family `X subseteq P([n])` is 1-balanced-chain exactly when

`for every P with |P|=m, there exists a maximal chain C_0,...,C_n in X`

such that `|d_P(C_i)|<=1` for every `i`. The quantifier order is
`for every coloring, there exists a chain`; it is not a single chain required
to work for every coloring.

Boundary consequences are sound:

1. A maximal chain has `C_0=emptyset`, `C_n=[n]`, and one vertex at every
   level. Since a positive even `n` has balanced colorings, every valid `X`
   contains both endpoints.
2. The empty and full sets have imbalance zero for every balanced coloring.
   Consequently `tau(n,0)=tau(n,n)=1`.
3. Positive even `n` is essential. For odd `n` there is no balanced
   `{+1,-1}` coloring, so extending only the universal quantifier literally
   would make the property vacuous. The repository correctly restricts O01
   to positive even `n`.
4. If one separately extended the definition to `n=0`, the only balanced
   coloring and maximal chain are both empty, giving a one-set base case.
   This is outside O01 and is not used by S1 or S2.
5. Whether the maximum in the paper is written over indices `1,...,n` or
   `0,...,n` is immaterial here: the omitted empty prefix has imbalance zero.

No endpoint, empty-set, sign-complement, or `P` versus `P^c` mismatch was
found in the Cycle-2 exact certificates or checkers.

## 3. Consecutive-pair characterization

### Claim

Let a maximal chain add the elements in order
`(pi_1,...,pi_n)`. It is 1-balanced for `P` if and only if every pair

`{pi_1,pi_2}, {pi_3,pi_4}, ..., {pi_(n-1),pi_n}`

crosses the cut `(P,[n] minus P)`.

### Independent proof

At an even level `2j`, `d_P(C_(2j))` is an even integer. If its absolute value
is at most one, it must be zero. Hence

`0=d_P(C_(2j))-d_P(C_(2j-2))`

is the sum of the two newly added signs, so those signs are opposite.
Conversely, if each consecutive pair has opposite signs, every even prefix
has imbalance zero and every odd prefix has imbalance `+1` or `-1`. This is
exactly the required chain.

The choices of which member of each pair is positive are independent. Thus a
fixed chain is good for exactly

`2^m = 2^(n/2)`

signed balanced colorings, not two colorings.

### Finite falsification result

The independent checker tested the equivalence for every permutation and
every signed balanced coloring at `n=2,4,6,8`. The numbers accepted per chain
were respectively `2,4,8,16`, exactly `2^(n/2)`.

## 4. Exact contracted subset-DAG reformulation

The informal contraction in `small_system_structure.md` is correct after the
objects and accounting convention are made explicit.

### 4.1 Exact graph associated with a family

For a family `X`, define `H_X` as follows.

- Its vertices are the selected even sets
  `V_X={S in X: |S| is even}`.
- There is an arc `S -> T` when `S subset T`, `|T minus S|=2`, and at least
  one of the two odd intermediaries `U` with `S subset U subset T` lies in
  `X`.
- The arc label is the forced pair `T minus S`.
- On coloring `P`, retain an arc exactly when its label is bichromatic.

Then `X` has a good maximal chain for `P` if and only if `H_X` has an
`emptyset`-to-`[n]` open path.

### 4.2 Proof in both directions

Contracting the two one-element steps from `C_(2j)` through `C_(2j+1)` to
`C_(2j+2)` produces an arc of `H_X`. Section 3 shows its label is
bichromatic.

Conversely, take an open path in `H_X`. For each arc choose one selected odd
intermediary witnessing that arc. Since every arc adds a crossing pair,
induction from the empty set gives imbalance zero at every even state. Either
odd intermediary has imbalance `+1` or `-1`. Expanding every arc therefore
gives a selected 1-balanced maximal chain.

The independent checker compared the uncontracted compatible Boolean-DAG
search with this contracted search for every one of the `16` families on two
points and all `65,536` families on four points, for every signed balanced
coloring. No mismatch occurred. It also checked both formulations on every
stored upper family through `n=8`.

### 4.3 Accounting qualification

This is an exact equivalence of **path functionality**, but raw sizes depend
on normalization:

- `N(n)` counts every distinct odd and even subset in `X`;
- the contracted graph's vertex count counts only even subsets; and
- an edge count or a general branching-program vertex count is a third
  quantity.

For O01's polynomial-existence question the normalization can be converted
without loss of polynomiality. From a size-`s` family one gets at most `s`
even vertices. Conversely, from a subset-labeled even-state DAG with `q`
vertices, choose one odd intermediary per arc and take their union with the
even vertices. Each even state has at most `binom(n,2)` possible inclusion-by-
two successors, so

`|X| <= q + |E| <= q(1+binom(n,2))`.

Thus polynomial-size existence is equivalent. Exact minima are not
identical. This normalization warning is already stated correctly in
`research_cycle_02/literature_novelty_audit.md`; it should remain attached to
the shorter formulation in `small_system_structure.md`.

The word **subset** is also essential. A general nondeterministic read-once
branching-program vertex may merge paths having different used-variable
sets. Such a control state does not automatically name one subset and cannot
be counted as one member of `X`.

## 5. Lemmas S1 and S2

### 5.1 Lemma S1 — PASS

Assume `X` is 1-balanced-chain and its unique singleton is `{v}`. Let

`Gamma={u != v: {v,u} in X}`.

Every witness chain has `C_1={v}`, hence its level-two vertex must be
`{v,u}` for some `u in Gamma`; every selected pair not incident with `v` is
unreachable in every maximal chain contained in `X`.

If `|Gamma|<=m-1`, choose a plus set `P` of size `m` containing
`{v} union Gamma`. This is possible because that prescribed set has size at
most `m`. Every reachable level-two set then has imbalance `+2`, contradicting
the existence of a 1-balanced witness. Therefore `|Gamma|>=m=n/2`.

The proof handles `n=2`: if no incident pair were selected, take `P={v}` and
the chain already fails at level two. The independent checker exhaustively
verified S1 over every valid family at `n=2,4`, and separately checked the
countercolor construction for every even `n<=12`, every anchor, and every
`Gamma` of size below `n/2`.

### 5.2 Lemma S2 — PASS

For `S subseteq[n]`, let `S^c=[n] minus S` and
`X^c={S^c:S in X}`. If `C_0,...,C_n` is a witness for a balanced `P`, then

`D_i=[n] minus C_(n-i)`

is a maximal chain in `X^c`, and

`d_P(D_i)=d_P([n])-d_P(C_(n-i))=-d_P(C_(n-i))`.

Thus complementation and chain reversal preserve 1-balanced-chain systems.
If the unique `(n-1)`-set of `X` is `[n] minus {w}`, the unique singleton of
`X^c` is `{w}`. Applying S1 to `X^c` says that it has at least `n/2`
selected pairs incident with `w`; complementing back gives at least `n/2`
selected `(n-2)`-sets whose omitted pair contains `w`.

The independent checker exhausted S2 over every valid family at `n=2,4` and
checked that complementing each stored `n=2,4,6,8` upper family preserves
coverage of every coloring.

No uniqueness claim about optimum terminal sets follows from either lemma,
and Cycle 2 correctly makes none.

## 6. `tau`, `L`, and the connectivity/coherence surcharge

For the balanced-coloring universe `B_n`, let

`K(S)={P in B_n: |d_P(S)|<=1}`.

The exact definition needed by the lower bound is

`tau(n,k)=min{|F|: F subseteq binom([n],k), union_(S in F) K(S)=B_n}`.

For any 1-balanced-chain family `X`, its level
`X_k={S in X: |S|=k}` covers `B_n`: the witness chain for a coloring contains
a compatible member at level `k`. Hence

`|X_k|>=tau(n,k)` for every `k`, and therefore

`N(n)>=L(n):=sum_(k=0)^n tau(n,k)`.

Both minima exist because the ground objects are finite and the whole level
is a cover. A valid family exists (for example the full Boolean lattice), so
`N(n)` is finite and attained. Consequently

`sigma(n):=N(n)-L(n)`

is a well-defined nonnegative integer. More exactly,

`sigma(n)=min_(X valid) sum_k (|X_k|-tau(n,k))`.

This justifies interpreting `sigma` as the minimum extra state count forced
by cross-level path coherence after all independent compatibility lower
bounds are paid.

Two qualifications are necessary:

1. `sigma` is not, by definition, the size of a canonical set `B` of bridge
   vertices added to one simultaneously chosen collection of minimum layer
   covers. The optimizing family and distribution of excess vertices may
   change globally.
2. A positive `sigma` isolates failure of layerwise compatibility to suffice
   for a full path, but the structural cause may involve reachability across
   several levels rather than a localized middle-layer defect.

For the certified finite cases, fresh exhaustive layer-cover enumeration
gave:

| `n` | `tau(n,0),...,tau(n,n)` | `L(n)` | certified `N(n)` | `sigma(n)` |
|---:|---|---:|---:|---:|
| 2 | `1,1,1` | 3 | 3 | 0 |
| 4 | `1,1,2,1,1` | 6 | 6 | 0 |
| 6 | `1,1,3,2,3,1,1` | 12 | 12 | 0 |
| 8 | `1,1,4,2,3,2,4,1,1` | 19 | 20 | 1 |

The symmetry `tau(n,k)=tau(n,n-k)` is valid because
`d_P([n] minus S)=-d_P(S)` for balanced `P`.

### 6.1 The `n=8` six-missed-color wording

The Cycle-2 no-size-19 proof is complete. Its checker enumerates lower
prefixes having exactly `4,2,3` globally reachable selected states at levels
two, three, and four. A hypothetical selected state unreachable for every
color can be discarded; fewer reachable states than `tau(8,k)` already
imply that some coloring fails at that level. This is enough to refute every
size-19 family.

There was, however, a narrow evidence-presentation gap in the stronger prose
claim that **every** minimum-count lower prefix misses at least six colorings:
the stored histogram covers the branches with all selected states globally
reachable, while the pruning argument by itself proves only that an excluded
branch misses at least one.

The new independent checker exhaustively included those excluded cases. For
`r=0,1,2,3,4` globally reachable selected pairs, it allowed the maximum
possible two reachable triples and three reachable four-sets (monotonicity
makes this dominate cases using unreachable upper states). The maximum
numbers of the 70 colorings reaching level four were respectively

`0, 40, 60, 64, 64`.

Thus the six-missed-color statement survives this adversarial check. Its
status is `COMPUTATIONALLY TESTED; UNFORMALIZED`; the new program, not the old
pruning sentence alone, is the explicit check covering unreachable-state
branches.

## 7. Stale repository inconsistency: one chain does not cover only two colors

Two pre-Cycle-2 audit passages are false as written:

- `audits/first_target_selection.md:94`;
- `audits/cross_validation_proof_sat.md:188-193`.

They assert that balance one forces signs to alternate at every adjacent
position, so a fixed maximal chain covers exactly two colorings. The valid
condition is alternation **within positions `(1,2),(3,4),...`**. Adjacent
positions `2` and `3` may have the same sign. For example, `+,-,-,+` has
prefix imbalances `1,0,-1,0`.

The correct per-chain count is `2^(n/2)`. Therefore an explicit list of
chains covering all signed balanced colorings needs at least

`binom(n,n/2)/2^(n/2)`

chains, not `binom(n,n/2)/2`. The corrected lower bound is still exponential,
so the qualitative conclusion that a polynomial explicit list cannot cover
all colorings remains valid. The incorrect count does not feed the Cycle-2
exact values, S1/S2, `tau`, `sigma`, or CF-LOGGAP; all current Cycle-2
structural documents use the correct `2^(n/2)` count.

This should be corrected before final Cycle-3 integration so future arguments
do not inherit a fixed-orientation error.

## 8. CF-LOGGAP leakage audit

Only the scope needed for Cycle 3 was audited. CF-LOGGAP fixes all of the
following:

- a uniformly bounded number `d` of equal ordered blocks;
- greedy minimum-absolute-imbalance choice;
- exactly one frontier consumed per step;
- all other inspected frontiers cached;
- a nonanticipating tie policy; and
- the specific `1-O(1/M)` guarantee that every directly filled balanced-
  return gap is `O(log M)` before block exhaustion.

Its primitive-Dyck event refutes that tail contract for that process. It does
not refute noticeable success, weaker tails, multi-frontier reconciliation,
a compressed long-gap cover, an arbitrary bounded-block rule, a subset-DAG
construction, unrestricted `N(n)`, or O01.

The canonical theorem report, Cycle-2 result, research state, failure ledger,
and scope disposition retain these qualifications. No dependency of the
path-DAG equivalence, S1/S2, `tau`, or `sigma` on CF-LOGGAP was found. None of
the new shared-state principles may cite CF-LOGGAP as a general obstruction
unless its proposed process is first proved to instantiate every frozen
hypothesis above.

## 9. Reproduction record

Commands run from the repository root:

```powershell
git rev-parse HEAD
python -B experiments/check_balanced_chain_certificates.py
python -B experiments/cycle03_verify_foundation.py
```

The frozen commit check returned
`e942729da8db176848354d8d0161e85bcee7c080`. The Cycle-2 checker returned all
five PASS lines and `ALL BALANCED-CHAIN CERTIFICATES PASS`.

The independent Cycle-3 checker reported:

- consecutive-pair equivalence for every permutation/coloring through
  `n=8`;
- agreement of uncontracted and contracted path existence for all `16`
  families at `n=2` and all `65,536` families at `n=4`;
- direct exhaustive `N(2)=3` and `N(4)=6`;
- exhaustive S1/S2 checks on all valid families at `n=2,4`;
- exact fresh `tau` vectors through `n=8`;
- direct path coverage and complement-duality checks for each stored upper
  family through `n=8`;
- the unreachable-state-complete `n=8` prefix maxima
  `{0:0,1:40,2:60,3:64,4:64}`;
- the S1 countercolor scheme for every even `n<=12`; and
- derived `sigma` values `{2:0,4:0,6:0,8:1}`.

It ended with `ALL CYCLE-3 FOUNDATION CHECKS PASS` in about ten seconds on the
current machine.

## 10. Final boundary

The reusable finite/combinatorial foundation passes independent adversarial
review subject to the explicit DAG size-normalization caveat and correction
of the two stale fixed-chain-count passages. The exact finite values remain
`COMPUTATIONALLY VERIFIED; ADVERSARIALLY REVIEWED; UNFORMALIZED`. S1, S2, and
the reformulations remain `ADVERSARIALLY REVIEWED; UNFORMALIZED`, not
`FORMALLY VERIFIED`.

O01 remains **OPEN**. Nothing here establishes `N(10)`, the finite quadratic
formula, a polynomial construction, an mABP separation, or P versus NP.

No line was appended to `failure_knowledge.jsonl`: the newly found issue is a
stale counting/documentation error rather than a failed construction family,
and the broader `n=8` wording survived the strengthened check.

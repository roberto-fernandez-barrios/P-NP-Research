# Research Cycle 3: independent Lean scope audit

**Audit date:** 2026-08-21
**Role:** independent formalization validator; the validator did not write the
formal development
**Files audited:** `formal/BalancedChain.lean`, `formal/check.ps1`, the pinned
Lake configuration and manifest, `formal/coverage.md`, and
`research_cycle_03/lean_formalization.md`
**Disposition:** **PASS WITH TWO SCOPE QUALIFICATIONS AND ONE NONBLOCKING
CHECKER WEAKNESS**

## Executive disposition

The current `BalancedChain.lean` source type-checks under the pinned Lean
4.32.1 / mathlib 4.32.1 environment.  A direct trust-level-zero elaboration
also succeeds.  An independent whole-source token search finds no use of
`sorry`, `admit`, a project-local `axiom`, `unsafe`, or `opaque`.  The four
central exported theorems have the stated types and depend only on mathlib's
ordinary foundational axioms `propext`, `Classical.choice`, and `Quot.sound`;
there is no `sorryAx` dependency.

The definitions faithfully encode balanced colorings, insertion-order
maximal chains, chain containment/goodness, and the intended
`forall coloring, exists chain` family property.  Lean accepts both
directions of the consecutive-pair characterization, both directions of the
contracted-path functionality statement for even cardinality, and Lemmas S1
and S2.  No vacuous premise, reversed quantifier, missing endpoint, or
positive-even boundary error was found.

The formal result has two important and correctly disclosed boundaries:

1. a maximal chain is *defined* by an insertion-order equivalence; the
   extensional equivalence to a separately defined order-theoretic maximal
   Boolean-lattice chain is not formalized; and
2. `ContractedPath` is an encoded path carried by the same insertion order,
   not a separately defined graph-theoretic path object.  The conversion
   between family size, even-state vertex count, and odd-intermediary/edge
   count is unformalized.

Accordingly, the status labels in `formal/coverage.md` are accurate: the
named finite combinatorial theorems are `FORMALLY VERIFIED`, while exact
values of `N`, `tau`/`sigma`, distinct-state accounting, CF-LOGGAP, and O01
remain `UNFORMALIZED`.  O01 remains open.

## 1. Reproduction and trust boundary

From the repository root I ran:

```powershell
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

It reported Lean 4.32.1, Lake 5.0.0, a successful 8,656-job build, and the
expected PASS line.  I then bypassed Lake's target replay and directly
elaborated the source at Lean trust level zero:

```powershell
cd formal
lake env lean -t 0 BalancedChain.lean
```

That command also succeeded.  Its messages are only linter warnings about
unused section variables or simplifier arguments; none affects a theorem.

I separately inspected the exact exported types and asked Lean to print
their axiom dependencies.  The results were:

| Declaration | Exact audited conclusion | Axiom dependency |
|---|---|---|
| `chainGood_iff_consecutivePairsCross` | `ChainGood P C iff ConsecutivePairsCross P C` | standard `propext`, choice, quotient soundness |
| `oneBalancedChain_iff_contractedPaths` | family property iff a contracted path exists for every balanced `P`, under even ground cardinality | same |
| `unique_singleton_half_star` | `|alpha|/2 <= |lowerNeighbors(X,v)|` | same |
| `unique_cosingleton_dual_half_star` | `|alpha|/2 <= |upperOmittedNeighbors(X,w)|` | same |

The source contains no `sorryAx`; “FORMALLY VERIFIED” here means accepted by
Lean relative to its usual classical mathlib foundations, not foundationally
axiom-free mathematics.

### Nonblocking checker weakness

`formal/check.ps1` currently rejects only a line whose first token is
`axiom`, `sorry`, or `admit`.  It would not reject, for example,
`exact sorry` or `by admit`, and `lake build` ordinarily permits such terms
with a warning.  This does **not** compromise the present result: an
independent unrestricted token scan of `BalancedChain.lean` found none, and
the printed theorem dependencies contain no `sorryAx`.  The script should be
hardened before relying on it for future edits, or its PASS wording should be
narrowed to say that the *current independently scanned source* has no such
tokens.

## 2. Definition fidelity

### Balanced coloring and imbalance — PASS

`Coloring alpha := Finset alpha` represents the positive side.  The equation
`2 * P.card = Fintype.card alpha` is exactly equal-size positive/negative
coloring.  `colorSign`, `imbalance`, and `Compatible` implement signs
`+1/-1`, their sum over a subset, and absolute imbalance at most one.  Lean
also proves the expected identity

`imbalance(P,S) = 2 |S intersect P| - |S|`.

There is no unnoticed change from signed colorings to unsigned cuts: `P` and
its complement remain different colorings, as intended.

### Maximal chains and family quantifiers — PASS WITH DISCLOSED BOUNDARY

`MaximalChain.order : Fin |alpha| equiv alpha` gives every element exactly
one insertion position.  Filtering inverse positions below `k` produces the
canonical prefix.  Lean proves empty/full endpoints, successor insertion of
one fresh element, and exact rank.  Thus the representation is
mathematically faithful to a Boolean-lattice maximal chain.

The translation to an independently defined order-theoretic notion of a
maximal chain has not been encoded and proved.  This is why the coverage
ledger correctly marks the maximal-chain row `PARTIALLY FORMALIZED`.

`IsOneBalancedChain X` has the crucial quantifier order

`forall balanced P, exists C, ChainContained X C and ChainGood P C`.

The family is fixed outside the coloring quantifier.  `ChainContained` and
`ChainGood` include every rank `0,...,|alpha|`, including both endpoints.
For a finite `alpha`, using `Set (Finset alpha)` rather than a finite-family
data type changes no membership semantics, but family cardinality and `N(n)`
are intentionally not defined in this development.

## 3. Consecutive-pair theorem — PASS

The accepted theorem is slightly stronger than required: it does not assume
that the whole coloring is balanced.  This is sound.  Compatibility at each
even prefix forces its even integer imbalance to be zero, hence each
successive two-sign sum is zero.  Conversely, crossing within every pair
makes even prefixes zero and an optional final odd prefix `+1` or `-1`.

The predicate pairs insertion positions `(0,1),(2,3),...`; it does not
silently impose alternation across a pair boundary.  Thus it agrees with the
corrected fixed-chain count and does not formalize the stale Cycle-1 error.

The theorem also remains true for odd ground cardinality, with the final
unpaired sign handled by the odd-prefix proof.  The O01 family theorem is
only used under even cardinality, so this extra generality creates no scope
problem.

## 4. Contracted path functionality — QUALIFIED PASS

`ContractedArc X P S a b` records:

- membership of the even source, chosen odd intermediary, and two-element
  target in `X`;
- freshness and distinctness of the two inserted elements; and
- crossing of their colors.

Within `ContractedPath`, `S`, `a`, and `b` are instantiated by an insertion
order's prefixes and next two positions.  Hence every arc is at an even rank,
successive targets are exactly the next even prefixes, and the selected odd
intermediary is the actual intervening prefix.  Swapping `a,b` represents
the alternative selected intermediary without losing functionality.

For even ground cardinality the arcs cover all odd and nonterminal even
prefixes; explicit source/full fields cover the endpoints, including the
zero-cardinality edge case.  Lean's two directions therefore establish the
claimed path *functionality* equivalence.

What Lean has not established is a theorem starting from a separately
defined subset-labelled graph and arbitrary graph path and constructing an
insertion order from it.  Nor has it proved the polynomial accounting bound
`q + |E| <= q(1+binom(n,2))`.  The current reports explicitly retain both
limitations, so `FULLY FORMALIZED FOR PATH FUNCTIONALITY` is the appropriate
status.  Raw DAG vertex count must not be identified with `N(n)` on the
strength of this theorem.

## 5. Lemma S1 — PASS

`HasUniqueSingleton X v` requires `{v}` in `X` and every selected rank-one
set to equal it.  `lowerNeighbors` counts exactly distinct `u != v` whose
pair `{v,u}` is selected.

Under the contradiction hypothesis, the neighbor set has size below
`|alpha|/2`; inserting `v` therefore has size at most half.  Mathlib extends
it to a positive set of exactly half the ground cardinality.  A witness
chain must use `{v}` at rank one and a selected incident pair at rank two, so
its second element is a recorded neighbor.  Both first-pair elements are
positive, contradicting the formally established crossing property.

The argument uses the explicit element `v`, so the empty-type case cannot
make the statement vacuous.  Evenness then turns the constructed half-size
set into an exactly balanced coloring.  The `n=2` boundary is included.

## 6. Lemma S2 — PASS

`HasUniqueCosingleton X w` requires the unique selected rank-`n-1` set to be
the universe with `w` erased.  `upperOmittedNeighbors` counts the distinct
`u != w` for which the selected rank-`n-2` set omits `{w,u}`.

The direct last-pair proof correctly identifies the final inserted element
as `w` from uniqueness of the co-singleton.  The preceding element belongs
to `upperOmittedNeighbors`, because the rank-`n-2` prefix is the universe
minus those final two distinct elements.  Coloring `w` and all alleged
neighbors positive makes the last consecutive pair monochromatic, yielding
the contradiction.  This proves S2 without depending on an unformalized
family-complement transport theorem and includes `n=2`.

## 7. Epistemic boundary and integration audit

The Lean files do **not** define or prove:

- a family-size minimization `N(n)` or any exact finite value, including
  `N(10)=35`;
- `tau`, `L`, `sigma`, or a certificate-reflection theorem;
- the graph/family polynomial state-accounting conversion;
- CF-LOGGAP or any Cycle-3 construction/obstruction outside S1 and S2;
- a polynomial-size shared-state construction; or
- O01, an mABP separation, or P versus NP.

At the time of this audit, `results/research_cycle_03.md` mentions the Lean
work only as unfinished in its stopping paragraph and
`research_cycle_03/README.md` still says the Lean report will be indexed
later.  Final integration should add links to the formalization report and
this independent audit, retain the exact scope above, and remove the
unfinished wording only after all other validation is complete.

## Final status

The present formalization is accepted and faithful within its expressly
chosen insertion-order and encoded-path representations.  The central
declarations may be called `FORMALLY VERIFIED` with the coverage ledger's
qualifiers.  The formalization supplies no asymptotic result and no evidence
that O01 is solved.

## Post-audit resolution — 2026-08-21

After the initial audit, `formal/check.ps1` was hardened from a line-leading
test to the standalone-token pattern

`(?<![A-Za-z0-9_])(axiom|sorry|admit)(?![A-Za-z0-9_])`.

I independently tested the revised expression on embedded examples.  It
rejects `by sorry`, `exact sorry`, `by admit`, and an `axiom` declaration,
while not confusing identifiers such as `sorryAx`, `admitted`, or
`axiomatic` with forbidden tokens.  It conservatively also rejects those
standalone words in comments or strings; that can create a harmless future
false positive, not a false negative for a proof admission.  The current
source contains none of the tokens, and the revised checker completes its
Lean/Lake build successfully.  The previously reported checker weakness is
therefore **RESOLVED** for this cycle.

I also reread the final formalization sections and links in
`results/research_cycle_03.md`, `RESEARCH_STATE.md`, and
`research_cycle_03/README.md`.  They accurately limit formal verification to
the encoded insertion-order definitions, consecutive-pair equivalence,
contracted-path functionality, S1, and S2.  They explicitly retain the
unformalized status of the order-theoretic translation, separate graph and
state accounting, exact `N` computations, `tau`/`sigma`, CF-LOGGAP,
structural classes, and O01.  The links to the proposer report, coverage
ledger, and this audit resolve correctly.  **FINAL FORMAL INTEGRATION: PASS.**

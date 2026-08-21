# Research Cycle 4: Lean formalization of relabeling and literal unions

**Date:** 2026-08-21
**Toolchain:** Lean 4.32.1 and mathlib 4.32.1, pinned in `formal/`
**Status:** the declarations named below are `FORMALLY VERIFIED` within the
existing insertion-order representation
**Scope:** the deterministic relabeling and union core of Phase 4A only

## Result

The Cycle-3 development represented a maximal chain by a total insertion
order and represented acceptance by membership of every literal prefix in a
fixed subset family.  Cycle 4 extends that representation with a permutation
action on:

* literal subsets: `relabelSubset`;
* literal subset families: `relabelFamily`;
* positive-set colorings: `pullbackColoring`; and
* insertion-order chains: `MaximalChain.relabel`.

Lean checks that relabeling preserves subset cardinality, transports
imbalance and compatibility exactly, sends every chain prefix to the literal
image of its old prefix, and presents the relabeled family as the set image
of the original family.

The central theorem is

```text
acceptsColoring_relabel_iff:
  AcceptsColoring (relabelFamily pi X) P
    iff AcceptsColoring X (pullbackColoring pi P).
```

Here `AcceptsColoring` quantifies over a complete maximal chain whose every
prefix is a literal member of the family.  The theorem therefore concerns
the full induced subset family, not merely a list of generating paths.  It
also fixes the orientation convention: the coloring on the original family
is pulled back by `pi`, so an original point `x` is positive exactly when
`pi x` is positive in `P`.

Lean additionally checks

```text
isOneBalancedChain_relabel_iff:
  IsOneBalancedChain (relabelFamily pi X)
    iff IsOneBalancedChain X.
```

## Literal-union theorem

The generic declaration

```text
iUnion_isOneBalancedChain_of_pointwise_accepts
```

proves that if, for each balanced coloring, some member of an indexed
collection accepts it, then the literal indexed union is a
1-balanced-chain family.  Its relabeling specialization is

```text
union_relabelings_isOneBalancedChain:
  (forall balanced P, exists i,
      AcceptsColoring X (pullbackColoring (pi i) P))
  -> IsOneBalancedChain (iUnion fun i => relabelFamily (pi i) X).
```

The proof embeds the accepting individual-copy chain into the union.  It
does not assume that the union has only paths inherited from one copy;
additional hybrid paths remain available and can only add witnesses.

## Exact formal boundary

This file does **not** formalize the probability space of uniformly random
permutations, the equal-fiber count on balanced colorings, independence, the
union bound, the strict integer threshold for the number of copies, or the
cardinality bound for distinct subsets in their union.  Thus Phase 4A is
`PARTIALLY FORMALIZED`: its exact deterministic equivariance and final union
step are checked, while its probabilistic and numeric steps remain in the
independently audited written proof.

The corrected cyclic-interval definition of `RR_n`, the deque equivalence,
the rooted complement/reversal equivalence with the ordinary interval
family, the inequality `A_n <= (n/2) p_(n-2)`, and the imported FLSY theorem
are also unformalized.  In particular, this development proves neither the
stretched-exponential acceptance bound nor O01.

## Verification record

The initial build found no retained binary mathlib cache and began compiling
dependencies from source.  After validating its exact process tree, that
build was stopped and the reproducible mathlib cache command was used:

```powershell
cd formal
lake exe cache get
```

The command exited successfully, reporting 6,585 cached files decompressed
and no files requiring download.  From the repository root,

```powershell
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

then reported Lean 4.32.1, Lake 5.0.0, a successful 8,656-job build, and the
source-level admission check PASS.  Direct elaboration at trust level zero
also succeeded:

```powershell
cd formal
lake env lean -t 0 BalancedChain.lean
```

Temporary `#print axioms` queries (removed after the audit) reported the
following ordinary mathlib foundational dependencies and no `sorryAx`:

| Declaration | Reported dependencies |
|---|---|
| `acceptsColoring_relabel_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `isOneBalancedChain_relabel_iff` | `propext`, `Classical.choice`, `Quot.sound` |
| `iUnion_isOneBalancedChain_of_pointwise_accepts` | `propext`, `Quot.sound` |
| `union_relabelings_isOneBalancedChain` | `propext`, `Classical.choice`, `Quot.sound` |

The checked source contains no standalone proof-admission token and no use
of `unsafe` or `opaque`.  Generated `.lake/` artifacts are ignored and are
not research evidence.

# Formal verification coverage

**Updated:** 2026-08-21 during Research Cycle 4.  The reusable finite
balanced-chain core and the deterministic relabeling/literal-union layer are
checked by Lean 4.32.1 with mathlib 4.32.1.  The project is pinned by
`lean-toolchain`, `lakefile.toml`, and `lake-manifest.json`; `.lake/` is
generated and ignored.

The labels below concern formal proof coverage only.  They do not establish
novelty and do not promote any finite computation to an asymptotic theorem.

| Result / definition | Coverage | Evidence and remaining boundary |
|---|---|---|
| Balanced coloring, sign, subset imbalance, and compatibility | FULLY FORMALIZED | `Coloring`, `IsBalanced`, `colorSign`, `imbalance`, `Compatible`, and `imbalance_eq_card` in `formal/BalancedChain.lean`. |
| Maximal chain and subset prefixes | PARTIALLY FORMALIZED | `MaximalChain` is a total insertion order and `prefix` is its canonical subset sequence; prefix-zero, prefix-full, successor, freshness, and exact-cardinality lemmas are checked.  An extensional equivalence with a separately defined maximal chain in the Boolean-lattice order was not needed and is not formalized. |
| 1-balanced-chain family | FULLY FORMALIZED | `ChainContained`, `ChainGood`, and `IsOneBalancedChain` encode the `forall coloring, exists chain` quantifier order over a fixed subset family. |
| Literal permutation action and acceptance equivariance | FULLY FORMALIZED | `relabelSubset`, `relabelFamily`, `pullbackColoring`, and `MaximalChain.relabel` act on literal subsets, full families, colorings, and insertion orders.  `acceptsColoring_relabel_iff` proves exact full-family acceptance equivariance, while `isOneBalancedChain_relabel_iff` proves worst-case invariance.  Rank/cardinality preservation, imbalance transport, and the literal set-image characterization are checked. |
| Deterministic union of relabelings | FULLY FORMALIZED | `iUnion_isOneBalancedChain_of_pointwise_accepts` proves that if one indexed literal family accepts each balanced coloring, its literal union is a 1-balanced-chain family.  `union_relabelings_isOneBalancedChain` specializes this to pulled-back acceptance by relabelings of one fixed family.  The theorem needs no assertion about, and does not discard, hybrid paths in the union. |
| Phase-4A probabilistic symmetrization and counting | PARTIALLY FORMALIZED | The exact deterministic equivariance and final literal-union implication are formalized.  Uniform sampling of balanced colorings under a random permutation, independence, the union bound, the exact sufficient `t`, and the distinct-subset cardinality bound are UNFORMALIZED.  The imported FLSY average-to-worst-case lemma is not re-proved in Lean. |
| Consecutive-pair characterization | FULLY FORMALIZED | `chainGood_iff_consecutivePairsCross`, including both directions and the even-prefix-zero invariant, is kernel-checked for every finite ground type. |
| Exact contracted path-DAG reformulation | FULLY FORMALIZED FOR PATH FUNCTIONALITY | `ContractedArc`, `ContractedPath`, `chainContained_and_good_iff_contractedPath`, and `oneBalancedChain_iff_contractedPaths` prove both directions for even ground cardinality.  An oriented arc records the selected odd intermediary.  A separate graph-library object and the polynomial `vertices + edges` accounting conversion are UNFORMALIZED. |
| Lemma S1 (unique singleton forces a half-star) | FULLY FORMALIZED | `unique_singleton_half_star`; the proof constructs a balanced countercolor using mathlib's finite superset-cardinality lemma and contradicts the first crossing pair. |
| Lemma S2 (unique co-singleton forces the dual half-star) | FULLY FORMALIZED | `unique_cosingleton_dual_half_star`; proved directly from the final crossing pair.  The separate theorem that complementation/reversal transports an entire family is UNFORMALIZED. |
| Exact `N(2)=3,N(4)=6,N(6)=12,N(8)=20` and Cycle-3 `n=10` claims | UNFORMALIZED | Exact computational certificates and independent checkers are separate evidence.  No certificate reflection layer has been implemented in Lean. |
| `tau`, `L`, and `sigma` definitions and finite values | UNFORMALIZED | The mathematical definitions were independently audited, but are not in the Lean development. |
| CF-LOGGAP cached-frontier logarithmic-gap obstruction | UNFORMALIZED | Deliberately deferred because the requested finite structural core was prioritized. |
| Variable-threshold reserve and geometric-log accounting lemmas | UNFORMALIZED | Existing written proofs are not imported into this Lean project. |
| Polynomial fixed-order recursive-cover obstruction | UNFORMALIZED | Depends on the unformalized FLSY theorem. |
| Corrected `RR_n`, deque equivalence, and rooted ordinary-interval reduction | UNFORMALIZED | The literal cyclic-interval definition, the rooted complement/reversal equivalence, the probability inequality `A_n <= (n/2) p_(n-2)`, and the imported FLSY stretched-exponential estimate remain in independently checked mathematical and computational artifacts, not this Lean development. |
| Polynomial 1-balanced-chain target O01 | UNFORMALIZED | OPEN; it is a target, not a theorem. |
| Counterexample to Alekseev--Gaevoy Conjecture 1.4/4.2 | UNFORMALIZED | Existing parametric and finite computational evidence is unchanged. |

## Reproduction

From the repository root on Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

The checker rejects a source-level `axiom`, `sorry`, or `admit`, prints the
tool versions, and runs `lake build`.  As of the update above it ends with:

```text
Build completed successfully (8656 jobs).
PASS: BalancedChain.lean contains no sorry/axiom/admit and lake build succeeded.
```

This is machine checking of the named combinatorial and deterministic
relabeling core only.  It does not verify the Phase-4A probability estimate,
the RR obstruction, O01, any exact optimum computation, CF-LOGGAP, an mABP
separation, or P versus NP.

# Exact finite 1-balanced-chain certificates

The four `exact_n*.json` files contain one extremal family and an explicit
maximal-chain witness for **every** balanced coloring, including both a
coloring and its global sign complement.

`level_cover_lower_bounds.json` certifies the minimum number of compatible
subsets required separately at each Boolean-lattice level.  Its entries are
exhaustively checked rather than trusted.

For `n=2,4,6`, the sum of the level minima matches the upper family.  For
`n=8`, the level sum is 19.  `n8_no_size19.json` records an unsymmetrized
exhaustion of every possible size-19 prefix through level four.  The checker
recomputes all branches and their digest from the definition.

Run from the repository root:

```text
python -B experiments/check_balanced_chain_certificates.py
```

The optimizer is separate:

```text
python -B experiments/balanced_chain_optimize.py --n 2 4 6 8
```

Subset masks use bit `i` for element `i` of the zero-based ground set.  These
are computational certificates, not a Lean formalization or a novelty claim.

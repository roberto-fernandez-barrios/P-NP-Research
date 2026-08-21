# Exact finite `n=10` balanced-chain certificates

The artifacts in this directory support the finite computational result
`N(10)=35`.  They do not imply an asymptotic bound.

## One-command check

From the repository root:

```text
python -B experiments/check_balanced_chain_n10_exact.py
```

This recomputes the relevant exhaustive searches using only the Python
standard library.  It does not trust the optimizer's objective, dual bound,
status code, the SAT answer, stored reachability signatures, or stored
enumeration digests.

## Files

* `level_cover_search.json`: SciPy/HiGHS search witnesses and metadata for
  levels zero through five.
* `level_cover_certificate.json`: exact minima, independent branch summaries,
  complement witnesses, histograms, and enumeration digests.
* `no_minimum_prefix.json`: all-color reachability exhaustion of the
  `1,1,5,3,5` lower prefix; 1,686,060 terminal branches.
* `upper_size35.json`: 35 distinct subset masks, full witnesses for all 252
  signed balanced colorings, all 60 maximal chains, and structural metadata.
* `sat_bound33.json` and `sat_bound33_no_anchor_prune.json`: corroborating SAT
  runs.  Their UNSAT answers have no checked proof and are not used for the
  exact lower bound.

Subset masks use bit `i` for element `i` of `{0,...,9}`.  Epistemic status:
`EXHAUSTIVELY COMPUTATIONALLY VERIFIED; UNFORMALIZED`; novelty is audited
separately.

## Digest byte encoding

The stored enumeration digests are integrity summaries, not proofs.  For a
nontrivial level-cover lower-bound branch, the checker appends, in enumeration
order, the canonical first mask, every other selected mask, and the number of
covered colorings, each as an unsigned two-byte little-endian integer.  The
rank-zero and rank-one empty-family case hashes the ASCII bytes
`empty-family`.  For a minimum-prefix terminal branch, it appends the three
selected triple masks, the five selected rank-four masks, and the covered
color count, again as unsigned two-byte little-endian integers.  SHA-256 is
applied to the resulting byte stream.

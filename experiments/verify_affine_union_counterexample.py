"""Finite checks for a counterexample to ECCC TR26-007, Conj. 1.4/4.2.

This script is deliberately independent of a SAT/SMT encoding.  It enumerates
the first 2L coordinates; the remaining ambient coordinates are free and only
multiply every relevant cardinality by the same factor.

It verifies the cover/private-layer construction used in
theory/conjectures/falsified/ag26_affine_union_robustness.md.
"""

from __future__ import annotations

import argparse
import itertools
import math


def zero_set(x: int, width: int) -> frozenset[int]:
    return frozenset(i for i in range(width) if not (x >> i) & 1)


def verify(l_value: int) -> None:
    width = 2 * l_value
    middle_subsets = tuple(
        frozenset(s) for s in itertools.combinations(range(width), l_value)
    )

    flats = {
        subset: {x for x in range(1 << width) if subset <= zero_set(x, width)}
        for subset in middle_subsets
    }
    private = {
        subset: {x for x in flat if zero_set(x, width) == subset}
        for subset, flat in flats.items()
    }
    trimmed = {
        subset: flats[subset] - private[subset] for subset in middle_subsets
    }

    union = set().union(*flats.values())
    private_union = set().union(*private.values())
    trimmed_union = set().union(*trimmed.values())

    expected_union = sum(math.comb(width, z) for z in range(l_value, width + 1))
    expected_middle = math.comb(width, l_value)

    assert len(flats) == math.comb(width, l_value)
    assert all(len(flat) == 1 << l_value for flat in flats.values())
    assert all(len(layer) == 1 for layer in private.values())
    assert len(union) == expected_union
    assert len(private_union) == expected_middle
    assert union - trimmed_union == private_union
    assert trimmed_union == union - private_union

    deletion_fraction = 1 / (1 << l_value)
    union_loss_fraction = len(private_union) / len(union)
    print(f"L={l_value}; active coordinates={width}")
    print(f"number of codimension-L flats={len(flats)}")
    print(f"cover size={len(union)} of {1 << width} (>= one half)")
    print(f"per-flat deletion fraction={deletion_fraction:.12g}")
    print(f"cover loss fraction={union_loss_fraction:.12g}")
    print(f"sqrt(L) * cover loss={math.sqrt(l_value) * union_loss_fraction:.12g}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("L", nargs="?", type=int, default=3)
    args = parser.parse_args()
    if args.L < 1:
        raise SystemExit("L must be positive")
    verify(args.L)

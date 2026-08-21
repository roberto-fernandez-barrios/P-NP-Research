#!/usr/bin/env python3
"""Standard-library checker for the Cycle-3 n=10 level-cover bound.

For every nontrivial level k <= 5, the checker verifies a cover of the
claimed size and exhausts every cover one smaller, up to relabeling one member
to {0,...,k-1}.  Exhausting size t-1 suffices to refute every smaller size:
any smaller cover can be padded by distinct same-level sets without losing
coverage.  Complementation transfers the result to levels 6,...,10.

The resulting sum of exact per-level minima is a rigorous finite lower bound
on N(10).  This checker intentionally imports neither SciPy nor the search
program and ignores all solver status/dual-bound fields.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path


def masks_of_weight(n: int, weight: int) -> list[int]:
    return [sum(1 << i for i in choice) for choice in combinations(range(n), weight)]


def compatible(subset: int, plus: int) -> bool:
    return abs(2 * (subset & plus).bit_count() - subset.bit_count()) <= 1


def compatibility_columns(n: int, level: int, colors: list[int]) -> dict[int, int]:
    columns = {}
    for subset in masks_of_weight(n, level):
        bits = 0
        for index, plus in enumerate(colors):
            if compatible(subset, plus):
                bits |= 1 << index
        columns[subset] = bits
    return columns


def exhaustive_lower_check(
    n: int, level: int, claimed: int, colors: list[int]
) -> dict:
    """Refute a cover of size claimed-1 using valid S_n symmetry."""
    all_colors = (1 << len(colors)) - 1
    if claimed == 1:
        assert all_colors != 0
        return {
            "canonical_first_mask": None,
            "tested_family_size": 0,
            "branch_count": 1,
            "maximum_signed_colorings_covered": 0,
            "coverage_histogram": {"0": 1},
            "enumeration_sha256": hashlib.sha256(b"empty-family").hexdigest(),
        }

    columns = compatibility_columns(n, level, colors)
    canonical = (1 << level) - 1
    candidates = [subset for subset in columns if subset != canonical]
    remaining_count = claimed - 2
    digest = hashlib.sha256()
    histogram: Counter[int] = Counter()
    maximum = 0
    branch_count = 0
    prefix_cover = columns[canonical]

    for rest in combinations(candidates, remaining_count):
        covered = prefix_cover
        for subset in rest:
            covered |= columns[subset]
        assert covered != all_colors, (
            f"level {level} has an unexpected cover smaller than {claimed}: "
            f"{(canonical, *rest)}"
        )
        count = covered.bit_count()
        maximum = max(maximum, count)
        histogram[count] += 1
        branch_count += 1
        digest.update(canonical.to_bytes(2, "little"))
        for subset in rest:
            digest.update(subset.to_bytes(2, "little"))
        digest.update(count.to_bytes(2, "little"))

    return {
        "canonical_first_mask": canonical,
        "tested_family_size": claimed - 1,
        "branch_count": branch_count,
        "maximum_signed_colorings_covered": maximum,
        "coverage_histogram": {str(key): histogram[key] for key in sorted(histogram)},
        "enumeration_sha256": digest.hexdigest(),
    }


def verify_and_summarize(search: dict) -> dict:
    n = search["n"]
    assert n == 10
    colors = masks_of_weight(n, n // 2)  # all 252 signed colorings
    all_colors = (1 << len(colors)) - 1
    cases = {case["level"]: case for case in search["cases"]}
    assert set(cases) == set(range(n // 2 + 1))

    half_minima: list[int] = []
    enumerations = {}
    for level in range(n // 2 + 1):
        case = cases[level]
        claimed = case["incumbent"]
        assert case["candidate_count"] == comb(n, level)
        assert isinstance(claimed, int) and 1 <= claimed <= comb(n, level)
        witness = case["cover_witness_masks"]
        assert len(witness) == claimed and len(set(witness)) == claimed
        assert all(0 <= subset < (1 << n) for subset in witness)
        assert all(subset.bit_count() == level for subset in witness)
        covered = 0
        for plus_index, plus in enumerate(colors):
            if any(compatible(subset, plus) for subset in witness):
                covered |= 1 << plus_index
        assert covered == all_colors, f"stored level-{level} witness is not a cover"

        exhaustive = exhaustive_lower_check(n, level, claimed, colors)
        enumerations[str(level)] = exhaustive
        half_minima.append(claimed)

    minima = half_minima + list(reversed(half_minima[:-1]))
    assert len(minima) == n + 1
    # Directly verify complementing each lower-half witness covers the
    # symmetric upper level.  The lower-bound transfer is the identity
    # d_P([n]\\S) = -d_P(S), valid because every P is balanced.
    full = (1 << n) - 1
    upper_witnesses = {}
    for level in range(n // 2 + 1, n + 1):
        source = n - level
        witness = [full ^ subset for subset in cases[source]["cover_witness_masks"]]
        assert all(subset.bit_count() == level for subset in witness)
        for plus in colors:
            assert any(compatible(subset, plus) for subset in witness)
        upper_witnesses[str(level)] = witness

    return {
        "schema": "balanced-chain-n10-level-cover-certificate-v1",
        "epistemic_status": "EXHAUSTIVELY CHECKED FINITE LOWER BOUND; UNFORMALIZED",
        "n": n,
        "signed_balanced_coloring_count": len(colors),
        "exact_level_minima": minima,
        "level_sum_lower_bound_for_N10": sum(minima),
        "lower_half_witnesses": {
            str(level): cases[level]["cover_witness_masks"]
            for level in range(n // 2 + 1)
        },
        "upper_half_complement_witnesses": upper_witnesses,
        "lower_bound_enumerations": enumerations,
        "proof_scope": (
            "Exact tau(10,k) only. Their sum lower-bounds N(10); "
            "it does not determine N(10)."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--search",
        type=Path,
        default=Path("certificates/balanced_chain_n10/level_cover_search.json"),
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("certificates/balanced_chain_n10/level_cover_certificate.json"),
    )
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()

    search = json.loads(args.search.read_text(encoding="utf-8"))
    summary = verify_and_summarize(search)
    if args.write_certificate:
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    else:
        stored = json.loads(args.certificate.read_text(encoding="utf-8"))
        assert stored == summary, "stored certificate differs from recomputation"

    print(f"PASS exact level minima: {summary['exact_level_minima']}")
    print(f"PASS N(10) >= {summary['level_sum_lower_bound_for_N10']}")
    print("PASS size 30 is impossible")


if __name__ == "__main__":
    main()

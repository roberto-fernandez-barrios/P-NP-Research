#!/usr/bin/env python3
"""Independent exhaustive checker for finite balanced-chain certificates.

This checker intentionally imports neither SciPy nor the optimizer.  It uses
the definition directly, verifies every stored coloring/chain witness, proves
the per-level covering lower bounds by exhaustive enumeration, and performs
an unsymmetrized exhaustive refutation of size 19 for n=8.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import reduce
from itertools import combinations
from pathlib import Path


def subset_mask(items) -> int:
    ans = 0
    for item in items:
        ans |= 1 << item
    return ans


def balanced_colorings(n: int) -> list[int]:
    return [subset_mask(c) for c in combinations(range(n), n // 2)]


def is_compatible(subset: int, plus: int) -> bool:
    value = 2 * (subset & plus).bit_count() - subset.bit_count()
    return abs(value) <= 1


def verify_upper_certificate(document: dict) -> None:
    n = document["n"]
    full = (1 << n) - 1
    family_list = document["family_masks"]
    family = set(family_list)
    assert len(family) == len(family_list), "duplicate subset in family"
    assert [subset_mask(items) for items in document["family_elements"]] == family_list
    assert all(0 <= subset <= full for subset in family)
    assert len(family) == document["claimed_optimum"]
    assert 0 in family and full in family

    expected_levels = [0] * (n + 1)
    for subset in family:
        expected_levels[subset.bit_count()] += 1
    assert expected_levels == document["level_counts"]

    entries = document["all_balanced_coloring_witnesses"]
    expected_colors = balanced_colorings(n)
    assert [entry["plus_mask"] for entry in entries] == expected_colors

    for entry in entries:
        plus = entry["plus_mask"]
        assert plus.bit_count() == n // 2
        assert entry["plus_elements"] == [
            i for i in range(n) if (plus >> i) & 1
        ]
        permutation = entry["permutation"]
        chain = entry["chain_masks"]
        assert sorted(permutation) == list(range(n))
        assert len(chain) == n + 1 and chain[0] == 0 and chain[-1] == full

        reconstructed = [0]
        current = 0
        for element in permutation:
            assert not ((current >> element) & 1)
            current |= 1 << element
            reconstructed.append(current)
        assert reconstructed == chain
        for level, subset in enumerate(chain):
            assert subset in family
            assert subset.bit_count() == level
            assert is_compatible(subset, plus)


def coverage_bits(n: int, subsets: list[int], colors: list[int]) -> int:
    bits = 0
    for color_index, plus in enumerate(colors):
        if any(is_compatible(subset, plus) for subset in subsets):
            bits |= 1 << color_index
    return bits


def verify_level_lower_bounds(document: dict) -> dict[int, list[int]]:
    verified = {}
    for n_text, case in sorted(document["cases"].items(), key=lambda x: int(x[0])):
        n = int(n_text)
        colors = balanced_colorings(n)
        all_colors = (1 << len(colors)) - 1
        minima = case["minima"]
        examples = case["cover_examples"]
        assert len(minima) == n + 1

        for level, claimed in enumerate(minima):
            candidates = [
                subset
                for subset in range(1 << n)
                if subset.bit_count() == level
            ]
            candidate_cover = {
                subset: coverage_bits(n, [subset], colors) for subset in candidates
            }
            # Exhaustively refute every smaller collection.
            for size in range(claimed):
                for choice in combinations(candidates, size):
                    cover = reduce(
                        int.__or__, (candidate_cover[s] for s in choice), 0
                    )
                    assert cover != all_colors, (
                        f"level minimum false for n={n}, k={level}: {choice}"
                    )

            example = examples[str(level)]
            assert len(example) == claimed and len(set(example)) == claimed
            assert all(s in candidates for s in example)
            assert coverage_bits(n, example, colors) == all_colors

        verified[n] = minima
    return verified


def compatibility_bitsets(n: int):
    colors = balanced_colorings(n)
    bitsets = []
    for subset in range(1 << n):
        bits = 0
        for color_index, plus in enumerate(colors):
            if is_compatible(subset, plus):
                bits |= 1 << color_index
        bitsets.append(bits)
    return colors, bitsets


def extend_reachability(previous, candidates, compatibility):
    ans = {}
    for candidate in candidates:
        reachable = 0
        for prior, color_bits in previous.items():
            if prior & ~candidate == 0:
                reachable |= color_bits
        reachable &= compatibility[candidate]
        if reachable:
            ans[candidate] = reachable
    return ans


def verify_n8_no_size19(document: dict) -> None:
    """Exhaust all size-19 prefixes through level four, without symmetry."""
    n = 8
    colors, compatibility = compatibility_bitsets(n)
    all_colors = (1 << len(colors)) - 1
    levels = [
        [subset for subset in range(1 << n) if subset.bit_count() == level]
        for level in range(n + 1)
    ]
    counts = Counter()
    histogram = Counter()
    digest = hashlib.sha256()
    best_coverage = 0

    # A hypothetical size-19 family has exact level counts
    # 1,1,4,2,3,2,4,1,1.  If one of its selected vertices at levels 2--4
    # is unreachable, the reachable vertices are fewer than the independently
    # certified level-cover minimum and cannot serve all colorings.  It is
    # therefore complete to enumerate reachable choices of exactly 4,2,3.
    for singleton in levels[1]:
        level1 = extend_reachability({0: all_colors}, [singleton], compatibility)
        level2_candidates = extend_reachability(
            level1, levels[2], compatibility
        )
        for level2_choice in combinations(level2_candidates, 4):
            counts["level2_choices"] += 1
            level2 = {s: level2_candidates[s] for s in level2_choice}
            level2_cover = reduce(int.__or__, level2.values(), 0)
            if level2_cover != all_colors:
                counts["level2_dead"] += 1
                continue
            counts["level2_live"] += 1

            level3_candidates = extend_reachability(
                level2, levels[3], compatibility
            )
            for level3_choice in combinations(level3_candidates, 2):
                counts["level3_choices"] += 1
                level3 = {s: level3_candidates[s] for s in level3_choice}
                level3_cover = reduce(int.__or__, level3.values(), 0)
                if level3_cover != all_colors:
                    counts["level3_dead"] += 1
                    continue
                counts["level3_live"] += 1

                level4_candidates = extend_reachability(
                    level3, levels[4], compatibility
                )
                for level4_choice in combinations(level4_candidates, 3):
                    counts["level4_choices"] += 1
                    level4 = {
                        s: level4_candidates[s] for s in level4_choice
                    }
                    covered = reduce(int.__or__, level4.values(), 0)
                    covered_count = covered.bit_count()
                    assert covered != all_colors, "found a size-19 prefix"
                    histogram[covered_count] += 1
                    best_coverage = max(best_coverage, covered_count)
                    digest.update(
                        bytes(
                            [
                                singleton,
                                *level2_choice,
                                *level3_choice,
                                *level4_choice,
                                covered_count,
                            ]
                        )
                    )

    expected_counts = Counter(document["branch_counts"])
    expected_histogram = Counter(
        {int(key): value for key, value in document["level4_coverage_histogram"].items()}
    )
    assert counts == expected_counts
    assert histogram == expected_histogram
    assert best_coverage == document["maximum_level4_colorings_covered"]
    assert digest.hexdigest() == document["enumeration_sha256"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate-dir",
        type=Path,
        default=Path("certificates/balanced_chain_exact"),
    )
    args = parser.parse_args()
    directory = args.certificate_dir

    level_document = json.loads(
        (directory / "level_cover_lower_bounds.json").read_text(encoding="utf-8")
    )
    minima = verify_level_lower_bounds(level_document)
    no19 = json.loads(
        (directory / "n8_no_size19.json").read_text(encoding="utf-8")
    )
    assert no19["prerequisite_level_counts"] == minima[8]
    verify_n8_no_size19(no19)

    expected_optima = {2: 3, 4: 6, 6: 12, 8: 20}
    for n, optimum in expected_optima.items():
        document = json.loads(
            (directory / f"exact_n{n}.json").read_text(encoding="utf-8")
        )
        verify_upper_certificate(document)
        level_lower_bound = sum(minima[n])
        if n < 8:
            assert level_lower_bound == optimum
        else:
            assert level_lower_bound == 19 and optimum == 20
        assert document["claimed_optimum"] == optimum
        print(
            f"PASS n={n}: upper witnesses exhaustive; "
            f"lower bound={optimum}"
        )

    print(
        "PASS n=8 no-size-19 enumeration: "
        f"{no19['branch_counts']['level4_choices']} level-4 branches"
    )
    print("ALL BALANCED-CHAIN CERTIFICATES PASS")


if __name__ == "__main__":
    main()

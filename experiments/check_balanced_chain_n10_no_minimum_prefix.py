#!/usr/bin/env python3
"""Exhaustively refute the minimum-count n=10 prefix through level four.

Prerequisite (checked separately): tau(10,k) = 1,1,5,3,5 at levels 0..4.
After relabeling, the unique singleton is {0} and the five usable selected
pairs are {0,i}, i=1,...,5.  This program keeps an exact 252-bit reachability
signature for every candidate triple and four-set, enumerates all choices of
three triples and then five reachable four-sets, and proves that no such
prefix reaches every signed balanced coloring.

The search uses only the Python standard library and the literal finite
definition.  It imports neither a SAT/MILP solver nor any search code.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


N = 10
FULL = (1 << N) - 1


def subset_mask(items) -> int:
    mask = 0
    for item in items:
        mask |= 1 << item
    return mask


def masks_of_weight(weight: int) -> list[int]:
    return [subset_mask(choice) for choice in combinations(range(N), weight)]


def balanced_colorings() -> list[int]:
    return masks_of_weight(N // 2)


def compatible(subset: int, plus: int) -> bool:
    signed_sum = sum(
        1 if plus & (1 << element) else -1
        for element in range(N)
        if subset & (1 << element)
    )
    return abs(signed_sum) <= 1


def compatibility_signatures(colors: list[int]) -> list[int]:
    signatures = []
    for subset in range(1 << N):
        bits = 0
        for color_index, plus in enumerate(colors):
            if compatible(subset, plus):
                bits |= 1 << color_index
        signatures.append(bits)
    return signatures


def propagate(
    previous: dict[int, int],
    candidates: list[int],
    compatibility: list[int],
) -> dict[int, int]:
    answer = {}
    for candidate in candidates:
        reachable_colors = 0
        for prior, prior_colors in previous.items():
            if prior & ~candidate == 0:
                reachable_colors |= prior_colors
        reachable_colors &= compatibility[candidate]
        if reachable_colors:
            answer[candidate] = reachable_colors
    return answer


def enumerate_minimum_prefix() -> dict:
    colors = balanced_colorings()  # all 252 signed colorings
    assert len(colors) == 252
    all_colors = (1 << len(colors)) - 1
    compatibility = compatibility_signatures(colors)

    singleton = 1 << 0
    pair_masks = [singleton | (1 << leaf) for leaf in range(1, 6)]
    level1 = {singleton: all_colors & compatibility[singleton]}
    level2_all = propagate(level1, masks_of_weight(2), compatibility)
    level2 = {pair: level2_all[pair] for pair in pair_masks}
    assert set(level2) == set(pair_masks)
    assert sum(level2.values(), 0) != 0  # guard against a vacuous setup
    assert (level2[pair_masks[0]] | level2[pair_masks[1]]) != all_colors
    pair_cover = 0
    for bits in level2.values():
        pair_cover |= bits
    assert pair_cover == all_colors

    level3_candidates = propagate(level2, masks_of_weight(3), compatibility)
    assert len(level3_candidates) == 30
    level3_choices = 0
    level3_live = 0
    level3_coverage_histogram: Counter[int] = Counter()
    live_triples: list[tuple[tuple[int, ...], dict[int, int]]] = []
    for choice in combinations(sorted(level3_candidates), 3):
        level3_choices += 1
        selected = {subset: level3_candidates[subset] for subset in choice}
        covered = 0
        for bits in selected.values():
            covered |= bits
        covered_count = covered.bit_count()
        level3_coverage_histogram[covered_count] += 1
        if covered == all_colors:
            level3_live += 1
            live_triples.append((choice, selected))

    digest = hashlib.sha256()
    level4_choices = 0
    level4_maximum = 0
    level4_coverage_histogram: Counter[int] = Counter()
    candidate_count_histogram: Counter[int] = Counter()
    best_branches: list[dict] = []

    for triple_choice, level3 in live_triples:
        level4_candidates = propagate(level3, masks_of_weight(4), compatibility)
        ordered_candidates = sorted(level4_candidates)
        candidate_count_histogram[len(ordered_candidates)] += 1
        for four_choice in combinations(ordered_candidates, 5):
            level4_choices += 1
            covered = 0
            for subset in four_choice:
                covered |= level4_candidates[subset]
            assert covered != all_colors, (
                "unexpected minimum-count prefix reaches every coloring: "
                f"triples={triple_choice}, fours={four_choice}"
            )
            covered_count = covered.bit_count()
            level4_coverage_histogram[covered_count] += 1
            if covered_count > level4_maximum:
                level4_maximum = covered_count
                best_branches = []
            if covered_count == level4_maximum and len(best_branches) < 10:
                missing = all_colors ^ covered
                best_branches.append(
                    {
                        "triple_masks": list(triple_choice),
                        "four_masks": list(four_choice),
                        "covered_signed_colorings": covered_count,
                        "missing_plus_masks": [
                            colors[index]
                            for index in range(len(colors))
                            if missing & (1 << index)
                        ],
                    }
                )
            for subset in triple_choice:
                digest.update(subset.to_bytes(2, "little"))
            for subset in four_choice:
                digest.update(subset.to_bytes(2, "little"))
            digest.update(covered_count.to_bytes(2, "little"))

    return {
        "schema": "balanced-chain-n10-no-minimum-prefix-v1",
        "epistemic_status": "EXHAUSTIVE FINITE CERTIFICATE; UNFORMALIZED",
        "n": N,
        "signed_balanced_coloring_count": len(colors),
        "normalized_singleton_mask": singleton,
        "normalized_level2_pair_masks": pair_masks,
        "prerequisite_level_counts_0_through_4": [1, 1, 5, 3, 5],
        "reachable_level3_candidate_count": len(level3_candidates),
        "level3_choice_count": level3_choices,
        "level3_live_choice_count": level3_live,
        "level3_coverage_histogram": {
            str(key): level3_coverage_histogram[key]
            for key in sorted(level3_coverage_histogram)
        },
        "level4_reachable_candidate_count_histogram_over_live_level3_choices": {
            str(key): candidate_count_histogram[key]
            for key in sorted(candidate_count_histogram)
        },
        "level4_choice_count": level4_choices,
        "level4_maximum_signed_colorings_reached": level4_maximum,
        "level4_coverage_histogram": {
            str(key): level4_coverage_histogram[key]
            for key in sorted(level4_coverage_histogram)
        },
        "enumeration_sha256": digest.hexdigest(),
        "first_best_branches": best_branches,
        "conclusion": (
            "No selected prefix with level counts 1,1,5,3,5 can provide "
            "color-specific reachability through level four for all balanced colorings."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--level-certificate",
        type=Path,
        default=Path("certificates/balanced_chain_n10/level_cover_certificate.json"),
    )
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("certificates/balanced_chain_n10/no_minimum_prefix.json"),
    )
    parser.add_argument("--write-certificate", action="store_true")
    args = parser.parse_args()

    levels = json.loads(args.level_certificate.read_text(encoding="utf-8"))
    assert levels["exact_level_minima"][:5] == [1, 1, 5, 3, 5]
    result = enumerate_minimum_prefix()
    if args.write_certificate:
        args.certificate.parent.mkdir(parents=True, exist_ok=True)
        args.certificate.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    else:
        stored = json.loads(args.certificate.read_text(encoding="utf-8"))
        assert stored == result, "stored prefix certificate differs from recomputation"

    print(
        "PASS no exact-minimum n=10 prefix: "
        f"level3={result['level3_choice_count']} choices, "
        f"live={result['level3_live_choice_count']}, "
        f"level4={result['level4_choice_count']} choices, "
        f"maximum={result['level4_maximum_signed_colorings_reached']}/252"
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Serialize the independently found size-35 n=10 upper family."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


N = 10
FULL = (1 << N) - 1
FAMILY = [
    0, 64, 65, 66, 72, 80, 88, 90, 120, 122, 194, 202, 218, 219,
    378, 474, 506, 507, 576, 577, 579, 705, 706, 707, 715, 723, 731,
    739, 755, 763, 987, 1011, 1018, 1019, 1023,
]


def masks_of_weight(weight: int) -> list[int]:
    return [sum(1 << i for i in choice) for choice in combinations(range(N), weight)]


def elements(mask: int) -> list[int]:
    return [element for element in range(N) if mask & (1 << element)]


def compatible(subset: int, plus: int) -> bool:
    return abs(2 * (subset & plus).bit_count() - subset.bit_count()) <= 1


def find_chain(family: set[int], plus: int) -> list[int] | None:
    if 0 not in family or FULL not in family:
        return None
    parent = {0: None}
    for level in range(1, N + 1):
        for subset in sorted(s for s in family if s.bit_count() == level):
            if not compatible(subset, plus):
                continue
            for element in range(N):
                prior = subset ^ (1 << element)
                if subset & (1 << element) and prior in parent:
                    parent[subset] = prior
                    break
    if FULL not in parent:
        return None
    chain = []
    current = FULL
    while current is not None:
        chain.append(current)
        current = parent[current]
    return list(reversed(chain))


def all_maximal_chains(family: set[int]) -> list[list[int]]:
    answer: list[list[int]] = []

    def visit(current: int, chain: list[int]) -> None:
        if current == FULL:
            answer.append(chain)
            return
        for element in range(N):
            if current & (1 << element):
                continue
            nxt = current | (1 << element)
            if nxt in family:
                visit(nxt, chain + [nxt])

    visit(0, [0])
    return answer


def valid_for(family: set[int], plus: int) -> bool:
    return find_chain(family, plus) is not None


def build_document() -> dict:
    family = set(FAMILY)
    assert len(family) == 35
    colors = masks_of_weight(N // 2)
    witnesses = []
    for plus in colors:
        chain = find_chain(family, plus)
        assert chain is not None
        witnesses.append({"plus_mask": plus, "chain_masks": chain})

    maximal_chains = all_maximal_chains(family)
    multiplicities = Counter()
    for plus in colors:
        multiplicities[sum(all(compatible(s, plus) for s in chain) for chain in maximal_chains)] += 1

    removal_losses = {}
    for subset in FAMILY:
        reduced = family - {subset}
        removal_losses[str(subset)] = sum(not valid_for(reduced, plus) for plus in colors)

    singleton = next(subset for subset in family if subset.bit_count() == 1)
    cosingleton = next(subset for subset in family if subset.bit_count() == N - 1)
    return {
        "schema": "balanced-chain-n10-upper-v1",
        "epistemic_status": "EXHAUSTIVELY CHECKABLE FINITE UPPER BOUND; UNFORMALIZED",
        "n": N,
        "claimed_size": len(family),
        "family_masks": FAMILY,
        "family_elements": [elements(subset) for subset in FAMILY],
        "level_counts": [sum(s.bit_count() == level for s in family) for level in range(N + 1)],
        "all_signed_coloring_chain_witnesses": witnesses,
        "structure": {
            "unique_singleton_mask": singleton,
            "unique_cosingleton_mask": cosingleton,
            "cosingleton_missing_element_mask": FULL ^ cosingleton,
            "level2_is_half_star_at_singleton": all(
                subset & singleton for subset in family if subset.bit_count() == 2
            ),
            "upper_level2_complements_are_half_star_at_missing_element": all(
                (FULL ^ subset) & (FULL ^ cosingleton)
                for subset in family
                if subset.bit_count() == N - 2
            ),
            "maximal_chain_count": len(maximal_chains),
            "maximal_chain_masks": maximal_chains,
            "signed_coloring_path_multiplicity_histogram": {
                str(key): multiplicities[key] for key in sorted(multiplicities)
            },
            "single_subset_removal_lost_coloring_counts": removal_losses,
            "inclusion_minimal": all(loss > 0 for loss in removal_losses.values()),
        },
        "scope": "Finite n=10 upper certificate only; no asymptotic inference.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("certificates/balanced_chain_n10/upper_size35.json"),
    )
    args = parser.parse_args()
    document = build_document()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote size {document['claimed_size']} upper certificate for all "
        f"{len(document['all_signed_coloring_chain_witnesses'])} signed colorings"
    )


if __name__ == "__main__":
    main()

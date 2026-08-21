#!/usr/bin/env python3
"""Independent standard-library checker for the n=10 size-35 upper family."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from pathlib import Path


def mask(items) -> int:
    answer = 0
    for item in items:
        answer |= 1 << item
    return answer


def compatible_by_literal_sum(subset: int, plus: int, n: int) -> bool:
    total = 0
    for element in range(n):
        if subset & (1 << element):
            total += 1 if plus & (1 << element) else -1
    return -1 <= total <= 1


def signed_colors(n: int) -> list[int]:
    return [mask(choice) for choice in combinations(range(n), n // 2)]


def enumerate_paths(family: set[int], n: int) -> list[tuple[int, ...]]:
    full = (1 << n) - 1
    paths = []

    def visit(current: int, path: tuple[int, ...]) -> None:
        if current == full:
            paths.append(path)
            return
        for element in range(n):
            if current & (1 << element):
                continue
            nxt = current | (1 << element)
            if nxt in family:
                visit(nxt, path + (nxt,))

    if 0 in family:
        visit(0, (0,))
    return paths


def verify(document: dict) -> None:
    n = document["n"]
    assert n == 10
    full = (1 << n) - 1
    family_list = document["family_masks"]
    family = set(family_list)
    assert len(family) == len(family_list) == document["claimed_size"] == 35
    assert all(0 <= subset <= full for subset in family)
    assert [mask(items) for items in document["family_elements"]] == family_list
    assert 0 in family and full in family
    levels = [sum(s.bit_count() == level for s in family) for level in range(n + 1)]
    assert levels == document["level_counts"] == [1, 1, 5, 3, 6, 3, 6, 3, 5, 1, 1]

    colors = signed_colors(n)
    entries = document["all_signed_coloring_chain_witnesses"]
    assert [entry["plus_mask"] for entry in entries] == colors
    for entry in entries:
        plus = entry["plus_mask"]
        chain = entry["chain_masks"]
        assert len(chain) == n + 1 and chain[0] == 0 and chain[-1] == full
        for level, subset in enumerate(chain):
            assert subset in family and subset.bit_count() == level
            assert compatible_by_literal_sum(subset, plus, n)
            if level:
                assert chain[level - 1] & ~subset == 0
                assert (chain[level - 1] ^ subset).bit_count() == 1

    paths = enumerate_paths(family, n)
    stored_paths = [tuple(path) for path in document["structure"]["maximal_chain_masks"]]
    assert paths == stored_paths
    assert len(paths) == document["structure"]["maximal_chain_count"] == 60

    multiplicity = Counter()
    for plus in colors:
        count = sum(
            all(compatible_by_literal_sum(subset, plus, n) for subset in path)
            for path in paths
        )
        assert count >= 1
        multiplicity[count] += 1
    expected_multiplicity = {
        str(key): multiplicity[key] for key in sorted(multiplicity)
    }
    assert expected_multiplicity == document["structure"]["signed_coloring_path_multiplicity_histogram"]
    assert sum(key * value for key, value in multiplicity.items()) == 60 * (1 << (n // 2))

    removal_losses = {}
    for removed in family_list:
        reduced_paths = enumerate_paths(family - {removed}, n)
        lost = sum(
            not any(
                all(compatible_by_literal_sum(subset, plus, n) for subset in path)
                for path in reduced_paths
            )
            for plus in colors
        )
        removal_losses[str(removed)] = lost
    assert removal_losses == document["structure"]["single_subset_removal_lost_coloring_counts"]
    assert all(loss > 0 for loss in removal_losses.values())
    assert document["structure"]["inclusion_minimal"] is True

    singleton = next(s for s in family if s.bit_count() == 1)
    cosingleton = next(s for s in family if s.bit_count() == n - 1)
    assert singleton == document["structure"]["unique_singleton_mask"]
    assert cosingleton == document["structure"]["unique_cosingleton_mask"]
    assert full ^ cosingleton == document["structure"]["cosingleton_missing_element_mask"]
    assert all(singleton & pair for pair in family if pair.bit_count() == 2)
    missing = full ^ cosingleton
    assert all(missing & (full ^ upper) for upper in family if upper.bit_count() == n - 2)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("certificates/balanced_chain_n10/upper_size35.json"),
    )
    args = parser.parse_args()
    document = json.loads(args.certificate.read_text(encoding="utf-8"))
    verify(document)
    print("PASS n=10 size-35 family for all 252 signed colorings")
    print("PASS 60 maximal chains and structural metadata")
    print("PASS inclusion-minimality under every single-subset deletion")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent finite checks for the Cycle-3 CP-G gluing audit.

The program uses only the Python standard library and the literal balanced-
chain definition.  It does not import any optimizer or earlier certificate
checker.  It performs four separate checks:

* exhaust all set families for n=2 and n=4 to find the first failure of the
  tempting "every adjacent interface works for every color" gluing rule;
* independently re-establish the needed lower-half level-cover minima for
  n=8 and n=10, using a relabelled first member of a putative smaller cover;
* exhaust the normalized exact-minimum prefixes through rank four at n=8
  and n=10; and
* verify literal source-to-sink reachability of displayed size-20 and size-35
  families, without trusting their stored witness paths.

All colorings are signed: a positive set and its complement are both kept.
The finite computations do not imply any asymptotic statement.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path


N8_UPPER = [
    0, 1, 3, 5, 7, 15, 17, 23, 31, 63, 65, 81, 85, 95, 113, 117,
    119, 125, 127, 255,
]

N10_UPPER = [
    0, 64, 65, 66, 72, 80, 88, 90, 120, 122, 194, 202, 218, 219,
    378, 474, 506, 507, 576, 577, 579, 705, 706, 707, 715, 723,
    731, 739, 755, 763, 987, 1011, 1018, 1019, 1023,
]

LOWER_COVER_WITNESSES = {
    8: {
        0: [0],
        1: [1],
        2: [3, 5, 9, 17],
        3: [7, 25],
        4: [202, 178, 120],
    },
    10: {
        0: [0],
        1: [512],
        2: [80, 528, 96, 160, 768],
        3: [21, 261, 530],
        4: [643, 101, 396, 564, 420],
        5: [230, 186, 220],
    },
}

LOWER_TAU = {
    8: [1, 1, 4, 2, 3],
    10: [1, 1, 5, 3, 5, 3],
}


def masks_of_weight(n: int, weight: int) -> list[int]:
    return [sum(1 << item for item in choice) for choice in combinations(range(n), weight)]


def signed_colors(n: int) -> list[int]:
    return masks_of_weight(n, n // 2)


def compatibility_signatures(n: int) -> tuple[list[int], int, list[int]]:
    colors = signed_colors(n)
    signatures: list[int] = []
    for subset in range(1 << n):
        size = subset.bit_count()
        bits = 0
        for color_index, positive in enumerate(colors):
            intersection = (subset & positive).bit_count()
            if abs(2 * intersection - size) <= 1:
                bits |= 1 << color_index
        signatures.append(bits)
    return colors, (1 << len(colors)) - 1, signatures


def levels(n: int, family: list[int] | set[int]) -> list[list[int]]:
    return [sorted(s for s in family if s.bit_count() == k) for k in range(n + 1)]


def propagated_reachability(
    n: int, family: list[int] | set[int], signatures: list[int], all_colors: int
) -> int:
    by_level = levels(n, family)
    if 0 not in by_level[0]:
        return 0
    reachable = {0: all_colors}
    for k in range(1, n + 1):
        next_reachable: dict[int, int] = {}
        for current in by_level[k]:
            bits = 0
            for prior, prior_bits in reachable.items():
                if prior & ~current == 0:
                    bits |= prior_bits
            bits &= signatures[current]
            if bits:
                next_reachable[current] = bits
        reachable = next_reachable
    return reachable.get((1 << n) - 1, 0)


def covers_every_color(selected: tuple[int, ...] | list[int], signatures: list[int], all_colors: int) -> bool:
    covered = 0
    for subset in selected:
        covered |= signatures[subset]
    return covered == all_colors


def adjacent_interfaces_cover(
    n: int, family: set[int], signatures: list[int], all_colors: int
) -> bool:
    by_level = levels(n, family)
    if any(not covers_every_color(level, signatures, all_colors) for level in by_level):
        return False
    for k in range(1, n + 1):
        covered = 0
        for lower in by_level[k - 1]:
            for upper in by_level[k]:
                if lower & ~upper == 0:
                    covered |= signatures[lower] & signatures[upper]
        if covered != all_colors:
            return False
    return True


def exhaustive_adjacent_interface_search(n: int) -> dict:
    """Exhaust all families with endpoints; feasible here only for n<=4."""

    colors, all_colors, signatures = compatibility_signatures(n)
    full = (1 << n) - 1
    interior = list(range(1, full))
    locally_glued = 0
    bad_histogram: Counter[int] = Counter()
    first_by_size: dict[int, tuple[list[int], int]] = {}

    for choice_bits in range(1 << len(interior)):
        family = {0, full}
        for index, subset in enumerate(interior):
            if choice_bits & (1 << index):
                family.add(subset)
        if not adjacent_interfaces_cover(n, family, signatures, all_colors):
            continue
        locally_glued += 1
        reached = propagated_reachability(n, family, signatures, all_colors)
        if reached != all_colors:
            size = len(family)
            bad_histogram[size] += 1
            candidate = (sorted(family), reached)
            if size not in first_by_size or candidate[0] < first_by_size[size][0]:
                first_by_size[size] = candidate

    if first_by_size:
        minimum_bad_size = min(first_by_size)
        first_family, reached = first_by_size[minimum_bad_size]
        missing = [
            colors[index]
            for index in range(len(colors))
            if not reached & (1 << index)
        ]
    else:
        minimum_bad_size = None
        first_family = None
        missing = []

    return {
        "n": n,
        "families_with_endpoints_exhausted": 1 << len(interior),
        "families_passing_all_adjacent_interfaces": locally_glued,
        "bad_family_count_by_size": {
            str(size): bad_histogram[size] for size in sorted(bad_histogram)
        },
        "minimum_bad_size": minimum_bad_size,
        "lexicographically_first_minimum_bad_family_masks": first_family,
        "missing_positive_masks": missing,
    }


def exact_lower_half_tau(n: int) -> dict:
    """Verify witnesses and exhaust covers one smaller, modulo relabelling."""

    _, all_colors, signatures = compatibility_signatures(n)
    minima = LOWER_TAU[n]
    witnesses = LOWER_COVER_WITNESSES[n]
    results: dict[str, dict] = {}

    for k, claimed in enumerate(minima):
        witness = witnesses[k]
        assert len(witness) == claimed
        assert all(subset.bit_count() == k for subset in witness)
        assert covers_every_color(witness, signatures, all_colors)

        tested_size = claimed - 1
        maximum = 0
        branch_count = 0
        if tested_size == 0:
            branch_count = 1
        else:
            # Any first member of a hypothetical cover can be relabelled to
            # {0,...,k-1}; S_n acts transitively on rank-k subsets and on the
            # balanced colorings.  Enumerate all remaining distinct members.
            canonical = (1 << k) - 1
            remaining = [s for s in masks_of_weight(n, k) if s != canonical]
            for tail in combinations(remaining, tested_size - 1):
                branch_count += 1
                covered = signatures[canonical]
                for subset in tail:
                    covered |= signatures[subset]
                maximum = max(maximum, covered.bit_count())
                assert covered != all_colors
            assert branch_count == comb(len(remaining), tested_size - 1)

        results[str(k)] = {
            "tau": claimed,
            "one_smaller_size": tested_size,
            "normalized_branch_count": branch_count,
            "maximum_signed_colors_covered": maximum,
        }

    full_profile = minima + minima[-2::-1]
    assert len(full_profile) == n + 1
    return {
        "lower_half": results,
        "full_tau_by_complementation": full_profile,
        "level_sum": sum(full_profile),
    }


def propagate_candidates(
    n: int, previous: dict[int, int], rank: int, signatures: list[int]
) -> dict[int, int]:
    answer: dict[int, int] = {}
    for current in masks_of_weight(n, rank):
        reached = 0
        for prior, prior_colors in previous.items():
            if prior & ~current == 0:
                reached |= prior_colors
        reached &= signatures[current]
        if reached:
            answer[current] = reached
    return answer


def exact_minimum_prefix_search(n: int, triples_needed: int, fours_needed: int) -> dict:
    """Exhaust the normalized minimum prefix at ranks 0,...,4."""

    colors, all_colors, signatures = compatibility_signatures(n)
    singleton = 1
    # With one singleton and exactly tau(n,2)=n/2 usable pairs, every pair
    # must meet the singleton and their other endpoints are relabelled here.
    pairs = [singleton | (1 << leaf) for leaf in range(1, n // 2 + 1)]
    pair_reach = {pair: signatures[pair] for pair in pairs}
    assert covers_every_color(pairs, signatures, all_colors)

    triple_candidates = propagate_candidates(n, pair_reach, 3, signatures)
    triple_histogram: Counter[int] = Counter()
    live_triples: list[dict[int, int]] = []
    for choice in combinations(sorted(triple_candidates), triples_needed):
        covered = 0
        for subset in choice:
            covered |= triple_candidates[subset]
        triple_histogram[covered.bit_count()] += 1
        if covered == all_colors:
            live_triples.append({s: triple_candidates[s] for s in choice})

    rank4_histogram: Counter[int] = Counter()
    rank4_candidate_histogram: Counter[int] = Counter()
    rank4_choices = 0
    rank4_maximum = 0
    rank4_full = 0
    first_max_missing: list[int] = []
    for selected_triples in live_triples:
        rank4_candidates = propagate_candidates(n, selected_triples, 4, signatures)
        ordered = sorted(rank4_candidates)
        rank4_candidate_histogram[len(ordered)] += 1
        for choice in combinations(ordered, fours_needed):
            rank4_choices += 1
            covered = 0
            for subset in choice:
                covered |= rank4_candidates[subset]
            count = covered.bit_count()
            rank4_histogram[count] += 1
            if count == len(colors):
                rank4_full += 1
            if count > rank4_maximum:
                rank4_maximum = count
                first_max_missing = [
                    colors[index]
                    for index in range(len(colors))
                    if not covered & (1 << index)
                ]

    return {
        "n": n,
        "normalized_singleton_mask": singleton,
        "normalized_pair_masks": pairs,
        "reachable_triple_candidate_count": len(triple_candidates),
        "triple_choice_count": sum(triple_histogram.values()),
        "triple_live_choice_count": len(live_triples),
        "triple_coverage_histogram": {
            str(count): triple_histogram[count] for count in sorted(triple_histogram)
        },
        "rank4_candidate_count_histogram": {
            str(count): rank4_candidate_histogram[count]
            for count in sorted(rank4_candidate_histogram)
        },
        "rank4_choice_count": rank4_choices,
        "rank4_full_choice_count": rank4_full,
        "rank4_maximum_signed_colors_reached": rank4_maximum,
        "first_maximum_missing_positive_masks": first_max_missing,
        "rank4_coverage_histogram": {
            str(count): rank4_histogram[count] for count in sorted(rank4_histogram)
        },
    }


def verify_upper(n: int, family: list[int], tau_profile: list[int]) -> dict:
    colors, all_colors, signatures = compatibility_signatures(n)
    assert len(family) == len(set(family))
    assert min(family) == 0 and max(family) == (1 << n) - 1
    profile = [sum(subset.bit_count() == k for subset in family) for k in range(n + 1)]
    reached = propagated_reachability(n, family, signatures, all_colors)
    assert reached == all_colors
    excess = [profile[k] - tau_profile[k] for k in range(n + 1)]
    assert all(value >= 0 for value in excess)
    embedded_minimum_covers: dict[str, int] = {}
    by_level = levels(n, family)
    for k, value in enumerate(excess):
        if value:
            embedded_minimum_covers[str(k)] = sum(
                covers_every_color(choice, signatures, all_colors)
                for choice in combinations(by_level[k], tau_profile[k])
            )
    return {
        "n": n,
        "distinct_subset_count": len(family),
        "level_counts": profile,
        "tau_profile": tau_profile,
        "level_sum": sum(tau_profile),
        "excess_by_level": excess,
        "minimum_cover_subfamilies_within_surplus_levels": embedded_minimum_covers,
        "signed_colors_with_source_to_sink_path": reached.bit_count(),
        "signed_balanced_color_count": len(colors),
    }


def recompute() -> dict:
    tau8 = exact_lower_half_tau(8)
    tau10 = exact_lower_half_tau(10)
    assert tau8["level_sum"] == 19
    assert tau10["level_sum"] == 33

    prefix8 = exact_minimum_prefix_search(8, triples_needed=2, fours_needed=3)
    prefix10 = exact_minimum_prefix_search(10, triples_needed=3, fours_needed=5)
    assert prefix8["rank4_full_choice_count"] == 0
    assert prefix10["rank4_full_choice_count"] == 0

    upper8 = verify_upper(8, N8_UPPER, tau8["full_tau_by_complementation"])
    upper10 = verify_upper(10, N10_UPPER, tau10["full_tau_by_complementation"])
    assert sum(upper8["excess_by_level"]) == 1
    assert sum(upper10["excess_by_level"]) == 2

    adjacent2 = exhaustive_adjacent_interface_search(2)
    adjacent4 = exhaustive_adjacent_interface_search(4)
    assert adjacent2["minimum_bad_size"] is None
    assert adjacent4["minimum_bad_size"] == 7

    return {
        "schema": "cycle03-cp-g-gluing-certificate-v1",
        "epistemic_status": "EXHAUSTIVE FINITE COMPUTATION; UNFORMALIZED",
        "adjacent_interface_rule": {"n2": adjacent2, "n4": adjacent4},
        "level_cover_checks": {"n8": tau8, "n10": tau10},
        "minimum_prefix_obstructions": {"n8": prefix8, "n10": prefix10},
        "positive_full_families": {"n8": upper8, "n10": upper10},
        "scope": "Finite n=2,4,8,10 checks only; no asymptotic inference.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("certificates/cycle03_cp_g_gluing.json"),
    )
    parser.add_argument("--print-json", action="store_true")
    args = parser.parse_args()

    result = recompute()
    if args.print_json:
        print(json.dumps(result, indent=2))
        return

    stored = json.loads(args.certificate.read_text(encoding="utf-8"))
    assert stored == result
    print("PASS adjacent-interface gluing: exhaustive first failure at n=4")
    print("PASS exact-minimum prefix obstruction: n=8 and n=10")
    print("PASS distinct-state/reachability checks: size 20 at n=8; size 35 at n=10")
    print("ALL CYCLE-3 CP-G CHECKS PASS")


if __name__ == "__main__":
    main()

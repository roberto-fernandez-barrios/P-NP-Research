#!/usr/bin/env python3
"""Independent finite checks for the Cycle-3 CP-S/recursion attack.

This script uses only the Python standard library.  It does not import the
Cycle-2 optimizer or any Cycle-3 n=10 search code.  Stored n=4,6,8 families
are treated only as candidate witnesses and are checked from the definition.

The checks are finite evidence.  The general CP-S bottleneck and the
one-step defect-router lift are proved in the accompanying note.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def subset_mask(points):
    ans = 0
    for point in points:
        ans |= 1 << point
    return ans


def level_masks(n, level):
    return [subset_mask(c) for c in itertools.combinations(range(n), level)]


def positive_masks(n, positive_count):
    return [subset_mask(c) for c in itertools.combinations(range(n), positive_count)]


def imbalance(mask, positive_mask):
    return 2 * (mask & positive_mask).bit_count() - mask.bit_count()


def has_band_path(n, family, positive_mask, lower, upper):
    """Literal selected-subset reachability with a prescribed imbalance band."""
    full = (1 << n) - 1
    reached = {0} if 0 in family and lower <= 0 <= upper else set()
    for level in range(1, n + 1):
        for mask in family:
            if mask.bit_count() != level:
                continue
            if not lower <= imbalance(mask, positive_mask) <= upper:
                continue
            if any(
                (mask ^ (1 << point)) in reached
                for point in range(n)
                if mask & (1 << point)
            ):
                reached.add(mask)
    return full in reached


def is_balanced_chain_family(n, family):
    return all(
        has_band_path(n, family, positive, -1, 1)
        for positive in positive_masks(n, n // 2)
    )


def defect_failures(n, family):
    """Colorings of total +/-2 lacking a one-sided defect chain."""
    failures = []
    for positive_count in (n // 2 - 1, n // 2 + 1):
        total = 2 * positive_count - n
        lower, upper = min(0, total), max(0, total)
        for positive in positive_masks(n, positive_count):
            if not has_band_path(n, family, positive, lower, upper):
                failures.append(positive)
    return failures


def uncolored_path_vertices(n, family):
    """Vertices on at least one uncolored empty-to-full selected path."""
    full = (1 << n) - 1
    forward = {0} if 0 in family else set()
    for level in range(1, n + 1):
        for mask in family:
            if mask.bit_count() == level and any(
                (mask ^ (1 << point)) in forward
                for point in range(n)
                if mask & (1 << point)
            ):
                forward.add(mask)

    backward = {full} if full in family else set()
    for level in range(n - 1, -1, -1):
        for mask in family:
            if mask.bit_count() == level and any(
                (mask | (1 << point)) in backward
                for point in range(n)
                if not mask & (1 << point)
            ):
                backward.add(mask)
    return forward & backward


def check_cp_s2_witness(n, family):
    """Check the exact minimum-star/two-odd-width profile CP-SQ."""
    m = n // 2
    counts = Counter(mask.bit_count() for mask in family)
    expected = {0: 1, n: 1, 1: 1, n - 1: 1}
    expected.update({level: m for level in range(2, n - 1, 2)})
    expected.update({level: 2 for level in range(3, n - 2, 2)})
    assert [counts[level] for level in range(n + 1)] == [
        expected[level] for level in range(n + 1)
    ]
    assert len(family) == m * (m + 1)

    singleton = next(mask for mask in family if mask.bit_count() == 1)
    v = singleton.bit_length() - 1
    cosingleton = next(mask for mask in family if mask.bit_count() == n - 1)
    omitted = ((1 << n) - 1) ^ cosingleton
    w = omitted.bit_length() - 1
    assert v != w

    pairs = [mask for mask in family if mask.bit_count() == 2]
    assert all(mask & (1 << v) for mask in pairs)
    upper = [mask for mask in family if mask.bit_count() == n - 2]
    assert all(not (mask & (1 << w)) for mask in upper)
    assert all((((1 << n) - 1) ^ mask).bit_count() == 2 for mask in upper)
    assert all(mask in uncolored_path_vertices(n, family) for mask in family)
    assert is_balanced_chain_family(n, family)
    return v, w


def diamond_spine_family(n, rails):
    """Generate the exact union of odd checkpoints and two-step diamonds."""
    full = (1 << n) - 1
    family = {0, full}
    for rail in rails:
        family.update(rail)
        for lower, upper in zip(rail, rail[1:]):
            difference = upper ^ lower
            assert lower & ~upper == 0 and difference.bit_count() == 2
            for point in range(n):
                if difference & (1 << point):
                    family.add(lower | (1 << point))
    return family


def check_stored_cp_s2_examples():
    rail_checkpoints = {
        4: ([1, 7], [1, 7]),
        6: ([1, 7, 31], [1, 19, 31]),
        8: ([1, 7, 31, 127], [1, 81, 117, 127]),
    }
    for n in (4, 6, 8):
        path = ROOT / "certificates" / "balanced_chain_exact" / f"exact_n{n}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        family = set(data["family_masks"])
        v, w = check_cp_s2_witness(n, family)
        generated = diamond_spine_family(n, rail_checkpoints[n])
        assert generated == family
        print(
            f"PASS CP-SD/CP-SQ witness n={n}: size={len(family)}, "
            f"lower anchor={v}, upper omitted anchor={w}"
        )


def check_cp_s2_first_obstruction():
    """Exhaust the local n=10 two-triple bottleneck after fixing its star."""
    n = 10
    m = n // 2
    anchor = 0
    leaves = tuple(range(1, m + 1))
    triples = level_masks(n, 3)
    branches = 0
    maximum_live = 0
    for first, second in itertools.combinations(triples, 2):
        branches += 1
        live = [
            leaf
            for leaf in leaves
            if any(
                (triple & (1 << anchor))
                and (triple & (1 << leaf))
                for triple in (first, second)
            )
        ]
        maximum_live = max(maximum_live, len(live))
        assert len(live) <= 4

        # This is the constructive S1-style countercolor: anchor and every
        # leaf that can continue to a selected triple are positive; fill to m.
        positive_points = [anchor, *live]
        for point in range(n):
            if len(positive_points) == m:
                break
            if point not in positive_points:
                positive_points.append(point)
        positive = subset_mask(positive_points)
        assert positive.bit_count() == m
        for leaf in live:
            pair = (1 << anchor) | (1 << leaf)
            assert imbalance(pair, positive) != 0

    assert branches == 7140
    assert maximum_live == 4 < m
    assert 6 * m - 4 == 26  # collision-free upper accounting for two diamonds
    print(
        "PASS CP-SD/CP-SQ n=10 obstruction: two rails expose at most 4 leaves; "
        "7140 two-triple choices continue at most 4 of 5 star leaves"
    )


def coverage_bits(candidate, colors):
    ans = 0
    for index, positive in enumerate(colors):
        if abs(imbalance(candidate, positive)) <= 1:
            ans |= 1 << index
    return ans


def check_n10_level_cover_bound():
    """Fresh exhaustive proof of tau(10,k), using only level transitivity."""
    n = 10
    colors = positive_masks(n, n // 2)
    all_colors = (1 << len(colors)) - 1
    claimed_tau = [1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1]
    witnesses = {
        0: [0],
        1: [512],
        2: [80, 528, 96, 160, 768],
        3: [21, 261, 530],
        4: [643, 101, 396, 564, 420],
        5: [230, 186, 220],
    }
    expected_lower_stats = {
        0: (1, 0),
        1: (1, 0),
        2: (13244, 250),
        3: (119, 250),
        4: (1499784, 248),
        5: (251, 244),
    }

    for level in range(6):
        candidates = level_masks(n, level)
        cover = {candidate: coverage_bits(candidate, colors) for candidate in candidates}
        witness_union = 0
        for candidate in witnesses[level]:
            assert candidate in cover
            witness_union |= cover[candidate]
        assert witness_union == all_colors

        target = claimed_tau[level]
        if target == 1:
            branches, max_covered = 1, 0
        else:
            # If a (target-1)-cover existed, point transitivity lets us map
            # any member to {0,...,level-1}.  Smaller covers can be padded.
            canonical = (1 << level) - 1
            others = [candidate for candidate in candidates if candidate != canonical]
            choose_count = target - 2
            branches = 0
            max_covered = 0
            for tail in itertools.combinations(others, choose_count):
                branches += 1
                union = cover[canonical]
                for candidate in tail:
                    union |= cover[candidate]
                covered = union.bit_count()
                max_covered = max(max_covered, covered)
                assert union != all_colors
        assert (branches, max_covered) == expected_lower_stats[level]
        print(
            f"PASS tau(10,{level})={target}: lower branches={branches}, "
            f"maximum={max_covered}/252; witness covers all"
        )

    for level in range(6, 11):
        assert claimed_tau[level] == claimed_tau[n - level]
    assert sum(claimed_tau) == 33
    print("PASS exact level-cover sum: L(10)=33, hence N(10)>=33 and size 30 is impossible")


def check_n10_minimum_prefix_and_upper():
    """Independent reachability recomputation of the extra n=10 dependencies."""
    n = 10
    colors = positive_masks(n, n // 2)
    all_colors = (1 << len(colors)) - 1
    compatibility = [coverage_bits(mask, colors) for mask in range(1 << n)]

    # Normalize the unique singleton and five live pairs by point relabeling.
    root = 1
    pair_reach = {
        root | (1 << leaf): compatibility[root | (1 << leaf)]
        for leaf in range(1, 6)
    }
    triple_reach = {}
    for triple in level_masks(n, 3):
        prior = 0
        for pair, signature in pair_reach.items():
            if pair & ~triple == 0:
                prior |= signature
        signature = prior & compatibility[triple]
        if signature:
            triple_reach[triple] = signature
    assert len(triple_reach) == 30

    triple_choices = 0
    live_triple_choices = []
    for chosen in itertools.combinations(sorted(triple_reach), 3):
        triple_choices += 1
        union = 0
        for triple in chosen:
            union |= triple_reach[triple]
        if union == all_colors:
            live_triple_choices.append(chosen)
    assert triple_choices == 4060
    assert len(live_triple_choices) == 90

    four_choices = 0
    max_reached = 0
    max_count = 0
    for chosen_triples in live_triple_choices:
        four_reach = {}
        for four in level_masks(n, 4):
            prior = 0
            for triple in chosen_triples:
                if triple & ~four == 0:
                    prior |= triple_reach[triple]
            signature = prior & compatibility[four]
            if signature:
                four_reach[four] = signature
        for chosen_fours in itertools.combinations(sorted(four_reach), 5):
            four_choices += 1
            union = 0
            for four in chosen_fours:
                union |= four_reach[four]
            reached = union.bit_count()
            if reached > max_reached:
                max_reached = reached
                max_count = 1
            elif reached == max_reached:
                max_count += 1
            assert union != all_colors
    assert four_choices == 1686060
    assert max_reached == 250
    assert max_count == 15120

    # Treat the stored family masks only as a candidate upper witness.  Do
    # not use its serialized chains or structural metadata.
    upper_path = ROOT / "certificates" / "balanced_chain_n10" / "upper_size35.json"
    upper_document = json.loads(upper_path.read_text(encoding="utf-8"))
    upper_family = set(upper_document["family_masks"])
    assert len(upper_family) == 35
    assert is_balanced_chain_family(n, upper_family)

    # With level sum 33, a size-34 family has one surplus level.  A surplus
    # at 5..9 leaves the forbidden lower prefix; one at 1..4 leaves its
    # complement-dual forbidden suffix.  Levels 0 and 10 cannot have surplus.
    endpoint_cases = [level for level in range(n + 1) if level in (0, n)]
    dual_suffix_cases = [level for level in range(n + 1) if 1 <= level <= 4]
    lower_prefix_cases = [level for level in range(n + 1) if 5 <= level <= 9]
    assert (endpoint_cases, dual_suffix_cases, lower_prefix_cases) == (
        [0, 10],
        [1, 2, 3, 4],
        [5, 6, 7, 8, 9],
    )
    assert all(len(level_masks(n, level)) == 1 for level in endpoint_cases)
    print(
        "PASS independent N(10) dependencies: no minimum prefix "
        f"({four_choices} branches, max {max_reached}/252), size-35 family valid"
    )
    print("PASS finite conclusion N(10)=35 and sigma(10)=2")


def self_router_lift(old_n, family):
    """The exact natural lift using the entire old family as defect router."""
    a = old_n
    b = old_n + 1
    old_full = (1 << old_n) - 1
    new_full = (1 << (old_n + 2)) - 1
    shifted = {mask | (1 << a) for mask in family}
    return set(family) | shifted | {old_full | (1 << b), new_full}


def masks_as_tuples(n, masks):
    return [tuple(i for i in range(n) if mask & (1 << i)) for mask in masks]


def check_recursion_failure():
    # The n=2 canonical family is both balanced and a one-sided +/-2 router.
    family = {0, 1, 3}
    assert is_balanced_chain_family(2, family)
    assert defect_failures(2, family) == []

    family4 = self_router_lift(2, family)
    assert len(family4) == 2 * len(family) + 2 == 8
    assert is_balanced_chain_family(4, family4)
    assert defect_failures(4, family4) == []

    family6 = self_router_lift(4, family4)
    assert len(family6) == 2 * len(family4) + 2 == 18
    assert is_balanced_chain_family(6, family6)
    failures6 = defect_failures(6, family6)
    assert masks_as_tuples(6, failures6) == [(4, 5), (0, 1, 2, 3)]

    # Continuing despite loss of the required property first loses balanced
    # coverage at n=8, for the same complementary pair of defect colorings.
    family8 = self_router_lift(6, family6)
    assert len(family8) == 2 * len(family6) + 2 == 38
    balanced_failures8 = [
        positive
        for positive in positive_masks(8, 4)
        if not has_band_path(8, family8, positive, -1, 1)
    ]
    assert masks_as_tuples(8, balanced_failures8) == [
        (0, 1, 2, 3),
        (4, 5, 6, 7),
    ]
    print(
        "PASS recursion falsification: self-router property first fails at n=6 "
        "for positives {4,5} and its complement; continued lift first misses "
        "balanced colorings at n=8"
    )


def main():
    check_stored_cp_s2_examples()
    check_cp_s2_first_obstruction()
    check_n10_level_cover_bound()
    check_n10_minimum_prefix_and_upper()
    check_recursion_failure()
    print("ALL CYCLE-3 CP-S/RECURSION CHECKS PASS")


if __name__ == "__main__":
    main()

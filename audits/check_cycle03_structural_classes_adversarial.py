#!/usr/bin/env python3
"""Independent adversarial checks for Cycle-3 CP-S, CP-P, and CP-G.

No proposer module is imported.  In particular, hierarchy validity and its
two-defect terminal property are checked in the contracted even-state graph,
whereas the proposer used the uncontracted Boolean-lattice reachability.
Finite output is evidence for the exact finite statements only.
"""

from __future__ import annotations

import itertools
import json
from collections import Counter
from functools import lru_cache
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def level(n: int, rank: int) -> tuple[int, ...]:
    return tuple(
        sum(1 << i for i in choice)
        for choice in itertools.combinations(range(n), rank)
    )


def plus_masks(n: int, count: int) -> tuple[int, ...]:
    return level(n, count)


def discrepancy(state: int, plus: int) -> int:
    return 2 * (state & plus).bit_count() - state.bit_count()


def literal_band_path(n: int, family: set[int], plus: int, lo: int, hi: int) -> bool:
    """Uncontracted selected path with every prefix discrepancy in [lo,hi]."""
    full = (1 << n) - 1
    reached = {0} if 0 in family and lo <= 0 <= hi else set()
    for rank in range(1, n + 1):
        nxt = set()
        for state in family:
            if state.bit_count() != rank or not lo <= discrepancy(state, plus) <= hi:
                continue
            if any(
                (state ^ bit) in reached
                for bit in (1 << i for i in range(n))
                if state & bit
            ):
                nxt.add(state)
        reached = nxt
    return full in reached


def contracted_reached(n: int, family: set[int], plus: int, stop: int | None = None) -> set[int]:
    """Reachable selected even states using crossing pairs and an odd bridge."""
    if stop is None:
        stop = n
    reached = {0} if 0 in family else set()
    for rank in range(2, stop + 1, 2):
        nxt = set()
        for upper in (s for s in family if s.bit_count() == rank):
            elements = [i for i in range(n) if upper & (1 << i)]
            for first, second in itertools.combinations(elements, 2):
                lower = upper ^ (1 << first) ^ (1 << second)
                if lower not in reached:
                    continue
                if bool(plus & (1 << first)) == bool(plus & (1 << second)):
                    continue
                if (lower | (1 << first) in family or
                        lower | (1 << second) in family):
                    nxt.add(upper)
                    break
        reached = nxt
    return reached


@lru_cache(None)
def balanced_pair_signatures(n: int) -> tuple[int, dict[tuple[int, int], int]]:
    colors = plus_masks(n, n // 2)
    all_bits = (1 << len(colors)) - 1
    signatures = {}
    for first in range(n):
        for second in range(first + 1, n):
            bits = 0
            for index, plus in enumerate(colors):
                if bool(plus & (1 << first)) != bool(plus & (1 << second)):
                    bits |= 1 << index
            signatures[(first, second)] = bits
    return all_bits, signatures


def contracted_accepted_bits(n: int, family: set[int]) -> int:
    """Propagate every balanced color at once in the contracted pair DAG."""
    all_bits, pair_signatures = balanced_pair_signatures(n)
    reached = {0: all_bits} if 0 in family else {}
    for rank in range(2, n + 1, 2):
        nxt = {}
        for upper in (s for s in family if s.bit_count() == rank):
            colors = 0
            elements = [i for i in range(n) if upper & (1 << i)]
            for first, second in itertools.combinations(elements, 2):
                lower = upper ^ (1 << first) ^ (1 << second)
                if lower not in reached:
                    continue
                if (lower | (1 << first) not in family and
                        lower | (1 << second) not in family):
                    continue
                colors |= reached[lower] & pair_signatures[(first, second)]
            if colors:
                nxt[upper] = colors
        reached = nxt
    return reached.get((1 << n) - 1, 0)


def balanced_family_contracted(n: int, family: set[int]) -> bool:
    all_bits, _ = balanced_pair_signatures(n)
    return contracted_accepted_bits(n, family) == all_bits


def one_sided_defect_router(n: int, family: set[int]) -> bool:
    for count in (n // 2 - 1, n // 2 + 1):
        total = 2 * count - n
        for plus in plus_masks(n, count):
            if not literal_band_path(n, family, plus, min(0, total), max(0, total)):
                return False
    return True


def dtp(n: int, family: set[int]) -> tuple[bool, int | None]:
    """Two-defect terminal property via the contracted crossing-pair DAG."""
    full = (1 << n) - 1
    for count in (n // 2 - 1, n // 2 + 1):
        majority_plus = count > n // 2
        for plus in plus_masks(n, count):
            candidates = contracted_reached(n, family, plus, n - 2)
            good = False
            for state in candidates:
                omitted = full ^ state
                if omitted.bit_count() != 2:
                    continue
                signs = [bool(plus & (1 << i)) for i in range(n) if omitted & (1 << i)]
                if signs == [majority_plus, majority_plus]:
                    good = True
                    break
            if not good:
                return False, plus
    return True, None


# ---------------------------------------------------------------------------
# CP-S and defect lifts


def self_router_lift(n: int, old: set[int]) -> set[int]:
    old_full = (1 << n) - 1
    a, b = 1 << n, 1 << (n + 1)
    return old | {a | state for state in old} | {old_full | b, old_full | a | b}


def defect_lift(n: int, x_family: set[int], router: set[int]) -> set[int]:
    old_full = (1 << n) - 1
    a, b = 1 << n, 1 << (n + 1)
    return x_family | {a | state for state in router} | {old_full | b, old_full | a | b}


def check_cp_s() -> dict:
    # Adversarially exhaust the q=2 terminal-fanout boundary at n=10.  Any
    # q<2 choice can be padded, and q=2 is still below ceil(5/2)=3.
    n = 10
    anchor = 0
    star_pairs = {(1 << anchor) | (1 << leaf) for leaf in range(1, 6)}
    triple_list = level(n, 3)
    max_live = 0
    branches = 0
    for selected in itertools.combinations(triple_list, 2):
        branches += 1
        live = {
            leaf
            for leaf in range(1, 6)
            if any(((1 << anchor) | (1 << leaf)) & ~triple == 0 for triple in selected)
        }
        max_live = max(max_live, len(live))
        prescribed = {anchor, *live}
        for point in range(n):
            if len(prescribed) == n // 2:
                break
            prescribed.add(point)
        assert len(prescribed) == n // 2
        plus = sum(1 << point for point in prescribed)
        prefix_family = {0, 1 << anchor} | star_pairs | set(selected)
        # There is no compatible selected path even through rank three.
        reached = {0}
        for rank in (1, 2, 3):
            reached = {
                state
                for state in prefix_family
                if state.bit_count() == rank
                and abs(discrepancy(state, plus)) <= 1
                and any(
                    state ^ (1 << i) in reached
                    for i in range(n)
                    if state & (1 << i)
                )
            }
        assert not reached
    assert (branches, max_live) == (7140, 4)

    # Exhaust all n=2 antecedent pairs for the conditional DEFECT-LIFT.  The
    # accompanying audit separately checks the general proof algebraically.
    subsets2 = list(range(4))
    lift_antecedents = 0
    for x_bits in range(1 << 4):
        x_family = {s for s in subsets2 if x_bits & (1 << s)}
        if not balanced_family_contracted(2, x_family):
            continue
        for d_bits in range(1 << 4):
            router = {s for s in subsets2 if d_bits & (1 << s)}
            if not one_sided_defect_router(2, router):
                continue
            lift_antecedents += 1
            lifted = defect_lift(2, x_family, router)
            assert len(lifted) == len(x_family) + len(router) + 2
            assert balanced_family_contracted(4, lifted)
    assert lift_antecedents > 0

    x2 = {0, 1, 3}
    assert balanced_family_contracted(2, x2) and one_sided_defect_router(2, x2)
    x4 = self_router_lift(2, x2)
    x6 = self_router_lift(4, x4)
    x8 = self_router_lift(6, x6)
    assert [len(x2), len(x4), len(x6), len(x8)] == [3, 8, 18, 38]
    assert balanced_family_contracted(4, x4) and one_sided_defect_router(4, x4)
    defect6 = []
    for count in (2, 4):
        total = 2 * count - 6
        for plus in plus_masks(6, count):
            if not literal_band_path(6, x6, plus, min(0, total), max(0, total)):
                defect6.append(plus)
    assert defect6 == [48, 15]
    balanced8_failures = [
        plus for plus in plus_masks(8, 4)
        if (1 << 8) - 1 not in contracted_reached(8, x8, plus)
    ]
    assert balanced8_failures == [15, 240]

    return {
        "tfo_n10_branches": branches,
        "tfo_max_live_leaves": max_live,
        "defect_lift_n2_antecedent_pairs": lift_antecedents,
        "self_router_defect_failures_n6": defect6,
        "continued_balanced_failures_n8": balanced8_failures,
    }


# ---------------------------------------------------------------------------
# CP-P hierarchy and its two lifts


# A leaf is (); an internal non-plane shape is a sorted pair of shapes.
Shape = tuple


def shape_text(shape: Shape) -> str:
    if not shape:
        return "*"
    return "(" + shape_text(shape[0]) + shape_text(shape[1]) + ")"


@lru_cache(None)
def tree_shapes(leaves: int) -> tuple[Shape, ...]:
    if leaves == 1:
        return ((),)
    found = {}
    for left_size in range(1, leaves):
        right_size = leaves - left_size
        if left_size > right_size:
            continue
        for left in tree_shapes(left_size):
            for right in tree_shapes(right_size):
                if left_size == right_size and shape_text(left) > shape_text(right):
                    continue
                candidate = (left, right)
                found[shape_text(candidate)] = candidate
    return tuple(found[key] for key in sorted(found))


def hierarchy(shape: Shape, first_label: int = 0) -> tuple[set[int], int, int]:
    if not shape:
        bit = 1 << first_label
        return {0, bit}, bit, first_label + 1
    left_family, left_ground, next_label = hierarchy(shape[0], first_label)
    right_family, right_ground, after = hierarchy(shape[1], next_label)
    family = (
        left_family | right_family |
        {left_ground | s for s in right_family} |
        {right_ground | s for s in left_family}
    )
    return family, left_ground | right_ground, after


def hierarchy_count(shape: Shape) -> int:
    if not shape:
        return 2
    return 2 * hierarchy_count(shape[0]) + 2 * hierarchy_count(shape[1]) - 4


def full_marker_lift(n: int, family: set[int]) -> set[int]:
    a, b = 1 << n, 1 << (n + 1)
    return {state | marker for state in family for marker in (0, a, b, a | b)}


def sparse_splice(n: int, family: set[int]) -> set[int]:
    old_full = (1 << n) - 1
    full = (1 << (n + 2)) - 1
    a, b = 1 << n, 1 << (n + 1)
    result = set(family)
    for marker in (a, b):
        for x, y in itertools.combinations(range(n), 2):
            result.add((old_full ^ (1 << x) ^ (1 << y)) | marker)
        for y in range(n):
            result.add((old_full ^ (1 << y)) | marker)
        result.add(old_full | marker)
    result.update(full ^ (1 << y) for y in range(n))
    result.add(full)
    return result


def check_cp_p() -> dict:
    expected_shapes = {2: 1, 4: 2, 6: 6, 8: 23, 10: 98, 12: 451}
    expected_valid_counts = {2: 1, 4: 1, 6: 2, 8: 3, 10: 6, 12: 11}
    expected_min_valid = {2: 4, 4: 16, 6: 48, 8: 160, 10: 448, 12: 1152}
    expected_min_any = {2: 4, 4: 12, 6: 28, 8: 44, 10: 76, 12: 108}
    table = {}
    for n in expected_shapes:
        shapes = tree_shapes(n)
        assert len(shapes) == expected_shapes[n]
        valid_sizes = []
        all_sizes = []
        for shape in shapes:
            family, ground, after = hierarchy(shape)
            assert after == n and ground == (1 << n) - 1
            assert len(family) == hierarchy_count(shape)
            assert {ground ^ state for state in family} == family
            all_sizes.append(len(family))
            if balanced_family_contracted(n, family):
                valid_sizes.append(len(family))
                assert dtp(n, family)[0]
        assert len(valid_sizes) == expected_valid_counts[n]
        assert min(valid_sizes) == expected_min_valid[n]
        assert min(all_sizes) == expected_min_any[n]
        table[n] = (len(shapes), len(valid_sizes), min(all_sizes), min(valid_sizes))

    # Independently instantiate the claimed layer-cover/no-path tree.
    leaf = ()
    gluing_shape = ((leaf, leaf), ((leaf, leaf), (leaf, leaf)))
    gluing, _, _ = hierarchy(gluing_shape)
    assert len(gluing) == 28
    counts = [sum(s.bit_count() == k for s in gluing) for k in range(7)]
    assert counts == [1, 6, 3, 8, 3, 6, 1]
    for plus in plus_masks(6, 3):
        for rank in range(7):
            assert any(
                s.bit_count() == rank and abs(discrepancy(s, plus)) <= 1
                for s in gluing
            )
    assert (1 << 6) - 1 not in contracted_reached(6, gluing, 7)

    # Root block rule: every mixed selected state exhausts one child.
    left_ground = 0b000011
    right_ground = 0b111100
    for state in gluing:
        if state & left_ground and state & right_ground:
            assert state & left_ground == left_ground or state & right_ground == right_ground

    # Full marker lift: check all balanced n=2 families, not merely one base.
    full_lift_cases = 0
    for bits in range(1 << 4):
        family = {s for s in range(4) if bits & (1 << s)}
        if balanced_family_contracted(2, family):
            full_lift_cases += 1
            lifted = full_marker_lift(2, family)
            assert len(lifted) == 4 * len(family)
            assert balanced_family_contracted(4, lifted)

    base = {0, 1, 3}
    s4 = sparse_splice(2, base)
    s6 = sparse_splice(4, s4)
    s8 = sparse_splice(6, s6)
    assert [len(s4), len(s6), len(s8)] == [14, 41, 92]
    assert balanced_family_contracted(4, s4) and dtp(4, s4)[0]
    assert balanced_family_contracted(6, s6)
    assert dtp(6, s6) == (False, 48)
    failures8 = [
        plus for plus in plus_masks(8, 4)
        if (1 << 8) - 1 not in contracted_reached(8, s8, plus)
    ]
    assert failures8[0] == 15 and 240 in failures8

    return {
        "shape_table": table,
        "n6_layer_profile": counts,
        "n6_countercolor": 7,
        "full_lift_balanced_base_cases_n2": full_lift_cases,
        "sparse_dtp_failure_n6": 48,
        "sparse_first_balanced_failure_n8": failures8[0],
    }


# ---------------------------------------------------------------------------
# CP-G adjacent interfaces, prefix defect, and skeleton accounting


def compatibility_columns(n: int) -> tuple[tuple[int, ...], list[int], int]:
    colors = plus_masks(n, n // 2)
    columns = []
    for state in range(1 << n):
        bits = 0
        for index, plus in enumerate(colors):
            if abs(discrepancy(state, plus)) <= 1:
                bits |= 1 << index
        columns.append(bits)
    return colors, columns, (1 << len(colors)) - 1


def accepted_color_bits(n: int, family: set[int], columns: list[int]) -> int:
    all_bits = columns[0]
    reached = {0: all_bits} if 0 in family else {}
    for rank in range(1, n + 1):
        nxt = {}
        for state in (s for s in family if s.bit_count() == rank):
            prior = 0
            for i in range(n):
                if state & (1 << i):
                    prior |= reached.get(state ^ (1 << i), 0)
            colors = prior & columns[state]
            if colors:
                nxt[state] = colors
        reached = nxt
    return reached.get((1 << n) - 1, 0)


def adjacent_predicate(n: int, family: set[int], columns: list[int], all_bits: int) -> bool:
    ranks = [tuple(s for s in family if s.bit_count() == k) for k in range(n + 1)]
    if any(not rank or __import__("functools").reduce(int.__or__, (columns[s] for s in rank), 0) != all_bits for rank in ranks):
        return False
    for k in range(1, n + 1):
        interface = 0
        for lower in ranks[k - 1]:
            for upper in ranks[k]:
                if lower & ~upper == 0:
                    interface |= columns[lower] & columns[upper]
        if interface != all_bits:
            return False
    return True


def adjacent_exhaustion(n: int) -> dict:
    colors, columns, all_bits = compatibility_columns(n)
    full = (1 << n) - 1
    interior = tuple(range(1, full))
    passing = 0
    bad = Counter()
    first = None
    missing = None
    for selector in range(1 << len(interior)):
        family = {0, full} | {
            state for index, state in enumerate(interior) if selector & (1 << index)
        }
        if not adjacent_predicate(n, family, columns, all_bits):
            continue
        passing += 1
        accepted = accepted_color_bits(n, family, columns)
        if accepted != all_bits:
            bad[len(family)] += 1
            candidate = sorted(family)
            if first is None or (len(candidate), candidate) < (len(first), first):
                first = candidate
                missing = [colors[i] for i in range(len(colors)) if not accepted & (1 << i)]
    return {"passing": passing, "bad": dict(sorted(bad.items())), "first": first, "missing": missing}


def minimum_prefix_n8() -> dict:
    n = 8
    colors, columns, all_bits = compatibility_columns(n)
    pairs = (3, 5, 9, 17)
    pair_reach = {p: columns[p] for p in pairs}
    triple_candidates = {}
    for triple in level(n, 3):
        prior = 0
        for pair, bits in pair_reach.items():
            if pair & ~triple == 0:
                prior |= bits
        bits = prior & columns[triple]
        if bits:
            triple_candidates[triple] = bits
    live = []
    triple_hist = Counter()
    for choice in itertools.combinations(sorted(triple_candidates), 2):
        covered = triple_candidates[choice[0]] | triple_candidates[choice[1]]
        triple_hist[covered.bit_count()] += 1
        if covered == all_bits:
            live.append(choice)
    terminal = Counter()
    branches = 0
    maximum = 0
    for triples in live:
        fours = {}
        for four in level(n, 4):
            prior = 0
            for triple in triples:
                if triple & ~four == 0:
                    prior |= triple_candidates[triple]
            bits = prior & columns[four]
            if bits:
                fours[four] = bits
        for choice in itertools.combinations(sorted(fours), 3):
            covered = fours[choice[0]] | fours[choice[1]] | fours[choice[2]]
            count = covered.bit_count()
            terminal[count] += 1
            maximum = max(maximum, count)
            branches += 1
    assert len(triple_candidates) == 18
    assert (sum(triple_hist.values()), len(live), branches, maximum) == (153, 3, 360, 64)
    return {"triple_hist": dict(sorted(triple_hist.items())), "terminal_hist": dict(sorted(terminal.items()))}


def check_cp_g() -> dict:
    adj2 = adjacent_exhaustion(2)
    adj4 = adjacent_exhaustion(4)
    assert adj2 == {"passing": 3, "bad": {}, "first": None, "missing": None}
    assert adj4["passing"] == 8874
    assert adj4["bad"] == {7: 24, 8: 180, 9: 264, 10: 88}
    assert adj4["first"] == [0, 1, 3, 5, 10, 11, 15]
    assert adj4["missing"] == [3, 12]

    prefix8 = minimum_prefix_n8()

    upper8 = {0, 1, 3, 5, 7, 15, 17, 23, 31, 63, 65, 81, 85, 95,
              113, 117, 119, 125, 127, 255}
    upper10_doc = json.loads(
        (ROOT / "certificates" / "balanced_chain_n10" / "upper_size35.json").read_text(encoding="utf-8")
    )
    upper10 = set(upper10_doc["family_masks"])
    profiles = {
        8: ([1, 1, 4, 2, 3, 2, 4, 1, 1], upper8),
        10: ([1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1], upper10),
    }
    skeleton_counts = {}
    for n, (tau, family) in profiles.items():
        colors, columns, all_bits = compatibility_columns(n)
        assert accepted_color_bits(n, family, columns) == all_bits
        rank_counts = [sum(s.bit_count() == k for s in family) for k in range(n + 1)]
        surplus_ranks = [k for k in range(n + 1) if rank_counts[k] > tau[k]]
        counts = {}
        for k in surplus_ranks:
            states = sorted(s for s in family if s.bit_count() == k)
            covers = 0
            for choice in itertools.combinations(states, tau[k]):
                covered = 0
                for state in choice:
                    covered |= columns[state]
                covers += covered == all_bits
            counts[k] = covers
        assert all(value == 0 for value in counts.values())
        skeleton_counts[n] = counts

    # Arithmetic instance of G4: r=4 gives overlapping bands for n=8 and
    # disjoint bands for n=10.  At n=10 exact size 35 means the two lower
    # bounds consume both surplus units, leaving none at rank five.
    assert set(range(0, 5)) & set(range(8 - 4, 9)) == {4}
    assert not (set(range(0, 5)) & set(range(10 - 4, 11)))

    return {
        "adjacent_n2": adj2,
        "adjacent_n4": adj4,
        "prefix8": prefix8,
        "embedded_minimum_cover_counts": skeleton_counts,
    }


def main() -> None:
    cp_s = check_cp_s()
    print("PASS independent CP-S terminal fanout and defect-lift checks", cp_s)
    cp_p = check_cp_p()
    print("PASS independent CP-P recurrence, block rule, shapes, and lifts", cp_p)
    cp_g = check_cp_g()
    print("PASS independent CP-G adjacent interface, prefix defect, and accounting", cp_g)
    print("ALL CYCLE-3 STRUCTURAL ADVERSARIAL CHECKS PASS (FINITE SCOPE)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent finite checks for the Cycle-3 CP-P hierarchy attack.

The program uses only the Python standard library.  It constructs every
unlabelled rooted non-plane full binary tree shape through 12 leaves, assigns
canonical DFS labels (all other labellings are ground-set permutations),
forms the exact recursively laminar frontier family from the accompanying
report, and checks actual Boolean-lattice path reachability for every signed
balanced colouring.

Nothing in this file estimates N(n), and no finite output is extrapolated.
"""

from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from itertools import combinations


# An unlabelled shape is None for a leaf and (left, right) for an internal
# node.  Children are canonicalized, so their order carries no information.
Shape = None | tuple["Shape", "Shape"]
LabelledTree = tuple


def shape_code(tree: Shape) -> str:
    if tree is None:
        return "*"
    return f"({shape_code(tree[0])},{shape_code(tree[1])})"


@lru_cache(maxsize=None)
def leaf_count(tree: Shape) -> int:
    if tree is None:
        return 1
    return leaf_count(tree[0]) + leaf_count(tree[1])


@lru_cache(maxsize=None)
def shapes(n: int) -> tuple[Shape, ...]:
    """All rooted non-plane full binary tree shapes with n leaves."""
    if n == 1:
        return (None,)
    answer: dict[str, Shape] = {}
    for left_size in range(1, n // 2 + 1):
        right_size = n - left_size
        for left in shapes(left_size):
            for right in shapes(right_size):
                if left_size == right_size and shape_code(left) > shape_code(right):
                    continue
                tree = (left, right)
                answer[shape_code(tree)] = tree
    return tuple(answer[key] for key in sorted(answer))


def label_dfs(tree: Shape, next_label: int = 0) -> tuple[LabelledTree, int]:
    if tree is None:
        return ("leaf", next_label), next_label + 1
    left, after_left = label_dfs(tree[0], next_label)
    right, after_right = label_dfs(tree[1], after_left)
    return (left, right), after_right


def hierarchy_family(tree: LabelledTree) -> tuple[set[int], int]:
    """Return the exact distinct-state family H(T) and its ground-set mask."""
    if tree[0] == "leaf":
        bit = 1 << tree[1]
        return {0, bit}, bit
    left_family, left_mask = hierarchy_family(tree[0])
    right_family, right_mask = hierarchy_family(tree[1])
    family = set(left_family)
    family.update(right_family)
    family.update(left_mask | state for state in right_family)
    family.update(right_mask | state for state in left_family)
    return family, left_mask | right_mask


def hierarchy_state_count(tree: Shape) -> int:
    if tree is None:
        return 2
    return 2 * hierarchy_state_count(tree[0]) + 2 * hierarchy_state_count(tree[1]) - 4


def by_level(family: set[int], n: int) -> list[tuple[int, ...]]:
    levels: list[list[int]] = [[] for _ in range(n + 1)]
    for state in family:
        levels[state.bit_count()].append(state)
    return [tuple(sorted(level)) for level in levels]


def compatible(state: int, plus_mask: int) -> bool:
    return abs(2 * (state & plus_mask).bit_count() - state.bit_count()) <= 1


def reachable_at_level(
    levels: list[tuple[int, ...]], n: int, plus_mask: int, last_level: int
) -> set[int]:
    reachable = {0}
    for rank in range(1, last_level + 1):
        next_reachable: set[int] = set()
        for state in levels[rank]:
            if not compatible(state, plus_mask):
                continue
            bits = state
            while bits:
                bit = bits & -bits
                if state ^ bit in reachable:
                    next_reachable.add(state)
                    break
                bits ^= bit
        reachable = next_reachable
        if not reachable:
            break
    return reachable


def first_balanced_path_failure(family: set[int], n: int) -> int | None:
    levels = by_level(family, n)
    full = (1 << n) - 1
    for plus_tuple in combinations(range(n), n // 2):
        plus_mask = sum(1 << vertex for vertex in plus_tuple)
        if full not in reachable_at_level(levels, n, plus_mask, n):
            return plus_mask
    return None


def first_layer_coverage_failure(family: set[int], n: int) -> tuple[int, int] | None:
    levels = by_level(family, n)
    for plus_tuple in combinations(range(n), n // 2):
        plus_mask = sum(1 << vertex for vertex in plus_tuple)
        for rank in range(n + 1):
            if not any(compatible(state, plus_mask) for state in levels[rank]):
                return plus_mask, rank
    return None


def first_two_defect_terminal_failure(family: set[int], n: int) -> int | None:
    """Check DTP: route crossing pairs to rank n-2, leaving majority pair."""
    levels = by_level(family, n)
    full = (1 << n) - 1
    for plus_count in (n // 2 - 1, n // 2 + 1):
        majority_plus = plus_count > n // 2
        for plus_tuple in combinations(range(n), plus_count):
            plus_mask = sum(1 << vertex for vertex in plus_tuple)
            reachable = reachable_at_level(levels, n, plus_mask, n - 2)
            succeeds = False
            for state in reachable:
                remainder = full ^ state
                if remainder.bit_count() != 2:
                    continue
                if all(
                    bool(plus_mask & (1 << vertex)) == majority_plus
                    for vertex in range(n)
                    if remainder & (1 << vertex)
                ):
                    succeeds = True
                    break
            if not succeeds:
                return plus_mask
    return None


def complete_balanced_shape(n: int) -> Shape:
    assert n >= 1 and n & (n - 1) == 0
    if n == 1:
        return None
    child = complete_balanced_shape(n // 2)
    return (child, child)


def two_leaf_product_lift(family: set[int], n: int) -> set[int]:
    a_bit = 1 << n
    b_bit = 1 << (n + 1)
    return {
        state | marker
        for state in family
        for marker in (0, a_bit, b_bit, a_bit | b_bit)
    }


def symmetric_sparse_tail_lift(family: set[int], n: int) -> set[int]:
    """The O(n^2)-overhead top-splice candidate from the report."""
    a, b = n, n + 1
    old_full = (1 << n) - 1
    new_full = (1 << (n + 2)) - 1
    lifted = set(family)

    for new_vertex in (a, b):
        new_bit = 1 << new_vertex
        for x, y in combinations(range(n), 2):
            lifted.add((old_full ^ (1 << x) ^ (1 << y)) | new_bit)
        for y in range(n):
            lifted.add((old_full ^ (1 << y)) | new_bit)
        lifted.add(old_full | new_bit)

    for y in range(n):
        lifted.add(new_full ^ (1 << y))
    lifted.add(new_full)
    return lifted


def mask_elements(mask: int, n: int) -> list[int]:
    return [vertex for vertex in range(n) if mask & (1 << vertex)]


def main() -> None:
    expected_shape_counts = {2: 1, 4: 2, 6: 6, 8: 23, 10: 98, 12: 451}
    expected_valid_sizes = {
        2: [4],
        4: [16],
        6: [48, 64],
        8: [160, 192, 256],
        10: [448, 576, 640, 768, 1024],
        12: [1152, 1408, 1664, 1792, 2176, 2304, 2560, 3072, 4096],
    }
    expected_valid_counts = {2: 1, 4: 1, 6: 2, 8: 3, 10: 6, 12: 11}
    expected_minimum_any = {2: 4, 4: 12, 6: 28, 8: 44, 10: 76, 12: 108}

    records: list[dict[str, object]] = []
    for n in expected_shape_counts:
        current_shapes = shapes(n)
        assert len(current_shapes) == expected_shape_counts[n]
        valid_sizes: list[int] = []
        all_sizes: list[int] = []
        valid_count = 0
        for shape in current_shapes:
            labelled, next_label = label_dfs(shape)
            assert next_label == n
            family, full = hierarchy_family(labelled)
            assert full == (1 << n) - 1
            assert len(family) == hierarchy_state_count(shape)
            assert {full ^ state for state in family} == family
            assert all((1 << vertex) in family for vertex in range(n))
            assert all((full ^ (1 << vertex)) in family for vertex in range(n))
            all_sizes.append(len(family))

            failure = first_balanced_path_failure(family, n)
            valid = failure is None
            if valid:
                valid_count += 1
                valid_sizes.append(len(family))
                # Every valid shape found in the exhaustive range also has
                # DTP.  This is finite evidence only, not a theorem.
                assert first_two_defect_terminal_failure(family, n) is None
            records.append(
                {
                    "n": n,
                    "shape": shape_code(shape),
                    "states": len(family),
                    "valid": valid,
                    "first_failure": failure,
                }
            )

        assert valid_count == expected_valid_counts[n]
        assert sorted(set(valid_sizes)) == expected_valid_sizes[n]
        assert min(all_sizes) == expected_minimum_any[n]
        print(
            f"PASS n={n}: {len(current_shapes)} unlabelled shapes, "
            f"{valid_count} valid, minimum any/valid states="
            f"{min(all_sizes)}/{min(valid_sizes)}"
        )

    # The polynomial-state complete balanced hierarchy is already killed at
    # n=4.  Its two selected pairs are monochromatic for plus set {0,1}.
    balanced4, _ = label_dfs(complete_balanced_shape(4))
    balanced4_family, _ = hierarchy_family(balanced4)
    assert len(balanced4_family) == 12
    assert first_layer_coverage_failure(balanced4_family, 4) == (0b0011, 2)
    assert first_balanced_path_failure(balanced4_family, 4) == 0b0011

    # A stronger n=6 obstruction: every level covers every colouring, but
    # plus set {0,1,2} has no source-to-sink path.
    leaf = lambda vertex: ("leaf", vertex)
    gluing_tree = (
        (leaf(0), leaf(1)),
        ((leaf(2), leaf(3)), (leaf(4), leaf(5))),
    )
    gluing_family, _ = hierarchy_family(gluing_tree)
    assert len(gluing_family) == 28
    assert [len(level) for level in by_level(gluing_family, 6)] == [1, 6, 3, 8, 3, 6, 1]
    assert first_layer_coverage_failure(gluing_family, 6) is None
    assert first_balanced_path_failure(gluing_family, 6) == 0b000111
    print("PASS n=6 gluing obstruction: all layers cover, plus={0,1,2} has no path")

    # Exact size formula and explicit failure for complete balanced trees.
    for n in (2, 4, 8, 16):
        shape = complete_balanced_shape(n)
        labelled, _ = label_dfs(shape)
        family, _ = hierarchy_family(labelled)
        assert len(family) == (2 * n * n + 4) // 3
        if n >= 4:
            plus_mask = (1 << (n // 2)) - 1
            assert not any(
                compatible(state, plus_mask)
                for state in by_level(family, n)[2]
            )
    print("PASS complete balanced hierarchy: exact quadratic count and explicit cut failure")

    # Full insertion closure preserves validity in the finite base check and
    # exactly quadruples distinct states, agreeing with the general proof.
    base = {0, 0b01, 0b11}
    assert first_balanced_path_failure(base, 2) is None
    product4 = two_leaf_product_lift(base, 2)
    assert len(product4) == 4 * len(base)
    assert first_balanced_path_failure(product4, 4) is None

    # The stronger symmetric sparse splice preserves both properties once,
    # then loses DTP at n=6.  One further unsupported iteration fails at n=8.
    sparse4 = symmetric_sparse_tail_lift(base, 2)
    assert len(sparse4) == 14
    assert first_balanced_path_failure(sparse4, 4) is None
    assert first_two_defect_terminal_failure(sparse4, 4) is None
    sparse6 = symmetric_sparse_tail_lift(sparse4, 4)
    assert len(sparse6) == 41
    assert first_balanced_path_failure(sparse6, 6) is None
    assert first_two_defect_terminal_failure(sparse6, 6) == 0b110000
    sparse8 = symmetric_sparse_tail_lift(sparse6, 6)
    assert len(sparse8) == 92
    assert first_balanced_path_failure(sparse8, 8) == 0b00001111
    print(
        "PASS recursion falsification: sparse splice loses DTP at n=6 "
        "and fails balanced coverage at n=8"
    )

    payload = json.dumps(records, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(payload).hexdigest()
    print(f"shape-record sha256={digest}")
    print("ALL CP-P HIERARCHY CHECKS PASS")


if __name__ == "__main__":
    main()

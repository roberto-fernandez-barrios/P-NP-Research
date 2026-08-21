#!/usr/bin/env python3
"""Deterministic independent verifier for Cycle-4 multi-RR certificates.

The search implementation is C++.  This verifier is standalone Python and
reconstructs all mathematical objects from the literal definitions:

* fixed-weight binary necklaces and all rejected RR_n rotation orbits;
* relabelled literal subset families and their distinct-union size;
* the exact intersection of the individual-copy rejection sets; and
* every inclusion-by-one edge in the full induced subset DAG on that
  intersection.

The last reduction is exact, not heuristic: any coloring outside the
intersection has a witness wholly inside one of the copies.  Hybrid paths
are still searched for every coloring in the intersection.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from pathlib import Path
from typing import Callable, Iterable, Iterator, Sequence


Mask = int


def rotate_down(value: Mask, amount: int, width: int) -> Mask:
    amount %= width
    mask = (1 << width) - 1
    if amount == 0:
        return value & mask
    return ((value >> amount) | (value << (width - amount))) & mask


def rr_accepts_fast(word: Mask, q: int) -> bool:
    """Bit-parallel forward interval-growth recurrence."""
    reachable = word
    adjacent_difference = word ^ rotate_down(word, 1, q)
    for length in range(1, q, 2):
        left_left = rotate_down(reachable, 2, q) & adjacent_difference
        split = rotate_down(reachable, 1, q) & (
            word ^ rotate_down(word, length + 1, q)
        )
        right_right = reachable & rotate_down(adjacent_difference, length, q)
        reachable = left_left | split | right_right
        if not reachable:
            return False
    return bool(reachable)


def rr_accepts_scalar(word: Mask, q: int) -> bool:
    """Separately written set-of-starts form, used for semantic cross-checks."""
    current = {position for position in range(q) if word & (1 << position)}
    for length in range(1, q, 2):
        following: set[int] = set()
        for start in current:
            triples = (
                ((start - 2) % q, (start - 2) % q, (start - 1) % q),
                ((start - 1) % q, (start - 1) % q, (start + length) % q),
                (start, (start + length) % q, (start + length + 1) % q),
            )
            for new_start, a, b in triples:
                if bool(word & (1 << a)) != bool(word & (1 << b)):
                    following.add(new_start)
        current = following
        if not current:
            return False
    return bool(current)


def fixed_weight_necklaces(q: int, weight: int) -> Iterator[Mask]:
    """FKM recursion: exactly one least-rotation representative per orbit."""
    digits = bytearray(q + 1)

    def generate(position: int, period: int, ones: int, word: Mask) -> Iterator[Mask]:
        remaining = q - position + 1
        if ones > weight or ones + remaining < weight:
            return
        if position > q:
            if ones == weight and q % period == 0:
                yield word
            return

        copied = digits[position - period]
        digits[position] = copied
        yield from generate(
            position + 1,
            period,
            ones + copied,
            word | (copied << (position - 1)),
        )
        if copied == 0:
            digits[position] = 1
            yield from generate(
                position + 1,
                position,
                ones + 1,
                word | (1 << (position - 1)),
            )

    yield from generate(1, 1, 0, 0)


def enumerate_failure_orbits(n: int) -> tuple[int, list[Mask]]:
    q = n - 1
    weight = n // 2
    if math.gcd(q, weight) != 1:
        raise AssertionError("the fixed-weight rotation orbits must be full")
    total = 0
    failures: list[Mask] = []
    for word in fixed_weight_necklaces(q, weight):
        total += 1
        if not rr_accepts_fast(word, q):
            failures.append(word)
    expected = math.comb(q, weight) // q
    if total != expected:
        raise AssertionError(("necklace count", total, expected))
    return total, failures


def expand_rotations(representatives: Iterable[Mask], q: int) -> list[Mask]:
    expanded = sorted(
        {rotate_down(representative, shift, q)
         for representative in representatives
         for shift in range(q)}
    )
    return expanded


def fnv1a64_little_endian_masks(masks: Iterable[Mask]) -> str:
    value = 1469598103934665603
    for mask in masks:
        for byte in mask.to_bytes(8, "little"):
            value ^= byte
            value = (value * 1099511628211) & ((1 << 64) - 1)
    return f"{value:016x}"


def parse_stored_representatives(path: Path) -> list[Mask]:
    lines = path.read_text(encoding="ascii").splitlines()
    if not lines or not lines[0].startswith("# q="):
        raise AssertionError(f"bad representative header: {path}")
    return [int(line, 16) for line in lines[1:] if line]


def validate_permutation(permutation: Sequence[int], n: int) -> tuple[int, ...]:
    if sorted(permutation) != list(range(n)):
        raise AssertionError("not a permutation")
    return tuple(permutation)


def inverse_permutation(permutation: Sequence[int]) -> tuple[int, ...]:
    inverse = [0] * len(permutation)
    for old, new in enumerate(permutation):
        inverse[new] = old
    return tuple(inverse)


def permute_mask(mask: Mask, permutation: Sequence[int]) -> Mask:
    result = 0
    while mask:
        low = mask & -mask
        old = low.bit_length() - 1
        result |= 1 << permutation[old]
        mask ^= low
    return result


def sign_normalize(plus: Mask, n: int) -> Mask:
    if plus & (1 << (n - 1)):
        plus ^= (1 << n) - 1
    return plus


def interval_mask(q: int, start: int, length: int) -> Mask:
    return sum(1 << ((start + offset) % q) for offset in range(length))


def base_rr_ranks(n: int) -> tuple[tuple[Mask, ...], ...]:
    q = n - 1
    rows: list[tuple[Mask, ...]] = [(0,)]
    rows.append(tuple(1 << point for point in range(q)))
    infinity = 1 << q
    for rank in range(2, n):
        rows.append(
            tuple(infinity | interval_mask(q, start, rank - 1) for start in range(q))
        )
    rows.append(((1 << n) - 1,))
    return tuple(rows)


def literal_union_ranks(
    n: int, permutations: Sequence[Sequence[int]]
) -> tuple[tuple[Mask, ...], ...]:
    base = base_rr_ranks(n)
    return tuple(
        tuple(sorted({permute_mask(state, permutation)
                      for permutation in permutations
                      for state in base[rank]}))
        for rank in range(n + 1)
    )


def induced_parents(
    ranks: Sequence[Sequence[Mask]],
) -> tuple[tuple[tuple[int, ...], ...], ...]:
    all_parents: list[tuple[tuple[int, ...], ...]] = [tuple()]
    for rank in range(1, len(ranks)):
        prior_index = {state: index for index, state in enumerate(ranks[rank - 1])}
        row: list[tuple[int, ...]] = []
        for state in ranks[rank]:
            parents: list[int] = []
            bits = state
            while bits:
                low = bits & -bits
                parent = state ^ low
                if parent in prior_index:
                    parents.append(prior_index[parent])
                bits ^= low
            row.append(tuple(parents))
        all_parents.append(tuple(row))
    return tuple(all_parents)


def literal_dag_accepts(
    ranks: Sequence[Sequence[Mask]],
    parents: Sequence[Sequence[Sequence[int]]],
    plus: Mask,
) -> bool:
    previous = [True]
    for rank in range(1, len(ranks)):
        current = [False] * len(ranks[rank])
        for index, state in enumerate(ranks[rank]):
            if abs(2 * (state & plus).bit_count() - rank) > 1:
                continue
            current[index] = any(previous[parent] for parent in parents[rank][index])
        if not any(current):
            return False
        previous = current
    return previous == [True]


def normalized_masks(n: int) -> Iterator[Mask]:
    for chosen in combinations(range(n - 1), n // 2):
        yield sum(1 << point for point in chosen)


def small_semantic_audit() -> None:
    """Cross-check recurrence against a direct literal-DAG search through n=12."""
    for n in range(2, 14, 2):
        q = n - 1
        ranks = base_rr_ranks(n)
        parents = induced_parents(ranks)
        for plus in normalized_masks(n):
            fast = rr_accepts_fast(plus, q)
            scalar = rr_accepts_scalar(plus, q)
            literal = literal_dag_accepts(ranks, parents, plus)
            if not (fast == scalar == literal):
                raise AssertionError(("RR semantic mismatch", n, plus, fast, scalar, literal))


def verify_certificate(
    path: Path, *, direct_full_dag_all_colors: bool = False
) -> dict[str, int | str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data["schema"] != "cycle04-multi-rr-v1":
        raise AssertionError("unexpected schema")
    n = int(data["n"])
    q = n - 1
    if data["q"] != q or n % 2 or n < 2:
        raise AssertionError("bad n/q")

    necklace_count, computed_representatives = enumerate_failure_orbits(n)
    stored_path = path.parent / data["failure_necklace_file"]
    stored_representatives = parse_stored_representatives(stored_path)
    if computed_representatives != stored_representatives:
        raise AssertionError("failure-necklace list differs from fresh exhaustion")
    if necklace_count != data["fixed_weight_necklaces"]:
        raise AssertionError("necklace total differs")
    if len(computed_representatives) != data["one_copy_failing_necklaces"]:
        raise AssertionError("failing-necklace total differs")

    failures = expand_rotations(computed_representatives, q)
    failure_set = set(failures)
    if len(failures) != len(computed_representatives) * q:
        raise AssertionError("a fixed-weight orbit was unexpectedly short")
    if len(failures) != data["one_copy_normalized_rejections"]:
        raise AssertionError("one-copy failure total differs")
    if fnv1a64_little_endian_masks(failures) != data["one_copy_failure_masks_fnv1a64_le"]:
        raise AssertionError("one-copy failure hash differs")
    if math.comb(q, n // 2) != data["normalized_balanced_colorings"]:
        raise AssertionError("balanced-color total differs")

    permutations = [
        validate_permutation(row, n) for row in data["permutations_old_to_new"]
    ]
    if len(permutations) != data["copy_count"]:
        raise AssertionError("copy count differs")
    if permutations[0] != tuple(range(n)):
        raise AssertionError("the certificate normalization requires identity first")
    inverses = [inverse_permutation(p) for p in permutations]

    common: list[Mask] = []
    for plus in failures:
        if all(
            sign_normalize(permute_mask(plus, inverse), n) in failure_set
            for inverse in inverses[1:]
        ):
            common.append(plus)
    if len(common) != data["common_individual_rejections"]:
        raise AssertionError("common individual rejection total differs")

    ranks = literal_union_ranks(n, permutations)
    profile = [len(row) for row in ranks]
    if profile != data["literal_rank_profile"]:
        raise AssertionError("literal rank profile differs")
    if sum(profile) != data["literal_distinct_subset_count"]:
        raise AssertionError("literal distinct-subset count differs")
    parents = induced_parents(ranks)
    union_rejections = sum(
        not literal_dag_accepts(ranks, parents, plus) for plus in common
    )
    hybrid_acceptances = len(common) - union_rejections
    if union_rejections != data["full_literal_union_rejections"]:
        raise AssertionError("full literal-union rejection total differs")
    if hybrid_acceptances != data["hybrid_only_acceptances"]:
        raise AssertionError("hybrid-only acceptance total differs")

    if data["minimum_t_exact"] == 2:
        if not failures or len(permutations) != 2 or union_rejections:
            raise AssertionError("minimum-t=2 claim lacks lower or upper certificate")

    direct_rejections = -1
    if direct_full_dag_all_colors:
        direct_rejections = sum(
            not literal_dag_accepts(ranks, parents, plus)
            for plus in normalized_masks(n)
        )
        if direct_rejections:
            raise AssertionError("direct all-color full-DAG check found a rejection")

    return {
        "n": n,
        "minimum_t_exact": data["minimum_t_exact"],
        "one_copy_rejections": len(failures),
        "common_individual_rejections": len(common),
        "hybrid_only_acceptances": hybrid_acceptances,
        "union_rejections": union_rejections,
        "literal_subsets": sum(profile),
        "direct_all_color_full_dag_rejections": direct_rejections,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "certificates",
        nargs="*",
        type=Path,
        help="certificate JSON files (default: all cycle04_multi_rr_n*.json)",
    )
    parser.add_argument(
        "--skip-small-semantic-audit",
        action="store_true",
        help="skip the direct recurrence-versus-literal check through n=12",
    )
    parser.add_argument(
        "--direct-full-dag-n22",
        action="store_true",
        help=(
            "also traverse the full two-copy induced DAG on all 352716 "
            "normalized n=22 colors, without the exact intersection shortcut"
        ),
    )
    args = parser.parse_args()

    if not args.skip_small_semantic_audit:
        small_semantic_audit()
        print("PASS independent RR recurrence/literal-DAG equivalence through n=12")

    paths = args.certificates
    if not paths:
        root = Path(__file__).resolve().parents[1]
        paths = sorted(
            (root / "certificates" / "cycle04_multi_rr").glob(
                "cycle04_multi_rr_n*.json"
            )
        )
    if not paths:
        raise SystemExit("no certificates found")

    for path in paths:
        direct = args.direct_full_dag_n22 and json.loads(
            path.read_text(encoding="utf-8")
        )["n"] == 22
        summary = verify_certificate(path, direct_full_dag_all_colors=direct)
        print("PASS", json.dumps(summary, sort_keys=True))
    print("ALL CYCLE-4 MULTI-RR CERTIFICATES PASS")


if __name__ == "__main__":
    main()

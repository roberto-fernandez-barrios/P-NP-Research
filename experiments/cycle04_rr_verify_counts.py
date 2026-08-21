#!/usr/bin/env python3
"""Independent checker for Cycle-4 RR necklace-count certificates.

The C++ producer uses q-bit formulas.  This checker reconstructs reachable
interval starts as Python sets, reconstructs the literal RR subset DAG at
small n, and can independently recount fixed-weight necklaces through a
requested even n.  It imports no code from the producer.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb, gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CERTIFICATE_DIR = ROOT / "certificates" / "cycle04_rr_acceptance"


def bit(word: int, position: int) -> int:
    return (word >> position) & 1


def interval_levels(word: int, q: int) -> dict[int, frozenset[int]]:
    """Exact forward recurrence, written independently with explicit sets."""
    current = {i for i in range(q) if bit(word, i)}
    levels = {1: frozenset(current)}
    for length in range(1, q, 2):
        following: set[int] = set()
        for start in current:
            if bit(word, (start - 2) % q) != bit(word, (start - 1) % q):
                following.add((start - 2) % q)
            if bit(word, (start - 1) % q) != bit(word, (start + length) % q):
                following.add((start - 1) % q)
            if bit(word, (start + length) % q) != bit(word, (start + length + 1) % q):
                following.add(start)
        current = following
        levels[length + 2] = frozenset(current)
    return levels


def interval_accepts(word: int, q: int) -> bool:
    return bool(interval_levels(word, q)[q])


def word_text(word: int, q: int) -> str:
    return "".join("1" if bit(word, i) else "0" for i in range(q))


def text_word(text: str) -> int:
    return sum((symbol == "1") << i for i, symbol in enumerate(text))


def rotations(text: str):
    for amount in range(len(text)):
        yield text[amount:] + text[:amount]


def least_rotation(text: str) -> str:
    return min(rotations(text))


def cyclic_run_data(text: str) -> tuple[int, int, int]:
    q = len(text)
    boundary = next(i for i in range(q) if text[i] != text[i - 1])
    ordered = text[boundary:] + text[:boundary]
    runs: list[tuple[str, int]] = []
    symbol = ordered[0]
    length = 0
    for value in ordered:
        if value == symbol:
            length += 1
        else:
            runs.append((symbol, length))
            symbol = value
            length = 1
    runs.append((symbol, length))
    return (
        len(runs),
        max(length for symbol, length in runs if symbol == "0"),
        max(length for symbol, length in runs if symbol == "1"),
    )


def necklaces_fixed_weight(q: int, weight: int):
    """A separate Python implementation of fixed-density FKM generation."""
    digits = [0] * (q + 1)

    def visit(position: int, period: int, ones: int, word: int):
        remaining = q - position + 1
        if ones > weight or ones + remaining < weight:
            return
        if position > q:
            if ones == weight and q % period == 0:
                yield word, period
            return
        copied = digits[position - period]
        digits[position] = copied
        yield from visit(
            position + 1,
            period,
            ones + copied,
            word | (copied << (position - 1)),
        )
        if copied == 0:
            digits[position] = 1
            yield from visit(
                position + 1,
                position,
                ones + 1,
                word | (1 << (position - 1)),
            )

    yield from visit(1, 1, 0, 0)


def rr_family(n: int) -> set[int]:
    q = n - 1
    infinity = 1 << q
    full = (1 << n) - 1
    family = {0, full}
    family.update(1 << point for point in range(q))
    for length in range(1, q):
        for start in range(q):
            interval = sum(1 << ((start + offset) % q) for offset in range(length))
            family.add(infinity | interval)
    return family


def rr_seed_prefix_family(n: int) -> set[int]:
    """Literal prefix union of the n-1 corrected round-robin seed orders."""
    q = n - 1
    m = n // 2
    result = {0}
    for center in range(q):
        order = [center, q]
        for offset in range(1, m):
            order.extend(((center + offset) % q, (center - offset) % q))
        assert len(order) == n and len(set(order)) == n
        state = 0
        for point in order:
            state |= 1 << point
            result.add(state)
    return result


def compatible(state: int, plus: int) -> bool:
    return abs(2 * (state & plus).bit_count() - state.bit_count()) <= 1


def literal_accepts(n: int, plus: int) -> bool:
    family = rr_family(n)
    reached = {0}
    for rank in range(1, n + 1):
        following = set()
        for state in family:
            if state.bit_count() != rank or not compatible(state, plus):
                continue
            if any((state ^ (1 << point)) in reached for point in range(n) if bit(state, point)):
                following.add(state)
        reached = following
    return ((1 << n) - 1) in reached


def check_literal_equivalence() -> None:
    for n in range(2, 36, 2):
        literal = rr_seed_prefix_family(n)
        intervals = rr_family(n)
        assert literal == intervals
        assert len(literal) == (n - 1) ** 2 + 2
    for n in range(2, 14, 2):
        q = n - 1
        for choice in combinations(range(q), n // 2):
            word = sum(1 << i for i in choice)
            assert literal_accepts(n, word) == interval_accepts(word, q)


def read_certificate(path: Path) -> tuple[dict, list[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    failure_path = ROOT / data["failure_representatives_file"]
    texts = failure_path.read_text(encoding="ascii").splitlines()
    return data, texts


def check_certificate(path: Path) -> None:
    data, texts = read_certificate(path)
    assert data["schema"] == "cycle04-rr-acceptance-v1"
    n = data["n"]
    q = n - 1
    weight = n // 2
    assert data["q"] == q and data["normalized_finite_weight"] == weight
    assert gcd(q, weight) == 1
    total = comb(q, weight)
    assert data["normalized_balanced_words"] == total
    assert data["rotation_orbit_size"] == q
    assert data["rotation_orbits_total"] * q == total
    assert data["rejected_rotation_orbits"] == len(texts)
    assert data["rejected_normalized_words"] == len(texts) * q
    assert data["accepted_normalized_words"] + data["rejected_normalized_words"] == total
    assert texts == sorted(texts)
    assert len(texts) == len(set(texts))

    run_counts: Counter[int] = Counter()
    max_counts: Counter[int] = Counter()
    max_zero_counts: Counter[int] = Counter()
    max_one_counts: Counter[int] = Counter()
    joint_counts: Counter[str] = Counter()
    reflected = 0
    xor = 0
    sum_mod = 0
    for text in texts:
        assert len(text) == q and set(text) <= {"0", "1"} and text.count("1") == weight
        assert least_rotation(text) == text
        word = text_word(text)
        assert not interval_accepts(word, q)
        if least_rotation(text[::-1]) == text:
            reflected += 1
        runs, max_zero, max_one = cyclic_run_data(text)
        run_counts[runs] += 1
        max_counts[max(max_zero, max_one)] += 1
        max_zero_counts[max_zero] += 1
        max_one_counts[max_one] += 1
        joint_counts[f"{runs}|{max_zero}|{max_one}"] += 1
        xor ^= word
        sum_mod = (sum_mod + word) & ((1 << 64) - 1)

    def integer_keyed(field: str) -> Counter[int]:
        return Counter({int(key): value for key, value in data[field].items()})

    assert run_counts == integer_keyed("cyclic_run_count_rejected_rotation_orbits")
    assert max_counts == integer_keyed("maximum_cyclic_run_rejected_rotation_orbits")
    assert max_zero_counts == integer_keyed("maximum_zero_run_rejected_rotation_orbits")
    assert max_one_counts == integer_keyed("maximum_one_run_rejected_rotation_orbits")
    assert joint_counts == Counter(data["joint_run_profile_rejected_rotation_orbits"])
    assert reflected == data["reflection_symmetric_rejected_rotation_orbits"]
    assert data["rejected_dihedral_orbits"] == reflected + (len(texts) - reflected) // 2
    assert (len(texts) - reflected) % 2 == 0
    assert xor == data["failure_representative_xor_uint64"]
    assert sum_mod == data["failure_representative_sum_mod_2_64"]
    if n == 22:
        expanded = sorted({rotation for text in texts for rotation in rotations(text)})
        digest = hashlib.sha256(("\n".join(expanded) + "\n").encode("ascii")).hexdigest()
        assert digest == "ea61fa625c178336031605dcb22349e167b8e9ed3b42698b8ea383b507e44581"


def independent_recount(certificate_dir: Path, through_n: int) -> None:
    for n in range(22, through_n + 1, 2):
        path = certificate_dir / f"cycle04_rr_acceptance_n{n}.json"
        expected, expected_texts = read_certificate(path)
        q = n - 1
        weight = n // 2
        seen = 0
        failures: list[str] = []
        for word, period in necklaces_fixed_weight(q, weight):
            assert period == q
            seen += 1
            if not interval_accepts(word, q):
                failures.append(word_text(word, q))
        assert seen == comb(q, weight) // q
        assert failures == expected_texts
        assert len(failures) == expected["rejected_rotation_orbits"]
        print(f"PASS independent exact recount n={n}: {seen} necklaces, {len(failures)} rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--certificate-dir", type=Path, default=DEFAULT_CERTIFICATE_DIR)
    parser.add_argument("--recount-through", type=int, default=0)
    parser.add_argument("--skip-literal-equivalence", action="store_true")
    args = parser.parse_args()

    if not args.skip_literal_equivalence:
        check_literal_equivalence()
        print("PASS literal induced-DAG/interval recurrence equivalence through n=12")

    paths = sorted(args.certificate_dir.glob("cycle04_rr_acceptance_n*.json"))
    assert paths, "no Cycle-4 RR certificates found"
    for path in paths:
        check_certificate(path)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f"PASS {path.name} and failure list (JSON sha256 {digest})")
    if args.recount_through:
        assert args.recount_through >= 22 and args.recount_through % 2 == 0
        independent_recount(args.certificate_dir, args.recount_through)
    print("ALL REQUESTED CYCLE-4 RR CERTIFICATE CHECKS PASS")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent adversarial checker for the corrected Cycle-3 CP-M report.

The proposer uses a memoized recursive deletion predicate.  This checker
instead propagates reachable cyclic intervals forward as sets of starting
positions and separately searches the literal induced subset DAG.  It does
not import the proposer module or trust its seed matching menu.
"""

from __future__ import annotations

import hashlib
import itertools
from collections import Counter
from math import comb


def weight_masks(n: int, weight: int):
    for choice in itertools.combinations(range(n), weight):
        yield sum(1 << i for i in choice)


def rr_order(n: int, center: int) -> tuple[int, ...]:
    q = n - 1
    m = n // 2
    result = [center, q]
    for offset in range(1, m):
        result.extend(((center + offset) % q, (center - offset) % q))
    assert len(result) == n and len(set(result)) == n
    return tuple(result)


def rr_factor(n: int, center: int) -> tuple[tuple[int, int], ...]:
    order = rr_order(n, center)
    return tuple((order[i], order[i + 1]) for i in range(0, n, 2))


def prefixes(order: tuple[int, ...]) -> tuple[int, ...]:
    state = 0
    result = [0]
    for point in order:
        state |= 1 << point
        result.append(state)
    return tuple(result)


def rr_family(n: int) -> set[int]:
    return {
        state
        for center in range(n - 1)
        for state in prefixes(rr_order(n, center))
    }


def interval_mask(q: int, start: int, length: int) -> int:
    return sum(1 << ((start + offset) % q) for offset in range(length))


def check_factorization_and_exact_family() -> dict:
    summaries = {}
    for n in range(2, 24, 2):
        q = n - 1
        edges = Counter(
            tuple(sorted(edge))
            for center in range(q)
            for edge in rr_factor(n, center)
        )
        assert len(edges) == comb(n, 2) and set(edges.values()) == {1}

        family = rr_family(n)
        expected = {0, (1 << n) - 1}
        expected.update(1 << point for point in range(q))
        infinity = 1 << q
        for rank in range(2, n):
            expected.update(
                infinity | interval_mask(q, start, rank - 1)
                for start in range(q)
            )
        assert family == expected
        profile = Counter(state.bit_count() for state in family)
        assert profile[0] == profile[n] == 1
        assert all(profile[rank] == q for rank in range(1, n))
        assert len(family) == q * q + 2
        summaries[n] = len(family)
    return summaries


def compatible(state: int, plus: int) -> bool:
    return abs(2 * (state & plus).bit_count() - state.bit_count()) <= 1


def literal_path(n: int, family: set[int], plus: int) -> tuple[int, ...] | None:
    """Search all inclusion edges; no restriction to generating seed paths."""
    full = (1 << n) - 1
    parents: dict[int, tuple[int, int] | None] = {0: None}
    for rank in range(1, n + 1):
        for state in sorted(s for s in family if s.bit_count() == rank):
            if not compatible(state, plus):
                continue
            for point in range(n):
                prior = state ^ (1 << point)
                if state & (1 << point) and prior in parents:
                    parents[state] = (prior, point)
                    break
    if full not in parents:
        return None
    order = []
    state = full
    while state:
        prior, point = parents[state]  # type: ignore[misc]
        order.append(point)
        state = prior
    return tuple(reversed(order))


def bit(word: int, position: int) -> int:
    return (word >> position) & 1


def forward_interval_levels(q: int, word: int) -> dict[int, frozenset[int]]:
    """Reachable odd-length finite intervals after crossing-pair extensions."""
    current = {i for i in range(q) if bit(word, i)}
    levels = {1: frozenset(current)}
    for length in range(1, q, 2):
        following = set()
        for start in current:
            left2 = (start - 2) % q
            left1 = (start - 1) % q
            right0 = (start + length) % q
            right1 = (start + length + 1) % q
            if bit(word, left2) != bit(word, left1):
                following.add(left2)
            if bit(word, left1) != bit(word, right0):
                following.add(left1)
            if bit(word, right0) != bit(word, right1):
                following.add(start)
        current = following
        levels[length + 2] = frozenset(current)
    return levels


def interval_accepts(q: int, word: int) -> bool:
    return bool(forward_interval_levels(q, word)[q])


def check_deque_literal_equivalence() -> dict:
    checked = {}
    for n in range(2, 14, 2):
        q = n - 1
        family = rr_family(n)
        count = 0
        # Fix infinity minus.  The finite word has m pluses and m-1 minuses.
        for finite_plus in weight_masks(q, n // 2):
            by_intervals = interval_accepts(q, finite_plus)
            by_literal_dag = literal_path(n, family, finite_plus) is not None
            assert by_intervals == by_literal_dag
            count += 1
        checked[n] = count
    return checked


def pair_crosses(pair: tuple[int, int], plus: int) -> bool:
    return bool(plus & (1 << pair[0])) != bool(plus & (1 << pair[1]))


def check_hybrid_n10() -> dict:
    n = 10
    plus = sum(1 << i for i in (0, 1, 2, 3, 6))
    crossing_counts = [
        sum(pair_crosses(edge, plus) for edge in rr_factor(n, center))
        for center in range(n - 1)
    ]
    assert crossing_counts == [3, 3, 3, 3, 3, 3, 1, 3, 3]
    assert max(crossing_counts) < n // 2

    hybrid = (3, 9, 4, 2, 5, 6, 7, 1, 8, 0)
    family = rr_family(n)
    assert all(state in family for state in prefixes(hybrid))
    assert all(pair_crosses((hybrid[i], hybrid[i + 1]), plus) for i in range(0, n, 2))
    assert literal_path(n, family, plus) is not None
    return {"seed_crossing_counts": crossing_counts, "hybrid_order": hybrid}


def rotate_mask(q: int, mask: int, amount: int) -> int:
    result = 0
    for position in range(q):
        if bit(mask, position):
            result |= 1 << ((position - amount) % q)
    return result


def mask_word(q: int, mask: int) -> str:
    return "".join("1" if bit(mask, i) else "0" for i in range(q))


def check_first_failure() -> dict:
    totals = {}
    for q in range(1, 22, 2):
        bad = []
        for word in weight_masks(q, (q + 1) // 2):
            if not interval_accepts(q, word):
                bad.append(word)
        totals[q + 1] = len(bad)
        if q < 21:
            assert not bad
        else:
            base_string = "111111110000011100000"
            base = sum(1 << i for i, symbol in enumerate(base_string) if symbol == "1")
            rotations = {rotate_mask(q, base, amount) for amount in range(q)}
            assert len(bad) == len(rotations) == 21 and set(bad) == rotations
            digest = hashlib.sha256(
                ("\n".join(sorted(mask_word(q, word) for word in bad)) + "\n").encode()
            ).hexdigest()
            assert digest == "ea61fa625c178336031605dcb22349e167b8e9ed3b42698b8ea383b507e44581"

            expected = {
                1: {0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 15},
                3: {6, 12, 14, 20},
                5: {5, 11, 12, 13, 19},
                7: {4, 18},
                9: {3, 17},
                11: {2, 3, 15, 16},
                13: set(),
            }
            levels = forward_interval_levels(q, base)
            assert {length: set(levels[length]) for length in expected} == expected
    return totals


def four_run_word(m: int) -> tuple[int, int]:
    symbols = "1" * (m - 3) + "0" * 5 + "1" * 3 + "0" * (m - 6)
    q = 2 * m - 1
    assert len(symbols) == q and symbols.count("1") == m
    return q, sum(1 << i for i, symbol in enumerate(symbols) if symbol == "1")


def check_four_run_closed_forms() -> dict:
    # Broad finite corroboration of the symbolic transition proof in the
    # audit report.  The report, rather than this finite loop, establishes all
    # m by separating m=11, m=12, and the stable m>=13 induction.
    for m in range(11, 301):
        q, word = four_run_word(m)
        levels = {length: set(starts) for length, starts in forward_interval_levels(q, word).items()}
        assert levels[3] == {m - 5, m + 1, m + 3, 2 * m - 2}
        assert levels[5] == {m - 6, m, m + 1, m + 2, 2 * m - 3}
        assert levels[7] == {m - 7, 2 * m - 4}
        assert levels[9] == {m - 8, 2 * m - 5}
        if m == 11:
            assert levels[11] == {m - 9, m - 8, m + 4, m + 5}
        else:
            assert levels[11] == {m - 9, m - 8, 2 * m - 6}
            for t in range(6, m - 6):
                assert levels[2 * t + 1] == {2 * m - t - 1}
            assert levels[2 * m - 11] == {m + 4, m + 5}
        assert levels[2 * m - 9] == set()
        assert not interval_accepts(q, word)
    return {"first_m": 11, "last_finitely_checked_m": 300}


def compatibility_signature(n: int, support: int) -> tuple[bool, ...]:
    return tuple(
        (plus & support).bit_count() * 2 == support.bit_count()
        for plus in weight_masks(n, n // 2)
    )


def check_unsafe_quotients() -> dict:
    # Color-signature merging at n=4 splices two live complementary supports.
    n = 4
    full = (1 << n) - 1
    support = 0b0011
    complement = full ^ support
    assert compatibility_signature(n, support) == compatibility_signature(n, complement)
    incoming_label = support
    outgoing_label = full ^ complement
    assert incoming_label == outgoing_label == support
    plus = 0b0101
    assert pair_crosses((0, 1), plus)
    assert support | outgoing_label == support != full

    # A fixed matching has 2^m crossing cuts and its full submatching closure
    # has 2^m distinct supports.  The stage-only support lift has all even sets.
    fixed_counts = {}
    for n in range(2, 14, 2):
        matching = rr_factor(n, 0)
        crossing = sum(
            all(pair_crosses(edge, plus) for edge in matching)
            for plus in weight_masks(n, n // 2)
        )
        assert crossing == 2 ** (n // 2)
        submatching_unions = {
            sum((1 << a) | (1 << b) for index, (a, b) in enumerate(matching) if selector & (1 << index))
            for selector in range(1 << len(matching))
        }
        assert len(submatching_unions) == 2 ** (n // 2)
        assert sum(comb(n, rank) for rank in range(0, n + 1, 2)) == 2 ** (n - 1)
        fixed_counts[n] = crossing

    repeated = ((0, 1), (0, 1))
    assert all(pair_crosses(edge, plus) for edge in repeated)
    assert len({point for edge in repeated for point in edge}) == 2
    return fixed_counts


def main() -> None:
    sizes = check_factorization_and_exact_family()
    print("PASS exact RR_n factorization, interval states, and size", sizes)
    hybrid = check_hybrid_n10()
    print("PASS n=10 seed-menu failure but literal hybrid success", hybrid)
    equivalent = check_deque_literal_equivalence()
    print("PASS forward interval recurrence equals literal induced DAG", equivalent)
    first = check_first_failure()
    print("PASS exhaustive first RR_n failure at n=22", first)
    closed = check_four_run_closed_forms()
    print("PASS four-run closed forms in broad finite audit", closed)
    unsafe = check_unsafe_quotients()
    print("PASS unsafe matching-state quotient/accounting checks", unsafe)
    print("ALL CYCLE-3 CP-M ADVERSARIAL CHECKS PASS (FINITE SCOPE)")


if __name__ == "__main__":
    main()

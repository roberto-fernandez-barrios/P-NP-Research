#!/usr/bin/env python3
"""Independent finite checks for the Cycle-3 CP-M matching attack.

This file deliberately uses only the Python standard library.  It checks
literal subset unions, not path or network-description counts.
"""

from __future__ import annotations

from collections import Counter
from functools import lru_cache
from hashlib import sha256
from itertools import combinations
from math import comb


def balanced_masks(n: int) -> list[int]:
    return [sum(1 << i for i in c) for c in combinations(range(n), n // 2)]


def cyclic_factor(n: int, r: int) -> tuple[tuple[int, int], ...]:
    """Round-robin one-factor M_r on Z_(n-1) union {infinity=n-1}."""
    assert n >= 2 and n % 2 == 0
    q = n - 1
    m = n // 2
    return ((q, r),) + tuple(((r + i) % q, (r - i) % q) for i in range(1, m))


def cyclic_factors(n: int) -> tuple[tuple[tuple[int, int], ...], ...]:
    return tuple(cyclic_factor(n, r) for r in range(n - 1))


def canonical_factor_order(n: int, r: int) -> tuple[int, ...]:
    """Orient and order M_r so every internal-rank prefix identifies r."""
    q = n - 1
    m = n // 2
    order = [r, q]
    for i in range(1, m):
        order.extend(((r + i) % q, (r - i) % q))
    assert len(order) == n and len(set(order)) == n
    return tuple(order)


def prefix_masks(order: tuple[int, ...]) -> tuple[int, ...]:
    out = [0]
    state = 0
    for x in order:
        state |= 1 << x
        out.append(state)
    return tuple(out)


def cyclic_path_family(n: int) -> set[int]:
    return {
        state
        for r in range(n - 1)
        for state in prefix_masks(canonical_factor_order(n, r))
    }


def crosses(pair: tuple[int, int], plus: int) -> bool:
    a, b = pair
    return bool((plus >> a) & 1) != bool((plus >> b) & 1)


def matching_crosses(matching: tuple[tuple[int, int], ...], plus: int) -> bool:
    return all(crosses(edge, plus) for edge in matching)


def crossing_count(matching: tuple[tuple[int, int], ...], plus: int) -> int:
    return sum(crosses(edge, plus) for edge in matching)


def check_factorization_and_literal_accounting() -> None:
    for n in range(2, 22, 2):
        factors = cyclic_factors(n)
        edge_mult = Counter(tuple(sorted(edge)) for matching in factors for edge in matching)
        assert len(factors) == n - 1
        assert len(edge_mult) == comb(n, 2)
        assert set(edge_mult.values()) == {1}

        family = cyclic_path_family(n)
        level_counts = Counter(mask.bit_count() for mask in family)
        assert len(family) == (n - 1) ** 2 + 2
        assert level_counts[0] == level_counts[n] == 1
        assert all(level_counts[k] == n - 1 for k in range(1, n))
    print("PASS cyclic one-factor paths: literal size (n-1)^2+2")


def compatible(state: int, plus: int) -> bool:
    return abs(2 * (state & plus).bit_count() - state.bit_count()) <= 1


def literal_witness(n: int, family: set[int], plus: int) -> tuple[int, ...] | None:
    """Search every inclusion-by-one edge induced by the literal family."""
    parent: dict[int, tuple[int, int] | None] = {0: None}
    for rank in range(1, n + 1):
        for state in sorted(s for s in family if s.bit_count() == rank):
            if not compatible(state, plus):
                continue
            for x in range(n):
                if (state >> x) & 1:
                    previous = state ^ (1 << x)
                    if previous in parent:
                        parent[state] = (previous, x)
                        break
    full = (1 << n) - 1
    if full not in parent:
        return None
    order = []
    state = full
    while state:
        previous, x = parent[state]  # type: ignore[misc]
        order.append(x)
        state = previous
    return tuple(reversed(order))


def make_line_reducer():
    """Return the exact deque-pair recurrence and its shared memo table."""

    @lru_cache(maxsize=None)
    def good(word: str) -> bool:
        if len(word) == 1:
            return word == "1"
        return (
            (word[0] != word[1] and good(word[2:]))
            or (word[-2] != word[-1] and good(word[:-2]))
            or (word[0] != word[-1] and good(word[1:-1]))
        )

    return good


def circle_reduces(word: str, line_good) -> bool:
    return any(line_good(word[r:] + word[:r]) for r in range(len(word)))


def normalized_finite_word(n: int, plus: int) -> str:
    """Reverse all signs if needed so infinity=n-1 is minus."""
    full = (1 << n) - 1
    if (plus >> (n - 1)) & 1:
        plus ^= full
    assert not ((plus >> (n - 1)) & 1)
    return "".join("1" if (plus >> i) & 1 else "0" for i in range(n - 1))


def reachable_interval_starts(word: str) -> dict[int, set[int]]:
    """Forward interval-growth DP at odd finite-interval lengths."""
    q = len(word)
    levels = {1: {i for i, bit in enumerate(word) if bit == "1"}}
    for length in range(1, q, 2):
        current = levels[length]
        following: set[int] = set()
        for start in current:
            options = (
                ((start - 2) % q, (start - 2) % q, (start - 1) % q),
                ((start - 1) % q, (start - 1) % q, (start + length) % q),
                (start, (start + length) % q, (start + length + 1) % q),
            )
            for new_start, a, b in options:
                if word[a] != word[b]:
                    following.add(new_start)
        levels[length + 2] = following
    return levels


def check_seed_factorization_and_hybrid_paths() -> None:
    # The sum/parity identity is checked exhaustively here; its proof is in
    # the companion report and applies to every one-factorization.
    for n in range(2, 12, 2):
        m = n // 2
        factors = cyclic_factors(n)
        for plus in balanced_masks(n):
            counts = [crossing_count(matching, plus) for matching in factors]
            assert sum(counts) == m * m
            assert all(c % 2 == m % 2 for c in counts)

    for n in (2, 4, 6, 8):
        factors = cyclic_factors(n)
        assert all(any(matching_crosses(M, plus) for M in factors) for plus in balanced_masks(n))

    # No listed n=10 factor crosses this cut, but the literal prefix union
    # has a hybrid path assembled from different factor prefixes.
    n = 10
    plus_set = {0, 1, 2, 3, 6}
    plus = sum(1 << i for i in plus_set)
    counts = [crossing_count(M, plus) for M in cyclic_factors(n)]
    assert counts == [3, 3, 3, 3, 3, 3, 1, 3, 3]
    assert not any(c == n // 2 for c in counts)
    witness = literal_witness(n, cyclic_path_family(n), plus)
    assert witness == (3, 9, 4, 2, 5, 6, 7, 1, 8, 0)
    assert all(crosses((witness[i], witness[i + 1]), plus) for i in range(0, n, 2))

    # A single fixed perfect matching already fails universality at n=4.
    matching = cyclic_factor(4, 0)
    plus = (1 << 3) | (1 << 0)
    assert not matching_crosses(matching, plus)
    print("PASS seed-menu warning: n=10 literal family has a hybrid witness")


def check_interval_equivalence_and_first_true_failure() -> None:
    # Compare the deque recurrence with a wholly separate literal-family DAG
    # search on every coloring through n=10.
    for n in range(2, 12, 2):
        family = cyclic_path_family(n)
        line_good = make_line_reducer()
        for plus in balanced_masks(n):
            word = normalized_finite_word(n, plus)
            by_intervals = circle_reduces(word, line_good)
            by_subsets = literal_witness(n, family, plus) is not None
            assert by_intervals == by_subsets

    # Exhaust all sign-reversal-normalized balanced colorings through n=20.
    for q in range(1, 20, 2):
        line_good = make_line_reducer()
        for positions in combinations(range(q), (q + 1) // 2):
            bits = ["0"] * q
            for i in positions:
                bits[i] = "1"
            assert circle_reduces("".join(bits), line_good)

    # At q=21 (n=22), precisely one rotation orbit of 21 words fails.
    q = 21
    line_good = make_line_reducer()
    bad = []
    for positions in combinations(range(q), (q + 1) // 2):
        bits = ["0"] * q
        for i in positions:
            bits[i] = "1"
        word = "".join(bits)
        if not circle_reduces(word, line_good):
            bad.append(word)
    counterword = "111111110000011100000"
    rotations = {counterword[r:] + counterword[:r] for r in range(q)}
    assert len(bad) == 21 and set(bad) == rotations
    digest = sha256(("\n".join(sorted(bad)) + "\n").encode()).hexdigest()
    assert digest == "ea61fa625c178336031605dcb22349e167b8e9ed3b42698b8ea383b507e44581"

    expected_levels = {
        1: {0, 1, 2, 3, 4, 5, 6, 7, 13, 14, 15},
        3: {6, 12, 14, 20},
        5: {5, 11, 12, 13, 19},
        7: {4, 18},
        9: {3, 17},
        11: {2, 3, 15, 16},
        13: set(),
    }
    levels = reachable_interval_starts(counterword)
    assert {length: levels[length] for length in expected_levels} == expected_levels
    print("PASS exhaustive RR coverage through n=20; first failure n=22 (21 rotations)")


def check_general_four_run_obstruction() -> None:
    # For every m>=11, the report proves this four-run word reaches no interval
    # of length 2m-9.  Check the claimed closed-form recurrence broadly.
    for m in range(11, 51):
        q = 2 * m - 1
        word = "1" * (m - 3) + "0" * 5 + "1" * 3 + "0" * (m - 6)
        assert len(word) == q and word.count("1") == m
        levels = reachable_interval_starts(word)
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
        assert not circle_reduces(word, make_line_reducer())
    print("PASS four-run countercolor for every symbolic case sampled, 11<=m<=50")


def compatibility_signature(n: int, state: int) -> tuple[bool, ...]:
    k = state.bit_count()
    assert k % 2 == 0
    return tuple((plus & state).bit_count() * 2 == k for plus in balanced_masks(n))


def check_signature_quotient_failure() -> None:
    # At n=4 the complementary middle supports S and T have identical
    # compatibility signatures.  Both are live on valid perfect-matching
    # paths, but merging them creates repeated-support cross-splices.
    n = 4
    source = 0
    sink = (1 << n) - 1
    S = (1 << 0) | (1 << 1)
    T = sink ^ S
    assert S != T
    assert compatibility_signature(n, S) == compatibility_signature(n, T)

    # The original live paths have labels (S,T) and (T,S).  After signature
    # quotienting, the cross-splice of source->S with T->sink repeats S.
    label_in = S ^ source
    label_out = sink ^ T
    assert label_in == label_out == S
    plus = (1 << 0) | (1 << 2)
    assert crosses((0, 1), plus)
    assert (source | label_in) == S
    assert (S | label_out) == S != sink
    print("PASS n=4 color-signature quotient counterexample")


def check_stage_only_support_explosion() -> None:
    # A stage-only pair selector has one abstract control state per even rank.
    # Once it is split by literal used support, every even subset occurs.
    for n in range(2, 18, 2):
        supports = []
        for state in range(1 << n):
            if state.bit_count() % 2 == 0:
                # Pair consecutive elements: every even support is reachable
                # by some sequence of disjoint unordered pairs.
                points = [i for i in range(n) if (state >> i) & 1]
                assert len(points) % 2 == 0
                pairs = list(zip(points[::2], points[1::2]))
                rebuilt = {x for pair in pairs for x in pair}
                assert rebuilt == set(points)
                supports.append(state)
        assert len(supports) == 2 ** (n - 1)

    # The unsplit abstraction first permits an illegal repeated-variable
    # length-two path at n=4.
    n = 4
    repeated_pair_path = ((0, 1), (0, 1))
    used = [x for pair in repeated_pair_path for x in pair]
    assert len(used) == n and len(set(used)) == 2 < n
    plus = (1 << 0) | (1 << 2)
    assert all(crosses(pair, plus) for pair in repeated_pair_path)
    print("PASS stage-only selector: support lift has 2^(n-1) even states")


def check_matching_menu_count() -> None:
    for n in range(2, 12, 2):
        m = n // 2
        matching = cyclic_factor(n, 0)
        accepted = sum(matching_crosses(matching, plus) for plus in balanced_masks(n))
        assert accepted == 2**m
        lower = (comb(n, m) + 2**m - 1) // 2**m
        assert lower >= 1
    print("PASS one fixed matching covers exactly 2^(n/2) signed balanced cuts")


def main() -> None:
    check_factorization_and_literal_accounting()
    check_seed_factorization_and_hybrid_paths()
    check_interval_equivalence_and_first_true_failure()
    check_general_four_run_obstruction()
    check_matching_menu_count()
    check_signature_quotient_failure()
    check_stage_only_support_explosion()
    print("ALL CP-M MATCHING CHECKS PASS")


if __name__ == "__main__":
    main()

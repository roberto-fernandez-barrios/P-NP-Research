#!/usr/bin/env python3
"""Independent finite checks for the Cycle-4 RR-to-interval reduction.

This checker does not use the asymptotic theorem of Fabris--Limaye--
Srinivasan--Yehudayoff.  It verifies the exact finite bijection on which the
application of that theorem rests:

* fix infinity negative and a finite positive root r;
* complement and reverse the nested cyclic intervals of a rooted RR chain;
* obtain a maximal chain in the ordinary one-interval family on the other
  n-2 finite points, with exactly negated discrepancies;
* perform the inverse construction from every ordinary interval witness.

All code uses only the Python standard library.
"""

from __future__ import annotations

from collections.abc import Iterable
from itertools import combinations


def balanced_masks(size: int) -> Iterable[int]:
    assert size % 2 == 0
    for choice in combinations(range(size), size // 2):
        yield sum(1 << point for point in choice)


def sign(mask: int, point: int) -> int:
    return 1 if mask & (1 << point) else -1


def discrepancy(mask: int, subset: int) -> int:
    return 2 * (mask & subset).bit_count() - subset.bit_count()


def cyclic_interval_mask(q: int, start: int, length: int) -> int:
    return sum(1 << ((start + offset) % q) for offset in range(length))


def rr_family(n: int) -> set[int]:
    """The literal corrected RR_n family, with infinity at n-1."""
    assert n >= 2 and n % 2 == 0
    q = n - 1
    infinity = 1 << q
    family = {0, (1 << n) - 1}
    family.update(1 << point for point in range(q))
    for rank in range(2, n):
        family.update(
            infinity | cyclic_interval_mask(q, start, rank - 1)
            for start in range(q)
        )
    return family


def direct_rr_witness(n: int, finite_plus: int, required_root: int) -> tuple[int, ...] | None:
    """Search the full literal induced subset DAG, fixing the first singleton."""
    q = n - 1
    assert finite_plus.bit_count() == n // 2  # infinity is fixed negative
    family = rr_family(n)
    full = (1 << n) - 1
    plus = finite_plus
    parents: dict[int, int | None] = {0: None}
    for rank in range(1, n + 1):
        for state in family:
            if state.bit_count() != rank or abs(discrepancy(plus, state)) > 1:
                continue
            if rank == 1 and state != 1 << required_root:
                continue
            for point in range(n):
                prior = state ^ (1 << point)
                if state & (1 << point) and prior in parents:
                    parents[state] = prior
                    break
    if full not in parents:
        return None
    reversed_chain = []
    state = full
    while state is not None:
        reversed_chain.append(state)
        state = parents[state]
    return tuple(reversed(reversed_chain))


def ordinary_interval_family(size: int) -> set[int]:
    family = {0}
    for left in range(size):
        state = 0
        for right in range(left, size):
            state |= 1 << right
            family.add(state)
    return family


def direct_interval_witness(size: int, plus: int) -> tuple[int, ...] | None:
    """Search every inclusion edge in the ordinary one-interval family."""
    assert size % 2 == 0 and plus.bit_count() == size // 2
    family = ordinary_interval_family(size)
    full = (1 << size) - 1
    parents: dict[int, int | None] = {0: None}
    for rank in range(1, size + 1):
        for state in family:
            if state.bit_count() != rank or abs(discrepancy(plus, state)) > 1:
                continue
            for point in range(size):
                prior = state ^ (1 << point)
                if state & (1 << point) and prior in parents:
                    parents[state] = prior
                    break
    if full not in parents:
        return None
    reversed_chain = []
    state = full
    while state is not None:
        reversed_chain.append(state)
        state = parents[state]
    return tuple(reversed(reversed_chain))


def place_restriction_around_root(restriction_plus: int, size: int, root: int) -> int:
    """Put [size] in cyclic order root+1,...,root-1 around a new root."""
    q = size + 1
    finite_plus = 1 << root
    for line_point in range(size):
        if restriction_plus & (1 << line_point):
            finite_plus |= 1 << ((root + 1 + line_point) % q)
    return finite_plus


def interval_chain_to_rr_chain(
    interval_chain: tuple[int, ...], size: int, root: int
) -> tuple[int, ...]:
    """Complement/reverse an interval chain and add root and infinity."""
    q = size + 1
    n = q + 1
    finite_full = (1 << q) - 1
    line_to_finite = tuple((root + 1 + point) % q for point in range(size))

    def embed(line_mask: int) -> int:
        result = 0
        for line_point, finite_point in enumerate(line_to_finite):
            if line_mask & (1 << line_point):
                result |= 1 << finite_point
        return result

    cyclic_intervals = tuple(
        finite_full ^ embed(interval_chain[size - offset])
        for offset in range(size + 1)
    )
    assert cyclic_intervals[0] == 1 << root
    assert cyclic_intervals[-1] == finite_full
    infinity = 1 << q
    return (0, 1 << root) + tuple(infinity | state for state in cyclic_intervals)


def rr_chain_to_interval_chain(
    rr_chain: tuple[int, ...], n: int, root: int
) -> tuple[int, ...]:
    """Remove infinity, complement, reverse, and relabel after cutting at root."""
    q = n - 1
    size = n - 2
    finite_full = (1 << q) - 1
    finite_to_line = {
        (root + 1 + line_point) % q: line_point for line_point in range(size)
    }

    def project(finite_mask: int) -> int:
        result = 0
        for finite_point, line_point in finite_to_line.items():
            if finite_mask & (1 << finite_point):
                result |= 1 << line_point
        return result

    # rr_chain[2:] is infinity joined with I_1,...,I_q.
    complements = tuple(
        project(finite_full ^ (state & finite_full)) for state in rr_chain[2:]
    )
    return tuple(reversed(complements))


def is_chain(chain: tuple[int, ...], ground_size: int) -> bool:
    return (
        len(chain) == ground_size + 1
        and chain[0] == 0
        and chain[-1] == (1 << ground_size) - 1
        and all(
            chain[rank].bit_count() == rank
            and chain[rank - 1] & ~chain[rank] == 0
            for rank in range(1, ground_size + 1)
        )
    )


def check_exact_bijection(max_n: int = 14) -> dict[int, dict[str, int]]:
    summaries: dict[int, dict[str, int]] = {}
    for n in range(2, max_n + 1, 2):
        size = n - 2
        q = n - 1
        interval_accept_count = 0
        checked_root_instances = 0
        for restriction_plus in balanced_masks(size):
            interval_witness = direct_interval_witness(size, restriction_plus)
            accepted_by_intervals = interval_witness is not None
            interval_accept_count += accepted_by_intervals
            for root in range(q):
                finite_plus = place_restriction_around_root(restriction_plus, size, root)
                rr_witness = direct_rr_witness(n, finite_plus, root)
                assert (rr_witness is not None) == accepted_by_intervals
                checked_root_instances += 1

                if interval_witness is not None:
                    constructed_rr = interval_chain_to_rr_chain(interval_witness, size, root)
                    assert is_chain(constructed_rr, n)
                    assert all(state in rr_family(n) for state in constructed_rr)
                    assert all(abs(discrepancy(finite_plus, state)) <= 1 for state in constructed_rr)

                if rr_witness is not None:
                    constructed_interval = rr_chain_to_interval_chain(rr_witness, n, root)
                    assert is_chain(constructed_interval, size)
                    assert all(
                        state in ordinary_interval_family(size)
                        for state in constructed_interval
                    )
                    assert all(
                        abs(discrepancy(restriction_plus, state)) <= 1
                        for state in constructed_interval
                    )

                    # The discrepancy identity is equality with a minus sign.
                    for rank in range(size + 1):
                        rr_state = rr_witness[n - rank]
                        interval_state = constructed_interval[rank]
                        assert discrepancy(finite_plus, rr_state) == -discrepancy(
                            restriction_plus, interval_state
                        )

        summaries[n] = {
            "ordinary_balanced_words": sum(1 for _ in balanced_masks(size)),
            "ordinary_interval_accepted": interval_accept_count,
            "root_instances_checked": checked_root_instances,
        }
    return summaries


def main() -> None:
    summaries = check_exact_bijection()
    for n, summary in summaries.items():
        print(f"n={n}: {summary}")
    print("PASS exact rooted RR <-> ordinary one-interval chain bijection")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Independent finite checks for the Cycle-3 balanced-chain foundation.

This program intentionally imports neither Cycle-2 optimizer/checker.  It
checks the literal set-system definition against the one-step Boolean DAG and
the two-step crossing-pair contraction, exhausts every family for n <= 4,
recomputes the layer-cover minima through n = 8, validates the stored upper
families without using their stored paths, and checks the n = 8 prefix claim
even when selected vertices are globally unreachable.

These are finite checks.  They do not prove an asymptotic construction.
"""

from __future__ import annotations

import json
from itertools import combinations, permutations
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CERTIFICATE_DIR = ROOT / "certificates" / "balanced_chain_exact"


def subsets_of_size(n: int, k: int) -> list[int]:
    return [
        sum(1 << i for i in choice)
        for choice in combinations(range(n), k)
    ]


def balanced_colorings(n: int) -> list[int]:
    if n % 2:
        return []
    return subsets_of_size(n, n // 2)


def imbalance(subset: int, plus: int) -> int:
    return 2 * (subset & plus).bit_count() - subset.bit_count()


def compatible(subset: int, plus: int) -> bool:
    return abs(imbalance(subset, plus)) <= 1


def prefix_chain(order: tuple[int, ...]) -> list[int]:
    chain = [0]
    current = 0
    for element in order:
        current |= 1 << element
        chain.append(current)
    return chain


def chain_is_good(order: tuple[int, ...], plus: int) -> bool:
    return all(compatible(subset, plus) for subset in prefix_chain(order))


def consecutive_pairs_cross(order: tuple[int, ...], plus: int) -> bool:
    return all(
        ((plus >> order[i]) & 1) != ((plus >> order[i + 1]) & 1)
        for i in range(0, len(order), 2)
    )


def boolean_dag_path_exists(n: int, family: set[int], plus: int) -> bool:
    """Literal selected compatible path in the Boolean lattice."""
    if 0 not in family or not compatible(0, plus):
        return False
    reachable = {0}
    for _level in range(n):
        next_reachable = set()
        for subset in reachable:
            for element in range(n):
                if (subset >> element) & 1:
                    continue
                nxt = subset | (1 << element)
                if nxt in family and compatible(nxt, plus):
                    next_reachable.add(nxt)
        reachable = next_reachable
    return (1 << n) - 1 in reachable


def contracted_pair_path_exists(n: int, family: set[int], plus: int) -> bool:
    """Path after contracting each odd prefix into a two-element edge."""
    full = (1 << n) - 1
    if 0 not in family or full not in family:
        return False
    reachable = {0}
    for _even_level in range(0, n, 2):
        next_reachable = set()
        for subset in reachable:
            missing = [i for i in range(n) if not ((subset >> i) & 1)]
            for a, b in combinations(missing, 2):
                if ((plus >> a) & 1) == ((plus >> b) & 1):
                    continue
                target = subset | (1 << a) | (1 << b)
                if target not in family:
                    continue
                odd_a = subset | (1 << a)
                odd_b = subset | (1 << b)
                if odd_a in family or odd_b in family:
                    next_reachable.add(target)
        reachable = next_reachable
    return full in reachable


def verify_pair_characterization() -> None:
    for n in (2, 4, 6, 8):
        colors = balanced_colorings(n)
        expected_count = 1 << (n // 2)
        for order in permutations(range(n)):
            count = 0
            for plus in colors:
                direct = chain_is_good(order, plus)
                paired = consecutive_pairs_cross(order, plus)
                assert direct == paired, (n, order, plus)
                count += direct
            assert count == expected_count, (n, order, count, expected_count)
        print(
            f"PASS consecutive-pair characterization n={n}; "
            f"each chain covers {expected_count} signed balanced colorings"
        )


def verify_all_families_small() -> dict[int, int]:
    optima: dict[int, int] = {}
    for n in (2, 4):
        subsets = 1 << n
        colors = balanced_colorings(n)
        best = subsets + 1
        valid_count = 0
        for family_code in range(1 << subsets):
            family = {
                subset
                for subset in range(subsets)
                if (family_code >> subset) & 1
            }
            direct_by_color = []
            for plus in colors:
                direct = boolean_dag_path_exists(n, family, plus)
                contracted = contracted_pair_path_exists(n, family, plus)
                assert direct == contracted, (n, family_code, plus)
                direct_by_color.append(direct)
            if not all(direct_by_color):
                continue

            valid_count += 1
            best = min(best, len(family))
            full = (1 << n) - 1
            assert 0 in family and full in family

            singletons = [s for s in family if s.bit_count() == 1]
            if len(singletons) == 1:
                v_bit = singletons[0]
                incident_pairs = sum(
                    s.bit_count() == 2 and bool(s & v_bit) for s in family
                )
                assert incident_pairs >= n // 2, (n, family_code)

            cosingletons = [s for s in family if s.bit_count() == n - 1]
            if len(cosingletons) == 1:
                omitted_bit = full ^ cosingletons[0]
                upper_pairs = sum(
                    s.bit_count() == n - 2 and bool((full ^ s) & omitted_bit)
                    for s in family
                )
                assert upper_pairs >= n // 2, (n, family_code)

        optima[n] = best
        print(
            f"PASS all {1 << subsets} families at n={n}: "
            f"path formulations agree, N({n})={best}, valid={valid_count}, S1/S2 hold"
        )
    return optima


def coverage_bitsets(n: int) -> tuple[list[int], list[int]]:
    colors = balanced_colorings(n)
    bitsets = []
    for subset in range(1 << n):
        bits = 0
        for index, plus in enumerate(colors):
            if compatible(subset, plus):
                bits |= 1 << index
        bitsets.append(bits)
    return colors, bitsets


def exact_tau(n: int, level: int, compatibility: list[int]) -> tuple[int, tuple[int, ...]]:
    colors = balanced_colorings(n)
    all_colors = (1 << len(colors)) - 1
    candidates = subsets_of_size(n, level)
    for size in range(len(candidates) + 1):
        for choice in combinations(candidates, size):
            covered = 0
            for subset in choice:
                covered |= compatibility[subset]
            if covered == all_colors:
                return size, choice
    raise AssertionError((n, level))


def verify_tau() -> dict[int, list[int]]:
    expected = {
        2: [1, 1, 1],
        4: [1, 1, 2, 1, 1],
        6: [1, 1, 3, 2, 3, 1, 1],
        8: [1, 1, 4, 2, 3, 2, 4, 1, 1],
    }
    result = {}
    for n, claimed in expected.items():
        colors, compatibility = coverage_bitsets(n)
        full = (1 << n) - 1
        assert colors
        assert all(
            compatibility[subset] == compatibility[full ^ subset]
            for subset in range(1 << n)
        )
        minima = [exact_tau(n, k, compatibility)[0] for k in range(n + 1)]
        assert minima == claimed, (n, minima, claimed)
        assert minima == list(reversed(minima))
        assert minima[0] == minima[n] == 1
        result[n] = minima
        print(f"PASS tau({n},k)={minima}; L({n})={sum(minima)}")
    return result


def verify_stored_upper_families() -> dict[int, int]:
    optima = {}
    for n in (2, 4, 6, 8):
        document = json.loads(
            (CERTIFICATE_DIR / f"exact_n{n}.json").read_text(encoding="utf-8")
        )
        family = set(document["family_masks"])
        assert len(family) == len(document["family_masks"])
        assert len(family) == document["claimed_optimum"]
        for plus in balanced_colorings(n):
            assert boolean_dag_path_exists(n, family, plus), (n, plus)
            assert contracted_pair_path_exists(n, family, plus), (n, plus)

        full = (1 << n) - 1
        complement_family = {full ^ subset for subset in family}
        for plus in balanced_colorings(n):
            assert boolean_dag_path_exists(n, complement_family, plus)

        optima[n] = document["claimed_optimum"]
        print(
            f"PASS stored n={n} family by fresh path search and complement duality; "
            f"size={len(family)}"
        )
    return optima


def extend_reachability(
    previous: dict[int, int], candidates: list[int], compatibility: list[int]
) -> dict[int, int]:
    answer = {}
    for candidate in candidates:
        colors = 0
        for prior, prior_colors in previous.items():
            if prior & ~candidate == 0:
                colors |= prior_colors
        colors &= compatibility[candidate]
        if colors:
            answer[candidate] = colors
    return answer


def verify_n8_prefix_bound_including_unreachable() -> None:
    """Check the six-missed-color claim beyond the Cycle-2 pruning.

    A family with minimum lower-layer counts can have r <= 4 globally
    reachable pairs.  For each r, it is monotone-safe to use as many as two
    reachable triples and three reachable four-sets: replacing an unreachable
    selected state by a reachable one cannot reduce coverage.  Thus the
    maxima below include families with selected-but-unreachable states.
    """
    n = 8
    colors, compatibility = coverage_bitsets(n)
    all_colors = (1 << len(colors)) - 1
    levels = [subsets_of_size(n, k) for k in range(n + 1)]
    maxima = {}

    for pair_count in range(5):
        best = 0
        for singleton in levels[1]:
            level1 = extend_reachability(
                {0: all_colors}, [singleton], compatibility
            )
            pair_candidates = extend_reachability(
                level1, levels[2], compatibility
            )
            for pair_choice in combinations(pair_candidates, pair_count):
                level2 = {s: pair_candidates[s] for s in pair_choice}
                triple_candidates = extend_reachability(
                    level2, levels[3], compatibility
                )
                triple_count = min(2, len(triple_candidates))
                for triple_choice in combinations(triple_candidates, triple_count):
                    level3 = {s: triple_candidates[s] for s in triple_choice}
                    four_candidates = extend_reachability(
                        level3, levels[4], compatibility
                    )
                    four_count = min(3, len(four_candidates))
                    for four_choice in combinations(four_candidates, four_count):
                        covered = 0
                        for subset in four_choice:
                            covered |= four_candidates[subset]
                        best = max(best, covered.bit_count())
        maxima[pair_count] = best

    assert maxima == {0: 0, 1: 40, 2: 60, 3: 64, 4: 64}, maxima
    print(
        "PASS n=8 minimum-count prefixes including unreachable selected states: "
        f"maxima by reachable-pair count {maxima}; global maximum 64/70"
    )


def verify_s1_countercolor_scheme() -> None:
    """Finite stress test of the quantified countercolor used in Lemma S1."""
    for n in range(2, 14, 2):
        half = n // 2
        for v in range(n):
            others = [u for u in range(n) if u != v]
            for degree in range(half):
                for neighbors in combinations(others, degree):
                    plus = {v, *neighbors}
                    plus.update(u for u in others if u not in plus and len(plus) < half)
                    assert len(plus) == half
                    assert v in plus
                    assert all(u in plus for u in neighbors)
                    assert all(
                        imbalance((1 << v) | (1 << u), sum(1 << x for x in plus))
                        == 2
                        for u in neighbors
                    )
    print("PASS S1 countercolor scheme for every even n<=12, v, and |Gamma|<n/2")


def verify_domain_edges() -> None:
    assert balanced_colorings(1) == []
    assert balanced_colorings(3) == []
    assert balanced_colorings(5) == []
    assert balanced_colorings(0) == [0]
    print(
        "PASS domain checks: odd n has no balanced coloring (hence would be vacuous); "
        "n=0 has the sole empty coloring and is outside O01"
    )


def main() -> None:
    verify_domain_edges()
    verify_pair_characterization()
    enumerated_optima = verify_all_families_small()
    tau = verify_tau()
    stored_optima = verify_stored_upper_families()
    verify_n8_prefix_bound_including_unreachable()
    verify_s1_countercolor_scheme()

    assert enumerated_optima == {2: 3, 4: 6}
    assert stored_optima == {2: 3, 4: 6, 6: 12, 8: 20}
    sigma = {n: stored_optima[n] - sum(tau[n]) for n in stored_optima}
    assert sigma == {2: 0, 4: 0, 6: 0, 8: 1}
    print(f"PASS derived sigma values {sigma}")
    print("ALL CYCLE-3 FOUNDATION CHECKS PASS")


if __name__ == "__main__":
    main()

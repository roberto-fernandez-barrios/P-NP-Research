#!/usr/bin/env python3
"""Clean-room adversarial checker for the finite Cycle-3 n=10 claim.

This file deliberately does not import any proposer search/checker module and
does not use stored coloring witnesses.  It reconstructs the literal
balanced-chain definition, independently exhausts the normalized level-cover
lower bounds and the normalized minimum-prefix obstruction, and verifies the
displayed upper family by forward dynamic programming.

The JSON artifacts are treated as claims to compare against recomputed
statistics, not as proof oracles.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import struct
from collections import Counter
from pathlib import Path


N = 10
UNIVERSE = (1 << N) - 1
ROOT = Path(__file__).resolve().parents[1]
CERT_DIR = ROOT / "certificates" / "balanced_chain_n10"
COLORS = tuple(m for m in range(1 << N) if m.bit_count() == N // 2)
ALL_COLOR_BITS = (1 << len(COLORS)) - 1


def balanced_at(subset: int, plus: int) -> bool:
    """Literal prefix condition: signed sum on subset has magnitude <= 1."""
    return abs(2 * (subset & plus).bit_count() - subset.bit_count()) <= 1


COMPAT = {
    subset: sum(
        1 << color_index
        for color_index, plus in enumerate(COLORS)
        if balanced_at(subset, plus)
    )
    for subset in range(1 << N)
}
LEVELS = {
    k: tuple(subset for subset in range(1 << N) if subset.bit_count() == k)
    for k in range(N + 1)
}


def assert_equal(actual, expected, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: got {actual!r}, expected {expected!r}")


def family_reached(family: set[int]) -> dict[int, int]:
    """For each selected state, bitset of colors with a literal path to it."""
    reached: dict[int, int] = {}
    if 0 not in family:
        return reached
    reached[0] = COMPAT[0]
    for level in range(1, N + 1):
        for state in sorted(family & set(LEVELS[level])):
            predecessor_colors = 0
            remaining = state
            while remaining:
                bit = remaining & -remaining
                predecessor_colors |= reached.get(state ^ bit, 0)
                remaining ^= bit
            reached[state] = predecessor_colors & COMPAT[state]
    return reached


def coverage_stats(level: int, proposed_tau: int) -> dict:
    """Exhaust all size-(tau-1) covers after fixing one canonical member.

    This implements a deliberately simple orbit normalization: the symmetric
    group is transitive on k-subsets, so relabel any member of a nonempty
    hypothetical cover to the first k coordinates.  No quotienting beyond
    that transitivity is used.
    """
    target_size = proposed_tau - 1
    if target_size == 0:
        return {
            "branches": 1,
            "maximum": 0,
            "histogram": {0: 1},
            "audit_digest": hashlib.sha256(struct.pack("<H", 0)).hexdigest(),
            "certificate_digest": hashlib.sha256(b"empty-family").hexdigest(),
        }

    canonical = (1 << level) - 1
    alternatives = tuple(x for x in LEVELS[level] if x != canonical)
    histogram: Counter[int] = Counter()
    digest = hashlib.sha256()
    maximum = -1
    branches = 0
    for rest in itertools.combinations(alternatives, target_size - 1):
        covered = COMPAT[canonical]
        for state in rest:
            covered |= COMPAT[state]
        count = covered.bit_count()
        histogram[count] += 1
        maximum = max(maximum, count)
        branches += 1
        # Independent, documented digest: coverage cardinalities in branch
        # order, encoded as little-endian unsigned 16-bit integers.
        digest.update(struct.pack("<H", count))
    return {
        "branches": branches,
        "maximum": maximum,
        "histogram": dict(sorted(histogram.items())),
        "audit_digest": digest.hexdigest(),
        "certificate_digest": certificate_level_digest(level, proposed_tau),
    }


def certificate_level_digest(level: int, proposed_tau: int) -> str:
    """Reproduce the artifact's documented-by-source branch-stream digest.

    This is separate from the clean-room digest above.  The artifact schema
    does not state its byte encoding, so this routine makes the producer's
    encoding explicit and checks that the stored hash is internally
    consistent; it is not used to prove the combinatorial result.
    """
    if proposed_tau == 1:
        return hashlib.sha256(b"empty-family").hexdigest()
    ordered = tuple(
        sum(1 << i for i in choice)
        for choice in itertools.combinations(range(N), level)
    )
    canonical = (1 << level) - 1
    candidates = tuple(s for s in ordered if s != canonical)
    digest = hashlib.sha256()
    for rest in itertools.combinations(candidates, proposed_tau - 2):
        covered = COMPAT[canonical]
        for state in rest:
            covered |= COMPAT[state]
        digest.update(canonical.to_bytes(2, "little"))
        for state in rest:
            digest.update(state.to_bytes(2, "little"))
        digest.update(covered.bit_count().to_bytes(2, "little"))
    return digest.hexdigest()


def exhaust_minimum_prefix() -> dict:
    """Exhaust every normalized reachable prefix with counts 1,1,5,3,5."""
    singleton = 1
    pairs = (3, 5, 9, 17, 33)

    pair_reach = {}
    for pair in pairs:
        pair_reach[pair] = COMPAT[singleton] & COMPAT[pair]

    triple_reach = {}
    for triple in LEVELS[3]:
        predecessor_colors = 0
        for pair in pairs:
            if pair & triple == pair:
                predecessor_colors |= pair_reach[pair]
        colors = predecessor_colors & COMPAT[triple]
        if colors:
            triple_reach[triple] = colors

    assert_equal(len(triple_reach), 30, "globally reachable triple candidates")

    triple_hist: Counter[int] = Counter()
    live_triples: list[tuple[tuple[int, ...], dict[int, int]]] = []
    for chosen in itertools.combinations(sorted(triple_reach), 3):
        count = (triple_reach[chosen[0]] | triple_reach[chosen[1]] |
                 triple_reach[chosen[2]]).bit_count()
        triple_hist[count] += 1
        if count == len(COLORS):
            live_triples.append((chosen, {t: triple_reach[t] for t in chosen}))

    level4_candidate_hist: Counter[int] = Counter()
    terminal_hist: Counter[int] = Counter()
    terminal_digest = hashlib.sha256()
    certificate_digest = hashlib.sha256()
    terminal_branches = 0
    terminal_maximum = -1
    first_best: list[dict] = []

    for chosen_triples, chosen_reach in live_triples:
        four_reach = {}
        for four in LEVELS[4]:
            predecessor_colors = 0
            for triple, colors in chosen_reach.items():
                if triple & four == triple:
                    predecessor_colors |= colors
            colors = predecessor_colors & COMPAT[four]
            if colors:
                four_reach[four] = colors
        level4_candidate_hist[len(four_reach)] += 1

        for chosen_fours in itertools.combinations(sorted(four_reach), 5):
            reached = 0
            for four in chosen_fours:
                reached |= four_reach[four]
            count = reached.bit_count()
            terminal_hist[count] += 1
            terminal_branches += 1
            terminal_digest.update(struct.pack("<H", count))
            for triple in chosen_triples:
                certificate_digest.update(triple.to_bytes(2, "little"))
            for four in chosen_fours:
                certificate_digest.update(four.to_bytes(2, "little"))
            certificate_digest.update(count.to_bytes(2, "little"))
            if count > terminal_maximum:
                terminal_maximum = count
                first_best = []
            if count == terminal_maximum and len(first_best) < 10:
                first_best.append(
                    {
                        "triple_masks": list(chosen_triples),
                        "four_masks": list(chosen_fours),
                        "covered_signed_colorings": count,
                        "missing_plus_masks": [
                            COLORS[i]
                            for i in range(len(COLORS))
                            if not (reached >> i) & 1
                        ],
                    }
                )

    return {
        "triple_candidate_count": len(triple_reach),
        "triple_choice_count": sum(triple_hist.values()),
        "triple_live_count": len(live_triples),
        "triple_histogram": dict(sorted(triple_hist.items())),
        "four_candidate_histogram": dict(sorted(level4_candidate_hist.items())),
        "terminal_branches": terminal_branches,
        "terminal_maximum": terminal_maximum,
        "terminal_histogram": dict(sorted(terminal_hist.items())),
        "audit_digest": terminal_digest.hexdigest(),
        "certificate_digest": certificate_digest.hexdigest(),
        "first_best": first_best,
    }


def check_upper_family(masks: list[int]) -> dict:
    family = set(masks)
    assert_equal(len(family), 35, "upper family distinct size")
    assert 0 in family and UNIVERSE in family
    reached = family_reached(family)
    assert_equal(reached.get(UNIVERSE, 0), ALL_COLOR_BITS,
                 "upper family accepted color bitset")

    level_counts = [sum(x.bit_count() == k for x in family) for k in range(N + 1)]
    deletion_losses = {}
    for removed in sorted(family):
        after = family_reached(family - {removed}).get(UNIVERSE, 0)
        lost = ALL_COLOR_BITS & ~after
        deletion_losses[removed] = lost.bit_count()
        if not lost:
            raise AssertionError(f"upper family is not inclusion-minimal: delete {removed}")

    # Count and enumerate all maximal selected chains without consulting
    # stored paths or coloring witnesses.
    path_count = {0: 1}
    for level in range(1, N + 1):
        for state in sorted(x for x in family if x.bit_count() == level):
            path_count[state] = sum(
                path_count.get(state ^ (1 << element), 0)
                for element in range(N)
                if state & (1 << element)
            )

    paths: list[tuple[int, ...]] = []
    def extend(state: int, path: tuple[int, ...]) -> None:
        if state == UNIVERSE:
            paths.append(path)
            return
        for element in range(N):
            nxt = state | (1 << element)
            if not state & (1 << element) and nxt in family:
                extend(nxt, path + (nxt,))
    extend(0, (0,))
    assert_equal(len(paths), path_count[UNIVERSE], "enumerated upper paths")
    per_path_color_counts = [
        sum(all(balanced_at(state, plus) for state in path) for plus in COLORS)
        for path in paths
    ]
    multiplicities = [
        sum(all(balanced_at(state, plus) for state in path) for path in paths)
        for plus in COLORS
    ]

    singletons = [s for s in family if s.bit_count() == 1]
    cosingletons = [s for s in family if s.bit_count() == N - 1]
    assert_equal(len(singletons), 1, "upper unique singleton count")
    assert_equal(len(cosingletons), 1, "upper unique cosingleton count")
    missing = UNIVERSE ^ cosingletons[0]
    assert all(s & singletons[0] for s in family if s.bit_count() == 2)
    assert all((UNIVERSE ^ s) & missing for s in family if s.bit_count() == N - 2)

    return {
        "level_counts": level_counts,
        "maximal_chain_count": path_count[UNIVERSE],
        "deletion_loss_min": min(deletion_losses.values()),
        "deletion_loss_max": max(deletion_losses.values()),
        "deletion_losses": deletion_losses,
        "per_path_color_counts": per_path_color_counts,
        "multiplicity_histogram": dict(sorted(Counter(multiplicities).items())),
        "unique_path_coloring_count": multiplicities.count(1),
        "multiplicity_range": [min(multiplicities), max(multiplicities)],
        "singleton": singletons[0],
        "cosingleton": cosingletons[0],
    }


def check_complement_duality() -> None:
    """Exhaust literal compatibility duality for all states and colors."""
    for plus in COLORS:
        for state in range(1 << N):
            assert_equal(
                balanced_at(state, plus),
                balanced_at(UNIVERSE ^ state, plus),
                f"complement compatibility state={state} plus={plus}",
            )


def main() -> None:
    with (CERT_DIR / "level_cover_certificate.json").open(encoding="utf-8") as f:
        cover_cert = json.load(f)
    with (CERT_DIR / "no_minimum_prefix.json").open(encoding="utf-8") as f:
        prefix_cert = json.load(f)
    with (CERT_DIR / "upper_size35.json").open(encoding="utf-8") as f:
        upper_cert = json.load(f)

    assert_equal(len(COLORS), 252, "signed balanced color count")
    claimed_tau = [1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1]
    assert_equal(cover_cert["exact_level_minima"], claimed_tau,
                 "level-cover certificate tau profile")
    assert_equal(sum(claimed_tau), 33, "tau level sum")

    independent_cover = {}
    # Directly check lower levels; upper levels follow only after the exhaustive
    # duality check below.  This avoids counting the same computation twice.
    for level in range(6):
        witnesses = cover_cert["lower_half_witnesses"][str(level)]
        covered = 0
        for state in witnesses:
            assert_equal(state.bit_count(), level, f"cover witness level {level}")
            covered |= COMPAT[state]
        assert_equal(covered, ALL_COLOR_BITS, f"cover witness coverage level {level}")
        assert_equal(len(set(witnesses)), claimed_tau[level],
                     f"cover witness size level {level}")

        stats = coverage_stats(level, claimed_tau[level])
        independent_cover[level] = stats
        stored = cover_cert["lower_bound_enumerations"][str(level)]
        assert_equal(stats["branches"], stored["branch_count"],
                     f"level {level} lower branch count")
        assert_equal(stats["maximum"], stored["maximum_signed_colorings_covered"],
                     f"level {level} lower maximum")
        assert_equal(
            {str(k): v for k, v in stats["histogram"].items()},
            stored["coverage_histogram"],
            f"level {level} lower histogram",
        )
        assert stats["maximum"] < len(COLORS)
        assert_equal(stats["certificate_digest"], stored["enumeration_sha256"],
                     f"level {level} stored enumeration SHA-256")

    check_complement_duality()
    for level in range(6, N + 1):
        witnesses = cover_cert["upper_half_complement_witnesses"][str(level)]
        assert_equal(len(set(witnesses)), claimed_tau[level],
                     f"upper cover witness size level {level}")
        assert all(state.bit_count() == level for state in witnesses)
        assert_equal(
            (lambda bits: bits)(
                __import__("functools").reduce(int.__or__,
                                               (COMPAT[x] for x in witnesses), 0)
            ),
            ALL_COLOR_BITS,
            f"upper cover witness coverage level {level}",
        )

    prefix = exhaust_minimum_prefix()
    assert_equal(prefix["triple_choice_count"], prefix_cert["level3_choice_count"],
                 "prefix triple branch count")
    assert_equal(prefix["triple_live_count"], prefix_cert["level3_live_choice_count"],
                 "prefix live triple count")
    assert_equal(
        {str(k): v for k, v in prefix["triple_histogram"].items()},
        prefix_cert["level3_coverage_histogram"],
        "prefix triple histogram",
    )
    assert_equal(
        {str(k): v for k, v in prefix["four_candidate_histogram"].items()},
        prefix_cert["level4_reachable_candidate_count_histogram_over_live_level3_choices"],
        "prefix level-four candidate histogram",
    )
    assert_equal(prefix["terminal_branches"], prefix_cert["level4_choice_count"],
                 "prefix terminal branch count")
    assert_equal(prefix["terminal_maximum"],
                 prefix_cert["level4_maximum_signed_colorings_reached"],
                 "prefix terminal maximum")
    assert_equal(
        {str(k): v for k, v in prefix["terminal_histogram"].items()},
        prefix_cert["level4_coverage_histogram"],
        "prefix terminal histogram",
    )
    assert_equal(prefix["first_best"], prefix_cert["first_best_branches"],
                 "prefix first best branches")
    assert_equal(prefix["certificate_digest"], prefix_cert["enumeration_sha256"],
                 "prefix stored enumeration SHA-256")
    assert prefix["terminal_maximum"] < len(COLORS)

    masks = upper_cert.get("family_masks", upper_cert.get("masks"))
    if masks is None:
        raise AssertionError("upper certificate contains no family mask list")
    upper = check_upper_family(masks)
    assert_equal(upper["level_counts"], [1, 1, 5, 3, 6, 3, 6, 3, 5, 1, 1],
                 "upper family level profile")
    assert_equal(upper["maximal_chain_count"], 60,
                 "upper family maximal-chain count")
    assert set(upper["per_path_color_counts"]) == {32}
    assert_equal(upper["multiplicity_range"], [1, 30],
                 "upper coloring path-multiplicity range")
    assert_equal(upper["unique_path_coloring_count"], 22,
                 "upper unique-path coloring count")
    assert_equal(upper_cert["level_counts"], upper["level_counts"],
                 "upper stored level profile")
    assert_equal(upper_cert["structure"]["maximal_chain_count"],
                 upper["maximal_chain_count"], "upper stored path count")
    assert_equal(
        upper_cert["structure"]["single_subset_removal_lost_coloring_counts"],
        {str(k): v for k, v in upper["deletion_losses"].items()},
        "upper stored deletion-loss counts",
    )
    assert_equal(
        upper_cert["structure"]["signed_coloring_path_multiplicity_histogram"],
        {str(k): v for k, v in upper["multiplicity_histogram"].items()},
        "upper stored path-multiplicity histogram",
    )
    assert_equal(upper_cert["structure"]["unique_singleton_mask"], upper["singleton"],
                 "upper singleton anchor")
    assert_equal(upper_cert["structure"]["unique_cosingleton_mask"], upper["cosingleton"],
                 "upper cosingleton anchor")

    # Pure arithmetic/accounting part of the size-34 argument.
    assert_equal(sum(claimed_tau), 33, "minimum level accounting")
    possible_surplus_levels = [
        k for k in range(N + 1) if len(LEVELS[k]) > claimed_tau[k]
    ]
    assert_equal(possible_surplus_levels, list(range(1, 10)),
                 "possible one-unit surplus levels")
    lower_prefix_excluded = {k for k in possible_surplus_levels if k >= 5}
    dual_suffix_excluded = {k for k in possible_surplus_levels if k <= 4}
    assert_equal(lower_prefix_excluded | dual_suffix_excluded,
                 set(possible_surplus_levels), "size-34 case split")
    assert not (lower_prefix_excluded & dual_suffix_excluded)

    file_hashes = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(CERT_DIR.glob("*.json"))
    }
    print("PASS clean-room literal n=10 balanced-chain reconstruction")
    print("PASS normalized exact level minima", claimed_tau, "sum=33")
    print("PASS minimum prefix:", prefix["terminal_branches"],
          "branches, maximum", prefix["terminal_maximum"], "/ 252")
    print("PASS exhaustive complement duality and size-34 surplus split")
    print("PASS upper family by forward DP; no stored witness used;", upper)
    print("AUDIT level digests", {k: v["audit_digest"] for k, v in independent_cover.items()})
    print("AUDIT prefix digest", prefix["audit_digest"])
    print("AUDIT certificate file SHA-256", file_hashes)
    print("FINITE CONCLUSION ONLY: the checked artifacts establish N(10)=35")


if __name__ == "__main__":
    main()

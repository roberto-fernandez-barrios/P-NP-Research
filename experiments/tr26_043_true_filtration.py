#!/usr/bin/env python3
"""Exact rational enumerator for the TR26-043 v0 two-block process.

This program implements Definition 3.1 of the original (April 1, 2026)
version of ECCC TR26-043 under two explicit reveal policies.  ``eager``
inspects both active candidates before comparison.  ``minimal`` observes that
at H=0 a tie is algebraically certain, tosses its coin first, and inspects only
the selected candidate; all nonzero-height comparisons still inspect both.
The probability space is a uniformly random
balanced coloring of [n], together with independent fair coins used exactly
when the two candidate extensions have equal absolute imbalance.

The crucial modelling choice is the *true* chain-step filtration.  At the end
of a step, both candidate colors consulted at that step have been revealed,
although only one candidate was consumed.  Consequently the unconsumed
frontier is recorded in the next state.  A newly exposed frontier is revealed
only during the next transition.  All probabilities are fractions.Fraction.

The enumerator is deliberately limited to the completely specified
two-block rule.  The paper's multiscale prose does not determine a unique
finite-state process (see the accompanying audit), so this file does not
silently choose a gap-filler or an odd-residual convention.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, replace
from fractions import Fraction
from typing import Any, Iterable


UNKNOWN = 0
MINUS = -1
PLUS = 1


def frac_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


@dataclass(frozen=True)
class BoundaryState:
    """One atom of the true filtration immediately after a chain step.

    Step 0 is the initial state.  ``revealed[i]`` is nonzero exactly when the
    process has inspected f(i+1).  In a nonterminal active state after step 0,
    exactly one current frontier was normally inspected but not consumed.
    ``probability`` is the exact probability of the complete observation/coin
    history represented by this state.
    """

    n: int
    a: int
    b: int
    height: int
    assigned_order: tuple[int, ...]
    revealed: tuple[int, ...]
    tie_outcomes: tuple[str, ...]
    probability: Fraction
    trace: tuple[dict[str, Any], ...]
    above_band_excursion: int | None
    next_excursion_id: int
    last_band_visit: int

    @property
    def half(self) -> int:
        return self.n // 2

    @property
    def step(self) -> int:
        return self.a + self.b

    @property
    def deviation(self) -> int:
        return self.a - self.b

    @property
    def left_active(self) -> bool:
        return self.a < self.half

    @property
    def right_active(self) -> bool:
        return self.b < self.half

    @property
    def complete(self) -> bool:
        return self.step == self.n

    @property
    def assigned_mask(self) -> int:
        mask = 0
        for element in self.assigned_order:
            mask |= 1 << element
        return mask

    def frontier_index(self, block: str) -> int | None:
        if block == "L":
            return self.a if self.left_active else None
        if block == "R":
            return self.half + self.b if self.right_active else None
        raise ValueError(block)

    def filtration_key(self) -> tuple[Any, ...]:
        """A complete atom identifier (derived state included for checking)."""

        return (
            self.n,
            self.a,
            self.b,
            self.height,
            self.assigned_order,
            self.revealed,
            self.tie_outcomes,
            self.above_band_excursion,
            self.next_excursion_id,
            self.last_band_visit,
        )


def initial_state(n: int) -> BoundaryState:
    if n <= 0 or n % 2:
        raise ValueError("n must be a positive even integer")
    return BoundaryState(
        n=n,
        a=0,
        b=0,
        height=0,
        assigned_order=(),
        revealed=(UNKNOWN,) * n,
        tie_outcomes=(),
        probability=Fraction(1),
        trace=(),
        above_band_excursion=None,
        next_excursion_id=1,
        last_band_visit=0,
    )


def _remaining_color_counts(state: BoundaryState) -> tuple[int, int, int]:
    plus_seen = sum(value == PLUS for value in state.revealed)
    minus_seen = sum(value == MINUS for value in state.revealed)
    plus_left = state.half - plus_seen
    minus_left = state.half - minus_seen
    unknown = state.n - plus_seen - minus_seen
    assert plus_left >= 0 and minus_left >= 0
    assert plus_left + minus_left == unknown
    return plus_left, minus_left, unknown


def _reveal(
    branches: list[tuple[BoundaryState, Fraction, list[dict[str, Any]]]],
    index: int,
    block: str,
) -> list[tuple[BoundaryState, Fraction, list[dict[str, Any]]]]:
    """Reveal one frontier, branching with its exact conditional law."""

    result: list[tuple[BoundaryState, Fraction, list[dict[str, Any]]]] = []
    for state, conditional, events in branches:
        if state.revealed[index] != UNKNOWN:
            result.append((state, conditional, events))
            continue
        plus_left, minus_left, unknown = _remaining_color_counts(state)
        for value, count in ((PLUS, plus_left), (MINUS, minus_left)):
            if count == 0:
                continue
            revealed = list(state.revealed)
            revealed[index] = value
            event = {
                "kind": "reveal",
                "element": index + 1,
                "block": block,
                "value": value,
                "conditional_probability": frac_text(Fraction(count, unknown)),
                "previously_unrevealed": unknown,
                "plus_remaining_before": plus_left,
                "minus_remaining_before": minus_left,
            }
            result.append(
                (
                    replace(state, revealed=tuple(revealed)),
                    conditional * Fraction(count, unknown),
                    events + [event],
                )
            )
    return result


def advance(
    state: BoundaryState, reveal_policy: str = "eager"
) -> list[tuple[BoundaryState, Fraction]]:
    """Return the exact conditional distribution of the next boundary state."""

    if state.complete:
        return []
    if reveal_policy not in {"eager", "minimal"}:
        raise ValueError("reveal_policy must be 'eager' or 'minimal'")

    branches: list[tuple[BoundaryState, Fraction, list[dict[str, Any]]]] = [
        (state, Fraction(1), [])
    ]
    left = state.frontier_index("L")
    right = state.frontier_index("R")
    decision_branches: list[
        tuple[BoundaryState, Fraction, list[dict[str, Any]], str, bool, str | None]
    ] = []
    if (
        reveal_policy == "minimal"
        and state.height == 0
        and left is not None
        and right is not None
    ):
        # At H=0 both candidate absolute heights equal one without inspecting
        # either color.  A query-minimal implementation can toss the tie coin
        # first and reveal only the candidate it will consume.
        for choice, index in (("L", left), ("R", right)):
            seeded = [
                (
                    state,
                    Fraction(1, 2),
                    [
                        {
                            "kind": "tie_coin_before_color_reveal",
                            "choice": choice,
                            "conditional_probability": "1/2",
                        }
                    ],
                )
            ]
            seeded = _reveal(seeded, index, choice)
            for revealed_state, conditional, events in seeded:
                decision_branches.append(
                    (revealed_state, conditional, events, choice, True, choice)
                )
    else:
        # A fixed reveal order is only a chain-rule representation.  The
        # decision state after all required reveals contains both observations.
        if left is not None:
            branches = _reveal(branches, left, "L")
        if right is not None:
            branches = _reveal(branches, right, "R")

        for revealed_state, conditional, events in branches:
            if left is None:
                decision_branches.append(
                    (revealed_state, conditional, events, "R", False, None)
                )
                continue
            if right is None:
                decision_branches.append(
                    (revealed_state, conditional, events, "L", False, None)
                )
                continue

            left_value = revealed_state.revealed[left]
            right_value = revealed_state.revealed[right]
            left_abs = abs(revealed_state.height + left_value)
            right_abs = abs(revealed_state.height + right_value)
            if left_abs < right_abs:
                decision_branches.append(
                    (revealed_state, conditional, events, "L", False, None)
                )
            elif right_abs < left_abs:
                decision_branches.append(
                    (revealed_state, conditional, events, "R", False, None)
                )
            else:
                for choice in ("L", "R"):
                    decision_branches.append(
                        (
                            revealed_state,
                            conditional * Fraction(1, 2),
                            events,
                            choice,
                            True,
                            choice,
                        )
                    )

    output: list[tuple[BoundaryState, Fraction]] = []
    for revealed_state, conditional, events, choice, tied, coin in decision_branches:
        chosen = revealed_state.frontier_index(choice)
        assert chosen is not None
        value = revealed_state.revealed[chosen]
        old_abs = abs(revealed_state.height)
        new_height = revealed_state.height + value
        new_abs = abs(new_height)
        new_a = revealed_state.a + (choice == "L")
        new_b = revealed_state.b + (choice == "R")
        new_step = new_a + new_b

        excursion = revealed_state.above_band_excursion
        next_excursion = revealed_state.next_excursion_id
        last_band = revealed_state.last_band_visit
        excursion_event: dict[str, Any] | None = None
        if old_abs <= 1 and new_abs > 1:
            excursion = next_excursion
            next_excursion += 1
            excursion_event = {
                "kind": "above_band_excursion_start",
                "excursion_id": excursion,
                "step": new_step,
            }
        elif old_abs > 1 and new_abs <= 1:
            excursion_event = {
                "kind": "above_band_excursion_end",
                "excursion_id": excursion,
                "step": new_step,
            }
            excursion = None
            last_band = new_step
        elif new_abs <= 1:
            last_band = new_step

        tie_outcomes = revealed_state.tie_outcomes
        if tied:
            assert coin is not None
            tie_outcomes += (coin,)

        persistent: list[dict[str, Any]] = []
        for block in ("L", "R"):
            # Compute frontier in the post-state coordinates directly.
            idx = new_a if block == "L" and new_a < revealed_state.half else None
            if block == "R" and new_b < revealed_state.half:
                idx = revealed_state.half + new_b
            if idx is not None and revealed_state.revealed[idx] != UNKNOWN:
                persistent.append(
                    {
                        "block": block,
                        "element": idx + 1,
                        "value": revealed_state.revealed[idx],
                    }
                )

        decision_event: dict[str, Any] = {
            "kind": "decision_and_consume",
            "step": new_step,
            "pre": {
                "a": state.a,
                "b": state.b,
                "H": state.height,
                "D": state.deviation,
                "assigned_subset": sorted(i + 1 for i in state.assigned_order),
            },
            "frontiers": {
                "L": None
                if left is None
                else {"element": left + 1, "value": revealed_state.revealed[left]},
                "R": None
                if right is None
                else {"element": right + 1, "value": revealed_state.revealed[right]},
            },
            "tied": tied,
            "tie_coin": coin,
            "chosen_block": choice,
            "chosen_element": chosen + 1,
            "chosen_value": value,
            "post": {
                "a": new_a,
                "b": new_b,
                "H": new_height,
                "D": new_a - new_b,
                "assigned_subset": sorted(
                    i + 1 for i in revealed_state.assigned_order + (chosen,)
                ),
            },
            "persistent_revealed_frontiers": persistent,
        }
        new_events = events + [decision_event]
        if excursion_event is not None:
            new_events.append(excursion_event)

        new_state = BoundaryState(
            n=revealed_state.n,
            a=new_a,
            b=new_b,
            height=new_height,
            assigned_order=revealed_state.assigned_order + (chosen,),
            revealed=revealed_state.revealed,
            tie_outcomes=tie_outcomes,
            probability=revealed_state.probability * conditional,
            trace=revealed_state.trace + (tuple(new_events),),
            above_band_excursion=excursion,
            next_excursion_id=next_excursion,
            last_band_visit=last_band,
        )
        output.append((new_state, conditional))
    assert sum((conditional for _, conditional in output), Fraction(0)) == 1
    return output


def one_step_statistics(
    state: BoundaryState, reveal_policy: str = "eager"
) -> dict[str, Fraction]:
    """Compute conditional h-growth probability and deviation drift."""

    children = advance(state, reveal_policy)
    upward = sum(
        (
            conditional
            for child, conditional in children
            if abs(child.height) == abs(state.height) + 1
        ),
        Fraction(0),
    )
    drift = sum(
        (
            conditional * (child.deviation - state.deviation)
            for child, conditional in children
        ),
        Fraction(0),
    )
    return {"upward_probability": upward, "deviation_drift": drift}


def enumerate_boundaries(
    n: int, reveal_policy: str = "eager"
) -> list[list[BoundaryState]]:
    """Enumerate every filtration atom, without merging coin histories."""

    levels: list[list[BoundaryState]] = [[initial_state(n)]]
    for _ in range(n):
        next_level: list[BoundaryState] = []
        for state in levels[-1]:
            next_level.extend(child for child, _ in advance(state, reveal_policy))
        levels.append(next_level)
        assert sum((s.probability for s in next_level), Fraction(0)) == 1
    return levels


def enumerate_to_first_exhaustion(
    n: int, reveal_policy: str = "eager"
) -> dict[str, Any]:
    """Enumerate the multiscale probe's first active phase exactly.

    Section 8 stops a scale as soon as one block is exhausted, unlike the
    complete Definition-3.1 path used by :func:`enumerate_boundaries`.  This
    routine records that exact stopping distribution.  It does not recurse:
    v0 has no split rule for an odd residual and no deterministic gap filler.
    """

    active = [initial_state(n)]
    terminal: list[BoundaryState] = []
    reachable_masks = {0}
    active_atoms_by_local_step = [1]
    while active:
        next_active: list[BoundaryState] = []
        for state in active:
            for child, _ in advance(state, reveal_policy):
                reachable_masks.add(child.assigned_mask)
                if child.left_active and child.right_active:
                    next_active.append(child)
                else:
                    terminal.append(child)
        active = next_active
        active_atoms_by_local_step.append(len(active))

    residual_distribution: dict[int, Fraction] = {}
    for state in terminal:
        residual = state.n - state.step
        residual_distribution[residual] = (
            residual_distribution.get(residual, Fraction(0)) + state.probability
        )
    terminal_mass = sum((state.probability for state in terminal), Fraction(0))
    odd_mass = sum(
        (
            probability
            for residual, probability in residual_distribution.items()
            if residual % 2
        ),
        Fraction(0),
    )
    return {
        "n": n,
        "reveal_policy": reveal_policy,
        "stopping_rule": "first time either local block is exhausted",
        "terminal_filtration_atoms": len(terminal),
        "terminal_probability_mass": frac_text(terminal_mass),
        "active_atoms_by_local_step": active_atoms_by_local_step,
        "residual_size_distribution": {
            str(residual): frac_text(probability)
            for residual, probability in sorted(residual_distribution.items())
        },
        "odd_residual_probability": frac_text(odd_mass),
        "distinct_probe_subsets_before_or_at_exhaustion": len(reachable_masks),
        "reachable_probe_subsets": [
            [i + 1 for i in range(n) if mask & (1 << i)]
            for mask in sorted(reachable_masks)
        ],
    }


def _state_summary(state: BoundaryState) -> dict[str, Any]:
    plus_left, minus_left, unknown = _remaining_color_counts(state)
    frontiers: dict[str, Any] = {}
    for block in ("L", "R"):
        idx = state.frontier_index(block)
        frontiers[block] = None if idx is None else {
            "element": idx + 1,
            "revealed_value": state.revealed[idx],
        }
    return {
        "n": state.n,
        "step": state.step,
        "a": state.a,
        "b": state.b,
        "H": state.height,
        "absolute_H": abs(state.height),
        "D": state.deviation,
        "assigned_order": [i + 1 for i in state.assigned_order],
        "assigned_subset": sorted(i + 1 for i in state.assigned_order),
        "revealed": {
            str(i + 1): value
            for i, value in enumerate(state.revealed)
            if value != UNKNOWN
        },
        "frontiers": frontiers,
        "tie_outcomes": list(state.tie_outcomes),
        "history_probability": frac_text(state.probability),
        "unrevealed_counts": {
            "plus": plus_left,
            "minus": minus_left,
            "total": unknown,
        },
        "above_band_excursion": state.above_band_excursion,
        "last_band_visit": state.last_band_visit,
    }


def certificate(
    state: BoundaryState, claim: str, reveal_policy: str = "eager"
) -> dict[str, Any]:
    stats = one_step_statistics(state, reveal_policy)
    result = {
        "claim": claim,
        "filtration_boundary": _state_summary(state),
        "conditional_upward_probability": frac_text(stats["upward_probability"]),
        "conditional_deviation_drift": frac_text(stats["deviation_drift"]),
        "trace": [list(events) for events in state.trace],
        "next_step_distribution": [],
    }
    for child, conditional in advance(state, reveal_policy):
        result["next_step_distribution"].append(
            {
                "conditional_probability": frac_text(conditional),
                "post": _state_summary(child),
                "new_trace_events": list(child.trace[-1]),
            }
        )
    return result


def find_first(
    levels: list[list[BoundaryState]], predicate
) -> BoundaryState | None:
    for level in levels[:-1]:
        for state in level:
            if predicate(state):
                return state
    return None


def analyze(
    n: int,
    include_reachable_subsets: bool = False,
    reveal_policy: str = "eager",
) -> dict[str, Any]:
    levels = enumerate_boundaries(n, reveal_policy)
    forced_eligible: list[BoundaryState] = []
    forced_bad: list[BoundaryState] = []
    martingale_bad_literal: list[BoundaryState] = []
    martingale_bad_active: list[BoundaryState] = []
    martingale_bad_strict_interior: list[BoundaryState] = []

    for level in levels[:-1]:
        for state in level:
            stats = one_step_statistics(state, reveal_policy)
            both_active = state.left_active and state.right_active
            if both_active and abs(state.height) >= 1:
                forced_eligible.append(state)
                if stats["upward_probability"] > Fraction(1, 4):
                    forced_bad.append(state)
            if stats["deviation_drift"] != 0:
                martingale_bad_literal.append(state)
                if both_active:
                    martingale_bad_active.append(state)
                    # Every possible next decision leaves both blocks active.
                    if all(
                        child.left_active and child.right_active
                        for child, _ in advance(state, reveal_policy)
                    ):
                        martingale_bad_strict_interior.append(state)

    reachable_by_level: list[list[int]] = []
    reachable_union: set[int] = set()
    for level in levels:
        masks = sorted({state.assigned_mask for state in level})
        reachable_by_level.append(masks)
        reachable_union.update(masks)

    result: dict[str, Any] = {
        "n": n,
        "reveal_policy": reveal_policy,
        "filtration_atoms_by_step": [len(level) for level in levels],
        "probability_mass_by_step": [
            frac_text(sum((state.probability for state in level), Fraction(0)))
            for level in levels
        ],
        "distinct_reachable_subsets_by_level": [
            len(masks) for masks in reachable_by_level
        ],
        "distinct_reachable_subsets_total": len(reachable_union),
        "forced_probability": {
            "eligible_atoms": len(forced_eligible),
            "violating_atoms": len(forced_bad),
            "maximum": frac_text(
                max(
                    (
                        one_step_statistics(state, reveal_policy)["upward_probability"]
                        for state in forced_eligible
                    ),
                    default=Fraction(0),
                )
            ),
            "first_certificate": None
            if not forced_bad
            else certificate(
                forced_bad[0], "Lemma 4.1: p_t <= 1/4", reveal_policy
            ),
        },
        "block_deviation": {
            "literal_nonzero_drift_atoms": len(martingale_bad_literal),
            "active_nonzero_drift_atoms": len(martingale_bad_active),
            "strict_interior_nonzero_drift_atoms": len(
                martingale_bad_strict_interior
            ),
            "first_literal_certificate": None
            if not martingale_bad_literal
            else certificate(
                martingale_bad_literal[0],
                "Lemma 3.3: D is a martingale (literal path)",
                reveal_policy,
            ),
            "first_active_certificate": None
            if not martingale_bad_active
            else certificate(
                martingale_bad_active[0],
                "Lemma 3.3: D is a martingale before block exhaustion",
                reveal_policy,
            ),
            "first_strict_interior_certificate": None
            if not martingale_bad_strict_interior
            else certificate(
                martingale_bad_strict_interior[0],
                "Lemma 3.3: D is a martingale strictly inside both blocks",
                reveal_policy,
            ),
        },
    }
    if include_reachable_subsets:
        result["reachable_subsets_by_level"] = [
            [[i + 1 for i in range(n) if mask & (1 << i)] for mask in masks]
            for masks in reachable_by_level
        ]
    return result


def compact_summary(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "n": result["n"],
        "filtration_atoms_by_step": result["filtration_atoms_by_step"],
        "distinct_reachable_subsets_by_level": result[
            "distinct_reachable_subsets_by_level"
        ],
        "distinct_reachable_subsets_total": result[
            "distinct_reachable_subsets_total"
        ],
        "forced_violations": result["forced_probability"]["violating_atoms"],
        "max_forced_probability": result["forced_probability"]["maximum"],
        "literal_martingale_violations": result["block_deviation"][
            "literal_nonzero_drift_atoms"
        ],
        "active_martingale_violations": result["block_deviation"][
            "active_nonzero_drift_atoms"
        ],
        "strict_interior_martingale_violations": result["block_deviation"][
            "strict_interior_nonzero_drift_atoms"
        ],
    }


def scan(max_n: int, reveal_policy: str = "eager") -> dict[str, Any]:
    if max_n <= 0 or max_n % 2:
        raise ValueError("max_n must be a positive even integer")
    results = [
        analyze(n, reveal_policy=reveal_policy)
        for n in range(2, max_n + 1, 2)
    ]
    return {
        "semantics": "true chain-step filtration",
        "reveal_policy": reveal_policy,
        "checked_even_n": list(range(2, max_n + 1, 2)),
        "summaries": [compact_summary(result) for result in results],
        "first_n": {
            "forced_probability": next(
                (
                    result["n"]
                    for result in results
                    if result["forced_probability"]["violating_atoms"]
                ),
                None,
            ),
            "literal_martingale": next(
                (
                    result["n"]
                    for result in results
                    if result["block_deviation"]["literal_nonzero_drift_atoms"]
                ),
                None,
            ),
            "active_martingale": next(
                (
                    result["n"]
                    for result in results
                    if result["block_deviation"]["active_nonzero_drift_atoms"]
                ),
                None,
            ),
            "strict_interior_martingale": next(
                (
                    result["n"]
                    for result in results
                    if result["block_deviation"][
                        "strict_interior_nonzero_drift_atoms"
                    ]
                ),
                None,
            ),
        },
        "certificates": {
            "forced_probability": next(
                (
                    result["forced_probability"]["first_certificate"]
                    for result in results
                    if result["forced_probability"]["first_certificate"]
                ),
                None,
            ),
            "literal_martingale": next(
                (
                    result["block_deviation"]["first_literal_certificate"]
                    for result in results
                    if result["block_deviation"]["first_literal_certificate"]
                ),
                None,
            ),
            "active_martingale": next(
                (
                    result["block_deviation"]["first_active_certificate"]
                    for result in results
                    if result["block_deviation"]["first_active_certificate"]
                ),
                None,
            ),
            "strict_interior_martingale": next(
                (
                    result["block_deviation"]["first_strict_interior_certificate"]
                    for result in results
                    if result["block_deviation"][
                        "first_strict_interior_certificate"
                    ]
                ),
                None,
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--n", type=int, help="analyze one positive even n")
    group.add_argument(
        "--scan-even-through", type=int, help="scan every positive even n up to this"
    )
    parser.add_argument(
        "--include-reachable-subsets",
        action="store_true",
        help="include the exact subsets, rather than only their counts",
    )
    parser.add_argument(
        "--first-exhaustion",
        action="store_true",
        help="with --n, enumerate the scale probe only to first block exhaustion",
    )
    parser.add_argument(
        "--reveal-policy",
        choices=("eager", "minimal"),
        default="eager",
        help="whether H=0 compares by inspecting both colors or tosses the known tie first",
    )
    args = parser.parse_args()
    if args.n is not None:
        if args.first_exhaustion:
            payload = enumerate_to_first_exhaustion(args.n, args.reveal_policy)
        else:
            payload = analyze(
                args.n, args.include_reachable_subsets, args.reveal_policy
            )
    else:
        if args.first_exhaustion:
            parser.error("--first-exhaustion requires --n")
        payload = scan(args.scan_even_through, args.reveal_policy)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Regression checks for the exact TR26-043 v0 filtration enumerator."""

from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from math import comb
import unittest

from tr26_043_true_filtration import (
    analyze,
    enumerate_boundaries,
    enumerate_to_first_exhaustion,
    one_step_statistics,
    scan,
)


class TrueFiltrationEnumeratorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.results = {n: analyze(n) for n in range(2, 11, 2)}

    def test_exact_probability_mass(self) -> None:
        for n, result in self.results.items():
            self.assertEqual(result["probability_mass_by_step"], ["1/1"] * (n + 1))

    def test_state_invariants(self) -> None:
        for n in range(2, 11, 2):
            for level in enumerate_boundaries(n):
                self.assertEqual(
                    len(level), len({state.filtration_key() for state in level})
                )
                for state in level:
                    self.assertEqual(state.step, len(state.assigned_order))
                    self.assertEqual(state.height, sum(state.revealed[i] for i in state.assigned_order))
                    self.assertEqual(state.deviation, state.a - state.b)
                    self.assertEqual(len(set(state.assigned_order)), state.step)
                    self.assertTrue(all(state.revealed[i] != 0 for i in state.assigned_order))

    def test_smallest_counterexamples(self) -> None:
        result = scan(10)
        self.assertEqual(result["first_n"]["forced_probability"], 8)
        self.assertEqual(result["first_n"]["literal_martingale"], 2)
        self.assertEqual(result["first_n"]["active_martingale"], 4)
        self.assertEqual(result["first_n"]["strict_interior_martingale"], 6)

        minimal = scan(10, "minimal")
        self.assertEqual(minimal["first_n"]["forced_probability"], 10)
        self.assertEqual(minimal["first_n"]["literal_martingale"], 2)
        self.assertEqual(minimal["first_n"]["active_martingale"], 6)
        self.assertEqual(minimal["first_n"]["strict_interior_martingale"], 6)

    def test_maximum_forced_probability_small_n(self) -> None:
        expected = {
            2: "0/1",
            4: "0/1",
            6: "1/4",
            8: "1/3",
            10: "3/8",
        }
        for n, maximum in expected.items():
            self.assertEqual(self.results[n]["forced_probability"]["maximum"], maximum)

    def test_parametric_first_step_atom(self) -> None:
        # f(L1)=f(R1)=+1 and the first fair tie chooses L.
        for n in range(4, 11, 2):
            k = n // 2
            state = next(
                state
                for state in enumerate_boundaries(n)[1]
                if state.a == 1
                and state.b == 0
                and state.height == 1
                and state.revealed[0] == 1
                and state.revealed[k] == 1
            )
            self.assertEqual(
                state.probability, Fraction(k - 1, 4 * (2 * k - 1))
            )
            stats = one_step_statistics(state)
            self.assertEqual(
                stats["upward_probability"], Fraction(k - 2, 2 * k - 2)
            )
            self.assertEqual(
                stats["deviation_drift"], Fraction(k, 2 * k - 2)
            )

    def test_reachable_prefix_pair_counts(self) -> None:
        # Exhaustively, through n=10, every point in the two-prefix grid occurs.
        for n, result in self.results.items():
            k = n // 2
            expected_by_level = [
                min(t, k) - max(0, t - k) + 1 for t in range(n + 1)
            ]
            self.assertEqual(
                result["distinct_reachable_subsets_by_level"], expected_by_level
            )
            self.assertEqual(result["distinct_reachable_subsets_total"], (k + 1) ** 2)

    def test_first_exhaustion_distribution(self) -> None:
        result = enumerate_to_first_exhaustion(10)
        self.assertEqual(result["terminal_probability_mass"], "1/1")
        self.assertEqual(result["terminal_filtration_atoms"], 9664)
        self.assertEqual(
            result["residual_size_distribution"],
            {
                "1": "3679/16128",
                "2": "443/1792",
                "3": "1867/8064",
                "4": "11/56",
                "5": "65/672",
            },
        )
        self.assertEqual(result["odd_residual_probability"], "997/1792")
        self.assertEqual(result["distinct_probe_subsets_before_or_at_exhaustion"], 35)

        minimal = enumerate_to_first_exhaustion(10, "minimal")
        self.assertEqual(minimal["terminal_probability_mass"], "1/1")
        self.assertEqual(minimal["terminal_filtration_atoms"], 9488)
        self.assertEqual(
            minimal["residual_size_distribution"],
            result["residual_size_distribution"],
        )
        self.assertEqual(
            minimal["odd_residual_probability"], result["odd_residual_probability"]
        )
        self.assertEqual(
            minimal["distinct_probe_subsets_before_or_at_exhaustion"], 35
        )

    def test_independent_full_coloring_crosscheck(self) -> None:
        # A deliberately separate implementation enumerates complete balanced
        # colorings first, then groups trajectories by true-filtration atom.
        # This cross-checks the deferred-decisions arithmetic through n=8.
        expected = {
            2: (Fraction(0), 0),
            4: (Fraction(0), 0),
            6: (Fraction(1, 4), 0),
            8: (Fraction(1, 3), 4),
        }
        for n, target in expected.items():
            self.assertEqual(_brute_force_forced_summary(n), target)


def _brute_force_forced_summary(n: int) -> tuple[Fraction, int]:
    k = n // 2
    atom_mass: defaultdict[tuple, Fraction] = defaultdict(Fraction)
    upward_mass: defaultdict[tuple, Fraction] = defaultdict(Fraction)

    def recurse(
        coloring: tuple[int, ...],
        a: int,
        b: int,
        height: int,
        revealed: tuple[int, ...],
        tie_history: tuple[str, ...],
        assigned_order: tuple[int, ...],
        weight: Fraction,
    ) -> None:
        if a + b == n:
            return
        key = (a, b, height, revealed, tie_history, assigned_order)
        atom_mass[key] += weight
        left = a if a < k else None
        right = k + b if b < k else None
        revealed_next = list(revealed)
        for index in (left, right):
            if index is not None:
                revealed_next[index] = coloring[index]
        if left is None:
            choices = (("R", Fraction(1)),)
        elif right is None:
            choices = (("L", Fraction(1)),)
        else:
            left_abs = abs(height + coloring[left])
            right_abs = abs(height + coloring[right])
            if left_abs < right_abs:
                choices = (("L", Fraction(1)),)
            elif right_abs < left_abs:
                choices = (("R", Fraction(1)),)
            else:
                choices = (("L", Fraction(1, 2)), ("R", Fraction(1, 2)))
        for choice, coin_weight in choices:
            index = left if choice == "L" else right
            assert index is not None
            new_a = a + (choice == "L")
            new_b = b + (choice == "R")
            new_height = height + coloring[index]
            child_weight = weight * coin_weight
            if abs(new_height) == abs(height) + 1:
                upward_mass[key] += child_weight
            recurse(
                coloring,
                new_a,
                new_b,
                new_height,
                tuple(revealed_next),
                tie_history + ((choice,) if len(choices) == 2 else ()),
                assigned_order + (index,),
                child_weight,
            )

    coloring_weight = Fraction(1, comb(n, k))
    for plus_positions in combinations(range(n), k):
        plus_set = set(plus_positions)
        coloring = tuple(1 if i in plus_set else -1 for i in range(n))
        recurse(coloring, 0, 0, 0, (0,) * n, (), (), coloring_weight)

    eligible_values: list[Fraction] = []
    for key, denominator in atom_mass.items():
        a, b, height = key[:3]
        if a < k and b < k and abs(height) >= 1:
            eligible_values.append(upward_mass[key] / denominator)
    return (
        max(eligible_values, default=Fraction(0)),
        sum(value > Fraction(1, 4) for value in eligible_values),
    )


if __name__ == "__main__":
    unittest.main()

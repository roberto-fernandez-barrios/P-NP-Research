#!/usr/bin/env python3
"""Exact cut-generation search for N(10), with only subset selectors.

This formulation is structurally different from the Cycle-2 multicommodity
flow MILP.  Its master has one binary variable x_S per Boolean-lattice
subset.  Whenever a selected family has no compatible source-to-sink path
for a coloring P, let R be its currently reachable compatible vertices and
let B be the heads outside R of compatible edges leaving R.  Every feasible
family must select at least one member of B, so sum_{S in B} x_S >= 1 is a
valid separating inequality.  Reoptimizing after batches of these vertex-cut
inequalities is an exact finite method; a feasible optimum of a master whose
cuts are all valid is a global optimum.

Solver optimality metadata is computational evidence, not by itself an
independent lower-bound certificate.  A final family is independently
checkable directly from the definition, and every stored cut can also be
checked without SciPy.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


N10_LEVEL_MINIMA = [1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1]


def masks_of_weight(n: int, weight: int) -> list[int]:
    return [sum(1 << i for i in choice) for choice in combinations(range(n), weight)]


def compatible(subset: int, plus: int) -> bool:
    return abs(2 * (subset & plus).bit_count() - subset.bit_count()) <= 1


def quotient_colors(n: int) -> list[int]:
    return [plus for plus in masks_of_weight(n, n // 2) if plus & 1]


def reachable_and_boundary(
    n: int, family: set[int], plus: int
) -> tuple[set[int], tuple[int, ...]]:
    full = (1 << n) - 1
    assert 0 in family and compatible(0, plus)
    reachable = {0}
    for level in range(1, n + 1):
        for subset in masks_of_weight(n, level):
            if subset not in family or not compatible(subset, plus):
                continue
            if any((subset ^ (1 << i)) in reachable for i in range(n) if subset & (1 << i)):
                reachable.add(subset)
    if full in reachable:
        return reachable, ()

    boundary = set()
    for tail in reachable:
        for element in range(n):
            if tail & (1 << element):
                continue
            head = tail | (1 << element)
            if head not in reachable and compatible(head, plus):
                boundary.add(head)
    assert boundary and boundary.isdisjoint(family)
    return reachable, tuple(sorted(boundary))


def build_constraint(n: int, cuts: list[dict]) -> LinearConstraint:
    vertex_count = 1 << n
    row_indices: list[int] = []
    col_indices: list[int] = []
    data: list[float] = []
    lower: list[float] = []
    upper: list[float] = []

    def add(columns, lo: float, hi: float) -> None:
        row = len(lower)
        for column in columns:
            row_indices.append(row)
            col_indices.append(column)
            data.append(1.0)
        lower.append(lo)
        upper.append(hi)

    for level, minimum in enumerate(N10_LEVEL_MINIMA):
        add(
            (subset for subset in range(vertex_count) if subset.bit_count() == level),
            float(minimum),
            np.inf,
        )

    # Every feasible family has some maximal chain.  Relabeling its addition
    # order to 0,...,n-1 makes these canonical prefixes selected and merely
    # permutes the universally quantified balanced colorings.
    prefix = 0
    add((prefix,), 1.0, 1.0)
    for element in range(n):
        prefix |= 1 << element
        add((prefix,), 1.0, 1.0)

    for cut in cuts:
        add(cut["boundary_masks"], 1.0, np.inf)

    matrix = coo_matrix(
        (data, (row_indices, col_indices)),
        shape=(len(lower), vertex_count),
    ).tocsr()
    return LinearConstraint(matrix, np.asarray(lower), np.asarray(upper))


def witness_chain(n: int, family: set[int], plus: int) -> list[int] | None:
    parents = {0: None}
    for level in range(1, n + 1):
        for subset in masks_of_weight(n, level):
            if subset not in family or not compatible(subset, plus):
                continue
            for element in range(n):
                if not subset & (1 << element):
                    continue
                parent = subset ^ (1 << element)
                if parent in parents:
                    parents[subset] = parent
                    break
    full = (1 << n) - 1
    if full not in parents:
        return None
    chain = []
    current = full
    while current is not None:
        chain.append(current)
        current = parents[current]
    return list(reversed(chain))


def checkpoint_document(
    n: int,
    cuts: list[dict],
    family: list[int] | None,
    witnesses: list[dict],
    iterations: list[dict],
    completed: bool,
) -> dict:
    return {
        "schema": "balanced-chain-n10-benders-v1",
        "epistemic_status": (
            "FINITE COMPUTATIONAL SEARCH; FINAL FAMILY DIRECTLY CHECKABLE; "
            "SOLVER LOWER BOUND NOT INDEPENDENTLY CERTIFIED"
        ),
        "n": n,
        "method": "binary subset master with iterated compatible-DAG vertex cuts",
        "python_version": platform.python_version(),
        "scipy_version": scipy.__version__,
        "level_minima": N10_LEVEL_MINIMA,
        "canonical_chain_symmetry_breaking": True,
        "global_sign_quotient": True,
        "completed_with_feasible_master_optimum": completed,
        "family_masks": family,
        "all_signed_coloring_chain_witnesses": witnesses,
        "cuts": cuts,
        "iterations": iterations,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10, choices=[10])
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--max-iterations", type=int, default=10000)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("certificates/balanced_chain_n10/benders_search.json"),
    )
    args = parser.parse_args()
    n = args.n
    vertex_count = 1 << n
    colors = quotient_colors(n)
    cuts: list[dict] = []
    cut_keys: set[tuple[int, ...]] = set()
    iterations: list[dict] = []
    started = time.perf_counter()
    final_family: list[int] | None = None
    final_witnesses: list[dict] = []
    completed = False

    for iteration in range(args.max_iterations):
        elapsed = time.perf_counter() - started
        remaining = args.time_limit - elapsed
        if remaining <= 0:
            break
        constraint = build_constraint(n, cuts)
        result = milp(
            np.ones(vertex_count),
            integrality=np.ones(vertex_count, dtype=np.uint8),
            bounds=Bounds(np.zeros(vertex_count), np.ones(vertex_count)),
            constraints=constraint,
            options={"time_limit": remaining, "mip_rel_gap": 0.0},
        )
        if result.x is None:
            iterations.append(
                {
                    "iteration": iteration,
                    "status_code": int(result.status),
                    "status_message": result.message,
                    "incumbent": None,
                    "dual_bound": getattr(result, "mip_dual_bound", None),
                    "cuts_before": len(cuts),
                }
            )
            break
        family = {subset for subset, value in enumerate(result.x) if value > 0.5}
        failed = []
        new_cuts = 0
        for plus in colors:
            reachable, boundary = reachable_and_boundary(n, family, plus)
            if not boundary:
                continue
            failed.append(plus)
            if boundary in cut_keys:
                continue
            cut_keys.add(boundary)
            cuts.append(
                {
                    "plus_mask": plus,
                    "reachable_masks": sorted(reachable),
                    "boundary_masks": list(boundary),
                }
            )
            new_cuts += 1

        record = {
            "iteration": iteration,
            "status_code": int(result.status),
            "status_message": result.message,
            "master_objective": int(round(float(result.fun))),
            "master_dual_bound": float(result.mip_dual_bound),
            "master_relative_gap": float(result.mip_gap),
            "master_branch_and_bound_nodes": int(result.mip_node_count),
            "cuts_before": len(cuts) - new_cuts,
            "new_cuts": new_cuts,
            "failed_quotient_colorings": len(failed),
            "elapsed_seconds": time.perf_counter() - started,
        }
        iterations.append(record)
        print(
            f"iter={iteration} obj={record['master_objective']} "
            f"failed={len(failed)} new_cuts={new_cuts} total_cuts={len(cuts)} "
            f"seconds={record['elapsed_seconds']:.2f}",
            flush=True,
        )

        if result.status != 0 or result.mip_gap > 1e-9:
            break
        if not failed:
            final_family = sorted(family)
            # Serialize direct witnesses for all signed colorings, not only
            # the sign quotient used by the search.
            for plus in masks_of_weight(n, n // 2):
                chain = witness_chain(n, family, plus)
                assert chain is not None
                final_witnesses.append({"plus_mask": plus, "chain_masks": chain})
            completed = True
            break
        assert new_cuts > 0, "failed family generated no new separating cut"

        if iteration % 10 == 0:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(
                    checkpoint_document(
                        n, cuts, None, [], iterations, completed=False
                    ),
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(
            checkpoint_document(
                n, cuts, final_family, final_witnesses, iterations, completed
            ),
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        f"done completed={completed} iterations={len(iterations)} cuts={len(cuts)} "
        f"elapsed={time.perf_counter() - started:.2f}",
        flush=True,
    )


if __name__ == "__main__":
    main()

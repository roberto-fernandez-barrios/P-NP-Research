#!/usr/bin/env python3
"""Exact level-cover search for the n=10 balanced-chain problem.

This is Cycle-3 preprocessing, not a solver for N(10).  At level k it solves
the finite set-cover problem defining tau(10,k).  Solver lower bounds are
recorded separately from independently checkable upper-cover witnesses.
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


def masks_of_weight(n: int, weight: int) -> list[int]:
    return [sum(1 << i for i in choice) for choice in combinations(range(n), weight)]


def compatible(subset: int, plus: int) -> bool:
    return abs(2 * (subset & plus).bit_count() - subset.bit_count()) <= 1


def solve_level(n: int, level: int, time_limit: float) -> dict:
    candidates = masks_of_weight(n, level)
    # Global sign gives exactly the same compatibility column, so element 0
    # may be fixed positive for the search model.  The checker need not use it.
    colors = [p for p in masks_of_weight(n, n // 2) if p & 1]

    row_indices: list[int] = []
    col_indices: list[int] = []
    for row, plus in enumerate(colors):
        for column, subset in enumerate(candidates):
            if compatible(subset, plus):
                row_indices.append(row)
                col_indices.append(column)
    matrix = coo_matrix(
        (np.ones(len(row_indices)), (row_indices, col_indices)),
        shape=(len(colors), len(candidates)),
    ).tocsr()

    started = time.perf_counter()
    result = milp(
        np.ones(len(candidates)),
        integrality=np.ones(len(candidates), dtype=np.uint8),
        bounds=Bounds(np.zeros(len(candidates)), np.ones(len(candidates))),
        constraints=LinearConstraint(matrix, np.ones(len(colors)), np.full(len(colors), np.inf)),
        options={"time_limit": time_limit, "mip_rel_gap": 0.0},
    )
    elapsed = time.perf_counter() - started
    witness = [] if result.x is None else [
        subset for subset, value in zip(candidates, result.x) if value > 0.5
    ]
    return {
        "level": level,
        "candidate_count": len(candidates),
        "color_count_modulo_sign": len(colors),
        "status_code": int(result.status),
        "status_message": result.message,
        "incumbent": None if result.x is None else int(round(float(result.fun))),
        "dual_bound": None
        if getattr(result, "mip_dual_bound", None) is None
        else int(np.ceil(float(result.mip_dual_bound) - 1e-8)),
        "relative_gap": None
        if getattr(result, "mip_gap", None) is None
        else float(result.mip_gap),
        "branch_and_bound_nodes": None
        if getattr(result, "mip_node_count", None) is None
        else int(result.mip_node_count),
        "elapsed_seconds": elapsed,
        "cover_witness_masks": witness,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--levels", type=int, nargs="*")
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("certificates/balanced_chain_n10/level_cover_search.json"),
    )
    args = parser.parse_args()
    if args.n % 2:
        raise SystemExit("n must be even")
    levels = args.levels if args.levels is not None else list(range(args.n // 2 + 1))
    cases = [solve_level(args.n, level, args.time_limit) for level in levels]
    document = {
        "schema": "balanced-chain-level-cover-search-v1",
        "epistemic_status": "FINITE SOLVER COMPUTATION; CHECK WITNESSES INDEPENDENTLY",
        "n": args.n,
        "python_version": platform.python_version(),
        "scipy_version": scipy.__version__,
        "global_sign_quotient_in_search": True,
        "cases": cases,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    for case in cases:
        print(
            f"k={case['level']}: incumbent={case['incumbent']} "
            f"dual={case['dual_bound']} nodes={case['branch_and_bound_nodes']} "
            f"seconds={case['elapsed_seconds']:.3f}"
        )


if __name__ == "__main__":
    main()

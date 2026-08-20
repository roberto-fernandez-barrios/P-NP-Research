#!/usr/bin/env python3
"""Exact finite optimizer for 1-balanced-chain set systems.

This is the *search* implementation.  It uses a mixed-integer multicommodity
flow formulation and SciPy/HiGHS.  The logically independent standard-library
checker is ``check_balanced_chain_certificates.py``.

For a balanced coloring P (the set of +1 elements), a selected family X is
valid precisely when the Boolean-lattice DAG induced by

    |2 |S intersect P| - |S|| <= 1

contains a path from the empty set to [n].  Binary variables select lattice
vertices.  Continuous unit flows, one for each coloring modulo global sign,
certify the paths.  Since the graph is acyclic and a positive flow contains a
source-to-sink path, the flow variables need not be integral.

The canonical-prefix-chain constraints are valid symmetry breaking.  Every
feasible family contains a maximal chain (take a witness for any coloring).
Relabeling the elements in that chain order maps it to the canonical chain,
preserves family size, and permutes the set of balanced colorings.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Iterable

import numpy as np
import scipy
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix


# Independently certified by check_balanced_chain_certificates.py.  These are
# valid inequalities, not assumptions about the optimum of the full problem.
LEVEL_MINIMA = {
    2: [1, 1, 1],
    4: [1, 1, 2, 1, 1],
    6: [1, 1, 3, 2, 3, 1, 1],
    8: [1, 1, 4, 2, 3, 2, 4, 1, 1],
}


def subset_mask(elements: Iterable[int]) -> int:
    mask = 0
    for element in elements:
        mask |= 1 << element
    return mask


def elements(mask: int, n: int) -> list[int]:
    return [i for i in range(n) if (mask >> i) & 1]


def balanced_colorings(n: int, quotient_complement: bool) -> list[int]:
    ans = []
    for plus in combinations(range(n), n // 2):
        mask = subset_mask(plus)
        if not quotient_complement or (mask & 1):
            ans.append(mask)
    return ans


def compatible(subset: int, plus: int) -> bool:
    imbalance = 2 * (subset & plus).bit_count() - subset.bit_count()
    return abs(imbalance) <= 1


@dataclass(frozen=True)
class FlowEdge:
    color_index: int
    tail: int
    head: int


class SparseRows:
    def __init__(self) -> None:
        self.row_indices: list[int] = []
        self.col_indices: list[int] = []
        self.data: list[float] = []
        self.lower: list[float] = []
        self.upper: list[float] = []

    def add(
        self,
        terms: Iterable[tuple[int, float]],
        lower: float,
        upper: float,
    ) -> None:
        row = len(self.lower)
        for column, coefficient in terms:
            self.row_indices.append(row)
            self.col_indices.append(column)
            self.data.append(coefficient)
        self.lower.append(lower)
        self.upper.append(upper)

    def constraint(self, variable_count: int) -> LinearConstraint:
        matrix = coo_matrix(
            (self.data, (self.row_indices, self.col_indices)),
            shape=(len(self.lower), variable_count),
        ).tocsr()
        return LinearConstraint(
            matrix,
            np.asarray(self.lower, dtype=float),
            np.asarray(self.upper, dtype=float),
        )


def build_model(n: int):
    vertex_count = 1 << n
    full = vertex_count - 1
    # P and its complement define the same compatibility predicate.
    colors = balanced_colorings(n, quotient_complement=True)

    edges: list[FlowEdge] = []
    for color_index, plus in enumerate(colors):
        for tail in range(vertex_count):
            if not compatible(tail, plus):
                continue
            for element in range(n):
                if (tail >> element) & 1:
                    continue
                head = tail | (1 << element)
                if compatible(head, plus):
                    edges.append(FlowEdge(color_index, tail, head))

    variable_count = vertex_count + len(edges)
    objective = np.zeros(variable_count)
    objective[:vertex_count] = 1.0
    integrality = np.zeros(variable_count, dtype=np.uint8)
    integrality[:vertex_count] = 1
    rows = SparseRows()

    # A positive-flow edge can use only selected endpoint vertices.
    for edge_offset, edge in enumerate(edges):
        flow_var = vertex_count + edge_offset
        rows.add(((flow_var, 1.0), (edge.tail, -1.0)), -np.inf, 0.0)
        rows.add(((flow_var, 1.0), (edge.head, -1.0)), -np.inf, 0.0)

    incidence: dict[tuple[int, int], list[tuple[int, float]]] = {}
    for edge_offset, edge in enumerate(edges):
        flow_var = vertex_count + edge_offset
        incidence.setdefault((edge.color_index, edge.tail), []).append(
            (flow_var, 1.0)
        )
        incidence.setdefault((edge.color_index, edge.head), []).append(
            (flow_var, -1.0)
        )

    for color_index in range(len(colors)):
        for vertex in range(vertex_count):
            terms = incidence.get((color_index, vertex))
            if not terms:
                continue
            rhs = 1.0 if vertex == 0 else (-1.0 if vertex == full else 0.0)
            rows.add(terms, rhs, rhs)

    # Exact level-cover lower bounds strengthen the relaxation.  Their
    # exhaustive certificates are checked without SciPy by the second script.
    for level, minimum in enumerate(LEVEL_MINIMA[n]):
        rows.add(
            (
                (subset, 1.0)
                for subset in range(vertex_count)
                if subset.bit_count() == level
            ),
            float(minimum),
            np.inf,
        )

    # Valid S_n symmetry breaking: contain the canonical prefix chain.
    prefix = 0
    rows.add(((prefix, 1.0),), 1.0, 1.0)
    for element in range(n):
        prefix |= 1 << element
        rows.add(((prefix, 1.0),), 1.0, 1.0)

    return (
        colors,
        edges,
        objective,
        integrality,
        Bounds(np.zeros(variable_count), np.ones(variable_count)),
        rows.constraint(variable_count),
    )


def find_witness(n: int, family: set[int], plus: int):
    """Direct DFS used only to serialize explicit upper-bound witnesses."""
    full = (1 << n) - 1

    def visit(current: int, permutation: list[int], chain: list[int]):
        if current == full:
            return permutation, chain
        for element in range(n):
            if (current >> element) & 1:
                continue
            nxt = current | (1 << element)
            if nxt not in family or not compatible(nxt, plus):
                continue
            result = visit(nxt, permutation + [element], chain + [nxt])
            if result is not None:
                return result
        return None

    return visit(0, [], [0])


def certificate_for_family(n: int, family: list[int], solver_meta: dict) -> dict:
    family_set = set(family)
    witnesses = []
    for plus in balanced_colorings(n, quotient_complement=False):
        witness = find_witness(n, family_set, plus)
        if witness is None:
            raise RuntimeError(f"optimizer family misses coloring {plus}")
        permutation, chain = witness
        witnesses.append(
            {
                "plus_mask": plus,
                "plus_elements": elements(plus, n),
                "permutation": permutation,
                "chain_masks": chain,
            }
        )

    level_counts = [0] * (n + 1)
    for subset in family:
        level_counts[subset.bit_count()] += 1

    return {
        "schema": "balanced-chain-exact-v1",
        "epistemic_status": (
            "COMPUTATIONALLY VERIFIED; ADVERSARIALLY REVIEWED; "
            "UNFORMALIZED; NOVELTY STATUS RECORDED SEPARATELY"
        ),
        "n": n,
        "claimed_optimum": len(family),
        "family_masks": family,
        "family_elements": [elements(subset, n) for subset in family],
        "level_counts": level_counts,
        "all_balanced_coloring_witnesses": witnesses,
        "optimizer": solver_meta,
    }


def optimize(n: int, time_limit: float) -> tuple[list[int], dict]:
    (
        colors,
        edges,
        objective,
        integrality,
        bounds,
        constraint,
    ) = build_model(n)
    started = time.perf_counter()
    result = milp(
        objective,
        integrality=integrality,
        bounds=bounds,
        constraints=constraint,
        options={"time_limit": time_limit, "mip_rel_gap": 0.0},
    )
    elapsed = time.perf_counter() - started
    if result.x is None:
        raise RuntimeError(f"HiGHS returned no incumbent: {result.message}")
    if result.status != 0 or result.mip_gap > 1e-9:
        raise RuntimeError(
            "exact optimum not certified by optimizer: "
            f"status={result.status}, gap={result.mip_gap}, {result.message}"
        )

    vertex_count = 1 << n
    family = [
        subset for subset in range(vertex_count) if result.x[subset] > 0.5
    ]
    objective_value = int(round(float(result.fun)))
    dual_bound = int(round(float(result.mip_dual_bound)))
    if len(family) != objective_value or dual_bound != objective_value:
        raise RuntimeError("nonintegral or inconsistent optimum metadata")

    metadata = {
        "method": "SciPy milp / HiGHS multicommodity Boolean-lattice flow",
        "scipy_version": scipy.__version__,
        "python_version": platform.python_version(),
        "colorings_modulo_global_sign": len(colors),
        "flow_edges": len(edges),
        "variables": len(objective),
        "constraints": int(constraint.A.shape[0]),
        "canonical_chain_symmetry_breaking": True,
        "level_lower_bound_constraints": LEVEL_MINIMA[n],
        "status_code": int(result.status),
        "status_message": result.message,
        "objective": objective_value,
        "dual_bound": dual_bound,
        "relative_gap": float(result.mip_gap),
        "branch_and_bound_nodes": int(result.mip_node_count),
        "elapsed_seconds": elapsed,
    }
    return family, metadata


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--n",
        nargs="+",
        type=int,
        default=[2, 4, 6, 8],
        choices=sorted(LEVEL_MINIMA),
    )
    parser.add_argument("--time-limit", type=float, default=600.0)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("certificates/balanced_chain_exact"),
    )
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    for n in args.n:
        family, metadata = optimize(n, args.time_limit)
        certificate = certificate_for_family(n, family, metadata)
        target = args.output_dir / f"exact_n{n}.json"
        target.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
        print(
            f"n={n}: optimum={len(family)}, dual={metadata['dual_bound']}, "
            f"nodes={metadata['branch_and_bound_nodes']}, wrote {target}"
        )


if __name__ == "__main__":
    main()

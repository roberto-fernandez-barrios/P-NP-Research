#!/usr/bin/env python3
"""Direct SAT decision model for Cycle-3 n=10 balanced-chain bounds.

For each balanced coloring P modulo global sign and each compatible subset S,
the Boolean r[P,S] means that S is on a backward witness ending at [n].  The
clauses are

    r[P,[n]],
    r[P,S] -> x[S],
    r[P,S] -> OR_{i in S, S-i compatible} r[P,S-i].

Strictly decreasing cardinality makes these clauses equivalent to a selected
compatible maximal chain; no flow variables occur.  Exact per-level counts,
canonical-chain symmetry, and optional anchor pruning strengthen the model.

An UNSAT answer without a separately checked proof is computational evidence,
not a rigorous lower-bound certificate.  A SAT family is verified directly
and serialized with witnesses for all 252 signed colorings.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import threading
import time
from itertools import combinations
from pathlib import Path

import pysat
from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver


N = 10
FULL = (1 << N) - 1
LEVEL_MINIMA = [1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1]

# Independently supplied heuristic incumbent, used only as a phase hint after
# relabeling one of its witness chains to the canonical prefix chain.
SIZE35_INCUMBENT = [
    0, 64, 65, 66, 72, 80, 88, 90, 120, 122, 194, 202, 218, 219,
    378, 474, 506, 507, 576, 577, 579, 705, 706, 707, 715, 723, 731,
    739, 755, 763, 987, 1011, 1018, 1019, 1023,
]


def masks_of_weight(weight: int) -> list[int]:
    return [sum(1 << i for i in choice) for choice in combinations(range(N), weight)]


LEVELS = [masks_of_weight(level) for level in range(N + 1)]


def compatible(subset: int, plus: int) -> bool:
    return abs(2 * (subset & plus).bit_count() - subset.bit_count()) <= 1


def quotient_colors() -> list[int]:
    return [plus for plus in LEVELS[N // 2] if plus & 1]


def find_chain(family: set[int], plus: int) -> list[int] | None:
    parent = {0: None}
    for level in range(1, N + 1):
        for subset in LEVELS[level]:
            if subset not in family or not compatible(subset, plus):
                continue
            for element in range(N):
                if subset & (1 << element):
                    prior = subset ^ (1 << element)
                    if prior in parent:
                        parent[subset] = prior
                        break
    if FULL not in parent:
        return None
    chain = []
    current = FULL
    while current is not None:
        chain.append(current)
        current = parent[current]
    return list(reversed(chain))


def canonicalized_incumbent() -> set[int]:
    family = set(SIZE35_INCUMBENT)
    chain = find_chain(family, LEVELS[N // 2][0])
    if chain is None:
        # Choose any coloring; validity is checked again before use.
        for plus in LEVELS[N // 2]:
            chain = find_chain(family, plus)
            if chain is not None:
                break
    assert chain is not None
    additions = [(chain[i] ^ chain[i - 1]).bit_length() - 1 for i in range(1, N + 1)]
    old_to_new = {old: new for new, old in enumerate(additions)}

    def relabel(mask: int) -> int:
        ans = 0
        for old, new in old_to_new.items():
            if mask & (1 << old):
                ans |= 1 << new
        return ans

    transformed = {relabel(mask) for mask in family}
    prefix = 0
    assert prefix in transformed
    for element in range(N):
        prefix |= 1 << element
        assert prefix in transformed
    assert all(find_chain(transformed, plus) is not None for plus in LEVELS[N // 2])
    return transformed


def append_cardinality(
    cnf: CNF, vpool: IDPool, literals: list[int], bound: int, equality: bool
) -> None:
    encoded = (
        CardEnc.equals(literals, bound=bound, vpool=vpool, encoding=EncType.seqcounter)
        if equality
        else CardEnc.atmost(literals, bound=bound, vpool=vpool, encoding=EncType.seqcounter)
    )
    cnf.extend(encoded.clauses)


def build_formula(bound: int, extra_level: int | None, anchor_prune: bool):
    if extra_level is None:
        counts = LEVEL_MINIMA[:]
        assert bound == sum(counts)
    else:
        counts = LEVEL_MINIMA[:]
        counts[extra_level] += 1
        assert bound == sum(counts)
    assert counts[0] <= 1 and counts[N] <= 1

    # Subset S has selector variable S+1.
    xvar = [subset + 1 for subset in range(1 << N)]
    vpool = IDPool(start_from=(1 << N) + 1)
    cnf = CNF()

    # Exact level distributions are exhaustive for bound 33, and each chosen
    # extra_level is one branch of the bound-34 case split.
    for level, count in enumerate(counts):
        append_cardinality(cnf, vpool, [xvar[s] for s in LEVELS[level]], count, True)

    # Canonical-chain relabeling is valid for every feasible family.
    prefix = 0
    cnf.append([xvar[prefix]])
    for element in range(N):
        prefix |= 1 << element
        cnf.append([xvar[prefix]])

    # When levels 1 and 9 have their minimum count one, every selected state
    # of an inclusion-minimal feasible family lies between the unique anchors:
    # it contains 0 and omits 9.  For bound 33, inclusion-minimality follows
    # from the independently checked lower bound 33.  For a later bound-34
    # case this pruning may be used only after bound 33 has been refuted.
    anchor_prune_mode = "none"
    if anchor_prune:
        unique_lower = counts[1] == 1
        unique_upper = counts[9] == 1
        if unique_lower or unique_upper:
            for level in range(1, N):
                for subset in LEVELS[level]:
                    if (unique_lower and not (subset & 1)) or (
                        unique_upper and (subset & (1 << 9))
                    ):
                        cnf.append([-xvar[subset]])
            anchor_prune_mode = (
                "contain-0-and-omit-9" if unique_lower and unique_upper
                else ("contain-0" if unique_lower else "omit-9")
            )

    colors = quotient_colors()
    compatible_by_color_level: list[list[list[int]]] = []
    rvar: dict[tuple[int, int], int] = {}
    for color_index, plus in enumerate(colors):
        levels = []
        for level in range(N + 1):
            states = [subset for subset in LEVELS[level] if compatible(subset, plus)]
            levels.append(states)
            for subset in states:
                rvar[(color_index, subset)] = vpool.id(("r", color_index, subset))
        compatible_by_color_level.append(levels)

    for color_index, plus in enumerate(colors):
        cnf.append([rvar[(color_index, FULL)]])
        for level, states in enumerate(compatible_by_color_level[color_index]):
            # Redundant compatible-set cover clauses give strong propagation.
            cnf.append([xvar[subset] for subset in states])
            for subset in states:
                reach = rvar[(color_index, subset)]
                cnf.append([-reach, xvar[subset]])
                if level == 0:
                    continue
                parents = [
                    rvar[(color_index, subset ^ (1 << element))]
                    for element in range(N)
                    if subset & (1 << element)
                    and compatible(subset ^ (1 << element), plus)
                ]
                assert parents
                cnf.append([-reach, *parents])

    return cnf, vpool, xvar, counts, anchor_prune_mode


def formula_sha256(cnf: CNF) -> str:
    digest = hashlib.sha256()
    for clause in cnf.clauses:
        digest.update((" ".join(map(str, clause)) + " 0\n").encode("ascii"))
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bound", type=int, choices=[33, 34, 35], required=True)
    parser.add_argument(
        "--extra-level",
        type=int,
        choices=list(range(N + 1)),
        help="for bound 34: exact level receiving the single unit above minima",
    )
    parser.add_argument("--solver", default="cadical195")
    parser.add_argument("--time-limit", type=float, default=3600.0)
    parser.add_argument("--no-anchor-prune", action="store_true")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("certificates/balanced_chain_n10/sat_decision.json"),
    )
    args = parser.parse_args()
    if args.bound == 33 and args.extra_level is not None:
        raise SystemExit("bound 33 has no extra level")
    if args.bound == 34 and args.extra_level is None:
        raise SystemExit("bound 34 requires --extra-level")
    if args.bound == 35:
        raise SystemExit("use the independently checked size-35 upper certificate")

    cnf, vpool, xvar, counts, prune_mode = build_formula(
        args.bound, args.extra_level, not args.no_anchor_prune
    )
    cnf_hash = formula_sha256(cnf)
    started = time.perf_counter()
    solver = Solver(name=args.solver)
    solver.append_formula(cnf.clauses)

    incumbent = canonicalized_incumbent()
    phases = [xvar[s] if s in incumbent else -xvar[s] for s in range(1 << N)]
    solver.set_phases(phases)
    timer = threading.Timer(args.time_limit, solver.interrupt)
    timer.start()
    try:
        sat = solver.solve_limited(expect_interrupt=True)
    finally:
        timer.cancel()
    elapsed = time.perf_counter() - started
    stats = solver.accum_stats()
    family = None
    witnesses = []
    if sat is True:
        positive = set(literal for literal in solver.get_model() if literal > 0)
        family = [subset for subset in range(1 << N) if xvar[subset] in positive]
        family_set = set(family)
        assert len(family) == args.bound
        assert [sum(s.bit_count() == k for s in family) for k in range(N + 1)] == counts
        for plus in LEVELS[N // 2]:
            chain = find_chain(family_set, plus)
            assert chain is not None
            witnesses.append({"plus_mask": plus, "chain_masks": chain})

    document = {
        "schema": "balanced-chain-n10-direct-sat-v1",
        "epistemic_status": (
            "SAT FAMILY DIRECTLY CHECKABLE" if sat is True else
            "UNSAT IS SOLVER EVIDENCE ONLY; NO CHECKED PROOF" if sat is False else
            "INTERRUPTED COMPUTATION; NO DECISION"
        ),
        "n": N,
        "bound": args.bound,
        "extra_level": args.extra_level,
        "exact_level_counts": counts,
        "anchor_prune_mode": prune_mode,
        "solver": args.solver,
        "python_version": platform.python_version(),
        "python_sat_version": pysat.__version__,
        "variables": vpool.top,
        "clauses": len(cnf.clauses),
        "dimacs_clause_stream_sha256": cnf_hash,
        "result": "SAT" if sat is True else ("UNSAT" if sat is False else "UNKNOWN"),
        "elapsed_seconds": elapsed,
        "solver_stats": stats,
        "family_masks": family,
        "all_signed_coloring_chain_witnesses": witnesses,
        "proof_file": None,
    }
    solver.delete()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
    print(
        f"result={document['result']} bound={args.bound} extra={args.extra_level} "
        f"vars={document['variables']} clauses={document['clauses']} "
        f"seconds={elapsed:.3f} output={args.output}",
        flush=True,
    )


if __name__ == "__main__":
    main()

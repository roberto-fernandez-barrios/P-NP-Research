#!/usr/bin/env python3
"""Clean-room hostile validator for the Cycle-7 corner construction.

This implementation was written without consulting either prohibited Cycle-7
validator.  It works directly from the raw construction and uses exact integer
combinatorics throughout.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from collections import Counter, deque
from dataclasses import dataclass
from fractions import Fraction as Q
from pathlib import Path
from typing import Iterable, Iterator, Sequence


Clause = frozenset[int]  # DIMACS literals, variables are 1-based


@dataclass(frozen=True)
class Parameters:
    n: int
    m: int
    base: int
    jmax: int
    delta: int | None
    p: tuple[int, ...]
    s: tuple[int, ...]
    q: tuple[int, ...]


@dataclass
class Construction:
    params: Parameters
    children: tuple[tuple[int, int], ...]
    adjacency: tuple[frozenset[int], ...]


def _is_adjacent_mod_n(x: int, y: int, n: int) -> bool:
    return (x - y) % n in (1, n - 1)


def make_parameters(n: int, m: int) -> Parameters:
    if n < 3:
        raise ValueError("n must be at least 3")
    if not (0 <= m <= n // 10):
        raise ValueError("need 0 <= m <= floor(n/10)")
    base = n // 3 + 1
    jmax = (n - 3) // 2
    if m == 0:
        return Parameters(n, m, base, jmax, None, (), (), ())

    p = tuple((i * n) // m for i in range(m))
    s = tuple((x - base) % n for x in p)
    pset, sset = set(p), set(s)
    upper = min(n // m - 2, jmax - base)
    chosen: tuple[int, tuple[int, ...]] | None = None
    for d in range(2, upper + 1):
        q = tuple((x + d) % n for x in p)
        qset = set(q)
        if qset & pset:
            continue
        if qset & sset:
            continue
        if any((x - 1) % n in sset or (x + 1) % n in sset for x in q):
            continue
        chosen = (d, q)
        break
    if chosen is None:
        raise ValueError(
            f"no admissible delta for n={n}, m={m}, interval=[2,{upper}]"
        )
    d, q = chosen
    return Parameters(n, m, base, jmax, d, p, s, q)


def construct(n: int, m: int) -> Construction:
    par = make_parameters(n, m)
    exceptional = dict(zip(par.s, par.q))
    children: list[tuple[int, int]] = []
    adjacency = [set() for _ in range(n)]
    for x in range(n):
        pair = ((x + 1) % n, exceptional.get(x, (x + par.base) % n))
        children.append(pair)
        for y in pair:
            adjacency[x].add(y)
            adjacency[y].add(x)
    return Construction(
        par,
        tuple(children),
        tuple(frozenset(neighbors) for neighbors in adjacency),
    )


def construct_from_g(n: int, m: int, g: Sequence[int]) -> Construction:
    """Build the graph from an externally supplied second-child map.

    This adapter is used only for post-clean-room comparison with stored
    certificates.  It does not assume that the stored map came from the final
    raw parameterization.
    """
    if len(g) != n or any(not (0 <= y < n) for y in g):
        raise ValueError("g must contain exactly n residues in [0,n)")
    base = n // 3 + 1
    par = Parameters(n, m, base, (n - 3) // 2, None, (), (), ())
    children = tuple(((x + 1) % n, int(g[x])) for x in range(n))
    adjacency = [set() for _ in range(n)]
    for x, pair in enumerate(children):
        for y in pair:
            adjacency[x].add(y)
            adjacency[y].add(x)
    return Construction(par, children, tuple(frozenset(a) for a in adjacency))


def degree_data(cons: Construction) -> dict[str, object]:
    n = cons.params.n
    indeg = [0] * n
    out_distinct = True
    loops: list[tuple[int, int]] = []
    for x, pair in enumerate(cons.children):
        out_distinct &= len(set(pair)) == 2
        for y in pair:
            indeg[y] += 1
            if x == y:
                loops.append((x, y))
    return {
        "indegrees": indeg,
        "indegree_histogram": dict(sorted(Counter(indeg).items())),
        "outdegree_two_distinct": out_distinct,
        "loops": loops,
        "max_undirected_degree": max(map(len, cons.adjacency)),
    }


def critical_clauses(cons: Construction) -> set[Clause]:
    clauses: set[Clause] = set()
    for x, (y, z) in enumerate(cons.children):
        clauses.add(frozenset((x + 1, -(y + 1), -(z + 1))))
    return clauses


def auxiliary_clauses(cons: Construction, variant: str) -> set[Clause]:
    n = cons.params.n
    clauses: set[Clause] = set()
    if variant == "pairs":
        for a, b in itertools.combinations(range(n), 2):
            if b not in cons.adjacency[a]:
                clauses.add(frozenset((a + 1, b + 1)))
    elif variant == "triples":
        for a, b, c in itertools.combinations(range(n), 3):
            if (
                b not in cons.adjacency[a]
                and c not in cons.adjacency[a]
                and c not in cons.adjacency[b]
            ):
                clauses.add(frozenset((a + 1, b + 1, c + 1)))
    else:
        raise ValueError("variant must be pairs or triples")
    return clauses


def formula(cons: Construction, variant: str) -> set[Clause]:
    return critical_clauses(cons) | auxiliary_clauses(cons, variant)


def _tautological(clause: Iterable[int]) -> bool:
    lits = set(clause)
    return any(-lit in lits for lit in lits)


def resolvents_width_at_most(
    clauses: set[Clause],
    *,
    parent_mode: str = "at_most_three",
    max_result_width: int = 3,
) -> tuple[set[Clause], dict[Clause, tuple[Clause, Clause, int]]]:
    """All non-tautological one-pivot resolvents of bounded width.

    `parent_mode` is either `exact_three` or `at_most_three`.  Unit and
    binary results are retained: this lets the caller separately impose an
    exact-three-result reading if desired.
    """
    if parent_mode == "exact_three":
        parents = [c for c in clauses if len(c) == 3]
    elif parent_mode == "at_most_three":
        parents = [c for c in clauses if len(c) <= 3]
    else:
        raise ValueError("bad parent mode")

    pos: dict[int, list[Clause]] = {}
    neg: dict[int, list[Clause]] = {}
    for clause in parents:
        for lit in clause:
            (pos if lit > 0 else neg).setdefault(abs(lit), []).append(clause)

    results: set[Clause] = set()
    witness: dict[Clause, tuple[Clause, Clause, int]] = {}
    for v in sorted(set(pos) & set(neg)):
        for cp in pos[v]:
            for cn in neg[v]:
                merged = (set(cp) - {v}) | (set(cn) - {-v})
                if _tautological(merged) or len(merged) > max_result_width:
                    continue
                resolvent = frozenset(merged)
                results.add(resolvent)
                witness.setdefault(resolvent, (cp, cn, v))
    return results, witness


def closure(
    initial: set[Clause],
    *,
    parent_mode: str,
    result_mode: str = "at_most_three",
    iterative: bool = False,
    max_rounds: int = 100,
    max_clauses: int = 2_000_000,
) -> tuple[set[Clause], list[int]]:
    current = set(initial)
    additions_by_round: list[int] = []
    for _ in range(max_rounds):
        inferred, _ = resolvents_width_at_most(
            current, parent_mode=parent_mode, max_result_width=3
        )
        if result_mode == "exact_three":
            inferred = {c for c in inferred if len(c) == 3}
        elif result_mode != "at_most_three":
            raise ValueError("bad result mode")
        new = inferred - current
        additions_by_round.append(len(new))
        current |= new
        if len(current) > max_clauses:
            raise RuntimeError("closure clause cap exceeded")
        if not iterative or not new:
            break
    else:
        raise RuntimeError("closure round cap exceeded")
    return current, additions_by_round


def critical_clause_counts(clauses: Iterable[Clause], n: int) -> list[int]:
    counts = [0] * n
    for clause in clauses:
        positives = [lit for lit in clause if lit > 0]
        if len(positives) == 1:
            counts[positives[0] - 1] += 1
    return counts


def undirected_triangles(cons: Construction) -> list[tuple[int, int, int]]:
    ans: list[tuple[int, int, int]] = []
    for a in range(cons.params.n):
        for b in (x for x in cons.adjacency[a] if x > a):
            for c in cons.adjacency[a] & cons.adjacency[b]:
                if c > b:
                    ans.append((a, b, c))
    return ans


def directed_two_cycles(cons: Construction) -> list[tuple[int, int]]:
    out = [set(pair) for pair in cons.children]
    return [
        (x, y)
        for x in range(cons.params.n)
        for y in out[x]
        if x < y and x in out[y]
    ]


def critical_overlap_defects(cons: Construction) -> list[tuple[int, int, str]]:
    """Coincidences that could shrink a critical-critical resolvent."""
    defects: list[tuple[int, int, str]] = []
    out = [set(pair) for pair in cons.children]
    for u, pair in enumerate(cons.children):
        for x in pair:
            other = pair[1] if pair[0] == x else pair[0]
            if u in out[x]:
                defects.append((u, x, "directed-two-cycle/tautology"))
            if other in out[x]:
                defects.append((u, x, "shared-child/triangle"))
    return defects


def directed_girth(cons: Construction) -> int | None:
    n = cons.params.n
    best = n + 1
    for start in range(n):
        dist = [-1] * n
        dist[start] = 0
        todo: deque[int] = deque((start,))
        while todo:
            x = todo.popleft()
            if dist[x] + 1 >= best:
                continue
            for y in cons.children[x]:
                if y == start:
                    best = min(best, dist[x] + 1)
                elif dist[y] == -1:
                    dist[y] = dist[x] + 1
                    todo.append(y)
    return None if best == n + 1 else best


def _cycle_key(cycle: Sequence[int]) -> tuple[int, ...]:
    cycle = tuple(cycle)
    rotations = [cycle[i:] + cycle[:i] for i in range(len(cycle))]
    return min(rotations)


def directed_cycles_up_to(cons: Construction, max_length: int) -> set[tuple[int, ...]]:
    cycles: set[tuple[int, ...]] = set()
    n = cons.params.n
    for start in range(n):
        path = [start]
        used = {start}

        def visit(x: int) -> None:
            if len(path) > max_length:
                return
            for y in cons.children[x]:
                if y == start:
                    cycles.add(_cycle_key(path))
                elif y not in used and len(path) < max_length:
                    used.add(y)
                    path.append(y)
                    visit(y)
                    path.pop()
                    used.remove(y)

        visit(start)
    return cycles


def independent_triple(
    vertices: Iterable[int], adjacency: Sequence[frozenset[int]]
) -> tuple[int, int, int] | None:
    for a, b, c in itertools.combinations(sorted(vertices), 3):
        if b not in adjacency[a] and c not in adjacency[a] and c not in adjacency[b]:
            return a, b, c
    return None


def nonedge_pair(
    vertices: Iterable[int], adjacency: Sequence[frozenset[int]]
) -> tuple[int, int] | None:
    for a, b in itertools.combinations(sorted(vertices), 2):
        if b not in adjacency[a]:
            return a, b
    return None


def uniqueness_cycle_certificate(cons: Construction, variant: str) -> dict[str, object]:
    delta = max(map(len, cons.adjacency))
    if variant == "triples":
        # If alpha <= 2 and max degree is Delta, greedy coloring bounds a
        # dangerous cycle by 2(Delta+1) vertices.
        bound = 2 * (delta + 1)
        forbidden = lambda vertices: independent_triple(vertices, cons.adjacency)
    elif variant == "pairs":
        # A dangerous cycle must be a clique and hence has <= Delta+1 vertices.
        bound = delta + 1
        forbidden = lambda vertices: nonedge_pair(vertices, cons.adjacency)
    else:
        raise ValueError("bad variant")

    # Search only paths that are still dangerous.  A path containing an
    # independent triple/nonedge pair can never become a dangerous cycle, so
    # pruning it is exact and dramatically faster than enumerating every
    # binary directed path of length 12.
    bad_set: set[tuple[int, ...]] = set()
    n = cons.params.n
    for start in range(n):
        path = [start]
        used = {start}

        def visit(x: int) -> None:
            for y in cons.children[x]:
                if y == start:
                    bad_set.add(tuple(path))
                elif (
                    y > start
                    and y not in used
                    and len(path) < bound
                    and forbidden(path + [y]) is None
                ):
                    used.add(y)
                    path.append(y)
                    visit(y)
                    path.pop()
                    used.remove(y)

        visit(start)
    bad = list(bad_set)
    bad.sort(key=lambda c: (len(c), c))
    return {
        "cycle_search_bound": bound,
        "dangerous_cycle_count": len(bad),
        "smallest_dangerous_cycle": list(bad[0]) if bad else None,
        "unique": not bad,
    }


def brute_force_uniqueness(cons: Construction, variant: str) -> dict[str, object]:
    """Independent all-subsets check, intended only for small n."""
    n = cons.params.n
    if n > 24:
        raise ValueError("brute-force subset checker limited to n<=24")
    for mask in range(1, 1 << n):
        zeros = [x for x in range(n) if mask >> x & 1]
        zset = set(zeros)
        if any(not (set(cons.children[x]) & zset) for x in zeros):
            continue
        if variant == "pairs":
            forbidden = nonedge_pair(zeros, cons.adjacency)
        else:
            forbidden = independent_triple(zeros, cons.adjacency)
        if forbidden is None:
            return {"unique": False, "second_zero_set": zeros}
    return {"unique": True, "second_zero_set": None}


def beatty_difference_property(n: int, m: int) -> bool:
    if m == 0:
        return True
    p = [(i * n) // m for i in range(m)]
    for i in range(m):
        for k in range(m):
            diff = (p[(i + k) % m] - p[i]) % n
            lo = (k * n) // m
            hi = (k * n + m - 1) // m
            if diff not in (lo % n, hi % n):
                return False
    return True


def forbidden_d_values(n: int, m: int) -> tuple[set[int], int]:
    if m == 0:
        return set(), 0
    base = n // 3 + 1
    jmax = (n - 3) // 2
    p = {(i * n) // m for i in range(m)}
    s = {(x - base) % n for x in p}
    upper = min(n // m - 2, jmax - base)
    bad: set[int] = set()
    for d in range(2, upper + 1):
        q = {(x + d) % n for x in p}
        if q & p or q & s or any((x - 1) % n in s or (x + 1) % n in s for x in q):
            bad.add(d)
    return bad, upper


def instance_report(n: int, m: int, *, closure_checks: bool = True) -> dict[str, object]:
    cons = construct(n, m)
    deg = degree_data(cons)
    report: dict[str, object] = {
        "n": n,
        "m": m,
        "base": cons.params.base,
        "jmax": cons.params.jmax,
        "delta": cons.params.delta,
        "P": list(cons.params.p),
        "S": list(cons.params.s),
        "Q": list(cons.params.q),
        "degree_histogram": deg["indegree_histogram"],
        "outdegree_two_distinct": deg["outdegree_two_distinct"],
        "loops": deg["loops"],
        "max_undirected_degree": deg["max_undirected_degree"],
        "directed_two_cycles": directed_two_cycles(cons),
        "undirected_triangle_count": len(undirected_triangles(cons)),
        "directed_girth": directed_girth(cons),
        "pairs_uniqueness": uniqueness_cycle_certificate(cons, "pairs"),
        "triples_uniqueness": uniqueness_cycle_certificate(cons, "triples"),
    }
    if n <= 24:
        report["pairs_bruteforce"] = brute_force_uniqueness(cons, "pairs")
        report["triples_bruteforce"] = brute_force_uniqueness(cons, "triples")

    if closure_checks:
        closure_data: dict[str, object] = {}
        for variant in ("pairs", "triples"):
            f = formula(cons, variant)
            vdata: dict[str, object] = {"initial_clause_count": len(f)}
            for parent_mode in ("exact_three", "at_most_three"):
                one, rounds = closure(
                    f,
                    parent_mode=parent_mode,
                    result_mode="at_most_three",
                    iterative=False,
                )
                counts = critical_clause_counts(one, n)
                vdata[f"one_round_{parent_mode}"] = {
                    "new_clause_count": len(one - f),
                    "new_width_histogram": dict(Counter(map(len, one - f))),
                    "critical_count_histogram": dict(Counter(counts)),
                    "two_cc": [x for x, count in enumerate(counts) if count >= 2],
                    "rounds": rounds,
                }
                if variant == "triples":
                    fixed, fixed_rounds = closure(
                        f,
                        parent_mode=parent_mode,
                        result_mode="at_most_three",
                        iterative=True,
                    )
                    fixed_counts = critical_clause_counts(fixed, n)
                    vdata[f"fixpoint_{parent_mode}"] = {
                        "new_clause_count": len(fixed - f),
                        "critical_count_histogram": dict(Counter(fixed_counts)),
                        "two_cc": [
                            x for x, count in enumerate(fixed_counts) if count >= 2
                        ],
                        "rounds": fixed_rounds,
                    }
            closure_data[variant] = vdata
        report["closure"] = closure_data
    return report


def fresh_suite() -> dict[str, object]:
    """Deterministic tests selected before opening stored Cycle-7 instances."""
    parameter_failures: list[dict[str, object]] = []
    smallest_missing_delta: dict[str, int] | None = None
    max_delta = -1
    max_delta_at: list[int] | None = None
    beatty_failures: list[list[int]] = []
    parameter_case_count = 0

    # Exhaust all theorem-range m for n through 1200.  This is deliberately
    # independent of the stored 21-instance selection.
    for n in range(10, 1201):
        for m in range(1, n // 10 + 1):
            parameter_case_count += 1
            if n <= 220 and not beatty_difference_property(n, m):
                beatty_failures.append([n, m])
            try:
                par = make_parameters(n, m)
            except ValueError as exc:
                if smallest_missing_delta is None:
                    smallest_missing_delta = {"n": n, "m": m}
                parameter_failures.append({"n": n, "m": m, "error": str(exc)})
                continue
            assert par.delta is not None
            if par.delta > max_delta:
                max_delta = par.delta
                max_delta_at = [n, m]

    small_recipe_failures: list[dict[str, object]] = []
    small_property_failures: list[dict[str, object]] = []
    for n in range(3, 28):
        for m in range(0, n // 10 + 1):
            try:
                cons = construct(n, m)
            except ValueError as exc:
                small_recipe_failures.append({"n": n, "m": m, "error": str(exc)})
                continue
            deg = degree_data(cons)
            issues: list[str] = []
            if deg["loops"]:
                issues.append("loop")
            if not deg["outdegree_two_distinct"]:
                issues.append("out-neighbor collision")
            if not uniqueness_cycle_certificate(cons, "pairs")["unique"]:
                issues.append("pairs non-unique")
            if not uniqueness_cycle_certificate(cons, "triples")["unique"]:
                issues.append("triples non-unique")
            if issues:
                small_property_failures.append({"n": n, "m": m, "issues": issues})

    structural_recipe_failures: list[dict[str, object]] = []
    structural_property_failures: list[dict[str, object]] = []
    structural_count = 0
    # All m from the original finite-search threshold through n=220, plus
    # sparse/dense/mid samples to n=2000.
    cases: set[tuple[int, int]] = set()
    for n in range(26, 221):
        cases.update((n, m) for m in range(0, n // 10 + 1))
    for n in range(225, 2001, 25):
        choices = {0, 1, 2, n // 20, max(0, n // 10 - 1), n // 10}
        cases.update((n, m) for m in choices if 0 <= m <= n // 10)

    for n, m in sorted(cases):
        try:
            cons = construct(n, m)
        except ValueError as exc:
            structural_recipe_failures.append(
                {"n": n, "m": m, "kind": "parameters", "error": str(exc)}
            )
            continue
        structural_count += 1
        deg = degree_data(cons)
        expected = {1: m, 2: n - 2 * m, 3: m} if m else {2: n}
        hist = {int(k): int(v) for k, v in deg["indegree_histogram"].items()}
        checks = {
            "degree_histogram": hist == expected,
            "outdegree": bool(deg["outdegree_two_distinct"]),
            "no_loops": not deg["loops"],
            "max_degree": int(deg["max_undirected_degree"]) <= 5,
            "no_directed_two_cycles": not directed_two_cycles(cons),
            "triangle_free": not undirected_triangles(cons),
            "no_critical_resolvent_overlap": not critical_overlap_defects(cons),
            "pairs_unique": uniqueness_cycle_certificate(cons, "pairs")["unique"],
            "triples_unique": uniqueness_cycle_certificate(cons, "triples")["unique"],
        }
        if not all(checks.values()):
            structural_property_failures.append({"n": n, "m": m, "checks": checks})

    # Full closure checks are cubic in n for triples.  Use a predeclared grid
    # spanning edge cases and theorem-scale instances.
    closure_cases = [
        (28, 0), (28, 1), (30, 3), (40, 1), (40, 4), (50, 3), (50, 5),
        (61, 1), (61, 6), (75, 4), (75, 7), (100, 6), (100, 10),
        (127, 1), (127, 12),
    ]
    closure_reports: list[dict[str, object]] = []
    for n, m in closure_cases:
        closure_reports.append(instance_report(n, m, closure_checks=True))

    result = {
        "implementation": "cr_cleanroom_validator.py",
        "implementation_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "parameter_scan": {
            "range": "all 10<=n<=1200 and 1<=m<=floor(n/10)",
            "case_count": parameter_case_count,
            "failure_count": len(parameter_failures),
            "failures": parameter_failures,
            "failures_with_n_at_least_26": [
                f for f in parameter_failures if int(f["n"]) >= 26
            ],
            "failures_with_n_at_least_28": [
                f for f in parameter_failures if int(f["n"]) >= 28
            ],
            "smallest_missing_delta": smallest_missing_delta,
            "max_delta": max_delta,
            "max_delta_at": max_delta_at,
            "beatty_failure_count_for_n_le_220": len(beatty_failures),
            "beatty_failures": beatty_failures,
        },
        "structural_scan": {
            "case_count": structural_count,
            "case_description": "all constructible m for 26<=n<=220; six density samples every 25 through n=2000",
            "recipe_failure_count": len(structural_recipe_failures),
            "recipe_failures": structural_recipe_failures,
            "property_failure_count": len(structural_property_failures),
            "property_failures": structural_property_failures,
        },
        "small_n_diagnostic": {
            "range": "all 3<=n<=27 and 0<=m<=floor(n/10)",
            "recipe_failures": small_recipe_failures,
            "property_failures": small_property_failures,
        },
        "closure_cases": closure_reports,
    }
    return result


def stored_suite(path: Path) -> dict[str, object]:
    # Preserve every JSON decimal as the exact rational denoted by its text.
    # The stored metadata is rounded, so compare it to the independently
    # counted statistic with an exact rational tolerance below.
    data = json.loads(path.read_text(encoding="utf-8"), parse_float=Q)
    reports: list[dict[str, object]] = []
    pass_count = 0
    for index, record in enumerate(data["instances"]):
        n = int(record["n"])
        m = int(record["m1"])
        variant_label = str(record["variant"])
        variant = "triples" if variant_label.startswith("triples") else "pairs"
        cons = construct_from_g(n, m, record["g"])
        deg = degree_data(cons)
        unique = uniqueness_cycle_certificate(cons, variant)
        f = formula(cons, variant)
        one, rounds = closure(
            f,
            parent_mode="at_most_three",
            result_mode="at_most_three",
            iterative=False,
        )
        counts = critical_clause_counts(one, n)
        raw_match: bool | None
        try:
            raw = construct(n, m)
            raw_match = [z for _, z in raw.children] == list(record["g"])
        except ValueError:
            raw_match = None
        expected_stats = [Q(0), Q(m, n), Q(0)]
        claimed_stats = [Q(x) for x in record["stats"]]
        checks = {
            "g_well_formed": len(record["g"]) == n
            and all(0 <= int(y) < n for y in record["g"]),
            "outdegree_two_distinct": bool(deg["outdegree_two_distinct"]),
            "no_loops": not deg["loops"],
            "no_indegree_zero": 0 not in deg["indegrees"],
            "exactly_m_indegree_one": deg["indegrees"].count(1) == m,
            "unique": bool(unique["unique"]),
            "one_round_twocc_empty": all(count == 1 for count in counts),
            "stats_match_metadata": all(
                abs(a - b) <= Q(1, 10**15)
                for a, b in zip(claimed_stats, expected_stats)
            ),
        }
        if variant == "triples":
            fixed, fixed_rounds = closure(
                f,
                parent_mode="at_most_three",
                result_mode="at_most_three",
                iterative=True,
            )
            fixed_counts = critical_clause_counts(fixed, n)
            checks["zero_width_le_three_resolvents"] = len(one - f) == 0
            checks["fixpoint_twocc_empty"] = all(count == 1 for count in fixed_counts)
        else:
            fixed_rounds = []
        passed = all(checks.values())
        pass_count += int(passed)
        reports.append(
            {
                "index": index,
                "n": n,
                "m": m,
                "variant": variant_label,
                "matches_final_raw_construction": raw_match,
                "degree_histogram": deg["indegree_histogram"],
                "directed_girth": directed_girth(cons),
                "undirected_triangle_count": len(undirected_triangles(cons)),
                "one_round_new_clause_count": len(one - f),
                "one_round_rounds": rounds,
                "fixpoint_rounds": fixed_rounds,
                "checks": checks,
                "passed": passed,
            }
        )
    return {
        "certificate_path": str(path),
        "certificate_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "instance_count": len(reports),
        "pass_count": pass_count,
        "reports": reports,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    inst = sub.add_parser("instance")
    inst.add_argument("n", type=int)
    inst.add_argument("m", type=int)
    inst.add_argument("--no-closure", action="store_true")
    sub.add_parser("fresh-suite")
    stored = sub.add_parser("stored-suite")
    stored.add_argument("path", type=Path)
    args = parser.parse_args()

    if args.command == "instance":
        result = instance_report(args.n, args.m, closure_checks=not args.no_closure)
    elif args.command == "fresh-suite":
        result = fresh_suite()
    else:
        result = stored_suite(args.path)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

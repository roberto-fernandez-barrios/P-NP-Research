#!/usr/bin/env python3
"""Cycle 7 Stage I - corner-realizability family: constructor + verifier.

Claim under test (Theorem CR, research_cycle_07/corner_realizability.md):
for every large n and every m1 in {0,...,floor(n/3)}, there is a uniquely
satisfiable 3-CNF F_n (width <= 3; a width-exactly-3 variant also exists)
with, for its forced (unique) canonical selection:
    TwoCC(F-tilde) = 0,  |J_0| = 0,  |J_1| = m1,
hence statistics (i_0, i_1, tau) = (0, m1/n, 0).  With m1 = round(i1* n),
i1* = 0.060043244708778326... (the [JC26] LP corner), the corner is
realizable to within 1/(2n) in i_1, exactly in i_0 and tau.

This script CONSTRUCTS the instances and VERIFIES every claimed property
by direct computation (no step of the construction proof is trusted):
  V1  syntactic: each variable has exactly one critical clause in F, of
      width exactly 3 with distinct negated variables; aux clauses are
      all-positive (their non-adjacency is by construction; the
      load-bearing consequences are verified directly by V3/V4).
  V2  alpha = 1^n satisfies F.
  V3  unique satisfiability: for every variable x, F with x=0 is UNSAT
      (complete DPLL with unit propagation; independent of the closed-set
      theory used in the paper proof).
  V4  F-tilde: all width-<=3 non-tautological resolvents from pairs of
      clauses of F, under BOTH readings of Definition 31 ("3-clauses" =
      width exactly 3 parents / width <= 3 parents); collect critical
      clauses per variable; verify every variable still has EXACTLY ONE
      critical clause in F-tilde => TwoCC = empty set under both readings.
  V5  degrees: indegree profile: no indegree-0; exactly m1 indegree-1;
      report full profile and the statistics (i_0, i_1, tau).
  V6  structural side conditions used by the paper proof (reported, not
      load-bearing given V3/V4): no 2-cycles, overlap-freeness, directed
      girth.

Exit 0 iff all verifications pass for all tested (n, m1, variant).
"""

import sys, time
from itertools import combinations

I1_STAR = 0.060043244708778326  # float only used to pick integer m1 targets

def build_explicit(n, m1):
    """Fully explicit g (matches the Theorem-CR proof; no search):
    g(x) = x + base, EXCEPT for i < m1: g(s_i) = q_i, where
    p_i = floor(i*n/m1) (spread), s_i = p_i - base, delta = max(2, n//(3*max(m1,1)))
    capped so base+delta <= jmax, q_i = p_i + delta.
    Then indegree(p_i) = 1 (W), indegree(q_i) = 3 (W'), all else 2."""
    base = n // 3 + 1
    jmax = (n - 3) // 2
    if m1 == 0:
        g = {x: (x + base) % n for x in range(n)}
        return g
    P = [(i * n) // m1 % n for i in range(m1)]
    assert len(set(P)) == m1
    spacing = n // m1
    S = set((p - base) % n for p in P)
    delta = None
    for d in range(2, min(spacing - 1, jmax - base + 1)):
        Q = set((p + d) % n for p in P)
        # forbid: q in W (would collide with an indegree-1 target), q a special
        # source (would chain two long jumps: the n=80 delta=5 resonance),
        # q adjacent to a special source (keeps the overlap checks clean)
        if Q & set(P) or Q & S:
            continue
        if any(((q - 1) % n) in S or ((q + 1) % n) in S for q in Q):
            continue
        delta = d
        break
    assert delta is not None, f"n={n}, m1={m1}: no collision-free displacement"
    g = {x: (x + base) % n for x in range(n)}
    for p in P:
        s = (p - base) % n
        g[s] = (p + delta) % n
    return g

def build(n, m1, variant, jump_width=None):
    """Return (clauses, arcs, g) or raise on construction failure.
    Arcs: x -> x+1 (mod n) and x -> g(x).  Capacity: W = indeg-1 targets
    (no g-preimage), Wp = indeg-3 targets (two g-preimages), rest one.
    variant 'pairs-explicit' / 'triples-explicit' use the search-free
    explicit g of build_explicit (the Theorem-CR construction)."""
    assert 0 <= 2 * m1 <= n
    if variant.endswith("-explicit"):
        g = build_explicit(n, m1)
        arcs = {x: ((x + 1) % n, g[x]) for x in range(n)}
        clauses = []
        for x in range(n):
            y, z = arcs[x]
            assert y != z and x not in (y, z)
            clauses.append((x + 1, -(y + 1), -(z + 1)))
        adj = set()
        for x in range(n):
            for u in arcs[x]:
                adj.add(frozenset((x, u)))
        core = variant[:-len("-explicit")]
        if core == "pairs":
            for a, b in combinations(range(n), 2):
                if frozenset((a, b)) not in adj:
                    clauses.append((a + 1, b + 1))
        else:
            for a, b, c in combinations(range(n), 3):
                if (frozenset((a, b)) not in adj and frozenset((a, c)) not in adj
                        and frozenset((b, c)) not in adj):
                    clauses.append((a + 1, b + 1, c + 1))
        return clauses, arcs, g
    if jump_width is None:
        jump_width = max(2, n // 100)
    base = n // 3 + 1
    jmax = (n - 3) // 2   # jump cap: 2*jmax <= n-3 < n-1 => no 2-cycles or triangles; girth >= 5
    assert base + 1 <= jmax, f"n={n} too small for the jump window"
    # spread W (indegree-1) and Wp (indegree-3) around the circle
    W = set((i * n) // m1 % n for i in range(m1)) if m1 else set()
    Wp = set(((i * n) // m1 + n // (2 * m1)) % n for i in range(m1)) if m1 else set()
    assert len(W) == m1 and len(Wp) == m1 and not (W & Wp), "W/Wp placement collision"
    cap = {v: (0 if v in W else 2 if v in Wp else 1) for v in range(n)}

    last_err = None
    for attempt in range(40):
        used = {v: 0 for v in range(n)}
        g = {}
        offs = list(range(base, jmax + 1))
        rot = attempt % max(1, len(offs))
        order = offs[rot:] + offs[:rot]   # deterministic rotation per attempt

        def ok_candidate(x, v):
            if used[v] >= cap[v]:
                return False
            if v in (x % n, (x + 1) % n, (x + 2) % n):
                return False      # v != x, x+1 (distinct negatives), x+2 (overlap on arc x->x+1)
            if g.get((x - 1) % n) == v or g.get((x + 1) % n) == v:
                return False      # g(x) != g(x+-1)  (overlap on arcs (x-1)->x resp. x->x+1)
            if g.get(v) == (x + 1) % n:
                return False      # x+1 not in out(g(x))  (overlap on arc x->g(x))
            return True

        def window_targets(x):
            return [(x + off) % n for off in order]

        def try_place(x, visited):
            """augmenting placement: put x on a free capacity slot, or relocate
            an existing occupant of a window target (depth-limited DFS)."""
            for v in window_targets(x):
                if v in ((x) % n, (x + 1) % n, (x + 2) % n):
                    continue
                if used[v] < cap[v]:
                    g[x] = v
                    used[v] += 1
                    return True
            if len(visited) > 12:
                return False
            for v in window_targets(x):
                if v in ((x) % n, (x + 1) % n, (x + 2) % n) or v in visited:
                    continue
                occupants = [u for u, t in g.items() if t == v]
                for u in occupants:
                    used[v] -= 1
                    del g[u]
                    if try_place(u, visited | {v}):
                        g[x] = v
                        used[v] += 1
                        return True
                    g[u] = v
                    used[v] += 1
            return False

        try:
            for x in range(n):
                for off in order:
                    v = (x + off) % n
                    if ok_candidate(x, v):
                        g[x] = v
                        used[v] += 1
                        break
                else:
                    if not try_place(x, frozenset()):
                        raise RuntimeError(f"g-assignment dead end at x={x}")

            def violations():
                bad = set()
                for x in range(n):
                    y, z = (x + 1) % n, g[x]
                    if z == g[y]:
                        bad.add(x)               # arc x->y overlap (z in out(y))
                    if (x + 1) % n == g.get(z) or (x + 1) % n == (z + 1) % n:
                        bad.add(x)               # arc x->z overlap (y in out(z))
                return bad

            for _ in range(60):
                bad = violations()
                if not bad:
                    break
                for x in sorted(bad):
                    old = g[x]
                    used[old] -= 1
                    g.pop(x)
                    for off in order:
                        v = (x + off) % n
                        if v != old and ok_candidate(x, v):
                            g[x] = v
                            used[v] += 1
                            break
                    else:
                        g[x] = old
                        used[old] += 1
            if violations():
                raise RuntimeError("overlap repair failed")
            break   # success
        except RuntimeError as ex:
            last_err = ex
            g = None
    if g is None:
        raise RuntimeError(f"construction failed after retries (n={n}, m1={m1}): {last_err}")
    arcs = {x: ((x + 1) % n, g[x]) for x in range(n)}
    # structural guarantee from the jump cap (checked, not assumed):
    for x in range(n):
        j = (g[x] - x) % n
        assert base <= j <= jmax, f"jump out of window at {x}"
    # clauses: literals as signed ints 1..n (positive) / negative
    clauses = []
    for x in range(n):
        y, z = arcs[x]
        clauses.append((x + 1, -(y + 1), -(z + 1)))
    adj = set()
    for x in range(n):
        for u in arcs[x]:
            adj.add(frozenset((x, u)))
    if variant == "pairs":
        for a, b in combinations(range(n), 2):
            if frozenset((a, b)) not in adj:
                clauses.append((a + 1, b + 1))
    elif variant == "triples":
        for a, b, c in combinations(range(n), 3):
            if (frozenset((a, b)) not in adj and frozenset((a, c)) not in adj
                    and frozenset((b, c)) not in adj):
                clauses.append((a + 1, b + 1, c + 1))
    else:
        raise ValueError(variant)
    return clauses, arcs, g

# ---------- verification primitives ----------
def is_critical(clause):
    """critical for its unique positive literal under alpha = all-ones:
    exactly one positive literal, all others negative."""
    pos = [l for l in clause if l > 0]
    return len(pos) == 1

def sat_dpll(clauses, forced_lit):
    """Return True iff clauses + [forced_lit] is satisfiable.  Small DPLL."""
    def unit_prop(assign, cls):
        changed = True
        while changed:
            changed = False
            newcls = []
            for c in cls:
                vals = []
                unassigned = []
                sat = False
                for l in c:
                    v = assign.get(abs(l))
                    if v is None:
                        unassigned.append(l)
                    elif (v and l > 0) or ((not v) and l < 0):
                        sat = True
                        break
                if sat:
                    continue
                if not unassigned:
                    return None, None  # conflict
                if len(unassigned) == 1:
                    l = unassigned[0]
                    assign[abs(l)] = l > 0
                    changed = True
                else:
                    newcls.append(c)
            cls = newcls
        return assign, cls
    def rec(assign, cls):
        assign, cls = unit_prop(dict(assign), cls)
        if assign is None:
            return False
        if not cls:
            return True
        # pick an UNASSIGNED variable from the first clause (branching on an
        # assigned literal would silently overwrite the forced assignment)
        l = next(l for l in cls[0] if abs(l) not in assign)
        v = abs(l)
        for val in (l > 0, not (l > 0)):
            a2 = dict(assign)
            a2[v] = val
            if rec(a2, cls):
                return True
        return False
    a0 = {abs(forced_lit): forced_lit > 0}
    return rec(a0, clauses)

def resolvents(clauses, parent_min_width3):
    """All width-<=3 non-tautological resolvents from pairs of clauses.
    parent_min_width3: if True, only width-exactly-3 clauses may be parents
    (the strict reading of Definition 31); else any width-<=3 clause."""
    parents = [c for c in clauses if (len(c) == 3 if parent_min_width3 else len(c) <= 3)]
    by_pos = {}
    by_neg = {}
    for idx, c in enumerate(parents):
        for l in c:
            (by_pos if l > 0 else by_neg).setdefault(abs(l), []).append(idx)
    out = set()
    for v in set(by_pos) & set(by_neg):
        for i in by_pos[v]:
            for j in by_neg[v]:
                ci, cj = parents[i], parents[j]
                lits = set(l for l in ci if l != v) | set(l for l in cj if l != -v)
                if any(-l in lits for l in lits):
                    continue  # tautology
                if len(lits) <= 3:
                    out.add(tuple(sorted(lits)))
    return out

def verify(n, m1, variant, quick=False):
    t0 = time.time()
    clauses, arcs, g = build(n, m1, variant)
    errors = []
    # V1 syntactic
    crit_in_F = {}
    for c in clauses:
        if is_critical(c):
            x = [l for l in c if l > 0][0]
            crit_in_F.setdefault(x, set()).add(tuple(sorted(c)))
    if set(crit_in_F) != set(range(1, n + 1)) or any(len(s) != 1 for s in crit_in_F.values()):
        errors.append("V1: not exactly one critical clause per variable in F")
    for x in range(n):
        y, z = arcs[x]
        if y == z or x in (y, z):
            errors.append(f"V1: bad arc pair at {x}")
    for c in clauses:
        if not is_critical(c):
            if any(l < 0 for l in c):
                errors.append(f"V1: aux clause with negative literal {c}")
    # V2
    if not all(any(l > 0 for l in c) for c in clauses):
        errors.append("V2: alpha=1^n does not satisfy F")
    # V3 uniqueness
    if not quick:
        for x in range(1, n + 1):
            if sat_dpll(clauses, -x):
                errors.append(f"V3: satisfiable with x{x}=0 -> NOT uniquely satisfiable")
                break
    # V4 closure and TwoCC (both readings)
    twocc_report = {}
    for strict in (True, False):
        res = resolvents(clauses, parent_min_width3=strict)
        crit_all = {x: set(s) for x, s in crit_in_F.items()}
        for c in res:
            if is_critical(c) and tuple(sorted(c)) not in set().union(*crit_in_F.values()):
                x = [l for l in c if l > 0][0]
                crit_all.setdefault(x, set()).add(c)
        twocc = [x for x, s in crit_all.items() if len(s) >= 2]
        twocc_report["strict" if strict else "loose"] = twocc
        if twocc:
            errors.append(f"V4({'strict' if strict else 'loose'}): TwoCC nonempty: {sorted(twocc)[:6]}...")
    # V5 degrees
    indeg = {v: 0 for v in range(n)}
    for x in range(n):
        for u in arcs[x]:
            indeg[u] += 1
    prof = {}
    for v, d in indeg.items():
        prof[d] = prof.get(d, 0) + 1
    if prof.get(0, 0) != 0:
        errors.append("V5: indegree-0 vertex exists")
    if prof.get(1, 0) != m1:
        errors.append(f"V5: |J_1| = {prof.get(1,0)} != m1 = {m1}")
    if not set(prof).issubset({1, 2, 3}):
        errors.append(f"V5: indegrees outside {{1,2,3}}: {sorted(set(prof)-{1,2,3})}")
    # V6 structure (reported)
    twocycles = sum(1 for x in range(n) for u in arcs[x] if x in arcs[u])
    overlap_bad = 0
    for x in range(n):
        y, z = arcs[x]
        if z in arcs[y] or y in arcs[z]:
            overlap_bad += 1
    # directed girth via BFS from each vertex
    import collections
    girth = None
    for s in range(n):
        dist = {s: 0}
        q = collections.deque([s])
        while q:
            u = q.popleft()
            for w in arcs[u]:
                if w == s:
                    gl = dist[u] + 1
                    girth = gl if girth is None else min(girth, gl)
                elif w not in dist:
                    dist[w] = dist[u] + 1
                    q.append(w)
    status = "PASS" if not errors else "FAIL"
    i0 = prof.get(0, 0) / n
    # ID_i = J_i \ TwoCC; TwoCC empty when V4 passes
    i1 = prof.get(1, 0) / n
    tau = len(twocc_report["loose"]) / n
    print(f"[{status}] n={n:3d} m1={m1:2d} {variant:7s} m={len(clauses):6d} "
          f"stats=({i0:.4f},{i1:.6f},{tau:.4f}) target_i1={m1/n:.6f} "
          f"profile={dict(sorted(prof.items()))} girth={girth} 2cyc={twocycles} "
          f"ovl={overlap_bad} t={time.time()-t0:.1f}s")
    for e in errors:
        print("   ERROR:", e)
    return not errors

def main():
    ok = True
    cases = []
    # constructor requires n >= 26 (window/repair feasibility; the family is asymptotic)
    for n in (26, 30, 40, 50, 60, 80, 100):
        m1 = round(I1_STAR * n)
        cases.append((n, m1, "pairs"))
    cases.append((60, 4, "triples"))
    cases.append((80, 5, "triples"))
    # explicit (search-free) Theorem-CR construction:
    for n in (30, 50, 80, 100, 120):
        cases.append((n, round(I1_STAR * n), "pairs-explicit"))
    cases.append((80, 5, "triples-explicit"))
    cases.append((100, 6, "triples-explicit"))
    # breadth of the realizable edge (i_0 = tau = 0, varying i_1):
    for m1 in (0, 2, 6, 12, 16):
        cases.append((50, m1, "pairs"))
    dataset = []
    for (n, m1, variant) in cases:
        try:
            good = verify(n, m1, variant)
            ok &= good
            if good:
                clauses, arcs, g = build(n, m1, variant)
                dataset.append({"n": n, "m1": m1, "variant": variant,
                                "g": [g[x] for x in range(n)],
                                "stats": [0.0, m1 / n, 0.0]})
        except Exception as ex:
            print(f"[FAIL] n={n} m1={m1} {variant}: EXCEPTION {ex}")
            ok = False
    if ok:
        import json, os
        os.makedirs("certificates/cycle07_corner", exist_ok=True)
        with open("certificates/cycle07_corner/instances.json", "w") as f:
            json.dump({"description": "Cycle-7 corner-realizability instances: "
                       "F = {(x OR NOT(x+1 mod n) OR NOT g[x])} + all-positive killers "
                       "(pairs variant: all CCG-non-adjacent pairs; triples variant: all "
                       "pairwise-non-adjacent triples). Verified: unique satisfiability, "
                       "TwoCC(F-tilde) = empty (both Definition-31 readings), "
                       "J_0 = empty, |J_1| = m1.",
                       "i1_star": "0.060043244708778326... = (A-P_reg)/(A+b_1) [JC26]",
                       "instances": dataset}, f, indent=1)
        print("dataset written: certificates/cycle07_corner/instances.json")
    print("RESULT:", "ALL VERIFICATIONS PASSED" if ok else "FAILURES PRESENT")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()

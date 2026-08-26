#!/usr/bin/env python3
"""cr_review_engine_diff.py — differential audit of the ENGINE's two load-bearing
primitives (sat_dpll, resolvents) in experiments/cycle07_corner_family.py,
against brute force, on random formulas.  Hostile review item B7.

- sat_dpll(clauses, forced_lit) vs exhaustive truth-table SAT (n <= 14).
- resolvents(clauses, parent_min_width3) vs a naive quadratic all-pairs,
  all-complementary-literal resolution written independently here.
"""
import sys, os, random, itertools, importlib.util

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
spec = importlib.util.spec_from_file_location(
    "engine", os.path.join(ROOT, "experiments", "cycle07_corner_family.py"))
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)

def brute_sat(n, clauses, forced_lit):
    fv = abs(forced_lit); fb = forced_lit > 0
    for bits in range(1 << n):
        assign = [(bits >> i) & 1 == 1 for i in range(n)]
        if assign[fv - 1] != fb:
            continue
        ok = True
        for c in clauses:
            if not any((assign[abs(l) - 1] and l > 0) or
                       (not assign[abs(l) - 1] and l < 0) for l in c):
                ok = False
                break
        if ok:
            return True
    return False

def naive_resolvents(clauses, strict):
    par = [tuple(c) for c in clauses if (len(c) == 3 if strict else len(c) <= 3)]
    out = set()
    for c1, c2 in itertools.product(par, repeat=2):
        for l in c1:
            if -l in c2:
                r = set(x for x in c1 if x != l) | set(x for x in c2 if x != -l)
                if len(r) <= 3 and not any(-x in r for x in r):
                    out.add(tuple(sorted(r)))
    return out

def rand_clause(rng, n, w):
    vs = rng.sample(range(1, n + 1), w)
    return tuple(v if rng.random() < 0.5 else -v for v in vs)

def main():
    rng = random.Random(818)
    bad = 0
    # --- DPLL diff ---
    for trial in range(300):
        n = rng.randint(4, 11)
        m = rng.randint(3, 45)
        clauses = [rand_clause(rng, n, rng.choice([1, 2, 2, 3, 3, 3])) for _ in range(m)]
        for forced in (1, -1, rng.randint(2, n) * rng.choice([1, -1])):
            got = engine.sat_dpll(clauses, forced)
            want = brute_sat(n, clauses, forced)
            if got != want:
                bad += 1
                print(f"DPLL MISMATCH trial={trial} n={n} forced={forced}: "
                      f"engine={got} brute={want}\n  clauses={clauses}")
    print(f"DPLL differential: 300 formulas x 3 forced literals, mismatches = {bad}")
    # also: uniquely-satisfiable-style formulas (positive-heavy, like the family)
    bad2 = 0
    for trial in range(150):
        n = rng.randint(4, 10)
        clauses = [(x, -(x % n + 1), -((x + 1) % n + 1)) for x in range(1, n + 1)]
        clauses = [c for c in clauses if len(set(abs(l) for l in c)) == 3]
        for _ in range(rng.randint(1, 12)):
            w = rng.choice([2, 3])
            clauses.append(tuple(rng.sample(range(1, n + 1), w)))
        for forced in [rng.randint(1, n) * rng.choice([1, -1]) for _ in range(3)]:
            got = engine.sat_dpll(clauses, forced)
            want = brute_sat(n, clauses, forced)
            if got != want:
                bad2 += 1
                print(f"DPLL MISMATCH(fam) trial={trial}: engine={got} brute={want}\n"
                      f"  forced={forced} clauses={clauses}")
    print(f"DPLL differential (family-style): 150 formulas x 3, mismatches = {bad2}")
    # --- resolvents diff ---
    bad3 = 0
    for trial in range(400):
        n = rng.randint(3, 9)
        m = rng.randint(2, 25)
        clauses = []
        for _ in range(m):
            w = rng.choice([2, 3, 3])
            clauses.append(rand_clause(rng, n, w))
        for strict in (True, False):
            got = engine.resolvents(clauses, parent_min_width3=strict)
            want = naive_resolvents(clauses, strict)
            if set(got) != want:
                bad3 += 1
                print(f"RESOLVENT MISMATCH trial={trial} strict={strict}:\n"
                      f"  engine-only={set(got)-want}\n  naive-only={want-set(got)}\n"
                      f"  clauses={clauses}")
    print(f"resolvents differential: 400 clause-sets x 2 readings, mismatches = {bad3}")
    total = bad + bad2 + bad3
    print("RESULT:", "ALL DIFFERENTIALS AGREE" if total == 0 else f"{total} MISMATCHES")
    sys.exit(0 if total == 0 else 1)

if __name__ == "__main__":
    main()

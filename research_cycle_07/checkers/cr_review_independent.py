#!/usr/bin/env python3
"""cr_review_independent.py — hostile-review independent checker for Theorem CR
(cycle 7 corner realizability).  Written from scratch for the arms-length review;
shares NO code with experiments/cycle07_corner_family.py.

Reconstructs every instance from certificates/cycle07_corner/instances.json
(only g and the variant are trusted; clauses rebuilt per the construction spec
in research_cycle_07/corner_realizability.md section 2) and re-verifies:

  R1  clause reconstruction + clause count (cross-checked against the engine
      transcript m-values hard-coded below from the transcript file).
  R2  independent indegree profile (J_0, J_1, full profile).
  R3  independent closure F~ (own resolvent code), BOTH parent-width readings,
      critical-clause census per variable, TwoCC; plus an ITERATED-closure
      experiment (fixpoint of width<=3 resolution) to probe the robustness of
      the one-round reading of Definition 31.
  R4  unique satisfiability by an independent method stack:
        (a) own counter-based DPLL model ENUMERATOR (counts all models, cap 2)
            — different algorithm/data structures from the engine's DPLL;
        (b) closed-set characterization, differentially validated against
            direct clause evaluation (random assignments + all |S| <= 3);
        (c) complete clique enumeration of the sibling-adjacency graph (pairs
            variant: any second solution's zero-set must be a closed clique);
        (d) simple directed cycle enumeration up to length 12 (triples
            variant: any closed set contains a directed cycle; with girth
            >= 13 and Delta(Adj) <= 5 an independent triple exists in any
            closed S, killing it);
        (e) exhaustive small-|S| sweep via the (validated) characterization
            (n=30 explicit: |S| <= 8; n=50 explicit: |S| <= 5).
  R5  structure: directed girth (own BFS), Delta(Adj), max clique size,
      2-cycles, grandparent-overlap count (own definition).
  R6  sanity constraints the family MUST satisfy if genuinely uniquely
      satisfiable (B9): 0 <= i0,i1,tau; i0+i1+tau <= 1; sum indeg = 2n;
      degree identity 2*n0 + n1 = sum_{k>=3}(k-2)*n_k; every variable owns
      >= 1 critical clause.
  R7  doc-vs-engine construction fidelity: rebuild g from the DOC's section-2
      formulas under (i) the doc's literal delta-condition (pairwise
      disjointness of {p},{s},{q}) and (ii) the engine-style condition
      (no P-cap-S requirement); compare with the stored g.
"""

import json, sys, time, itertools, os
from collections import deque

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
DATA = os.path.join(ROOT, "certificates", "cycle07_corner", "instances.json")

# m-values from research_cycle_07/corner_family_verification_output.txt (transcript)
TRANSCRIPT_M = {
    (26, 2, "pairs"): 299, (30, 2, "pairs"): 405, (40, 2, "pairs"): 740,
    (50, 3, "pairs"): 1175, (60, 4, "pairs"): 1710, (80, 5, "pairs"): 3080,
    (100, 6, "pairs"): 4850, (60, 4, "triples"): 27684, (80, 5, "triples"): 70245,
    (30, 2, "pairs-explicit"): 405, (50, 3, "pairs-explicit"): 1175,
    (80, 5, "pairs-explicit"): 3080, (100, 6, "pairs-explicit"): 4850,
    (120, 7, "pairs-explicit"): 7020, (80, 5, "triples-explicit"): 70245,
    (100, 6, "triples-explicit"): 142806,
    (50, 0, "pairs"): 1175, (50, 2, "pairs"): 1175, (50, 6, "pairs"): 1175,
    (50, 12, "pairs"): 1175, (50, 16, "pairs"): 1175,
}
TRANSCRIPT_GIRTH = {
    (26, 2, "pairs"): 6, (30, 2, "pairs"): 6, (40, 2, "pairs"): 6,
    (50, 3, "pairs"): 5, (60, 4, "pairs"): 9, (80, 5, "pairs"): 8,
    (100, 6, "pairs"): 11, (60, 4, "triples"): 9, (80, 5, "triples"): 8,
    (30, 2, "pairs-explicit"): 6, (50, 3, "pairs-explicit"): 16,
    (80, 5, "pairs-explicit"): 20, (100, 6, "pairs-explicit"): 30,
    (120, 7, "pairs-explicit"): 26, (80, 5, "triples-explicit"): 20,
    (100, 6, "triples-explicit"): 30,
    (50, 0, "pairs"): 18, (50, 2, "pairs"): 6, (50, 6, "pairs"): 6,
    (50, 12, "pairs"): 7, (50, 16, "pairs"): 8,
}

FAILURES = []
def check(cond, label):
    tag = "ok" if cond else "**FAIL**"
    if not cond:
        FAILURES.append(label)
    print(f"      [{tag}] {label}")
    return cond

# ---------------- reconstruction ----------------

def reconstruct(n, g, core):
    """Clauses per corner_realizability.md sec 2. Variables 0..n-1, literal
    encoding: +(v+1) positive, -(v+1) negative. Returns (crit, aux, out, adj)."""
    out = {x: (( x + 1) % n, g[x]) for x in range(n)}
    crit = []
    for x in range(n):
        y, z = out[x]
        assert y != z and x not in (y, z), f"bad arcs at {x}"
        crit.append((x + 1, -(y + 1), -(z + 1)))
    adjset = set()
    for x in range(n):
        for u in out[x]:
            adjset.add((min(x, u), max(x, u)))
    aux = []
    if core == "pairs":
        for a in range(n):
            for b in range(a + 1, n):
                if (a, b) not in adjset:
                    aux.append((a + 1, b + 1))
    else:
        for a, b, c in itertools.combinations(range(n), 3):
            if ((a, b) not in adjset and (a, c) not in adjset
                    and (b, c) not in adjset):
                aux.append((a + 1, b + 1, c + 1))
    return crit, aux, out, adjset

# ---------------- R2 indegree ----------------

def indegree_profile(n, out):
    indeg = [0] * n
    for x in range(n):
        for u in out[x]:
            indeg[u] += 1
    prof = {}
    for d in indeg:
        prof[d] = prof.get(d, 0) + 1
    return indeg, prof

# ---------------- R3 closure ----------------

def my_resolvents(clauses, strict_parents):
    """Own implementation: width<=3 non-tautological resolvents from pairs of
    clauses of `clauses`. strict_parents=True: only width-exactly-3 parents."""
    par = [frozenset(c) for c in clauses if (len(c) == 3 if strict_parents else len(c) <= 3)]
    pos_occ, neg_occ = {}, {}
    for i, c in enumerate(par):
        for lit in c:
            d = pos_occ if lit > 0 else neg_occ
            d.setdefault(abs(lit), []).append(i)
    seen = set()
    for v in pos_occ:
        if v not in neg_occ:
            continue
        for i in pos_occ[v]:
            for j in neg_occ[v]:
                r = (par[i] - {v}) | (par[j] - {-v})
                if len(r) > 3:
                    continue
                if any(-t in r for t in r):
                    continue
                seen.add(frozenset(r))
    return seen

def critical_census(n, base_clauses, resolvent_sets):
    """Count distinct critical clauses (exactly one positive literal) per
    variable among base clauses plus resolvents."""
    cc = {x: set() for x in range(1, n + 1)}
    def add(fs):
        pos = [t for t in fs if t > 0]
        if len(pos) == 1:
            cc[pos[0]].add(fs)
    for c in base_clauses:
        add(frozenset(c))
    for fs in resolvent_sets:
        add(fs)
    return cc

def iterated_closure(clauses, cap=60000):
    """Fixpoint of width<=3 resolution (all width<=3 clauses as parents),
    to probe the alternative (iterated) reading of Definition 31."""
    universe = set(frozenset(c) for c in clauses)
    pos_occ, neg_occ = {}, {}
    def index(fs):
        for lit in fs:
            (pos_occ if lit > 0 else neg_occ).setdefault(abs(lit), set()).add(fs)
    for fs in universe:
        index(fs)
    work = deque(universe)
    truncated = False
    while work:
        c = work.popleft()
        partners = set()
        for lit in c:
            v = abs(lit)
            partners |= (neg_occ.get(v, set()) if lit > 0 else pos_occ.get(v, set()))
        for d in partners:
            for lit in c:
                if -lit in d:
                    r = (c - {lit}) | (d - {-lit})
                    if len(r) > 3 or any(-t in r for t in r):
                        continue
                    fr = frozenset(r)
                    if fr not in universe:
                        universe.add(fr)
                        index(fr)
                        work.append(fr)
        if len(universe) > cap:
            truncated = True
            break
    return universe, truncated

# ---------------- R4a own DPLL enumerator ----------------

class Enumerator:
    """Counter-based DPLL model counter (cap 2). Own design: occurrence lists,
    per-clause unassigned/satisfied counters, explicit trail undo."""
    def __init__(self, n, clauses):
        self.n = n
        self.cl = [tuple(c) for c in clauses]
        self.occ = {}
        for i, c in enumerate(self.cl):
            for lit in c:
                self.occ.setdefault(lit, []).append(i)
        self.val = [None] * (n + 1)          # 1-indexed
        self.unass = [len(c) for c in self.cl]
        self.satcnt = [0] * len(self.cl)
        self.models = []
        self.nodes = 0

    def assign(self, lit, trail):
        v, b = abs(lit), lit > 0
        self.val[v] = b
        trail.append(v)
        conflict = None
        units = []
        for i in self.occ.get(lit, ()):        # satisfied occurrences
            self.satcnt[i] += 1
        for i in self.occ.get(lit, ()):
            self.unass[i] -= 1
        for i in self.occ.get(-lit, ()):       # falsified occurrences
            self.unass[i] -= 1
            if self.satcnt[i] == 0:
                if self.unass[i] == 0:
                    conflict = i
                elif self.unass[i] == 1:
                    units.append(i)
        return conflict, units

    def undo(self, trail, mark):
        while len(trail) > mark:
            v = trail.pop()
            for sgn in (1, -1):
                lit = sgn * v
                is_true = (self.val[v] if sgn > 0 else not self.val[v])
                for i in self.occ.get(lit, ()):
                    self.unass[i] += 1
                    if is_true:
                        self.satcnt[i] -= 1
            self.val[v] = None

    def propagate(self, lit, trail):
        queue = deque([lit])
        while queue:
            l = queue.popleft()
            v = abs(l)
            if self.val[v] is not None:
                if self.val[v] != (l > 0):
                    return False
                continue
            conflict, units = self.assign(l, trail)
            if conflict is not None:
                return False
            for i in units:
                if self.satcnt[i] == 0 and self.unass[i] == 1:
                    for t in self.cl[i]:
                        if self.val[abs(t)] is None:
                            queue.append(t)
                            break
        return True

    def all_satisfied(self):
        return all(self.satcnt[i] > 0 or self.unass[i] > 0 for i in range(len(self.cl))) \
            and all(self.satcnt[i] > 0 for i in range(len(self.cl)) if self.unass[i] == 0)

    def pick(self):
        for i in range(len(self.cl)):
            if self.satcnt[i] == 0:
                for t in self.cl[i]:
                    if self.val[abs(t)] is None:
                        return t
        return None

    def search(self):
        self.nodes += 1
        if len(self.models) >= 2:
            return
        lit = self.pick()
        if lit is None:
            # every clause satisfied; free variables => multiple models
            free = sum(1 for v in range(1, self.n + 1) if self.val[v] is None)
            if free == 0:
                self.models.append(tuple(self.val[1:]))
            else:
                m1 = list(self.val[1:])
                self.models.append(tuple(m1))
                self.models.append(("free", free))
            return
        for choice in (lit, -lit):
            trail = []
            if self.propagate(choice, trail):
                self.search()
            self.undo(trail, 0)
            if len(self.models) >= 2:
                return

    def count(self):
        trail = []
        self.search()
        return self.models

# ---------------- R4b characterization + validation ----------------

def eval_clauses_direct(clauses, zero_set):
    for c in clauses:
        ok = False
        for lit in c:
            v = abs(lit) - 1
            val = v not in zero_set
            if (val and lit > 0) or ((not val) and lit < 0):
                ok = True
                break
        if not ok:
            return False
    return True

def characterization(n, out, adjset, core, S):
    if not S:
        return True
    for x in S:
        if not any(u in S for u in out[x]):
            return False
    Sl = sorted(S)
    if core == "pairs":
        for a, b in itertools.combinations(Sl, 2):
            if (a, b) not in adjset:
                return False
    else:
        for a, b, c in itertools.combinations(Sl, 3):
            if ((a, b) not in adjset and (a, c) not in adjset
                    and (b, c) not in adjset):
                return False
    return True

# ---------------- R4c clique enumeration ----------------

def all_cliques(n, adjset):
    nb = {v: set() for v in range(n)}
    for a, b in adjset:
        nb[a].add(b); nb[b].add(a)
    cliques = []
    def extend(cur, cand):
        for v in sorted(cand):
            newcur = cur + [v]
            cliques.append(newcur)
            extend(newcur, cand & nb[v] & set(range(v + 1, n)))
    extend([], set(range(n)))
    return cliques, nb

# ---------------- R4d simple directed cycles ----------------

def short_cycles(n, out, maxlen):
    found = []
    for s in range(n):
        stack = [(s, [s])]
        while stack:
            v, path = stack.pop()
            for u in out[v]:
                if u == s and len(path) >= 2:
                    found.append(list(path))
                elif u > s and u not in path and len(path) < maxlen:
                    stack.append((u, path + [u]))
    return found

# ---------------- R5 girth ----------------

def directed_girth(n, out):
    best = None
    for s in range(n):
        dist = {s: 0}
        q = deque([s])
        while q:
            v = q.popleft()
            if best is not None and dist[v] + 1 >= best:
                continue
            for u in out[v]:
                if u == s:
                    cyc = dist[v] + 1
                    if best is None or cyc < best:
                        best = cyc
                elif u not in dist:
                    dist[u] = dist[v] + 1
                    q.append(u)
    return best

# ---------------- R7 doc-vs-engine explicit construction ----------------

def doc_explicit_g(n, m1, require_ps_disjoint):
    """Section-2 formulas of corner_realizability.md. require_ps_disjoint=True
    follows the doc LITERALLY ({p},{s},{q} pairwise disjoint); False follows
    the engine (only Q-conditions)."""
    base = n // 3 + 1
    jmax = (n - 3) // 2
    if m1 == 0:
        return {x: (x + base) % n for x in range(n)}, None, []
    P = [ (i * n) // m1 % n for i in range(m1)]
    S = [ (p - base) % n for p in P]
    spacing = n // m1
    hi = min(spacing - 2, jmax - base)
    notes = []
    if set(P) & set(S):
        notes.append(f"P-cap-S nonempty: {sorted(set(P) & set(S))}")
    delta = None
    for d in range(2, hi + 1):
        Q = [ (p + d) % n for p in P]
        okc = True
        if set(Q) & set(P) or set(Q) & set(S):
            okc = False
        if okc and any(((q - 1) % n) in set(S) or ((q + 1) % n) in set(S) for q in Q):
            okc = False
        if okc and require_ps_disjoint and (set(P) & set(S)):
            okc = False
        if okc and require_ps_disjoint and (len(set(P) | set(S) | set(Q)) < 3 * m1):
            okc = False
        if okc:
            delta = d
            break
    if delta is None:
        return None, None, notes
    g = {x: (x + base) % n for x in range(n)}
    for i, p in enumerate(P):
        g[S[i]] = (p + delta) % n
    return g, delta, notes

# ---------------- driver ----------------

def run_instance(inst, heavy_uniqueness, smallS_cap, do_iter_closure):
    n, m1, variant, g = inst["n"], inst["m1"], inst["variant"], inst["g"]
    core = "pairs" if variant.startswith("pairs") else "triples"
    key = (n, m1, variant)
    print(f"\n=== instance n={n} m1={m1} {variant} ===")
    t0 = time.time()
    crit, aux, out, adjset = reconstruct(n, g, core)
    clauses = crit + aux
    m = len(clauses)

    # R1
    check(m == TRANSCRIPT_M.get(key), f"R1 clause count m={m} matches transcript {TRANSCRIPT_M.get(key)}")
    check(all(len(set(abs(t) for t in c)) == len(c) for c in clauses), "R1 no repeated variable inside any clause")
    check(all(all(t > 0 for t in c) for c in aux), "R1 aux clauses all-positive")
    ncrit_widths = set(len(c) for c in crit)
    check(ncrit_widths == {3}, "R1 all critical clauses width exactly 3")

    # R2
    indeg, prof = indegree_profile(n, out)
    check(prof.get(0, 0) == 0, "R2 no indegree-0 vertex")
    check(prof.get(1, 0) == m1, f"R2 |J_1| = {prof.get(1,0)} equals m1 = {m1}")
    check(set(prof) <= {1, 2, 3} or (m1 == 0 and set(prof) == {2}),
          f"R2 profile support in {{1,2,3}}: {dict(sorted(prof.items()))}")
    check(sum(d * c for d, c in prof.items()) == 2 * n, "R2 sum of indegrees = 2n")
    n0 = prof.get(0, 0); n1 = prof.get(1, 0)
    rhs = sum((k - 2) * c for k, c in prof.items() if k >= 3)
    check(2 * n0 + n1 == rhs, "R6 degree identity 2*n0+n1 = sum_(k>=3)(k-2)n_k")

    # R6 statistics sanity
    i0, i1, tau_claim = 0.0, m1 / n, 0.0
    check(0 <= i0 + i1 + tau_claim <= 1, "R6 simplex: i0+i1+tau in [0,1]")

    # R3 closure, both readings
    for strict in (True, False):
        res = my_resolvents(clauses, strict)
        cc = critical_census(n, clauses, res)
        counts = {x: len(s) for x, s in cc.items()}
        twocc = [x for x, k in counts.items() if k >= 2]
        zero = [x for x, k in counts.items() if k == 0]
        tag = "strict(w=3 parents)" if strict else "loose(w<=3 parents)"
        check(not zero, f"R3[{tag}] every variable owns >= 1 critical clause in F~")
        check(not twocc, f"R3[{tag}] TwoCC empty (|resolvents|={len(res)})")
        check(all(k == 1 for k in counts.values()),
              f"R3[{tag}] EXACTLY one critical clause per variable in F~ (forced selection)")
        if not strict:
            n_res_loose = len(res)

    # iterated-closure probe (alternative Definition-31 reading)
    if do_iter_closure:
        uni, truncated = iterated_closure(clauses)
        cc = critical_census(n, [], uni)
        counts = {x: len(s) for x, s in cc.items()}
        twocc_iter = sum(1 for k in counts.values() if k >= 2)
        print(f"      [info] ITERATED closure: {len(uni)} clauses"
              f"{' (TRUNCATED)' if truncated else ''}; |TwoCC_iter| = {twocc_iter}"
              f" (tau_iter = {twocc_iter/n:.3f}) — one-round reading is load-bearing"
              f" for pairs iff this is nonzero")

    # R5 structure
    girth = directed_girth(n, out)
    check(girth == TRANSCRIPT_GIRTH.get(key),
          f"R5 girth (own BFS) = {girth} matches transcript {TRANSCRIPT_GIRTH.get(key)}")
    two_cyc = sum(1 for x in range(n) for u in out[x] if x in out[u])
    check(two_cyc == 0, "R5 no 2-cycles")
    ovl = 0
    for u in range(n):
        for x in out[u]:
            others = set(out[u]) - {x}
            if others & set(out[x]):
                ovl += 1
    check(ovl == 0, "R5 grandparent-overlap-free (own definition)")
    cliques, nb = all_cliques(n, adjset)
    Delta = max(len(nb[v]) for v in range(n))
    maxclq = max(len(c) for c in cliques)
    check(Delta <= 5, f"R5 Delta(Adj) = {Delta} <= 5")
    print(f"      [info] max clique size = {maxclq}, girth = {girth} "
          f"(closed-set route needs maxclique < girth for pairs: "
          f"{'HOLDS' if maxclq < (girth or 10**9) else 'FAILS -> uniqueness rests on search methods'})")

    # R4b differential validation of the characterization
    import random
    rng = random.Random(20260826)
    ok_diff = True
    for _ in range(4000):
        k = rng.randint(0, min(n, 12))
        S = set(rng.sample(range(n), k))
        if eval_clauses_direct(clauses, S) != characterization(n, out, adjset, core, S):
            ok_diff = False
            break
    for S in itertools.chain(itertools.combinations(range(n), 1),
                             itertools.combinations(range(n), 2),
                             itertools.combinations(range(n), 3)):
        if eval_clauses_direct(clauses, set(S)) != characterization(n, out, adjset, core, set(S)):
            ok_diff = False
            break
    check(ok_diff, "R4b closed-set characterization == direct clause evaluation "
                   "(4000 random + all |S|<=3)")

    # R4c / R4d uniqueness via structure
    if core == "pairs":
        bad = [c for c in cliques if c and characterization(n, out, adjset, core, set(c))
               and all(any(u in set(c) for u in out[x]) for x in c)]
        # characterization already includes closedness; keep explicit closedness too
        bad = [c for c in cliques if c and all(any(u in set(c) for u in out[x]) for x in c)]
        check(not bad, f"R4c NO closed clique among all {len(cliques)} cliques of Adj "
                       f"=> no second solution (complete for pairs variant)")
    else:
        cycles = short_cycles(n, out, 12)
        need = 2 * (Delta + 1) + 1
        if not cycles and girth is not None and girth >= need:
            check(True, f"R4d no cycle <= 12 and girth {girth} >= 2(Delta+1)+1 = {need} "
                        f"=> any closed S contains an independent triple => killed "
                        f"(structural uniqueness proof complete for triples)")
        else:
            # not a soundness failure of the reviewed claims: the doc's sec-3.3
            # closed-set argument simply does not cover this low-girth instance
            # (finding B3); uniqueness rests on the enumeration methods.
            print(f"      [warn] R4d girth {girth} < {need} (or short cycles exist): "
                  f"the closed-set/girth uniqueness argument does NOT cover this "
                  f"instance; uniqueness rests on R4a/engine-V3 search")

    # R4e exhaustive small-S sweep (uses validated characterization)
    if smallS_cap:
        cap = smallS_cap
        bad = None
        tested = 0
        for k in range(1, cap + 1):
            for S in itertools.combinations(range(n), k):
                tested += 1
                Sset = set(S)
                closed = all(any(u in Sset for u in out[x]) for x in S)
                if not closed:
                    continue
                if characterization(n, out, adjset, core, Sset):
                    bad = Sset
                    break
            if bad:
                break
        check(bad is None, f"R4e no satisfying zero-set with 1 <= |S| <= {cap} "
                           f"({tested} subsets swept)")

    # R4a own enumerator
    if heavy_uniqueness:
        en = Enumerator(n, clauses)
        models = en.count()
        ok1 = len(models) == 1 and models[0] == tuple([True] * n)
        check(ok1, f"R4a own DPLL enumerator: model count = {len(models)}; "
                   f"unique model is all-ones (nodes={en.nodes})")

    print(f"      time {time.time()-t0:.1f}s")


ONLY = None   # optional set of (n, m1, variant) filters from argv

def main():
    global ONLY
    if len(sys.argv) > 1:
        ONLY = set()
        for spec in sys.argv[1:]:
            a, b, c = spec.split(",")
            ONLY.add((int(a), int(b), c))
    with open(DATA) as f:
        data = json.load(f)
    instances = data["instances"]
    print(f"loaded {len(instances)} instances from {DATA}")

    # R7 doc-vs-engine construction comparison for the explicit instances
    print("\n=== R7 explicit-construction fidelity (doc sec 2 formulas vs stored g) ===")
    for inst in instances:
        if not inst["variant"].endswith("-explicit"):
            continue
        n, m1 = inst["n"], inst["m1"]
        g_doc, delta_doc, notes_doc = doc_explicit_g(n, m1, require_ps_disjoint=True)
        g_eng, delta_eng, notes_eng = doc_explicit_g(n, m1, require_ps_disjoint=False)
        stored = {x: inst["g"][x] for x in range(n)}
        lit = "constructible" if g_doc is not None else "NO VALID delta (doc condition vacuous)"
        print(f"  n={n} m1={m1}: doc-literal condition: {lit}"
              + (f"  [{'; '.join(notes_doc)}]" if notes_doc else ""))
        if g_eng is None:
            check(False, f"R7 n={n},m1={m1}: engine-style condition also fails!")
        else:
            check(g_eng == stored, f"R7 n={n},m1={m1}: my re-derivation (engine-style, "
                                   f"delta={delta_eng}) reproduces stored g exactly")
        if g_doc is not None:
            check(g_doc == stored, f"R7 n={n},m1={m1}: doc-literal construction matches stored g")

    # per-instance verification
    for inst in instances:
        n, m1, variant = inst["n"], inst["m1"], inst["variant"]
        heavy = True                       # own enumerator on all instances
        smallS = 0
        if (n, variant) == (30, "pairs-explicit"):
            smallS = 8
        elif (n, variant) == (50, "pairs-explicit"):
            smallS = 5
        do_iter = (n, variant) in ((30, "pairs-explicit"), (26, "pairs"),
                                   (80, "triples-explicit"), (100, "triples-explicit"))
        if ONLY and (n, m1, variant) not in ONLY:
            continue
        run_instance(inst, heavy, smallS, do_iter)

    print("\n=== SUMMARY ===")
    if FAILURES:
        print(f"{len(FAILURES)} FAILURES:")
        for f_ in FAILURES:
            print("  -", f_)
        sys.exit(1)
    print("all independent checks passed")
    sys.exit(0)

if __name__ == "__main__":
    main()

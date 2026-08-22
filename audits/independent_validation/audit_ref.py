"""Independent auditor reference engine for Cycle-5 hybrid multi-RR validation.

Written from scratch from the definitions in research_cycle_05/hybrid_definitions.md
(section 1: RR_n literal family; full induced-subset-DAG acceptance) WITHOUT
consulting any Cycle-5 experiment code.

Ground set: Z_q u {INF}, q = n-1, INF encoded as index q (so ground = 0..n-1).
Normalized coloring: f(INF) = -1; word w = bitmask over Z_q of the +1 positions,
popcount(w) = m = n/2.
"""
from itertools import combinations
import random, sys

def popcount(x): return bin(x).count('1')

# ---------------------------------------------------------------- literal family
def rr_family(n):
    q = n - 1
    INF = q
    fam = set()
    fam.add(frozenset())
    fam.add(frozenset(range(n)))
    for x in range(q):
        fam.add(frozenset([x]))
    for L in range(1, q):
        for s in range(q):
            iv = frozenset(((s + i) % q) for i in range(L))
            fam.add(iv | {INF})
    assert len(fam) == q * q + 2
    return fam

def apply_perm_fam(fam, perm):
    return set(frozenset(perm[x] for x in S) for S in fam)

def literal_accepts(fam_by_rank, n, fvals):
    """Generic induced-subset-DAG acceptance. fam_by_rank[k] = list of frozensets.
    fvals[x] = +-1 for x in 0..n-1."""
    def disc(S): return sum(fvals[x] for x in S)
    reach = {frozenset()}
    for k in range(1, n + 1):
        nxt = set()
        for S in fam_by_rank[k]:
            if abs(disc(S)) <= 1:
                for x in S:
                    if S - {x} in reach:
                        nxt.add(S)
                        break
        reach = nxt
        if not reach:
            return False
    return True

def by_rank(fam, n):
    br = [[] for _ in range(n + 1)]
    for S in fam:
        br[len(S)].append(S)
    return br

def word_to_fvals(w, n):
    """word bitmask over Z_q -> fvals list with f(INF)=-1."""
    q = n - 1
    return [1 if (w >> x) & 1 else -1 for x in range(q)] + [-1]

# ------------------------------------------------------- interval-walk semantics
def intervals_by_len(pf, q):
    """pf: length-q list, the finite part of an INF-fixing permutation.
    Circle O: position i holds pf[i].  Int(O) = images of std cyclic intervals.
    Returns list ints[L] = set of bitmasks, L = 1..q-1."""
    ints = [set() for _ in range(q)]
    for s in range(q):
        m = 0
        for L in range(1, q):
            m |= 1 << pf[(s + L - 1) % q]
            ints[L].add(m)
    return ints

def sum_ok(m, w, l):
    s = 2 * popcount(m & w) - l
    return (s == 1) if (l & 1) else (s == 0 or s == 2)

def union_accepts_walk(w, circles, q):
    """circles: list of intervals_by_len structures. Auditor's own set-level DP."""
    cur = set()
    for c in circles:
        for m in c[1]:
            if sum_ok(m, w, 1):
                cur.add(m)
    if not cur:
        return False
    for l in range(1, q - 1):
        cand = set()
        for c in circles:
            cand |= c[l + 1]
        nxt = set()
        for T in cand:
            if not sum_ok(T, w, l + 1):
                continue
            mm = T
            while mm:
                b = mm & -mm
                if (T ^ b) in cur:
                    nxt.add(T)
                    break
                mm ^= b
        cur = nxt
        if not cur:
            return False
    return True

def single_accepts_fast(w, q):
    """Identity-circle single-copy acceptance, O(q^2) bit-DP, independent coding."""
    # std intervals [s, s+L); reach mask over starts s
    full = (1 << q) - 1
    # counts of ones in [s, s+L) maintained incrementally
    cnt = [0] * q
    reach = 0
    for s in range(q):
        if (w >> s) & 1:
            reach |= 1 << s   # L=1 needs sum=+1
    cnt = [(w >> s) & 1 for s in range(q)]
    if reach == 0:
        return False
    for L in range(2, q):
        newcnt = [cnt[s] + ((w >> ((s + L - 1) % q)) & 1) for s in range(q)]
        okm = 0
        for s in range(q):
            d = 2 * newcnt[s] - L
            if (L & 1 and d == 1) or (not (L & 1) and d in (0, 2)):
                okm |= 1 << s
        # predecessors: [s, s+L) from [s, s+L-1) (extend right) or [s+1, s+L) (extend left)
        ext = reach | (((reach >> 1) | (reach << (q - 1))) & full)
        reach = ext & okm
        cnt = newcnt
        if reach == 0:
            return False
    return True

# ------------------------------------------------------------------- validation
def validate_small(seed=12345):
    rng = random.Random(seed)
    for n in (8, 10, 12):
        q = n - 1
        m = n // 2
        rr = rr_family(n)
        words = [sum(1 << i for i in c) for c in combinations(range(q), m)]
        # 1) single copy: literal vs walk vs fast
        br = by_rank(rr, n)
        idc = intervals_by_len(list(range(q)), q)
        for w in words:
            fv = word_to_fvals(w, n)
            a = literal_accepts(br, n, fv)
            b = union_accepts_walk(w, [idc], q)
            c = single_accepts_fast(w, q)
            assert a == b == c, (n, w, a, b, c)
        # 2) random INF-fixing pairs/triples: literal union vs walk union
        for t in (2, 3):
            for trial in range(6):
                perms = [list(range(q))]
                for _ in range(t - 1):
                    pf = list(range(q))
                    rng.shuffle(pf)
                    perms.append(pf)
                fam = set()
                circles = []
                for pf in perms:
                    perm = pf + [q]
                    fam |= apply_perm_fam(rr, perm)
                    circles.append(intervals_by_len(pf, q))
                brU = by_rank(fam, n)
                for w in words:
                    fv = word_to_fvals(w, n)
                    a = literal_accepts(brU, n, fv)
                    b = union_accepts_walk(w, circles, q)
                    assert a == b, (n, t, trial, w, a, b)
        # 3) an INF-moving copy: literal only (walk not asserted) - just run it
        perm = list(range(n))
        rng.shuffle(perm)
        fam = apply_perm_fam(rr, list(range(q)) + [q]) | apply_perm_fam(rr, perm)
        brU = by_rank(fam, n)
        acc = sum(1 for w in words if literal_accepts(brU, n, word_to_fvals(w, n)))
        print(f"n={n}: all cross-checks passed; sample INF-moving union accepts {acc}/{len(words)}")
    print("VALIDATION OK")

def count_single_rejects(n, verbose=True):
    q = n - 1
    m = n // 2
    rej = []
    for c in combinations(range(q), m):
        w = sum(1 << i for i in c)
        if not single_accepts_fast(w, q):
            rej.append(w)
    if verbose:
        print(f"n={n}: single-copy rejects {len(rej)} of C({q},{m})")
    return rej

if __name__ == "__main__":
    if sys.argv[1:] and sys.argv[1] == "validate":
        validate_small()
    elif sys.argv[1:] and sys.argv[1] == "rejects":
        n = int(sys.argv[2])
        rej = count_single_rejects(n)
        print(sorted(rej))

#!/usr/bin/env python3
"""cr_review_girth_scan.py — hostile-review scan of the asymptotic claims of
Theorem CR (corner_realizability.md sections 2, 3.2):

  A. delta-existence: for which (n, m1), m1 <= n/10, does the explicit
     construction find a valid displacement delta?
       - engine condition (Q disjoint from P and S; Q not +-1-adjacent to S)
       - doc-literal condition (additionally {p} \\cap {s} = empty)
     Records every failure of either condition.
  B. girth: computes the true directed girth of the explicit construction and
     compares it against the doc's claimed bound  girth >= n/3 - 3*delta - 3
     (section 3.2), and against the thresholds needed by section 3.3
     (> 6 for the pairs closed-set argument, >= 18 for the triples argument
      as written; >= 13 suffices with the sharp greedy constant).
  C. reports the minimum n after which girth >= 18 holds for m1=round(i1*n).

All code independent of the engine.
"""
import sys
from collections import deque

I1S = 0.060043244708778326

def build(n, m1, doc_literal=False):
    base = n // 3 + 1
    jmax = (n - 3) // 2
    if m1 == 0:
        return {x: (x + base) % n for x in range(n)}, 0
    P = [(i * n) // m1 % n for i in range(m1)]
    if len(set(P)) != m1:
        return None, "P collision"
    S = set((p - base) % n for p in P)
    if doc_literal and (set(P) & S):
        return None, f"P-cap-S={sorted(set(P)&S)}"
    spacing = n // m1
    hi = min(spacing - 2, jmax - base)
    for d in range(2, hi + 1):
        Q = set((p + d) % n for p in P)
        if Q & set(P) or Q & S:
            continue
        if any(((q - 1) % n) in S or ((q + 1) % n) in S for q in Q):
            continue
        g = {x: (x + base) % n for x in range(n)}
        for p in P:
            g[(p - base) % n] = (p + d) % n
        return g, d
    return None, "no delta in range"

def girth(n, g):
    out = [((x + 1) % n, g[x]) for x in range(n)]
    best = None
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            nd = dist[v] + 1
            if best is not None and nd >= best:
                continue
            for u in out[v]:
                if u == s:
                    best = nd if best is None else min(best, nd)
                elif dist[u] < 0:
                    dist[u] = nd
                    q.append(u)
    return best

def main():
    # ---- A. delta existence over a large grid ----
    eng_fail, doc_fail_examples, doc_fail_count, tot = [], [], 0, 0
    NMAX_EXIST = 1200
    for n in range(26, NMAX_EXIST + 1):
        for m1 in range(0, n // 10 + 1):
            tot += 1
            g, d = build(n, m1)
            if g is None:
                eng_fail.append((n, m1, d))
            gd, dd = build(n, m1, doc_literal=True)
            if gd is None:
                doc_fail_count += 1
                if len(doc_fail_examples) < 12:
                    doc_fail_examples.append((n, m1, dd))
    print(f"A. delta-existence scan n in [26,{NMAX_EXIST}], all m1 <= n/10 "
          f"({tot} pairs):")
    print(f"   engine-condition failures: {len(eng_fail)}")
    for f in eng_fail[:10]:
        print(f"      FAIL {f}")
    print(f"   doc-literal-condition failures ({{p}} cap {{s}} nonempty or no delta): "
          f"{doc_fail_count}")
    for f in doc_fail_examples:
        print(f"      e.g. {f}")

    # ---- B. girth vs doc bound ----
    print("\nB. girth of the explicit construction vs doc bound n/3 - 3*delta - 3:")
    print("   n    m1  delta  girth   docbound  ok?   (m1 = round(i1* n) unless noted)")
    viol = []
    first18 = None
    ns = list(range(26, 401, 2)) + [450, 500, 600, 700, 800]
    for n in ns:
        m1 = round(I1S * n)
        g, d = build(n, m1)
        if g is None:
            print(f"   {n:4d} {m1:3d}  BUILD FAIL {d}")
            continue
        gr = girth(n, g)
        bound = n / 3 - 3 * d - 3
        ok = gr >= bound
        if not ok:
            viol.append((n, m1, d, gr, bound))
        if first18 is None and gr >= 18:
            first18 = n
        if n <= 130 or n % 20 == 0 or not ok:
            print(f"   {n:4d} {m1:3d} {d:5d} {gr:6d} {bound:9.2f}  {'ok' if ok else '**VIOLATED**'}")
    print(f"\n   doc girth-bound violations: {len(viol)}")
    for v in viol[:20]:
        print(f"      n={v[0]} m1={v[1]} delta={v[2]} girth={v[3]} < bound {v[4]:.2f}")
    print(f"   first n with girth >= 18 (m1=round(i1*n)): {first18}")

    # minimum girth over ALL m1 <= n/10 for a few n (worst-case corner of the
    # theorem's quantifier)
    print("\n   worst-case girth over all m1 <= n/10:")
    for n in (60, 100, 150, 200, 260, 320, 400):
        worst = None
        for m1 in range(0, n // 10 + 1):
            g, d = build(n, m1)
            if g is None:
                continue
            gr = girth(n, g)
            if worst is None or gr < worst[0]:
                worst = (gr, m1, d)
        print(f"   n={n:4d}: min girth {worst[0]} at m1={worst[1]} (delta={worst[2]})")

    # ---- C. the specific counterexample candidate n=200, m1=11 ----
    print("\nC. targeted: n=200 m1=11 (predicted special-chain cycle of length 52):")
    g, d = build(200, 11)
    gr = girth(200, g)
    print(f"   delta={d} girth={gr} docbound={200/3 - 3*d - 3:.2f} "
          f"{'** doc bound VIOLATED **' if gr < 200/3 - 3*d - 3 else 'bound holds'}")

if __name__ == "__main__":
    main()

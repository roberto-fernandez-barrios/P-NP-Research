"""Exact middle switch depth D_mid for two-order unions.

D_mid = maximum, over all coloring-free nested chains I_1 ⊂ … ⊂ I_{q-1}
(|I_j| = j, each a cyclic interval of at least one of the two orders), of the
number of switches counted only among sets of sizes in [3, q-3]:
for t = 2 the minimum block count of a chain equals 1 + (number of adjacent
unequal pairs in the subsequence of single-label elements), so we maximize
alternations of the "only" labels with a DP over (descriptor, last-only).

Usage: python -B experiments/cycle05_switch_depth.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cycle05_hybrid_core import OrderData  # noqa: E402


def d_mid(q: int, perm: list[int]) -> int:
    orders = [tuple(range(q)), tuple(perm[i] for i in range(q))]
    data = [OrderData(o) for o in orders]
    # per size: dict mask -> label set
    bylen: list[dict[int, int]] = [dict() for _ in range(q)]
    for o, od in enumerate(data):
        for L in range(1, q):
            d = bylen[L]
            for s in range(q):
                m = od.interval_mask(s, L)
                d[m] = d.get(m, 0) | (1 << o)
    # DP over sizes: state (mask, last_only in {0,1,2}) -> max middle alternations
    # last_only: 0 = none seen yet, 1 = order1, 2 = order2
    cur: dict[tuple[int, int], int] = {}
    for m, lab in bylen[1].items():
        lo = 0  # sizes < 3 don't count as middle "only" elements
        cur[(m, lo)] = 0
    best = 0
    for L in range(2, q):
        nxt: dict[tuple[int, int], int] = {}
        for m, lab in bylen[L].items():
            for (pm, plast), val in cur.items():
                if pm & ~m != 0:
                    continue
                # determine label contribution at this size
                if 3 <= L <= q - 3 and lab in (1, 2):
                    only = 1 if lab == 1 else 2
                    nv = val + (1 if plast != 0 and plast != only else 0)
                    nl = only
                else:
                    nv, nl = val, plast
                key = (m, nl)
                if nv > nxt.get(key, -1):
                    nxt[key] = nv
        cur = nxt
        if cur:
            best = max(best, max(cur.values()))
    return best


def transposition(q: int, u: int, v: int) -> list[int]:
    p = list(range(q))
    p[u], p[v] = p[v], p[u]
    return p


def pairswap(q: int) -> list[int]:
    p = list(range(q))
    for i in range(0, q - 1, 2):
        p[i], p[i + 1] = p[i + 1], p[i]
    return p


def mult(q: int, a: int) -> list[int]:
    return [(a * i) % q for i in range(q)]


def blockswap(q: int, a: int, b: int, ln: int) -> list[int]:
    p = list(range(q))
    for i in range(ln):
        p[(a + i) % q], p[(b + i) % q] = p[(b + i) % q], p[(a + i) % q]
    return p


if __name__ == "__main__":
    for q in (13, 17, 21):
        rows = []
        rows.append(("mult2", mult(q, 2)))
        rows.append(("mult5", mult(q, 5)))
        for d in (2, q // 4, q // 2):
            rows.append((f"transp(0,{d})", transposition(q, 0, d)))
        rows.append(("pairswap", pairswap(q)))
        rows.append((f"blockswap(0,{q//2},3)", blockswap(q, 0, q // 2, 3)))
        rows.append((f"blockswap(0,{q//2},{q//4})", blockswap(q, 0, q // 2, q // 4)))
        out = ", ".join(f"{name}: {d_mid(q, p)}" for name, p in rows)
        print(f"q={q}: {out}", flush=True)

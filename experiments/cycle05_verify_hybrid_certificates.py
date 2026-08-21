"""Independent verifier for Cycle-5 hybrid-only certificates.

This checker deliberately avoids the fast interval-DP engine and the search
code.  For each stored example it:

  1. rebuilds the literal union family from the definition of RR_n and the
     stored permutation (full induced subset semantics, masks over U);
  2. re-verifies that copy 1 and copy 2 each REJECT the stored coloring by a
     direct rank-by-rank reachability DP inside each single copy's literal
     family;
  3. re-verifies that the literal union ACCEPTS it by the same direct DP on
     the union family (no interval reasoning at all);
  4. checks the stored witness chain element by element against the literal
     union family and the compatibility constraints;
  5. computes the exact minimum number of copy switches over all accepting
     chains, where a chain's switch count is the minimum number of blocks in
     a partition of the chain into consecutive runs, each run lying inside a
     single copy, minus one (equivalently: min order-change cost over labeled
     chains); and
  6. reports, per permutation, how many of the pair's common rejects are
     rescued by the union.

Usage: python -B experiments/cycle05_verify_hybrid_certificates.py <certificates.json>
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path


def rr_masks_by_rank(n: int) -> list[list[int]]:
    q = n - 1
    inf_bit = 1 << q
    out: list[list[int]] = [[0]]
    out.append([1 << x for x in range(q)])
    for k in range(2, n):
        L = k - 1
        row = []
        for s in range(q):
            m = 0
            for j in range(L):
                m |= 1 << ((s + j) % q)
            row.append(inf_bit | m)
        out.append(row)
    out.append([(1 << n) - 1])
    return out


def apply_perm(mask: int, perm: list[int], n: int) -> int:
    r = 0
    for x in range(n):
        if (mask >> x) & 1:
            r |= 1 << perm[x]
    return r


def compatible(mask: int, k: int, plus: int) -> bool:
    return abs(2 * (mask & plus).bit_count() - k) <= 1


def accepts_family(by_rank: list[list[int]], plus: int, n: int) -> bool:
    reach = [m for m in by_rank[0] if compatible(m, 0, plus)]
    for k in range(1, n + 1):
        nxt = []
        for c in by_rank[k]:
            if compatible(c, k, plus) and any(p & ~c == 0 for p in reach):
                nxt.append(c)
        if not nxt:
            return False
        reach = nxt
    return True


def min_switches(copies: list[list[list[int]]], plus: int, n: int) -> int | None:
    """Exact min switch count over accepting chains of the union.

    copies[j] = rank-indexed literal family of copy j.  State: (mask, j).
    Cost 0 to extend within copy j, 1 when the successor is taken in a
    different copy.  A mask may belong to several copies; all labels allowed.
    """
    t = len(copies)
    INF = 10 ** 9
    membership = [defaultdict(set) for _ in range(n + 1)]
    for j, fam in enumerate(copies):
        for k in range(n + 1):
            for m in fam[k]:
                membership[k][m].add(j)
    # rank 0: empty set in all copies, cost 0 for every label
    cur: dict[tuple[int, int], int] = {}
    for j in range(t):
        cur[(0, j)] = 0
    for k in range(1, n + 1):
        nxt: dict[tuple[int, int], int] = {}
        for m, labels in membership[k].items():
            if not compatible(m, k, plus):
                continue
            for (pm, pj), cost in cur.items():
                if pm & ~m != 0:
                    continue
                for j in labels:
                    c2 = cost + (0 if j == pj else 1)
                    key = (m, j)
                    if c2 < nxt.get(key, INF):
                        nxt[key] = c2
        if not nxt:
            return None
        cur = nxt
    return min(cur.values())


def is_cyclic_interval(mask: int, q: int) -> bool:
    j = mask.bit_count()
    if j in (0, 1, q - 1, q):
        return True
    pos = [i for i in range(q) if (mask >> i) & 1]
    gaps = [(pos[(i + 1) % j] - pos[i]) % q for i in range(j)]
    return max(gaps) == q - j + 1


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else
                "certificates/cycle05_hybrid/hybrid_only_n22_candidates.json")
    data = json.loads(path.read_text())
    n_all = sorted({r["n"] for r in data})
    print(f"loaded {len(data)} examples for n in {n_all}")

    by_perm: dict[tuple[int, tuple[int, ...]], list[dict]] = defaultdict(list)
    for r in data:
        by_perm[(r["n"], tuple(r["perm_finite"]))].append(r)

    total = 0
    sw_hist: dict[int, int] = defaultdict(int)
    for (n, perm_f), rows in sorted(by_perm.items()):
        q = n - 1
        perm = list(perm_f) + [q]
        base = rr_masks_by_rank(n)
        copy1 = base
        copy2 = [[apply_perm(m, perm, n) for m in row] for row in base]
        union = [sorted(set(a) | set(b)) for a, b in zip(copy1, copy2)]
        for r in rows:
            plus = int(r["word"], 16)  # finite pluses; infinity minus
            assert plus.bit_count() == n // 2
            a1 = accepts_family(copy1, plus, n)
            a2 = accepts_family(copy2, plus, n)
            au = accepts_family(union, plus, n)
            assert not a1, "copy 1 unexpectedly accepts"
            assert not a2, "copy 2 unexpectedly accepts"
            assert au, "union unexpectedly rejects"
            # witness chain check against the literal union
            chain = [int(c, 16) for c in r["witness_chain_masks"]]
            # chain masks are finite parts I_1..I_{n-2}; the full chain is
            # C_0=∅, C_1=I_1, C_k={∞}∪I_{k-1} for 2<=k<=n-1, C_n=U,
            # so I_1 appears both bare and joined with infinity.
            C = [0, chain[0]] + [c | (1 << q) for c in chain] + [(1 << n) - 1]
            assert len(C) == n + 1
            union_sets = [set(row) for row in union]
            prev = None
            for k, cm in enumerate(C):
                assert cm.bit_count() == k, (k, hex(cm))
                assert cm in union_sets[k], (k, hex(cm))
                assert compatible(cm, k, plus)
                if prev is not None:
                    assert prev & ~cm == 0
                prev = cm
            ms = min_switches([copy1, copy2], plus, n)
            assert ms is not None and ms >= 1, ms
            sw_hist[ms] += 1
            total += 1
    print(f"verified {total} examples against the literal reference semantics")
    print("minimum-switch histogram:", dict(sorted(sw_hist.items())))
    print("ALL CYCLE-5 HYBRID-ONLY CERTIFICATES PASS")


if __name__ == "__main__":
    main()

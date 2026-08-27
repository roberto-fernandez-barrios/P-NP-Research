"""Cycle 5 core library: literal unions of relabelled RR_n copies and hybrid paths.

Written from scratch for Research Cycle 5.  It does not import any Cycle-4
experiment code; agreement with the Cycle-4 certificates is used as a check,
never as a premise.

Conventions
-----------
n = 2m even, q = n-1.  Ground set U = Z_q union {infinity}; the infinity
point carries the integer label q.  Subsets of U are Python ints with bit x
set iff point x is in the subset (bits 0..q).

The literal corrected family RR_n:
  rank 0: empty set
  rank 1: every finite singleton {x}, x in Z_q
  rank k, 2<=k<=n-1: {infinity} union I, I a cyclic interval of Z_q with
                     |I| = k-1
  rank n: U.

A relabelled copy is pi(RR_n) = {pi(S) : S in RR_n} for a permutation pi of
U (pi need not fix infinity).  The union family F(P) = union of the copies,
as a set of literal subsets.  Acceptance is through the full induced
inclusion-by-one DAG on the literal subsets: a balanced coloring f is
accepted iff there is a chain empty=C_0 subset C_1 subset ... subset C_n=U
with |C_k|=k, every C_k in F(P), and |f(C_k)| <= 1 for all k.

Colorings: a coloring is the set (bitmask) of PLUS points; balanced means
popcount = n/2.  Acceptance is invariant under global sign flip, so we
normalize f(infinity) = -1 (infinity not in the plus mask); a normalized
coloring is a q-bit word with exactly m one-bits (the finite plus points).

Cyclic orders: an order is a tuple `ord` of length q, position i holds point
ord[i].  Its interval family Int(ord) = point sets occupying cyclically
consecutive positions.  Copy pi (infinity-fixing) has finite interval family
Int(C2) with C2[i] = pi(i): pi(RR_n) rank-k sets are {infinity} union pi(I),
and {pi(I) : I std interval} = Int(C2).
"""

from __future__ import annotations

import itertools
import random
from functools import lru_cache

# ---------------------------------------------------------------------------
# literal families as bitmask sets
# ---------------------------------------------------------------------------


def rr_family_masks(n: int) -> list[list[int]]:
    """Literal RR_n by rank; masks over n bits (bit q = infinity)."""
    q = n - 1
    inf_bit = 1 << q
    full = (1 << n) - 1
    by_rank: list[list[int]] = [[] for _ in range(n + 1)]
    by_rank[0].append(0)
    for x in range(q):
        by_rank[1].append(1 << x)
    for k in range(2, n):
        L = k - 1
        for s in range(q):
            mask = 0
            for j in range(L):
                mask |= 1 << ((s + j) % q)
            by_rank[k].append(inf_bit | mask)
    by_rank[n].append(full)
    return by_rank


def apply_perm_mask(mask: int, perm: list[int], n: int) -> int:
    out = 0
    for x in range(n):
        if (mask >> x) & 1:
            out |= 1 << perm[x]
    return out


def union_family_masks(n: int, perms: list[list[int]]) -> list[list[int]]:
    """Literal union of pi(RR_n) over pi in perms, deduplicated, by rank."""
    base = rr_family_masks(n)
    by_rank: list[list[int]] = []
    for k in range(n + 1):
        seen: set[int] = set()
        for perm in perms:
            for mask in base[k]:
                seen.add(apply_perm_mask(mask, perm, n))
        by_rank.append(sorted(seen))
    return by_rank


# ---------------------------------------------------------------------------
# reference acceptance: full induced inclusion-by-one DAG, any family
# ---------------------------------------------------------------------------


def brute_accepts(by_rank: list[list[int]], plus_mask: int, n: int) -> bool:
    """Reference semantics.  plus_mask over n bits; |f(S)| = |2|S∩plus|-|S||."""

    def compatible(mask: int, k: int) -> bool:
        return abs(2 * (mask & plus_mask).bit_count() - k) <= 1

    reachable = [m for m in by_rank[0] if compatible(m, 0)]
    for k in range(1, n + 1):
        nxt = []
        for cand in by_rank[k]:
            if not compatible(cand, k):
                continue
            for prev in reachable:
                if prev & ~cand == 0:  # prev subset of cand (ranks differ by 1)
                    nxt.append(cand)
                    break
        if not nxt:
            return False
        reachable = nxt
    return True


# ---------------------------------------------------------------------------
# fast acceptance for infinity-fixing copies: interval-growth DP
# ---------------------------------------------------------------------------


class OrderData:
    """Precomputed data for one cyclic order on Z_q."""

    __slots__ = ("q", "order", "pos", "prefix")

    def __init__(self, order: tuple[int, ...]):
        q = len(order)
        self.q = q
        self.order = order
        self.pos = [0] * q
        for i, x in enumerate(order):
            self.pos[x] = i
        # prefix[i] = OR of point bits at positions 0..i-1 (0 <= i <= q)
        pref = [0] * (q + 1)
        for i, x in enumerate(order):
            pref[i + 1] = pref[i] | (1 << x)
        self.prefix = pref

    def interval_mask(self, s: int, length: int) -> int:
        """Point-set mask of the interval of given length starting at position s."""
        q = self.q
        s %= q
        e = s + length
        if e <= q:
            return self.prefix[e] ^ self.prefix[s]
        full = self.prefix[q]
        return full ^ (self.prefix[s] ^ self.prefix[e - q])


def make_multiplier_order(q: int, a: int, b: int = 0) -> tuple[int, ...]:
    """Order whose position i holds a*i+b mod q (copy of RR under x -> a x + b)."""
    return tuple((a * i + b) % q for i in range(q))


class UnionEngine:
    """Acceptance engine for the union of infinity-fixing copies.

    orders: list of position->point tuples (the first is usually identity).
    Precomputes, for every length L, the set-level identifications:
      eq[L]:    list of groups of descriptors (o,s) denoting the same set
      cross[L]: list of pairs ((o,s) at length L, (o2,s2) at length L+1)
                with interval_o(s,L) subset interval_o2(s2,L+1), o != o2 as
                sets related by adding one point.
    Only genuinely cross-order arrows are stored: same-order growth is
    handled by the shift step of the DP.
    """

    def __init__(self, orders: list[tuple[int, ...]]):
        self.q = len(orders[0])
        q = self.q
        self.t = len(orders)
        self.data = [OrderData(o) for o in orders]
        # per length: dict mask -> list of (order_index, start)
        self.bylen: list[dict[int, list[tuple[int, int]]]] = [dict() for _ in range(q)]
        for o, od in enumerate(self.data):
            for L in range(1, q):
                d = self.bylen[L]
                for s in range(q):
                    d.setdefault(od.interval_mask(s, L), []).append((o, s))
        # cross arrows between consecutive lengths (any pair of orders,
        # including o==o2 when the added point is interior in o2 —
        # impossible for intervals of the same order, so o2 != o there,
        # but keep the general test)
        self.cross: list[list[tuple[tuple[int, int], tuple[int, int]]]] = [
            [] for _ in range(q)
        ]
        for L in range(1, q - 1):
            lower = self.bylen[L]
            arrows = self.cross[L]
            for o2, od2 in enumerate(self.data):
                for s2 in range(q):
                    big = od2.interval_mask(s2, L + 1)
                    mm = big
                    while mm:
                        bit = mm & -mm
                        mm ^= bit
                        sub = big ^ bit
                        hit = lower.get(sub)
                        if hit:
                            for (o, s) in hit:
                                # skip pure same-order end-growth (handled by shift)
                                if o == o2 and (
                                    s2 % q == s % q
                                    or (s2 % q) == (s - 1) % q
                                ):
                                    continue
                                arrows.append(((o, s), (o2, s2)))

    def accepts(self, word: int) -> bool:
        """word: q-bit plus mask over Z_q (normalized coloring).

        Chain semantics: nested I_1 subset ... subset I_{q-1}, |I_j| = j, each
        an interval of at least one order, with running plus-count constraint
          odd j:  plus(I_j) = (j+1)//2      (sign sum exactly +1)
          even j: plus(I_j) in {j//2, j//2+1}  (sign sum 0 or 2).
        Sizes 1 and q-1 are intervals in every order automatically.
        Accept iff some I_{q-1} reachable (final steps are then forced fine).
        """
        q = self.q
        data = self.data
        # plus-count prefix per order
        pc = []
        for od in data:
            arr = [0] * (q + 1)
            for i, x in enumerate(od.order):
                arr[i + 1] = arr[i] + ((word >> x) & 1)
            pc.append(arr)

        def plus_count(o: int, s: int, L: int) -> int:
            s %= q
            e = s + L
            if e <= q:
                return pc[o][e] - pc[o][s]
            return pc[o][q] - pc[o][s] + pc[o][e - q]

        def ok(o: int, s: int, L: int) -> bool:
            p = plus_count(o, s, L)
            if L & 1:
                return p == (L + 1) // 2
            return p == L // 2 or p == L // 2 + 1

        # reachable descriptor sets per order as q-bit masks of starts
        reach = [0] * self.t
        for o in range(self.t):
            m = 0
            od = data[o]
            for s in range(q):
                if (word >> od.order[s]) & 1:  # singleton at position s is plus
                    m |= 1 << s
            reach[o] = m
        if not any(reach):
            return False

        fullq = (1 << q) - 1
        for L in range(1, q - 1):
            # sync: same set known under several descriptors at length L
            if self.t > 1:
                for mask, lst in self.bylen[L].items():
                    if len(lst) > 1:
                        if any((reach[o] >> s) & 1 for (o, s) in lst):
                            for (o, s) in lst:
                                reach[o] |= 1 << s
            nxt = [0] * self.t
            # same-order end growth: start s keeps or start s-1
            for o in range(self.t):
                r = reach[o]
                if r:
                    # length L start s grows to (s, L+1) or (s-1, L+1)
                    grown = r | ((r >> 1) | ((r & 1) << (q - 1))) & fullq
                    nxt[o] = grown
            # cross arrows
            for (osrc, odst) in self.cross[L]:
                (o, s) = osrc
                if (reach[o] >> s) & 1:
                    (o2, s2) = odst
                    nxt[o2] |= 1 << (s2 % q)
            # compatibility filter at length L+1
            for o in range(self.t):
                r = nxt[o]
                if not r:
                    continue
                keep = 0
                m = r
                while m:
                    b = m & -m
                    m ^= b
                    s = b.bit_length() - 1
                    if ok(o, s, L + 1):
                        keep |= b
                nxt[o] = keep
            reach = nxt
            if not any(reach):
                return False
        return True

    def accepts_with_witness(self, word: int):
        """Like accepts, but returns (True, chain_of_masks) or (False, None).

        chain_of_masks lists I_1..I_{q-1} as point masks.
        """
        q = self.q
        data = self.data
        pc = []
        for od in data:
            arr = [0] * (q + 1)
            for i, x in enumerate(od.order):
                arr[i + 1] = arr[i] + ((word >> x) & 1)
            pc.append(arr)

        def plus_count(o, s, L):
            s %= q
            e = s + L
            if e <= q:
                return pc[o][e] - pc[o][s]
            return pc[o][q] - pc[o][s] + pc[o][e - q]

        def ok(o, s, L):
            p = plus_count(o, s, L)
            if L & 1:
                return p == (L + 1) // 2
            return p == L // 2 or p == L // 2 + 1

        layers: list[dict[tuple[int, int], tuple | None]] = []
        cur: dict[tuple[int, int], tuple | None] = {}
        for o in range(self.t):
            od = data[o]
            for s in range(q):
                if (word >> od.order[s]) & 1:
                    cur[(o, s)] = None
        layers.append(cur)
        if not cur:
            return False, None
        for L in range(1, q - 1):
            cur = layers[-1]
            # sync
            for mask, lst in self.bylen[L].items():
                if len(lst) > 1:
                    src = next(((o, s) for (o, s) in lst if (o, s) in cur), None)
                    if src is not None:
                        for d in lst:
                            if d not in cur:
                                cur[d] = ("eq", src)
            nxt: dict[tuple[int, int], tuple | None] = {}
            for (o, s) in cur:
                for s2 in (s, (s - 1) % q):
                    if ok(o, s2, L + 1) and (o, s2) not in nxt:
                        nxt[(o, s2)] = ("grow", (o, s))
            for (osrc, odst) in self.cross[L]:
                if osrc in cur:
                    (o2, s2) = odst
                    if ok(o2, s2 % q, L + 1) and (o2, s2 % q) not in nxt:
                        nxt[(o2, s2 % q)] = ("cross", osrc)
            layers.append(nxt)
            if not nxt:
                return False, None
        # backtrack from any final descriptor; layers[L-1] holds length L
        cur_d = next(iter(layers[-1]))
        curL = q - 1
        masks = []
        while True:
            masks.append(data[cur_d[0]].interval_mask(cur_d[1], curL))
            if curL == 1:
                break
            entry = layers[curL - 1][cur_d]
            while entry is not None and entry[0] == "eq":
                cur_d = entry[1]
                entry = layers[curL - 1][cur_d]
            assert entry is not None, "non-initial layer entry missing provenance"
            cur_d = entry[1]
            curL -= 1
        masks.reverse()
        return True, masks


# ---------------------------------------------------------------------------
# single-copy bit-parallel recurrence (independent recount tool)
# ---------------------------------------------------------------------------


def single_copy_rejects_word(word: int, q: int) -> bool:
    """True iff RR_n rejects the normalized coloring `word` (q-bit plus mask).

    Independent implementation of the odd-interval growth recurrence derived
    in Cycle 5 from the literal family: R_1 = plus positions; R_{l+2} allows
    left-left, split, right-right opposite-sign extensions; accept iff some
    start survives to length q ... equivalently length q-2 then forced.
    Here we run to length q (the full cycle) exactly as derived.
    """
    w = word
    R = w  # starts i with w_i = 1, length 1
    L = 1
    while L + 2 <= q:
        # start i, length L; interval covers i..i+L-1
        nxt = 0
        # left-left: new start i-2, requires w_{i-2} != w_{i-1}
        # split: new start i-1, requires w_{i-1} != w_{i+L}
        # right-right: start i, requires w_{i+L} != w_{i+L+1}
        m = R
        while m:
            b = m & -m
            m ^= b
            i = b.bit_length() - 1
            if ((w >> ((i - 2) % q)) & 1) != ((w >> ((i - 1) % q)) & 1):
                nxt |= 1 << ((i - 2) % q)
            if ((w >> ((i - 1) % q)) & 1) != ((w >> ((i + L) % q)) & 1):
                nxt |= 1 << ((i - 1) % q)
            if ((w >> ((i + L) % q)) & 1) != ((w >> ((i + L + 1) % q)) & 1):
                nxt |= 1 << (i % q)
        R = nxt
        L += 2
        if not R:
            return True
    return R == 0


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def normalized_words(q: int, m: int):
    """All q-bit words with m one-bits (as ints)."""
    for combo in itertools.combinations(range(q), m):
        w = 0
        for c in combo:
            w |= 1 << c
        yield w


def word_of_perm_pullback(word: int, perm_finite: list[int], q: int) -> int:
    """Word of f∘pi for infinity-fixing pi: (f∘pi)(x) = f(pi(x))."""
    out = 0
    for x in range(q):
        if (word >> perm_finite[x]) & 1:
            out |= 1 << x
    return out


def rotations(word: int, q: int):
    full = (1 << q) - 1
    w = word
    for _ in range(q):
        yield w
        w = ((w << 1) | (w >> (q - 1))) & full


def word_from_runs(runs: list[tuple[int, int]]) -> int:
    """runs: list of (bit, length) from position 0 upward."""
    w = 0
    pos = 0
    for bit, length in runs:
        for _ in range(length):
            if bit:
                w |= 1 << pos
            pos += 1
    return w


# ---------------------------------------------------------------------------
# self-tests
# ---------------------------------------------------------------------------


def _self_test():
    rng = random.Random(20260821)
    # 1) union counts: identity-only family equals RR_n literal count
    for n in (8, 10, 12):
        fam = union_family_masks(n, [list(range(n))])
        total = sum(len(r) for r in fam)
        assert total == (n - 1) ** 2 + 2, (n, total)

    # 2) brute force vs fast DP on all normalized colorings, several perm lists
    for n in (8, 10, 12):
        q, m = n - 1, n // 2
        ident = list(range(n))
        perm_lists = [[ident]]
        for _ in range(3):
            p = list(range(q))
            rng.shuffle(p)
            perm_lists.append([ident, p + [q]])
        for _ in range(2):
            p1 = list(range(q))
            p2 = list(range(q))
            rng.shuffle(p1)
            rng.shuffle(p2)
            perm_lists.append([ident, p1 + [q], p2 + [q]])
        for perms in perm_lists:
            fam = union_family_masks(n, perms)
            orders = [tuple(p[i] for i in range(q)) for p in perms]
            eng = UnionEngine(orders)
            for wrd in normalized_words(q, m):
                b = brute_accepts(fam, wrd, n)  # plus mask: infinity minus
                f = eng.accepts(wrd)
                assert b == f, (n, perms, bin(wrd), b, f)
                acc, chain = eng.accepts_with_witness(wrd)
                assert acc == f
                if acc:
                    _check_chain(chain, wrd, orders)

    # 3) single-copy recurrence agrees with fast DP at n=12,14
    for n in (12, 14):
        q, m = n - 1, n // 2
        eng = UnionEngine([tuple(range(q))])
        for wrd in normalized_words(q, m):
            assert eng.accepts(wrd) == (not single_copy_rejects_word(wrd, q))

    # 4) the known n=22 failure word is rejected by the single copy
    q = 21
    w22 = word_from_runs([(1, 8), (0, 5), (1, 3), (0, 5)])
    assert single_copy_rejects_word(w22, q)
    eng = UnionEngine([tuple(range(q))])
    assert not eng.accepts(w22)
    # and every rotation is rejected
    for r in rotations(w22, q):
        assert single_copy_rejects_word(r, q)
    print("cycle05_hybrid_core self-tests PASS")


def _check_chain(chain_masks: list[int], word: int, orders):
    """Independent witness check: nested, sizes, interval-in-some-order, sums."""
    q = len(orders[0])
    datas = [OrderData(o) for o in orders]
    prev = None
    for j, mask in enumerate(chain_masks, start=1):
        assert mask.bit_count() == j
        if prev is not None:
            assert prev & ~mask == 0
        prev = mask
        if 1 <= j <= q - 1:
            ok = False
            for od in datas:
                pos = sorted(od.pos[x] for x in range(q) if (mask >> x) & 1)
                gaps = [(pos[(i + 1) % j] - pos[i]) % q for i in range(j)]
                if j == q or max(gaps) == q - j + 1 or j == 1:
                    ok = True
                    break
                # interval iff exactly one gap greater than 1 and rest 1
                if sorted(gaps) == [1] * (j - 1) + [q - j + 1]:
                    ok = True
                    break
            assert ok, (j, bin(mask))
        p = (mask & word).bit_count()
        s = 2 * p - j
        if j % 2 == 1:
            assert s == 1
        else:
            assert s in (0, 2)


if __name__ == "__main__":
    _self_test()

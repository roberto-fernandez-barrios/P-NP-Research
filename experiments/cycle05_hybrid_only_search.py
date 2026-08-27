"""Cycle 5 Phase 5C: search for the smallest hybrid-only two-copy example.

A hybrid-only example at n is a pair of relabelings (WLOG copy 1 = identity)
and a normalized balanced coloring f such that

  copy 1 rejects f,  copy 2 = pi(RR_n) rejects f,  the literal union accepts f.

Since RR_n accepts every balanced coloring for even n <= 20 and relabeling
preserves acceptance of everything, n = 22 is the smallest candidate.

Copy 2 rejects f  iff  RR_n rejects f∘pi (relabeling equivariance), i.e. iff
the pulled-back word lies in the rejection set R_n of the identity copy.

Search strategy (structured first): candidate pi are word-compatible block
moves of the finite circle Z_q:

  * swap of two disjoint arcs whose color patterns under f agree;
  * reversal of an arc whose color pattern is a palindrome;
  * internal rotation of an arc (pattern invariant under that rotation);
  * compositions of two such moves.

These keep f∘pi = f (so f stays in both rejection sets) while creating rich
common-interval structure between the two cyclic orders, which is exactly
what hybrid switching needs.  A random-coset sampler is included as a
control.

Usage:
  python -B experiments/cycle05_hybrid_only_search.py --n 22
  python -B experiments/cycle05_hybrid_only_search.py --n 24 --failures certificates/cycle04_rr_acceptance/cycle04_rr_failures_n24.txt
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cycle05_hybrid_core import (  # noqa: E402
    OrderData,
    UnionEngine,
    _check_chain,
    rotations,
    single_copy_rejects_word,
    word_from_runs,
    word_of_perm_pullback,
)


def arc(points_start: int, length: int, q: int) -> list[int]:
    return [(points_start + i) % q for i in range(length)]


def pattern(word: int, positions: list[int]) -> tuple[int, ...]:
    return tuple((word >> p) & 1 for p in positions)


def perm_from_moves(q: int, mapping: dict[int, int]) -> list[int] | None:
    """Total permutation of Z_q from a partial point mapping; identity elsewhere."""
    perm = list(range(q))
    for src, dst in mapping.items():
        perm[src] = dst
    if len(set(perm)) != q:
        return None
    return perm


def swap_arcs_perm(q: int, a: int, b: int, length: int) -> list[int] | None:
    """pi exchanging arc [a,a+len) with [b,b+len) pointwise; None if overlap."""
    A, B = arc(a, length, q), arc(b, length, q)
    if set(A) & set(B):
        return None
    mapping = {}
    for x, y in zip(A, B):
        mapping[x] = y
        mapping[y] = x
    return perm_from_moves(q, mapping)


def reverse_arc_perm(q: int, a: int, length: int) -> list[int]:
    A = arc(a, length, q)
    mapping = {A[i]: A[length - 1 - i] for i in range(length)}
    return perm_from_moves(q, mapping)


def rotate_arc_perm(q: int, a: int, length: int, d: int) -> list[int]:
    A = arc(a, length, q)
    mapping = {A[i]: A[(i + d) % length] for i in range(length)}
    return perm_from_moves(q, mapping)


def compose(p1: list[int], p2: list[int]) -> list[int]:
    """(p1 ∘ p2)(x) = p1[p2[x]]."""
    return [p1[p2[x]] for x in range(len(p1))]


def candidate_moves(word: int, q: int, max_len: int):
    """Yield (label, perm) word-preserving single moves: word∘pi = word.

    word∘pi = word means word[pi(x)] = word[x] for all x, i.e. pi maps each
    color class into itself.
    """
    seen: set[tuple[int, ...]] = set()

    def emit(label, perm):
        if perm is None:
            return None
        key = tuple(perm)
        if key in seen or all(perm[i] == i for i in range(q)):
            return None
        # word-preservation check
        for x in range(q):
            if (word >> perm[x]) & 1 != (word >> x) & 1:
                return None
        seen.add(key)
        return (label, perm)

    for length in range(1, max_len + 1):
        for a in range(q):
            pa = pattern(word, arc(a, length, q))
            # reversals of palindromic arcs
            if pa == pa[::-1]:
                r = emit(f"rev[{a},{length}]", reverse_arc_perm(q, a, length))
                if r:
                    yield r
            # swaps of equal-pattern disjoint arcs
            for b in range(a + 1, q):
                if pattern(word, arc(b, length, q)) == pa:
                    r = emit(f"swap[{a},{b},{length}]", swap_arcs_perm(q, a, b, length))
                    if r:
                        yield r
            # internal rotations of rotation-invariant arcs
            for d in range(1, length):
                if all(pa[i] == pa[(i + d) % length] for i in range(length)):
                    r = emit(f"rot[{a},{length},{d}]", rotate_arc_perm(q, a, length, d))
                    if r:
                        yield r


def analyze_pair(word: int, perm: list[int], q: int, rej_words: set[int]):
    """Return (common_rejects, hybrid_accepted_list) for copy pair (id, perm)."""
    ident = tuple(range(q))
    c2 = tuple(perm[i] for i in range(q))
    eng = None
    found = []
    common = []
    for f in set(rotations(word, q)) | rej_words:
        if f not in rej_words:
            continue
        fp = word_of_perm_pullback(f, perm, q)
        if fp in rej_words:
            common.append(f)
            if eng is None:
                eng = UnionEngine([ident, c2])
            if eng.accepts(f):
                found.append(f)
    return common, found, eng


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=22)
    ap.add_argument("--failures", type=str, default=None,
                    help="failure-necklace file; default: the n=22 word")
    ap.add_argument("--max-len", type=int, default=None)
    ap.add_argument("--compose2", action="store_true",
                    help="also try compositions of two single moves (slow)")
    ap.add_argument("--random-coset", type=int, default=0,
                    help="also try K random color-preserving permutations")
    ap.add_argument("--cross-orbit", action="store_true",
                    help="also try arc swaps/reversals mapping a failure "
                         "word to any (possibly different) failure word")
    ap.add_argument("--out", type=str, default=None)
    args = ap.parse_args()

    n = args.n
    q, m = n - 1, n // 2

    # rejection set of the identity copy: all rotations of all failure necklaces
    if args.failures:
        words = []
        for line in Path(args.failures).read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # cycle04_rr_acceptance failure lists are binary strings of
            # length q (LSB = position 0 at the right); multi_rr necklace
            # lists are hex.  Detect by charset and length.
            if set(line) <= {"0", "1"} and len(line) == q:
                w = int(line, 2)
            else:
                w = int(line, 16)
            assert w.bit_length() <= q and w.bit_count() == m, \
                f"bad failure word {line!r}: bits={w.bit_length()} weight={w.bit_count()}"
            words.append(w)
    else:
        assert n == 22
        words = [word_from_runs([(1, 8), (0, 5), (1, 3), (0, 5)])]
    rej_words: set[int] = set()
    for w0 in words:
        assert single_copy_rejects_word(w0, q), "stored failure not rejected!"
        rej_words.update(rotations(w0, q))
    print(f"n={n}: identity-copy rejection set = {len(rej_words)} words "
          f"({len(words)} orbits)")

    max_len = args.max_len or (q - 2)
    results = []
    tested = 0
    base_words = sorted(set(words))
    singles: list[tuple[str, list[int]]] = []
    for w0 in base_words:
        for label, perm in candidate_moves(w0, q, max_len):
            singles.append((f"w{w0:x}:{label}", perm))
    # dedupe permutations across base words
    seen_perm: set[tuple[int, ...]] = set()
    uniq: list[tuple[str, list[int]]] = []
    for label, perm in singles:
        k = tuple(perm)
        if k not in seen_perm:
            seen_perm.add(k)
            uniq.append((label, perm))
    print(f"single word-preserving moves to test: {len(uniq)}")

    def run_candidate(label: str, perm: list[int]):
        nonlocal tested
        tested += 1
        common, found, eng = analyze_pair(0, perm, q, rej_words)
        if found:
            for f in found:
                acc, chain = eng.accepts_with_witness(f)
                assert acc
                _check_chain(chain, f, [tuple(range(q)),
                                        tuple(perm[i] for i in range(q))])
                fp = word_of_perm_pullback(f, perm, q)
                assert single_copy_rejects_word(f, q)
                assert single_copy_rejects_word(fp, q)
                results.append({
                    "n": n,
                    "label": label,
                    "perm_finite": perm,
                    "word": f"{f:x}",
                    "pulled_back_word": f"{fp:x}",
                    "common_rejects_of_pair": len(common),
                    "witness_chain_masks": [f"{c:x}" for c in chain],
                })
                print(f"HYBRID-ONLY FOUND: {label} word={f:x} "
                      f"(pair has {len(common)} common rejects)")
        return bool(found)

    for label, perm in uniq:
        run_candidate(label, perm)
    print(f"after single moves: tested={tested}, found={len(results)}")

    if args.compose2 and not results:
        print("composing pairs of moves ...")
        for i in range(len(uniq)):
            for j in range(len(uniq)):
                if i == j:
                    continue
                label = f"{uniq[i][0]}∘{uniq[j][0]}"
                perm = compose(uniq[i][1], uniq[j][1])
                if all(perm[x] == x for x in range(q)):
                    continue
                if run_candidate(label, perm):
                    break
            if results:
                break
        print(f"after compositions: tested={tested}, found={len(results)}")

    if args.cross_orbit:
        print("cross-orbit arc moves (word maps to a possibly different "
              "failure word) ...")
        tried = set()
        for w0 in base_words:
            # all arc swaps, any content
            for length in range(1, q // 2 + 1):
                for a in range(q):
                    for b in range(q):
                        if a == b:
                            continue
                        perm = swap_arcs_perm(q, a, b, length)
                        if perm is None:
                            continue
                        pull = word_of_perm_pullback(w0, perm, q)
                        if pull not in rej_words:
                            continue
                        key = tuple(perm)
                        if key in tried:
                            continue
                        tried.add(key)
                        run_candidate(f"w{w0:x}:xswap[{a},{b},{length}]", perm)
            # all arc reversals
            for length in range(2, q - 1):
                for a in range(q):
                    perm = reverse_arc_perm(q, a, length)
                    pull = word_of_perm_pullback(w0, perm, q)
                    if pull not in rej_words:
                        continue
                    key = tuple(perm)
                    if key in tried:
                        continue
                    tried.add(key)
                    run_candidate(f"w{w0:x}:xrev[{a},{length}]", perm)
        print(f"after cross-orbit: tested={tested}, found={len(results)}")

    if args.random_coset:
        rng = random.Random(20260821)
        w0 = base_words[0]
        plus = [x for x in range(q) if (w0 >> x) & 1]
        minus = [x for x in range(q) if not (w0 >> x) & 1]
        for k in range(args.random_coset):
            pp, mm2 = plus[:], minus[:]
            rng.shuffle(pp)
            rng.shuffle(mm2)
            perm = [0] * q
            for a, b in zip(plus, pp):
                perm[a] = b
            for a, b in zip(minus, mm2):
                perm[a] = b
            run_candidate(f"coset{k}", perm)
        print(f"after random coset: tested={tested}, found={len(results)}")

    if args.out and results:
        Path(args.out).write_text(json.dumps(results, indent=1))
        print(f"wrote {args.out}")
    print(f"TOTAL: tested={tested} candidates, hybrid-only examples={len(results)}")


if __name__ == "__main__":
    main()

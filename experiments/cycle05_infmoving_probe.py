"""Cycle 5: probe for hybrid-only examples with infinity-moving relabelings.

The Cycle-5 obstruction theorems assume ∞-fixing copies.  This probe
documents that the hybrid-only phenomenon itself does not need that
restriction: at n = 22 it tests second copies pi = (transpose ∞ with a
finite minus point z) ∘ (finite transposition of two plus points u,v of the
failure word), using ONLY the literal reference semantics (brute-force
induced-subset DAG), and records every case where both copies reject the
failure word while the literal union accepts it.

Usage: python -B experiments/cycle05_infmoving_probe.py
Writes certificates/cycle05_hybrid/infmoving_probe_n22.json
"""

from __future__ import annotations

import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cycle05_hybrid_core import (  # noqa: E402
    brute_accepts,
    rotations,
    single_copy_rejects_word,
    union_family_masks,
    word_from_runs,
)


def main() -> None:
    n, q = 22, 21
    w22 = word_from_runs([(1, 8), (0, 5), (1, 3), (0, 5)])
    assert single_copy_rejects_word(w22, q)
    ident = list(range(n))

    def copy2_rejects(f_plus: int, perm: list[int]) -> bool:
        fp = 0
        for x in range(n):
            if (f_plus >> perm[x]) & 1:
                fp |= 1 << x
        if (fp >> q) & 1:  # normalize: infinity minus
            fp ^= (1 << n) - 1
        return single_copy_rejects_word(fp & ((1 << q) - 1), q)

    minus_pts = [x for x in range(q) if not (w22 >> x) & 1]
    plus_pts = [x for x in range(q) if (w22 >> x) & 1]
    finds = []
    tested = 0
    for z in minus_pts:
        for (u, v) in itertools.combinations(plus_pts, 2):
            perm = ident[:]
            perm[q], perm[z] = perm[z], perm[q]
            perm[u], perm[v] = perm[v], perm[u]
            tested += 1
            if not copy2_rejects(w22, perm):
                continue
            fam = union_family_masks(n, [ident, perm])
            if brute_accepts(fam, w22, n):
                finds.append({"n": n, "inf_swapped_with": z,
                              "finite_transposition": [u, v],
                              "perm": perm, "word": f"{w22:x}"})
    out = {"tested": tested, "hybrid_only_found": len(finds),
           "semantics": "literal induced-subset DAG (reference)",
           "finds": finds}
    path = Path("certificates/cycle05_hybrid/infmoving_probe_n22.json")
    path.write_text(json.dumps(out, indent=1))
    print(f"tested {tested}; hybrid-only (both copies reject, union accepts): "
          f"{len(finds)}; wrote {path}")


if __name__ == "__main__":
    main()

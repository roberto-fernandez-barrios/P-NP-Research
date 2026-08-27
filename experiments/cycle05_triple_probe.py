"""Cycle 5: three-copy probe {id, pair-swap, shifted pair-swap}.

Pair-swap: transpose points (0,1),(2,3),...,(q-3,q-2); point q-1 fixed.
Shifted pair-swap: transpose points (1,2),(3,4),...,(q-2,q-1); point 0 fixed.

For n = 28 (exhaustive) and n = 42 (sampled, fixed seed), this probe:
  1. runs the C++ scanner on the pair (id, pair-swap) with the per-word
     common-reject dump enabled;
  2. filters the pair's common rejects by rejection under the shifted
     pair-swap copy (single-copy recurrence on the pulled-back word);
  3. runs the exact three-order union engine on the triple-common set.

Outputs certificates/cycle05_hybrid/triple_probe.json with all counters.

Usage: python -B experiments/cycle05_triple_probe.py
(requires experiments/cycle05_union_scan.exe; build with
 g++ -O2 -std=c++17 -o experiments/cycle05_union_scan.exe experiments/cycle05_union_scan.cpp)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cycle05_hybrid_core import (  # noqa: E402
    UnionEngine,
    single_copy_rejects_word,
    word_of_perm_pullback,
)

EXE = str(Path(__file__).parent / "cycle05_union_scan.exe")


def pairswap(q: int) -> list[int]:
    p = list(range(q))
    for i in range(0, q - 1, 2):
        p[i], p[i + 1] = p[i + 1], p[i]
    return p


def shifted_pairswap(q: int) -> list[int]:
    p = list(range(q))
    for i in range(1, q - 1, 2):
        p[i], p[i + 1] = p[i + 1], p[i]
    return p


def run_case(n: int, sample: int | None, seed: int) -> dict:
    q = n - 1
    ps = pairswap(q)
    ps2 = shifted_pairswap(q)
    args = [EXE, "--n", str(n), "--perm", ",".join(map(str, ps))]
    if sample:
        args += ["--sample", str(sample), "--seed", str(seed)]
    env = dict(os.environ, CYCLE05_DUMP_COMMON="1")
    with tempfile.NamedTemporaryFile(mode="w+", delete=False,
                                     suffix=".txt") as tf:
        dump_path = tf.name
    with open(dump_path, "w") as errf:
        r = subprocess.run(args, stdout=subprocess.PIPE, stderr=errf,
                           env=env, text=True)
    assert r.returncode == 0, r.stdout
    scan = json.loads(r.stdout.strip().splitlines()[-1])
    rows = []
    for line in open(dump_path):
        parts = line.split()
        if parts and parts[0] == "COMMON":
            rows.append((int(parts[1], 16), int(parts[2])))
    os.unlink(dump_path)
    assert len(rows) == scan["commonrej"]
    triple = [(w, f) for (w, f) in rows
              if single_copy_rejects_word(word_of_perm_pullback(w, ps2, q), q)]
    eng3 = UnionEngine([tuple(range(q)), tuple(ps), tuple(ps2)])
    resc3 = sum(1 for w, _ in triple if eng3.accepts(w))
    pair_resc_on_triple = sum(f for _, f in triple)
    out = {
        "n": n,
        "mode": "sample" if sample else "exhaustive",
        "sample": sample or 0,
        "seed": seed if sample else None,
        "total_words": scan["total"],
        "pair_common": scan["commonrej"],
        "pair_rescued": scan["rescued"],
        "triple_common": len(triple),
        "pair_rescued_on_triple_common": pair_resc_on_triple,
        "triple_rescued": resc3,
        "triple_union_rejects_on_triple_common": len(triple) - resc3,
    }
    print(json.dumps(out), flush=True)
    return out


def main() -> None:
    results = {
        "copies": "id, pairswap (0,1)(2,3)..., shifted pairswap (1,2)(3,4)...",
        "semantics": "exact 3-order union interval DP "
                     "(cross-checked engine, cycle05_hybrid_core)",
        "cases": [
            run_case(28, None, 0),
            run_case(42, 2000000, 20260821),
        ],
    }
    path = Path("certificates/cycle05_hybrid/triple_probe.json")
    path.write_text(json.dumps(results, indent=1) + "\n")
    print(f"wrote {path}")


if __name__ == "__main__":
    main()

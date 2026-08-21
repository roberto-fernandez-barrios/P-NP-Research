"""Cycle 5 audit: differential test of the SKEPTIC's independent C++ literal
DP (cycle05_audit_thm_pipeline.exe --dump-all) against the proposer's literal
reference brute_accepts (cycle05_hybrid_core.py) at n = 10, 12, for the
pairswap and mult:2 two-copy unions.  The proposer's brute_accepts is used
here as ONE SIDE of a differential test only.

Run:  python -B experiments/cycle05_audit_thm_diffsmall.py
"""

import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from cycle05_hybrid_core import (  # noqa: E402
    brute_accepts, union_family_masks, normalized_words,
)

EXE = Path(__file__).parent / "cycle05_audit_thm_pipeline.exe"
SCRATCH = Path(__file__).parent.parent / "audits"


def pairswap(q):
    p = list(range(q))
    for i in range(0, q - 1, 2):
        p[i], p[i + 1] = p[i + 1], p[i]
    return p


def mult(q, a):
    return [(a * i) % q for i in range(q)]


def run_case(n, spec, perm_finite):
    q, m = n - 1, n // 2
    out = SCRATCH / f"tmp_audit_dumpall_{n}_{spec.replace(':', '_')}.txt"
    subprocess.run([str(EXE), "--scan", "--n", str(n), "--copy2", spec,
                    "--dump-all", str(out), "--no-minimax"],
                   check=True, capture_output=True)
    mine = {}
    for line in out.read_text().splitlines():
        parts = line.split()
        if parts[0] == "W":
            mine[int(parts[1], 16)] = (int(parts[2]), int(parts[3]), int(parts[4]))
    ident = list(range(n))
    p2full = perm_finite + [q]
    fam1 = union_family_masks(n, [ident])
    fam2 = union_family_masks(n, [p2full])
    famU = union_family_masks(n, [ident, p2full])
    bad = 0
    tot = 0
    for w in normalized_words(q, m):
        tot += 1
        b1 = brute_accepts(fam1, w, n)
        b2 = brute_accepts(fam2, w, n)
        bu = brute_accepts(famU, w, n)
        if mine[w] != (int(b1), int(b2), int(bu)):
            bad += 1
            print("MISMATCH", n, spec, hex(w), mine[w], (b1, b2, bu))
    print(f"[{'PASS' if bad == 0 else 'FAIL'}] differential n={n} {spec}: "
          f"{tot} words, {bad} mismatches")
    out.unlink()
    return bad == 0


ok = True
for n in (10, 12):
    q = n - 1
    ok &= run_case(n, "pairswap", pairswap(q))
    ok &= run_case(n, "mult:2:0", mult(q, 2))
sys.exit(0 if ok else 1)

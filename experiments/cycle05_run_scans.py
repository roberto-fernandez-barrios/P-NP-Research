"""Cycle 5 Phase 5D experiment battery driver.

Runs experiments/cycle05_union_scan.exe over families of relative
permutations and collects JSONL results.  All scans are exact exhaustive
enumerations except where mode=sample.

Families:
  T(delta): transposition (0, delta), delta = 1..(q-1)/2 (all transpositions
            up to rotation/reflection conjugacy, under which all counters are
            invariant).
  S(b,len): block swap of arcs [0,len) and [b,b+len).
  M(a):     multiplier x -> a x mod q (control: no mid-rank hybrid arrows).
  R(seed):  uniform random permutation of Z_q (control).
  PS:       adjacent-pair-swap order (1,0,3,2,...; last point fixed) — the
            cross-arrow-rich family.

Usage: python -B experiments/cycle05_run_scans.py <battery>
  battery in {trans, blocks, controls, big, sample}
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

EXE = str(Path(__file__).parent / "cycle05_union_scan.exe")
OUT = Path("certificates/cycle05_hybrid/scan_results.jsonl")


def run(args: list[str], tag: str) -> dict:
    r = subprocess.run([EXE] + args, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"scan failed: {args}: {r.stderr}")
    rec = json.loads(r.stdout.strip().splitlines()[-1])
    rec["tag"] = tag
    with OUT.open("a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec), flush=True)
    return rec


def pairswap_perm(q: int) -> str:
    p = list(range(q))
    for i in range(0, q - 1, 2):
        p[i], p[i + 1] = p[i + 1], p[i]
    return ",".join(map(str, p))


def main() -> None:
    battery = sys.argv[1] if len(sys.argv) > 1 else "trans"
    OUT.parent.mkdir(parents=True, exist_ok=True)

    if battery == "trans":
        for n in (22, 24, 26, 28, 30):
            q = n - 1
            for d in range(1, q // 2 + 1):
                run(["--n", str(n), "--transpose", f"0,{d}"], f"trans:{n}:{d}")

    elif battery == "blocks":
        for n in (22, 24, 26, 28, 30):
            q = n - 1
            for ln in sorted({2, 3, max(2, q // 8), max(3, q // 4)}):
                for b in sorted({ln, q // 4, (q - ln) // 2, q // 2}):
                    if b < ln or b + ln > q:
                        continue
                    run(["--n", str(n), "--swap", f"0,{b},{ln}"],
                        f"swap:{n}:{b}:{ln}")

    elif battery == "controls":
        for n in (22, 24, 26, 28, 30):
            q = n - 1
            for a in (2, 3, 5):
                run(["--n", str(n), "--mult", str(a)], f"mult:{n}:{a}")
            for seed in (1, 2, 3, 4, 5):
                run(["--n", str(n), "--randperm", str(seed)], f"rand:{n}:{seed}")
            run(["--n", str(n), "--perm", pairswap_perm(q)], f"pairswap:{n}")

    elif battery == "big":
        # n=32,34 for the strongest small-n families (chosen after 'trans')
        for n in (32, 34):
            q = n - 1
            for d in (1, 2, 3, q // 4, q // 2 - 1, q // 2):
                run(["--n", str(n), "--transpose", f"0,{d}"], f"trans:{n}:{d}")
            run(["--n", str(n), "--perm", pairswap_perm(q)], f"pairswap:{n}")

    elif battery == "sample":
        # sampled larger n: rescue-rate scaling in the decaying-acceptance regime
        for n in (38, 42, 46, 50, 54, 58, 62):
            q = n - 1
            for d in (1, q // 4, q // 2):
                run(["--n", str(n), "--transpose", f"0,{d}",
                     "--sample", "2000000", "--seed", "20260821"],
                    f"trans-sample:{n}:{d}")
            run(["--n", str(n), "--perm", pairswap_perm(q),
                 "--sample", "2000000", "--seed", "20260821"],
                f"pairswap-sample:{n}")
            run(["--n", str(n), "--randperm", "1",
                 "--sample", "2000000", "--seed", "20260821"],
                f"rand-sample:{n}")

    else:
        raise SystemExit(f"unknown battery {battery}")


if __name__ == "__main__":
    main()

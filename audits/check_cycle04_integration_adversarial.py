#!/usr/bin/env python3
"""Repository-level consistency checks for the Research Cycle 4 audit.

This is not a proof checker for the imported FLSY theorem.  It freezes the
cross-artifact arithmetic, hashes, scopes, links, and formal-coverage boundary
that the final adversarial audit inspected separately.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = "c26f4688437fd79d283cb8cf673f0f5709fe9730"

RR_ROWS = {
    22: (352_716, 352_695, 21, 1, 1),
    24: (1_352_078, 1_351_664, 414, 18, 10),
    26: (5_200_300, 5_195_600, 4_700, 188, 100),
    28: (20_058_300, 20_017_908, 40_392, 1_496, 760),
    30: (77_558_760, 77_266_353, 292_407, 10_083, 5_088),
    32: (300_540_195, 298_654_992, 1_885_203, 60_813, 30_500),
    34: (1_166_803_110, 1_155_611_853, 11_191_257, 339_129, 169_862),
}

MULTI_ROWS = {
    22: (21, 821, 2),
    24: (414, 991, 2),
    26: (4_700, 1_177, 2),
    28: (40_392, 1_379, 4),
    30: (292_407, 1_597, 5),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_manifest(directory: Path, manifest: Path) -> None:
    lines = manifest.read_text(encoding="ascii").splitlines()
    assert lines and len(lines) == len(set(lines))
    for line in lines:
        expected, name = line.split("  ", 1)
        target = directory / name
        assert target.is_file(), target
        assert sha256(target) == expected, target


def check_rr_certificates() -> None:
    directory = ROOT / "certificates" / "cycle04_rr_acceptance"
    check_manifest(directory, directory / "SHA256SUMS.txt")
    assert len(list(directory.glob("cycle04_rr_acceptance_n*.json"))) == 7
    for n, expected in RR_ROWS.items():
        data = json.loads(
            (directory / f"cycle04_rr_acceptance_n{n}.json").read_text(
                encoding="utf-8"
            )
        )
        total, accepted, rejected, rotation_orbits, dihedral_orbits = expected
        q = n - 1
        assert data["schema"] == "cycle04-rr-acceptance-v1"
        assert data["normalized_balanced_words"] == total == math.comb(q, n // 2)
        assert data["accepted_normalized_words"] == accepted
        assert data["rejected_normalized_words"] == rejected
        assert accepted + rejected == total
        assert data["rejected_rotation_orbits"] == rotation_orbits
        assert rejected == q * rotation_orbits
        assert data["rejected_dihedral_orbits"] == dihedral_orbits
        failures = (
            directory / f"cycle04_rr_failures_n{n}.txt"
        ).read_text(encoding="ascii").splitlines()
        assert len(failures) == rotation_orbits
        assert failures == sorted(set(failures))


def check_multi_certificates() -> None:
    directory = ROOT / "certificates" / "cycle04_multi_rr"
    check_manifest(directory, directory / "cycle04_multi_rr_SHA256SUMS.txt")
    for n, (one_rejects, literal_count, multiplier) in MULTI_ROWS.items():
        data = json.loads(
            (directory / f"cycle04_multi_rr_n{n}.json").read_text(encoding="utf-8")
        )
        q = n - 1
        assert data["schema"] == "cycle04-multi-rr-v1"
        assert data["copy_count"] == data["minimum_t_exact"] == 2
        assert data["one_copy_normalized_rejections"] == one_rejects > 0
        assert data["common_individual_rejections"] == 0
        assert data["full_literal_union_rejections"] == 0
        assert data["hybrid_only_acceptances"] == 0
        assert data["literal_distinct_subset_count"] == literal_count
        assert literal_count == 2 + q * (2 * n - 5)
        assert sum(data["literal_rank_profile"]) == literal_count
        expected_profile = [1, q, q] + [2 * q] * (n - 4) + [q, 1]
        assert data["literal_rank_profile"] == expected_profile
        identity, second = data["permutations_old_to_new"]
        assert identity == list(range(n))
        assert second[q] == q
        assert second[:q] == [(multiplier * x) % q for x in range(q)]
        assert math.gcd(multiplier, q) == 1


def check_jsonl() -> None:
    records = [
        json.loads(line)
        for line in (ROOT / "failure_knowledge.jsonl").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    ]
    ids = [record["id"] for record in records]
    assert len(ids) == len(set(ids))
    by_id = {record["id"]: record for record in records}
    assert {"RC4-RR-01", "RC4-RR-02"} <= by_id.keys()
    assert "hybrid" in by_id["RC4-RR-01"]["scope"].lower()
    assert "not" in by_id["RC4-RR-02"]["scope"].lower()


LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def check_markdown_links() -> None:
    files = [
        ROOT / "README.md",
        ROOT / "RESEARCH_STATE.md",
        ROOT / "results" / "research_cycle_04.md",
        *sorted((ROOT / "research_cycle_04").glob("*.md")),
        ROOT / "certificates" / "cycle04_rr_acceptance" / "README.md",
        ROOT / "certificates" / "cycle04_multi_rr" / "cycle04_multi_rr_README.md",
        ROOT / "formal" / "coverage.md",
        ROOT / "literature" / "known_results.md",
        ROOT / "literature" / "novelty_log.md",
        ROOT / "audits" / "cycle04_rr_obstruction_adversarial.md",
        ROOT / "audits" / "barriers" / "cycle04_rr_interval_obstruction.md",
        ROOT / "audits" / "cycle04_final_integration_adversarial.md",
    ]
    for source in files:
        assert source.is_file(), source
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().split()[0].strip("<>")
            if re.match(r"^(?:https?|mailto):", target):
                continue
            path_text = target.split("#", 1)[0]
            if not path_text:
                continue
            resolved = (source.parent / path_text).resolve()
            assert resolved.exists(), (source, target)


def check_formal_boundary() -> None:
    source = (ROOT / "formal" / "BalancedChain.lean").read_text(encoding="utf-8")
    for name in (
        "acceptsColoring_relabel_iff",
        "isOneBalancedChain_relabel_iff",
        "iUnion_isOneBalancedChain_of_pointwise_accepts",
        "union_relabelings_isOneBalancedChain",
    ):
        assert re.search(rf"\btheorem\s+{name}\b", source)
    assert not re.search(r"(?m)^\s*(?:axiom|opaque)\b", source)
    assert not re.search(r"\b(?:sorry|admit|unsafe)\b", source)
    coverage = (ROOT / "formal" / "coverage.md").read_text(encoding="utf-8")
    assert "Phase-4A probabilistic symmetrization and counting | PARTIALLY FORMALIZED" in coverage
    assert "Corrected `RR_n`, deque equivalence, and rooted ordinary-interval reduction | UNFORMALIZED" in coverage


def check_scope_and_state() -> None:
    state = (ROOT / "RESEARCH_STATE.md").read_text(encoding="utf-8")
    result = (ROOT / "results" / "research_cycle_04.md").read_text(encoding="utf-8")
    for text in (state, result):
        assert "O01 remains **OPEN**" in text or "O01 | **OPEN**" in text
        assert "S4-D" in text
        assert "hybrid" in text.lower()
        assert "Research Cycle 5" in text
        assert "A_n <= (n/2)" in text
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            ROOT / "RESEARCH_STATE.md",
            ROOT / "results" / "research_cycle_04.md",
            ROOT / "research_cycle_04" / "rooted_interval_obstruction.md",
            ROOT / "research_cycle_04" / "rr_probability_attack.md",
            ROOT / "audits" / "cycle04_rr_obstruction_adversarial.md",
        ]
    )
    bad_equalities = [
        line
        for line in combined.splitlines()
        if re.search(r"A_n\s*=\s*(?:2\^|exp\().*Omega", line)
        and "not" not in line.lower()
    ]
    assert not bad_equalities, bad_equalities
    assert "CANDIDATE O01 RESOLUTION" not in combined


def check_source_hash_claims() -> None:
    report = (ROOT / "research_cycle_04" / "cycle04_multi_rr.md").read_text(
        encoding="utf-8"
    )
    for relative, expected in {
        "experiments/cycle04_multi_rr_search.cpp":
            "5cf24180d1cf659cf0d6e040801b9cb79614403c76234aacc081887e7acbed40",
        "experiments/cycle04_multi_rr_verify.py":
            "29a616e5caff0dfd218f49cd9f24637132ffd212b792ebc826426b8a456fa6a5",
    }.items():
        assert sha256(ROOT / relative) == expected
        assert expected in report


def check_no_temp_garbage() -> None:
    ignored_directories = {".git", ".lake", "__pycache__"}
    forbidden_suffixes = {".exe", ".pyc", ".pyo", ".tmp"}
    garbage: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in ignored_directories for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            garbage.append(path)
    assert not garbage, garbage


def main() -> None:
    base_is_ancestor = subprocess.run(
        ["git", "merge-base", "--is-ancestor", BASE, "HEAD"],
        cwd=ROOT,
        check=False,
    )
    assert base_is_ancestor.returncode == 0, (
        "Cycle-4 base is not an ancestor of HEAD",
        BASE,
    )
    check_rr_certificates()
    check_multi_certificates()
    check_jsonl()
    check_formal_boundary()
    check_scope_and_state()
    check_source_hash_claims()
    check_no_temp_garbage()
    check_markdown_links()
    print("PASS Cycle-4 integration arithmetic, hashes, links, scope, and trust boundary")


if __name__ == "__main__":
    main()

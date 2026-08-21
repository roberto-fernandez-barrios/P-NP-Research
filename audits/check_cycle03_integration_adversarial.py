#!/usr/bin/env python3
"""Static consistency checks for the final Cycle-3 integration.

This checker does not establish mathematical claims.  It catches stale
cross-file status, missing local artifacts, malformed certificates/JSONL,
duplicate failure IDs, unparseable Python, and an accidentally broadened
formal or asymptotic conclusion.
"""

from __future__ import annotations

import ast
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def check_python_and_json() -> tuple[int, int]:
    py_count = 0
    for path in ROOT.rglob("*.py"):
        if ".lake" in path.parts or "__pycache__" in path.parts:
            continue
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        py_count += 1

    json_count = 0
    for path in ROOT.rglob("*.json"):
        if ".lake" in path.parts or "__pycache__" in path.parts:
            continue
        json.loads(path.read_text(encoding="utf-8"))
        json_count += 1
    return py_count, json_count


def check_markdown_links() -> int:
    documents = [
        ROOT / "README.md",
        ROOT / "results" / "research_cycle_03.md",
        *sorted((ROOT / "research_cycle_03").glob("*.md")),
        ROOT / "formal" / "coverage.md",
        *sorted((ROOT / "audits").glob("cycle03*.md")),
    ]
    link_pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    checked = 0
    for document in documents:
        text = document.read_text(encoding="utf-8")
        for target in link_pattern.findall(text):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("#"):
                continue
            target = target.split("#", 1)[0]
            if not target:
                continue
            resolved = (document.parent / target).resolve()
            if not resolved.exists():
                raise AssertionError(f"broken local link in {document}: {target}")
            checked += 1
    return checked


def check_failure_ledger() -> int:
    records = []
    for line_number, line in enumerate(read("failure_knowledge.jsonl").splitlines(), 1):
        record = json.loads(line)
        # The persistent ledger predates Cycle 3 and intentionally contains
        # both one-axis `failure` records and older three-axis A/B/C records.
        required = {"id", "date", "family", "candidate",
                    "retry_condition", "evidence", "scope"}
        assert required <= record.keys(), (line_number, required - record.keys())
        assert "failure" in record or {"A", "B", "C"} <= record.keys(), line_number
        records.append(record)
    ids = [record["id"] for record in records]
    assert len(ids) == len(set(ids)), "duplicate failure-ledger ID"
    by_id = {record["id"]: record for record in records}
    assert {f"RC3-CPM-0{i}" for i in range(1, 6)} <= by_id.keys()
    assert "hybrid witness" in by_id["RC3-CPM-01"]["failure"]
    assert "n=22" in by_id["RC3-CPM-02"]["failure"]
    assert "not arbitrary" in by_id["RC3-CPM-02"]["scope"]
    assert "not a lower bound" in by_id["RC3-CPM-03"]["scope"]
    assert "no change" in by_id["RC3-CPM-04"]["scope"]
    assert "not an exponential lower bound" in by_id["RC3-CPM-05"]["scope"]
    return len(records)


def check_epistemic_integration() -> None:
    top_readme = read("README.md")
    results = read("results/research_cycle_03.md")
    state = read("RESEARCH_STATE.md")
    index = read("research_cycle_03/README.md")
    cp_m = read("research_cycle_03/cp_m_matching_equivalence.md")
    formal_report = read("research_cycle_03/lean_formalization.md")
    formal_audit = read("research_cycle_03/formal_adversarial_audit.md")

    for text in (top_readme, results, state, index):
        assert "O01 remains **OPEN**" in text
        assert "N(10)=35" in text
    assert "Stopping condition:** S3-D" in results
    assert "Research Cycle 4 is not begun automatically" in results
    assert "Do not begin Research Cycle 4" in state

    # Corrected CP-M status: the factor menu fails at n=10, but the literal
    # interval family succeeds there and first fails at n=22.
    assert "hybrid witness order" in cp_m
    assert "The first exhaustive failure is `n=22`" in cp_m
    assert re.search(r"first fails at\s+`n(?:=q\+1)?=22`, not at `n=10`", cp_m)
    assert "valid for every even `n<=20`" in cp_m
    assert "fails first at `n=22`" in results
    assert re.search(
        r"factor-only `n=10` counterargument was caught and\s+retracted", state
    )

    forbidden_resolution_phrases = (
        "O01 is solved", "O01 is proved", "P != NP", "P = NP",
        "mABP separation is proved",
    )
    for name, text in (
        ("top-level README", top_readme),
        ("results", results),
        ("state", state),
        ("index", index),
    ):
        for phrase in forbidden_resolution_phrases:
            assert phrase not in text, (name, phrase)

    # Formal claims stay inside the encoded representations and explicitly
    # exclude N(10), accounting, and O01.
    assert "within the encoded" in results
    assert "remain unformalized" in results
    assert "does not prove any exact value of `N(n)`" in formal_report
    assert "FINAL FORMAL INTEGRATION: PASS" in formal_audit
    assert "RESOLVED" in formal_audit


def check_formal_pin_and_tokens() -> None:
    source = read("formal/BalancedChain.lean")
    forbidden = re.compile(r"(?<![A-Za-z0-9_])(axiom|sorry|admit)(?![A-Za-z0-9_])")
    assert not forbidden.search(source)
    assert read("formal/lean-toolchain").strip() == "leanprover/lean4:v4.32.1"
    manifest = json.loads(read("formal/lake-manifest.json"))
    mathlib = next(package for package in manifest["packages"] if package["name"] == "mathlib")
    assert mathlib["inputRev"] == "v4.32.1"
    checker = read("formal/check.ps1")
    assert "(?<![A-Za-z0-9_])(axiom|sorry|admit)(?![A-Za-z0-9_])" in checker


def main() -> None:
    py_count, json_count = check_python_and_json()
    link_count = check_markdown_links()
    ledger_count = check_failure_ledger()
    check_epistemic_integration()
    check_formal_pin_and_tokens()
    print(f"PASS parsed {py_count} Python files and {json_count} JSON files")
    print(f"PASS resolved {link_count} Cycle-3 local Markdown links")
    print(f"PASS failure ledger: {ledger_count} unique records, CP-M 01..05 scoped")
    print("PASS O01/formal/CP-M/stopping-condition integration guards")
    print("ALL CYCLE-3 FINAL INTEGRATION STATIC CHECKS PASS")


if __name__ == "__main__":
    main()

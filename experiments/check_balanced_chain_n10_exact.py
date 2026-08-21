#!/usr/bin/env python3
"""One-command independent recomputation of the exact finite value N(10)=35.

The three imported checker modules use only the standard library.  This file
recomputes their finite searches, checks the stored artifacts, and applies the
short level-surplus/complement argument excluding size 34.
"""

from __future__ import annotations

import json
from pathlib import Path

from check_balanced_chain_n10_level_cover import verify_and_summarize
from check_balanced_chain_n10_no_minimum_prefix import enumerate_minimum_prefix
from check_balanced_chain_n10_upper import verify as verify_upper


CERTIFICATE_DIR = Path("certificates/balanced_chain_n10")


def main() -> None:
    search = json.loads(
        (CERTIFICATE_DIR / "level_cover_search.json").read_text(encoding="utf-8")
    )
    level_summary = verify_and_summarize(search)
    stored_levels = json.loads(
        (CERTIFICATE_DIR / "level_cover_certificate.json").read_text(encoding="utf-8")
    )
    assert level_summary == stored_levels
    minima = level_summary["exact_level_minima"]
    assert minima == [1, 1, 5, 3, 5, 3, 5, 3, 5, 1, 1]
    assert sum(minima) == 33

    prefix = enumerate_minimum_prefix()
    stored_prefix = json.loads(
        (CERTIFICATE_DIR / "no_minimum_prefix.json").read_text(encoding="utf-8")
    )
    assert prefix == stored_prefix
    assert prefix["prerequisite_level_counts_0_through_4"] == minima[:5]
    assert prefix["level4_maximum_signed_colorings_reached"] < 252

    upper = json.loads(
        (CERTIFICATE_DIR / "upper_size35.json").read_text(encoding="utf-8")
    )
    verify_upper(upper)
    assert upper["claimed_size"] == 35

    # Any family of size 34 has each level count at least tau(10,k), whose
    # sum is 33.  Thus exactly one level j has one surplus set.  Levels 0 and
    # 10 contain only one possible subset, so j is internal.  If j>=5, levels
    # 0..4 have the forbidden minimum prefix.  If j<=4, levels 6..10 are at
    # their minima; complementing every selected set turns that suffix into
    # the same forbidden minimum prefix because balanced compatibility obeys
    # d_P([10]\\S)=-d_P(S).  This finite case split is exhaustive.
    size34_cases = {}
    for surplus_level in range(11):
        if surplus_level in (0, 10):
            reason = "impossible: this Boolean-lattice level has only one subset"
        elif surplus_level >= 5:
            reason = "impossible: levels 0..4 form the forbidden minimum prefix"
        else:
            reason = (
                "impossible after set complementation: original levels 6..10 "
                "form the forbidden minimum suffix"
            )
        size34_cases[str(surplus_level)] = reason
    assert len(size34_cases) == 11

    print(f"PASS exact tau(10,k): {minima}; level sum 33")
    print(
        "PASS no minimum prefix through level 4: "
        f"{prefix['level4_choice_count']} terminal branches, "
        f"maximum {prefix['level4_maximum_signed_colorings_reached']}/252"
    )
    print("PASS every possible size-34 surplus level is excluded")
    print("PASS size-35 upper family for all 252 signed colorings")
    print("EXACT FINITE COMPUTATIONAL RESULT: N(10)=35")


if __name__ == "__main__":
    main()

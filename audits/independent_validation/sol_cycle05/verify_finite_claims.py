#!/usr/bin/env python3
"""Independent finite validator for the Cycle-5 RR/hybrid certificates.

This file deliberately imports no repository experiment or audit module.  It
uses the literal definition of RR_n and elementary subset-DAG reachability.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
from pathlib import Path


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def read_failures(path: Path) -> set[int]:
    return {int(line.strip(), 16) for line in path.read_text().splitlines() if line.strip()}


def cyclic_levels(order: tuple[int, ...]) -> list[set[int]]:
    q = len(order)
    levels: list[set[int]] = [set() for _ in range(q)]
    for length in range(1, q):
        for start in range(q):
            mask = 0
            for offset in range(length):
                mask |= 1 << order[(start + offset) % q]
            levels[length].add(mask)
        require(len(levels[length]) == q, f"unexpected interval collision at length {length}")
    return levels


def union_label_levels(order: tuple[int, ...]) -> list[dict[int, int]]:
    q = len(order)
    identity = cyclic_levels(tuple(range(q)))
    second = cyclic_levels(order)
    labelled: list[dict[int, int]] = [dict() for _ in range(q)]
    for length in range(1, q):
        for mask in identity[length]:
            labelled[length][mask] = labelled[length].get(mask, 0) | 1
        for mask in second[length]:
            labelled[length][mask] = labelled[length].get(mask, 0) | 2
    return labelled


def balanced_interval(word: int, state: int, size: int) -> bool:
    total = 2 * (word & state).bit_count() - size
    return total == 1 if size & 1 else total in (0, 2)


def push_word(word: int, permutation: tuple[int, ...]) -> int:
    pushed = 0
    for source, target in enumerate(permutation):
        if word >> source & 1:
            pushed |= 1 << target
    return pushed


def pull_word(word: int, permutation: tuple[int, ...]) -> int:
    pulled = 0
    for source, target in enumerate(permutation):
        if word >> target & 1:
            pulled |= 1 << source
    return pulled


def witness_switches(masks: list[int], labelled: list[dict[int, int]]) -> int:
    costs: dict[int, int] = {}
    first_labels = labelled[1][masks[0]]
    for label in (1, 2):
        if first_labels & label:
            costs[label] = 0
    for size, mask in enumerate(masks[1:], start=2):
        available = labelled[size][mask]
        next_costs: dict[int, int] = {}
        for label in (1, 2):
            if available & label:
                next_costs[label] = min(cost + (old_label != label) for old_label, cost in costs.items())
        costs = next_costs
    require(costs, "witness has no label assignment")
    return min(costs.values())


def union_accepts(word: int, labelled: list[dict[int, int]]) -> bool:
    q = len(labelled)
    reachable = {
        mask for mask in labelled[1] if balanced_interval(word, mask, 1)
    }
    for size in range(2, q):
        next_reachable: set[int] = set()
        for state in labelled[size]:
            if not balanced_interval(word, state, size):
                continue
            bits = state
            while bits:
                bit = bits & -bits
                if state ^ bit in reachable:
                    next_reachable.add(state)
                    break
                bits ^= bit
        if not next_reachable:
            return False
        reachable = next_reachable
    return bool(reachable)


def n22_transposition_profile(failures: set[int]) -> list[dict[str, int]]:
    q = 21
    profile = []
    for delta in range(1, q // 2 + 1):
        permutation = list(range(q))
        permutation[0], permutation[delta] = permutation[delta], permutation[0]
        order = tuple(permutation)
        second_failures = {push_word(failure, order) for failure in failures}
        common = failures & second_failures
        labelled = union_label_levels(order)
        rescued = sum(union_accepts(word, labelled) for word in common)
        profile.append({"delta": delta, "common_rejects": len(common), "rescued": rescued})
    require([row["rescued"] for row in profile[:8]] == [0] * 8, "delta <= 8 unexpectedly rescues")
    require(profile[8]["rescued"] == 2 and profile[9]["rescued"] == 4, "delta 9/10 profile changed")
    return profile


def validate_fixed_infinity_file(path: Path, failures: set[int]) -> dict[str, int]:
    records = json.loads(path.read_text())
    require(isinstance(records, list), f"{path.name}: expected a JSON list")
    n = int(records[0]["n"])
    q = n - 1
    require(all(int(record["n"]) == n for record in records), f"{path.name}: mixed n")

    label_cache: dict[tuple[int, ...], list[dict[int, int]]] = {}
    pushed_failure_cache: dict[tuple[int, ...], set[int]] = {}
    switch_histogram: collections.Counter[int] = collections.Counter()
    keys: list[tuple[tuple[int, ...], int]] = []

    for index, record in enumerate(records):
        prefix = f"{path.name} record {index}"
        permutation = tuple(int(value) for value in record["perm_finite"])
        require(len(permutation) == q and set(permutation) == set(range(q)), f"{prefix}: non-permutation")
        word = int(record["word"], 16)
        require(word.bit_count() == n // 2 and word < 1 << q, f"{prefix}: invalid normalized word")
        require(word in failures, f"{prefix}: first copy accepts")

        if permutation not in pushed_failure_cache:
            pushed_failure_cache[permutation] = {push_word(failure, permutation) for failure in failures}
        second_failures = pushed_failure_cache[permutation]
        require(word in second_failures, f"{prefix}: second copy accepts")
        require(
            int(record["common_rejects_of_pair"]) == len(failures & second_failures),
            f"{prefix}: common-reject count mismatch",
        )
        require(
            int(record["pulled_back_word"], 16) == pull_word(word, permutation),
            f"{prefix}: pulled-back word mismatch",
        )

        if permutation not in label_cache:
            label_cache[permutation] = union_label_levels(permutation)
        labelled = label_cache[permutation]
        masks = [int(value, 16) for value in record["witness_chain_masks"]]
        require(len(masks) == q - 1, f"{prefix}: wrong witness length")
        previous = 0
        for size, mask in enumerate(masks, start=1):
            require(mask < 1 << q and mask.bit_count() == size, f"{prefix}: wrong state size {size}")
            require(previous & ~mask == 0, f"{prefix}: non-nested step {size}")
            require(mask in labelled[size], f"{prefix}: state not in either circle at size {size}")
            require(balanced_interval(word, mask, size), f"{prefix}: unbalanced state at size {size}")
            previous = mask

        switches = witness_switches(masks, labelled)
        require(switches == 1, f"{prefix}: witness switch count is {switches}, not 1")
        if "min_switches" in record:
            require(int(record["min_switches"]) == 1, f"{prefix}: stored min_switches mismatch")
        switch_histogram[switches] += 1
        keys.append((permutation, word))

    key_counts = collections.Counter(keys)
    duplicate_excess = sum(count - 1 for count in key_counts.values())
    require(max(key_counts.values()) <= 2, f"{path.name}: a key occurs more than twice")

    if n == 22:
        require(len(records) == 122, "n=22 record count is not 122")
        require(len(key_counts) == 122 and duplicate_excess == 0, "n=22 records are not distinct examples")
        canonical = [record for record in records if record.get("canonical")]
        require(len(canonical) == 1, "n=22 does not have exactly one canonical record")
        expected = list(range(q))
        expected[1], expected[13] = expected[13], expected[1]
        require(canonical[0]["perm_finite"] == expected, "unexpected canonical permutation")
        require(int(canonical[0]["word"], 16) == int("1fe0e", 16), "unexpected canonical word")
    elif n == 24:
        require(len(records) == 14_864, "n=24 stored-record count is not 14,864")
        require(len(key_counts) == 8_258, "n=24 distinct-example count is not 8,258")
        require(duplicate_excess == 6_606, "n=24 duplicate excess is not 6,606")
        duplicate_labels = []
        by_key: dict[tuple[tuple[int, ...], int], list[str]] = collections.defaultdict(list)
        for record, key in zip(records, keys):
            by_key[key].append(record["label"])
        for labels in by_key.values():
            if len(labels) == 2:
                duplicate_labels.append(tuple(label.split(":", 1)[1].split("[", 1)[0] for label in labels))
        require(
            all(set(labels) == {"swap", "xswap"} for labels in duplicate_labels),
            "n=24 duplicates are not exactly swap/xswap route duplicates",
        )
        require(len({key[0] for key in key_counts}) == 440, "n=24 distinct-permutation count is not 440")
        require({key[1] for key in key_counts} == failures, "n=24 records do not cover exactly all RR failures")

    return {
        "n": n,
        "records": len(records),
        "distinct_examples": len(key_counts),
        "duplicate_excess": duplicate_excess,
        "distinct_permutations": len({key[0] for key in key_counts}),
        "distinct_words": len({key[1] for key in key_counts}),
        "switch_one": switch_histogram[1],
    }


def literal_rr_levels(n: int, permutation: tuple[int, ...]) -> list[set[int]]:
    q = n - 1
    require(len(permutation) == n and set(permutation) == set(range(n)), "invalid full permutation")
    levels: list[set[int]] = [set() for _ in range(n + 1)]

    def transport(mask: int) -> int:
        image = 0
        for source, target in enumerate(permutation):
            if mask >> source & 1:
                image |= 1 << target
        return image

    levels[0].add(0)
    levels[n].add((1 << n) - 1)
    for finite in range(q):
        levels[1].add(1 << permutation[finite])
    identity_circle = cyclic_levels(tuple(range(q)))
    infinity_bit = 1 << q
    for rank in range(2, n):
        for interval in identity_circle[rank - 1]:
            levels[rank].add(transport(infinity_bit | interval))
    return levels


def literal_accepts(word: int, copy_levels: list[list[set[int]]], n: int) -> bool:
    reachable = {0}
    for rank in range(1, n + 1):
        candidates: set[int] = set().union(*(copy[rank] for copy in copy_levels))
        next_reachable: set[int] = set()
        for state in candidates:
            total = 2 * (state & word).bit_count() - rank
            if abs(total) > 1:
                continue
            if any(parent & ~state == 0 for parent in reachable):
                next_reachable.add(state)
        if not next_reachable:
            return False
        reachable = next_reachable
    return True


def validate_infinity_moving(path: Path) -> dict[str, int]:
    payload = json.loads(path.read_text())
    finds = payload["finds"]
    require(int(payload["tested"]) == 550, "infinity-moving tested count changed")
    require(int(payload["hybrid_only_found"]) == 32 and len(finds) == 32, "infinity-moving find count changed")
    cache: dict[tuple[int, ...], list[set[int]]] = {}
    identity_cache: dict[int, list[set[int]]] = {}
    for index, record in enumerate(finds):
        n = int(record["n"])
        word = int(record["word"], 16)
        permutation = tuple(int(value) for value in record["perm"])
        require(word.bit_count() == n // 2 and word < 1 << (n - 1), f"infinity record {index}: bad word")
        identity = identity_cache.setdefault(n, literal_rr_levels(n, tuple(range(n))))
        second = cache.setdefault(permutation, literal_rr_levels(n, permutation))
        require(not literal_accepts(word, [identity], n), f"infinity record {index}: identity copy accepts")
        require(not literal_accepts(word, [second], n), f"infinity record {index}: second copy accepts")
        require(literal_accepts(word, [identity, second], n), f"infinity record {index}: union rejects")
    return {"tested_metadata": int(payload["tested"]), "verified_finds": len(finds)}


def verify_manifest(cert_dir: Path) -> int:
    manifest = cert_dir / "cycle05_hybrid_SHA256SUMS.txt"
    checked = 0
    for line in manifest.read_text().splitlines():
        expected, marked_name = line.split(maxsplit=1)
        name = marked_name.lstrip("*")
        actual = hashlib.sha256((cert_dir / name).read_bytes()).hexdigest()
        require(actual == expected, f"SHA-256 mismatch for {name}")
        checked += 1
    return checked


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--failure-n22", type=Path, required=True)
    parser.add_argument("--failure-n24", type=Path, required=True)
    parser.add_argument(
        "--certificate-dir", type=Path, default=Path("certificates/cycle05_hybrid")
    )
    args = parser.parse_args()

    failures22 = read_failures(args.failure_n22)
    failures24 = read_failures(args.failure_n24)
    require(len(failures22) == 21, "independent n=22 failure dump does not contain 21 words")
    require(len(failures24) == 414, "independent n=24 failure dump does not contain 414 words")

    cert_dir = args.certificate_dir
    summary = {
        "manifest_files_verified": verify_manifest(cert_dir),
        "n22": validate_fixed_infinity_file(cert_dir / "hybrid_only_n22_candidates.json", failures22),
        "n24": validate_fixed_infinity_file(cert_dir / "hybrid_only_n24_candidates.json", failures24),
        "n22_transpositions": n22_transposition_profile(failures22),
        "infinity_moving": validate_infinity_moving(cert_dir / "infmoving_probe_n22.json"),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

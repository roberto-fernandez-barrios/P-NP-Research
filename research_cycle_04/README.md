# Research Cycle 4: randomized relabeling / RR-cover attack

**Base commit:** `c26f4688437fd79d283cb8cf673f0f5709fe9730`
**Date:** 2026-08-21
**Stopping condition:** **S4-D** for the individual-copy RR
acceptance/symmetrization route
**Primary target:** O01 remains **OPEN**

Cycle 4 independently reconstructed the corrected cyclic-interval family
`RR_n`, verified the proposed random-relabeling reduction, computed exact
acceptance data through `n=34`, and then found a decisive asymptotic
obstruction to the reduction's premise.

For a normalized coloring and a fixed finite rank-one root `r`, an RR witness
is in exact bijection with a 1-balanced maximal chain in the ordinary
one-interval family on the other `n-2` finite points.  If `p_N` denotes the
ordinary interval-family success probability, then

```text
A_n <= (n/2) p_(n-2).
```

FLSY Theorem 4.4 (Theorem 1.7) gives

```text
p_N <= 2^(-c N^(1/5))
```

for all sufficiently large even `N`.  Therefore

```text
A_n <= (n/2) 2^(-c (n-2)^(1/5))
    = exp(-Omega(n^(1/5))).
```

This refutes the proposed inverse-polynomial lower bound on `A_n` and shows
that coverage by witnesses lying wholly inside individual relabelled copies
needs stretched-exponentially many copies.  It does **not** rule out chains
that splice subsets from several copies in their literal union, and it is not
a lower bound on `N(n)`.

## Canonical reports

* [`../results/research_cycle_04.md`](../results/research_cycle_04.md) —
  integrated result and stopping disposition.
* [`symmetrization_independent.md`](symmetrization_independent.md) — exact
  Phase-4A proof, threshold, attribution, and distinct-subset accounting.
* [`rooted_interval_obstruction.md`](rooted_interval_obstruction.md) — main
  rooted complement/reversal proof.
* [`rr_probability_attack.md`](rr_probability_attack.md) — independent
  reconstruction and probabilistic/failure-mode audit.
* [`literature_novelty_audit.md`](literature_novelty_audit.md) — primary-source
  theorem numbering, attribution, and bounded novelty search.
* [`cycle04_rr_exact_count.md`](cycle04_rr_exact_count.md) — exact necklace
  counting, orbit structure, and run statistics through `n=34`.
* [`cycle04_multi_rr.md`](cycle04_multi_rr.md) — exact two-copy certificates
  for `n=22,24,26,28,30`, with no asymptotic inference.
* [`lean_formalization.md`](lean_formalization.md) — Cycle-4 formal coverage.
* [`../audits/cycle04_rr_obstruction_adversarial.md`](../audits/cycle04_rr_obstruction_adversarial.md)
  — independent obstruction audit.
* [`../audits/barriers/cycle04_rr_interval_obstruction.md`](../audits/barriers/cycle04_rr_interval_obstruction.md)
  — mandatory restricted-result barrier audit.
* [`../audits/cycle04_final_integration_adversarial.md`](../audits/cycle04_final_integration_adversarial.md)
  — final repository-level audit.

## Reproduction

```powershell
python -B research_cycle_04/cycle04_probability_interval_reduction.py
python -B experiments/cycle04_rr_verify_counts.py
python -B experiments/cycle04_multi_rr_verify.py
powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
```

The exact-count and multi-RR certificate payloads are under
`certificates/cycle04_rr_acceptance/` and `certificates/cycle04_multi_rr/`.
All size statements count distinct literal subsets, never descriptions,
permutations, paths, factors, or abstract states.

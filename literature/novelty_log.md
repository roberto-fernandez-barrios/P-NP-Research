# Novelty audit log

**Current search cutoff:** 2026-08-13  
**Rule:** these labels concern prior-art status, not mathematical truth.
`UNCLEAR` is intentionally used when public searches found no prior source
but recency, terminology, or index coverage prevents a stronger conclusion.

The detailed Cycle-2 queries, official-source checks, adjacent literature,
and negative-search limitations are in
[`literature_novelty_audit.md`](../research_cycle_02/literature_novelty_audit.md).

| Claim | Novelty status | Basis and limitation |
|---|---|---|
| `N(2)=3` and `N(4)=6` | **KNOWN** | Routine direct arguments are complete; absence of a published finite table is irrelevant. |
| Exact finite values `N(6)=12` and `N(8)=20` under the FLSY set-system convention | **UNCLEAR** | Exact-notation, equivalent-DAG, numerical-sequence, paper, thesis, and public-code searches found no prior computation. The problem is recent and equivalent-model size conventions vary; no novelty claim is made. |
| Exact smallest-even-`n` counterhistories for the withdrawn two-block conditional claims, with eager/query-minimal reveal semantics separated | **UNCLEAR** | The official withdrawal already records the filtration gap. Searches found no public source giving these exact minima, but they are a diagnosis of a withdrawn proof and may exist in private referee/author work. |
| CF-LOGGAP: the primitive-Dyck lower-tail obstruction for the precisely defined greedy, uniformly bounded-`d`, single-consumption cached-frontier family and high-confidence logarithmic-gap contract | **UNCLEAR** | Standard random-walk first-passage tails are known, but no application to this actual adaptive stale-frontier process was found. The exact process-specific theorem was not located; recent-paper and terminology coverage remain substantial caveats. |
| Variable absorb/recurse threshold (Proposition 5.1) | **LIKELY KNOWN** | Elementary conditional bookkeeping; recorded to close a concrete argument gap, not offered as an original theorem. |
| Geometric-log distinct-subset accounting (Proposition 6.1) | **LIKELY KNOWN** | Reconstructs/generalizes standard multiplicative recursive accounting already present in spirit in FLSY/TR26-043; no novelty claim. |

The public status of O01 is separate: FLSY leaves the exact complexity open,
TR26-043's polynomial claim is withdrawn, and no public repair was found.
That supports `OPEN` for O01; it does not assign novelty to any future proof.

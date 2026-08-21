# Novelty audit log

**Current search cutoff:** 2026-08-21
**Rule:** these labels concern prior-art status, not mathematical truth.
`UNCLEAR` is intentionally used when public searches found no prior source
but recency, terminology, or index coverage prevents a stronger conclusion.

The current primary-source, equivalent-object, and terminology searches are
in the Cycle-4
[`literature_novelty_audit.md`](../research_cycle_04/literature_novelty_audit.md).
The Cycle-3 audit remains at
[`research_cycle_03/literature_novelty_audit.md`](../research_cycle_03/literature_novelty_audit.md).
The separate Cycle-2 process audit remains in
[`research_cycle_02/literature_novelty_audit.md`](../research_cycle_02/literature_novelty_audit.md).

| Claim | Novelty status | Basis and limitation |
|---|---|---|
| `N(2)=3` and `N(4)=6` | **KNOWN** | Routine direct arguments are complete; absence of a published finite table is irrelevant. |
| Exact finite values `N(6)=12`, `N(8)=20`, and `N(10)=35` under the FLSY set-system convention | **UNCLEAR** | Exact-notation, equivalent-DAG, numerical-sequence, paper, thesis, public-code, and post-computation `N(10)=35` searches found no prior computation. The problem is recent and equivalent-model size conventions vary; `PRIOR-ART-NOT-FOUND` is not a novelty claim. |
| Canonical-support quotient and literal matching-prefix-union formulations | **UNCLEAR** | FLSY already gives the pair-labelled open-path read-once program.  The support-normalized statement and exact distinct-prefix metric were not located separately, but they may be implicit in branching-program folklore; no novelty claim is made. |
| Quadratic cyclic-interval family `RR_n`, finite validity through `n=20`, and its `n=22` obstruction | **UNCLEAR** | Searches across universal routing, alternating chains, crossing matchings, switching networks, and Boolean-lattice terminology found no matching statement.  The result is internally checked only, the terminology space is broad, and no novelty claim is made. |
| Rooted `RR_n` complement/reversal equivalence with FLSY's ordinary one-interval family | **UNCLEAR; NO NOVELTY CLAIM** | FLSY already proves the decisive interval probability bound and uses closely related cyclic-interval geometry.  Deque-language, noncrossing-pairing, interval-chain, sequence, and exact-phrase searches did not locate the precise rooted statement, but it is elementary enough to be implicit or folklore. |
| `A_n(RR_n) <= (n/2)2^{-c(n-2)^{1/5}}` | **KNOWN-THEOREM COROLLARY** | The asymptotic input is exactly FLSY Theorem 4.4/1.7; Cycle 4 supplies the elementary rooted reduction and makes no new-asymptotic-theorem claim. |
| Exact RR acceptance/orbit counts through `n=34` and exact two-copy values through `n=30` | **UNCLEAR** | Bounded sequence/code/terminology searches found no prior table under the same literal-subset/full-induced-DAG convention.  These are finite internal computations, and `PRIOR-ART-NOT-FOUND` is not a novelty claim. |
| Exact smallest-even-`n` counterhistories for the withdrawn two-block conditional claims, with eager/query-minimal reveal semantics separated | **UNCLEAR** | The official withdrawal already records the filtration gap. Searches found no public source giving these exact minima, but they are a diagnosis of a withdrawn proof and may exist in private referee/author work. |
| CF-LOGGAP: the primitive-Dyck lower-tail obstruction for the precisely defined greedy, uniformly bounded-`d`, single-consumption cached-frontier family and high-confidence logarithmic-gap contract | **UNCLEAR** | Standard random-walk first-passage tails are known, but no application to this actual adaptive stale-frontier process was found. The exact process-specific theorem was not located; recent-paper and terminology coverage remain substantial caveats. |
| Variable absorb/recurse threshold (Proposition 5.1) | **LIKELY KNOWN** | Elementary conditional bookkeeping; recorded to close a concrete argument gap, not offered as an original theorem. |
| Geometric-log distinct-subset accounting (Proposition 6.1) | **LIKELY KNOWN** | Reconstructs/generalizes standard multiplicative recursive accounting already present in spirit in FLSY/TR26-043; no novelty claim. |
| N1 (Cycle 5): Lemma A.1 — difference-`a` APs of size `2..q-2` in `Z_q` are never cyclic intervals for `a ≠ ±1` | **POTENTIALLY NOVEL** | ~12 searches (three-distance corollaries, dilates mod p, Bohr/GAP structure, Cooper's quasirandom arithmetic permutations read directly, MO/competition angles) found no stated source; elementary corollary of classical three-gap adjacency counting, so folklore risk is explicitly recorded — present as "not located", not as a headline novelty. See `research_cycle_05/novelty_audit_theorems.md` §N1. |
| N2 (Cycle 5): Theorem A's shape — unions of affinely related cyclic interval systems admit no hybrid chains | **POTENTIALLY NOVEL** | C1P/PQ/PC literature composes interval systems conjunctively (intersection/coupling/k-block within one order); no union-rigidity or switching-chain precedent found; FLSY §6 poses no such question. Residual risk lives in the N1 component. §N2 of the Cycle-5 audit. |
| N3 (Cycle 5): Theorem E's mechanism — bounded-defect hull approximation transferring FLSY's interval balanced-chain bound to near-interval families | **POTENTIALLY NOVEL** | The balanced-chain literature is exactly FLSY TR26-001 (exact intervals, one order, per-summand sums only) and withdrawn TR26-043 (two-block, defect Θ(n), no hull machinery; still withdrawn, no repair as of 2026-08-21); no hull/almost-interval transfer found in general discrepancy sources. Priority risk is time-based (active area), not prior-art-based. §N3. |
| N4 (Cycle 5): switch depth `D_mid` and the run-sandwich argument (bounded alternation forces hull density) | **POTENTIALLY NOVEL** | The Cycle-5 survey's NOT-FOUND for switching chains is confirmed to extend to the quantitative forms: no alternation-counting parameter for nested chains in unions of interval systems and no run-length↔defect trade-off located anywhere (incl. direct reads of both 2026 papers). §N4. |
| N5 (Cycle 5): no prior source outside FLSY and this repository studies unions of relabelled RR-type/interval families as balanced-chain systems | **NOVELTY STRONGLY SUPPORTED** | The eight-month-old balanced-chain literature was enumerated completely (ECCC 2026 scan + arXiv): two papers, neither studies such unions with hybrid chains. Nearest outside neighbors, none subsuming: CKSS24 sums-of-ordered-smABPs and FLSY §5.5 Σ_π (per-summand, no switching), NNN12 three-permutation discrepancy (union family, no chains), DMPY12 arc partitions (single copy). Private/in-progress work invisible to searches. §N5. |

The public status of O01 is separate: the official FLSY CCC 2026 paper leaves
the exact complexity open, TR26-043's polynomial claim is withdrawn, and no
public repair was found.  That supports `OPEN` for O01; it does not assign
novelty to any future proof.

Re-verified 2026-08-21 (Cycle-5 audit): TR26-043 = arXiv:2604.00746 remains
withdrawn (v2 of 2026-05-11; author-acknowledged filtration gap in
Lemma 4.1), and an ECCC year-2026 scan plus arXiv sweeps located no repair
or successor.  The Cycle-5 theorem-level audit is in
[`research_cycle_05/novelty_audit_theorems.md`](../research_cycle_05/novelty_audit_theorems.md).

# Novelty audit log

**Current search cutoff:** 2026-08-26
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
The final independent cross-model corrections, including the expanded
feasible-word/regular-system/antimatroid search, are recorded in
[`cycle05_sol_final_cross_model_validation.md`](../audits/cycle05_sol_final_cross_model_validation.md)
§10 and incorporated below.

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
| N1 (Cycle 5): Lemma A.1 — difference-`a` APs of size `2..q-2` in `Z_q` are never cyclic intervals for `a ≠ ±1` | **UNCLEAR** | No exact source was found, but this is an elementary adjacency-counting consequence adjacent to mature simple/common-interval, arc-permutation, and arithmetic-permutation theory. Folklore risk is high; present only as an exact statement not located. See `research_cycle_05/novelty_audit_theorems.md` §N1. |
| N2 (Cycle 5): repaired Theorem A — affine, balance-sensitive literal-union rigidity forbids hybrid chains | **POTENTIALLY NOVEL** | This status is narrow: no exact repaired affine theorem was located. Arc permutations name pure cyclic growth words, and regular-set-system/antimatroid literature contains broad feasible-word and extra-chain phenomena, so the switching framework itself is not included in this status. §N2. |
| N3 (Cycle 5): Theorem E's exact bounded-defect hull/refinement/rooted-FLSY transfer | **POTENTIALLY NOVEL** | This status is narrow: approximate/gapped common intervals are known, but no exact `t`-independent hull/refinement/rooted-complement reduction to the FLSY estimate was located. The exact `balanced-chain` phrase having a small 2026 footprint does not enumerate the broader relevant literature. §N3. |
| N4 (Cycle 5): switching-chain/switch-depth/run-sandwich framework | **UNCLEAR** | Extra maximal chains under a union and alternative feasible paths have direct prior art (Algaba–van den Brink–Dietz Example 4.7; regular set systems; greedoids/antimatroids; learning spaces). The narrow `D_mid` parameter and `defect ≤ run-length + 2` inequality may be **POTENTIALLY NOVEL**, but the aggregate framework is not. §N4. |
| N5 (Cycle 5): literal unions of relabelled RR-type/interval families as balanced-chain systems | **KNOWN** | FLSY Definition 1.2 and full-version Lemma 2.3 construct `𝓨 = 𝓧 ∪ ⋃_i σ_i(𝓧)` and quantify over every full Boolean chain contained in that literal set system. Instantiating the base family with RR gives the object. FLSY does not analyze hybrid provenance; RR-specific minimality, certificates, and switch-depth theory remain separately classified. §N5. |
| SEG localization of the FLSY interval estimate | **UNCLEAR** | The exact segment statement is not published verbatim. Its probability engine is published FLSY machinery, while the offset, rounding, first-leg, tail, and cyclic-full adaptations are a repository proof checked with repairs by the deep, arms-length, and final cross-model audits. Provenance: **NEW BUT PROVED IN THIS REPOSITORY**; mathematical status: **ADVERSARIALLY REVIEWED PROOF CANDIDATE; UNFORMALIZED**, `SOUND WITH REPAIRS`. This is not a novelty certification. |

The public status of O01 is separate: the official FLSY CCC 2026 paper leaves
the exact complexity open, TR26-043's polynomial claim is withdrawn, and no
public repair was found.  That supports `OPEN` for O01; it does not assign
novelty to any future proof.

Re-verified 2026-08-21 (Cycle-5 audit): TR26-043 = arXiv:2604.00746 remains
withdrawn (v2 of 2026-05-11; author-acknowledged filtration gap in
Lemma 4.1), and an ECCC year-2026 scan plus arXiv sweeps located no repair
or successor.  The Cycle-5 theorem-level audit is in
[`research_cycle_05/novelty_audit_theorems.md`](../research_cycle_05/novelty_audit_theorems.md).

Final cross-model correction 2026-08-26: FLSY Lemma 2.3 makes the literal-
union object known; Algaba–van den Brink–Dietz, TI 15-007/II (2015),
[Example 4.7, p. 23](https://papers.tinbergen.nl/15007.pdf), directly shows
an extra full chain generated by a union of input prefix-state chains. No
Cycle-5 item has a strong novelty status.

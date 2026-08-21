# Research Cycle 5 final integration adversarial audit

**Date:** 2026-08-22
**Base commit:** `745f2bdf8b6d1e472279da913245aa048b36112c` (= current `HEAD`, branch `cycle05-fable`)
**Role:** independent repository-level consistency, reproduction, and scope
audit, performed BEFORE the Cycle-5 commit
**Verdict:** **NOT READY — one BLOCKER (D1, certificate byte-stability /
SHA manifest platform fragility); everything else MINOR or COSMETIC**

This audit treated every Cycle-5 claim as hostile until reproduced.  It read
the summary report, the state file, all six `research_cycle_05/` documents,
all three prior Cycle-5 audits, the barrier audit, the five RC5 failure
records, and the formal coverage ledger; it reran the verifier suites, the
Lean build, the scanner, the searches, and the probes; it recomputed more
than thirty published numbers from primary artifacts, including one headline
result (the `t = 3` union) that had no stored artifact at all.  It edited
nothing outside this file.  A note on self-reference: `RESEARCH_STATE.md`,
`results/research_cycle_05.md` §10, and `research_cycle_05/README.md` list
this file among the Cycle-5 artifacts; it is created by this audit and did
not exist before it.

---

## C1. Status-label integrity — PASS (two MINOR label findings, D2/D3)

Every theorem-status statement in `results/research_cycle_05.md` and
`RESEARCH_STATE.md` was compared against the verdict actually recorded in
the supporting audit file.

* **Theorem A.**  PASS.  Both summary documents state the theorem only in
  the **precomposition** form (`π_i^{-1}∘π_j` affine, multiplier `∉ {±1}`),
  matching the repaired statement in `switch_structure_theory.md` §2 and the
  audit verdict in `audits/cycle05_theorems_adversarial.md` ("UNSOUND AS
  STATED; SOUND AFTER REPAIRS").  A full grep of `results/`,
  `RESEARCH_STATE.md`, `research_cycle_05/`, and `failure_knowledge.jsonl`
  for `π_j∘π_i^{-1}` / "postcomposition" found the postcomposition form only
  inside FALSIFIED/warning contexts (results §1 and §11 ledger; STATE
  Cycle-5 bullet; theory file §2 warning; RC5-HY-05, which records the
  falsification as its own failure entry with the exact counterexample
  `π`, `ψ = ×2`, coloring `0xae2b3` — identical to audit §T1.e).  No
  residual statement presents the postcomposition version as true.
* **Theorem E.**  PASS.  Stated everywhere as `ADVERSARIALLY REVIEWED —
  SOUND AFTER REPAIRS`; the summary's parenthetical details (single cosmetic
  Step-5 indexing repair; hull lemma verified exactly tight; pipeline check
  zero violations, min-k `= 2` vs bound `10` on every rescued coloring at
  `n = 24, 26`) match audit §§T2.a–T2.f verbatim.  The repair is applied in
  `dense_circle_obstruction.md` (Step 5 uses `G_1^c`, not `G_0^c`).
* **Theorems C and F.**  PASS.  Marked CONDITIONAL on SEG at every load-
  bearing occurrence (results §1, §8, §11 ledger; STATE bullet with
  "Granting SEG:"; theory file §5/§5b; barrier audit item 7; RC5-HY-03
  "CONDITIONALLY OBSTRUCTED").  Theorem F's split label ("t = 2
  unconditional in its density branch, conditional through SEG in its
  long-run branch") matches §5b exactly.
* **Lemma SEG.**  PASS.  Everywhere `PROOF CANDIDATE` (reconstruction) with
  skeptic verdict quoted as **SOUND WITH REPAIRS, all repairs
  statement-level** — the exact §8 verdict of
  `audits/cycle05_seg_lemma_adversarial.md` — plus the mandatory §9 reminder
  reproduced in both summary documents ("SEG is not a published theorem; the
  conditional labels stand").  No unconditional use of SEG exists anywhere
  (grep evidence; the only "Theorem C/F" lines without a same-line
  conditional marker are two reference sentences in results §6, covered by
  the document's own §1/§8/§11 labels — COSMETIC, D9).
* **Novelty verdicts.**  PASS.  Results §3 and STATE quote exactly:
  Lemma A.1, Theorem A's shape, Theorem E's hull-transfer mechanism, and the
  switch-depth/run-sandwich parameters `POTENTIALLY NOVEL` (with the
  explicit folklore-risk caveat for A.1), and the multi-RR-union object of
  study `NOVELTY STRONGLY SUPPORTED` — matching
  `research_cycle_05/novelty_audit_theorems.md` N1–N5 and the updated
  `literature/novelty_log.md` rows verbatim, and both summaries add
  "recorded as search outcomes, not claims".
* **FLSY/literature citations.**  PASS.  Results §8's claims (verbatim
  verification of all four imports incl. published numbering 23/8 and 14/6;
  Fréchet anti-concentration engine, milestones + first-passage lower
  tails; `1/5` balancing `exp(-Ω(d))` vs `exp(-Ω(n/d⁴))`; upper bound a
  `log n/log log n`-depth randomized hierarchy explicitly not a union of
  interval orders; `Σ_π` handled by rank subadditivity, literal unions never
  analyzed; `𝓘_{n,m}` untouched for `1 < m < 2⌈lg n⌉`; TR26-043 withdrawn;
  range `Ω(n²) ≤ N(n) ≤ n^{O(log n/log log n)}` standing) all appear, with
  sources, in `flsy_reconstruction.md` §§1–7.  Results §3's literature
  attributions (Uno–Yagiura 2000; BCMR 2008; Albert–Atkinson–Klazar 2003
  `e^{-2}`; Corteel–Louchard–Pemantle 2006 Poisson(2); Heber–Mayr–Stoye
  2011 Lemma 8 complement-closure; Blin–Faye–Stoye 2010 nested common
  intervals; simultaneous-PQ NP-completeness; multiplication maps and
  switching chains NOT FOUND) each match `common_interval_literature.md`.

**Findings:**

* **D2 (MINOR — stale sentence).**  `switch_structure_theory.md` §6 ends:
  "Theorem C (conditional) settles it for low-depth lists; **the pair-swap
  regime is genuinely open**."  This predates Theorem E and contradicts §4
  of the same file ("killed **unconditionally** by the density
  obstruction") and every other document.  The genuinely open regime is
  high-depth AND non-dense (Lemma M territory), as results §1/§7 state
  correctly.  The error is in the conservative direction (understates what
  is proved) but is an internal inconsistency.
* **D3 (MINOR — label inflation for `D_mid ≤ 1`).**  Results §3 lists
  "middle switch depth `D_mid ≤ 1`" for transpositions under "Exact
  characterizations **proved**", and STATE says "Exact `D_mid` values:
  … transpositions/single block swaps ≤ 1".  The source (Theorem B part 3)
  is labeled `PROOF CANDIDATE (recorded case skeleton …; exact D_mid DP
  confirmation for q ≤ 21)` and says a fully written-out case enumeration
  was not produced; block-swap `≤ 1` is DP-verified at `q ≤ 21` only.  The
  theory file itself is honest; the two summaries drop the candidate
  qualifier.  (Theorem B parts 1–2 are PROVED, and the pair-swap bullet is
  correctly scoped: equality only for `q ≤ 21`, general `≥ (q-7)/2` by the
  verified construction.)

## C2. Number integrity — PASS (findings D4, D5, D8)

Numbers were verified against primary artifacts, not other prose.  All
checks below were run by this audit (commands abbreviated; every stored-row
comparison used all six counters `total/rej1/rej2/commonrej/rescued/
unionrej`, not just the two quoted).

| # | Claim (results doc) | Primary source | Result |
|---|---|---|---|
| 1 | 122 verified `n=22` certificates, min switches all 1 | `hybrid_only_n22_candidates.json` + verifier | PASS (122; histogram `{1: 122}`) |
| 2 | 14,864 at `n=24`, min switches all 1 | `hybrid_only_n24_candidates.json` + verifier | PASS (14,864; `{1: 14864}`) |
| 3 | canonical example `π=(1 13)`, coloring `0x1fe0e` | n22 JSON `canonical: true` entry | PASS (label `we0ff:swap[1,13,1]`, word `1fe0e`, `perm_finite` = transposition 1↔13) |
| 4 | 43 distinct relative permutations, 66 from single transpositions (`n=22`) | n22 JSON recount | PASS (43 / 66) |
| 5 | 440 distinct permutations; all 414 failure words rescued (`n=24`) | n24 JSON recount | PASS (440 distinct perms; 414 distinct rescued words = the full failure set) |
| 6 | 349 moves tested (`n=22`); 2,647 (`n=24`) | search reruns (see C3) | PASS (349/122 and 2647/14864 reproduced) |
| 7 | ∞-moving probe: 550 candidates, 32 hybrid-only | `infmoving_probe_n22.json` + probe rerun | PASS (550/32 stored and reproduced identically; 550 = 10 minus points × C(11,2) checks structurally) |
| 8 | trans:30:14 = 16892/154891 | `scan_results.jsonl` | PASS |
| 9 | pairswap:28 = 4138/4709; pairswap:34 = 2065656/2413835; pairswap-sample:62 = 103716/148726 | `scan_results.jsonl` | PASS (all counters) |
| 10 | mult:30:2 = 0/667; ALL `mult:*` rescued = 0 (12 rows); ALL `rand:*` rescued = 0 (32 rows); commons up to 2,179 | `scan_results.jsonl` | PASS (no nonzero-rescued mult/rand row exists; rand:30:1 common = 2179) |
| 11 | full §5 transposition best-δ table (22:4/11 … 34:425086/5979437) and aggregate column 6.00/4.79/3.90/3.24/2.71% | stored rows + recomputed aggregates | PASS (all seven rows; all five aggregates to the printed precision) |
| 12 | full §5 pair-swap table `n = 24 … 64` (14 rows) | stored rows | PASS (every row) |
| 13 | sampled best transposition 4.7% → 0.9% (`n = 38..62`); near δ ≤ 7 rescue nothing anywhere | recomputed over all `trans*` rows | PASS (4.7% at 38, 0.9% at 62; zero rescues for every exhaustive δ ≤ 7 row at every `n`) |
| 14 | `D_mid` = 3/5/7 for pair-swap at `q = 13/17/21` | `python -B experiments/cycle05_switch_depth.py` rerun | PASS (full printed table matches `switch_structure_theory.md` §1, incl. multipliers 0, transp rows, block swaps 1) |
| 15 | `t = 3` union at `n=28`: rejects 3 of 20,058,300; triple-common 308; 305 rescued; triple/pair-common 6.5% | **no stored artifact** — independently reproduced by this audit | PASS numerically (see D5): from the scanner's `CYCLE05_DUMP_COMMON=1` pair dump (4709 words) + `UnionEngine([id, pairswap, shifted])`, this audit obtained exactly 308 / 305 / 3 / 6.5%, with "shifted pair-swap" reconstructed as the rotation-conjugate (swaps (1,2),(3,4),…,(25,26), fixes 0) |
| 16 | §6 interpolations: rev4 `(D_mid, defect) = (3, 6)`; pair-swap `(7, 2)`; bit-reversal `D_mid = 0`; xor maps `≤ 4` at `q = 21` | recomputed with `d_mid()` + a defect scan under natural reconstructions of the (undocumented) constructions | PASS for rev4/pair-swap/bit-reversal; xor holds for `c = 2,3,5,7` (the `c = 1` xor IS the pair-swap, so the claim is read as excluding it — construction not recorded, see D5) |
| 17 | Lean: no sorry/axiom/admit, 8,656 jobs | `formal/check.ps1` rerun | PASS (see C3d) |
| 18 | Cycle-4 reverification: both suites PASS, both manifests check, 21/414 reproduced | reruns (C3 extras) | PASS |
| 19 | `n=22` single rejected orbit = 21 rotations of `1^8 0^5 1^3 0^5` | independently re-derived in `audits/cycle05_theorems_adversarial.md` T1.f; consistent with `rej1 = 21` in every n=22 row and the core self-test | PASS |
| 20 | cross-arrow trichotomy (`--list-cross`): multipliers no mid arrows, transpositions Θ(1) anchored, pair-swap Θ(q) | rebuilt scanner, profiles at `n=22` | PASS (M2: zero at sizes 3–17; T0,10: 8–10/size mid; pairswap: 44/size); Theorem B.1's common-interval count also spot-checked exactly at `L = 9`, δ = 10 (3 commons) |

**Findings:**

* **D4 (MINOR — unsupported "87.5%", repeated 4×).**  Results §1, STATE,
  RC5-HY-02, and RC5-HY-03 say the pair-swap circle "rescued 87.5% of
  common rejects at `n ≤ 30`".  The exact stored rates are 85.7 / 87.8 /
  87.9 / 87.4% (`n = 24..30`) and the aggregate is 43510/49775 = **87.4%**;
  no primary artifact yields 87.5%.  Off by only 0.1pp from the aggregate,
  but this repository's standard is exact numbers and the figure is
  repeated in four places.  (The theory file's own "87.4–87.9%" is
  correct.)
* **D5 (MINOR — headline numbers without stored artifacts).**  (i) The
  `t = 3` results (item 15) and the sampled `n = 42` triple figures (95.0%
  rescue; triple/pair-common 6.5% → 31.8%) appear in results §5, STATE, and
  RC5-HY-02 but have **no scan row, certificate, or script** —
  `scan_results.jsonl` has no triple family, `cycle05_union_scan.cpp` is
  two-copy only, and "shifted pair-swap" is defined nowhere.  This audit
  reproduced the exhaustive `n=28` numbers exactly (and thereby fixed the
  construction: rotation-conjugate), but the sampled `n=42` triple figures
  remain unreproducible without the lost seed/driver.  (ii) The
  `min_switches`/`canonical` annotations in the stored n22 JSON are correct
  (independently recomputed by the verifier) but were added by an
  unrecorded step: the committed search script emits entries without those
  fields, and the committed verifier never writes.  (iii) §6's revB /
  bit-reversal / xor constructions (item 16) likewise have no committed
  generator.  All verified numbers are right; the defect is provenance,
  not correctness.
* **D8 (COSMETIC — "~40 searches").**  Results §3 credits the novelty audit
  with "~40 searches"; the file documents 20 numbered queries (12+2+5+1)
  plus listing scans, version-history fetches, and direct reads.  The
  novelty log itself says "~12 searches" for N1.  Recommend "~20 documented
  searches plus listing scans and direct reads".

## C3. Reproduction — PASS (all five mandated reproductions, plus extras)

All commands were run from the repository root on this machine
(Windows 11, PowerShell for the Lean check per the tip; git-bash for POSIX
tools).  Exact final outputs shown.

**(a) Core self-tests — PASS.**

```text
> python -B experiments/cycle05_hybrid_core.py
cycle05_hybrid_core self-tests PASS
```

Source inspection confirms the self-test really does the claimed §2 cross
check: brute-force literal induced-subset-DAG vs fast interval DP on EVERY
normalized coloring at `n ∈ {8,10,12}` over randomized copy lists
(including `t = 3` lists), witness chains re-checked element-wise, plus the
single-copy recurrence at `n = 12, 14` and the `n = 22` failure orbit.

**(b) Certificate verification, both JSONs — PASS.**

```text
> python -B experiments/cycle05_verify_hybrid_certificates.py certificates/cycle05_hybrid/hybrid_only_n22_candidates.json
loaded 122 examples for n in [22]
verified 122 examples against the literal reference semantics
minimum-switch histogram: {1: 122}
ALL CYCLE-5 HYBRID-ONLY CERTIFICATES PASS

> python -B experiments/cycle05_verify_hybrid_certificates.py certificates/cycle05_hybrid/hybrid_only_n24_candidates.json
loaded 14864 examples for n in [24]
verified 14864 examples against the literal reference semantics
minimum-switch histogram: {1: 14864}
ALL CYCLE-5 HYBRID-ONLY CERTIFICATES PASS
```

**(c) Scanner rebuild + two exact row reproductions — PASS.**

```text
> g++ -O2 -std=c++17 -o experiments/cycle05_union_scan.exe experiments/cycle05_union_scan.cpp   # builds clean
> ./experiments/cycle05_union_scan.exe --n 22 --transpose 0,10
{"n": 22, "perm": "T0,10", "mode": "exhaustive", "total": 352716, "rej1": 21, "rej2": 21, "commonrej": 11, "rescued": 4, "unionrej": 7}
> ./experiments/cycle05_union_scan.exe --n 26 --mult 2
{"n": 26, "perm": "M2", "mode": "exhaustive", "total": 5200300, "rej1": 4700, "rej2": 4700, "commonrej": 0, "rescued": 0, "unionrej": 0}
```

Both rows are byte-equal (all counters) to the stored `trans:22:10` and
`mult:26:2` rows in `scan_results.jsonl`.

**(d) Lean formal check, native PowerShell — PASS.**

```text
> powershell -ExecutionPolicy Bypass -File .\formal\check.ps1
Lean (version 4.32.1, x86_64-w64-windows-gnu, ...)
...
Build completed successfully (8656 jobs).
PASS: BalancedChain.lean contains no sorry/axiom/admit and lake build succeeded.
```

(Linter warnings only — unused section variables / simp args; no errors.)
All eleven newly-claimed multi-copy identifiers (`labelSet`, `ChainPure`,
`AcceptsPure`, `HybridOnly`, `chainContained_mono`,
`acceptsPure_acceptsUnion`, `acceptsUnion_pure_or_hybridOnly`,
`IsLabeling`, `SwitchBound`, `switchBound_zero_iff_chainPure`,
`chainContained_union_switchBound`) are present in
`formal/BalancedChain.lean` (`section MultiCopy`, lines 845–947, +115 lines
vs `HEAD`), matching `formal/coverage.md`'s Cycle-5 rows, which correctly
keep `RR_n`, Lemma 5A.1, Theorems A/C/E/F, and SEG/RS/M UNFORMALIZED.

**(e) SHA-256 manifest — PASS in the current working tree (but see D1).**

```text
> cd certificates/cycle05_hybrid && sha256sum -c cycle05_hybrid_SHA256SUMS.txt
hybrid_only_n22_candidates.json: OK
hybrid_only_n24_candidates.json: OK
infmoving_probe_n22.json: OK
scan_results.jsonl: OK
```

**Extra reproductions performed by this audit (all PASS):**

* `python -B experiments/cycle05_switch_depth.py` — full `D_mid` table
  reproduced, including 3/5/7 for pair-swap (mandated C2 item).
* `cycle05_hybrid_only_search.py --n 22` → `tested=349, found=122`;
  the 122 `(label, word)` pairs are **identical** to the stored
  certificate.
* `cycle05_hybrid_only_search.py --n 24 --failures
  certificates/cycle04_rr_acceptance/cycle04_rr_failures_n24.txt
  --cross-orbit` → `tested=2647, found=14864`; **identical** to the stored
  certificate.  (Note: `--n 24` without `--failures` asserts out; the
  README quick-reference shows only the n=22 form.)
* `cycle05_infmoving_probe.py` (run in a scratch CWD to avoid touching the
  certificate) → `tested 550; hybrid-only 32`; output JSON **identical** to
  the stored one.
* Three-copy reproduction (D5): pair dump `CYCLE05_DUMP_COMMON=1 …
  --n 28 --perm <pairswap>` (4709 commons / 4138 rescued, matching
  `pairswap:28`), then a 3-order `UnionEngine` run → triple-common 308,
  rescued 305, union rejects 3, ratio 6.5% — exactly the §5 claims.
* Cycle-4 dependency claims (results §10): both Cycle-4 manifests verify
  (`sha256sum -c` OK in `cycle04_rr_acceptance` and `cycle04_multi_rr`);
  `cycle04_multi_rr_verify.py` → `ALL CYCLE-4 MULTI-RR CERTIFICATES PASS`
  (n=22..30, disjoint rejection sets, 0 hybrid-only);
  `cycle04_rr_verify_counts.py --skip-literal-equivalence
  --recount-through 26` → `ALL REQUESTED CYCLE-4 RR CERTIFICATE CHECKS
  PASS` (16796/58786/208012 necklaces; 1/18/188 rejected orbits — the
  claimed 21 and 414 word counts follow and also appear as `rej1` in every
  independent scan row).

## C4. Scope discipline — PASS (all items)

* **No `N(n)` bound claimed.**  Grep of every `N(n)` occurrence in the
  Cycle-5 documents: all are targets ("would give"), disclaimers ("Nothing
  here bounds `N(n)`", results §1; dense_circle §1 Scope; barrier audit
  item 8), or verified FLSY facts.  STATE explicitly: "every Cycle-5
  theorem is an obstruction to restricted multi-RR construction routes,
  not a bound on `N(n)`."
* **No unrestricted multi-RR impossibility.**  Every obstruction carries
  its class hypothesis; the open boundary (`t ≥ 3` non-dense deep-switching;
  ∞-moving; SEG itself) is stated in results §1/§7 and STATE "Open
  boundary, stated exactly"; Lemma M is marked OPEN with an explicit
  anti-overclaim note ("absence of a counterexample is not evidence of a
  proof", theory §5b).
* **Infinity-moving copies.**  Explicitly OUTSIDE the theorems ("outside
  the theorems' scope and remain formally open", results §1; STATE (ii);
  dense_circle Scope; Lemma 5A.1's non-∞-fixing caveat in
  `hybrid_definitions.md` §4) — while the finite examples are recorded as a
  probe only.  No document claims coverage.
* **No O01 progress claimed either way; no P vs NP.**  "O01 remains OPEN"
  in results (header, §1, §11) and STATE (three places); the only
  P-vs-NP-adjacent text is the FLSY paper summary and the STATE Critical
  rule ("Do not directly attempt P versus NP.  No Boolean or algebraic
  complexity separation follows from any cycle so far.").  The barrier
  audit (`audits/barriers/cycle05_hybrid_obstructions.md`) answers all
  eight mandated questions and claims no barrier was "bypassed".
* **Anti-self-deception test (finite two-copy coverage vs asymptotics).**
  Explicitly addressed at least three times: the `t = 3` paragraph
  ("excellent finite performance, provably doomed scaling — the cycle's
  sharpest illustration of the finite-vs-asymptotic trap", results §5);
  Theorem E Remark 3 (at `n = 62` the bound exceeds 1, so the 69.7% finite
  rescue is consistent); RC5-HY-04 scope ("no asymptotic proof is claimed
  from data alone").  Theorem A's audit additionally records WHY the scans
  missed the composition bug (all had `π_1 = id`) — self-deception surfaced
  and documented rather than hidden.
* **Stop rule.**  Applied as mandated: results §12 stops under S5-D (with
  the S5-F candidate flagged as "pending external scrutiny"), recommends
  **retiring RR-family unions as the primary O01 route**, states the exact
  reopen conditions, and "Cycle 6 is not started automatically";
  STATE's Next action opens with "Stop.  Do not begin Research Cycle 6
  automatically." and its ban list matches the theorems' actual scopes
  (single-copy rigorously false; affine `G = 0`; dense any-`t`;
  two-copy/low-depth marked conditional).  Naming convention (S5-D/S5-F
  defined inline in the results header) follows the Cycle-4 precedent.

## C5. Artifact hygiene — FAIL on byte-stability (D1); rest PASS with MINOR list gaps (D6, D10, D11)

* **Existence.**  Every file named in `research_cycle_05/README.md` and in
  STATE's Canonical Cycle-5 artifact list exists (programmatic sweep of 34
  paths), with the single expected exception of this audit file, which the
  lists reference and this audit creates.  All 208 scan rows parse; the
  failure ledger parses with 39 unique IDs including exactly the five RC5
  records, whose statuses match the theorem labels (C1).
* **SHA manifest coverage.**  PASS: `cycle05_hybrid_SHA256SUMS.txt` covers
  exactly the four certificate payloads (n22, n24, infmoving, scan rows)
  and verifies in the current tree (C3e).
* **Format note.**  PASS: the binary-vs-hex failure-list hazard is recorded
  in `research_cycle_05/README.md` (format note), STATE (Hardened
  foundation), results §10 (with the discarded-and-rerun void `n = 24`
  search), and is actually enforced in code
  (`cycle05_hybrid_only_search.py` detects by charset/length and validates
  weight and length).
* **Scratch paths.**  PASS: `grep -rn "MASTER~1" **/*.md` (and
  `AppData`/`Temp\claude` variants) over the tree finds nothing; the SEG
  audit's "scratchpad copies fetched 2026-08-21" provenance phrase carries
  no literal session path — the acceptable form.
* **Ignored generated files.**  PASS: `.gitignore` covers
  `experiments/*.exe`, `experiments/__pycache__/`, `formal/.lake/`; `git
  status` shows no stray executables or caches among the untracked files.

**Findings:**

* **D1 (BLOCKER — certificate bytes will not survive the commit).**  All
  four SHA-recorded payloads in `certificates/cycle05_hybrid/` currently
  have **CRLF** line endings, and the manifest hashes those CRLF bytes.
  `core.autocrlf=true` on this machine, and — unlike both Cycle-4
  certificate trees, which `.gitattributes` pins `text eol=lf` explicitly
  "to keep LF even when core.autocrlf=true" — the cycle-5 directory has
  **no attributes coverage** (`git check-attr` → unspecified).  At `git
  add`, git will normalize the stored blobs to LF, so the committed bytes
  will NOT be the bytes the manifest describes: `sha256sum -c` will fail on
  every LF checkout (Linux/macOS/CI, or any clone without autocrlf), and
  `git hash-object --no-filters` ≠ staged blob — precisely the condition
  the Cycle-4 final audit's "Final staging reproducibility note" declared
  must not hold for SHA-recorded evidence.  Fix before commit (integrator's
  choice, e.g. normalize the four payloads to LF + regenerate + re-verify
  the manifest + extend `.gitattributes` with
  `/certificates/cycle05_hybrid/** text eol=lf`, mirroring Cycle 4).
  This audit changed nothing.
* **D6 (MINOR — artifact lists incomplete).**
  `research_cycle_05/README.md`'s tables omit
  `novelty_audit_theorems.md` (documents), `cycle05_infmoving_probe.py`
  (experiments), and `infmoving_probe_n22.json` (certificates — despite it
  being in the SHA manifest); STATE's Canonical Cycle-5 list omits
  `research_cycle_05/novelty_audit_theorems.md` and
  `audits/barriers/cycle05_hybrid_obstructions.md` (the Cycle-4 list
  includes its barrier audit).  All files exist and are referenced from
  running text; only the indexes are incomplete.
* **D10 (COSMETIC — declared audit working files).**  `audits/` carries the
  theorems-audit dumps and diff intermediates (`audit_common_*.txt`,
  `proposer_common_*.txt`, `{m,p}2{4,6,8}.sorted`, `audit_scan_*.out`; two
  legitimately empty at n=22).  They are declared in that audit's "Files
  produced" section, so they are evidence rather than strays; the six
  `.sorted` copies are redundant with their sources.
* **D11 (MINOR — README reproduction command mutates evidence).**  The
  quick-reference line `cycle05_hybrid_only_search.py --n 22 --out
  certificates/cycle05_hybrid/hybrid_only_n22_candidates.json` points the
  rerun at the stored certificate; because the search emits entries WITHOUT
  the `min_switches`/`canonical` annotations present in the stored file
  (added by an unrecorded step, cf. D5(ii)), following the documented
  command verbatim would strip annotations and break the SHA manifest.  It
  should target a scratch path.  Related COSMETIC (D7): README calls the
  n24 JSON "same schema" as n22, but n24 entries lack those two fields.

---

## Defect register

| ID | Severity | Summary | Where |
|---|---|---|---|
| D1 | **BLOCKER** | Cycle-5 certificates are CRLF + unpinned under `core.autocrlf=true`; committed bytes will not match the SHA manifest on LF checkouts; violates the Cycle-4 byte-stability standard | `certificates/cycle05_hybrid/*`, `.gitattributes` |
| D2 | MINOR | Stale "the pair-swap regime is genuinely open" contradicts Theorem E and §4 of the same file | `research_cycle_05/switch_structure_theory.md` §6 |
| D3 | MINOR | Transposition/block-swap `D_mid ≤ 1` presented as proved/exact in the two summaries; source labels it PROOF CANDIDATE (DP-checked `q ≤ 21` only) | `results/research_cycle_05.md` §3; `RESEARCH_STATE.md` Structure-theory bullet |
| D4 | MINOR | "87.5%" pair-swap rescue at `n ≤ 30` unsupported (exact: 85.7–87.9% per `n`, 87.4% aggregate); repeated in 4 places | results §1; STATE; RC5-HY-02; RC5-HY-03 |
| D5 | MINOR | `t = 3` results (and n=42 sampled triple), n22 annotations, and §6 revB/bit-reversal/xor constructions lack stored artifacts/scripts; "shifted pair-swap" undefined (n=28 numbers independently reproduced exactly by this audit; n=42 sampled triple not reproducible) | results §5–§6; STATE; RC5-HY-02 |
| D6 | MINOR | README/STATE artifact indexes omit the novelty audit, the ∞-probe script/JSON, and (STATE) the barrier audit | `research_cycle_05/README.md`; `RESEARCH_STATE.md` |
| D7 | COSMETIC | README "same schema" claim for the n24 JSON (lacks `min_switches`/`canonical`) | `research_cycle_05/README.md` |
| D8 | COSMETIC | "~40 searches" vs 20 documented numbered queries in the novelty audit | results §3 |
| D9 | COSMETIC | Two §6 sentences cite Theorem C without the conditional qualifier (label established elsewhere in the document) | results §6 |
| D10 | COSMETIC | Redundant `.sorted` diff intermediates among the declared theorems-audit dumps | `audits/` |
| D11 | MINOR | Documented n22 reproduction command overwrites the annotated certificate and would break the manifest | `research_cycle_05/README.md` quick reference |

No defect touches the mathematical content: every theorem label matches its
audit, every checked number is either exact or (D4) 0.1pp loose, every
mandated reproduction passed, and the one artifact-free headline claim was
reproduced exactly by this audit.

## Overall verdict

**NOT READY — one BLOCKER.**  Resolve D1 (make the four
`certificates/cycle05_hybrid/` payloads byte-stable across checkouts and
make the manifest describe the committed bytes, following the Cycle-4
`.gitattributes` precedent, then re-run `sha256sum -c`) and the tree is
ready to commit; D2–D6/D11 are worth fixing in the same pass but none of
them blocks, and none affects any recorded verdict, number of record, or
scope statement.  After the fix, the final integrator should re-verify the
manifest against the STAGED bytes (`git hash-object --no-filters`
comparison, as Cycle 4 did), commit, and confirm a clean `git status`.
This audit does not authorize Research Cycle 6.

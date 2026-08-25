# Cycle 7 — Stage V hostile independent validation of Jiang–Cai [JC26]

**Date:** 2026-08-25.  **Branch:** `cycle07-o18-fable` (base `3918bd6`).
**Object validated:** [JC26] = Tao Jiang, Shaowei Cai, *A Better Analysis
For PPSZ For 3-SAT*, arXiv:2607.10697 **v1** (2026-07-12), claiming
randomized Unique-3-SAT in `O*(1.306969598^n)` and general 3-SAT in
`O*(1.307031578^n)` via an LP-dual recombination of Scheder's regular and
irregular estimates plus the Scheder–Steinberger lifting.
**Validation stance:** hostile; every source treated as potentially wrong;
all fetches frozen with SHA-256; independent implementations at arm's
length.

---

## VERDICT: **JC-SOUND-WITH-REPAIRS**

**Repaired frontier (unchanged from the paper's claim):** randomized
general 3-SAT in `O(1.307031578^n)`; Unique-3-SAT in `O(1.306969598^n)`.
Every repair below re-establishes validity at [JC26]'s exact operating
parameters without moving any number, relabels a definition, weakens a
quantifier form while preserving the stated running-time bases, or
corrects background exposition only.  No repair changes the certified
bases, the LP, its optimum, or its dual slacks.

**Stage-I gate decision:** Stage V passes strongly enough to proceed.
The recombination LP, its corner `(i_0, i_1, tau) = (0, 0.0600432…, 0)`,
and the dual slack structure survive validation unchanged, so the Stage-I
question (is the corner realizable, or does a new valid inequality
exclude it?) is well-posed against the frontier `1.307031578`.

---

## 1. What was validated, by whom, and how (evidence map)

| Layer | Method | Artifact | Result |
|---|---|---|---|
| Source existence + freeze | live fetch, SHA-256 manifests, GitHub blobs pinned to commit `3e732e0` | `research_cycle_07/frozen_sources/`, `stageV_log.md` §V0 | real; frozen |
| Authors' checker | code inspection, then execution | `frozen_sources/authors_checker_rerun_output.txt` | exit 0; transcript identical to frozen (mod CRLF) |
| Arithmetic layer (independent) | from-scratch exact-rational interval checker, arms-length (authors' code never read by its author) | `research_cycle_07/checkers/independent_checker.py` + output + report | 89/90 PASS; 1 genuine finding (F1, §4) |
| Recombination LP | from-scratch re-derivation + first-principles corner proof | `research_cycle_07/lp_reconstruction.md` | sound; corner = unique optimum, zero duality gap |
| Scheder imports (regular/irregular/structural/endgame) | verbatim import ledger against ECCC TR21-069 rev 1 (SHA-frozen) with rendered-page verification | `research_cycle_07/scheder_import_ledger.md`, `frozen_sources/scheder_extracts.md` | transcription exact; hypothesis-layer mismatches → repairs R1–R4 |
| SS lifting imports + baselines | verbatim ledger against the open-access journal version + Hertli + HKZZ | `research_cycle_07/ss_lifting_import_ledger.md` | CLEAN; deviations attribution-level only |
| Repair certifications | exact-rational certification engine (this cycle) | `research_cycle_07/checkers/repair_certifications.py` + output | ALL PASS (exit 0); adversarial review in `checkers/repair_certifications_review.md` |
| Novelty/frontier | live literature sweep, 19 searches + 22 fetches | `research_cycle_07/novelty_frontier_audit.md` | frontier claim SUPPORTED; no follow-ups; no better bound |

Three independent implementations touched the arithmetic: the authors'
checker, the arms-length independent checker, and main-loop spot
computations (the F1 fraction, float sanity, and the repair engine).

## 2. What is CONFIRMED sound

1. **The paper's new mathematics.**  The recombination derivation
   (`gain_R/n ≥ A(1−i_1−2i_0) − P_reg + S·tau` from the four imports),
   the octant relaxation direction, Proposition 3.1's dual certificate,
   the corner location and uniqueness (proved from first principles by
   subgradient optimality, not certificate trust: strictly positive
   slacks `b_0−2b_1 ≈ 1.3410·10⁻³` and `b_T+λS ≈ 1.3854·10⁻²` on the
   `i_0` and `tau` dual constraints; `i_1`-constraint tight; zero duality
   gap), Lemma A.1's derivative calculus, Lemmas C.1/C.2 (liquid
   restriction, prefix realization — re-proved independently), the
   root/branch analysis of §4, and the quantifier bookkeeping of the
   proofs.  (`lp_reconstruction.md` §§3–6.)
2. **Every displayed number.**  All coefficients, margins, enclosures,
   root brackets, and outward-rounded bases replicate in exact rationals
   with certified strict margins; the tightest is `4.15·10⁻¹⁴` (safe
   branch margins over the claimed `2.69/2.70·10⁻¹¹`).  The corner
   satisfies `L_reg = L_irr = γ*` to width `< 10⁻⁷⁷`.  All 9 JSON
   reported intervals contain the independent enclosures.
3. **Transcription of all imports.**  Both coefficient displays (§7.8,
   §8.4 of TR21-069 rev 1 — all sixteen decimals), Eq. (11), Lemma 34/A.3,
   the endgame constants, Definition 67's densities, and the
   change-of-measure identity match the frozen source glyph-for-glyph;
   the `ID_i` notation reconciliation (§6 all-variables vs §8
   TwoCC-excluded) is verified correct; the source itself takes
   `max{gain_R, gain_I}` unconditionally (no case hypotheses), so the
   simultaneity step is exactly the source's own.
4. **The SS lifting layer.**  JC's Imported Theorem 4.1 = SS journal Main
   Theorem 1.17 verbatim (JC add the monotone/closure hypotheses that
   SS's own proof uses but its statement omits — safe direction);
   `p_w = p0 + ε_w` = SS Theorem 1.10, stated for exactly JC's heuristic
   `P^(w)`; `p* = (2−log₂e)/2 = 1−1/(2 ln 2)` digit-exact; liquid/Q/I
   definitions match, making Lemmas C.1/C.2 well-posed.
5. **The frontier claim.**  No source states any explicit randomized
   general-3-SAT base below Hertli's `1.30704` before [JC26]; HKZZ's
   `1.306995` and Qin–Watanabe's `1.306984` are Unique-3-SAT figures
   (verified from their own texts); within the SS lifting route the
   lifted bonus is strictly increasing in the unique bonus, so weaker
   unique inputs cannot beat the Scheder/JC route.  (Caveat: [JC26] cite
   neither Hertli, HKZZ, nor QW; a bespoke general-case biased-PPSZ
   analysis was never written but is not logically excluded.)

## 3. Mismatches found and their repairs (the "WITH-REPAIRS" content)

**R1 [HIGH → repaired, certified].  ε_R exceeds the printed hypothesis.**
Imported estimate 2.1 claims validity for `ε_R ∈ [0, 0.13]`; the source's
printed proof of the `0.9·Thr` component (Prop C.12, ECCC pp. 77–78)
carries the hypothesis `ϵ ≤ 0.1`, and [JC26]'s chosen
`ε_R = 0.1024756… > 0.1`.  Moreover the source's internal claim
"`s′(r) ≤ 1.05` provided `ϵ ≤ 0.13`" is **false** (certified exact
witness at `ε = 0.13`, `r ≈ 0.4161`: `s′ = 1.05 + 1.135·10⁻²`), so the
claimed range `[0, 0.13]` is unsupportable.  *Repair:* all four numeric
claims of Prop C.12 (`2δ_max(1−r) ≤ 0.05·r(1−2r)`; `f(r) ≥ 0.98 f(s)`;
`s′ ≤ 1.05`; `g(r) ≥ 0.945 g(s)`, plus the range facts `0 ≤ s ≤ r`)
are **certified in exact rational arithmetic at the exact operating point
`ε_R = 0.1024756190168075228998451658`** (and at Scheder's `0.1`), via
the substitution `t = √(1−2r)` making all claims piecewise-polynomial
(`repair_certifications.py`, Part A; adversarially reviewed).  The
repaired hypothesis of Imported estimate 2.1 is "every ε_R at which
Prop C.12's claims hold", which includes both `0.1` and `ε_R`; the range
`(≈0.105, 0.13]` is withdrawn.  **No number changes.**

**R2 [MEDIUM → repaired, certified].  Thr quantifier.**  "Every fixed
`Thr > 0`" overstates the source: Prop C.13(2) requires `Thr ≤ 1/1150`,
and its own margin is hairline (`OCB*(4) = 0.000869965… ≥ 1/1150 =
0.000869565…`, margin `4.0·10⁻⁷` — certified exactly, closed form
rational + rational·ln 2).  [JC26]'s `Thr = 2A/0.9 = 2.2168·10⁻⁴` and
Scheder's `2.1963·10⁻⁴` both comply (certified).  Repaired statement:
`0 < Thr ≤ 1/1150`.  **No number changes.**  (Also certified while
here: C.13(1) `OCB*(d) ≥ MLB*(d)` for all `5 ≤ d ≤ 161` by exact closed
forms — the source asserted this only "by numerical computation" — and
the `d ≥ 162` symbolic chain's numeric facts including the hairline
`E(162) = 0.0977 ≤ 1/10`.)

**R3 [MEDIUM → repaired, certified].  ε_I range claim.**  The source's
printed restriction `ϵ ≤ 256/600` rests on the false claim
"`10r²(1−2r)² ≤ 10/256`" (true maximum `10/64`, via the exact identity
`1/8 − r(1−2r) = 2(r−1/4)²`); the corrected constraint is
`ϵ ≤ 64/600 ≈ 0.1067`.  Consequently [JC26] Lemma A.1's secondary claim
that the whole range `[0, 1/5]` is admissible fails on `(64/600, 1/5]`;
but the operating point `ε_I = 0.0731 < 64/600` **complies with the
corrected constraint** (certified), and Lemma A.1's own nonnegativity
calculus (`|φ_ID| ≤ 5/2`, `|φ_pID| ≤ 61/54`, `φ_TwoCC ≥ −5` — the last
via the exact factorization `φ_TwoCC + 5 = (1/2−r)(160r²+20r+10)`) is
certified exactly.  Repaired claim: `ε_I = 0.0731…` is admissible; the
range statement is restricted to `[0, 64/600]`.  **No number changes.**

**R4 [MEDIUM-LOW → relabel].  TwoCC definition.**  [JC26] §2.1 defines
TwoCC as "variables having at least two critical clauses"; the source's
operative Definition 31 counts critical clauses **in the closure `F̃`**
(F plus all 3-clauses inferable from pairs of 3-clauses).  [JC26] use
`|TwoCC|` opaquely and consistently, so the recombination is unaffected;
the repair is to read every occurrence of TwoCC in [JC26] as
Definition 31's set.  **Material for Stage I:** any finite enumeration of
`(i_0, i_1, tau)` must use the closure-based TwoCC and Scheder's
canonical-critical-clause selection semantics.

**R5 [LOW → statement-form repair].  Finite-strength packaging.**  [JC26]
state the imported estimates with a fixed-strength error decomposition
`ξ_X(w)n + r_{X,w}(n)` (`ξ_X(w) → 0`, `r = o(n)` per fixed `w`); the
source proves its theorems only for `w = w(n)` slowly growing, with
per-variable errors vanishing as heights grow, and nowhere states the
fixed-`w` decomposition ([ledger I2(vi)/I3(vi)]).  *Repair (verified
reasoning, `lp_reconstruction.md` §6 + this audit):* rerun [JC26]'s
chain in the source-verbatim `w(n)` packaging.  The unique bound becomes
`P[PPSZ_{w(n)}(F) = α] ≥ 2^{−p0n+γ*n−o(n)} ≥ 2^{−p0n+γ_new n}` for
large `n` (the certified slack `γ* − γ_new = 8.05·10⁻¹¹ > 0` absorbs the
`o(n)`).  In the lifting, the large-`I` branch uses SS Thm 1.10 at
`w(n)` (error `ε_{w(n)} → 0`), and the unique-residual branch applies the
unique bound to the residual on `m = n − ⌊δn⌋` variables at strength
`w(n) ≥ w(m)` via the (independently re-proved) strength-monotonicity
coupling.  Both headline running times survive verbatim because the
outward-rounded bases carry strictly positive margins
(`2^{p0−γ_new} < 1.306969598` by `4.8·10⁻¹⁰`;
`2^{p0−η_safe} < 1.307031578` by `6.9·10⁻¹¹` in base terms), each of
which absorbs the `2^{o(n)}` repetition/run-cost factor
(`n^{O(w(n))} = 2^{o(n)}`).  The only casualty is the literal quantifier
form "∃ fixed w₀ ∀w ≥ w₀" of Theorem 1.1/Corollary 1.2, which is
**unverified as stated** (it would need the fixed-`w` reading of the
source's height bookkeeping) and is repaired to "for any nondecreasing
slowly growing `w(n)`, for all large `n`" — with identical `O(·)`
running-time conclusions.  **No number changes.**

**F1 [background exposition → correction recorded].  The 1/15218
endgame.**  [JC26] eq. (2) reproduces the source's end-of-§6 chain
`max{(1−irr)/10118 − 1/41391, irr/1380} ≥ 1/15218`.  This inequality is
**exactly false**, in the source and in [JC26]: the minimax value is
`31273/475913718 ≈ 6.5711491·10⁻⁵ < 1/15218 = 6.5711657·10⁻⁵` (shortfall
exactly `43/258659105733 ≈ 1.66·10⁻¹⁰`; certified independently twice;
`1/15218` is a wrong-direction rounding of `15218.0385…`; the valid
clean bound is `1/15219`).  Consequences: Scheder's Theorem 6
(`1.306973^{−n}`) **survives** (`2^{p0−v} = 1.3069723767… < 1.306973`),
but his printed bonus `1/15218` and [JC26]'s derived "unrounded base
`1.306972376565153…`" for Scheder's analysis are microscopically wrong
(true corrected value `1.3069723767157…`); [JC26]'s "old" lifted row
(`1.307031593709762…`) inherits the same microscopic optimism.  [JC26]'s
own new results never use eq. (2) (certified); `γ_new > γ_old` holds a
fortiori against the corrected (smaller) old bonus.  **No effect on the
new frontier.**

**Provenance defects (recorded, non-mathematical):** artifact repo
certificate is `…rational-v5` while the paper says `…rational-v6` (no v6
public); `REVISION_NOTES.md` listed in the README with a SHA-256 but
absent from the repo; checker committed under an upload-artifact
filename (bytes match the README checksum).

**Publication-status finding (structural):** every k = 3 numeric import
(both coefficient displays, Eq. (11), Lemma 34, the endgame, Theorem 6)
exists **only in the unrefereed ECCC report TR21-069 Revision 1**.  The
refereed TheoretiCS 2024 version deliberately dropped the whole k = 3
part, stating its constants are not tight; only the change-of-measure
identity is refereed.  A refereed 12-page FOCS 2021 extended abstract
exists but was not frozen; it cannot be assumed to contain the detailed
displays.  [JC26]'s certificate therefore inherits the evidentiary
status of an unrefereed technical report at every numeric layer above
the change of measure — now mitigated by this cycle's independent
certifications of the load-bearing hairline constants (R1–R3 above,
Lemma 55's `0.001687` with margin `3.6·10⁻⁷`, `BFS − DFB ≥ 0.030966`
with margin `5.2·10⁻⁷`, the full §8 closed-form family re-integrated
symbolically, and the falsity of the printed `JUNK₂ ≤ 0.000184`
certified harmless downstream).

**Residual unverified mass (stated honestly).**  The probabilistic core
of Scheder's §§5–8 (critical clause trees, cuts, the correlated §7
distribution, Theorem 65's derivation, the §7.6 bijection machinery) and
of SS's Theorem 1.17 was verified at STATEMENT level (hypotheses,
quantifiers, displays), not re-proved line-by-line; that is the accepted
import discipline of this repository (FLSY precedent).  One float-level
reconnaissance discrepancy in the source's §7.7 (printed
`DFS2CC ≤ 0.0455` vs recomputed `≈ 0.04575`; printed
`JUNK2CC ≤ −0.019` vs recomputed `≈ +0.00098`) could not be reconciled
with the printed text; a certified robustness envelope shows the dual
certificate tolerates a `c_T` degradation 33.5× larger than the worst
reading of that discrepancy, and `γ*` does not depend on `c_T` at all
(it depends only on `A`, `P_reg`, `b_1`), so the certified value is
insensitive to it.  This is recorded as an open source-side erratum
candidate, not a validation blocker.

## 4. Independent-checker finding register

* F1 (above) — the only arithmetic defect found anywhere in the audit.
* Version v5/v6 mismatch (above).
* JSON-only thresholds (1.306972376566, 0.0503, 0.04668) verified true.
* All margins of the paper's Appendix B table replicated with ≥ 17–65
  significant digits; smallest margin in the whole certificate chain:
  the two safe-branch margins exceed their claimed `2.69/2.70·10⁻¹¹`
  by only `4.2/5.1·10⁻¹⁴` — genuine but thin; exact arithmetic is
  load-bearing (floats cannot resolve the `10⁻²⁶`-wide root brackets:
  both endpoints evaluate to the same float).

## 5. Stage-V mandate items — disposition

1. Authors' checker run: **done, passes, reproduces frozen transcript.**
2. Independent checker from scratch: **done (arms-length), 89/90 + F1.**
3. LP reconstruction + corner verification from first principles:
   **done; corner confirmed as the unique optimum with positive `i_0`
   and `tau` dual slacks — not inferred from the certificate.**
4. Scheder verbatim import ledger: **done; I1–I10 with repairs R1–R4.**
5. Unique-to-general lifting verification: **done; SS ledger CLEAN;
   [JC26]'s own lifting lemmas re-proved; instantiation certified.**
6. Numerical instability / order-of-limits search: **done; the
   fixed-`w` packaging identified as the one real order-of-limits gap
   and repaired (R5); no floating-point sign risk anywhere (exact
   rationals end-to-end).**

## 6. Frontier statement after Stage V

* Certified randomized general 3-SAT: **`O(1.307031578^n)`** ([JC26]
  Corollary 1.2, validated with repairs; quantifier form per R5).
* Certified randomized Unique-3-SAT: **`O(1.306969598^n)`** ([JC26]
  Theorem 1.1, same status).
* Best *refereed* explicit numeric predecessor: Hertli's `O(1.30704^n)`
  (general, modified PPSZ).  Scheder's `1.306973` (unique) is
  ECCC/FOCS-level; the "old general base `1.307031594`" is [JC26]'s own
  computation and should be attributed to them (with the F1-corrected
  value being microscopically larger).
* Stage-I target: a certified general-3-SAT base **strictly below
  `1.307031578`**, via at least one new proved valid structural
  inequality on `(i_0, i_1, tau)` (closure-based TwoCC semantics per
  R4), strictly violated at the LP corner — pursued
  falsification-first per the cycle mandate.

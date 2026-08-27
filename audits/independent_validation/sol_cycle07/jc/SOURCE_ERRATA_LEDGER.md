# Cycle-7 Jiang--Cai source and errata ledger

Independent retrieval/audit date: **2026-08-27** (Europe/Madrid).

This ledger was prepared from fresh downloads before comparison with
`research_cycle_07/frozen_sources`.  Hex digests are SHA-256 over the downloaded
bytes.  The mathematical sources did **not** change since Cycle 7.  The only
byte-level trap was Git's Windows `core.autocrlf`: hashes below are the bytes of
the immutable Git blobs/raw URLs, not CRLF-converted checkout files.

## Primary-source manifest

### Jiang--Cai, arXiv:2607.10697v1

Submitted 2026-07-12; v1 is still the only arXiv version.

| Artifact | Exact URL | SHA-256 | Cycle-7 comparison |
|---|---|---|---|
| v1 PDF | `https://arxiv.org/pdf/2607.10697v1` | `c2930b052b0d2da5186e09fc2297df6a1e777c1812c64b05f39daf28516b6db3` | byte-identical |
| v1 source bundle | `https://export.arxiv.org/e-print/2607.10697v1` | `30a0de3271e5b96c97caa5bdf4a764dad71f31f2cb5226c98438a1074110dd87` | byte-identical |
| source-bundle metadata member | member `00README.json` | `973a86d06c005e8fe9c3d5360f3313201f0513c59ecfd649634168e2f67190df` | byte-identical |
| extracted TeX | member `a_better_analysis_for_ppsz_3_.tex` | `ec1a49684387e4dd3542d2239d8badaeafe6353db27558c70a78c8da0cdf9758` | byte-identical |
| abstract metadata page | `https://arxiv.org/abs/2607.10697` | `0331d2cf43870d1fd7bfbcaa67b1aa52f10ab183dab54e6b09dddc7d07c14f68` | byte-identical |

For completeness, the explicit-version metadata endpoint
`https://arxiv.org/abs/2607.10697v1` hashes to
`abf4c7252c0d2815c62e2183f45167a3f858f9d93fddda03bee0a273fea09c6b`.
It differs from the unversioned page only by `v1` in titles/download links; this
is endpoint rendering, not a source change.

### Authors' public artifact

Repository: `https://github.com/jiangxioabai/A-Better-Analysis-For-PPSZ.git`.
Fresh clone HEAD and Cycle-7 recorded HEAD are the same immutable commit:

* commit `3e732e06fee90d10e31c157fb433699e7f766fdc`, 2026-07-12T16:27:55+08:00,
  subject `Update README.md`;
* tree `00ceebedd63234377458e29ce51bb67f3812a9ff`;
* parent `324e8f1ebd9863ac2698e3ef50e8956bf4048141`.

| Git path at that commit | Git blob | Raw-blob SHA-256 | Cycle-7 comparison |
|---|---|---|---|
| `README.md` | `1cbee1babc5ac84f6425350caf26c71454dd8a1d` | `9fb22aae04cccc799e82943a2136bc2eef6d4883b2aa04729c555c599d8ab529` | byte-identical |
| `ppsz_certificate.json` | `ae5a1a831f5e49a2902d293a25d41b15c8146943` | `d683abf6fad7ed6b9983c782ae4308a66511cbfb938106b7dac1ee9ebb2aca5c` | byte-identical |
| `verification_output.txt` | `94a651e022c9ef37165abb0bd6aedf92e13c9868` | `1b5a8779d9d65bb785f895ec6c46fd4a94b0a987f3dca19ef6e88209c2ff0879` | byte-identical |
| `verify_ppsz_constants(1) (1).py` | `f3f2d281bc5d84435418dcd001de3a28ecd634a5` | `1d29144b25b7a72de963787b587b804c443c3fef7ff3bfc33782a07ffd956be5` | byte-identical |

Raw files were independently fetched from
`https://raw.githubusercontent.com/jiangxioabai/A-Better-Analysis-For-PPSZ/3e732e06fee90d10e31c157fb433699e7f766fdc/<path>`.

Artifact documentation defects, all non-source-change findings:

* the JSON says `2026-07-12-rational-v5`, while the paper says
  `2026-07-12-rational-v6`;
* the README names `verify_ppsz_constants.py`, while the tracked filename has
  the suffix `(1) (1)`;
* the README lists `REVISION_NOTES.md` and its alleged SHA-256
  `567c1f51345e3a436ad852eed4b80d83fe87b315d68e5702627239157bd6b86e`,
  but no such path exists in the tree.

The authors' checker was run from the fresh checkout with Python 3.13.12.  It
exited 0 and ended `ALL CHECKS PASSED`.  Its stdout is exactly the committed
transcript after LF/CRLF normalization (the CRLF checkout/run hash is
`dd83b1b1a0d5d8c8543f48ba313c2009941ea6e909e5de6ed922f2a403ed543c`).
This is reproducibility evidence only, not independent mathematical evidence.

### Scheder sources

The exact imported k=3 source is the ECCC revision named in Jiang--Cai's
bibliography.  The later arXiv manuscript is distinct (it changes k=3 constants),
and the refereed v2/TheoretiCS article drops the k=3 numerical analysis.

| Source/version | Exact URL | SHA-256 | Cycle-7 comparison |
|---|---|---|---|
| ECCC TR21-069, Revision 1, 2021-10-15 | `https://eccc.weizmann.ac.il/report/2021/069/revision/1/download/` | `e4d634c4ea46f58041fd35bfd4978b7bb95e77ad26530735aa0577822dc4e506` | byte-identical |
| arXiv:2207.11071v1, 2022-07-22, full k=3 manuscript | `https://arxiv.org/pdf/2207.11071v1` | `186eb5f0695a144952d4054fa91a7cd0153c40b0109a6385b534e57ec3917c60` | fresh additional corroborating source; no Cycle-7 counterpart |
| arXiv:2207.11071v2, 2024-03-12, k=3 part removed | `https://arxiv.org/pdf/2207.11071v2` | `fbcb127dc6e6f30277297ae3400fccbe39bb852a1fa65a318f6b8c3219e0ae94` | byte-identical |
| TheoretiCS 3 (2024), article 5 | `https://theoretics.episciences.org/13222/pdf` | `fbcb127dc6e6f30277297ae3400fccbe39bb852a1fa65a318f6b8c3219e0ae94` | byte-identical; also byte-identical to arXiv v2 |

The ECCC revision, not arXiv v1, contains the exact `10118`, `41391`,
`1380`, and `15218` chain transcribed by Jiang--Cai.  The later arXiv v1
instead prints `10397`, `45408`, and `15275`; it cannot silently be substituted
into the JC import.

### Scheder--Steinberger unique-to-general sources

| Source/version | Exact URL | SHA-256 | Cycle-7 comparison |
|---|---|---|---|
| CCC 2017, LIPIcs 79, paper 9, DOI `10.4230/LIPIcs.CCC.2017.9` | `https://drops.dagstuhl.de/storage/00lipics/lipics-vol079-ccc2017/LIPIcs.CCC.2017.9/LIPIcs.CCC.2017.9.pdf` | `43ff64c4b249cb91c4788439e8ebf3666a82b8f4a8cc097f314adb1285914a30` | byte-identical |
| Computational Complexity 33:13 (2024), DOI `10.1007/s00037-024-00259-y` | `https://link.springer.com/content/pdf/10.1007/s00037-024-00259-y.pdf` | `20eae9e7a05a8384c271212b0cb157653d018eee869ad49f61e8b4162d79d88a` | byte-identical |

The legacy TheoretiCS endpoint `https://theoretics.episciences.org/9832/pdf`
redirected to the final `13222/pdf` URL above.  The German National Library
mirror `https://d-nb.info/1357042876/34` served the same Scheder--Steinberger
journal bytes as the official Springer URL.  These redirects/mirrors do not
represent version changes.

**Source-change verdict:** no mathematical primary source or Git blob used by
Cycle 7 changed.  There is therefore no `SOURCE CHANGED` explanation for any
finding below.

## Exact 89/90 disposition

The sole failed Cycle-7 subcheck is ID **`09d`**: the terminal inequality in
JC equation (2), inherited verbatim from ECCC p. 21,

`max{(1-irr)/10118 - 1/41391, irr/1380} >= 1/15218`.

The two affine branches meet at

* `irr* = 7192790/79318953`, and
* exact minimax `v = 31273/475913718 = 1/(15218+1204/31273)`.

Thus

`v - 1/15218 = -43/258659105733 < 0`.

The clean integer-denominator repair is `v >= 1/15219`.  Classification:

**source-statement defect with valid repaired claim**.

It is not a checker mismatch, diagnostic, or documentation error.  JC
transcribed Scheder faithfully.  The repaired unique base is
`1.3069723767157558885... < 1.306972377`.  Propagating the repair through the
same lifting gives `1.3070315937106168663... < 1.307031594`; hence the rounded
old rows survive, although the old unrounded display `<1.307031593710` does not.
JC's new bounds do not use `1/15218` to derive their gain.

## Epsilon-R import-domain ledger

JC uses the exact rational

`epsilon_R = 0.1024756190168075228998451658 > 0.1`.

Tracing the ECCC Section 7 dependency chain found only these restrictive
source-side conditions at that point:

1. the general Section-7 constructions and numerical claims state
   `epsilon <= 0.13`;
2. Proposition C.12 itself states `epsilon <= 0.1` for the OCB/MLB cleanup;
3. Proposition C.13(2) uses `1/1150 >= Thr`, hence requires
   `Thr <= 1/1150`.

At the JC point, the standalone exact repair in
`scheder_source_validator.py` proves on both exact branches of `delta_max`,
for every `r in [0,1/2]`, all facts needed by C.12:

* `delta >= 0`, `0 <= s <= r`, and `s' >= 0`;
* the `0.95` prefactor bound;
* `f(r) >= 0.98 f(s(r))`;
* `s'(r) <= 1.05`;
* `g(r) >= 0.945 g(s(r))`.

These are 32 exact polynomial/rational sign certificates (Sturm sequences,
zero interior roots), not a grid.  They imply C.12's `0.88` and `0.9`
integral constants directly.  The paper's broad extension to all
`epsilon <= 0.13` is false: at `epsilon=13/100`, `r=5/12`,
`1.05-s'(r)=-3923/343000`.

JC chooses

`Thr = 3740933169559153155446980603853942527036929295082051503901 /
       16875000000000000000000000000000000000000000000000000000000000
     = 0.000221684928566468... < 1/1150`.

Therefore the explicit verdict is **EPS-R-REPAIR-SOUND** at the fixed operating
point.  The JC statements "every epsilon_R <= .13" and "every Thr>0" must not
survive; only the fixed certified point (or a separately certified smaller
domain) is supported.

## Scheder errata ledger

Allowed classification labels are used verbatim.  `REAL-ERROR-AFFECTS-JC`
means JC imported the affected statement; it does not mean the new frontier
fails after the repair described here.

| Primary location/claim | Reconstruction | Classification | Effect |
|---|---|---|---|
| ECCC p. 21, `>=1/15218` | Exact minimax is `31273/475913718`, short by `43/258659105733` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | Rounded old unique/general bases survive; new JC gain unaffected |
| ECCC p. 51, Lemma 75 Case 4, `10 r^2(1-2r)^2 <=10/256`, hence `epsilon<=256/600` | `1/8-r(1-2r)=2(r-1/4)^2`, so max is `10/64` and cap is `64/600` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** at JC's fixed `epsilon_I`; JC's advertised full `[0,1/5]` range is **REAL-ERROR-AFFECTS-JC** as a statement | `epsilon_I=0.073072...<64/600` |
| ECCC pp. 77--78, C.12 printed hypothesis `epsilon<=.1` | The printed hypothesis itself is accurate; JC uses a point above it | **NOT-AN-ERROR** in Scheder; JC's broadened hypothesis is **REAL-ERROR-AFFECTS-JC** | Fixed-point exact repair above is sound |
| C.12 proof's internal `s'<=1.05 provided epsilon<=.13` | Exact counterexample `(epsilon,r)=(13/100,5/12)` gives deficit `-3923/343000` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | C.12 only states `.1`; JC fixed point separately certified |
| ECCC p. 79, C.13(2), implicit `Thr<=1/1150` | `OCB*(4)=0.000869965582596...>1/1150`; source step is valid only with the cap | **REAL-ERROR-AFFECTS-JC** (quantifier omission) | JC's exact Thr satisfies it |
| ECCC p. 45, second regular-gain line marked `=` after `.0064 -> .006404` and `5/(48 ln2) -> .1503` | Both are safe weakenings, so the symbol must be `>=` | **TYPO-ONLY** | No numerical damage |
| ECCC p. 44, fact 1 restates `2|TwoCC|` rather than equation (11)'s `3|TwoCC|` | The p. 45 derivation uses 3 | **TYPO-ONLY** | Unused bad restatement |
| ECCC p. 47, Definition 68, `JUNK2<=.000184` | Exact value `8767591/192-65880 ln2 = .0002030441363489...`; nevertheless `JUNK1+2JUNK2=.00274200799889...<.0028` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | JC irregular coefficient `.0028` survives |
| ECCC p. 54, Section 8.3, `DFD2CC<=.074135` | Exact `11420 ln2-23747/3=.07413532790876...`; exact sum with DFS is `.24047413427028...<.2405` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | JC `.2405` survives.  Cycle 7's recorded `.2404721` should be corrected to `.240474134270...` |
| ECCC p. 44, Section 7.7, `DFS2CC<=.0455`, `DFD2CC<=.0095`, `JUNK2CC<=-.019` | Certified enclosures: DFS `[.0457381642502,.0457916473409]`, DFD `[.00948391710827,.00948536594530]`, JUNK `[.000982872183387,.000984810990365]` | **REAL-ERROR-AFFECTS-JC** | Replace regular TwoCC damage `.055 epsilon` by the safe `.05529 epsilon+.001 epsilon^2`; repaired tau-dual slack is `.0133919191881...>0`; optimum/frontier unchanged because its primal point has `tau=0` |
| ECCC p. 48, Lemma 73, printed `epsilon<=4/5` | Its displayed condition reduces to `epsilon<=2/5` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | JC fixed `epsilon_I` (and `[0,.2]`) is safe |
| ECCC p. 51, Lemma 75 Case 3 inequality direction | Multiplication by the negative factor reverses the displayed comparison; intended direction proves the next line | **TYPO-ONLY** | No numerical damage |
| ECCC p. 61, Lemma A.3, `sum deg_SG=n` | Handshake lemma gives `2n`; the following cancellation/conclusion is the one obtained with `2n` | **TYPO-ONLY** | Lemma 34 survives; later arXiv v1 prints `2n` |
| ECCC/TheoretiCS p. 5 cites the lifting theorem as `[8]` despite attributing it to Scheder--Steinberger | Bibliographic cross-reference is wrong | **TYPO-ONLY** | Provenance/documentation only |

The load-bearing regular/irregular decimal coefficients were independently
re-derived from their defining integrals.  Apart from the repaired regular
TwoCC term just listed, the JC fixed-point affine inequalities retain their
claimed conservative directions.

## Scheder--Steinberger import verdict

The 2024 journal source supplies:

* Theorem 1.10: the finite heuristic has error `c_k+epsilon_{w,k}` with
  `epsilon_{w,k}->0`;
* Definitions 1.14--1.15: closure under restrictions and monotonicity;
* Observation 1.16: `Q(pi,alpha)=1/n! * 2^{-I(pi,alpha)}`;
* Main Theorem 1.17: success at least `2^{-pn+(p-p*) E_Q I}`;
* Lifting Theorem 1.18 and its Section 3.1 large-/small-liquid-set proof.

The printed statement of Main Theorem 1.17 omits monotonicity/closure, although
its proof explicitly invokes Lemma 3.3 with those hypotheses.  JC safely adds
them.  For 3-CNF and `P^(w)`, both are satisfied.  Reconstructing the two cases
gives exactly JC's `q0*delta` high branch and
`gamma(1-delta)-(1-p0)delta-h2(delta)` unique-residual branch.  JC's liquid-set
restriction lemma and prefix-realization argument correctly handle integrality,
extension to `floor(delta n)`, conditioning, and reuse of the heuristic.

**SS lifting verdict: SOUND WITH AN EXPLICIT-HYPOTHESIS REPAIR.**  No numerical
or logical defect was found in JC's quantitative specialization.  The fresh
exact validator certifies both root brackets, uniqueness by monotonicity, both
branch margins, and the final safe base `<1.307031578`.

The separate finite-strength caveat lies in the Scheder unique-case input:
ECCC proves its estimates for a slowly growing `w(n)` and `o(n)` errors, not
JC's literal uniform fixed-`w` decomposition `xi(w)n+r_w(n)`.  The latter is not
established by the cited source.  Downgrading to source-verbatim slowly growing
`w(n)` preserves the `O^*` Unique and general running-time bases because one may
choose `w(n)->infinity` with `w(n)=o(n/log n)`, so a run costs
`n^{O(w(n))}=2^{o(n)}`.  A literal fixed-`w` theorem needs a new proof.

## Fresh-tool count and independence

`jc_exact_validator.py` was designed and implemented before either prohibited
Cycle-7 checker was opened; the frozen design is in `CHECKER_DESIGN.md`.  It
does not read/import the authors' checker or any Cycle-7 checker.  It transcribes
the primary-paper formulas and uses only standard-library `Fraction` closed
intervals.  Every proof decision is rational; decimals are display only.

Its final run reports **72 passed proof obligations**.  Separately, it prints
**49 transcendental evaluations** (atanh-log or Taylor-exp), each with exactly
90 terms and an exact rational remainder bound.  The 49 ledger entries are not
added to 72 and are not presented as a replica of Cycle 7's heterogeneous
"90".  The 72 obligations cover all mathematical JSON fields, coefficient
enclosures, domains, signs/slacks, symbolic primal/dual identities, root signs,
monotonicity, branch margins, bases, and the repaired old minimax/lift.

`scheder_source_validator.py` is also fresh.  Its only scalar counter is **37
exact Sturm sign certificates**: 32 for the fixed-point C.12 repair and 5 for
density derivative bounds.  Its additional printed exact identities, rational
log-form integrals, and certified interval integrations are fail-fast proof
obligations but are deliberately not folded into that 37 count.

Reproduction commands from the repository root:

```text
python -B audits/independent_validation/sol_cycle07/jc/jc_exact_validator.py
python -B audits/independent_validation/sol_cycle07/jc/scheder_source_validator.py
```

Both exit 0.

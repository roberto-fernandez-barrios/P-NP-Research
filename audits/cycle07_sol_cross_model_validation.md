# Independent cross-model hostile validation of Research Cycle 7

**Audit date:** 2026-08-27 (Europe/Madrid)
**Audit branch:** `cycle07-sol-validation`
**Audited base:** `e126b88b3274bcb407f066f21882e2d687f028f1`, created directly from `cycle07-o18-fable`
**Scope:** Cycle 7 only. No Cycle 8 work, new PPSZ-bound search, Jiang--Cai improvement, merge, or candidate-file edit was performed.

## Verdicts

```text
JC-CERTIFICATE: VALIDATED
JC-IMPORTS: VALIDATED-WITH-STATEMENT-AND-DOMAIN-REPAIRS
EPSILON-R-REPAIR: EPS-R-REPAIR-SOUND
SCHEDER-ERRATA: CONFIRMED-WITH-ADDITIONAL-EXACT-REPAIR
LP-RECONSTRUCTION: SOUND-AFTER-SOURCE-COEFFICIENT-REPAIR
THEOREM-CR: SOUND-WITH-REPAIRS
COROLLARY-CR1: CR1-SOUND-WITH-REPAIRS
COROLLARY-CR2: FALSE-AS-STATED; INFIMUM-FORM-SOUND
OLD-STATISTIC-NOGO: SOUND-IN-FIXED-OBJECTIVE-INFIMUM-FORM
NOVELTY: POTENTIALLY-NOVEL

PRIMARY VERDICT: CYCLE07-VALIDATED-WITH-MINOR-CORRECTIONS
```

Here “minor corrections” describes the effect on the surviving Cycle-7 conclusions: neither headline running-time base, the LP optimizer/value, Theorem CR's repaired mathematical statement, CR-1's closed segment, nor the final “new estimates or new information/statistics” strategy changes. It does **not** mean that every repair is trivial. The all-parameter CR proof needs a new uniform argument, the source's Section 7.7 coefficient needs a certified replacement, and literal Corollary CR-2 is false without a topology/infimum qualification.

No claim here is a P-versus-NP resolution, a formal proof, or an externally validated novelty claim.

## 1. Independence boundary and method

The audit began by reading `INITIAL_RESEARCH_MISSION.md`, `RESEARCH_STATE.md`, the literature/proof/experiment inventory, and the branch state. The branch and merge-base checks gave the base above and a clean initial worktree.

The mathematical lanes were then separated:

1. The Jiang--Cai validator design was frozen before either Cycle-7 checker was opened. The new implementation imports neither the authors' checker nor any Cycle-7 checker. It uses `fractions.Fraction` intervals, exact symbolic identities, exact Sturm sequences, and certified series remainders.
2. The LP was reconstructed from the fresh Jiang--Cai TeX and Scheder source before comparing it with Cycle 7's LP note or dual.
3. The CR derivation used only the raw construction statement at first. Its proof section, both prohibited Cycle-7 implementations, and the stored 21-instance certificate were withheld until the derivation and fresh engine were frozen.
4. The source PDFs were freshly downloaded, hashed, text-extracted, rendered where layout mattered, and visually checked at the operative pages: Scheder Definition 31, the Section-6 endgame, Sections 7.7--7.8, Lemma 75, and Proposition C.12.
5. The authors' checker was run, but its success is recorded only as reproducibility evidence. It is not counted as independent evidence.

The fresh implementations are under `audits/independent_validation/sol_cycle07/`, as required.

## 2. Frozen external sources

All core sources were retrieved on 2026-08-27. SHA-256 values below are over the retrieved bytes. The fuller immutable-blob manifest is in `independent_validation/sol_cycle07/jc/SOURCE_ERRATA_LEDGER.md`.

### 2.1 Jiang--Cai arXiv v1

| Artifact | Version and URL | SHA-256 | Comparison with Cycle 7 |
|---|---|---|---|
| PDF | arXiv:2607.10697v1, submitted 2026-07-12, [PDF](https://arxiv.org/pdf/2607.10697v1) | `c2930b052b0d2da5186e09fc2297df6a1e777c1812c64b05f39daf28516b6db3` | byte-identical |
| source bundle | v1, [e-print](https://export.arxiv.org/e-print/2607.10697v1) | `30a0de3271e5b96c97caa5bdf4a764dad71f31f2cb5226c98438a1074110dd87` | byte-identical |
| `00README.json` | source-bundle member | `973a86d06c005e8fe9c3d5360f3313201f0513c59ecfd649634168e2f67190df` | byte-identical |
| TeX | `a_better_analysis_for_ppsz_3_.tex` | `ec1a49684387e4dd3542d2239d8badaeafe6353db27558c70a78c8da0cdf9758` | byte-identical |
| unversioned metadata | [abstract page](https://arxiv.org/abs/2607.10697) | `0331d2cf43870d1fd7bfbcaa67b1aa52f10ab183dab54e6b09dddc7d07c14f68` | byte-identical |

The explicit `/abs/2607.10697v1` rendering has SHA-256 `abf4c7252c0d2815c62e2183f45167a3f858f9d93fddda03bee0a273fea09c6b`; its endpoint-level HTML difference is not a mathematical version change. No arXiv version later than v1 was present on the audit date.

### 2.2 Authors' artifact repository

Repository: [jiangxioabai/A-Better-Analysis-For-PPSZ](https://github.com/jiangxioabai/A-Better-Analysis-For-PPSZ). Fresh `main`/`HEAD` remained commit `3e732e06fee90d10e31c157fb433699e7f766fdc` (2026-07-12), tree `00ceebedd63234377458e29ce51bb67f3812a9ff`, parent `324e8f1ebd9863ac2698e3ef50e8956bf4048141`.

| Path at the pinned commit | Git blob | raw-byte SHA-256 | Comparison |
|---|---|---|---|
| `README.md` | `1cbee1babc5ac84f6425350caf26c71454dd8a1d` | `9fb22aae04cccc799e82943a2136bc2eef6d4883b2aa04729c555c599d8ab529` | byte-identical |
| `ppsz_certificate.json` | `ae5a1a831f5e49a2902d293a25d41b15c8146943` | `d683abf6fad7ed6b9983c782ae4308a66511cbfb938106b7dac1ee9ebb2aca5c` | byte-identical |
| `verification_output.txt` | `94a651e022c9ef37165abb0bd6aedf92e13c9868` | `1b5a8779d9d65bb785f895ec6c46fd4a94b0a987f3dca19ef6e88209c2ff0879` | byte-identical |
| `verify_ppsz_constants(1) (1).py` | `f3f2d281bc5d84435418dcd001de3a28ecd634a5` | `1d29144b25b7a72de963787b587b804c443c3fef7ff3bfc33782a07ffd956be5` | byte-identical |

The artifact has three documentation/reproducibility defects: the JSON calls itself rational-v5 while the paper says v6; the README gives a different checker filename; and it advertises a nonexistent `REVISION_NOTES.md`. These are packaging defects, not evidence against the mathematics.

### 2.3 Scheder sources

| Source | Exact version and URL | SHA-256 | Role/comparison |
|---|---|---|---|
| ECCC | TR21-069 Revision 1, 2021-10-15, [download](https://eccc.weizmann.ac.il/report/2021/069/revision/1/download/) | `e4d634c4ea46f58041fd35bfd4978b7bb95e77ad26530735aa0577822dc4e506` | JC's exact numerical source; byte-identical |
| arXiv | 2207.11071v1, 2022-07-22, [PDF](https://arxiv.org/pdf/2207.11071v1) | `186eb5f0695a144952d4054fa91a7cd0153c40b0109a6385b534e57ec3917c60` | additional fresh comparison; numerically distinct from ECCC |
| arXiv | 2207.11071v2, 2024-03-12, [PDF](https://arxiv.org/pdf/2207.11071v2) | `fbcb127dc6e6f30277297ae3400fccbe39bb852a1fa65a318f6b8c3219e0ae94` | byte-identical to Cycle 7 and journal; k=3 numerics removed |
| TheoretiCS | volume 3 (2024), article 5, [PDF](https://theoretics.episciences.org/13222/pdf) | `fbcb127dc6e6f30277297ae3400fccbe39bb852a1fa65a318f6b8c3219e0ae94` | byte-identical to arXiv v2 |

The ECCC revision contains the imported `10118`, `41391`, `1380`, and `15218` chain. ArXiv v1 instead has different historical constants, so it cannot be substituted silently. The refereed 2024 version deliberately omits the k=3 numerical part.

### 2.4 Scheder--Steinberger unique-to-general sources

| Source | Version and URL | SHA-256 | Comparison |
|---|---|---|---|
| CCC 2017 | LIPIcs 79, paper 9, DOI 10.4230/LIPIcs.CCC.2017.9, [PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol079-ccc2017/LIPIcs.CCC.2017.9/LIPIcs.CCC.2017.9.pdf) | `43ff64c4b249cb91c4788439e8ebf3666a82b8f4a8cc097f314adb1285914a30` | byte-identical |
| Computational Complexity 2024 | 33:13, DOI 10.1007/s00037-024-00259-y, [PDF](https://link.springer.com/content/pdf/10.1007/s00037-024-00259-y.pdf) | `20eae9e7a05a8384c271212b0cb157653d018eee869ad49f61e8b4162d79d88a` | byte-identical |

The legacy TheoretiCS and German National Library URLs redirected/served the same bytes as the final publisher URLs; no source version changed.

**Source-change finding:** no mathematical source or Git blob used by Cycle 7 changed. Accordingly, none of the mathematical findings below is classified as `SOURCE CHANGED`; they are source-statement defects, JC import-statement defects, or Cycle-7 proof/status defects.

## 3. Jiang--Cai certificate reconstructed from zero

The public checker exits 0 with `ALL CHECKS PASSED`, and its transcript is reproduced modulo LF/CRLF. That observation is deliberately non-independent.

The fresh checker recomputes all certificate fields from the printed formulas. It reports 72 passed proof obligations. Separately, it records 49 logarithm/exponential evaluations, each with exactly 90 terms and an exact rational remainder. The largest displayed remainder bounds are below `5.44e-89` for logarithms and `2.12e-190` for exponentials. No pass/fail decision uses ordinary floating point.

At the exact parameters

```text
epsilon_R = 0.1024756190168075228998451658
epsilon_I = 0.07307238160252154687451293138
```

the original printed coefficients are enclosed by

| quantity | certified value/enclosure |
|---|---:|
| `A` | `0.00009975821785491075081191948277...` |
| `P_reg` | `0.00002498903030970015978061198356...` |
| original `S` | `0.002354451478220411392370256683...` |
| `b_0` | `0.003631968772856013971666915295...` |
| `b_1` | `0.001145497395959033093542833420...` |
| `b_T` | `-0.01318180201458237930429026217...` |

All parameter-domain tests, coefficient enclosures, and signs pass. The hidden source condition `Thr <= 1/1150` also passes at JC's exact `Thr = 0.000221684928566468...`.

For the original printed affine coefficient, the dual slacks are

```text
b_0 - 2 b_1                         = 0.001340973980937947784581248454... > 0
b_T + (b_1/A) S                     = 0.01385374548423064739326101447...  > 0
```

The Section-7.7 source repair changes only the `tau` coefficient. A safe replacement is

```text
c_T,rep = 0.009307 - 0.05529 epsilon_R - 0.001 epsilon_R^2
          - 0.1503 f_KL(epsilon_R),
S_rep   = c_T,rep - 5A
        = 0.002314232296212659327102982475... .
```

The repaired `tau` dual slack remains

```text
b_T + (b_1/A) S_rep = 0.0133919191881305264... > 0.
```

Thus the repaired LP has the same optimizer and value. The exact-optimum enclosures are

```text
i_1* in [0.060043244708778326627395247971,
         0.060043244708778326627395247972]

gamma* in [0.000068779380458836565503549434,
           0.000068779380458836565503549435].
```

JC uses the safe theorem gain `gamma_new=0.0000687793 < gamma*`. Certified final values are

```text
Unique base  = 1.306969597516246982445914854... < 1.306969598
general base = 1.307031577931205253443608607... < 1.307031578.
```

The new lifting root is bracketed by

```text
[0.00000338183369577144614,
 0.00000338183369577144615],
```

with exact negative/positive endpoint signs and strict monotonicity on `(0,1/2)`. The safe separator `delta=0.00000338183369` has margins

```text
large-I branch:        2.6941529384223982e-11 > 0
unique-residual branch:2.7050581864978499e-11 > 0.
```

The historical printed-old root and independently repaired-old root were also checked:

```text
printed-old root:  [0.00000321978491531273261, 0.00000321978491531273262]
repaired-old root: [0.00000321977615008507678, 0.00000321977615008507680].
```

Every root bracket has certified opposite endpoint signs; the entropy-root functions are strictly increasing on the relevant interval.

**Certificate conclusion:** the repaired Unique and general Jiang--Cai frontier is independently certified. The source/import corrections below do not consume the positive numerical margins.

## 4. The exact 89/90 issue

The vague “89/90” is resolved. The sole failed Cycle-7 subcheck is ID **09d**, the terminal old endgame claim inherited from Scheder ECCC p. 21 and transcribed in JC equation (2):

```text
min_{irr >= 0} max{(1-irr)/10118 - 1/41391, irr/1380} >= 1/15218.
```

The branches meet uniquely at

```text
irr* = 7192790/79318953,
v    = 31273/475913718 = 1/(15218 + 1204/31273).
```

Exact comparison gives

```text
v - 1/15218 = -43/258659105733 < 0.
```

The valid clean statement is `v >= 1/15219`, or preferably the exact equality above. Its required classification is:

```text
source-statement defect with valid repaired claim
```

It is neither a checker mismatch nor an irrelevant diagnostic. JC transcribed the bad source display faithfully. The repaired old Unique base is `1.3069723767157558885... < 1.306972377`; after the same lift the old general base is `1.3070315937106168663... < 1.307031594`. The tighter old display `<1.307031593710` is false, but the rounded historical row and all new JC values survive.

## 5. Epsilon-R and import-chain repair

Scheder Proposition C.12 is printed with the hypothesis `epsilon <= 0.1`; JC's exact point is larger. This is not a typo in that proposition and could not be waived by numerical sampling.

The fresh repair traces every restrictive Section-7 condition used at the point:

1. the surrounding construction uses `epsilon <= 0.13`;
2. Proposition C.12 itself requires `epsilon <= 0.1`;
3. Proposition C.13(2) silently requires `Thr <= 1/1150`.

On both exact rational branches of Scheder's `delta_max`, exact Sturm-sequence certificates prove, for all `r in [0,1/2]`,

```text
delta >= 0,
0 <= s <= r,
s' >= 0,
the 0.95 prefactor bound,
f(r) >= 0.98 f(s(r)),
s'(r) <= 1.05,
g(r) >= 0.945 g(s(r)).
```

There are 32 exact sign certificates for this repair, with no interior roots on the certified branch intervals. They imply the required C.12 integral constants at JC's exact point. The attempted whole-range extension is genuinely false: at `(epsilon,r)=(13/100,5/12)`,

```text
1.05 - s'(r) = -3923/343000 < 0.
```

The hidden threshold is also safe: the independently integrated value is `OCB*(4)=0.000869965582596... > 1/1150`, and JC's `Thr` is below the cap.

The explicit domain verdict is therefore:

```text
EPS-R-REPAIR-SOUND
```

Only the fixed certified point (or another separately certified domain) may be used. JC's literal “every epsilon through .13” and “every Thr>0” formulations are unsupported.

The Scheder--Steinberger lifting chain otherwise survives. The journal's Main Theorem 1.17 statement omits monotonicity and restriction-closure assumptions used by its proof through Lemma 3.3; JC safely adds them, and the weak implication heuristic on 3-CNF satisfies them. JC's liquid-set restriction lemma and prefix-realization proof reconstruct the two lifting branches correctly.

One further source/provenance repair is necessary: Scheder proves the unique estimates for a slowly growing `w(n)` with `o(n)` error, not JC's literal uniform fixed-`w` decomposition. Taking `w(n)->infinity` slowly enough that `w(n)=o(n/log n)` gives per-run cost `n^{O(w(n))}=2^{o(n)}`; the strict base margins absorb that subexponential factor. Therefore both `O^*` frontier numbers survive, but the literal fixed-`w` theorem remains unproved and must be restated in the source-supported order of limits.

## 6. Scheder errata reconstructed from the primary source

The following labels are exactly the classification vocabulary requested. `REAL-ERROR-AFFECTS-JC` means JC imported the affected statement; it does not mean the final frontier fails after the stated repair.

| Primary claim | Exact reconstruction | Classification | Consequence |
|---|---|---|---|
| ECCC p. 21, `>=1/15218` | exact value `31273/475913718`, short by `43/258659105733` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | rounded old rows survive; new JC gain independent |
| p. 51, `10r^2(1-2r)^2 <= 10/256`, hence `epsilon<=256/600` | maximum is `10/64`, hence cap `64/600` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** at fixed `epsilon_I`; advertised `[0,1/5]` is **REAL-ERROR-AFFECTS-JC** as a range | `epsilon_I < 64/600` |
| pp. 77--78, C.12 states `epsilon<=.1` | the source hypothesis itself is accurate; JC exceeds it | **NOT-AN-ERROR** in Scheder; JC broadening is **REAL-ERROR-AFFECTS-JC** | exact point repaired above |
| C.12 proof says `s'<=1.05` through `.13` | exact counterexample has deficit `-3923/343000` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | proposition only promises `.1`; fixed point repaired |
| p. 79 implicitly uses `Thr<=1/1150` | cap is required; source margin is positive | **REAL-ERROR-AFFECTS-JC** | JC point satisfies cap |
| p. 45 writes `=` after two conservative roundings | correct relation is `>=` | **TYPO-ONLY** | none |
| p. 44 restates `2|TwoCC|` instead of equation (11)'s `3|TwoCC|` | actual derivation uses 3 | **TYPO-ONLY** | unused restatement |
| p. 47, `JUNK2<=.000184` | exact `.0002030441363489...`; downstream total `.00274200799889...<.0028` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | JC irregular coefficient survives |
| p. 54, `DFD2CC<=.074135` | exact `.07413532790876...`; exact sum `.24047413427028...<.2405` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | JC `.2405` survives; Cycle 7's `.2404721` is wrong |
| p. 44, Section 7.7 `DFS<=.0455`, `DFD<=.0095`, `JUNK<=-.019` | DFS in `[.0457381642502,.0457916473409]`; DFD in `[.00948391710827,.00948536594530]`; JUNK in `[.000982872183387,.000984810990365]` | **REAL-ERROR-AFFECTS-JC** | safe repaired envelope gives positive `tau` slack; frontier unchanged |
| p. 48, Lemma 73, `epsilon<=4/5` | displayed condition gives `epsilon<=2/5` | **REAL-ERROR-NUMERIC-CONCLUSION-SURVIVES** | JC fixed point safe |
| p. 51, Lemma 75 Case 3 direction | negative multiplication reverses comparison | **TYPO-ONLY** | intended proof continues |
| p. 61, `sum deg_SG=n` | handshake sum is `2n`; next cancellation already uses `2n` | **TYPO-ONLY** | Lemma 34 survives |
| lifting theorem cited as `[8]` despite Scheder--Steinberger attribution | wrong cross-reference | **TYPO-ONLY** | documentation only |

This confirms Cycle 7's principal errata, corrects one recorded Section-8.3 decimal, and upgrades its formerly non-certifying Section-7.7 concern to a certified source error plus a standalone repair. No repair uses a stronger unproved fact than the source chain needs at the fixed JC parameters.

## 7. Recombination LP reconstructed from first principles

Normalize the unique assignment to all ones. Select one canonical critical clause `(x or not y or not z)` per variable and put arcs `x->y,z` in the critical-clause digraph. With Scheder Definition 31's one-round augmented formula, let `TwoCC` be the variables with at least two critical clauses there. Scheder Section 8's `ID_j` excludes `TwoCC`, so the common coordinates are

```text
i_0 = |ID_0|/n,
i_1 = |ID_1|/n,
tau = |TwoCC|/n.
```

They are nonnegative and every realizable vector also satisfies `i_0+i_1+tau<=1`. JC relaxes the feasible region to the nonnegative orthant; its optimizer lies inside the simplex, so this relaxation does not change the value.

Scheder Lemma 34 and equation (11) give

```text
|H| >= n-|ID_1|-2|ID_0|-2|TwoCC|,
(18/17)|H_low|+2|H_high|+3|TwoCC| >= |H|.
```

Substitution into the two simultaneous source estimates gives the repaired affine bounds

```text
L_R(i_0,i_1,tau) = A-P_reg-2A i_0-A i_1+S_rep tau,
L_I(i_0,i_1,tau) = b_0 i_0+b_1 i_1+b_T tau,

f(i_0,i_1,tau) = max{L_R,L_I}.
```

This is the Unique-3-SAT LP. The general result is obtained afterward through Scheder--Steinberger lifting; there is no separate “general” structural LP.

Set `lambda=b_1/A`. For every point of the orthant,

```text
f >= (lambda L_R + L_I)/(1+lambda)
  = gamma*
    + [(b_0-2b_1)i_0
       +(b_T+(b_1/A)S_rep)tau]/(1+lambda).
```

Both displayed coefficients are strictly positive by the certified intervals above. Equality therefore forces `i_0=tau=0`. On that ray,

```text
f(0,i_1,0) = max{A-P_reg-A i_1, b_1 i_1},
```

the maximum of a strictly decreasing and a strictly increasing affine function. Their unique intersection is

```text
x* = (0, (A-P_reg)/(A+b_1), 0),
gamma* = b_1(A-P_reg)/(A+b_1).
```

This proves global uniqueness from first principles, without a numerical optimizer or the authors' dual. Reading the weighted proof as an epigraph dual gives the independently derived weights

```text
y_R = b_1/(A+b_1),
y_I = A/(A+b_1),
y_R+y_I=1.
```

Primal feasibility, the two active equalities, dual feasibility, the tight `i_1` equation, both positive nonactive slacks, and primal-dual equality were all checked exactly. The optimum and location claimed by Cycle 7 survive the source coefficient repair.

## 8. Theorem CR reconstructed and attacked

### 8.1 Raw construction, with pairs and triples frozen separately

Work in `Z/nZ`. For `m=m_1>0`, define

```text
b     = floor(n/3)+1,
jmax  = floor((n-3)/2),
p_i   = floor(i n/m),
s_i   = p_i-b,
P     = {p_i}, S={s_i}.
```

Choose the least `d` in

```text
[2, min(floor(n/m)-2, jmax-b)]
```

such that `Q=P+d` is disjoint from `P` and `S`, and no element of `Q` is adjacent modulo `n` to an element of `S`. Put

```text
g(x)=x+b       for x not in S,
g(s_i)=p_i+d.
```

For `m=0`, which the Cycle-7 display failed to define, take `P=S=Q=empty` and `g(x)=x+b`; no `d` is required.

Both variants contain one critical clause per variable,

```text
C_x = (x or not(x+1) or not g(x)).
```

Let `Adj` be the undirected projection of the arcs `x->x+1,g(x)`.

* The **pairs variant** adds every all-positive pair whose endpoints are nonadjacent in `Adj`.
* The **triples variant** adds every all-positive triple independent in `Adj`.

The triples variant is the robust primary carrier of the no-go result.

### 8.2 H1: all-parameter existence

Write `n=am+r`, `0<=r<m`. Since `m<=n/10`, `a=floor(n/m)>=10`. For a cyclic index difference `k`, the corresponding positive residues in `P-P` are among

```text
floor(k n/m), ceil(k n/m).
```

Consequently every nonzero circular spacing in `P-P` is at least `a`. Thus every `d<=a-2` already ensures `(P+d) cap P=empty`.

For a fixed `k`, collision with `S` or adjacency to `S` can forbid only

```text
d in {Delta-b-1, Delta-b, Delta-b+1},
```

where `Delta` takes at most two consecutive values. Hence a `k` forbids at most four consecutive integers. Consecutive forbidden-block starts are separated by at least `a`; at most one such block can intersect `[2,a-2]`. Once `jmax-b>=6`, the five candidates `2,3,4,5,6` are available, at most four are forbidden, and the least admissible `d` exists with

```text
2 <= d <= 6
```

uniformly for **every** `1<=m<=n/10`, including fixed and sublinear `m`. This is the missing all-`n` proof; a scan to 1200 is not being used as its substitute.

### 8.3 H2: exact degree statistics and widths

Translation by `b` is a permutation. Redirecting the sources `S=P-b` removes precisely the images `P` and adds precisely the distinct images `Q`. Since `P cap Q=empty`, the `g`-arc indegrees are zero on `P`, two on `Q`, and one elsewhere. The successor arcs add one everywhere. Therefore

```text
indegree 1: exactly P, size m;
indegree 3: exactly Q, size m;
indegree 2: every other vertex;
indegree 0: none.
```

For `m=0`, every indegree is two. The two outgoing children are distinct and nonlooping once the asymptotic bounds apply, and `b+d<=jmax<n/2` handles wraparound and directed 2-cycles. The conclusion does not require `P cap S=empty`, a condition incorrectly demanded in an earlier construction draft.

### 8.4 H3: unique satisfiability and repaired girth

For any assignment let `Z` be its zero variables. If `x in Z`, satisfaction of `C_x` forces at least one child of `x` into `Z`. Thus every nonempty satisfying `Z` contains a directed cycle.

Directed steps are `1`, `b`, and `b+d`. Put `c=3b-n`, so `1<=c<=3`. Suppose a directed cycle of length `ell<=17` contains `r` long edges, total exceptional offset `E`, `u=ell-r` unit edges, and winds `k` times. Then

```text
r b+E+u = k n.
```

If `r>=3k`, the left side is already strictly greater than `kn`; hence `h=3k-r>=1`, and

```text
E+u = h b-kc >= b-kc.
```

For `d<=6` and `n>357`, a length-17 walk has total step sum below `6n`, so `k<=5`. Since `E+u<=17(d+1)`, a short cycle would imply

```text
b <= 17d+32,
n <= 51d+96.
```

With `d<=6`, every `n>402` therefore has directed girth greater than 17. This proof is uniform in all allowed `m`; Cycle 7's statement “`d` is constant for `m=Theta(n)`” did not establish its theorem's all-`m` quantifier.

For `m=0`, the same winding equation has `E=0` and only steps `1,b`; the bound applies a fortiori without introducing a fictitious parameter `d`.

The undirected graph `Adj` is triangle-free: a triangle would give a signed modular sum of three elements of `{1,b,b+d}`. The cases of zero, one, two, and three long terms respectively give a nonzero small integer, a value strictly between zero and `n`, a nonzero value modulo `n` because `d>=2`, or a value strictly between consecutive multiples of `n`. Also `Delta(Adj)<=5`.

Now:

* In pairs, all vertices of a satisfying `Z` must form a clique. Triangle-freeness gives `|Z|<=2`, while closure gives a directed cycle and loops/2-cycles are absent. Contradiction.
* In triples, a directed cycle has at least 18 vertices. A maximum-degree-five graph on at least 18 vertices has an independent triple by the greedy bound. Its all-positive auxiliary clause is falsified. Contradiction.

Thus `1^n` is the unique satisfying assignment in both variants for the repaired uniform range. No second assignment or infinite counterfamily survives.

### 8.5 H4: actual Definition-31 closure and TwoCC

The freshly rendered ECCC Definition 31 defines `F~` as `F` plus all width-at-most-three clauses inferred by resolution from pairs of 3-clauses **of `F`**. The words “of `F`” make this one round, not an iterative fixed point. Scheder defines k-CNF clauses as width at most k. Because “3-clause” can still be read as exact width three in isolation, both parent-width readings were checked.

For triples:

1. two auxiliary clauses have no complementary literals;
2. a critical--auxiliary resolvent has nominal width four; a width-reducing parent collision is prohibited by independence, while the other collision is tautological;
3. a critical--critical resolvent has nominal width four; a repeated negative child would create an undirected triangle, while an opposite parent would create a directed 2-cycle.

Therefore there is **no non-tautological resolvent of width at most three**. The triples closure is exactly `F`, even under a hypothetical iterated convention.

For pairs, the broad one-round reading can add mixed three-clauses, but each has two positive literals and is not critical. Under the exact-width parent reading, positive pairs are not parents. Thus actual one-round `TwoCC` is empty in pairs as well. A hypothetical iterative closure is not Definition 31 and can make the pairs variant fail; this is why triples remains the primary carrier.

### 8.6 H5: forced critical-clause choice and statistics

In triples, `F~=F`. The only clause with exactly one positive literal `x` is `C_x`; all auxiliaries have three positive literals. Every variable therefore has exactly one critical clause, `TwoCC=empty`, and no canonical-selection freedom. Combining this with the degree calculation gives exactly

```text
(i_0,i_1,tau) = (0,m/n,0).
```

The same critical-clause conclusion holds for pairs under the actual one-round definition.

### 8.7 Theorem-level finding

The repaired theorem is valid with the explicit uniform threshold

```text
n_0 = 403.
```

The Cycle-7 candidate proof does not currently contain the complete proof just given: it leaves `m=0` undefined, gives only a vague/computational `d` argument, and does not prove uniform girth for non-`Theta(n)` values of `m`. Its unused constant `c>0` should also be removed. These are required proof repairs, not counterexamples to the repaired theorem.

## 9. Fresh finite engine

The engine was implemented before either prohibited Cycle-7 file was opened. Its combinatorial decisions use integers/exact sets. Stored JSON decimals are parsed as exact rationals and compared with the independently counted statistics using an exact rational tolerance.

The predeclared fresh suite found:

* **71,520 parameter cases**, every `10<=n<=1200` and `1<=m<=floor(n/10)`: maximum `d=6`; no missing `d` for `n>=28`;
* **2,936 constructible structural cases**, all `m` for `26<=n<=220` plus six density regimes every 25 variables through `n=2000`: zero property failures;
* **15 full closure cases** through `n=127`: zero triples resolvents under both one-round readings and at either tested fixpoint; pairs `TwoCC` empty under both actual one-round readings;
* after opening the stored certificate, an independent **21/21** reproduction of formula syntax, unique satisfiability, degree statistics, closure, critical clauses, `TwoCC`, and `(i_0,i_1,tau)`.

The search beyond stored instances also records the smallest small-parameter failures rather than hiding them:

* smallest raw-property failure: `(n,m)=(3,0)`, outside the asymptotic theorem;
* smallest nonzero parameter-recipe failure: `(10,1)`;
* in the formerly advertised range starting at 26: the sole recipe failure is `(27,2)`;
* there is no recipe failure for `n>=28` in the finite scan and no mathematical failure for `n>=403` by the separate proof.

Finite evidence is not used to justify the asymptotic quantifier.

## 10. The critical limit point and CR-1

For every fixed real `t in [0,1/10]`, set

```text
m_n = floor(t n).
```

For every `n>=403`, `0<=m_n<=floor(n/10)`, including the upper endpoint. At `t=0`, use the separate `m=0` branch. The repaired theorem gives a formula at every sufficiently large integer `n`, and

```text
m_n/n -> t.
```

In particular, the certified `i_1*` lies strictly below `1/10`, so

```text
m_n=floor(i_1* n)
```

is admissible at every sufficiently large size and realizes vectors converging to `(0,i_1*,0)`. This proves

```text
(0,i_1*,0) in closure(R),
```

where `R` is the genuinely finite-instance-realizable statistic set. A finite realization at `0.06` is irrelevant to this proof.

The strongest interval proved is exactly the claimed closed segment

```text
{(0,t,0): 0<=t<=1/10} subset closure(R).
```

Both endpoints and the all-sufficiently-large-`n` quantifier are covered. CR-1 is therefore sound with the construction/proof repairs above.

## 11. Corollary CR-2 and the old-statistic no-go

### 11.1 Literal point-exclusion claim is false

Cycle 7 says that no valid constraint “linear or not” can exclude the exact corner. That is false without a closedness/regularity condition.

The exact second coordinate is transcendental. Indeed, with exact rational `epsilon_I`,

```text
b_1 = r_0-c log(1-epsilon_I)
```

for rational `r_0` and nonzero rational `c`. If `log(1-epsilon_I)` were nonzero algebraic, Hermite--Lindemann would make its exponential transcendental, contradicting the rational value `1-epsilon_I`. Hence `b_1` is transcendental. If `i_1*=(A-P_reg)/(A+b_1)` were algebraic, solving for `b_1` would make it algebraic, a contradiction.

Every statistic vector from a finite formula has rational coordinates. Therefore the discontinuous predicate

```text
Q(x)= 1  if x is in Q^3,
     -1  otherwise
```

is valid on every finite instance but excludes `x*`. Likewise, with unrestricted real constants, the nonclosed semialgebraic set `D \ {x*}` contains every finite realized point but omits `x*`.

So the sentence “no constraint -- linear or not -- can exclude the corner” is not salvageable for arbitrary predicates.

### 11.2 Strongest correct theorem

Let `D` be the old-statistic ambient domain, `R` the finite realized set, and `f=max(L_R,L_I)` the fixed continuous repaired objective. From LP uniqueness and CR-1,

```text
x* in closure(R),
min_D f = f(x*) = gamma*.
```

For **any** additional constraint whose feasible set `C` is valid on every finite instance, `R subset C`. Hence

```text
inf_{x in C cap D} f(x) = gamma*.
```

The lower bound follows from global optimality on `D`; the upper bound follows from a realized sequence approaching `x*`. No regularity is needed for this infimum statement.

Point retention is more restrictive:

| Constraint class | Must contain `x*`? | Can raise the fixed objective's infimum? |
|---|---:|---:|
| continuous inequality `Q>=0` valid on `R` | yes | no |
| arbitrary closed feasible set | yes | no |
| non-strict linear inequalities | yes | no |
| basic closed semialgebraic system (non-strict polynomial inequalities) | yes | no |
| general semialgebraic set with strict inequalities/Boolean complement and real constants | not necessarily | no |
| arbitrary discontinuous predicate | not necessarily | no |
| uniformly valid size-dependent constraints for all sufficiently large instances | point language may be inapplicable | no positive asymptotic gap, because CR supplies a realizing sequence at every large size |

For approximate asymptotic inequalities, continuity or a closed outer-limit condition is needed to pass the inequality itself to `x*`. If the actual CR points remain feasible, however, they still preclude a fixed positive gap in the old continuous objective.

Thus CR-2 is false as a literal optimizer-retention theorem but sound, and actually maximally general, as an **infimum no-go for feasibility restrictions**.

### 11.3 Claims A--E separated

| Claim | Audit result |
|---|---|
| A. The abstract repaired JC LP has the stated unique corner optimum. | **PROVED** by the weighted affine/dual argument. |
| B. The corner is in the closure of instance-realizable old statistics. | **PROVED WITH CR REPAIRS**, at every sufficiently large size. |
| C. The imported estimates are loose on CR instances. | **NOT ESTABLISHED** and unnecessary. Realizability alone says nothing about their instancewise tightness. |
| D. No valid extra old-statistic constraint of the relevant class can remove/improve the corner. | **POINT RETENTION** for closed classes; **INFIMUM NO-GO** for arbitrary valid classes. |
| E. No improvement whatsoever is possible without new statistics. | **FALSE IF READ LITERALLY.** A stronger estimate may still depend only on the same coordinates. |

The exact surviving old-statistic theorem is:

> Feasibility information in `(i_0,i_1,tau)` alone cannot increase the infimum of the fixed repaired two-affine recombination objective. A further improvement must strengthen or add estimates (possibly still using these coordinates), or introduce additional structural/algorithmic information or statistics.

This preserves Cycle 7's final “new estimates **or** new statistics/information” strategy, while ruling out its stronger informal claims about all point-excluding predicates, source-estimate looseness, and global optimality over every possible same-coordinate analysis.

## 12. Novelty and prior-art audit

The novelty search was performed only after the mathematics above survived. It covered arXiv, ECCC, DROPS/CCC, FOCS, TheoretiCS, and exact-title/exact-number web searches using combinations of:

```text
PPSZ realizability critical clause graph indegree TwoCC
PPSZ structural LP coordinates / optimality / recombination
PPSZ prescribed indegree distribution
PPSZ TwoCC empty
0.060043244708778
1.307031578
```

The search recovered the known PPSZ line: Scheder's critical-clause graph/`TwoCC` analysis, Jiang--Cai's recombination, Hertli's critical-clause methods, Scheder--Steinberger lifting, and adjacent PPSZ hard-instance constructions. It did not locate an earlier source for prescribed realization of the exact `(i_0,i_1,tau)` coordinates, a uniquely satisfiable construction with forced selection and `TwoCC=empty` covering this segment, or the resulting fixed-objective realizability no-go.

| Topic | Classification |
|---|---|
| Scheder statistics, JC affine recombination, and SS lifting | **KNOWN** |
| adversarial/hard-instance constructions for PPSZ in other senses | **KNOWN**, but not prior art for CR as stated |
| exact CR pairs/triples construction and closed-segment realizability | **POTENTIALLY-NOVEL** |
| fixed-objective old-statistic infimum no-go derived from CR | **POTENTIALLY-NOVEL** |
| exact ECCC errata and the Section-7.7 repair | **UNCLEAR**; no prior correction located, but negative search is insufficient |

This is a negative-search result, not a novelty proof. No stronger novelty label is warranted.

## 13. Strategic consequence

After all repairs, the defensible strategic conclusion is exactly:

```text
To improve the 1.307031578 frontier within this line, one must either

1. derive a stronger estimate, which may still depend on the existing
   (i_0,i_1,tau) coordinates; or
2. introduce additional structural statistics or algorithmic information.
```

The audit does not search for either improvement. A mere new feasibility constraint on the old three coordinates cannot improve the fixed recombination infimum; a genuinely stronger same-coordinate estimate remains logically possible.

## 14. Integration and status audit

### 14.1 Status corrections

| Cycle-7 item | Surviving status |
|---|---|
| JC new exact arithmetic and frontier | independently certified |
| Scheder/JC import chain | sound only with the fixed-point epsilon, threshold, `TwoCC`, Section-7.7, and order-of-limits repairs |
| historical `1/15218` | false exact display; repaired rounded historical conclusion survives |
| original JC LP/dual | algebraically sound; repaired source `tau` coefficient still has positive slack |
| Theorem CR | proof candidate sound with explicit repairs; not “all repairs applied” in the current candidate file |
| finite CR evidence | fresh 21/21 reproduction plus broader failure search; not an asymptotic proof |
| CR-1 | sound with repairs, closed interval `[0,1/10]` |
| CR-2 point-exclusion wording | false for arbitrary nonclosed/discontinuous constraints |
| fixed-objective old-statistic value no-go | sound in infimum form |
| “estimates are simply very loose on CR” | unsupported |
| “improvement needs new estimates or new information/statistics” | sound |
| novelty | potentially novel only |

### 14.2 Exact candidate files and changes required

No file listed here was modified during this audit. A future corrected Cycle-7 candidate should make these exact changes:

1. **`research_cycle_07/corner_realizability.md`**
   * change the title/intro from exact-corner “realizable” to **closure-realizable**; finite vectors are rational while `i_1*` is transcendental;
   * remove the unused theorem constant `c>0`;
   * add the separate `m_1=0` definition `P=S=Q=empty`, `g(x)=x+base`;
   * replace the current delta paragraph/scanning evidence by the cyclic Beatty-block proof, explicitly yielding `d<=6` for every allowed `m`;
   * replace the nonuniform girth prose by the winding-number proof and a safe `n_0=403`;
   * replace Corollary CR-2's “no constraint, linear or not, can exclude the corner” by the closed-set point theorem plus arbitrary-set infimum theorem;
   * qualify “exactly optimal” as the fixed repaired two-affine objective's **infimum** under old-statistic feasibility restrictions;
   * remove or separately prove the assertion that the imported estimates are “simply very loose” on these formulas.
2. **`research_cycle_07/lp_reconstruction.md`**
   * add the certified Section-7.7 replacement `0.05529 epsilon_R+0.001 epsilon_R^2`, `S_rep`, and repaired positive `tau` slack;
   * distinguish exact fixed-objective optimality from global optimality over other estimates/parameters.
3. **`results/research_cycle_07.md`**
   * make the same closure-versus-exact-realization and minimum-versus-infimum repairs in the executive summary and Stage-I conclusion;
   * qualify “not a cleverer recombination” to mean no new feasibility restriction/reweighting of the two fixed affine bounds;
   * upgrade Section 7.7 from an unreconciled non-certifying concern to the certified erratum/repair;
   * correct `.2404721` to `.240474134270283...`;
   * retain the source-supported slowly-growing-`w(n)` theorem rather than a literal fixed-`w` claim.
4. **`RESEARCH_STATE.md`**
   * replace “corner is REALIZABLE” by “corner lies in the closure of finite realizable statistics”;
   * replace unrestricted point-exclusion/exact-optimality language by the fixed-objective infimum result;
   * stop saying all CR asymptotic repairs are already applied until the `m=0`, delta, and all-`m` girth proofs are inserted;
   * preserve the correctly stated “new estimates or new statistics” strategic alternative.
5. **`failure_knowledge.jsonl`**
   * repair `RC7-O18-01`: finite grid points are exact, the irrational optimizer is only a limit; arbitrary valid constraints may exclude it but cannot raise the fixed objective's infimum; stronger same-coordinate estimates remain open;
   * update `RC7-JC-01` with the certified Section-7.7 errors/repair and corrected Section-8.3 sum.
6. **`audits/cycle07_corner_theorem_review.md`**
   * supersede the claim that CR-2 is “airtight” as written;
   * add the missing `m=0`, uniform Beatty, and uniform girth proofs, and distinguish finite review evidence from the all-`n` theorem.
7. **`audits/cycle07_final_adversarial.md`** and **`audits/cycle07_final_adversarial_disposition.md`**
   * revise the overclaim/no-go PASS disposition using the topology/infimum distinction;
   * incorporate the certified Section-7.7 repair;
   * label the CR engine's documented `c00ae...` SHA as the LF-normalized hash, not the CRLF working-tree byte hash.
8. **`audits/cycle07_jc_validation.md`**, **`research_cycle_07/scheder_import_ledger.md`**, and **`research_cycle_07/stageV_log.md`**
   * replace the Section-7.7 “unreconciled” item by the exact enclosures and repaired `tau` coefficient/slack;
   * correct the Section-8.3 sum;
   * retain the epsilon/Thr/range/Definition-31/fixed-`w` qualifications.
9. **`research_cycle_07/novelty_frontier_audit.md`**
   * if CR/CR-2 novelty is integrated, use at most `POTENTIALLY-NOVEL` and state the corrected infimum theorem, not unrestricted point retention.

`research_cycle_07/stage1_semantics.md` already uses the operative Definition-31 closure convention and needs no semantic change. Frozen primary-source bytes and the stored failure artifacts must remain preserved.

### 14.3 Provenance and hash consistency

The Cycle-7 raw source manifest matches the fresh external bytes. The authors' four raw Git blobs match their immutable blob hashes. The stored CR certificate hash is

```text
1af8aff15117d948285bf32e82a87a8574195ea5c3266aeb4c1ccb42acac28cd.
```

The CR transcript hash `eac85d35581b697f625c6454aec7eb397b56732011b1ab02c62f82d19c93017b` matches. The current Windows working-tree bytes of `experiments/cycle07_corner_family.py` hash to `7e8752b1...d0c5b5`; normalizing CRLF to LF yields the documented `c00ae723...f8c55`. This is a line-ending provenance issue, not a mathematical/content mismatch, but the manifest wording should say which byte convention it hashes.

No missing transcript, changed source, or unexplained numerical discrepancy was found. The independent tools intentionally do not mimic Cycle 7's heterogeneous check count.

## 15. Reproduction artifacts

From the repository root:

```text
python -B audits/independent_validation/sol_cycle07/jc/jc_exact_validator.py
python -B audits/independent_validation/sol_cycle07/jc/scheder_source_validator.py
python -B audits/independent_validation/sol_cycle07/lp/verify_lp.py
python -B audits/independent_validation/sol_cycle07/cr/cr_cleanroom_validator.py fresh-suite
python -B audits/independent_validation/sol_cycle07/cr/cr_cleanroom_validator.py stored-suite certificates/cycle07_corner/instances.json
```

The committed JSON outputs freeze the two CR suite runs. The JC tools print their complete exact remainder/sign ledgers directly.

Final artifact hashes are recorded in the next subsection after the final clean rerun. No candidate theorem/proof file is part of this audit commit.

### 15.1 Independent-tool hashes

| Relative path below `audits/independent_validation/sol_cycle07/` | SHA-256 |
|---|---|
| `cr/clean_room_derivation.md` | `a2a01a73b56744e8859bce0aa4911a3fdf87f7ab2c501429952c3b8e05535629` |
| `cr/cr_cleanroom_validator.py` | `65be2c49fe712d5c8030e538eb01a3b17b5626c87283ea670e12e704f776ffcb` |
| `cr/fresh_suite_output.json` | `06dcb112ed6ef72d8aef9fe1fc5abb4b61acad44d62ba6f6acdec17ebbbab6f7` |
| `cr/stored_21_comparison.json` | `f7f04d93cb3b7e3b42adda31508de323c611abf68a04ff2ef9e33945998292e7` |
| `jc/CHECKER_DESIGN.md` | `a7f92cc2d0a1cb3e4fe71f92d4d362b5071f269a89931582444be675cefba7ad` |
| `jc/jc_exact_validator.py` | `7144e0e0570d6e2dcf8e964a941f7d180f1c2f264faf8a66181cfebd74253e50` |
| `jc/scheder_source_validator.py` | `2efb126799c7b02eafbc22b539cabd309ef14880f60e43fb5b3eabbc2b55a802` |
| `jc/SOURCE_ERRATA_LEDGER.md` | `2c693a4c5d5c156ba62968b4a089bd3349a3f7717c09d4e079daf77e598f3087` |
| `jc/VERDICT_MEMO.md` | `87853f74343f44b408feca3f904f19db045633127563a2f449aa07168c5fb1b1` |
| `lp/README.md` | `1163dfa2459380ebf954afbde9b4b5f055fe138a07e90c03cad7ad7411241776` |
| `lp/verify_lp.py` | `0474f7a5a536bf70780c804a2b29c3fbd2c23d24e3c35ad8d243568b7b2aeb07` |

All five reproduction commands exited 0 in the final rerun. The fresh suite's embedded implementation hash equals the current validator hash, and the stored comparison reports `pass_count=21` of `instance_count=21`.

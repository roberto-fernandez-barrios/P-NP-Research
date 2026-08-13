# Independent cross-validation of first-cycle targets

**Audit date:** 2026-08-13
**Validator:** circuit-complexity/barriers track, independent of the proposers of the
proof-complexity and meta-complexity lists
**Files reviewed:** `literature/drafts/proof_sat.md`; the ranked top-three candidate summary
supplied directly by the meta-complexity validator while
`literature/drafts/meta_magnification.md` was still being finalized; and the primary sources
linked below. The completed meta-complexity draft was not yet present at close, so this audit does
not imply that the entire eventual file was reviewed.
**Search cutoff:** public literature and ECCC/arXiv records visible on 2026-08-13.

This is an adversarial status audit, not a novelty claim. I tried to make each selected target go
away by finding a theorem that proves it, a stronger theorem that subsumes it, a routine parameter
substitution, or a defect that makes it non-propositional. Failure to find a result is not by itself
proof of openness; confidence levels below reflect that limitation.

## Executive verdict

The two strongest candidates outside the circuit/barriers dossier are:

1. **PC-CP2:** improve the inequality-space lower bound for bounded-coefficient Cutting Planes
   `CP_2` refutations of the complete tree contradiction `CT_n` beyond
   `Omega(log log log n)`.
2. **META-BP:** prove an `Omega(N^2/polylog N)` deterministic unrestricted branching-program
   lower bound for total MCSP, preferably `Omega(N^2/log^2 N)`, improving
   `N^2/2^{O(sqrt(log N))}`.

Both survive the known-result search, with the qualifications below. `PC-CP2` is **OPEN** with
medium-high confidence, but the proposed “infinite subsequence” milestone does not imply the
stated little-omega target and `CT_n` is exponentially large in its variable parameter. `META-BP`
is **OPEN** with medium confidence, but must be stated for a fixed MCSP convention and a fixed
polylogarithmic exponent; the exact quadratic-over-log-squared theorem for MKTP does not transfer
to MCSP.

After comparing them with polynomial-size 1-balanced-chain existence, I still recommend exactly
one first target:

> **For every even `n`, construct a 1-balanced-chain set system on `[n]` of size at most `n^C`
> for one absolute constant `C`.**

This means the general existence theorem, not merely repairing the withdrawn TR26-043 proof.

## Why these two competitors were selected

`proof_sat.md` ranks `PC-CP2` and strict effective simulation of Resolution by regular Resolution
joint first. The former wins this cross-track comparison because it is a fixed proof system, fixed
formula family, and quantitative next bound with finite instances. Buss--Yolcu's strict-simulation
question is also explicitly open, but quantifies over a formula transformation and all Resolution
proof complexities; finite tests can falsify a proposed transformation, not the existential target.
The latter is therefore less suitable for the first repository attack even though its literature
status is clean. The primary paper itself asks whether the proof-size/height parameter can be
removed: [Buss--Yolcu, *Regular Resolution Effectively Simulates Resolution*, Question 3.2 and
Remark 1.2](https://emreyolcu.com/research/regular-effectively-general.pdf).

The meta-complexity list's MCSP branching-program target is its cleanest stable incremental
statement. Its generic-uniformization proposal still needs its quantifiers and enumerability
hypotheses fixed, while transferring the known one-tape lower bound into the small-threshold
hardness-magnification regime would come perilously close to obtaining the magnified major
separation itself. Those are poor first-cycle choices under the mission's “smallest unresolved
statement” rule.

## Audit A: bounded-coefficient Cutting Planes space

### A.1 Exact target and model

For each assignment `alpha in {0,1}^n`, `CT_n` contains the unique width-`n` clause falsified by
`alpha`; hence it has `n` variables and `2^n` clauses. A Cutting Planes line is an integer linear
inequality. The version in the source permits axiom download, deletion, positive-integer linear
combination of any number of simultaneously present premises, and division with rounding. A
configuration is the set of inequalities currently on the blackboard, and **inequality space** is
the maximum number of inequalities in any configuration. `CP_k` restricts every left-hand-side
coefficient in every line to absolute value at most the fixed constant `k`. These conventions
matter: binary addition rules and total/variable space are different measures.

The proposed target can be made precise as

```text
Sp_CP2(CT_n) = omega(log^(3) n) as n -> infinity,
```

where `log^(3) n = log log log n`. If the engine wants a conventional `Omega` theorem rather
than a little-omega class of improvements, it should freeze one first increment, for example
`Omega(log^(3) n * log^(4) n)` or `Omega((log^(3) n)^2)`.

### A.2 What is actually known

Galesi, Pudlak, and Thapen prove the stronger parameterized statement: if `CT_n` has a CP
refutation in inequality space `c`, and every line uses at most `b` distinct coefficients, then

```text
b^c >= sqrt(log log n).
```

For `CP_2`, the possible left coefficients lie in `{-2,-1,0,1,2}`, so `b <= 5`, yielding
`c = Omega(log log log n)`. Their Theorem 17 states the same asymptotic conclusion for every
fixed `CP_k`. The proof maps a configuration to the assignments falsifying it, observes that a
space-`c`, `b`-coefficient configuration is `b^c`-symmetric, and counts the possible cardinalities
of symmetric slices. See [Galesi--Pudlak--Thapen, primary author PDF, Theorems 16--17 and
Problem 3](https://users.math.cas.cz/~thapen/CP_constant_space.pdf) and the
[CCC 2015 proceedings version](https://drops.dagstuhl.de/storage/00lipics/lipics-vol033-ccc2015/LIPIcs.CCC.2015.433/LIPIcs.CCC.2015.433.pdf).

The same paper proves two nearby facts that must not be conflated with this target:

* unrestricted CP has inequality-space `5` refutations of every unsatisfiable set of inequalities,
  but that construction uses coefficients as large as exponential in `n` and is not a `CP_2`
  upper bound;
* pigeonhole-principle formulas have polynomial-size, inequality-space `5` `CP_2` refutations,
  but that says nothing about `CT_n`.

The authors explicitly list “prove a better space lower bound for `CP_2`” as Problem 3. That is
primary-source evidence that the gap existed in 2015, not by itself evidence that it survived to
2026.

### A.3 Attempt to make the target known or stale

I searched the exact formula name, `CP_2`/`CP2`, bounded coefficients, inequality/formula space,
and the open-problem wording, including ECCC and 2024--2026 variants. I also checked the nearby
recent Cutting Planes literature returned by those searches.

No later primary source located in this audit improves the **pure inequality-space** bound for
`CP_2` on `CT_n`. The nearby results do not subsume it:

* modern CP results for concise pigeonhole principles prove size lower bounds, tree-like lower
  bounds, or joint length--space tradeoffs, not a larger unconditional pure-space lower bound for
  this family; for example, [Beame--Whitmeyer, ECCC TR25-057](https://eccc.weizmann.ac.il/report/2025/057/)
  concerns size of Cutting Planes proofs of bit pigeonhole formulas;
* Stabbing Planes and branch-and-cut results use a different proof system;
* the padding corollary in the original paper produces a linear-size family with superconstant
  `CP_k` space, but it does not strengthen the numerical `CT_n` lower bound.

I also looked for a bounded-coefficient upper bound small enough to refute the target and found
none. The only constant-space construction in the source crucially leaves `CP_2`.

**Status: OPEN (medium-high confidence in the audited public literature).** This classification
rests on an explicit original open problem plus a fresh exact/variant search, but it cannot exclude
an unpublished result or a paper using unanticipated terminology.

### A.4 Formulation and value defects found

The underlying open problem is genuine, but the draft's first increment needs two corrections.

1. A lower bound larger than `log^(3) n` on an explicit infinite subsequence does **not** prove
   `Sp_CP2(CT_n) = omega(log^(3) n)`; little omega requires the ratio to diverge for all
   sufficiently large `n`. A subsequence result must be labeled as a weaker diagnostic theorem.
2. `CT_n` is unusual: it has `2^n` clauses. In terms of the formula's explicit length `M`, the
   present bound is only on the order of `log^(4) M` (up to encoding conventions). The source
   itself flags the exponential size and says a more natural example would be desirable. The
   padding trick preserves only a correspondingly tiny superconstant lower bound.

The proposed computation is therefore less decisive than its score suggests. Enumerating
coefficient-normalized inequalities or their Boolean truth sets can expose false invariants for
very small `n`, but the family already contains all `2^n` assignment clauses and the asymptotic
distinction between successive iterated logarithms is invisible at feasible sizes. Formalizing a
specific invariant is realistic; brute-force data alone cannot validate the asymptotic target.

**Independent target-quality verdict:** a valid and attractively small proof-complexity target,
but not the best repository-wide first move. Its connection to stronger lower bounds is indirect,
its family is artificial, and its proposed falsifiability was overstated.

## Audit B: near-quadratic branching-program lower bounds for MCSP

### B.1 Exact target and necessary convention

Let `N = 2^n` be the length of the truth table of `f:{0,1}^n->{0,1}`. In total MCSP the input is
`(tt(f), theta)` and the answer is whether `f` has a Boolean circuit of size at most `theta`.
The target is a lower bound for deterministic unrestricted Boolean branching programs computing
this total language, with size measured by the number of program nodes:

```text
BPsize(MCSP_N) = Omega(N^2 / log^C N)
```

for one explicitly fixed absolute constant `C`, ideally `C=2`. Saying only
`Omega(N^2/polylog N)` leaves whether `C` is fixed, uniform across input lengths, and part of the
claim implicit. The threshold encoding and whether the result is for the full `(tt,theta)` language
or a fixed-threshold slice must also be frozen before proof work.

### B.2 What is actually known

Cheraghchi, Kabanets, Lu, and Myrisiotis prove that every arbitrary-basis formula or general
branching program computing MCSP on truth tables of length `N` has size

```text
N^2 / 2^{O(sqrt(log N))}.
```

Their engine is a strongly local PRG. Lemma 24 gives local complexity
`s^(1/2) 2^{O(sqrt(log s))}` against size-`s` formulas/general branching programs, and Theorem 13
turns that locality into the MCSP lower bound. See [Cheraghchi--Kabanets--Lu--Myrisiotis,
ICALP 2019, Theorem 2, Theorem 13, and Lemma 24](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.39/LIPIcs.ICALP.2019.39.pdf)
and the [ECCC full-version record TR19-022](https://eccc.weizmann.ac.il/report/2019/022/).

The proposed denominator is genuinely smaller: `2^{Theta(sqrt(log N))}` grows faster than every
polylogarithm. Thus the target is not a restatement of `N^{2-o(1)}`.

### B.3 The closest apparent settlement is for the wrong problem

Cheraghchi, Hirahara, Myrisiotis, and Yoshida later prove

```text
BPsize(MKTP_N) = Omega(N^2/log^2 N).
```

This is Theorem 4 of their STACS 2021 paper. It is exactly the desired numerical bound but for
**MKTP**, defined using time-bounded Kolmogorov complexity, not MCSP. The same paper explicitly
explains why this does not transfer: although circuit complexity and `KT` complexity are
polynomially related, that relationship is not tight enough for their Neciporuk argument, and they
“fail to apply” the method to MCSP. This is direct negative evidence against treating the target
as routine. See [Cheraghchi--Hirahara--Myrisiotis--Yoshida, Theorem 4 and the discussion following
it](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf).

### B.4 Attempt to make the target known or stale

I searched exact theorem strings, `MCSP` with general/deterministic branching programs, quadratic
and almost-quadratic denominators, author follow-ups, and ECCC/arXiv records from 2024 through
August 2026. The strongest nearby later results change at least one essential axis:

* the STACS 2021 exact `Omega(N^2/log^2 N)` result is for MKTP;
* its MCSP results for nondeterministic, co-nondeterministic, and parity branching programs give
  `N^{1.5-o(1)}`, a different model and exponent;
* Glinskih--Riazanov obtain superpolynomial lower bounds for **read-once nondeterministic**
  branching programs computing total minimization problems. Read-once nondeterminism and
  unrestricted deterministic branching programs are not interchangeable. Their 2025 paper also
  studies partial minimum *branching-program* size and ETH-hardness, not a quadratic lower bound
  for total MCSP in the target model: [ITCS 2025 primary proceedings paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol325-itcs2025/LIPIcs.ITCS.2025.54/LIPIcs.ITCS.2025.54.pdf);
* 2026 PRG/lower-bound papers found in the search concern permutation or read-once parity
  branching programs, not unrestricted programs computing MCSP.

None supplies a restriction, reduction, or simulation that implies the proposed total-MCSP
bound. In particular, the numerical strength of a theorem for a less powerful or incomparable
branching-program model cannot be imported into the unrestricted deterministic model.

**Status: OPEN (medium confidence in the audited public literature).** The confidence is lower
than for `PC-CP2` because no source located here states this exact sharpening as a numbered open
problem, and “general branching program” literature is broad. The primary results and their
explicit MCSP/MKTP non-transfer make the classification substantially stronger than an
absence-only guess.

### B.5 Difficulty and connection defects found

This target is close to the best known lower bound for *any* explicit Boolean function in general
branching programs. The STACS paper describes `Omega(N^2/log^2 N)` as matching that frontier up
to constants. Consequently this is not merely a harmless cleanup of a denominator: it asks MCSP
to attain the general-model frontier.

Within the 2019 proof route, the subpolynomial loss comes from the locality of the branching-
program PRG. Replacing it by polylogarithmic loss would require a substantially sharper local PRG
or an alternative lower-bound mechanism. That is reusable and significant, but makes the target
less tractable than the first-cycle score should assume.

Finally, this exact-total-MCSP target is adjacent to hardness magnification, not itself a stated
magnification premise. Known magnification theorems use carefully parameterized or gap variants.
One must not report this lower bound, if proved, as implying `P != NP` without a separate theorem
whose hypotheses match the exact MCSP slice and branching-program model.

**Independent target-quality verdict:** clean and meaningful after conventions are fixed, with a
potentially valuable PRG payoff, but too near the general branching-program frontier for the first
attack.

## Repository-wide comparison

The following is an independent qualitative re-ranking, not a replacement for the track tables.

| Criterion | Polynomial 1-balanced-chain existence | `PC-CP2` improvement | `META-BP` improvement |
|---|---|---|---|
| Best known | `n^{O(log n/log log n)}` upper; `Omega(n^2)` lower | `Omega(log^(3) n)` | `N^2/2^{O(sqrt(log N))}` |
| Evidence gap is open | 2026 predecessor theorem plus withdrawn exact claim and referee-identified fatal dependency | Explicit 2015 open problem plus fresh no-closure search | Primary state of art, explicit MKTP non-transfer, fresh no-closure search |
| Smallest meaningful increment | Any fixed polynomial construction | Any global unbounded factor, but must repair formulation | Replace a superpolylog loss by a fixed polylog loss |
| Finite falsification | Exact `N(n)`/set-cover/SAT instances; attack proposed construction classes | Tiny proof-search instances can kill invariants, but iterated logs are empirically invisible | Tiny MCSP/BP synthesis is possible but says little about a near-frontier asymptotic bound |
| Formalization | Finite set systems, chains, discrepancy; probability only if a stochastic construction is used | Finite inequalities/configurations are feasible; asymptotic counting is moderate | PRG/extractor and branching-program analysis is a much larger library burden |
| Reusable payoff | Discrepancy/random-walk constructions and an algebraic lower-bound-method barrier | Bounded-coefficient proof-space invariant | Stronger local PRG or new general-BP lower-bound technique |
| Principal risk | The polynomial statement may be false; the withdrawn adaptive-drift route may be irreparable | Artificial exponential-size family; weak connection outward | Near-best-possible general-model bound; MCSP convention and magnification overclaim risks |

### Why the balanced-chain target remains first

Fabris, Limaye, Srinivasan, and Yehudayoff define `N(n)`, the minimum size of a
1-balanced-chain set system, and prove

```text
Omega(n^2) <= N(n) <= n^{O(log n/log log n)}.
```

They connect such systems to the power of min-partition rank for multilinear algebraic branching
programs. See [FLSY, ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/) and the
[primary PDF](https://eccc.weizmann.ac.il/report/2026/001/download/).

TR26-043 claimed `N(n)=n^{O(1)}`, but the claim is withdrawn. The current ECCC record states
that Lemma 4.1 bounds a forced probability only unconditionally, not conditional on the
filtration needed by the supermartingale, and that all results rely on that lemma. The arXiv record
is likewise withdrawn. See the [official ECCC revision/gap notice](https://eccc.weizmann.ac.il/report/2026/043/)
and [arXiv:2604.00746](https://arxiv.org/abs/2604.00746). Searches recorded in
`literature/drafts/circuits_barriers.md` found no repaired or independent polynomial construction.
Thus polynomial existence remains **OPEN**, not `UNKNOWN-STATUS` and not known via the withdrawn
paper.

Relative to the two validated competitors, this target has the best combination required by the
mission:

* the exact failed claim is fresh and the reason it is not known is documented by a referee notice;
* there is a proved quasipolynomial construction to dissect, rather than only a distant lower-bound
  frontier;
* small instances are genuine finite covering problems and can falsify structural conjectures;
* both constructive and negative work can expose reusable discrepancy/random-walk ideas;
* the definitions and a deterministic construction, if found, are comparatively formalization
  friendly.

The failure mode must remain explicit. A counterexample to the two-block steering process, or a
proof that TR26-043 cannot be repaired, does **not** refute polynomial 1-balanced-chain existence.
It only closes one proposed method. Conversely, a polynomial construction would establish the
associated min-partition-rank barrier; it would not prove an mABP lower bound, a Boolean circuit
lower bound, or `P != NP`.

## Final recommendation

**Select only the general polynomial 1-balanced-chain existence statement as the first research
target.** Keep `PC-CP2` as the strongest proof-complexity backup after repairing its asymptotic
milestone, and keep `META-BP` as a higher-risk PRG/meta-complexity target. Do not begin any of
these proof attacks during Phase 0/1.

## Evidence and uncertainty ledger

* **Known:** `CP_k` requires `Omega(log^(3) n)` inequality space for `CT_n`, for every fixed `k`.
* **Open, medium-high confidence:** a global `omega(log^(3) n)` `CP_2` lower bound for `CT_n`.
* **Formulation defect:** an infinite-subsequence improvement does not prove the preceding
  little-omega statement.
* **Known:** total MCSP requires deterministic general branching-program size
  `N^2/2^{O(sqrt(log N))}`.
* **Known but non-transferring:** MKTP requires deterministic branching-program size
  `Omega(N^2/log^2 N)`; the source explains why its method does not give the MCSP result.
* **Open, medium confidence:** a fixed-`C` `Omega(N^2/log^C N)` bound for total MCSP in the
  exact unrestricted deterministic model.
* **Known:** `Omega(n^2) <= N(n) <= n^{O(log n/log log n)}` for 1-balanced-chain systems.
* **Withdrawn / not a theorem:** TR26-043's claimed polynomial upper bound.
* **Open, high confidence in the audited public record:** `N(n)=n^{O(1)}` in general.
* **Residual uncertainty:** no literature search proves a negative. The two competitor status
  labels should be rechecked immediately before an attack, and the MCSP threshold/input
  convention must be copied verbatim into any conjecture file.

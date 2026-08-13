# Phase 0/1 dossier: meta-complexity, hardness magnification, and pseudorandomness

**Status:** literature reconstruction and target triage only (2026-08-13).  No
claim below is a proof of a new lower bound or of `P != NP`.  Labels are
`KNOWN`, `CONJECTURED`, `OPEN (source-stated)`, or `OPEN/UNKNOWN after search`.

## 1. Scope, conventions, and audit method

The truth table of a Boolean function on `n` variables has length
`N = 2^n`.  This file reserves `n` for the number of function variables and
`N` for truth-table length even when a cited paper calls the truth-table
length `n`.  All logarithms are base two up to immaterial constants.

* `MCSP[s]` is the total language of `N`-bit strings that are truth tables of
  functions computed by fan-in-two Boolean circuits of size at most `s(n)`.
* `Gap-MCSP[s_1,s_2]` has YES instances of circuit size at most `s_1` and NO
  instances of circuit size greater than `s_2`; behavior in the gap is
  unrestricted.
* Approximate MCSP notation is paper-dependent.  Oliveira--Santhanam use
  `(alpha,beta)-MCSP[s]` for a promise separating functions that a size-`s`
  circuit agrees with on at least an `alpha` fraction from those with no such
  circuit agreeing on a `beta` fraction.  Atserias--Muller use
  `epsilon-MCSP[sigma]` for exact small-circuit YES instances versus strings
  at relative Hamming distance at least `epsilon` from every size-`sigma`
  truth table.
* `KT(x)` is the random-access measure `min(|d|+T)`, where program `d`, on
  query `i`, returns `x_i` within `T` steps.  `MKTP` asks whether `KT(x)` is at
  most a threshold.  This is polynomially related to circuit size.
* `Kt(x) = min(|p| + ceil(log t))`, where a program prints all of `x` in `t`
  steps, is Levin's measure; `MKtP` is qualitatively more EXP-like.
* `K^t(x)` below denotes plain Kolmogorov complexity under a fixed polynomial
  time bound `t`; it is neither `KT` nor Levin `Kt`.

I checked theorem statements in the primary paper PDFs linked below, including
model definitions and parameter ranges.  I also searched by exact target
phrases, paper titles, later citing papers, ECCC, arXiv, DROPS, and authors'
pages for results through the search date.  An `OPEN/UNKNOWN after search`
label therefore means that no theorem settling the precise statement was
located; it is not a certified exhaustive novelty claim.

## 2. Ground truth: exact results and dependencies

### 2.1 Original hardness-magnification templates

**Oliveira--Santhanam, FOCS 2018 (`KNOWN`).**  Let `N=2^n`.

1. If `s=n^k`, `delta=n^{-k}`, and the approximate problem
   `(1,1-delta)-MCSP[s]` has no formulas of size `N polylog N`, then some NP
   language has no polynomial-size formulas.  If the lower bound is
   `N^{1+epsilon}`, one obtains an exponential formula lower bound
   `2^{m^{delta'}}` for an NP language.  With `s=2^{o(n)}` and
   `delta=2^{-o(n)}`, an `N^{1+epsilon}` lower bound implies NP has no
   polynomial-size formulas.
2. For every fixed `delta>0`, a lower bound
   `Gap-MKtP[N^epsilon,N^epsilon+5 log N] notin Circuit[N^{1+delta}]`
   implies `EXP notsubset SIZE(poly)` (and consequent error-correcting-code
   constructions).  The hypothesis is about the promise version of **Levin
   `Kt`**, not standard MCSP or random-access `KT`.
3. If `MCSP[2^{sqrt(n)}]` has no `o(N)` zero-error average-case formula--a
   formula may output `?`, never errs, and answers on at least half the uniform
   inputs--then NP has no polynomial-size formulas.
4. For constants `1/2 < beta < alpha <= 1` and `s <= 2^{n^gamma}` with
   `gamma<1`, sufficiently strong sublinear random-access average-case lower
   bounds for `(alpha,beta)-MCSP[s]` imply `NP notsubset BPP`.

The proof technology is a random projection/compression of a hard NP or EXP
language into a meta-complexity instance, plus nonuniform derandomization.
The limitations are material: the problem is approximate or gapped, the
threshold is prescribed, and the model/uniformity in the premise cannot be
silently replaced by a worst-case lower bound for total MCSP.

Primary source: [Oliveira and Santhanam, *Hardness Magnification for Natural Problems*, ECCC TR18-139 / FOCS 2018](https://eccc.weizmann.ac.il/report/2018/139/download).

**Oliveira--Pich--Santhanam, CCC 2019 / ToC 2021 (`KNOWN`).**  Their
Theorem 1.1 gives a universal constant `c`; if, for some `epsilon>0` and all
sufficiently small `beta>0`,

`Gap-MKtP[2^{beta n}, 2^{beta n}+c n]`

requires any of the following, then the corresponding polynomial lower bound
for EXP follows:

| Premise model and truth-table lower bound | Consequence |
|---|---|
| general circuits `N^{1+epsilon}` | `EXP notsubset Circuit[poly]` |
| `U_2` De Morgan Formula-XOR `N^{1+epsilon}` | `EXP notsubset Formula[poly]` |
| AND--THR--THR--XOR `N^{1+epsilon}` | `EXP notsubset TC^0_2[poly]` |
| specified constant-depth majority, exponent `1+2/d_0+epsilon` | matching majority lower bound |
| arbitrary-basis (`B_2`) formulas `N^{2+epsilon}` | `EXP notsubset Formula[poly]` |
| De Morgan (`U_2`) formulas `N^{3+epsilon}` | `EXP notsubset Formula[poly]` |
| deterministic branching programs `N^{2+epsilon}` | `EXP notsubset BP[poly]` |
| depth-six AC0 `N^{1+epsilon}` | `EXP notsubset AC0[6]` |

Here formula size is number of leaves; `B_2` permits an arbitrary binary
Boolean gate, `U_2` uses AND/OR/NOT, and XOR gates occur only at leaves in the
Formula-XOR model.  Their Theorem 1.4 is the important MCSP analogue: for the
same universal `c`, if for some `epsilon>0` and all sufficiently small `beta`,

`Gap-MCSP[2^{beta n}/(c n), 2^{beta n}] notin Circuit[N^{1+epsilon}],`

then `NP notsubset Circuit[poly]`.  It uses constructive anti-checkers and
approximate counting under the contrary assumption `NP subset P/poly`.

The near-threshold unconditional lower bounds in the same paper do **not**
settle these premises.  For example, Theorem 1.2 uses the much wider promise
`Gap-MKtP[2^{(1-delta)n},2^{n-1}]`; Theorems 1.3/1.5 similarly use parameter
ranges that do not match the magnifying gaps.  This parameter mismatch is a
recurring false positive in informal summaries.

Primary source: [Oliveira, Pich, and Santhanam, *Hardness Magnification near State-of-the-Art Lower Bounds*, Theory of Computing 17(11), 2021](https://www.theoryofcomputing.org/articles/v017a011/v017a011.pdf).

### 2.2 Locality, non-naturalization, and search upper bounds

**McKay--Murray--Williams, STOC 2019 (`KNOWN`).**  Relative to an oracle `A`,
Search-MCSP has:

* uniform constant-depth circuits of size `tilde O(N s^2)`, depth
  `O(n/log ell)`, using bounded-fanin `Sigma_3-SAT^A` oracle gates of fan-in
  `tilde O(ell)` when `ell >= s^2`;
* a one-pass streaming algorithm with total time `N tilde O(s)`, update time
  `tilde O(s^2)`, space `tilde O(s)`, and short `Sigma_3-SAT^A` queries.

For `A in PH`, lower bounds excluding analogous `poly(s)`-space/update search
algorithms imply `P != NP`; shallow threshold-circuit lower bounds for
Search-MCSP imply `NP notsubset TC^0`, `NP notsubset NC^1`, or
`NP notsubset P/poly` depending on depth and size.  Exact analogues for MKTP
yield NP consequences, and for MKtP yield EXP consequences.  The technique is
short-query compression plus merging candidate circuits.  It explains why
many local lower-bound arguments automatically relativize to a model that
already computes Search-MCSP: such a method cannot prove the desired premise.

Primary source: [McKay, Murray, and Williams, *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*, STOC 2019](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf).

**Chen--Hirahara--Oliveira--Pich--Rajgopal--Santhanam, ITCS 2020
(`KNOWN`).**  Their barrier framework makes both *localization* and
*naturalization* parameter-sensitive.

* For appropriate constants, the following are equivalent: a slightly
  superlinear lower bound for an approximate/gap MCSP problem, a worst-case
  lower bound for `MCSP[n^c,2^n/n^c]`, failure of subexponential nonadaptive
  membership-query learning for polynomial-size circuits, absence of a
  `Circuit[poly(N)]`-natural property useful against `Circuit[n^d]`, and
  absence of the corresponding nonuniform PRF family.  The exact accuracy and
  infinitary quantifiers matter; it is not a blanket statement that every
  MCSP lower bound breaks natural proofs.
* Their Formula-XOR frontier uses
  `Gap-MCSP[2^{n^{1/3}},2^{n^{2/3}}]`.  An `N^{1.01}` Formula-XOR lower bound
  would imply `NQP notsubset NC^1`.  An ordinary-formula lower bound near
  `N^{1.99}` and an interactive-proof/Formula-XOR lower bound near `N^{1.99}`
  are known, but the combined Formula-XOR statement is not.
* The problem has small Formula--oracle--XOR circuits when oracle gates of
  fan-in `N^epsilon` are placed immediately above parity leaves.  On the other
  hand, interactive proofs retain lower bounds around `N^{2-3 delta}` under
  bounded number/fan-in of oracle gates and, for another gap regime, under
  `o(log N/log log N)` adaptivity.  Thus a proof that fully localizes is ruled
  out, but a nonlocal proof is not.

Primary source: [Chen et al., *Beyond Natural Proofs: Hardness Magnification and Locality*, ITCS 2020](https://drops.dagstuhl.de/storage/00lipics/lipics-vol151-itcs2020/LIPIcs.ITCS.2020.70/LIPIcs.ITCS.2020.70.pdf).

### 2.3 Constructive and uniform lower bounds

**Atserias--Muller, arXiv v2 (June 2025; preprint status) (`KNOWN as a
preprint theorem`).**  Circuits/formulas use fan-in-two NOT/AND/OR gates and
size counts gates.  `P`-uniform means that `1^n -> C_n` is computable in time
polynomial in `n`.

* Their Theorem 8 constructs in polynomial time an explicit binary
  `(n,m,n^{-epsilon},1/8)` distinguisher with `m <= n^7` and maximum column
  weight at most `ceil(2 n^epsilon)`, for every fixed real
  `0<epsilon<=1`.
* Theorem 9: if, for some `epsilon>0`, a `2^{n^{o(1)}}`-sparse `Q in NP`
  satisfies either an `n^{-epsilon}`-approximate formula lower bound
  `n^{1+2epsilon+o(1)}` or the corresponding one-sided probabilistic-formula
  lower bound `n^{2epsilon+o(1)}`, then NP has no polynomial-size formulas.
  In the one-sided model, YES strings are accepted with probability one and
  NO strings with probability at most `1/4`.
* Theorem 10 gives the matching unconditional premise
  `n^{-epsilon}-MCSP[2^{sqrt(ell)}] notin PFML[n^{2epsilon-o(1)}]`.
* Theorem 11: if, for some `epsilon>0` and some
  `sigma(ell) <= 2^{o(ell)}`,
  `n^{-epsilon}-MCSP[sigma]` has no P-uniform circuits of size
  `n^{1+epsilon+o(1)}`, then `P != NP^{oplus P}`.

This is a uniform route around the usual locality obstruction: the
Santhanam--Williams uniform lower-bound argument does not localize in the same
way.  The source explicitly asks for a constructive Santhanam--Williams proof
that exhibits a natural explicit hard problem, and for a general sparse-set
version of the uniform threshold.  The latter requires a precise complexity
restriction: allowing an arbitrary undecidable sparse set would make the
putative implication vacuous/false as a proof template.

Primary source: [Atserias and Muller, *New Frontiers in Hardness Magnification*, arXiv:2503.24061v2](https://arxiv.org/pdf/2503.24061).

### 2.4 Present unconditional lower bounds near candidate thresholds

**Cheraghchi--Kabanets--Lu--Myrisiotis, ICALP 2019 (`KNOWN`).**  For standard
total MCSP on `N` bits they prove:

* De Morgan formula size `N^3 / 2^{O(log^{2/3} N)}`;
* arbitrary-basis formula and deterministic branching-program size
  `N^2 / 2^{O(sqrt(log N))}`;
* depth-`d>2` AC0 size `2^{Omega(N^{1/(d+2+gamma)})}` for every `gamma>0`;
* CNF/DNF size `2^{N/tilde O(log^2 N)}`.

The method constructs a local PRG that fools the lower-bound model while every
seed output is itself the truth table of a small circuit; MCSP distinguishes
the easy outputs from random hard truth tables.  It does not automatically
transfer to the sparse/gapped parameter choices used by magnification.

Primary source: [Cheraghchi et al., *Circuit Lower Bounds for MCSP from Local Pseudorandom Generators*, ICALP 2019](https://drops.dagstuhl.de/storage/00lipics/lipics-vol132-icalp2019/LIPIcs.ICALP.2019.39/LIPIcs.ICALP.2019.39.pdf).

**Cheraghchi--Hirahara--Myrisiotis--Yoshida, STACS 2021 (`KNOWN`).**

* There is a universal small `mu>0` such that proving
  `MCSP[2^{mu n}] notin DTIME_1[N^{1.01}]` separates `P` from `NP`.  Here
  `DTIME_1` is a one-tape-style model with a one-way read-only input tape and a
  two-way work tape.
* For `mu<1` sufficiently close to one, the same problem is unconditionally
  outside two-sided `BPTIME_1[N^{1.99}]`.  More exactly, for every
  `1/2<mu<1`, every oracle `O`, and every `1/2<mu'<mu`, it is outside
  `BPTIME_1^O[N^{2(mu'-o(1))}]` when oracle-query length is `N^{o(1)}`.  This
  also shows why a short-oracle localization argument cannot extend the
  magnification theorem into `mu>1/2` unchanged.
* MKTP has deterministic branching-program lower bound
  `Omega(N^2/log^2 N)` and nondeterministic/parity branching-program lower
  bound `Omega(N^{3/2}/log N)`, optimal for the Nechiporuk method.
* Standard MCSP has nondeterministic, co-nondeterministic, and parity
  branching-program lower bounds `N^{3/2-o(1)}`.  The paper explicitly notes
  that the MKTP Nechiporuk proof does not yield the deterministic MCSP result:
  known polynomial relations between `KT` and circuit size lose too much.

Primary source: [Cheraghchi et al., *One-Tape Lower Bounds and the Complexity of MCSP*, STACS 2021](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf).

**Chen--Jin--Williams, STOC 2020 (`KNOWN`).**  A probabilistic formula is a
finite distribution over De Morgan formulas that computes each input
correctly with probability at least `2/3` (the distribution can be reduced to
support `O(N)`).

* If for some `epsilon>0` and all sufficiently small `alpha`,
  `MCSP[N^alpha]` needs probabilistic formulas `N^{2+epsilon}`, then
  `oplus P notsubset NC^1`; the analogous MKtP statement yields
  `EXP notsubset NC^1`.
* Even an `N^2 (log N)^{f(N)}` lower bound for `MCSP[(log N)^d]`, for any
  unbounded `f`, yields the same parity-P consequence.
* For constants `c,d,K`, with `c log N < t(N) <= N/20` and
  `(log N)^d < s(N) <= N/(200 log N)`, they prove probabilistic-formula lower
  bounds `N^{2-K/log log N}/t(N)` for MKtP and
  `N^{2-K/log log N}/s(N)` for MCSP.  The denominator is outside the exponent.
* For every `alpha in (0,1)` and `epsilon>0`,
  `MCSP[N^alpha]` has no probabilistic formula of size
  `N^{2+alpha-epsilon}`.  This is strong, but it is at a larger threshold and
  does not instantiate the sparse-threshold magnification premise.

The proof combines restrictions, PCPs of proximity, NC1 proof systems, and
sparse kernelization.  A highlighted intermediate obstruction asks for a
polynomial-size list of labels inconsistent with every formula of a target
size; the `N^{2-epsilon}` versus `N^{2+epsilon}` transition is the operative
threshold.

Primary source: [Chen, Jin, and Williams, *Hardness Magnification for all Sparse NP Languages*, ECCC TR20-065 / STOC 2020](https://eccc.weizmann.ac.il/report/2020/065/download).

**Chen--Li--Yang, CCC 2022 (`KNOWN`).**  They construct an almost-universal
hash family with `ell=(log n)^2/log log n`, `Theta(ell)` output bits,
`exp(-Omega(ell))` collision error, seed `O(ell(log n)^2)`, and
`CC^0[2]` circuits using `2n+o(n)` wires; the sampler is polynomial-time and
POLYLOGTIME-uniform.  Consequences include:

* a fixed explicit `O(n)`-sparse P language whose probabilistic circuits need
  at least `2n-2` wires;
* for `N=2^n` and `n <= s(n) <= n^2/log n`, if `MCSP[s]` requires
  probabilistic circuits `2N+O(N/log log N)`, then for some `c>0`,
  `oplus P notsubset SIZE[2^{N^c}]`;
* explicit low-complexity PRFs with `2n+o(n)`-wire circuits under
  subexponentially secure one-way functions, and AC0[2] variants under the
  paper's stated standard assumptions.

The paper explicitly leaves an unconditional `2N-o(N)` deterministic circuit
lower bound for MCSP as a frontier.  This is linear-wire complexity, not gate
complexity, and must not be conflated with the `N^{1+epsilon}` magnification
premises above.

Primary source: [Chen, Li, and Yang, *Hardness Magnification for Small Circuits*, CCC 2022](https://drops.dagstuhl.de/storage/00lipics/lipics-vol234-ccc2022/LIPIcs.CCC.2022.23/LIPIcs.CCC.2022.23.pdf).

### 2.5 Complexity and cryptographic status of the meta-problems

**Total MCSP/MKTP.**  Both are in NP.  Unconditional NP-completeness of the
standard total versions is still not established by the sources found.  MKTP
has zero-sided randomized reductions from Graph Isomorphism and related
isomorphism problems; factoring and discrete logarithm reduce to MCSP/MKTP in
the specified randomized sense, and Statistical Zero Knowledge has
bounded-error oracle reductions.  These reductions use entropy/compression
properties and do not establish ordinary many-one NP-hardness.

Primary source: [Allender et al., *Minimum Circuit Size, Graph Isomorphism, and Related Problems*, arXiv:1710.09806](https://arxiv.org/abs/1710.09806).

The strongest recent standard-total-MCSP hardness located is conditional:
Hirahara--Ilango obtain deterministic quasipolynomial-time nonadaptive NP
hardness of constant-factor MCSP assuming a package of subexponential NIWI,
coNP circuit-lower-bound, and near-Shannon lower-bound hypotheses.  This does
not make the unconditional target known.  Results for Partial MCSP, implicit
variants, or randomized reductions cannot be substituted for total MCSP.

Primary source: [Hirahara and Ilango, *NP-Hardness of Minimum Circuit Size Problem for Constant Depth Circuits*, FOCS 2025 proceedings version](https://www.rahulilango.com/papers/MCSP-Proceedings-2025.pdf).

**Kolmogorov complexity and one-way functions.**

* For every polynomial `t(n) >= (1+epsilon)n`, one-way functions exist iff
  exact `K^t` is mildly hard on average under the uniform distribution: for
  some polynomial `p`, no PPT algorithm succeeds with probability greater
  than `1-1/p`.  This is fixed-time-bounded plain Kolmogorov complexity, not
  `Kt` or `KT`.
  [Liu and Pass, *On One-Way Functions and Kolmogorov Complexity*, FOCS 2020](https://arxiv.org/pdf/2009.11514).
* Uniform average-case hardness of `Kt` characterizes one-way functions in
  the corresponding bounded-error regime; `KT` has a uniform-NC1 one-way
  function characterization.  For MCSP itself, the implications located are
  asymmetric: strong average-case MCSP hardness gives a hard one-way function,
  while a sufficiently hard low-complexity one-way function gives average
  MCSP hardness.
  [Ren and Santhanam, *Hardness of KT Characterizes Parallel Cryptography*, CCC 2021](https://drops.dagstuhl.de/opus/volltexte/2021/14309/pdf/LIPIcs-CCC-2021-35.pdf).
* One-way functions are equivalent to average-case hardness of carefully
  gapped MCSP under an **existential locally samplable distribution**.  In one
  direction, for some `delta>0` and `s=Omega(n^delta)`,
  `Gap-MCSP[s,s n^{5delta}]` is weakly hard under an `n^delta`-locally
  samplable distribution.  In the robust direction, for every `delta>0`
  there is such a distribution making
  `Gap-MCSP[n^delta,o(n/log n)]` strongly hard.  Weak means inverse-polynomial
  failure on almost every length; strong means advantage only
  `1/n^{omega(1)}` over one half.  It is not a uniform-input theorem.
  [Ilango, Ren, and Santhanam, *Robustness of Average-Case Meta-Complexity*, STOC 2022](https://hanlin-ren.github.io/files/pdf/stoc22_robustness.pdf).

These distinctions block a tempting but invalid inference: “OWFs exist, so
standard total MCSP is hard on average under uniform random truth tables.”  A
uniform random truth table is overwhelmingly a NO instance for every
sub-Shannon threshold, so even defining a balanced decision distribution
requires care.

## 3. Dependency graph and barriers

```text
local PRG / restrictions / Nechiporuk / hashing
        |                       |
        v                       v
unconditional weak MCSP LBs   constructive sparse distinguishers
        |                       |
        +------ parameter/model matching ------+
                                                v
  exact magnifying premise (gap, threshold, model, uniformity)
            |                         |
            | locality/naturalness    | uniform SW route
            v                         v
  NP/EXP nonuniform LB          P != NP^{oplus P} or NP formula LB
            |
            v
  PRFs / learning / natural properties (only in stated parameter regimes)
```

The hard step is the horizontal one: present lower bounds and magnification
premises usually refer to different thresholds, promise gaps, approximation
radii, uniformity, or models.  The following negative findings should be
retained:

1. `Omega(N^2/log^2 N)` branching-program complexity is known for **MKTP**,
   not standard MCSP.  Polynomial equivalence of `KT` and circuit size is too
   lossy for the desired MCSP threshold.
2. A lower bound for a wide gap such as
   `[2^{(1-delta)n},2^{n-1}]` does not settle a narrow additive/multiplicative
   gap used by magnification.
3. Search-MCSP has small circuits/streaming algorithms with short SAT-like
   oracle gates.  A proof stable under those gates cannot establish a premise
   whose consequence contradicts that relativized upper bound.
4. Natural-proofs equivalences are tied to approximation and parameter
   quantifiers.  They do not prove that every lower bound on every MCSP
   variant is natural.
5. Formula, Formula-XOR, interactive-proof formula, probabilistic formula,
   deterministic circuit, wire, branching-program, and one-tape lower bounds
   are not interchangeable.
6. Partial-MCSP hardness, implicit-MCSP hardness, conditional hardness, and
   randomized/Turing reductions do not establish unconditional many-one
   NP-completeness of total MCSP.
7. `K^t`, `Kt`, and `KT` are different measures with different completeness,
   magnification, and cryptographic theorems.
8. OWF equivalences using locally samplable distributions do not imply a
   balanced uniform-distribution hardness theorem for MCSP.

## 4. Ranked unresolved intermediate targets

Scores use the mission rubric `(novelty, tractability, centrality,
formalizability, validation clarity)`, each in `[1,5]`; the product ranks the
list.  “Open” is always relative to the explicit source/search audit above.

### M1. Near-quadratic deterministic branching-program lower bound for total MCSP

**Precise target (`OPEN/UNKNOWN after search`):** Prove, for a fixed explicit
sub-Shannon threshold such as `s(n)=n^2` (or a comparably standard
`n^{Theta(1)}` threshold),

`BP(MCSP[s]) = Omega(N^2/polylog N)`;

the clean benchmark is `Omega(N^2/log^2 N)`.

**Nearest known theorems / attempted disproof of openness.**  ICALP 2019 gives
only `N^2/2^{O(sqrt(log N))}` for deterministic BPs.  STACS 2021 gives
`Omega(N^2/log^2 N)` for MKTP and `N^{3/2-o(1)}` for nondeterministic,
co-nondeterministic, and parity BPs for MCSP.  Exact-title, exact-bound, and
citation searches through 2026 found no transfer to deterministic standard
MCSP.  The STACS paper expressly identifies the circuit-size/KT distortion as
the obstruction.  No smaller BP upper bound that would falsify the target was
located.

**Technique/dependencies.**  Refine the local-PRG analysis or replace the
MKTP-specific Nechiporuk subfunction count by a direct count for circuit-size
truth-table slices.  Dependencies are finite circuit enumeration, restriction
stability, and a blockwise subfunction lemma; no magnification theorem is
needed to state or validate it.  A successful technique may later feed the
`N^{2+epsilon}` BP magnification frontier, but this target itself does not
claim a class separation.

**Falsification/experiment.**  For small `n`, enumerate size-`s` circuits and
compute the number of distinct subfunctions induced by balanced blocks; compare
the resulting Nechiporuk sum with MKTP and search for restrictions collapsing
the MCSP slice.  Formalize the finite BP/subfunction lemma before asymptotics.

**Score:** `(4,4,3,5,4)`, product `960`.

### M2. General uniform magnification for explicit sparse problems

**Precise target (`OPEN (source-stated), formulation incomplete`):** Find the
weakest checkable uniformity/enumerability hypothesis `E(Q)` on a
`2^{n^{o(1)}}`-sparse decision problem `Q` under which the Atserias--Muller
Theorem 11 implication remains valid with Q in place of approximate MCSP:

`n^{-epsilon}-Q notin P-uniform-SIZE[n^{1+epsilon+o(1)}]`

implies `P != NP^{oplus P}` (or a precisely stated comparable uniform
separation).

**Nearest known theorem / openness audit.**  Theorem 11 proves the claim for
approximate MCSP; Theorems 8--10 cover sparse NP/formula and constructive
distinguisher ingredients.  The paper poses the generalization.  An arbitrary
sparse `Q` cannot be allowed without an effectivity condition--an undecidable
sparse set supplies a spurious premise--so the first research deliverable is
a correct minimal formulation (e.g. `Q in P`, uniform sparse enumeration, or
a uniform reduction property), not a proof under an ambiguous phrase.

**Technique/dependencies.**  Audit exactly where MCSP self-reducibility or
uniform constructivity enters the uniform Santhanam--Williams simulation.
Formalize that dependency as an abstract interface and test it on MKTP, a
sparse P set, and an adversarial sparse set.

**Score:** `(5,3,5,4,3)`, product `900`.

### M3. Constructive Santhanam--Williams lower bound

**Precise target (`OPEN (source-stated)`):** Make the uniform
Santhanam--Williams lower-bound argument constructive enough to output a
specific natural P problem `L` and prove that `L` lacks P-uniform circuits of
the promised near-linear size, with all uniformity and running-time bounds
explicit.

**Nearest known theorem / openness audit.**  Atserias--Muller identify this as
an open frontier; their explicit sparse distinguisher is an ingredient but
does not itself name the required hard P language.  Existing nonconstructive
diagonalization and meta-problem magnification do not settle the target.

**Technique/dependencies.**  Uniform diagonalization, explicit selection of a
hard stage, and constructive distinguishers.  The likely first falsification
test is to expose whether selecting the hard stage requires a circuit lower
bound oracle or noncomputable advice.

**Score:** `(5,2,5,3,3)`, product `450`.

### M4. Cross the `2N` deterministic-circuit/wire barrier for sparse MCSP

**Precise target (`OPEN (source-stated)`):** For a fixed
`n <= s(n) <= n^2/log n`, prove an unconditional deterministic fan-in-two
circuit lower bound of `2N-o(N)` **in the same wire/size convention used by the
CCC 2022 construction** for `MCSP[s]`.

**Nearest known theorem / openness audit.**  An explicit sparse P language
needs `2N-2` wires against probabilistic circuits, but it is not MCSP.  CCC
2022 conditionally magnifies a `2N+O(N/log log N)` probabilistic-circuit lower
bound for MCSP and explicitly highlights the deterministic `2N-o(N)`
frontier.  No theorem found crosses it for the specified sparse MCSP regime.

**Technique/dependencies.**  Almost-universal hashing plus a direct-sum or
wire-elimination lemma specialized to circuit-minimal truth tables.  Finite
experiments should distinguish gate count from wire count and enumerate the
best trivial membership circuits; a lower bound below an existing upper bound
must be rejected immediately.

**Score:** `(4,2,5,5,4)`, product `800`.

### M5. Sparse-threshold probabilistic-formula lower bound above quadratic

**Precise target (`OPEN/UNKNOWN after search`):** For some fixed `d` and
`epsilon>0`, prove

`MCSP[(log N)^d] notin ProbFormula[N^{2+epsilon}]`.

Even `N^2(log N)^{omega(1)}` in the exact Chen--Jin--Williams regime is a
meaningful calibrated subtarget.

**Nearest known theorem / attempted disproof of openness.**  The known lower
bound in this sparse range is
`N^{2-K/log log N}/s(N)`, while the unconditional
`N^{2+alpha-epsilon}` theorem takes `s=N^alpha`.  The latter cannot be plugged
in by monotonicity: changing the MCSP threshold changes both YES and NO sets.
No sparse-threshold superquadratic theorem was found.

**Technique/dependencies.**  Strengthen the inconsistent-label/list
construction in the restrictions/PCP-of-proximity framework.  Computational
search can enumerate the smallest obstruction lists and detect whether the
list-size recurrence already loses a power of `N`.

**Score:** `(4,1,5,5,4)`, product `400`.

### M6. Worst-case-to-approximate reduction in the non-natural parameter regime

**Precise target (`OPEN (source-stated family)`):** Give a size-preserving
reduction, or prove an equivalence with quantified losses, from worst-case

`MCSP[n^c,2^{n^gamma}]`

for a fixed `gamma<1` to the approximate/gap MCSP problem appearing in the
ITCS 2020 naturalization equivalence, while keeping a hypothetical
`N^{1+epsilon}` lower bound above the magnification threshold.

**Nearest known theorem / openness audit.**  ITCS 2020 proves an equivalence
for a different worst-case gap extending to about `2^n/n^c` and explicitly
asks for the `2^{n^gamma}` extension.  Existing hardness amplification loses
parameters or localizes.  No parameter-preserving extension was found.

**Technique/dependencies.**  Error-correcting encodings of truth tables,
hardness amplification, and circuit reconstruction with an explicit table of
all size and distance losses.  A reduction that expands truth-table length
enough to turn `N^{1+epsilon}` into linear size fails the target.

**Score:** `(5,2,5,4,3)`, product `600`.

### M7. Close the deterministic one-tape exponent gap

**Precise target (`OPEN/UNKNOWN after search`):** For the constant `mu>0` in
the STACS 2021 magnification theorem, prove

`MCSP[2^{mu n}] notin DTIME_1[N^{1.01}]`

in its exact one-way-input/two-way-work-tape model, or first prove a uniform
exponent `1+delta` for an explicit `delta>0` in the same magnifying range.

**Nearest known theorem / attempted disproof of openness.**  The source gives
the implication to `P != NP` and unconditional near-quadratic randomized
lower bounds only for `mu>1/2`; its short-oracle theorem explains why those
parameters do not transfer to the small magnifying `mu`.  Searches found no
later theorem matching both `mu` and the model.  Because the exact target
would already imply `P != NP`, it is a benchmark rather than the recommended
first attack.

**Technique/dependencies.**  Crossing sequences/information transfer plus a
nonlocal encoding that works for small circuit thresholds.  Small-machine
enumeration can test proposed crossing-sequence invariants but cannot validate
the asymptotic separation.

**Score:** `(4,2,5,5,3)`, product `600`.

### M8. Replace existential local distributions by a canonical balanced distribution

**Precise target (`OPEN-STATUS UNCERTAIN; needs a dedicated 2023--2026 audit`):**
Construct a canonical efficiently samplable, balanced distribution family
`D_n` for a fixed `Gap-MCSP[n^delta,o(n/log n)]` such that bounded-error
average-case hardness under `D_n` is equivalent to the existence of one-way
functions, with all almost-everywhere and advantage quantifiers matching.
A stronger uniform-input claim should not be adopted without first resolving
the severe NO-instance imbalance.

**Nearest known theorem / attempted disproof of openness.**  STOC 2022 proves
the equivalence for an existential locally samplable distribution.  Liu--Pass
and Ren--Santhanam give uniform-distribution characterizations for `K^t`,
`Kt`, and `KT`, not this total Gap-MCSP statement.  Search surfaced later
worst-to-average and zero-knowledge formulations whose exact assumptions have
not yet been theorem-by-theorem checked here; accordingly this is not safe to
call definitely open.

**Technique/dependencies.**  Distributional reductions, balanced yes-instance
samplers, and local coding.  Immediate falsification test: compute YES mass
under uniform truth tables and reject any formulation permitting the constant
NO algorithm.

**Score:** `(4,2,4,4,2)`, product `256` (uncertainty penalty).

### M9. Nonlocal Formula-XOR lower bound at Frontier B

**Precise target (`OPEN (source-stated)`):** Prove

`Gap-MCSP[2^{n^{1/3}},2^{n^{2/3}}] notin Formula-XOR[N^{1.01}]`

by a method that demonstrably fails after the specific `N^epsilon`-fanin
oracle gates from the locality upper bound are inserted.

**Nearest known theorem / attempted disproof of openness.**  ITCS 2020 proves
an ordinary-formula lower bound around `N^{1.99}` and an
interactive-proof/Formula-XOR lower bound around `N^{1.99}`, but neither is a
Formula-XOR lower bound for the problem itself.  The paper's oracle upper
bound rules out a fully local proof, not the statement.  No later resolution
was located.

**Technique/dependencies.**  A parity-sensitive restriction or communication
measure that is not preserved by the short oracle.  First formal task: express
and verify the oracle upper bound in the same Formula-XOR syntax so that a
candidate measure's failure can be tested mechanically.

**Score:** `(4,1,5,5,3)`, product `300`.

## 5. Exactly one recommended first target

**Recommend M1: prove an `Omega(N^2/polylog N)` deterministic branching-program
lower bound for standard total `MCSP[n^2]`.**

It is the best first attack because the statement is finite and unambiguous,
the current-vs-target gap is only subpolynomial, the exact target is already
known for the neighboring random-access problem MKTP, and failure can produce
useful structural information about why circuit size lacks the blockwise
rigidity of `KT`.  It does not require assuming a magnification conclusion or
trying to prove `P != NP`.  It is also independently falsifiable through BP
upper-bound searches, subfunction counts, and a formal Nechiporuk lemma.

The first work package should be strictly bounded:

1. fix `s(n)=n^2`, the fan-in-two basis, BP size convention, and rounding;
2. reproduce the MKTP `Omega(N^2/log^2 N)` Nechiporuk proof lemma by lemma;
3. isolate the one lemma that uses random-access `KT` rather than circuit size;
4. exhaustively enumerate small circuit-size truth-table slices and their
   block subfunctions to test the strongest plausible replacement lemma;
5. attempt a counterexample restriction family before attempting an
   asymptotic proof; and
6. submit any surviving replacement lemma to independent proof and literature
   audits before classifying it as a proof candidate.

## 6. Remaining uncertainties

* The Atserias--Muller results are a June 2025 arXiv preprint; no peer-reviewed
  version was located during this audit.
* Several magnification theorems contain nested “for every sufficiently small
  beta,” `o(1)`, or almost-everywhere quantifiers.  Any later use must quote the
  source theorem rather than infer a uniform constant silently.
* MCSP threshold encodings and circuit basis conventions vary.  A reduction
  can lose exactly the factor needed for magnification.
* M8 is deliberately marked uncertain pending an exact audit of post-2022
  average-case MCSP papers; it should not enter the core open-target set as a
  high-confidence novelty claim yet.
* A negative literature search is not proof of openness.  M1, M5, M7, and M9
  require a second independent source audit before any attack is labeled
  potentially novel.

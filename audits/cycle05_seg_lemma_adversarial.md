# Adversarial audit: Lemma SEG (segment version of the FLSY interval theorem)

**Role:** SKEPTIC (adversarial mathematical review).
**Date:** 2026-08-21.
**Target:** the reconstruction-based "Lemma SEG" of
`research_cycle_05/flsy_reconstruction.md` §3, imported as a labeled
conditional hypothesis by Theorem C of
`research_cycle_05/switch_structure_theory.md` §5.
**Working assumption during review:** SEG is FALSE; hunt for
anchor-dependence and boundary failures in the localization argument.

**Primary sources (fetched and read for this audit, not taken from the
reconstruction):**

- ECCC TR26-001 (Fabris, Limaye, Srinivasan, Yehudayoff, "Multilinear
  Algebraic Branching Programs and the Min-Partition Rank Method", Jan 1,
  2026), downloaded from `https://eccc.weizmann.ac.il/report/2026/001/download`
  (42 PDF pages). Read line by line: Definition 3.1 (p. 16), all of §4
  (pp. 18-25): Definition 4.1, Lemma 4.2 + proof (§4.2, pp. 19-21),
  Lemma 4.3 + proof (§4.4, pp. 24-25), Lemma 4.5 + proof (pp. 21-22),
  Lemma 4.6 + proof (pp. 22-23), Lemma 4.7 + proof (pp. 23-24),
  Theorem 4.4 + proof (p. 19).
- Published version, LIPIcs vol. 383 (CCC 2026) Art. 22, downloaded from
  drops.dagstuhl.de; pp. 22:16-22:19 read. Lemma 21 = ECCC 4.2,
  Lemma 22 = ECCC 4.3, Theorem 23 = ECCC 4.4, statements identical
  (including `O(n^{5/2})`, `max_{r in [n]}`, and the hypothesis
  `n^{1/4-eps} >= (2/3) ln n`). The published version omits the proof of
  Lemma 22 ("We omit the proof of this lemma"); the ECCC full version is
  therefore the authoritative source for the proof and is what this audit
  examined.

Only after forming my own reading of §4 did I compare against
`flsy_reconstruction.md` §3. Monte Carlo scripts:
`experiments/cycle05_audit_seg_mc.py` (main),
`experiments/cycle05_audit_seg_selftest.py` (DP verified against an
independent brute force on 2,170 small instances before use), results in
`experiments/cycle05_audit_seg_mc_results.json`.

---

## 0. Inventory: where the anchoring at the empty set actually enters FLSY §4

This is the load-bearing question for SEG. My independent census of every
use of the chain anchor (C_0 = emptyset, walks starting at value 0) in the
primary source:

**In Lemma 4.2 (the reduction), three uses, all bookkeeping:**

1. The chain's first added element s and last added element e are
   enumerated (union bound over (s,e) in [n]^2, cost O(n^2)); the cyclic
   interval P = [s,e] with s+1 in P splits every chain element R as
   S_+(m) = R cap P = [s, a_m], S_-(m) = R cap N = [b_m, s-1]
   (Equation (2), p. 19). The cyclic bookkeeping exists to uniformize the
   two endpoint cases (for chains of linear intervals ending at [n], the
   last added element is always 1 or n).
2. Both extracted walks are normalized to start at value 0
   (X(0) := 0 =: Y(0), p. 20), matching f(emptyset) = 0; the chain event
   becomes |X(alpha(t)) - Y(beta(t))| = |f(S_+(t)) + f(S_-(t))| <= k.
3. Balancedness of f is removed at cost O(n^{1/2}) via
   P_f[E] = P_g[E | g balanced] <= P_g[E] / P_g[balanced] (p. 21).

**In Lemma 4.3 / 4.7 (the exponential engine), exactly one use:**

4. Lemma 4.7 defines a (g,Delta)-sequence by |g(x_i) - g(x_{i-1})| >= Delta
   "with x_0 := 0" (p. 23), and the proof of Lemma 4.3 sets z_i := X(x_i)
   and notes "|z_i - z_{i-1}| >= Delta for all i in [L] (for z_0 := 0)"
   (p. 24). Since X(0) = 0 = Y(0), the base case of the first-passage
   decomposition uses |z_1 - Y(0)| = |z_1| >= Delta. This is the single
   point where the engine touches the common anchor: the first summand of
   T_{z_1,...,z_L}(Y) = sum_i F_{|Y(T_{...,z_{i-1}}) - z_i| - d} dominates
   F_{Delta - 2d} because Y starts at the same value from which the
   milestone gaps are measured. Every later summand uses only the
   consecutive gap |z_i - z_{i-1}| >= Delta and the fact that the previous
   tracking position is within d of z_{i-1} (p. 25) - fully translation
   invariant.

Nothing else in Lemmas 4.5, 4.6, 4.7 or the proof of 4.3 refers to the
origin: 4.5 and 4.6 are statements about fresh first-passage variables;
4.7's proof concatenates fresh |.|-passages to level Delta via the strong
Markov property. This census agrees with `flsy_reconstruction.md` §3(a)-(b).

---

## 1. Attack surface 1 - Definition 4.1's staircase coupling. **VERDICT: HOLDS** (two boundary repairs noted)

**Checked against the primary text.** Definition 4.1 (p. 18): minimum over
nondecreasing alpha: {0..n} -> {0..l}, beta: {0..n} -> {0..r} with
alpha(0) = 0 = beta(0), alpha(n) = l, beta(n) = r, per-step increments in
{0,1} summing to exactly 1; d_F = min max_{t in [n]} |X(alpha(t)) - Y(beta(t))|.

**(a) Segment event -> Fréchet event.** For nonempty intervals
A = [a,b] subset B = [a',b'] of the line, any chain
A = D_0 subset D_1 subset ... subset D_L = B of intervals automatically has
D_i = [a - u_i, b + v_i] with (u_i, v_i) a unit-step monotone staircase from
(0,0) to (a - a', b' - b). With U(u) := f([a-u, a-1]), V(v) := f([b+1, b+v])
(honest Definition-3.1 walks: value 0 at 0, +-1 increments),
f(D_i) = f(A) + U(u_i) + V(v_i). Setting X := f(A) + V, Y := -U, the chain
condition |f(D_i)| <= k for i in [L] is verbatim "some staircase of
Definition 4.1 achieves max <= k", i.e., d_F(X,Y) <= k; the i = 0 condition
|f(A)| <= k is an extra conjunct (Definition 4.1's max ranges over
t in [n], excluding t = 0, so the time-0 pair is not part of d_F). The map
chain -> staircase is a bijection. Definition 4.1 nowhere uses X(0) = Y(0);
it applies verbatim to offset walks. **Confirmed.**

**(b) Left-only stretches.** A chain extending only left for its first m
steps is the staircase alpha(t) = 0, beta(t) = t (t <= m): legal, since
alpha is only required to be nondecreasing with increments in {0,1}. The
Fréchet condition then reads |X(0) - Y(t)| = |f(A) + U(t)| = |f(D_t)| <= k.
**Correct translation; no failure.**

**(c) Boundary repair 1 (present already in the paper).** Definition 4.1
requires l, r in [n], i.e., both walks nonempty; but Lemma 4.2's own
conclusion takes max_{r in [n]} P_W[d_F(X_r, Y_{n-r}) <= k], which at r = n
invokes d_F against a length-0 walk (this exact degenerate case arises for
prefix-only chains, whose last added element makes P = [n]). The paper is
internally sloppy here. Repair (one line): state Definition 4.1 for
l, r in {0,...,n}, l + r = n; when r = 0, beta == 0 is forced and
d_F(X, Y_0) = max_t |X(t) - Y(0)|, the classical tube event, for which the
target bound holds a fortiori (P[walk of length L confined to width-2k
tube] <= exp(-Omega(L/k^2)), far below exp(-c L^{1/5}) for k < L^{1/5}).
The segment version inherits the same repair for one-sided growth
(B extends A on one side only).

**(d) Boundary repair 2 (segment statement).** The canonical decomposition
in (a) needs A nonempty. For A = emptyset the intermediate intervals share
no anchor and the seed s = D_1 must be enumerated (<= L choices for fixed
B), exactly as FLSY do; the bound survives with one extra polynomial
factor. SEG should either hypothesize A nonempty (all of Theorem C's uses
have |A| >= 3) or include that factor.

---

## 2. Attack surface 2 - milestones and first-passage domination under an initial offset. **VERDICT: HOLDS** (verified line by line; the offset costs nothing beyond k <= d)

**The offset claim.** Let |X(0) - Y(0)| = |f(A)| = |a_0| <= k <= d,
Delta = 3d. Apply Lemma 4.7 to the centered milestone walk (the longer of
U, V; the (g,Delta)-sequence condition is invariant under adding the
constant a_0, so L_Delta is unchanged). Milestone values z_i := X(x_i)
satisfy |z_i - z_{i-1}| >= Delta for i >= 2 and |z_1 - X(0)| >= Delta.
The first-passage decomposition (p. 25) then needs:

- Base case i = 1: |z_1 - Y(0)| >= |z_1 - X(0)| - |X(0) - Y(0)|
  >= Delta - k, so the first summand stochastically dominates
  F_{Delta - k - d} >= F_{Delta - 2d} iff k <= d. **This is the entire
  effect of the offset.** (Alternatively drop milestone 1 and run with
  L - 1 summands; then no constraint linking k and the offset is needed at
  all. Either way only constants move.)
- Steps i >= 2: the printed argument (p. 25) uses only
  Delta <= |z_i - z_{i-1}| <= |z_i - Y(T_{...,z_{i-1}})| + d, hence
  F_{Delta-2d} <= F_{|z_i - Y(...)| - d}, with no reference to the origin.
  **Translation invariant, untouched by the offset. Confirmed against the
  displayed identity T_{z_1..z_L}(Y) = sum_{i=1}^L F_{|Y(T_{..z_{i-1}}) - z_i| - d}.**

**Hidden uses of full length n - exhaustive check.** Substituting n := L
(total added length), the proof of Lemma 4.3 uses the walk lengths in
exactly three places, all of which scale:

1. w.l.o.g. the milestone walk has length >= n/2 (d_F is symmetric in its
   arguments; Definition 4.1 is symmetric under swapping (X,l,alpha) and
   (Y,r,beta)) -> longer extension side has length >= L/2; Lemma 4.7 gives
   L' >= L/(2 c_3 Delta^3) milestones except with probability exp(-Omega(Delta)).
2. The tracking walk has length r <= n/2, used as
   P[sum F <= r] <= P[sum F <= n/2] -> shorter side <= L/2. If the shorter
   side is very short (even length 0), the event only gets harder; Lemma
   4.6's bound is uniform in the tracking walk's length because truncation
   makes F_delta stochastically larger and only the lower tail of the sum
   is used (see the slop note below).
3. Delta >= 2 log(milestone-walk length) in Lemma 4.7 -> implied by
   Delta = 3d, d >= (2/3) ln L (with log = ln, which is the reading that
   makes 4.7's own final display "l 2^{-Delta} <= 2^{-Delta + log(n/c_3 Delta^3)}
   <= e^{-Omega(Delta)}" correct).

The "sufficiently large n" hypothesis of Lemma 4.3 is an absolute
threshold, uniform in l(n) and eps(n); under n := L it becomes L >= L_0
with L_0 universal. The hypothesis n^{1/4-eps} >= (2/3) ln n becomes, at
eps = 1/20 (the value that balances min{L^{1/4-eps}, L^{4 eps}} to
L^{1/5}), the requirement L^{1/5} >= (2/3) ln L - true for all
L >= ~7.5e3 and absorbed into L_0. Lemma 4.6's hypotheses instantiate with
polynomial margin: k := L' = Theta(L/d^3), delta := d gives
k delta^2 = Theta(L/d) <= c_4 L/2 and (k delta)^2 = Theta(L^{6/5}) = omega(L),
yielding exp(-Omega(L/d^4)) = exp(-Omega(L^{1/5})), exactly Equation (6)
of the paper with n replaced by L. **No hidden global-length dependence
found. The reconstruction's §3(b) claim ("F_{Delta-d-k} vs F_{Delta-2d},
constants only") is exactly right.**

**Empirical cross-check (Monte Carlo, §6):** conditional survival curves
for offset |a_0| = 2 vs a_0 = 0 at k = 2 differ by a constant factor
~0.68 over L = 10..150 with fitted decay rates 0.0128 vs 0.0143
(equal within noise): the offset shifts the constant, not the rate.

---

## 3. Attack surface 3 - unconditioning (balanced f -> uniform g) and independence. **VERDICT: HOLDS**

**Independence.** Under uniform g on {+-1}^[N], the triple
(g(A), U, V) consists of functions of three pairwise disjoint coordinate
sets (A, the left arc of B\A, the right arc of B\A); hence mutually
independent, with U, V exact simple random walks. Conditioning on
g(A) = a_0 leaves (U, V) uniform, so
P_g[segment event] <= max_{|a_0| <= k} P_{U,V}[d_F(a_0 + V, -U) <= k],
which is what the offset engine bounds. (One can keep the free extra
factor P[|g(A)| <= k] = O(k/sqrt(|A|)) for sharpness; not needed.)
**No circularity, no hidden correlation.**

**Placement of the O(sqrt(N)).** The step
P_f[E] = P_g[E | g balanced] <= P_g[E] / P_g[g balanced] = O(sqrt(N)) P_g[E]
is a pointwise counting inequality, valid for every event E regardless of
any correlation between E and balancedness; P_g[g balanced] = Theta(N^{-1/2})
is the central binomial estimate for the WHOLE ambient coloring. So the
factor is correctly O(sqrt(N)) - the ambient size - and cannot be improved
to O(sqrt(L)) by this route. The SEG statement in
`switch_structure_theory.md` places it correctly. Under balanced f the
restriction of f to B\A is not balanced and is weakly negatively
correlated; none of that is used or needed, because the whole argument
runs under uniform g after this one inequality. **Airtight.** (Consequence,
correctly flagged by the reconstruction: the bound is vacuous unless
exp(-c L^{1/5}) beats sqrt(N) times the union-bound polynomial, i.e.,
unless L >= C (log N)^5.)

**Parity/normalization gap (repair needed in the statement).** SEG as
written speaks of "a uniformly random balanced coloring f of [N]"; Theorem
C applies it on Z_q with q = n - 1 odd, where balanced colorings do not
exist and the repository's normalized colorings have |f(Z_q)| = 1. The
identical unconditioning argument covers this: for any fixed sigma with
|sigma| <= 1 (indeed |sigma| <= C sqrt(N)),
P_g[g([N]) = sigma] = Theta(N^{-1/2}). SEG should be stated for the
conditioning f([N]) = sigma, |sigma| <= 1. Trivial repair, but as
literally written the statement does not cover its one intended
application.

---

## 4. Attack surface 4 - cyclic-to-linear cutting. **VERDICT: HOLDS with proviso (B != Z_q; A != emptyset)**

If B != Z_q, the complement Z_q \ B is a nonempty arc; cutting the circle
at ANY point c of the complement (endpoint or not) turns every cyclic
interval D with A subset D subset B into a linear interval of the cut
order (a cyclic interval avoiding the cut point is a linear interval), the
cut is a measure-preserving relabeling, and the two arcs of B\A are the
same coordinate sets before and after. So the linear SEG bound applies
verbatim. **Always available exactly when B != Z_q.**

If B = Z_q the cut point does not exist. The event is still controlled:
for A != emptyset the decomposition D_i = A cup [a-u_i, a-1] cup [b+1, b+v_i]
(cyclic arcs) remains valid for every chain from A to Z_q - the two
extension arcs are disjoint until they exactly tile Z_q \ A at the final
step - but the terminal split (u_L, v_L) is no longer determined by B, so
one pays a union bound over the <= L + 1 splits. Repair: either state SEG
with B != Z_q for the cyclic case, or add the (L+1) factor for B = Z_q.
Theorem C never needs the excluded case: its runs live at sizes in
[3, q-3], so |A| >= 3 (nonempty) and |B| <= q - 3 (proper), and the
growth never enters the complement of B, exactly as its sketch says.

---

## 5. Findings not on the requested list (paper-level slops; none fatal, all pre-existing in the anchored proof and inherited unchanged)

These were found during the line-by-line reading. They affect the FLSY
write-up itself, carry over to any segment re-derivation, and each has a
one-line repair; they do not change any statement:

1. **Overstated extraction claim (p. 25):** "if d_F(X,Y) <= d then for
   every strictly increasing (a_1..a_m) there is a strictly increasing
   (b_1..b_m) with |X(a_i) - Y(b_i)| <= d" is false as universally
   quantified (e.g., no strictly increasing sequence of length m > r + 1
   exists in {0..r}; X oscillating in a tube against a length-1 Y gives a
   concrete counterexample). It is true for the milestone sequence used,
   because consecutive milestone values differ by >= Delta = 3d > 2d,
   which forces the extracted b_i to be strictly increasing. Repair: state
   it for sequences with |X(a_{i+1}) - X(a_i)| > 2d. The segment/offset
   version uses the identical corrected form (gaps are offset-invariant).
2. **Lemma 4.5's range vs walk length:** Lemma 4.6's proof applies the
   lower bound P[F_delta >= t] >= c delta / sqrt(t) for t up to n/2
   (threshold parameter), while the tracking walk may be shorter than 2t;
   Lemma 4.7's proof applies the upper bound at z equal to the full
   segment length rather than half. Both repaired by stating Lemma 4.5
   for the infinite walk (its proof already is length-uniform: the
   pointwise formula P[F_delta = y] = (delta/y) 2^{-y} binom(y, (y+delta)/2)
   does not involve n) plus monotonicity under truncation
   ({F_delta(g_r) >= t} contains {F_delta(g_inf) >= t}). Only the lower
   tail of sum F is ever used, so shorter tracking walks only help.
3. **l, r in [n] vs r = 0** in Definition 4.1 / Lemma 4.2's max (§1(c) above).
4. **log vs ln:** Lemma 4.7's "Delta >= 2 log n" must be read with
   log = ln for its final display to close; Lemma 4.3's hypothesis
   supplies Delta = 3d >= 2 ln n. Constants only.
5. **<= vs < at the threshold:** Theorem 4.4's proof bounds
   P_W[d_F <= n^{1/5}] by Lemma 4.3's bound on P_W[d_F < n^{1/4-eps}];
   for non-fifth-power n these coincide (d_F is an integer), otherwise
   adjust eps infinitesimally. In the segment derivation this never
   arises: k < L^{1/5} = d strictly, and {exists k-chain} subset
   {d_F <= k} subset {d_F < d}.

**Reconstruction-level issues (must be fixed in the repository statement):**

6. The SEG display in `switch_structure_theory.md` §5 is garbled: it
   contains both "|f(D_i) - f(A)| ..." (truncated) and "all |f(D_i)| <= k".
   The two variants (absolute and relative-to-f(A)) are BOTH provable by
   the same engine (the relative one with zero offset, the absolute one
   with offset |f(A)| <= k), but the statement must pick one. Theorem C
   uses the absolute one (running sums in {0,1,2}, k = 2). Endorsed text
   in §7 below.
7. Missing hypotheses: A nonempty (§1(d)); cyclic case needs B != Z_N or
   an extra (L+1) factor (§4); ambient normalization f([N]) = sigma,
   |sigma| <= 1, rather than "balanced" (§3), so that odd ambient sizes
   (Theorem C's q = n - 1) are covered.
8. Cosmetic: "D_L = B with |B\A| = L" plus "every k < L^{1/5}" should also
   record k >= 1 (below 1 the event is empty for L >= 1 by parity) and
   that the "any B" form costs a factor L + 1.

None of these touches the exponential engine; items 6-8 are statement
hygiene, items 1-5 are inherited from the paper and repairable in place.

---

## 6. Monte Carlo sanity check (attack surface 5)

**Design** (`experiments/cycle05_audit_seg_mc.py`, seed 20260821): N = 2000,
A = positions [800, 1199] (|A| = 400, central; 800 slots on each side),
f uniformly random balanced. Event: exists interval chain
A = D_0 subset ... subset D_L with all |f(D_i)| <= k, for ANY B >= A with
|B\A| = L (the union-over-B form used by Theorem C). Since the event is
monotone in L it equals {T >= L} for the survival depth T; T computed
exactly per coloring by the reachable-set DP over (u, v) frontier states
(O(L^2) per coloring, batched in numpy). The DP was verified against an
independent DFS brute force on 2,170 random small instances (N = 14, 16,
20; k = 1, 2) with zero mismatches (`cycle05_audit_seg_selftest.py`).
92,000 balanced colorings sampled; conditioning on the (L-independent)
acceptance event |f(A)| <= k; M = 4,000 accepted colorings analyzed for
k = 1 (P[f(A) = 0] ~ 0.0440), M = 6,000 for k = 2 (P[|f(A)| <= 2] ~ 0.1311).

**Results** (conditional survival P[T >= L | |f(A)| <= k]; absolute
estimate = conditional x P[accept]; "prefix-only" = one-sided rightward
growth only, the classical tube event, for contrast):

| L | k=1 cond. | k=1 absolute | k=2 cond. | k=2 absolute | k=2 prefix-only cond. |
|------|-----------|--------------|-----------|--------------|------------------------|
| 10 | 0.58025 | 2.55e-02 | 0.67467 | 8.84e-02 | 0.21933 |
| 20 | 0.37650 | 1.66e-02 | 0.55967 | 7.34e-02 | 0.04833 |
| 50 | 0.12350 | 5.44e-03 | 0.34500 | 4.52e-02 | 0.00050 |
| 100 | 0.02050 | 9.02e-04 | 0.16917 | 2.22e-02 | 0 |
| 150 | 0.00325 | 1.43e-04 | 0.08900 | 1.17e-02 | 0 |
| **200** | **0.00075** | **3.30e-05** | **0.04467** | **5.85e-03** | 0 |
| 300 | 0 (< 7.5e-4) | < 3.3e-05 | 0.01150 | 1.51e-03 | 0 |
| 400 | 0 | - | 0.00267 | 3.50e-04 | 0 |
| **500** | 0 | < 3.3e-05 | **0.00067** | **8.74e-05** | 0 |
| 700 | 0 | - | 0 (< 5e-4) | < 6.6e-05 | 0 |
| **1000** | 0 | < 3.3e-05 | 0 | < 6.6e-05 | 0 |

("< x" entries are rule-of-three 95% upper limits for zero observed
successes. Max observed T: 239 for k = 1, 590 for k = 2; no coloring
censored at the cap 1600.)

**Offset dependence, k = 2** (conditional on acceptance, split by
a_0 = f(A); M = 2,029 with a_0 = 0, M = 3,971 with |a_0| = 2):

| L | P[T >= L, a_0 = 0] | P[T >= L, abs(a_0) = 2] | ratio |
|-----|--------------------|--------------------------|-------|
| 10 | 0.85461 | 0.58272 | 0.682 |
| 20 | 0.71217 | 0.48174 | 0.676 |
| 50 | 0.43765 | 0.29766 | 0.680 |
| 100 | 0.21587 | 0.14530 | 0.673 |
| 150 | 0.11286 | 0.07681 | 0.681 |
| 200 | 0.05323 | 0.04029 | 0.757 |
| 300 | 0.01232 | 0.01108 | 0.899 |
| 400 | 0.00148 | 0.00327 | 2.2 (3 vs 13 survivors: noise) |

The ratio is a constant ~0.68 over two decades of probability; fitted
exponential rates 0.0143 (a_0 = 0) vs 0.0128 (|a_0| = 2). Offset moves
the constant, not the rate - the empirical counterpart of §2.

**Shape fits** (least squares of ln P[T >= L] against -c g(L) + b on grid
points with >= 10 survivors, L >= 50; R^2 shown):

| model g(L) | k=1: c (R^2) | k=2: c (R^2) |
|------------|---------------|---------------|
| L^{1/5} | 6.67 (0.984) | 4.25 (0.940) |
| L^{1/3} | 2.21 (0.988) | 1.31 (0.958) |
| L^{1/2} | 0.70 (0.993) | 0.38 (0.976) |
| L | 0.036 (0.9999) | 0.014 (0.9997) |
| ln L | 3.23 (0.975) | 2.27 (0.906) |

**Interpretation and anomaly scan.**

- The probability decays monotonically and strictly with L for both k,
  with no plateau, over ~3 decades. **No anomaly of the falsifying kind
  (non-decay) is present.**
- k = 1 decays faster than k = 2, and the one-sided (prefix) event decays
  enormously faster than the adaptive two-sided event (at L = 50, k = 2:
  0.0005 vs 0.345) - a direct empirical confirmation that two-sided
  adaptivity is the phenomenon that forces the Fréchet machinery rather
  than classical tube confinement, exactly the paper's motivation for
  Lemma 4.3.
- In this range the decay is best fit by a PURE exponential in L
  (R^2 > 0.999), i.e., far FASTER than exp(-c L^{1/5}). An upper-bound
  claim of the form P <= O(sqrt(N)) exp(-c L^{1/5}) is consistent with
  any decay at least that fast, so the data is fully consistent with SEG;
  it also confirms the expectation that FLSY's 1/5 exponent is far from
  tight (nothing in SEG's use requires tightness). Standard caveat: at
  L <= 590 with survival >= 1/6000, an asymptotic stretched-exponential
  regime would not yet be visible; finite data can neither confirm nor
  refute an exponent. The check is qualitative, and it is passed.

---

## 7. Exact statement of SEG endorsed by this audit

> **Lemma SEG (endorsed form).** There exist universal constants
> c > 0, C > 0, L_0 such that the following holds for every N in N and
> every sigma in Z with |sigma| <= 1. Let f be uniform on
> {g : [N] -> {-1,+1}, g([N]) = sigma} (for even N and sigma = 0 this is
> the uniform balanced coloring). Let A subset B subset [N] be fixed
> intervals with A != emptyset and L := |B \ A| >= L_0, and let
> 1 <= k < L^{1/5}. Then
>
> P_f[ exists a chain A = D_0 subset D_1 subset ... subset D_L = B,
> each D_i an interval of [N], with |f(D_i)| <= k for all 0 <= i <= L ]
> <= C sqrt(N) exp(-c L^{1/5}).
>
> Moreover:
> (i) (uniform version) for g uniform on {-1,+1}^[N] the same event has
> P_g <= C exp(-c L^{1/5}), with no sqrt(N) factor;
> (ii) (any-B version) the event "exists an interval B >= A with
> |B \ A| = L and a chain as above" costs an extra factor (L + 1);
> (iii) (cyclic version) both hold verbatim on the cyclic order Z_N
> provided B != Z_N (cut the circle at any point of Z_N \ B); for
> B = Z_N they hold with an extra factor (L + 1) (union over the final
> split of Z_N \ A);
> (iv) (relative version) with the constraint |f(D_i) - f(A)| <= k
> (i >= 1) in place of |f(D_i)| <= k, bounds (i)-(iii) hold with the
> offset set to 0.
>
> On the event of the absolute form, |f(A)| <= k automatically (i = 0);
> the proof uses only |f(A)| <= L^{1/5}.

Provenance of every ingredient: Lemma 4.3 restated with n := L and an
initial offset <= d (proof unchanged, §2 above = ECCC pp. 24-25);
Lemma 4.7 with n := length of the longer extension (ECCC pp. 23-24);
Lemmas 4.5-4.6 verbatim (ECCC pp. 21-23); the reduction of §1 above,
which is a strict simplification of Lemma 4.2's (ECCC pp. 19-21: no (s,e)
enumeration, no cyclic bookkeeping); unconditioning as in ECCC p. 21.
This matches `flsy_reconstruction.md` §3(c) up to the added hypotheses
(A != emptyset; B != Z_N or factor; sigma-normalization; k >= 1) and the
disambiguated event.

**Consequence for Theorem C:** Theorem C's import is covered by the
endorsed form: it uses the absolute event with k = 2, cyclic order,
|A| >= 3 (nonempty), |B| <= q - 3 (so B != Z_q and a cut point exists),
ambient normalization |f(Z_q)| = 1 (needs form with sigma != 0 since
q odd - this is why repair §5.7 matters), and its own union bound
t x (<= q^2 choices of A) x (<= q splits) <= t q^4 with slack. The
absorption condition L* >= C (log q)^5 is exactly what makes
t q^4 sqrt(q) exp(-c (L*)^{1/5}) <= t exp(-(c/2)(L*)^{1/5}) for
poly-size lists. Theorem C's arithmetic checks out GIVEN SEG; its
CONDITIONAL label remains the correct epistemic status.

---

## 8. Overall verdict

**SOUND WITH REPAIRS.**

The core adversarial hypothesis - that the FLSY proof secretly depends on
the anchoring at the empty set in a way that blocks localization - is
REFUTED by the primary source. The anchor enters the exponential engine at
exactly one point (z_0 := 0 in the milestone base case, ECCC pp. 23-24),
and an initial offset |f(A)| <= k <= d degrades exactly one of the
L = Theta(L/d^3) first-passage summands from F_{Delta-2d} to
F_{Delta-d-k}, which still dominates F_{Delta-2d}; every other ingredient
(Lemmas 4.5, 4.6, 4.7, the p. 25 domination chain, the Chernoff step) is
translation invariant and length-local, verified line by line. The
reduction side is strictly simpler than the paper's own Lemma 4.2. The
unconditioning inequality is pointwise and correctly priced at
O(sqrt(N)). The Monte Carlo shows monotone decay with an offset effect
that is a constant factor, not a rate change, and nothing inconsistent
with (indeed much stronger than) exp(-c L^{1/5}) decay.

The repairs required before SEG could be written out as a full proof are
all statement-level and routine (§5 items 6-8: disambiguate the garbled
event; add A != emptyset; add B != Z_N or an (L+1) factor in the cyclic
case; state the ambient normalization as f([N]) = sigma, |sigma| <= 1 so
odd ambient sizes are covered; record k >= 1 and the any-B factor), plus
five one-line expository repairs inherited from the paper itself (§5
items 1-5, of which the p. 25 extraction overstatement and the Lemma
4.5 range slop are the only ones requiring an actual sentence of
mathematics). No repair touches the exponential mechanism. With the §7
statement substituted for the current SEG display, I would classify the
lemma as PROOF CANDIDATE with a complete proof outline whose every
nontrivial step has been checked against the primary source; writing it
out in full would be a mechanical exercise.

---

## 9. Epistemic status reminder (required)

**Lemma SEG is a derived-from-technique claim, not a published theorem,
regardless of this audit's verdict.** FLSY (ECCC TR26-001 = CCC 2026)
state and prove ONLY the anchored interval theorem (Theorem 4.4 /
published Theorem 23: chains from emptyset to [n] under 1-interval set
systems); no segment, offset, or fixed-endpoint variant appears anywhere
in either version of the paper, and no independent publication of such a
variant is known. This audit verifies that the paper's own technique
proves the §7 statement; it does not change the fact that the statement
has never been refereed. Theorem C of
`research_cycle_05/switch_structure_theory.md` must therefore keep its
CONDITIONAL label, and any downstream result must inherit it, until
either (a) SEG is written out in full and independently verified as a
standalone proof, or (b) an equivalent statement appears in the
literature.

---

## Files

- This audit: `audits/cycle05_seg_lemma_adversarial.md`
- MC script: `experiments/cycle05_audit_seg_mc.py`
- DP self-test (brute-force cross-check): `experiments/cycle05_audit_seg_selftest.py`
- Raw results: `experiments/cycle05_audit_seg_mc_results.json`
- Primary sources (scratchpad copies fetched 2026-08-21): ECCC TR26-001
  full PDF; LIPIcs.CCC.2026.22 PDF.

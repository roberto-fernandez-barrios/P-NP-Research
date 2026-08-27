# Independent LP and old-statistic logic audit

This directory was prepared without reading the Cycle-7 LP reconstruction,
stage-I semantics, corner-realizability document, stored Cycle-7 audits, or
Cycle-7 checker code.  Primary-source retrieval date: `2026-08-27`.  It uses
these primary copies:

- Jiang--Cai, arXiv `2607.10697v1`, source fetched from
  `https://export.arxiv.org/e-print/2607.10697v1`, SHA-256
  `30A0DE3271E5B96C97CAA5BDF4A764DAD71F31F2CB5226C98438A1074110DD87`
  for the archive and
  `EC1A49684387E4DD3542D2239D8BADAEAFE6353DB27558C70A78C8DA0CDF9758`
  for its TeX file.
- Scheder, ECCC TR21-069 revision 1, PDF fetched from
  `https://eccc.weizmann.ac.il/report/2021/069/revision/1/download/`, SHA-256
  `E4D634C4EA46F58041FD35BFD4978B7BB95E77AD26530735AA0577822DC4E506`.

Both primary files byte-match the corresponding Cycle-7 frozen copies.  This
comparison was made only after the independent derivation was frozen.

The exact-rational checker is `verify_lp.py`.

## Reconstruction

Normalize the unique satisfying assignment to all ones.  From one canonical
critical clause `(x or not y or not z)` per variable, put arcs `x -> y,z` in
the critical-clause digraph.  In Scheder section 6, `J_j` (there printed
`ID_j`) is the class of all indegree-`j` variables.  In Scheder section 8,
`ID_j` is redefined to consist of indegree-`j` variables outside `TwoCC`.
Here `TwoCC` consists of variables with at least two critical clauses in the
Definition-31 augmented formula.  Therefore

```
i_0 = |ID_0|/n,   i_1 = |ID_1|/n,   tau = |TwoCC|/n.
```

All three coordinates are nonnegative.  Since the three counted sets are
pairwise disjoint, realizable vectors also obey `i_0+i_1+tau <= 1`.  The
Jiang--Cai LP deliberately relaxes to the whole nonnegative orthant.  This is
harmless for its optimum because the optimizer below is strictly inside the
simplex.

Scheder's Lemma 34 says

```
|H| >= n-|J_1|-2|J_0|.
```

Since `J_j = ID_j disjoint-union (J_j intersect TwoCC)` and
`|J_1 intersect TwoCC|+2|J_0 intersect TwoCC| <= 2|TwoCC|`, this implies

```
|H| >= n-|ID_1|-2|ID_0|-2|TwoCC|.                 (H)
```

Scheder's equation (11) is

```
(18/17)|H_low|+2|H_high|+3|TwoCC| >= |H|.         (S)
```

For fixed parameters, define

```
c_L = 0.001687 eps_R - 0.006404 eps_R^2
c_T = 0.009307 - 0.055 eps_R - 0.1503 f_KL(eps_R)
A   = (17/18)c_L
Thr = 2A/0.9
P   = 1.1 eps_R Thr
S   = c_T-5A.
```

The coefficients on `H_low,H_high` in the regular estimate are then
`(18/17)A,2A`.  Applying (S), and then (H), costs respectively `3A tau`
and `2A tau`, and gives

```
L_R(i_0,i_1,tau) = A-P-2A i_0-A i_1+S tau.
```

The irregular estimate directly gives

```
L_I(i_0,i_1,tau) = b_0 i_0+b_1 i_1+b_T tau,
```

where the three `b` coefficients are exactly the functions printed in
Jiang--Cai equations (b1)--(bT), transcribed from Scheder section 8.4.
Thus the fixed-parameter relaxation is

```
inf_{i_0,i_1,tau >= 0} max(L_R,L_I).               (P)
```

It is a Unique-3-SAT LP.  The general-3-SAT number is not the value of a
different structural LP: it is obtained afterward by applying the
Scheder--Steinberger unique-to-general lift to a safe unique bonus below the
value of (P).  In particular, the exact relaxation value `gamma*` below is
distinguished from Jiang--Cai's theorem-safe
`gamma_new=0.0000687793`; the Unique exponent is `p_0-gamma_new` with
`p_0=2 ln(2)-1`, while the general theorem uses the separately lifted safe
bonus `eta=0.000000364`.

## Symbolic solution and uniqueness

Put `c=A-P` and assume

```
c>0, b_1>0,
b_0-2b_1>0,
b_T+(b_1/A)S>0.
```

Take `lambda=b_1/A`.  For every point in the orthant,

```
max(L_R,L_I)
 >= (lambda L_R+L_I)/(1+lambda)
  = gamma
    + [(b_0-2b_1)i_0
       +(b_T+(b_1/A)S)tau]/(1+lambda),
```

where

```
gamma = b_1(A-P)/(A+b_1).
```

The two displayed slack coefficients are strictly positive, so equality in
this lower bound forces `i_0=tau=0`.  On that line the objective is

```
max(c-A i_1, b_1 i_1).
```

The first term is strictly decreasing and the second strictly increasing.
Their unique intersection, hence the unique minimizer, is

```
(i_0,i_1,tau) = (0,(A-P)/(A+b_1),0).
```

This proof does not use a numerical optimizer or the authors' dual.  Reading
the same calculation as an epigraph-LP dual gives the independently derived
weights

```
y_R=b_1/(A+b_1),  y_I=A/(A+b_1).
```

`verify_lp.py` certifies, entirely with rational intervals,

```
b_0-2b_1
  in [0.001340973980937947784581248454,
      0.001340973980937947784581248455]

b_T+(b_1/A)S
  in [0.013853745484230647393261014465,
      0.013853745484230647393261014466]

i_1*
  in [0.060043244708778326627395247971,
      0.060043244708778326627395247972]

gamma*
  in [0.000068779380458836565503549434,
      0.000068779380458836565503549435].
```

## What closure-realizability can and cannot imply

Let `D` be the old-statistic ambient domain, let `R` be the set of vectors
realized by finite admissible instances, let `f=max(L_R,L_I)`, and suppose a
separate proof establishes `x*=(0,i_1*,0) in closure(R)`.

1. Since `f` is continuous and `x*` minimizes it on `D`,
   `inf_{r in R} f(r)=f(x*)`.  This proves exactness of the *fixed two-affine-
   estimate objective* over realizable old statistics, in the infimum sense.
2. If an extra valid constraint has a closed feasible set `C` containing
   `R`, then `x* in C`.  This covers non-strict linear inequalities,
   continuous inequalities `Q>=0`, and finite conjunctions of non-strict
   polynomial inequalities (basic closed semialgebraic sets).
3. A general semialgebraic set need not be closed if strict inequalities or
   complements are allowed.  An arbitrary discontinuous predicate can also
   contain every point of `R` while excluding `x*`.  In fact this is not just
   hypothetical here.  Put `e=epsilon_I`, an exact rational in `(0,1)`.  The
   coefficient `b_1` has the form

   ```
   b_1 = r_0 - 0.4027(1-e) log(1-e)
   ```

   for rational `r_0`, with a nonzero rational log coefficient.  The real
   number `log(1-e)` is transcendental: if it were nonzero algebraic, the
   Hermite--Lindemann theorem would make its exponential transcendental,
   whereas that exponential is the rational `1-e`.  Hence `b_1`, and then
   `(A-P)/(A+b_1)=i_1*`, are transcendental (`A,P` are rational and
   `A-P != 0`).  Every finite normalized statistic is rational.  Therefore
   the valid predicate

   ```
   Q(i_0,i_1,tau) = 1  if all three coordinates are rational,
                    -1 otherwise
   ```

   satisfies `Q>=0` on every finite instance but fails at `x*`.  Thus the
   literal statement that *every* valid `Q` is satisfied at, or cannot remove,
   the corner is false unless a closedness/upper-semicontinuity condition is
   imposed.
4. Nevertheless, even an arbitrary predicate valid at every point of `R`
   cannot raise the **infimum** of the continuous objective: its feasible set
   still contains a realizable sequence converging to `x*`.  Thus a wording
   about asymptotic value can be stronger than a wording about retaining the
   optimizer, provided `minimum` is repaired to `infimum` when nonclosed
   constraints are admitted.
5. A constraint valid for all sufficiently large instances is likewise
   defeated by the tail of an admissible sequence with sizes tending to
   infinity.  For approximate inequalities `Q(r_n)>=-o(1)`, continuity (or a
   directly stated closed outer-limit condition) is needed to conclude
   `Q(x*)>=0`; the sequence still rules out any fixed positive improvement in
   the old continuous objective if those actual points remain feasible.

In the classes requested by the audit: non-strict linear inequalities and
continuous inequalities retain the corner; closed feasible-set constraints
retain it by definition; non-strict polynomial inequalities and basic closed
semialgebraic systems retain it; a general semialgebraic predicate with strict
inequalities need not (with real constants, `D \ {x*}` is semialgebraic);
arbitrary discontinuous predicates need not; and uniformly valid
size-dependent/asymptotic constraints cannot create a positive asymptotic
value gap because the realizing sequence exists at unbounded sizes (at every
large size if the all-`n` form of Theorem CR is validated).

Closure-realizability does **not** show the imported probability estimates
are tight on the realizing formulas, and it does not by itself prove that
they are loose there either; either assertion needs an independent analysis
of PPSZ/the source inequalities on that family.  It does not preclude a
stronger third estimate `L_new(i_0,i_1,tau)`, even one using only the same
three coordinates, nor a strengthening/reoptimization of the estimates that
produced `L_R` and `L_I`.  It also does not establish that the fixed numerical
parameter search was globally optimal over all allowable parameter choices.
The defensible strategic conclusion is therefore only:

> Feasibility information in the old three statistics alone cannot increase
> the fixed recombination infimum.  A further improvement must strengthen the
> estimates (which may still use the old statistics) or use additional
> structural/algorithmic information or statistics.

## Post-freeze comparison with Cycle 7

The formulas, orthant relaxation, exact value, optimizer, uniqueness proof,
and dual/slack signs in `research_cycle_07/lp_reconstruction.md` agree with
this independent derivation.  No LP discrepancy was found.

The following statement repairs are required; they do not alter the infimum
no-go:

- `research_cycle_07/corner_realizability.md` lines 63--69 says that no
  constraint, "linear or not", can exclude the corner.  The rationality
  predicate above is a direct counterexample.  Replace this with the
  closure/infimum theorem, adding closedness only for point retention.
- The same file's title and line 16, `results/research_cycle_07.md` lines 9
  and 37, and `RESEARCH_STATE.md` line 16 call the exact corner realizable.
  Since its second coordinate is transcendental, it is only
  closure-realizable.
- `results/research_cycle_07.md` lines 191--194 says every valid constraint
  "admits the corner".  Replace this by "contains realized points converging
  to the corner"; add "and admits the corner if closed".  Make the analogous
  repair to failure-knowledge entry `RC7-O18-01`.
- Qualify "exactly optimal over the statistic system" everywhere as exact
  optimality, in the infimum sense, of the fixed Jiang--Cai two-affine
  objective under old-statistic feasibility restrictions.  Jiang--Cai
  explicitly makes no global-optimality claim for its exploratory parameter
  search.
- Qualify "not a cleverer recombination" as "not another feasibility
  restriction or weighting of the two fixed affine functions".  A
  multi-parameter envelope or stronger estimate using the same coordinates
  is not ruled out.
- The assertions that the corner formulas are algorithmically easy and that
  the imported estimates are "simply very loose" are not consequences of
  realizability, and no independent PPSZ analysis establishing this was
  located in the Cycle-7 proof.  They are unnecessary for CR-2 and should be
  proved separately or downgraded.

Thus the LP reconstruction survives; CR-2 survives with a nontrivial but
statement-level topology/infimum repair, conditional on independent
validation of Theorem CR and its all-large-`n` sequence.

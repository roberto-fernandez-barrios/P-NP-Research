# Jiang--Cai exact validator: frozen independent design

Date frozen: 2026-08-27 (Europe/Madrid).

This design was written after reading the primary Jiang--Cai arXiv-v1 source
and public certificate, but before reading either
`research_cycle_07/checkers/independent_checker.py` or
`research_cycle_07/checkers/repair_certifications.py`.

## Independence boundary

The validator will be newly implemented with Python standard-library
`fractions.Fraction`; it will not import, execute, copy, diff, or adapt any
Cycle-7 validator.  It will not use ordinary floating point for a proof
decision.  Decimal formatting is non-evidentiary.

The public certificate supplies only fixed rational inputs and claimed
brackets.  Every mathematical check is recomputed from the formulas printed in
arXiv:2607.10697v1.

## Enclosure primitives

1. Closed rational intervals with exact `Fraction` endpoints and exact
   outward interval operations.
2. `ln(x)` for positive rational or rational intervals:
   reduce by an exact power of two to a mantissa in `[1,2)`, and use

       ln(y) = 2 sum_{j=0}^{N-1} z^(2j+1)/(2j+1) + R_N,
       z=(y-1)/(y+1),
       |R_N| <= 2 |z|^(2N+1)/((2N+1)(1-z^2)).

   `ln(2)` is the special case `z=1/3`.  Endpoint monotonicity encloses
   interval inputs.  The checker will use and explicitly audit `N=90`, the
   certificate's claimed truncation.
3. `exp(x)`: for nonnegative rational endpoints, sum the first `N=90`
   positive Taylor terms and bound the remaining tail by the next term times
   the geometric factor `1/(1-x/(N+1))` once `x < N+1`; for negative inputs,
   use reciprocal monotonicity.  Endpoint monotonicity encloses intervals.
4. `2^x = exp(x ln 2)`.  Every pass/fail comparison uses rational endpoints.

Each transcendental call records the exact truncation count and a rational
remainder-width bound, so successful final comparisons also certify all series
truncations and remainders used in them.

## Recomputed claims

From exact decimal rationals `epsilon_R`, `epsilon_I`, and the printed formulas,
recompute `f_KL`, `c_L`, `A`, `Thr`, `P_reg`, `c_T`, `S`, `b_0`, `b_1`, and
`b_T`.  Check every printed coefficient enclosure and all parameter domains.

Check signs and strict margins for:

- `A > P_reg > 0`, `S > 0`, `b_0,b_1 > 0`, `b_T < 0`;
- `b_0-2b_1 > 0`;
- `b_T+(b_1/A)S > 0`;
- `gamma_* - 0.0000687793 > 0`;
- the old/new gain and lifted-gain comparisons;
- every rounded Unique/general running-time base.

Construct the primal point symbolically as

    i_0=tau=0,
    i_1=(A-P_reg)/(A+b_1),
    z=b_1(A-P_reg)/(A+b_1),

and verify the orthant/domain inequalities; the two active primal constraints
are algebraic identities by construction.  Construct the dual point

    y_R=b_1/(A+b_1), y_I=A/(A+b_1)

and verify nonnegativity, `y_R+y_I=1`, both positive dual slacks, and the tight
`i_1` constraint.  Equalities are checked as symbolic rational identities of
the defining expressions, not inferred from rounded optimizer output.

For both printed lifting-root brackets, evaluate

    h_2(delta)+(1-p_*+gamma)delta-gamma

at the exact endpoints and certify opposite strict signs.  Independently check
the derivative/monotonicity conditions on `(0,1/2)`, propagate the brackets to
the lifted gains, and check limiting and safe finite-strength bases.  At the
safe rational separator, certify both branch margins strictly positive.

Finally, reconstruct Scheder's printed Section-6 minimax exactly from

    max{(1-x)/10118 - 1/41391, x/1380}, x >= 0,

derive its intersection and compare it exactly with `1/15218`.  This is kept
separate from the Jiang--Cai theorem certificate because it audits a source
statement, not the new recombination.

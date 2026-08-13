# Robustness of unions of low-codimension affine subspaces

## External statement

Yaroslav Alekseev and Nikita Gaevoy, *New Polynomial-Depth
Res(\(\oplus\)) Lower Bounds*, ECCC TR26-007 (2026), Conjecture 1.4
(repeated as Conjecture 4.2), state the following.  For fixed constants
\(q,r>0\), let \(\Phi_1,\ldots,\Phi_m\) be affine subspaces of
\(\mathbb F_2^n\), each of codimension at most \((\log n)^q\), whose union
has size at least \(2^{n-1}\).  For arbitrary
\(\Phi_i'\subseteq\Phi_i\) satisfying

\[
 |\Phi_i'|\geq (1-n^{-r})|\Phi_i|,
\]

the conjecture asserts the existence of a constant \(c=c(q)>0\) such that

\[
 \left|\bigcup_i\Phi_i'\right|
 \geq (1-n^{-rc})\left|\bigcup_i\Phi_i\right|.
\]

Their Theorems 1.1 and 4.3 use this conjecture (for \(q>1\) and a specified
\(r\)) to obtain size--depth tradeoffs for polynomial-depth
Res(\(\oplus\)) refutations of constrained bit pigeonhole principles.

Primary source: <https://eccc.weizmann.ac.il/report/2026/007/>.

## Classification

**FALSE AS WRITTEN for every fixed \(q>1\) and \(r>0\).**

This classification concerns exactly the quantified combinatorial statement
above.  It does not refute a repaired version with extra hypotheses, nor the
paper's unconditional RevRes(\(\oplus\)) and subquadratic-depth
Res(\(\oplus\)) results.

Epistemic history (2026-08-13): `IDEA -> CONJECTURE` (the assertion that the
external conjecture has a counterexample) `-> COMPUTATIONALLY TESTED -> PROOF
CANDIDATE -> ADVERSARIALLY REVIEWED`.  A blinded validator independently
derived a different private-fiber construction with the same asymptotic
contradiction; see
[`../../../audits/eccc_tr26_007_conjecture_audit_meta.md`](../../../audits/eccc_tr26_007_conjecture_audit_meta.md).
Exact-title/erratum/follow-up searches found no prior public correction or
counterexample, but this was not an exhaustive novelty audit and no novelty
claim is made.  The result remains `UNFORMALIZED` and has not received
external peer review.

## Parametric counterexample candidate

All logarithms below may be taken base two.  Fix \(q>1\) and \(r>0\).  For
all sufficiently large \(n\), choose an integer

\[
 L=\lceil r\log_2 n\rceil.
\]

Then \(2L\leq n\) and \(L\leq(\log n)^q\).  For each
\(S\in\binom{[2L]}{L}\), define the linear (hence affine) subspace

\[
 A_S=\{x\in\mathbb F_2^n:x_i=0\text{ for every }i\in S\}.
\]

Each \(A_S\) has codimension \(L\).  Its union \(U\) consists exactly of
the strings having at least \(L\) zeroes among their first \(2L\)
coordinates.  Symmetry of the binomial distribution gives

\[
 |U|=2^{n-2L}\left(2^{2L-1}+\tfrac12\binom{2L}{L}\right)>2^{n-1}.
\]

For each \(S\), let

\[
 D_S=\{x:\{i\in[2L]:x_i=0\}=S\},\qquad A'_S=A_S\setminus D_S.
\]

The last \(n-2L\) coordinates are free.  Thus

\[
 |D_S|=2^{n-2L},\quad |A_S|=2^{n-L},\quad
 \frac{|D_S|}{|A_S|}=2^{-L}\leq n^{-r}.
\]

A point with exactly \(L\) zeroes in the first \(2L\) coordinates belongs
to exactly one \(A_S\); a point with more than \(L\) such zeroes remains in
every trimmed flat that originally contained it.  Consequently

\[
 U\setminus\bigcup_S A'_S=\bigcup_S D_S
\]

and the removed fraction is

\[
 \frac{\binom{2L}{L}}
 {2^{2L-1}+\frac12\binom{2L}{L}}
 =\Theta(L^{-1/2})=\Theta((\log n)^{-1/2}).
\]

(Choosing \(L=\lfloor(\log n)^q\rfloor\) instead gives
\(\Theta((\log n)^{-q/2})\); either version suffices.)  For every constant
\(c>0\), this loss eventually exceeds \(n^{-rc}\).  Hence no positive
constant \(c(q)\) can satisfy the conjectured conclusion.

## Finite sanity check

For \(L=3\) on the six active coordinates there are \(\binom63=20\)
codimension-three flats.  Their union has 42 points.  Deleting one private
point from each flat removes 20 of those 42 points while deleting only
\(1/8\) of each flat.  Run:

```powershell
python experiments/verify_affine_union_counterexample.py 3
```

The finite example illustrates the overlap mechanism; the asymptotic choice
of \(L\) above is what meets arbitrary fixed \(q>1,r>0\).

## Scope and repair questions

The failure uses an unbounded family of highly overlapping subspaces and
individually private middle-layer points.  Plausible repairs would have to
restrict at least one of:

* overlap multiplicity or the number of subspaces;
* their directions/intersection pattern;
* the permitted subsets \(\Phi_i'\); or
* the deletion rate as a function of codimension.

Whether the structured deletions arising in the paper's Res(\(\oplus\))
application satisfy a narrower true statement remains **UNKNOWN-STATUS** and
is not addressed by this counterexample.

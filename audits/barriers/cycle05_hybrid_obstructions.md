# Barrier audit: Cycle-5 hybrid-routing obstructions (Theorems A, E; conditional C, F)

**Date:** 2026-08-21
**Results audited:** Theorem A (affine hybrid-vanishing), Theorem E
(dense-circle obstruction), and the SEG-conditional Theorems C and F, all in
`research_cycle_05/`.

The mandated questions, answered for this scope:

1. **Does the argument relativize?**  NOT APPLICABLE.  The results are
   finite combinatorial statements about literal subset families on an
   `n`-point ground set; no machine model, oracle access, or diagonalization
   is involved.  There is no oracle-relative version of the statements to
   contrast with.

2. **Would relativization prevent the claimed consequence?**  NOT
   APPLICABLE, as in 1.  The only consequence drawn is the closure of one
   restricted construction route toward O01 (a set-system size question),
   not a complexity-class separation.

3. **Is the method a natural proof (Razborov–Rudich)?**  NO, and the
   framework does not apply: the theorems are not lower bounds against a
   circuit class and define no property of Boolean functions.  They bound
   the acceptance measure of specific set systems.  Largeness and
   constructivity have no referent here.

4. **Constructivity/largeness conditions.**  NOT APPLICABLE (see 3).

5. **Does the argument algebrize?**  NOT APPLICABLE; no algebraic extension
   of an oracle or low-degree polynomial machinery is used.  (The imported
   FLSY interval theorem is itself a probabilistic-combinatorial statement.)

6. **Known oracle, black-box, or magnification barriers.**  None apply to
   finite set-system measure bounds.  The one relevant *methodological*
   barrier is internal to the program: the FLSY worst-to-average Lemma 2.3
   makes `H(P) ≥ 1/poly` sufficient for O01, so any obstruction must rule
   out inverse-polynomial acceptance, not merely full coverage — Theorems
   A/E/C/F are stated to that standard.

7. **Is a hidden assumption equivalent to, or stronger than, the desired
   conclusion?**  CHECKED, NO — with one explicit conditional import:
   Theorems C and F assume Lemma SEG, which is strictly weaker than any
   O01-side statement (it is an upper bound on segment acceptance for the
   *single-order* interval family, a strengthening of the already published
   Theorem 4.4 in scope, not in kind).  Circularity with O01 would require
   SEG to imply something about *all* polynomial families; it does not.
   Theorems A and E import only the published FLSY theorem.

8. **Is the result merely hardness for a restricted model?**  YES, BY
   DESIGN, and the scope is stated in each theorem: restricted classes of
   multi-copy RR unions (affine relative maps; common-reference-dense
   circles; bounded switch depth; two copies).  None of it is a lower bound
   on `N(n)`, none of it says anything about arbitrary 1-balanced-chain
   families, and no Boolean or algebraic complexity consequence is claimed.

**Conclusion.**  No checked known barrier invalidates this route.  As in
Cycle 4, the correct reading is that the classical barrier taxonomy is out
of scope for these finite combinatorial obstructions; this audit records
that determination rather than claiming any barrier was "bypassed".

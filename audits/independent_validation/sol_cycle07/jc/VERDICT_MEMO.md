# Jiang--Cai / Scheder import lane: final verdict memo

Date: 2026-08-27.

## Verdicts

* **JC-CERTIFICATE: VALIDATED.**  Fresh exact-rational/certified-interval
  reconstruction proves the new fixed-point arithmetic, LP certificate,
  lifting roots/margins, Unique base `1.306969597516...<1.306969598`, and safe
  general base `1.307031577931...<1.307031578`.
* **JC-IMPORTS: VALIDATED WITH STATEMENT/DOMAIN REPAIRS.**  The fixed numerical
  points survive, but JC overstates epsilon/Thr ranges, closure notation, and
  fixed-strength provenance; the regular TwoCC coefficient needs the certified
  repair below.
* **EPSILON-R-REPAIR: EPS-R-REPAIR-SOUND.**  C.12 is proved at the exact
  `epsilon_R=0.1024756190168075228998451658`; the claimed whole `.13` range is
  false.
* **SCHEDER-ERRATA: CONFIRMED WITH ADDITIONAL EXACT REPAIR.**  In particular,
  `1/15218`, `256/600`, Definition-68 JUNK2, Section-8.3 DFD, and the
  Section-7.7 DFS/JUNK displays are genuine errors.  Every error affecting the
  new JC frontier has a standalone certified repair with positive slack.
* **SS-LIFTING: VALIDATED WITH EXPLICIT HYPOTHESES.**  JC correctly supplies
  monotonicity/closure omitted from the printed Main-Theorem statement and its
  quantitative two-branch specialization is sound.
* **FIXED-W IMPORT: NOT ESTABLISHED AS STATED.**  The cited Scheder source proves
  the needed estimates for slowly growing `w(n)`, not JC's uniform fixed-`w`
  packaging.  The source-verbatim `w(n)` formulation preserves both `O^*`
  frontier numbers.

## Exact 90th-check disposition

The sole failed Cycle-7 subcheck is `09d`, the inherited terminal
`>=1/15218` minimax step.  Classification:

**source-statement defect with valid repaired claim**.

Exact repair: `31273/475913718 >= 1/15219`; shortfall from `1/15218` is
`43/258659105733`.  This changes the historical unrounded constants, not the
new Jiang--Cai frontier.

## Corrections needed outside this independent-tool directory

Do not edit them during this audit, but any future corrected candidate should:

1. replace the old exact `1/15218` consequence by
   `31273/475913718` (or clean `1/15219`) and update its unrounded lifted-old
   display to `1.307031593710616...` while retaining the safe rounded
   `1.307031594`;
2. state the regular import only at the certified fixed `epsilon_R` (not every
   epsilon through `.13`) and require `Thr<=1/1150`;
3. replace the regular TwoCC damage `.055 epsilon` by a certified safe envelope
   `.05529 epsilon+.001 epsilon^2` (the tau dual slack remains
   `.013391919188...>0`);
4. replace irregular admissibility `[0,1/5]` by a range respecting
   `epsilon<=64/600`, or state only the fixed certified point;
5. either prove the literal uniform fixed-`w` theorem or state the
   source-supported slowly-growing-`w(n)`/`O^*` result;
6. correct Cycle 7's Section-8.3 sum `.2404721` to the exact
   `.240474134270283...`, and upgrade its Section-7.7 item from
   `NON-CERTIFYING` to the certified erratum/repair in the source ledger;
7. retain the actual Definition-31 closure-based `TwoCC` convention.

## Lane conclusion

The Jiang--Cai Stage-V **headline repaired frontier survives independent hostile
validation**, but the literal paper/import statements do not survive unchanged.
The appropriate lane-level disposition is:

**VALIDATED WITH REPAIRS; NOT VALIDATED AS LITERALLY STATED.**

This memo makes no finding on Theorem CR or its corollaries.

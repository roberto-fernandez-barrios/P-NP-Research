# Scope audit: cached-frontier construction-family obstruction

**Date:** 2026-08-13  
**Object:** `research_cycle_02/construction_family_obstruction.md`  
**Audit boundary:** scope, barrier language, and Stop A only. I do not recheck the Catalan formula or asymptotic proof. For mathematical validation I rely on the separate verdict in `audits/cycle02_repair_obstruction_adversarial.md`.

## Verdict

**QUALIFIED PASS.** The report's full prose correctly restricts the result to a frozen process family and explicitly denies an implication for unrestricted `N(n)`. The result can nevertheless be overstated if only its theorem identifier or short name is quoted. Two wording changes are important before canonical integration.

| Possible misreading | Audit disposition |
|---|---|
| The theorem resolves or refutes O01 | **Not supported.** It falsifies one `1-O(1/M)` logarithmic-return claim for one construction family. It neither proves nor disproves `N(n)=n^{O(1)}`. The opening disclaimer and Section 6 say this correctly. |
| The theorem is an mABP lower bound | **Not supported.** Failure of an attempted upper-bound construction for balanced-chain systems gives no mABP lower bound and no separation in algebraic complexity. This non-implication should be stated explicitly; it is presently only implicit through the `N(n)` disclaimer. |
| The theorem rules out every bounded-block construction | **Not supported.** Its formal hypotheses freeze greedy minimization of `|H+s|`, one consumed frontier per step, retention of every other inspected frontier, and a uniformly bounded number of equal ordered blocks. Other selection rules, multi-frontier consumption/reconciliation, sparse state representations, and weaker tail goals are outside the theorem. The opening and Section 6 recognize this, but the short name “bounded-block cached-frontier obstruction” is easy to quote too broadly. |
| Stop A is reached | **Yes, narrowly.** Assuming the separate mathematical validator's PASS, the original stopping rule is met for this precise construction class and precise logarithmic-gap guarantee. It is a stop-and-reassess trigger for this attack, not a theorem about O01 or all bounded-block methods. |

## Main scope hazards

### 1. Rename `CF-O1`

`CF-O1` is visually confusable with the repository target `O01`, especially in summaries or tables stripped of the theorem subtitle. Rename it to something that encodes the failed property, for example:

```text
CF-LOGGAP (greedy single-consumption cached-frontier logarithmic-gap obstruction)
```

This is the single most useful protection against an accidental O01 claim.

### 2. Make the algebraic non-implication explicit

Add one sentence near the first scope disclaimer and repeat it after the theorem:

> This is not an mABP lower bound, a min-partition-rank lower bound, or an algebraic-complexity separation; it only invalidates the stated probabilistic guarantee for the defined construction process.

The logical reason matters: showing that one proposed route to a small balanced-chain system fails does not show that balanced-chain systems, full-rank mABPs, or mABPs in general must be large.

### 3. Do not abbreviate the family to “bounded-block”

When the result is summarized, retain at least these restrictions:

```text
uniformly bounded d + greedy min-|H+s| selection
+ exactly one frontier consumed + all other inspected frontiers cached
+ the specific 1-O(1/M), O(log M)-gap target.
```

“Bounded-block impossibility” alone would be false as a description of the theorem's scope. Even “cached-frontier obstruction” is incomplete unless the greedy single-consumption rule and the failed tail target remain visible.

### 4. State the exact strength of the negative conclusion

The defensible conclusion is that no analysis can establish the **stated** high-confidence logarithmic-return property for the unchanged process because that property is false. It is not that:

- the process succeeds only with negligible probability;
- every inverse-polynomial or weaker return estimate fails;
- every polynomial cover derived from its trajectories is impossible; or
- posterior-aware potentials are useless after the process or target guarantee changes.

Section 6 already contains most of these qualifications. They should survive any executive summary.

## Stop A audit

The Cycle-1 stopping rule in `audits/first_target_selection.md` calls for:

> a checked smallest counterhistory plus a proved obstruction for a precise two-/bounded-block construction class.

The repository has the checked finite counterhistory, and the separate adversarial audit passes the restricted cached-frontier theorem. Therefore Stop A is justified as an **internal research-loop disposition**, with the following canonical wording:

> **Stop A reached for the greedy, uniformly bounded-`d`, single-consumption cached-frontier process and its posted `1-O(1/M)` logarithmic direct-gap guarantee. Stop and reassess this construction family. No broader fixed-`d`, mABP, `N(n)`, or O01 obstruction is claimed.**

Do not shorten this to “Stop A: bounded-block obstruction proved.” That would erase the decisive process and tail restrictions.

The sentence in `research_cycle_02/proof_sat_repair_track.md` saying that the stopping rule is reached “only at a bounded B/C diagnostic” is now stale relative to the separately validated obstruction. It should be replaced by the qualified Stop A wording above when canonical files are integrated. This scope audit does not itself upgrade the theorem beyond its recorded internally reviewed, unformalized status.

## Required integration corrections

1. Rename `CF-O1` to `CF-LOGGAP` or another identifier that cannot be confused with `O01`.
2. Add the explicit “not an mABP lower bound or algebraic separation” sentence.
3. In every summary, name the greedy single-consumption cached-frontier family and the exact `1-O(1/M)` logarithmic-gap conclusion; do not say merely “bounded-block obstruction.”
4. Use the qualified Stop A sentence above and treat it as a reassessment trigger, not completion of the main target.
5. If the independent mathematical audit is now final, update the report's “pending independent adversarial audit” metadata; retain `UNFORMALIZED` and make no novelty or external-validation claim.

## Bottom line

The restricted theorem is a legitimate Stop A outcome for one sharply defined failed construction. It has no direct consequence for O01, unrestricted `N(n)`, mABP lower bounds, or bounded-block methods outside the frozen greedy single-consumption cached-frontier model. The body says most of this correctly; the theorem identifier and abbreviated name need tightening so the qualifications cannot be lost in integration.

# Research Cycle 2: O01 bounded repair-or-obstruction diagnostic

**Cycle dates:** 2026-08-13 through 2026-08-21  
**Target:** O01 only — polynomial-size 1-balanced-chain set systems  
**Outcome:** qualified Stop A reached; O01 remains OPEN and unclaimed  
**Cycle boundary:** no Research Cycle 3 work was begun

## Executive conclusion

The withdrawn two-block process was reconstructed on its actual reveal
filtration, its conditional claims were falsified at the smallest even sizes,
the first four feasible values of `N(n)` were independently certified, and
all requested repair families were separated into actual-filtration control
(A), residual control (B), and total distinct-subset accounting (C).

No positive repair satisfies A+B+C. The cycle stops at this precise negative
endpoint:

> **Stop A reached for the greedy, uniformly bounded-`d`, single-consumption
> cached-frontier process and its posted `1-O(1/M)` logarithmic direct-gap
> guarantee. No broader fixed-`d`, mABP, `N(n)`, or O01 obstruction is
> claimed.**

An independently checked primitive-Dyck subevent gives a first-excursion
probability `Omega_D((log M)^(-3/2))` of exceeding any prescribed
`C log M` cutoff. This is asymptotically larger than `K/M`, so the stated
high-confidence conclusion is false for the frozen process, not merely
unsupported by the withdrawn potential proof.

This result does **not** show that the process has non-noticeable success,
that every weaker tail fails, or that every polynomial use of its trajectories
is impossible. It is not a lower bound on unrestricted `N(n)`, an mABP or
min-partition-rank lower bound, an algebraic separation, a Boolean separation,
or a P-versus-NP result.

## 1. Ground-truth baseline

Fabris, Limaye, Srinivasan, and Yehudayoff (FLSY) prove

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`

for 1-balanced-chain systems and leave the exact complexity open. Primary
source: [ECCC TR26-001](https://eccc.weizmann.ac.il/report/2026/001/),
especially Theorems 1.3 and 1.6, Lemmas 2.3 and 3.2, and Theorem 3.3.

The only located polynomial claim, TR26-043, is not a theorem. Its current
[ECCC record](https://eccc.weizmann.ac.il/report/2026/043/) posts a retraction
note saying Lemma 4.1 lacks the required conditional bound and all results
depend on it; [arXiv:2604.00746](https://arxiv.org/abs/2604.00746) is explicitly
withdrawn. The original v0 PDF was frozen by SHA-256
`B72A0EEDB80AEA50DD3B9ED5C1E69CFD3A717FAB7225EC69F46CFA6C15ECDA0F`.
The FLSY PDF used here had SHA-256
`56F91E2C658DC689DA9F543ACBAF8DD9E127D551CB1F915C76B49001FBA92A4A`.

Fresh exact-title, author, identifier, terminology, citation, conference,
equivalent-DAG, and public-code searches through 2026-08-13 found no public
repair of O01. Because indexes can lag and unpublished work cannot be
excluded, this is recorded as `PRIOR-ART-NOT-FOUND`, not as proof of novelty.
Full search log: [literature_novelty_audit.md](../research_cycle_02/literature_novelty_audit.md).

## 2. Exact process reconstruction and smallest failures

The actual decision-time filtration records consumed values, every inspected
but unconsumed frontier, tie coins, block positions, posterior sign counts,
scale/recursion state, probe order, and emitted-chain order. The unconsumed
frontier cannot be deleted from the filtration after its sign has influenced
an adaptive choice.

TR26-043 v0 is ambiguous at height zero. An eager implementation inspects all
frontiers before resolving the algebraically certain tie; a query-minimal
implementation resolves the tie first and reveals only the selected
frontier. Both semantics were modeled and retained.

| Failed source claim | Exact smallest positive even size | Certificate |
|---|---:|---|
| Lemma 4.1 conditional `p_t<=1/4`, eager comparison | `n=8` | positive-probability atom has `p_t=1/3`; no failure at `n=2,4,6` |
| Lemma 4.1, query-minimal height-zero reveals | `n=10` | failure occurs after a nonzero-height comparison; no smaller failure |
| Lemma 3.3 load martingale, literal complete path | `n=2` | forced post-exhaustion increment |
| Lemma 3.3, both blocks active, eager comparison | `n=4` | conditional drift `+1` |
| Lemma 3.3, both blocks active, query-minimal comparison | `n=6` | nonzero conditional drift |
| Lemma 3.3, strict interior under eager comparison | `n=6` | drift `3/4` |

For eager comparison, a parametric family at `n=2k` conditions the two first
frontiers to be positive and consumes one. At the next boundary,

`p_up=(k-2)/(2k-2)` and `E[Delta D]=k/(2k-2)`.

Thus the conditional upward probability approaches `1/2`, not `1/4`. At
`n=10` this gives `p_up=3/8` and load drift `5/8`. A separate query-minimal
`n=10` history reproduces the earlier `p_up=2/7` counterhistory.

The exact rational enumerator conserves probability mass at every level. For
every even `n<=10`, every two-block prefix-grid subset is reachable under some
balanced coloring and tie history; at `n=10` these are all 36 grid subsets.
Stopping at first block exhaustion reaches 35 of them. Eager and query-minimal
semantics have respectively 9,664 and 9,488 terminal filtration atoms but the
same exact residual distribution; the odd-residual probability is
`997/1792`.

The original multiscale prose does not define one total transition system:
odd residuals have no equal-half split rule, the gap filler is existential
and noncanonical, small initial sizes lack an operational entry case, and a
next-scale inequality uses a residual lower bound not supplied by the
preceding upper bound. The machine reconstruction therefore labels these
states `UNDEFINED` instead of inventing conventions.

Artifacts:

* [true-filtration audit](../research_cycle_02/tr26_043_true_filtration_audit.md);
* [state schema](../research_cycle_02/tr26_043_true_process_state.schema.json)
  and [transition system](../research_cycle_02/tr26_043_v0_transition_system.json);
* [enumerator](../experiments/tr26_043_true_filtration.py),
  [tests](../experiments/test_tr26_043_true_filtration.py), and
  [exact certificates](../certificates/tr26_043_true_filtration_counterexamples.json);
* [independent adversarial audit](../audits/cycle02_true_filtration_adversarial.md)
  and [post-correction PASS disposition](../audits/cycle02_true_filtration_disposition.md).

## 3. Exact finite `N(n)`

Under the FLSY set-system convention, counting both the empty and full sets:

| `n` | balanced colorings | exact `N(n)` | displayed optimum by level |
|---:|---:|---:|---|
| 2 | 2 | **3** | `1,1,1` |
| 4 | 6 | **6** | `1,1,2,1,1` |
| 6 | 20 | **12** | `1,1,3,2,3,1,1` |
| 8 | 70 | **20** | `1,1,4,2,4,2,4,1,1` |

The search used a multicommodity-flow MILP with binary subset selectors and
one compatible Boolean-lattice flow per balanced coloring. Only two proved
symmetries were used: global sign and relabeling one witness chain to the
canonical chain. Equivalent SAT reachability and per-level set-cover models
are recorded in the exact-value report.

An independent standard-library checker does not trust the solver, its dual
bound, flows, symmetry quotient, or witness selection. It verifies every
explicit chain for every signed balanced coloring, exhausts every smaller
level cover, and proves `N(8)>19` with an unsymmetrized search. The decisive
`n=8` search checks 280 level-two branches, 42,840 level-three choices, and
100,800 level-four choices. None reaches all 70 colorings; the maximum is 64.

A third independent set-based implementation and a fresh HiGHS run reproduced
all four values, all level minima, the `n=8` branch histogram, and the
displayed families. No exact value is claimed for `n=10`; the model and an
independent exhaustive lower-bound certificate were not completed there.

Artifacts:

* [exact-value report](../research_cycle_02/exact_balanced_chain_values.md);
* [optimizer](../experiments/balanced_chain_optimize.py) and
  [independent checker](../experiments/check_balanced_chain_certificates.py);
* [families, all coloring witnesses, and lower certificates](../certificates/balanced_chain_exact/README.md);
* [independent adversarial audit](../audits/cycle02_exact_n_adversarial.md).

The finite values are not asymptotic evidence. `N(2)=3` and `N(4)=6` are
routine known facts. No prior public computation of the certified `N(6)` and
`N(8)` values was found, but their novelty status remains `UNCLEAR`.

## 4. Structural information from the optima

Two finite patterns admit general proofs:

1. If a system has a unique singleton `{v}`, it needs at least `n/2`
   selected two-sets incident with `v`.
2. Dually, a unique co-singleton forces at least `n/2` selected
   `(n-2)`-sets whose omitted pairs share its omitted point.

The `n=8` optimum exhibits a one-vertex **connectivity surcharge**: the sums
of independently minimum layer covers total 19, but no such family connects
compatible states for all colorings; one extra middle set gives size 20. The
optimal families are sparse, nonrectangular subset DAGs sharing prefixes
among many ordered perfect matchings, unlike FLSY fixed-order recursion or
the withdrawn full two-prefix grid.

Four precise, unproved construction principles were extracted for future
falsification: a two-anchor star spine, a paired-leaf hierarchy, layer-cover
gluing with an explicit bridge surcharge, and shared matching-state
compression. They are recorded in
[small_system_structure.md](../research_cycle_02/small_system_structure.md).
The numerical fit `N(n)=(n/2)(n/2+1)` for `n=4,6,8` is explicitly rejected as
an unsupported extrapolation.

## 5. Repair-family A/B/C audit

Every candidate was tested separately for:

* **A:** drift/return control on the actual filtration;
* **B:** residual and block-size control; and
* **C:** a polynomial bound on the total distinct subsets across all
  colorings, coins, histories, and recursive executions.

| Candidate | A | B | C | Disposition |
|---|---|---|---|---|
| Posterior-state potential, unchanged process | posted `O(log m)` / `O(1/m)` return conclusion false | old load martingale false; no substitute | conditional for fixed `d` | reject |
| Fresh tuple, consume one/defer rest | posterior forced probability false | linear deferred residual | exponential tie histories | reject |
| Consume every fixed batch | proposed constant drift false; no return theorem | pass | pass for fixed batch size | reject |
| Greedy fixed/bounded-`d`, consume one/cache rest | posted high-confidence logarithmic return false | martingale route false | conditional for fixed `d`; full grid fails for growing `d` | Stop A for frozen direct-gap contract only |
| Fixed/logarithmic-horizon domination | fixed-bias domination false | not established | direct filling fails at useful superlogarithmic horizons | reject |
| Polynomial list of fixed recursive orders | exponentially small good-order measure | pass only on rare event | conditional for the list | restricted fixed-order obstruction |
| Variable absorb/recurse threshold | assumed | reserve arithmetic passes; full transition remains incomplete | compatible | bounded diagnostic only |
| Geometric-log accounting | assumed | assumed power shrink | passes under globally quantified description families | bounded diagnostic only |

No repair satisfies A+B+C. In particular, a measurable posterior potential
cannot prove a false tail; residual control cannot be inferred from a height
calculation; and a polynomial-time adaptive path is not a polynomial set
system unless every distinct reachable subset is counted.

Detailed derivations and exact finite checks:

* [repair track](../research_cycle_02/proof_sat_repair_track.md);
* [repair diagnostics](../research_cycle_02/experiments/check_proof_sat_repairs.py);
* [independent mathematical audit](../audits/cycle02_repair_obstruction_adversarial.md).

## 6. Restricted obstruction reached

Fix `D>=2`. At a scale with `2M` points, choose any `2<=d(M)<=D` dividing
`2M`; split into equal ordered blocks; expose all active frontiers; greedily
consume exactly one minimizing absolute imbalance; retain every unconsumed
inspected frontier; and use any nonanticipating tie policy.

Condition on `E_d`, the event that the initial frontiers all have one sign.
After one consumption there are `d-1` cached bad frontiers. For
`1<=k<=M-d` and `2k+1<2M/d`, the next balanced-band return time satisfies

`Pr[T_bal=2k | E_d]
 >= Cat_(k-1) (M-d)_k (M)_k / (2M-d)_(2k)`,

while `Pr[E_d]=2(M)_d/(2M)_d`. For uniformly bounded `d` and
`k=o(sqrt M)`, the conditional right side is `Theta(k^(-3/2))` uniformly.
Taking `k` just above `C log M/2` gives

`Pr[T_bal>C log M] = Omega_D((log M)^(-3/2)) > K/M`

for all sufficiently large admissible `M`.

The proof is independent of the tie policy because a correcting fresh sign is
the unique minimizer, while a bad fresh sign creates a complete same-sign tie
and leaves `d-1` bad frontiers cached regardless of which one is consumed.
The room condition prevents block exhaustion on the certified primitive-Dyck
word.

Canonical statement and audits:

* [CF-LOGGAP statement and proof](../research_cycle_02/construction_family_obstruction.md);
* [independent adversarial proof audit](../audits/cycle02_repair_obstruction_adversarial.md);
* [independent scope/barrier audit](../audits/cycle02_obstruction_scope_audit.md).

Status: `ADVERSARIALLY REVIEWED; UNFORMALIZED; NOVELTY UNCLEAR`. This is an
internal research result, not an externally validated theorem.

## 7. Failure knowledge and negative findings

The canonical [failure ledger](../failure_knowledge.jsonl) records the exact
structural failure and retry condition for:

* filtration erasure, the conditional-height claim, the load martingale, and
  the incomplete multiscale transition system;
* posterior-state potentials;
* fresh/defer and consume-entire-batch exposure;
* fixed/bounded-`d` greedy cached-frontier steering;
* longer-horizon fixed-bias domination;
* polynomial fixed-order recursive covers; and
* the fixed-threshold residual transition.

Negative literature searches and scope limitations are preserved rather than
converted into novelty or impossibility claims.

## 8. Reproduction and validation

Run from the repository root:

```powershell
python -B experiments/test_tr26_043_true_filtration.py -v
python -B experiments/check_balanced_chain_certificates.py
python -B research_cycle_02/experiments/check_proof_sat_repairs.py
```

The first and third use exact `fractions.Fraction` arithmetic. The second uses
only the Python standard library and reruns the complete finite lower-bound
enumerations. A fresh optimizer reproduction is available through:

```powershell
python -B experiments/balanced_chain_optimize.py --n 2 4 6 8 --time-limit 180 --output-dir <temporary-directory>
```

No Lean artifact was completed. Computational certification and internal
adversarial review are therefore not labeled formal verification.

## 9. Stop disposition

Research Cycle 2 stops under the qualified construction-family alternative A.
O01 remains the current OPEN target, but this cycle does not escalate toward
an O01 proof and does not select a replacement target. The unchanged
single-consumption cached-frontier/logarithmic-direct-fill route should not be
retried. A future authorized cycle could test a rule that reconciles all
revealed frontiers or could reassess the target portfolio, but neither action
has been started here.

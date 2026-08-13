# Research cycle 1: Phase 0 and Phase 1

**Completed:** 2026-08-13
**Scope:** ground-truth reconstruction and target selection only.  No P-versus-
NP proof attack was undertaken.

## Outcome

The cycle reconstructed the relevant circuit, proof-complexity, SAT,
hardness/randomness, algebraic, and meta-complexity frontiers; built a typed
dependency DAG; audited and ranked 25 intermediate targets; shortlisted
exactly five; and selected exactly one first target:

> **O01 — Prove that for every positive even `n` there exists a
> 1-balanced-chain set system on `[n]` of size at most `n^C`, for one absolute
> constant `C`.**

The established bounds are

`Omega(n^2) <= N(n) <= n^{O(log n/log log n)}`.

The sole preprint claiming a polynomial upper bound was withdrawn after a
fatal filtration error.  Independent internal validation found a concrete `n=10`
history refuting the advertised conditional-drift lemma and the separate
block-deviation martingale lemma.  Those counterhistories were adversarially
reviewed within this cycle and exactly checked, but remain `UNFORMALIZED` and
are not external publication claims.  No corrected or independent polynomial
construction was found through the audit date.  O01 therefore remains OPEN.

The next cycle is constrained to a bounded repair-or-obstruction diagnostic
for the withdrawn construction before attempting the general theorem.

## Canonical Phase 0/1 artifacts

* [`../literature/known_results.md`](../literature/known_results.md) — theorem,
  model, uniformity, asymptotic, technique, limitation, dependency, and source
  map.
* [`../literature/barriers.md`](../literature/barriers.md) — relativization,
  natural proofs, algebrization, explicitness/nonuniformity, locality, and
  named method barriers with exact scopes.
* [`../literature/dependency_graph.md`](../literature/dependency_graph.md) —
  typed DAG with `KNOWN`, `OPEN`, `CONJECTURED`, `FALSE`, and
  `UNKNOWN-STATUS` nodes.
* [`../literature/open_problems.md`](../literature/open_problems.md) — 25
  candidates, required estimates, product ranking, already-known audit,
  exactly five shortlisted targets, and exactly one selection.
* [`../audits/first_target_selection.md`](../audits/first_target_selection.md)
  — detailed open-status, consequence, comparison, falsification, proof, and
  verification plan for O01.
* [`../audits/final_integration_disposition.md`](../audits/final_integration_disposition.md)
  — disposition of the three independent final integration audits.
* [`../formal/coverage.md`](../formal/coverage.md) — formal-verification ledger.

Detailed track dossiers remain as research evidence in `literature/drafts/`.

## Exactly five shortlisted targets

1. O01 — polynomial-size 1-balanced-chain systems;
2. O03 — an explicit quadratic disperser with the gate-elimination parameters;
3. O02 — a stronger `CP_2` inequality-space lower bound for `CT_n`;
4. O18 — an independently certified strict PPSZ improvement; and
5. O05 — removal of the proof-size parameter (currently weakenable to proof
   height) from effective regular-Resolution simulation.

Only O01 was selected.

## Important negative findings

1. **Alekseev--Gaevoy Conjecture 1.4/4.2 is false as written according to the
   current internal proof.** Two independently derived internal private-layer
   constructions refute it for every fixed `q>1,r>0`; one uses only
   polynomially many affine subspaces.  The result is adversarially reviewed
   within this cycle and computationally checked, but `UNFORMALIZED`, not
   externally peer reviewed, and not novelty-audited.  It does not refute the
   paper's unconditional results.  See
   [`../theory/conjectures/falsified/ag26_affine_union_robustness.md`](../theory/conjectures/falsified/ag26_affine_union_robustness.md)
   and
   [`../audits/eccc_tr26_007_conjecture_audit_meta.md`](../audits/eccc_tr26_007_conjecture_audit_meta.md).
2. **TR26-043 is not a theorem.** It is withdrawn, and the internally
   adversarially reviewed, `UNFORMALIZED` counterhistory falsifies two posted
   stochastic-process lemmas.  O01 remains open.
3. **Single quadratic-PTF SAT is already nontrivial.** The 2018 open statement
   was closed by later exact #SAT algorithms; it was rejected as a candidate.
4. **The old subquadratic threshold frontier is stale.** CTW 2026 prove
   `n^{2.5-epsilon}` lower bounds for an `E^NP` function for every fixed
   positive `epsilon`.
5. **CTW at `n^{2.5}/polylog n` is not safely classifiable as open.** A
   shrinking-`epsilon` substitution looks plausible for a sufficiently large
   logarithmic exponent, but hidden uniform dependence is unaudited.  Status:
   `UNKNOWN-STATUS`.
6. **The near-quadratic deterministic BP theorem is for MKTP, not MCSP.** The
   source explicitly says its Nechiporuk proof does not transfer.
7. **Monotone perfect matching already has a
   `2^{n^{Omega(1)}}` lower bound.** The live target must ask for
   `2^{Omega(n)}`.

## Independent work split

Independent agents reconstructed and cross-checked:

* Boolean circuits, restricted lower bounds, and known barriers;
* proof complexity and SAT algorithms;
* meta-complexity and hardness magnification;
* the public status of candidate targets; and
* adversarial counterexamples/parameter audits.

The affine-union counterexample was independently re-derived without access
to the first construction.  The balanced-chain target was separately audited
by the proof/SAT and circuit/barrier validators, both of whom tried to prove it
known or ill-posed before recommending it.

Three final read-only integration audits then checked the canonical circuit,
proof/SAT, and meta-complexity claims.  Their corrections and replacements
are recorded in
[`../audits/final_integration_disposition.md`](../audits/final_integration_disposition.md).

## Epistemic status

* No novelty claim is made for the literature synthesis.
* The affine-union result is `ADVERSARIALLY REVIEWED`, not formally verified
  or novelty-audited.
* O01 is OPEN, not a conjecture proved or computationally supported by this
  cycle.
* No result in this cycle separates a standard complexity class.

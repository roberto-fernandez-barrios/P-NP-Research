# P vs NP Research Engine

This repository is a long-horizon theoretical computer science research program.

## Primary rule

Mathematical correctness dominates apparent progress.

Never claim novelty, a theorem, or a complexity separation without the validation required by INITIAL_RESEARCH_MISSION.md.

## Research workflow

Before starting work:

1. Read INITIAL_RESEARCH_MISSION.md.
2. Read RESEARCH_STATE.md.
3. Inspect existing literature, proofs, experiments and audits.

Maintain persistent research state in the repository.

Use subagents for independent tasks whenever useful, especially:

- literature reconstruction;
- theorem verification;
- adversarial review;
- counterexample search;
- barrier analysis;
- independent derivations.

Independent validators must not simply repeat the reasoning of the original proposer.

## Evidence discipline

Prefer primary sources.

Never invent citations.

For every important literature claim, record its source.

Separate strictly:

- known theorem;
- conjecture;
- empirical evidence;
- proof candidate;
- formally verified result;
- novelty-audited result.

## Failure discipline

Do not delete failed approaches.

Record structural failures and counterexamples so they are not rediscovered repeatedly.

## P vs NP

Never autonomously declare P = NP or P != NP solved.

Any apparent resolution must be labeled:

CANDIDATE RESOLUTION REQUIRING EXTERNAL VALIDATION.

## Git

Commit meaningful completed research states.

Do not commit temporary garbage, generated caches or irrelevant files.

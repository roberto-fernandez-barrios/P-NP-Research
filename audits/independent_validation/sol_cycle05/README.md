# SOL Cycle-5 independent validation tools

These tools were written for the final cross-model audit.  They deliberately
do not import the Cycle-5 experiment engines.

## Finite RR enumeration and certificate verification

From the repository root in PowerShell:

```powershell
$auditBuild = Join-Path ([IO.Path]::GetTempPath()) 'sol-cycle05-validation'
New-Item -ItemType Directory -Force -Path $auditBuild | Out-Null

g++ -std=c++20 -O3 -Wall -Wextra -pedantic `
  audits/independent_validation/sol_cycle05/enumerate_rr_failures.cpp `
  -o (Join-Path $auditBuild 'enumerate_rr_failures.exe')

2..24 | Where-Object { $_ % 2 -eq 0 } | ForEach-Object {
  & (Join-Path $auditBuild 'enumerate_rr_failures.exe') --n $_
}

& (Join-Path $auditBuild 'enumerate_rr_failures.exe') --n 22 `
  --dump (Join-Path $auditBuild 'failures_n22.txt')
& (Join-Path $auditBuild 'enumerate_rr_failures.exe') --n 24 `
  --dump (Join-Path $auditBuild 'failures_n24.txt')

python audits/independent_validation/sol_cycle05/verify_finite_claims.py `
  --failure-n22 (Join-Path $auditBuild 'failures_n22.txt') `
  --failure-n24 (Join-Path $auditBuild 'failures_n24.txt')
```

The enumerator tests every normalized balanced word.  The expected rejected
counts for `n=2,4,...,24` are respectively

```text
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 414.
```

The Python verifier checks the committed SHA-256 manifest, literal witness
chains, per-copy rejection, union acceptance, minimum switch count, the
`n=22` canonical example, `n=24` duplicate accounting, the infinity-moving
sample, and the complete `n=22` transposition-distance profile.

## Lean axiom audit

After a clean build of `formal/`, run from that directory:

```powershell
lake env lean ..\audits\independent_validation\sol_cycle05\FormalAxiomAudit.lean
```

The file prints the kernel dependencies of every theorem family credited in
`formal/coverage.md`.  Only Lean/mathlib's documented standard axioms should
appear; it does not expand the repository's formal coverage.

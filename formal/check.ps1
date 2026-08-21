$ErrorActionPreference = 'Stop'

$elanBin = Join-Path $env:USERPROFILE '.elan\bin'
$lean = Join-Path $elanBin 'lean.exe'
$lake = Join-Path $elanBin 'lake.exe'

if (-not (Test-Path -LiteralPath $lean) -or -not (Test-Path -LiteralPath $lake)) {
    throw 'Lean/Elan was not found in the standard per-user installation.'
}

$sourcePath = Join-Path $PSScriptRoot 'BalancedChain.lean'
$source = Get-Content -Raw -LiteralPath $sourcePath
if ($source -match '(?<![A-Za-z0-9_])(axiom|sorry|admit)(?![A-Za-z0-9_])') {
    throw 'Forbidden unproved token found in BalancedChain.lean.'
}

Push-Location $PSScriptRoot
try {
    & $lean --version
    if ($LASTEXITCODE -ne 0) { throw 'lean --version failed.' }
    & $lake --version
    if ($LASTEXITCODE -ne 0) { throw 'lake --version failed.' }
    & $lake build
    if ($LASTEXITCODE -ne 0) { throw 'lake build failed.' }
    Write-Output 'PASS: BalancedChain.lean contains no sorry/axiom/admit and lake build succeeded.'
}
finally {
    Pop-Location
}

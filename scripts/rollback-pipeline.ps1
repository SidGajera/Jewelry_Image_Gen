# One-click pipeline rollback / switch (Windows PowerShell). Safe-versioning rule 3.
#   .\scripts\rollback-pipeline.ps1 legacy
#   .\scripts\rollback-pipeline.ps1 composite-v1
# Sets the active pipeline via config/pipeline_versions.json (env PIPELINE_MODE still
# overrides at runtime). Restores that version's prompt/provider/QC/geometry/
# compositing profile (all stored per-version), then verifies both pipelines import.
# Never edits source and never deletes a version's config.
param([Parameter(Mandatory = $true)][string]$Mode)
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $RepoRoot "tool\backend"
$venv = Join-Path $Backend ".venv\Scripts\python.exe"
if (-not (Test-Path $venv)) {
    Write-Host "No virtualenv - run .\scripts\setup.ps1 first."
    exit 1
}

Push-Location $Backend
try {
    # --set persists the active mode; --verify confirms both versions still import.
    & $venv -m lib.pipeline.mode --set $Mode --verify
    if ($LASTEXITCODE -ne 0) { Write-Host "Rollback failed for mode '$Mode' - investigate."; exit 1 }
    Write-Host "Active pipeline is now '$Mode'. Restart the server to pick it up: .\scripts\start.ps1"
}
finally {
    Pop-Location
}

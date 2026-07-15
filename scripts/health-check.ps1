# Standalone health check (Windows PowerShell) - never spends generation credits.
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $RepoRoot "tool\backend"
$venvPython = Join-Path $Backend ".venv\Scripts\python.exe"

if (Test-Path $venvPython) {
    & $venvPython (Join-Path $Backend "health_check.py")
} else {
    python (Join-Path $Backend "health_check.py")
}
exit $LASTEXITCODE

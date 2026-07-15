# Start the Lucent Carat Lab catalog generator backend (Windows PowerShell).
# Run scripts\setup.ps1 first if you haven't.
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $RepoRoot "tool\backend"
$venvPython = Join-Path $Backend ".venv\Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    Write-Host "No virtualenv found - run .\scripts\setup.ps1 first."
    exit 1
}

Set-Location $Backend
if (-not $env:HOST) { $env:HOST = "127.0.0.1" }
if (-not $env:PORT) { $env:PORT = "8000" }
Write-Host "Starting server at http://$($env:HOST):$($env:PORT) ..."
& (Join-Path $Backend ".venv\Scripts\uvicorn.exe") server:app --host $env:HOST --port $env:PORT

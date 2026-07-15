# One-command setup for the Lucent Carat Lab catalog generator (Windows PowerShell).
# Safe to re-run. Never spends generation credits.
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$Backend = Join-Path $RepoRoot "tool\backend"
$Missing = @()

Write-Host "== Lucent Carat Lab setup =="

# 1. Required software
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) { $python = Get-Command py -ErrorAction SilentlyContinue }
if (-not $python) {
    $Missing += "Python (>=3.10) - install it, then re-run this script"
}

if ($Missing.Count -gt 0) {
    Write-Host "Cannot continue - missing prerequisites:"
    $Missing | ForEach-Object { Write-Host "  - $_" }
    exit 1
}

$pythonExe = $python.Source
Write-Host "Using $pythonExe"

# 2. Virtualenv + dependencies
$venvDir = Join-Path $Backend ".venv"
if (-not (Test-Path $venvDir)) {
    Write-Host "Creating virtualenv..."
    & $pythonExe -m venv $venvDir
}
$venvPython = Join-Path $venvDir "Scripts\python.exe"
& $venvPython -m pip install --quiet --upgrade pip
& $venvPython -m pip install --quiet -r (Join-Path $Backend "requirements.txt")

# 3. .env
$envFile = Join-Path $RepoRoot "tool\.env"
if (-not (Test-Path $envFile)) {
    Write-Host "Copying .env.example -> tool\.env (fill in your keys before generating)"
    Copy-Item (Join-Path $Backend ".env.example") $envFile
}

# 4. Workspace directories
foreach ($d in @("source", "reference", "input", "output", "cache", "temp", "deliveries")) {
    New-Item -ItemType Directory -Force -Path (Join-Path $RepoRoot "workspace\$d") | Out-Null
}
New-Item -ItemType Directory -Force -Path (Join-Path $Backend "jobs") | Out-Null

# 5. Health check (structural only - never calls a provider, never spends credits)
Write-Host ""
& $venvPython (Join-Path $Backend "health_check.py")
$Status = $LASTEXITCODE

Write-Host ""
if ($Status -eq 0) {
    Write-Host "Setup complete. Next: add your keys to tool\.env if you haven't, then run:"
    Write-Host "  .\scripts\start.ps1"
} else {
    Write-Host "Setup finished with structural problems above - fix them and re-run setup.ps1."
}
exit $Status

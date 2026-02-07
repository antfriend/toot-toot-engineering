param(
  [switch]$DryRun,
  [switch]$Verify
)

$ErrorActionPreference = "Stop"

function Invoke-Step($msg, $cmd) {
  Write-Host "[step] $msg"
  if ($DryRun) {
    Write-Host "[dry-run] $cmd"
  } else {
    Invoke-Expression $cmd
  }
}

Invoke-Step "Create venv" "python -m venv .venv"
Invoke-Step "Activate venv" ".\.venv\Scripts\Activate.ps1"
Invoke-Step "Upgrade pip" "python -m pip install --upgrade pip"
Invoke-Step "Install requirements" "pip install -r requirements.txt"

if ($Verify) {
  Write-Host "[verify] Hub health check"
  if (-not $DryRun) {
    try {
      $resp = Invoke-WebRequest -UseBasicParsing http://localhost:8081/health
      Write-Host "[verify] status=$($resp.StatusCode)"
    } catch {
      Write-Host "[verify] failed"; exit 1
    }
  }
}

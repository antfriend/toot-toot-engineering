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

Invoke-Step "Activate venv" ".\.venv\Scripts\Activate.ps1"
Invoke-Step "Start TTN hub v2" "python deliverables/cycle-02/src/windows_hub/ttn_hub_v2.py"

if ($Verify) {
  Write-Host "[verify] open http://localhost:8081/monitor_v2.html"
}

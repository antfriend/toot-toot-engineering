Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$logPath = Join-Path $env:TEMP "tte_monitor.log"
Start-Process -FilePath "python" -ArgumentList "tte_monitor.py" -RedirectStandardOutput $logPath -RedirectStandardError $logPath -WindowStyle Hidden
python tte_agent.py

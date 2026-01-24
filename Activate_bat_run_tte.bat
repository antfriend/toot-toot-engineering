@echo off
setlocal

set "ROOT=%~dp0"
mode con: cols=80 lines=25

where py >nul 2>&1
if errorlevel 1 (
  echo [error] Python launcher "py" not found. Install Python or add it to PATH.
  exit /b 1
)

start "" /b py "%ROOT%tte_monitor.py" > "%TEMP%\tte_monitor.log" 2>&1
py "%ROOT%tte_agent.py"

endlocal

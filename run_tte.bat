@echo off
setlocal

start "" /b python tte_monitor.py > "%TEMP%\tte_monitor.log" 2>&1
python tte_agent.py

endlocal

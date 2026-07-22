@echo off
REM stop.bat — Stop ONLY the services started by start.bat (uses .pids file)
REM IMPORTANT: Only kills PIDs recorded in .pids — never uses taskkill /IM
REM which could accidentally kill other processes on the system.

echo Stopping services...
if exist .pids (
    for /f %%p in (.pids) do (
        taskkill /PID %%p /F >nul 2>&1
        if errorlevel 1 (
            echo   PID %%p not running
        ) else (
            echo   Stopped PID %%p
        )
    )
    del .pids
    echo All services stopped
) else (
    echo No .pids found — services may not be running or were stopped already
)

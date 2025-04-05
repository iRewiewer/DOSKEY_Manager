@echo off
:: Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    :: Restart script as admin
    powershell -Command "Start-Process cmd.exe -ArgumentList '/c \"\"%~f0\"\"' -Verb RunAs"
    exit /b
)

:: Save existing AutoRun value
set "regPath=HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Command Processor"
set "backupFile=%TEMP%\AutoRunBackup.reg"
reg query "%regPath%" /v AutoRun >nul 2>&1
if %errorlevel% equ 0 (
    echo Saving existing AutoRun value...
    reg export "%regPath%" "%backupFile%" /y >nul
    echo AutoRun value saved to: %backupFile%
) else (
    echo No AutoRun entry found to save.
)

:: Delete AutoRun entry
echo Deleting AutoRun entry...
reg delete "%regPath%" /v AutoRun /f >nul 2>&1
if %errorlevel% equ 0 (
    echo AutoRun entry deleted successfully.
) else (
    echo Failed to delete AutoRun entry or it does not exist.
)

:: Schedule re-add on next startup
echo Scheduling re-add of AutoRun entry on next startup...
set "restoreScript=%TEMP%\RestoreAutoRun.bat"
(
    echo @echo off
    echo reg import "%backupFile%"
    echo del "%restoreScript%"
) > "%restoreScript%"
schtasks /create /tn "RestoreAutoRun" /tr "\"%restoreScript%\"" /sc onstart /ru SYSTEM >nul 2>&1
if %errorlevel% equ 0 (
    echo Restore script scheduled to run on next startup.
) else (
    echo Failed to schedule restore script.
)

echo All tasks completed.
pause

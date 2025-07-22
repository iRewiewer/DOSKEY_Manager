@echo off
setlocal

:: Check for Admin Privileges
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Requesting administrative privileges...
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %*", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs"
exit /b

:gotAdmin
if exist "%temp%\getadmin.vbs" del "%temp%\getadmin.vbs"
pushd "%CD%"
cd /d "%~dp0"

:: Delete reg keys
reg delete "HKLM\SOFTWARE\Microsoft\Command Processor" /v AutoRun /f
reg delete "HKLM\SOFTWARE\Microsoft\Command Processor" /v DoskeyManagerPath /f
echo Registry keys removed. Closing in 2 seconds..
timeout 2 >nul

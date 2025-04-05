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

:: Enable AutoRun of DOSKEY_Manager when terminal starts
set "localpath=%~dp0"
set "appname=DOSKEY_Loader.bat"
set "regpath=HKLM\SOFTWARE\Microsoft\Command Processor"

reg add "%regpath%" /v AutoRun /t REG_SZ /d "\"%localpath%%appname%\"" /f
reg add "%regpath%" /v DoskeyManagerPath /t REG_SZ /d "\"%localpath%%appname%\"" /f

echo Configuration complete. Closing in 2 seconds...
timeout 2 >nul

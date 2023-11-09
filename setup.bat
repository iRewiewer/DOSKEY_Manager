@echo off
setlocal

:: Get Admin Privileges ::

>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
  echo Requesting administrative privileges...
  goto UACPrompt
) else ( goto gotAdmin )

:UACPromptcho Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
ech
eo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"
"%temp%\getadmin.vbs" 
exit /b

:gotAdmin
if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )
pushd "%CD%"
CD /D "%~dp0"

:: Enable AutoRun of DOSKEY_Manager when terminal starts ::

set localpath=%~dp0
set appname=DOSKEY_Loader.bat
set ext="\"

reg add "HKLM\SOFTWARE\Microsoft\Command Processor" /v AutoRun /t REG_SZ /d \""%localpath%%appname%%ext%"
reg add "HKLM\SOFTWARE\Microsoft\Command Processor" /f /v DoskeyManagerPath /t REG_SZ /d \""%localpath%%appname%%ext%"

timeout 2 > NUL
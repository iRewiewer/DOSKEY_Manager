@echo off

set doskeyLocalPath=%~dp0
set aliasFile=%TEMP%\doskey_manager_aliases_%RANDOM%_%RANDOM%.bat

if not "%~1"=="" (
    python "%doskeyLocalPath%src\doskey_manager.py" %*
    exit /b %errorlevel%
)

if exist "%doskeyLocalPath%.doskey_manager.disabled" exit /b 0

echo(%CMDCMDLINE% | findstr /i /c:" /c " /c:"/c " >nul
if %errorlevel% equ 0 exit /b 0

python "%doskeyLocalPath%src\doskey_manager.py" startup --alias-output "%aliasFile%"

if exist "%aliasFile%" (
    call "%aliasFile%"
    del "%aliasFile%" >nul 2>&1
)

start "" /b python "%doskeyLocalPath%src\doskey_manager.py" startup-background >nul 2>&1

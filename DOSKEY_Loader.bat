@echo off
cls

:: Variables ::
set localpath=%~dp0

if exist "C:\Program Files\Notepad++\notepad++.exe" (
    set np="C:\Program Files\Notepad++\notepad++.exe"
) else (
    if exist "C:\Program Files (x86)\Notepad++\notepad++.exe" (
        set np="C:\Program Files (x86)\Notepad++\notepad++.exe"
    ) else (
        set np="C:\Windows\notepad.exe"
    )
)

:: Title Sequence ::
type "%localpath%\welcome.txt"
echo.
echo.
echo.
python "%localpath%\changeBackground.py"

:: CMD Settings ::
DOSKEY hcfg="%localpath%\helpcfg.bat"
DOSKEY edit_hcfg=%np% "%localpath%\helpcfg.bat"
DOSKEY cfg=%np% "%localpath%\DOSKEY_Loader.bat"
DOSKEY wcfg=%np% "%localpath%\welcome.txt"
DOSKEY version=echo Version 2.09

:: Aliases ::
DOSKEY ls=dir
DOSKEY clear=cls
DOSKEY mv=move $* %*
DOSKEY cp=copy $* %*
DOSKEY cpy=copy $* %*
DOSKEY pwd=echo^|set /p=%%cd%%^|clip
DOSKEY nc=ncat $* %*
DOSKEY unzip=tar -xf $* %*
DOSKEY cat=type $* %*
DOSKEY rm=del $* %*
DOSKEY np=%np% $* %*
DOSKEY history=echo off $T echo Path to bash history: C:\Users\%username%\.bash_history $T echo. $T echo Bash History: $T type "C:\Users\%username%\.bash_history" $T echo on
DOSKEY bg=python "%localpath%\changeBackground.py" $* %*

:: App Shortcuts ::
DOSKEY viewColors="%localpath%\colors.bat"

:: Notes ::
:: pass arguments - $* %*
:: separate doskey commands - $T
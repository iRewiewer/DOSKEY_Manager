@echo off
cls

:: Variables ::
set doskeyLocalPath=%~dp0
set version=2.38.5

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
type "%doskeyLocalPath%\welcome.txt"
echo.
echo.
echo.
python "%doskeyLocalPath%\changeBackground.py"

:: CMD Settings ::
DOSKEY hcfg="%doskeyLocalPath%\helpcfg.bat"
DOSKEY edit_hcfg=%np% "%doskeyLocalPath%\helpcfg.bat"
DOSKEY cfg=%np% "%doskeyLocalPath%\DOSKEY_Loader.bat"
DOSKEY wcfg=%np% "%doskeyLocalPath%\welcome.txt"
DOSKEY version=echo Version %version%

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
DOSKEY bg=python "%doskeyLocalPath%\changeBackground.py" $* %*

:: App Shortcuts ::
DOSKEY viewColors="%doskeyLocalPath%\colors.bat"

:: Notes ::
:: pass arguments - $* %*
:: separate doskey commands - $T
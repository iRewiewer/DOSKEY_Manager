@echo off
cls

:: Enable enhanced batch capabilities
:: SETLOCAL EnableExtensions EnableDelayedExpansion

:: Variables ::
set doskeyLocalPath=%~dp0
set version=2.4

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
python "%doskeyLocalPath%\display_title.py"
python "%doskeyLocalPath%\change_background.py"

:: CMD Settings ::
DOSKEY help-cfg="%doskeyLocalPath%\helpcfg.bat"
DOSKEY edit-hcfg=%np% "%doskeyLocalPath%\helpcfg.bat"
DOSKEY cfg=%np% "%doskeyLocalPath%\DOSKEY_Loader.bat"
DOSKEY version=echo DOSKEY Manager Version %version%
DOSKEY disable-cfg="%doskeyLocalPath%\disable.bat"

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
DOSKEY startup=explorer "C:\Users\iRewiewer\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"

:: App Shortcuts ::
DOSKEY viewColors="%doskeyLocalPath%\colors.bat"

:: Notes ::
:: pass arguments - $* %*
:: separate doskey commands - $T
@echo off

:: Variables ::
set np="C:\Program Files\Notepad++\notepad++.exe"
set localpath=%~dp0

:: Title Sequence ::
cls
type "%localpath%\welcome.rew"
echo.
echo.
echo.

:: Aliases ::

DOSKEY helpcfg="%localpath%\helpcfg.bat"
DOSKEY edithelpcfg=%np% "%localpath%\helpcfg.bat"
DOSKEY aliascfg=%np% "%localpath%\DOSKEY_Loader.cmd"
DOSKEY welcomecfg=%np% "%localpath%\welcome.rew"

:: Current Hotkeys ::

DOSKEY test=python "C:\Users\%username%\Desktop\test.py"

:: Scripts ::

DOSKEY ls=dir
DOSKEY clear=cls
DOSKEY pwd=echo^|set /p=%%cd%%^|clip
DOSKEY cat=type $* %*

:: Notes ::

:: pass arguments - $* %*
:: separate doskey commands - $T

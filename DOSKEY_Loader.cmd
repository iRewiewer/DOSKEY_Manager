@echo off

:: Variables ::

if exist "C:\Program Files\Notepad++\notepad++.exe" (
set np="C:\Program Files\Notepad++\notepad++.exe"
) else (
set np=notepad
)

set localpath=%~dp0

:: Print Help Section ::

DOSKEY helpcfg="%localpath%\helpcfg.bat"

:: Aliases ::

DOSKEY ls=dir
DOSKEY clear=cls

:: Scripts ::

DOSKEY edithelpcfg=%np% "%localpath%\helpcfg.bat"
DOSKEY aliascfg=%np% "%localpath%\DOSKEY_Loader.cmd"

REM if you wanna pass arguments to a .py file $* %*
DOSKEY test=python "path\to\file\file.py" $* %*

@echo off
reg delete "HKLM\SOFTWARE\Microsoft\Command Processor" /v AutoRun /f
reg delete "HKLM\SOFTWARE\Microsoft\Command Processor" /v DoskeyManagerPath /f
echo Registry keys removed.
pause

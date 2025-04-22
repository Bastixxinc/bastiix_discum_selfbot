@echo off
REM ----------------------------------------
REM \src\core\system\restart_debug.bat
REM \author @bastiix

REM ----------------------------------------

SET MAIN_PY=%%~dp0\..\..\..\main.py
py -3 "%MAIN_PY%" DEBUG
if errorlevel 1 exit /B %%ERRORLEVEL%%
exit /B 0

@echo off
REM ----------------------------------------
REM \src\core\system\restart_debug.bat
REM \author @bastiix
REM ----------------------------------------

SET "SCRIPT_DIR=%~dp0"
SET "MAIN_PY=%SCRIPT_DIR%..\..\..\main.py"
SET "PROJECT_DIR=%SCRIPT_DIR%..\..\.."
SET "VENV_ACT=%PROJECT_DIR%\venv\Scripts\activate.bat"
IF EXIST "%VENV_ACT%" (
    call "%VENV_ACT%"
    SET "PY_CMD=python"
) ELSE (
    where py >nul 2>&1
    IF %ERRORLEVEL%==0 (
        SET "PY_CMD=py -3"
    ) ELSE (
        SET "PY_CMD=python"
    )
)
"%PY_CMD%" "%MAIN_PY%" DEBUG

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Failed to restart the script in debug mode.
    exit /B 1
)

exit /B 0

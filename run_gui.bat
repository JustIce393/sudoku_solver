@echo off
:: Change directory to the folder where this batch file is located
cd /d "%~dp0"

echo Starting Sudoku DLX GUI...
"C:\msys64\mingw64\bin\python.exe" "gui.py"

if %ERRORLEVEL% neq 0 (
    echo.
    echo [ERROR] The application failed to run or crashed.
    echo Please see the error messages above.
    echo.
    pause
)

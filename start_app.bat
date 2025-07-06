@echo off
echo Starting Team Availability Application...
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/upgrade requirements
echo Installing requirements...
pip install -r requirements.txt

REM Run the application
echo Starting application...
python -m src.main

echo.
echo Application closed.
pause

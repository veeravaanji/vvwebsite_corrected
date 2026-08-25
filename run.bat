@echo off
REM Veera Vaanji Martial Arts Academy - Flask Application Startup Script

echo =========================================
echo Veera Vaanji Martial Arts Academy
echo Flask Application Startup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed. Please install Python 3.
    pause
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo [+] Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo [*] Installing dependencies...
pip install -r requirements.txt

REM Initialize database
echo [*] Initializing database...
python -c "from database import create_database; create_database()"

REM Run the Flask application
echo.
echo =========================================
echo [+] Starting Flask Application...
echo =========================================
echo [*] Application will be available at:
echo     http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo =========================================
echo.

python app.py

pause

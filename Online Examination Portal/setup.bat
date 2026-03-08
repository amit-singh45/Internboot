@echo off
REM Online Examination Portal - Setup Script for Windows

echo.
echo =========================================
echo  Online Examination Portal Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/5] Python found: 
python --version

REM Check if venv exists
if exist ".venv" (
    echo [2/5] Virtual environment already exists
) else (
    echo [2/5] Creating virtual environment...
    python -m venv .venv
)

REM Activate venv
echo [3/5] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install Django
echo [4/5] Installing Django...
python -m pip install django --quiet

REM Run migrations
echo [5/5] Setting up database...
python manage.py migrate --quiet

echo.
echo =========================================
echo  Setup Complete!
echo =========================================
echo.
echo Next steps:
echo 1. Activate virtual environment:
echo    .venv\Scripts\activate
echo.
echo 2. Create superuser (admin account):
echo    python manage.py createsuperuser
echo.
echo 3. Run development server:
echo    python manage.py runserver
echo.
echo 4. Open browser and visit:
echo    http://127.0.0.1:8000/
echo.
echo For more information, read README.md
echo.
pause

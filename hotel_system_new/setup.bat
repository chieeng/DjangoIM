@echo off
REM Hotel Management System - Quick Setup Script for Windows

echo.
echo ========================================
echo  Hotel Management System Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [Step 1] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

echo [Step 2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [Step 3] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo [Step 4] Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo Error: Failed to run migrations
    pause
    exit /b 1
)

echo [Step 5] Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo Error: Failed to collect static files
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.
echo You need to create a superuser account.
echo Running: python manage.py createsuperuser
echo.
python manage.py createsuperuser

echo.
echo ========================================
echo  Ready to Run!
echo ========================================
echo.
echo To start the development server, run:
echo   python manage.py runserver
echo.
echo Then access the application at:
echo   http://127.0.0.1:8000/
echo.
echo Admin panel:
echo   http://127.0.0.1:8000/admin/
echo.
pause

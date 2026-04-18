#!/bin/bash
# Hotel Management System - Quick Setup Script for Linux/Mac

echo ""
echo "========================================"
echo "  Hotel Management System Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    exit 1
fi

echo "[Step 1] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo "[Step 2] Activating virtual environment..."
source venv/bin/activate

echo "[Step 3] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[Step 4] Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "Error: Failed to run migrations"
    exit 1
fi

echo "[Step 5] Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "Error: Failed to collect static files"
    exit 1
fi

echo ""
echo "========================================"
echo "  Setup Complete!"
echo "========================================"
echo ""
echo "You need to create a superuser account."
echo "Running: python manage.py createsuperuser"
echo ""
python manage.py createsuperuser

echo ""
echo "========================================"
echo "  Ready to Run!"
echo "========================================"
echo ""
echo "To start the development server, run:"
echo "  python manage.py runserver"
echo ""
echo "Then access the application at:"
echo "  http://127.0.0.1:8000/"
echo ""
echo "Admin panel:"
echo "  http://127.0.0.1:8000/admin/"
echo ""

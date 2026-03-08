#!/bin/bash

# Online Examination Portal - Setup Script for Linux/Mac

echo ""
echo "========================================="
echo "  Online Examination Portal Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from python.org"
    exit 1
fi

echo "[1/5] Python found:"
python3 --version

# Check if venv exists
if [ -d ".venv" ]; then
    echo "[2/5] Virtual environment already exists"
else
    echo "[2/5] Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate venv
echo "[3/5] Activating virtual environment..."
source .venv/bin/activate

# Install Django
echo "[4/5] Installing Django..."
python -m pip install django --quiet

# Run migrations
echo "[5/5] Setting up database..."
python manage.py migrate --quiet

echo ""
echo "========================================="
echo "  Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Activate virtual environment:"
echo "   source .venv/bin/activate"
echo ""
echo "2. Create superuser (admin account):"
echo "   python manage.py createsuperuser"
echo ""
echo "3. Run development server:"
echo "   python manage.py runserver"
echo ""
echo "4. Open browser and visit:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "For more information, read README.md"
echo ""

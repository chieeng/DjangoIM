# Setup Instructions for Hotel Management System

## Quick Start Guide

### Option 1: Using PowerShell (Windows)

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install requirements
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### Option 2: Using Command Prompt (Windows)

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat

# Install requirements
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

### Option 3: Using Git Bash (Windows/Mac/Linux)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/Scripts/activate

# Install requirements
pip install -r requirements.txt

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run development server
python manage.py runserver
```

## After Setup

1. **Access the Application**: Open your browser and go to `http://127.0.0.1:8000/`

2. **Admin Panel**: Go to `http://127.0.0.1:8000/admin/` and login with the superuser credentials you created

3. **Add Sample Data**: 
   - Go to admin panel
   - Add Room Types
   - Add Rooms
   - Add Services
   - Add Service Categories

## Project URLs

- **Home**: http://127.0.0.1:8000/
- **Login**: http://127.0.0.1:8000/accounts/login/
- **Register**: http://127.0.0.1:8000/accounts/register/
- **Rooms**: http://127.0.0.1:8000/rooms/
- **Services**: http://127.0.0.1:8000/services/
- **Admin**: http://127.0.0.1:8000/admin/

## Default Admin User

When you run `python manage.py createsuperuser`, follow these steps:
1. Enter username (e.g., admin)
2. Enter email (e.g., admin@hotel.com)
3. Enter password (make it strong)
4. Confirm password

## Common Commands

```bash
# Stop the server
Ctrl + C

# Deactivate virtual environment
deactivate

# See available commands
python manage.py help

# Check for any issues
python manage.py check

# Create a new app
python manage.py startapp app_name

# Run tests
python manage.py test
```

## Troubleshooting

### Issue: "python: command not found"
- Make sure Python is installed
- Add Python to PATH environment variable

### Issue: "venv: No such file or directory"
- Make sure you're in the project root directory
- Virtual environment might not be created, try again

### Issue: "ModuleNotFoundError"
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Issue: Database error
- Delete `db.sqlite3` file
- Run `python manage.py migrate` again

## Next Steps

1. Create sample data through admin panel
2. Customize templates in `templates/` folder
3. Add more features as needed
4. Deploy to production when ready

## Support

For detailed information, see README.md

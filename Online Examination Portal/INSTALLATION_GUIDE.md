# 🚀 Installation & Setup Guide

Complete step-by-step guide to set up and run the Online Examination Portal.

## 📋 Table of Contents
1. [System Requirements](#system-requirements)
2. [Quick Start (Automated)](#quick-start-automated)
3. [Manual Installation](#manual-installation)
4. [Verification](#verification)
5. [Running the Server](#running-the-server)
6. [First-Time Configuration](#first-time-configuration)
7. [Troubleshooting](#troubleshooting)

---

## ✅ System Requirements

### Minimum Requirements
- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum
- **Disk Space**: 500 MB
- **OS**: Windows, macOS, or Linux

### Recommended Setup
- **Python**: 3.10+
- **RAM**: 2 GB or higher
- **Disk Space**: 1 GB
- **Browser**: Chrome, Firefox, Safari, or Edge (latest version)

---

## 🟢 Quick Start (Automated)

### On Windows
```bash
# Navigate to project directory
cd "Online Examination Portal"

# Run setup script
setup.bat
```

### On macOS/Linux
```bash
# Navigate to project directory
cd "Online Examination Portal"

# Make script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

The automated script will:
1. ✓ Create virtual environment
2. ✓ Install Django
3. ✓ Run database migrations
4. ✓ Display next steps

---

## 📝 Manual Installation

### Step 1: Verify Python Installation

**Windows:**
```bash
python --version
```

**macOS/Linux:**
```bash
python3 --version
```

Expected output: `Python 3.8.0` or higher

### Step 2: Navigate to Project Directory

**Windows:**
```bash
cd "Online Examination Portal"
```

**macOS/Linux:**
```bash
cd ~/Desktop/"Online Examination Portal"
```

### Step 3: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

✅ You should see `(venv)` prefix in terminal

### Step 4: Upgrade pip (Optional but Recommended)

**Windows:**
```bash
python -m pip install --upgrade pip
```

**macOS/Linux:**
```bash
python3 -m pip install --upgrade pip
```

### Step 5: Install Dependencies

**Option A: Using requirements.txt**
```bash
pip install -r requirements.txt
```

**Option B: Install Django directly**
```bash
pip install django
```

Verify installation:
```bash
django-admin --version
```

### Step 6: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, exam, sessions
Running migrations:
  ... OK
```

### Step 7: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts:
```
Username: admin
Email address: admin@example.com
Password: ••••••••
Password (again): ••••••••
Superuser created successfully.
```

**Tips:**
- Username: Use something memorable (e.g., `admin`, `superadmin`)
- Email: Any valid email (e.g., `admin@examportal.com`)
- Password: Must be at least 8 characters and not all numeric

---

## ✔️ Verification

### Check Project Setup

```bash
python manage.py check
```

Expected output:
```
System check identified no issues (0 silenced).
```

### Verify Database

```bash
python manage.py showmigrations
```

You should see `[X]` marks next to all migrations (indicating they're applied).

### Test Import

```bash
python -c "import django; print(django.VERSION)"
```

Expected output:
```
(6, 0, 2, 'final', 0)
```

---

## ▶️ Running the Server

### Start Development Server

```bash
python manage.py runserver
```

Expected output:
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

### Access the Application

Open your web browser and visit:
```
http://127.0.0.1:8000/
```

### Using Different Port

If port 8000 is already in use:
```bash
python manage.py runserver 8001
python manage.py runserver 8080
python manage.py runserver 0.0.0.0:8000
```

### Stop Server

Press `Ctrl+C` in the terminal

---

## ⚙️ First-Time Configuration

### 1. Access Admin Panel

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Create some sample exams and questions

### 2. Create Sample Exam

1. Click "Exams" → "Add Exam"
2. Fill in:
   - **Title**: "Python Basics Quiz"
   - **Description**: "Test your Python knowledge"
   - **Duration**: 30 (minutes)
3. Click "Save"

### 3. Add Questions to Exam

1. Click "Questions" → "Add Question"
2. Select the exam you just created
3. Add question text and 4 options
4. Select the correct option
5. Click "Save and add another"

### 4. Test Student Registration

1. Go to: `http://127.0.0.1:8000/register/`
2. Create a new student account
3. Verify email confirmation (if configured)

### 5. Test Exam Attempt

1. Login as student
2. Go to Dashboard
3. Click "Start Exam"
4. Answer questions and submit

---

## 🐛 Troubleshooting

### Python Not Found

**Error**: `python: command not found` or `'python' is not recognized`

**Solution**:
```bash
# Windows - Use full path
C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\python.exe

# macOS/Linux - Use python3
python3 manage.py runserver
```

### Virtual Environment Not Activating

**Windows:**
```bash
# PowerShell error? Use Command Prompt instead
cmd
cd "Online Examination Portal"
venv\Scripts\activate
```

**macOS/Linux:**
```bash
# Make sure you're in the correct directory
source ./venv/bin/activate
```

### Django Not Installed

```bash
# Verify virtual environment is activated (should see (venv) prefix)
pip install django
```

### Port Already in Use

```bash
# Use different port
python manage.py runserver 8001

# Or on all IPs
python manage.py runserver 0.0.0.0:8000
```

### Database Locked

```bash
# Delete database and start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading

```bash
python manage.py collectstatic
```

### Template Not Found

Verify `exam/templates/` directory exists with all HTML files

### Module Import Error

```bash
# Verify INSTALLED_APPS in settings.py includes 'exam'
# Reinstall requirements
pip install -r requirements.txt
```

### Superuser Password Forgotten

```bash
# Create a new superuser
python manage.py createsuperuser

# Or change existing superuser password
python manage.py changepassword admin
```

### Permission Denied Error

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Memory Issues

Close other applications and try again. If persistent:
```bash
# Use less memory intensive approach
python manage.py runserver --nothreading
```

---

## 📚 Additional Resources

### Project Documentation
- [README.md](README.md) - Project overview
- [FEATURES.md](FEATURES.md) - Detailed feature list
- [API_GUIDE.md](API_GUIDE.md) - API reference

### Django Documentation
- [Django Official Docs](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/6.0/intro/)
- [Django Models](https://docs.djangoproject.com/en/6.0/topics/db/models/)

### Bootstrap Documentation
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.0/)
- [Bootstrap Components](https://getbootstrap.com/docs/5.0/components/)

---

## ✅ Post-Installation Checklist

- [ ] Python installed (version 3.8+)
- [ ] Virtual environment created and activated
- [ ] Django installed
- [ ] Database migrations applied
- [ ] Superuser account created
- [ ] Development server runs without errors
- [ ] Admin panel accessible at `/admin/`
- [ ] Registration page works
- [ ] Can create sample exam
- [ ] Can login and view dashboard

---

## 🎯 Next Steps

1. **Create Sample Data**
   - Add exams and questions via Django admin
   - Create test student accounts

2. **Test All Features**
   - Test registration and login
   - Attempt an exam
   - View results and leaderboard

3. **Customize (Optional)**
   - Modify colors in CSS
   - Add logo/branding
   - Adjust timer duration

4. **Deploy (When Ready)**
   - Move to production server
   - Configure proper database
   - Set up SSL/HTTPS
   - Configure email backend

---

## 📞 Support

If you encounter issues:

1. **Check Logs**
   ```bash
   # Django logs appear in terminal during runserver
   ```

2. **Verify Configuration**
   ```bash
   python manage.py check
   ```

3. **Check Django Documentation**
   - Search official Django docs
   - Check Stack Overflow

4. **Review Project README**
   - Contains troubleshooting section
   - Includes common issues and solutions

---

**Congratulations! 🎉 Your Online Examination Portal is ready to use.**

For questions or issues, refer to the README.md file or check the Django documentation.

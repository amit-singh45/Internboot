# ⚡ Quick Start Guide

Get the Online Examination Portal up and running in 5 minutes!

## 🚀 Ultra Quick Start (Copy-Paste)

### Windows Command Prompt

```bash
cd "Online Examination Portal"
python -m venv venv
venv\Scripts\activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit: `http://127.0.0.1:8000/`

### macOS/Linux Terminal

```bash
cd "Online Examination Portal"
python3 -m venv venv
source venv/bin/activate
pip install django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then visit: `http://127.0.0.1:8000/`

---

## 📋 Step-by-Step (5 Minutes)

### 1️⃣ Open Terminal/Command Prompt (30 seconds)

**Windows**: Press `Win+R`, type `cmd`, press Enter

**macOS**: Press `Cmd+Space`, type `terminal`, press Enter

**Linux**: Press `Ctrl+Alt+T`

### 2️⃣ Navigate to Project (10 seconds)

```bash
cd "Online Examination Portal"
```

### 3️⃣ Create Virtual Environment (20 seconds)

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

✅ You should see `(venv)` in your terminal

### 4️⃣ Install Django (20 seconds)

```bash
pip install django
```

### 5️⃣ Setup Database (20 seconds)

```bash
python manage.py migrate
```

### 6️⃣ Create Admin Account (1 minute)

```bash
python manage.py createsuperuser
```

When prompted, enter:
- **Username**: `admin`
- **Email**: `admin@exam.com`
- **Password**: Any secure password (e.g., `Test@1234`)

### 7️⃣ Start Server (10 seconds)

```bash
python manage.py runserver
```

Look for:
```
Starting development server at http://127.0.0.1:8000/
```

### 8️⃣ Open in Browser (10 seconds)

Visit: `http://127.0.0.1:8000/`

---

## 🎯 First Actions (2 Minutes)

### 1. Create Sample Exam

1. Go to: `http://127.0.0.1:8000/admin/`
2. Login with username: `admin`
3. Click "Exams" → "Add Exam"
4. Fill in:
   - **Title**: "Python Quiz"
   - **Description**: "Test your Python knowledge"
   - **Duration**: 10 (minutes)
5. Click "Save"

### 2. Add Questions

1. Click "Questions" → "Add Question"
2. Select your exam
3. Add a question: "What is Python?"
4. Add 4 options:
   - A) Programming language ← **Mark as correct**
   - B) Snake
   - C) Movie
   - D) None
5. Click "Save and add another"
6. Add 2-3 more questions

### 3. Test as Student

1. Go to: `http://127.0.0.1:8000/register/`
2. Create account: 
   - Username: `student1`
   - Password: `Test@1234`
3. Click "Start Exam"
4. Answer questions and submit
5. View your results!

---

## 🔗 Important URLs

| Purpose | URL |
|---------|-----|
| Home | `http://localhost:8000/` |
| Register | `http://localhost:8000/register/` |
| Login | `http://localhost:8000/login/` |
| Dashboard | `http://localhost:8000/dashboard/` |
| Admin Panel | `http://localhost:8000/admin/` |
| Leaderboard | `http://localhost:8000/leaderboard/` |

---

## 💡 Pro Tips

### Tip 1: Keep Server Running
Don't close terminal while using the app. To stop:
```bash
Ctrl+C
```

### Tip 2: Create Multiple Users
Test with different student accounts to populate leaderboard.

### Tip 3: Different Port
If 8000 is busy:
```bash
python manage.py runserver 8080
```

### Tip 4: Create Exam from CLI
```bash
python manage.py shell
>>> from exam.models import Exam
>>> Exam.objects.create(
...     title="Java Quiz",
...     description="Test Java knowledge",
...     duration=15
... )
```

### Tip 5: View Database
```bash
python manage.py dbshell
sqlite> SELECT * FROM exam_exam;
```

---

## ❌ Troubleshooting Quick Fixes

### "Python not found"
```bash
# Use full path or try python3
python3 --version
```

### "Virtual environment won't activate"
```bash
# Windows - Try Command Prompt instead of PowerShell
cmd
python -m venv venv
venv\Scripts\activate
```

### "Django not installed"
```bash
pip install django
```

### "Port 8000 already in use"
```bash
python manage.py runserver 8080
```

### "Database locked"
```bash
rm db.sqlite3
python manage.py migrate
```

---

## ✅ Verification Checklist

- [ ] Terminal shows `(venv)` prefix
- [ ] Django check: `python manage.py check` returns "0 issues"
- [ ] Server starts without errors
- [ ] Can access admin panel at `/admin/`
- [ ] Can register new user
- [ ] Can create exam
- [ ] Can take exam
- [ ] Can view results

---

## 🎓 Next Steps

1. **Explore Admin Panel** - Create more exams and questions
2. **Read README.md** - Full project documentation
3. **Check FEATURES.md** - Complete feature list
4. **Customize UI** - Add your own styling
5. **Add More Data** - Create comprehensive exam database
6. **Deploy** - When ready, move to production

---

## 📚 Quick Help

**Forgot admin password?**
```bash
python manage.py changepassword admin
```

**Reset everything?**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

**Need more questions added?**
Go to admin panel and click "Add Question"

**Want to backup data?**
```bash
cp db.sqlite3 db.sqlite3.backup
```

---

## 🎯 That's It! 🎉

You now have a fully functional Online Examination Portal!

**Happy Exam Taking!** 📚✨

For detailed docs, see:
- `README.md` - Full documentation
- `INSTALLATION_GUIDE.md` - Detailed setup
- `FEATURES.md` - Complete feature list

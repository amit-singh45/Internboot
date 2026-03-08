# 📚 Online Examination Portal

A full-stack web application built with Django for conducting online examinations with features like MCQ-based exams, automatic scoring, and a leaderboard system.

## 🎯 Project Overview

The Online Examination Portal is a comprehensive e-learning platform that enables institutions to conduct secure online examinations. It provides a user-friendly interface for students to take exams and administrators to manage the examination process.

## ✨ Features

### Core Features
- **Student Registration & Authentication** - Secure registration and login system
- **Exam Management** - Admins can create and manage exams
- **MCQ-Based Exams** - Multiple Choice Questions with 4 options
- **Timer-Based Exam** - Countdown timer with auto-submission
- **Automatic Score Calculation** - Real-time score and percentage calculation
- **Result Dashboard** - Detailed results with correct answers
- **Leaderboard System** - Top 10 performers ranked by score
- **Role-Based Access Control** - Separate dashboards for students and admins
- **Responsive Bootstrap 5 UI** - Mobile-friendly design

### Advanced Features
- Attempt history and tracking
- Exam duration management
- Admin analytics dashboard
- Detailed question review after submission
- Performance metrics and statistics
- Professional and intuitive UI/UX

## 🛠️ Tech Stack

- **Backend**: Django 6.0.2 (Python)
- **Database**: SQLite3
- **Frontend**: Bootstrap 5
- **JavaScript**: Vanilla JavaScript (Timer functionality)
- **Server**: Django Development Server / Gunicorn

## 📋 Requirements

- Python 3.8 or higher
- pip (Python package manager)
- Virtual Environment (recommended)

## 🚀 Installation Guide

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd examportal

# Or if downloaded as zip
cd "Online Examination Portal"
```

### Step 2: Create Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install django
```

The project structure is already created. If you need to recreate it from scratch:

```bash
django-admin startproject examportal .
python manage.py startapp exam
```

### Step 4: Configure Database

The project uses SQLite which is already configured. Run migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: (Enter your choice)
- Email: (Enter your email)
- Password: (Enter a strong password)

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## 📱 Usage Instructions

### For Students

1. **Register**: Go to `/register/` and create a new account
2. **Login**: Use your credentials to login at `/login/`
3. **Dashboard**: View available exams and previous results
4. **Start Exam**: Click "Start Exam" button on any available exam
5. **Answer Questions**: Select one answer for each MCQ (auto-saves)
6. **Submit**: Click "Submit Exam" or let timer auto-submit
7. **View Results**: See your score, percentage, and correct answers
8. **Leaderboard**: Check your rank among top performers

### For Admins

1. **Login**: Use superuser credentials at `/admin/`
2. **Create Exam**: Go to Django Admin > Exams > Add Exam
   - Enter Title, Description, Duration (in minutes)
3. **Add Questions**: While creating exam or from Questions section
   - Add question text and 4 options
   - Select the correct option (1-4)
4. **Monitor Results**: View student attempts and scores in Results section
5. **Analytics**: Check admin dashboard for statistics at `/admin-dashboard/`

## 🔐 Security Features

- CSRF Protection enabled
- Login Required decorators on protected routes
- Role-based access control (Admin/Student)
- Password hashing with Django authentication
- SQL injection prevention with ORM
- Form validation on both client and server side
- Secure session management

## 📊 Database Models

### Exam Model
```python
- title: CharField
- description: TextField
- duration: IntegerField (minutes)
- created_at: DateTimeField
```

### Question Model
```python
- exam: ForeignKey(Exam)
- question_text: TextField
- option1-4: CharField
- correct_option: IntegerField (1-4)
```

### Result Model
```python
- user: ForeignKey(User)
- exam: ForeignKey(Exam)
- score: IntegerField
- percentage: FloatField
- timestamp: DateTimeField
```

## 🌐 URL Structure

| URL | Purpose |
|-----|---------|
| `/register/` | Student registration |
| `/login/` | Student login |
| `/logout/` | Logout user |
| `/dashboard/` | Student dashboard |
| `/exam/<id>/` | Start exam |
| `/exam/<id>/submit/` | Submit exam |
| `/result/<id>/` | View result |
| `/leaderboard/` | View top performers |
| `/admin-dashboard/` | Admin dashboard |
| `/admin/` | Django admin panel |

## 🎨 UI Components

- **Responsive Navigation Bar** with user menu
- **Dashboard Cards** for exam listing
- **Progress Bars** for score visualization
- **Countdown Timer** with color warnings
- **MCQ Radio Buttons** with hover effects
- **Result Summary Cards** with statistics
- **Leaderboard Table** with rankings
- **Alert Messages** for user feedback

## 📸 Screenshots/Demo Workflow

1. **Registration Page** - Clean form with validation
2. **Login Page** - Simple username/password form
3. **Student Dashboard** - Lists exams and previous results
4. **Exam Page** - Questions with timer and progress
5. **Result Page** - Score, percentage, and detailed review
6. **Leaderboard** - Top 10 students with rankings
7. **Admin Dashboard** - Statistics and management options

## ⚙️ Configuration

### Settings
Edit `examportal/settings.py`:
- `DEBUG = True` (Change to False in production)
- `ALLOWED_HOSTS` (Add your domain in production)
- `INSTALLED_APPS` (Already configured with 'exam' app)
- `DATABASES` (SQLite configured by default)

### Static Files
Create a `static/` directory in project root:
```
examportal/
├── static/
│   ├── css/
│   └── js/
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
python manage.py runserver 8001
```

### Database Errors
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
```

### Static Files Not Loading
```bash
python manage.py collectstatic
```

### ModuleNotFoundError
Ensure Django is installed:
```bash
pip install django
```

## 🚀 Deployment Guide

### For Production:
1. Set `DEBUG = False` in settings.py
2. Add domain to `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL recommended)
4. Use Gunicorn or similar WSGI server
5. Configure secure HTTPS
6. Set up environment variables for sensitive data
7. Use a reverse proxy (Nginx/Apache)

### Using Gunicorn:
```bash
pip install gunicorn
gunicorn examportal.wsgi
```

## 📚 Future Enhancements

- [ ] Email notifications for exam results
- [ ] User profile customization
- [ ] Exam attempts limiting
- [ ] Negative marking system
- [ ] Question shuffling
- [ ] Code/Writing based questions
- [ ] Real-time notifications
- [ ] Video exam monitoring
- [ ] Advanced analytics and reports
- [ ] Mobile native app
- [ ] Exam scheduling
- [ ] Question bank management
- [ ] Answer key management
- [ ] Certificates generation

## 🤝 Contributing

To contribute to this project:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Developer Information

**Created**: March 2026
**Version**: 1.0.0
**Status**: Production Ready

## 📞 Support

For issues or questions:
- Check the documentation
- Review the code comments
- Check Django official documentation
- Submit an issue on repository

## ✅ Checklist for First-Time Setup

- [ ] Install Django
- [ ] Create Django project and app
- [ ] Configure INSTALLED_APPS
- [ ] Create models
- [ ] Create forms
- [ ] Create views
- [ ] Create URLs
- [ ] Create templates
- [ ] Register in admin
- [ ] Run makemigrations
- [ ] Run migrate
- [ ] Create superuser
- [ ] Test registration
- [ ] Test exam creation
- [ ] Test exam attempt
- [ ] Test results page
- [ ] Test leaderboard
- [ ] Test admin dashboard

## 🎓 Learning Outcomes

This project teaches:
- Django project structure and best practices
- Models, Views, and Templates (MVT) architecture
- Django ORM and database relationships
- Form handling and validation
- User authentication and authorization
- Bootstrap responsive design
- JavaScript timer implementation
- Admin interface customization
- Static file management
- Template inheritance

---

**Happy Learning! 🚀**

For the latest updates, visit the project repository.

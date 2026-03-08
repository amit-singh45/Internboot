# ConnectHub

A modern Instagram-inspired Social Media Web Application built using Django.

Developed by Amit Kumar.

---

## 🚀 Project Overview

ConnectHub is a full-stack social media platform that allows users to create accounts, share posts, follow other users, like posts with animated effects, receive notifications, and explore content through a personalized feed.

The application features a modern UI inspired by Instagram with smooth animations and responsive design.

---

## ✨ Key Features

### 🔐 Authentication System
- User registration
- Secure login/logout
- Profile management
- Edit profile with profile picture upload

### 🏠 Home Feed
- Personalized post feed
- Display user profile pictures
- Like button with heart animation
- Comment-ready structure

### ❤️ Like System
- AJAX-based like toggle
- Floating heart animation when post is liked
- Instant UI update without page reload

### 👥 Follow System
- Follow/Unfollow users
- Dynamic follow button updates
- Follower & following count

### 🔔 Notifications
- Like notifications
- Follow notifications
- Unread indicator
- Notification count badge

### 🔍 Search System
- Search users
- Search posts
- Animated results display
- Clean search UI

### 🎨 UI & Animations
- Instagram-inspired clean layout
- Soft gradient background
- Card-based post design
- Hover transitions
- Smooth fade-in animations
- Floating heart animation on like
- Responsive mobile-friendly design

### 🛠 Admin Dashboard
- Custom admin dashboard
- User management
- Post management
- Leaderboard support

---

## 🏗 Tech Stack

**Backend:**
- Python
- Django

**Frontend:**
- HTML5
- CSS3
- Bootstrap
- JavaScript
- AJAX

**Database:**
- SQLite (development)

---

## 📂 Project Structure

- `connecthub/` - Main project directory containing settings and configurations.
- `core/` - Core application handling primary features (posts, likes, follows, etc.).
- `templates/` - HTML templates for the frontend UI.
- `static/` - Static files (CSS, JS, Images).
- `media/` - User-uploaded media files (profile pictures, post images).
- `manage.py` - Django project management script.

---

## ⚙️ Installation Guide

Follow these steps to set up the project locally:

1. Clone repository
2. Create virtual environment
3. Install dependencies
4. Run migrations
5. Create superuser
6. Start development server

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 🌐 Access Application

Open your browser and navigate to:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👨‍💻 Developer

**Amit Kumar**  
Full Stack Developer  
Django Enthusiast  

---

## 📜 License

MIT License
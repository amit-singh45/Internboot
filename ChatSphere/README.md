# ChatSphere

A modern real-time messaging web application built using Django and WebSockets.

Developed by Amit Kumar

ChatSphere is a fully-featured, production-ready communication platform inspired by the fluid experiences of WhatsApp and Instagram Direct. It provides users with seamless private chats, dynamic group messaging, and disappearing stories. Leveraging Django Channels and WebSockets, the application guarantees instantaneous message delivery and a highly responsive, modern dark-themed user interface.

## Features

- Real-time private messaging
- Group chat support
- Story upload with 24-hour expiry
- Profile management system
- Online/offline status
- Modern animated dark UI
- WebSocket-based live updates
- Secure authentication
- Responsive layout
- Clean and scalable backend architecture

## Tech Stack

**Backend:**
- Django
- Django Channels
- WebSockets

**Frontend:**
- HTML5
- CSS3
- JavaScript
- Bootstrap

**Database:**
- SQLite (Development)

## Installation Guide

Follow these steps to set up the project locally:

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/chatsphere-real-time-chat.git

# Navigate to folder
cd chatsphere-real-time-chat

# Create virtual environment
python -m venv venv

# Activate environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## Usage

- **Register or Login**: Create a new account or sign in to access the platform.
- **Start Private Chat**: Select any user from the sidebar to instantly begin a 1-on-1 real-time conversation.
- **Create Group Chat**: Use the group creation modal to invite multiple members into a shared chatroom.
- **Upload Stories**: Share image updates with your contacts that automatically expire after 24 hours.
- **Manage Profile**: Customize your user avatar, bio, and visual theme preferences.

## Project Structure

```text
ChatSphere/
│
├── chat/
├── templates/
├── static/
├── media/
├── chatsphere/
└── manage.py
```

## Developer

Developed by  
**Amit Kumar**  

Full Stack Developer

## License

This project is licensed under the MIT License.

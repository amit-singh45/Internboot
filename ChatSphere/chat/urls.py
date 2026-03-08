from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_home, name='chat_home'),
    path('chat/user/<int:user_id>/', views.chat_home, name='chat_user'),
    path('chat/group/<int:group_id>/', views.chat_home, name='chat_group'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # API endpoints for Premium Features
    path('api/upload_media/', views.upload_media, name='upload_media'),
    path('api/create_group/', views.create_group, name='create_group'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('api/upload_story/', views.upload_story, name='upload_story'),
]

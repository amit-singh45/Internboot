from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('explore/', views.explore, name='explore'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('about/', views.about, name='about'),
    path('search/', views.search_view, name='search'),
    path('follow-toggle/', views.follow_toggle, name='follow_toggle'),
    path('like-toggle/', views.like_toggle, name='like_toggle'),
]

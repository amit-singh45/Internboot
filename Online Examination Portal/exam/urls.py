from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('exam/<int:exam_id>/', views.start_exam, name='start_exam'),
    path('exam/<int:exam_id>/submit/', views.submit_exam, name='submit_exam'),
    path('result/<int:result_id>/', views.result, name='result'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
]

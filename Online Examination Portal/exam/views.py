from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Avg, Count
from .models import Exam, Question, Result
from .forms import RegistrationForm, LoginForm, ExamAnswerForm
import json


def register(request):
    """Handle student registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def login_view(request):
    """Handle student login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Handle logout"""
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    """Display student dashboard"""
    exams = Exam.objects.all()
    user_results = Result.objects.filter(user=request.user)
    
    # Add attempt status to exams
    for exam in exams:
        exam.attempted = user_results.filter(exam=exam).exists()
        exam.result = user_results.filter(exam=exam).first()
    
    context = {
        'exams': exams,
        'results': user_results,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
def start_exam(request, exam_id):
    """Display exam questions"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user has already attempted
    if Result.objects.filter(user=request.user, exam=exam).exists():
        return redirect('result', result_id=Result.objects.get(user=request.user, exam=exam).id)
    
    questions = exam.questions.all()
    form = ExamAnswerForm(exam)
    
    context = {
        'exam': exam,
        'questions': questions,
        'form': form,
        'duration': exam.duration * 60,  # Convert to seconds
    }
    return render(request, 'exam.html', context)


@login_required(login_url='login')
@require_http_methods(['POST'])
def submit_exam(request, exam_id):
    """Handle exam submission and score calculation"""
    exam = get_object_or_404(Exam, id=exam_id)
    
    # Check if user has already attempted
    if Result.objects.filter(user=request.user, exam=exam).exists():
        return JsonResponse({'error': 'Exam already attempted'}, status=400)
    
    questions = exam.questions.all()
    score = 0
    
    # Calculate score
    for question in questions:
        answer_key = f'question_{question.id}'
        if answer_key in request.POST:
            selected_option = int(request.POST[answer_key])
            if selected_option == question.correct_option:
                score += 1
    
    # Calculate percentage
    total_questions = questions.count()
    percentage = (score / total_questions * 100) if total_questions > 0 else 0
    
    # Save result
    result = Result.objects.create(
        user=request.user,
        exam=exam,
        score=score,
        percentage=percentage
    )
    
    return redirect('result', result_id=result.id)


@login_required(login_url='login')
def result(request, result_id):
    """Display exam result"""
    result = get_object_or_404(Result, id=result_id, user=request.user)
    exam = result.exam
    questions = exam.questions.all()
    
    # Get user's answers from post data (if available)
    user_answers = {}
    if request.method == 'POST':
        for question in questions:
            answer_key = f'question_{question.id}'
            if answer_key in request.POST:
                user_answers[question.id] = int(request.POST[answer_key])
    
    # Calculate accuracy
    correct_count = result.score
    total = questions.count()
    accuracy = (correct_count / total * 100) if total > 0 else 0
    
    context = {
        'result': result,
        'exam': exam,
        'questions': questions,
        'accuracy': accuracy,
        'user_answers': user_answers,
    }
    return render(request, 'result.html', context)


@login_required(login_url='login')
def leaderboard(request):
    """Display leaderboard - top 10 students by score"""
    results = Result.objects.select_related('user', 'exam').order_by('-score', '-percentage')[:10]
    
    context = {
        'results': results,
    }
    return render(request, 'leaderboard.html', context)


@login_required(login_url='login')
def admin_dashboard(request):
    """Admin dashboard - only for superusers"""
    if not request.user.is_superuser:
        return redirect('dashboard')
    
    total_exams = Exam.objects.count()
    total_questions = Question.objects.count()
    total_results = Result.objects.count()
    
    exams = Exam.objects.annotate(
        question_count=Count('questions'),
        attempt_count=Count('results'),
        avg_score=Avg('results__score')
    )
    
    context = {
        'total_exams': total_exams,
        'total_questions': total_questions,
        'total_results': total_results,
        'exams': exams,
    }
    return render(request, 'admin_dashboard.html', context)

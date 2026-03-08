from django.contrib import admin
from .models import Exam, Question, Result


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'duration', 'question_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    ordering = ['-created_at']
    inlines = [QuestionInline]

    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'exam', 'correct_option']
    list_filter = ['exam']
    search_fields = ['question_text', 'exam__title']
    fieldsets = (
        ('Question Details', {
            'fields': ('exam', 'question_text')
        }),
        ('Options', {
            'fields': ('option1', 'option2', 'option3', 'option4')
        }),
        ('Correct Answer', {
            'fields': ('correct_option',)
        }),
    )


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'exam', 'score', 'percentage', 'timestamp']
    list_filter = ['exam', 'timestamp', 'percentage']
    search_fields = ['user__username', 'user__email', 'exam__title']
    ordering = ['-timestamp']
    readonly_fields = ['user', 'exam', 'score', 'percentage', 'timestamp']

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

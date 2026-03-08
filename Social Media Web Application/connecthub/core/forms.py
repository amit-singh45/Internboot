from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Post, Comment

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username','email','first_name','last_name')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('profile_picture','bio','location')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('content','image')
        widgets = {
            'content': forms.Textarea(attrs={'rows':3, 'placeholder':'What\'s happening?'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows':2, 'placeholder':'Write a comment...'}),
        }

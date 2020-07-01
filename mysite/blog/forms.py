from django import forms
from .models import Post, Comment, Post2, Comment2
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from .models import User, Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {
        'password': forms.PasswordInput(),
        }
        fields = ('username', 'email', 'password')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'interest')

class PostForm2(forms.ModelForm):
    class Meta:
        model = Post2
        fields = ('meeting_time','title', 'text',)

class CommentForm2(forms.ModelForm):

    class Meta:
        model = Comment2
        fields = ('text',)
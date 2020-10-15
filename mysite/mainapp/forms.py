from django import forms

from .models import *

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class ArticleForm(forms.ModelForm):
    description = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}))
    name = forms.CharField(required=False)
    class Meta:
        model = Article
        fields = ['image', 'description', 'name']
        labels = {
            'image': 'Изображение',
            'description': 'Описание',
            'name': 'Название',
        }
        help_texts = {
            'name': '',
        }
        error_messages = {
            'name': {
                'max_length': 'this is too long',
            },
        }

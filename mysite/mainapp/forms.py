from django import forms

from .fields import ListTextWidget

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

from .models import Article, HashTag

from django.utils.translation import ugettext as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)


class ArticleForm(forms.ModelForm):
    description = forms.CharField(label='Описание', required=False,
                                  widget=forms.Textarea(attrs={'rows': 1, 'cols': 50}))
    name = forms.CharField(label='Название', required=False)
    url = forms.URLField(required=False,
                         error_messages={
                             "required": "Please enter a valid URL to an image (.jpg .jpeg .png)"
                         },
                         )

    class Meta:
        model = Article
        fields = ['image', 'description', 'name', 'url']
        labels = {
            'image': 'Изображение',
        }
        help_texts = {
            'name': '',
        }
        error_messages = {
            'name': {
                'max_length': 'this is too long',
            },
        }


class HashTagForm(forms.Form):
    name = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        _list = kwargs.pop('data_list', None)
        super(HashTagForm, self).__init__(*args, **kwargs)
        choices = HashTag.objects.values_list('name', flat=True)
        choices.query.set_limits(0, 10)
        _list = choices
        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['name'].widget = ListTextWidget(data_list=_list, name='list')

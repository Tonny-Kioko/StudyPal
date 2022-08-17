from dataclasses import fields
from django.forms import ModelForm
from .models import Game, User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'bio' 'password1', 'password2']


class GameForm(ModelForm):
    class Meta:
        fields = '__all__'
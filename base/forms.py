
from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django import forms

from django.contrib.auth import get_user_model
User = get_user_model()


class MyUserCreationform(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'avatar', 'email', 'bio']
        
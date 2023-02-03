
from django.forms import ModelForm
from .models import Room, User
from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from django import forms


class MyUserCreationform(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = 'name', 'topic','description'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','avatar', 'email','bio']
        
from ast import Not
from email import message
import email
from multiprocessing import context
from pydoc_data.topics import topics
import re
from django.contrib import messages
from django.shortcuts import render, redirect
from . models import User, Game
from . forms import MyUserCreationForm, GameForm
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect ('home')

    if request.method == 'POST':
        email = request.POST.get ('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email =  email)
        except:
            messages.error(request, "Username or Password is Incorrect")
    

        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request, user)
            return redirect ('home')
        
        else:
            messages.error(request, "Oops! User does't Exist")

    context = {'page': page }
    return render (request, 'login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect ('home')

def registerUser(request):
    form = MyUserCreationForm()
    
    context = {'form': form}

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            User.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An Error Occurred in Registration")
        
    return render(request, 'login_register.html', context )

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    games = Game.objects.filter(
        Q(genre__name__icontains=q) |
        Q(name__icontains = q) |
        Q(description__icontains = q)
    )

    games = Game.objects.all()
    game_count = games.count()

    context = {'games': games, 'game_count': game_count}
    return render(request, 'home.html', context)


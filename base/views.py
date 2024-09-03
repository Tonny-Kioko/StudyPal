from base64 import encode
from email import message
from pydoc_data.topics import topics
from django.contrib import messages
from django.shortcuts import render, redirect
from base.models import Room, Topic, Message, User
from base.forms import RoomForm, UserForm,MyUserCreationform
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView

from django.core.cache import cache
from django.views.decorators.cache import cache_page
from studypal.utils import generate_cache_key
from django.conf import settings

CACHE_TTL = 60 * 10


from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

# rooms = [
#    {'id':1, 'name': 'Learning Python With Pals!'},
#   {'id':2, 'name': 'Learning JavaScript With Pals!'},
#   {'id':3, 'name': 'Learning SQL With Pals!'},
#  {'id':4, 'name': 'Learning Frontend Development With Pals!'},
# {'id':5, 'name': 'Learning Design With Pals!'},
# ]

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


@cache_page(CACHE_TTL, key_prefix="login_page")
def loginPage(request):
    page = "login"

    # Skip caching for authenticated users
    if request.user.is_authenticated:
        return redirect("home")

    # Only cache GET requests, no cache for POST
    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect("login")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Username or password is incorrect")
            return redirect("login")

    context = {"page": page}
    return render(request, "login_register.html", context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = MyUserCreationform()

    if request.method == "POST":
        form = MyUserCreationform(request.POST)
        try:
            if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)
                return redirect('home')
            else:
                raise ValidationError("Invalid form data")
        except ValidationError as e:
            messages.error(request, f"An error occurred in registration: {str(e)}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            # Log the error for debugging purposes.
            print(e)
            # You can log the error using Python's built-in logging or external logging libraries.

    return render(request, 'login_register.html', {'form': form})


def home(request):
    q = request.GET.get("q", "")

    # Generate a unique cache key for this view and query
    cache_key = generate_cache_key("home", q)
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data  # Return cached response

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    room_messages = Message.objects.all()

    context = {
        "rooms": rooms,
        "topics": topics,
        "room_count": room_count,
        "room_messages": room_messages,
    }
    response = render(request, "home.html", context)

    cache.set(cache_key, response, timeout=settings.CACHE_TTL)

    return response


def room(request, pk):
  
    cache_key = generate_cache_key("room", pk)
    cached_data = cache.get(cache_key)

    
    if cached_data:
        room, room_messages, participants = cached_data
    else:
        # Fetch room data, messages, and participants if not cached
        room = get_object_or_404(Room, id=pk)
        room_messages = room.message_set.all()
        participants = room.participants.all()

       
        cache.set(
            cache_key, (room, room_messages, participants), timeout=settings.CACHE_TTL
        )

    if request.method == "POST":
       
        Message.objects.create(
            user=request.user, room=room, body=request.POST.get("body")
        )
        room.participants.add(request.user)

        
        cache.delete(cache_key)

        return redirect("room", pk=room.id)

    context = {
        "room": room,
        "room_messages": room_messages,
        "participants": participants,
    }
    return render(request, "room.html", context)


@login_required(login_url='login')
def CreateRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user, 
            topic = topic, 
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
       
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'room_form.html', context) 


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = User.room_set.all()
    room_messages = User.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse("You aren't allowed this operation")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    
    context = {'topics': topics}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id = pk)

    if request.user != room.host:
        return HttpResponse("You aren't allowed this operation")

    if request.method == 'POST':
        room.delete()
        return redirect('home') 

    return render(request, 'delete.html', {'obj': room})

@login_required(login_url='login')
def deletemessage(request, pk):
    message = Message.objects.get(id = pk)

    if request.user != message.user:
        return HttpResponse("You aren't allowed this operation")

    if request.method == 'POST':
        message.delete()
        return redirect('home') 

    return render(request, 'delete.html', {'obj': message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'update-user.html', {'form': form})


def topicsPage(request):

    q = request.GET.get("q") if request.GET.get("q") != None else ""
    cache_key = generate_cache_key("topics_page", q)

    topics = cache.get(cache_key)

    if not topics:
        topics = Topic.objects.filter(name__icontains=q)
        cache.set(cache_key, topics, timeout=settings.CACHE_TTL)
    return render(request, "topics.html", {"topics": topics})


def activityPage(request):
   
    cache_key = generate_cache_key("activity_page", "")

    
    room_messages = cache.get(cache_key)

    if not room_messages:        
        room_messages = Message.objects.all()        
        cache.set(cache_key, room_messages, timeout=settings.CACHE_TTL)
    return render(request, "activity.html", {"room_messages": room_messages})


# def LipaNaMpesa():

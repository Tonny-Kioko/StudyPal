from email.policy import default
from pydoc_data.topics import topics
from pyexpat import model
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.forms import CharField, ModelForm
from allauth.account.forms import SignupForm
from django import forms


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email= models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)


    avatar = models.ImageField(null=True, default="avatar.png", upload_to='StudyPal/images/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
  

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank= True)
    participants = models.ManyToManyField(User, related_name='participants', blank= True )
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return (self.name)



class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return (self.body[0:50])


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, phone_number, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, phone_number, is_admin, password=None):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            
            is_admin=is_admin,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user
    
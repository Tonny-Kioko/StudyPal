from contextlib import nullcontext
from email.policy import default
from pydoc_data.topics import topics
from pyexpat import model
from tkinter.tix import MAX
from unicodedata import name
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin
from django.forms import CharField, ModelForm

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null= True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null = True, default = "")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = []

class Game(models.Model):
    name = models.CharField(max_length=200, null=False)
    description = models.TextField(max_length=MAX, null=True)
    rating = models.PositiveIntegerField(null=True)
    posted = models.DateTimeField(auto_now_add=True)
    genre = models.CharField(max_length=200, null=False)


    class Meta:
        ordering = ['-posted']

    def __str__(self):
        return (self.name)
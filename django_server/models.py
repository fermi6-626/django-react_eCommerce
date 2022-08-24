from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Users(AbstractUser):
    first_name = models.CharField(max_length=25)
    last_name  = models.CharField(max_length=25)
    email = models.EmailField(max_length=25, unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=25, unique=True)
    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

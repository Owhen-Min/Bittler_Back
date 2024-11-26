from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=20, unique=True, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True)
    profile_picture = models.ImageField(upload_to="profilepictures/", null=True, blank=True, default='static/baseprofile.jpeg')
    join_date = models.DateField(auto_now_add=True)
    token = models.IntegerField(default=100)
    first_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)  
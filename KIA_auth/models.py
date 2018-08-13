from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=16, default='user')
    account_number = models.CharField(max_length=16)
    balance = models.IntegerField(default=0)
    phone_number = models.CharField(max_length=11)
    is_restricted = models.BooleanField(default=False)

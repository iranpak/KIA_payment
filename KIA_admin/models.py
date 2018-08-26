from django.db import models
from django.utils import timezone


class SystemCredit(models.Model):
    owner = models.CharField(max_length=24, default='system')
    rial_credit = models.IntegerField(default=0)


class HistoryOfAdminActivities(models.Model):
    type = models.CharField(max_length=32, default='Add user')
    description = models.CharField(max_length=256)
    message = models.CharField(max_length=512, null=True)
    date = models.DateField(default=timezone.now)


class SystemTransactions(models.Model):
    type = models.CharField(max_length=32, default='Charge')
    description = models.CharField(max_length=256)
    date = models.DateField(default=timezone.now)
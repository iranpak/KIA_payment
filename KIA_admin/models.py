from django.db import models

# Create your models here.


class SystemCredit(models.Model):
    owner = models.CharField(max_length=24, default='system')
    rial_credit = models.IntegerField(default=0)


class HistoryOfAdminActivities(models.Model):
    description = models.CharField(max_length=256)


class SystemTransactions(models.Model):
    description = models.CharField(max_length=256)

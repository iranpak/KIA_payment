from django.db import models
import jdatetime
import datetime
from django_jalali.db import models as jmodels


class SystemCredit(models.Model):
    owner = models.CharField(max_length=24, default='system')
    rial_credit = models.IntegerField(default=0)
    dollar_credit = models.IntegerField(default=0)
    euro_credit = models.IntegerField(default=0)
    pound_credit = models.IntegerField(default=0)


class HistoryOfAdminActivities(models.Model):
    type = models.CharField(max_length=32, default='Add user')
    description = models.CharField(max_length=256)
    message = models.CharField(max_length=512, default='')
    date = jmodels.jDateTimeField(default=datetime.datetime.now)


class SystemTransactions(models.Model):
    type = models.CharField(max_length=32, default='Charge')
    description = models.CharField(max_length=256)
    date = jmodels.jDateTimeField(default=datetime.datetime.now)


class ContactUsMessages(models.Model):
    sender_name = models.CharField(max_length=32)
    sender_phone_number = models.CharField(max_length=11)
    sender_email = models.CharField(max_length=64)
    message = models.CharField(max_length=256)

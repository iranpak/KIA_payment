from django.db import models
import jdatetime
from django_jalali.db import models as jmodels
from django.utils import timezone

timezone.get_current_timezone()


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
    date = jmodels.jDateTimeField(default=jdatetime.datetime.now)


class SystemTransactions(models.Model):
    type = models.CharField(max_length=32, default='Charge')
    description = models.CharField(max_length=256)
    date = jmodels.jDateTimeField(default=jdatetime.datetime.now)

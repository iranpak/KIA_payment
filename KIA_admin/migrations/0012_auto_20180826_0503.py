# Generated by Django 2.0.7 on 2018-08-26 05:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('KIA_admin', '0011_auto_20180826_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historyofadminactivities',
            name='date',
            field=models.DateField(default=datetime.datetime(2018, 8, 26, 5, 3, 52, 903278)),
        ),
    ]

# Generated by Django 2.2.13 on 2020-07-11 16:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0003_user_avr_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='birth_date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_run',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='test_passed',
            field=models.SmallIntegerField(default=0, null=True),
        ),
    ]
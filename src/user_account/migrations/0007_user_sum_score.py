# Generated by Django 2.2.13 on 2020-07-11 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0006_remove_user_tests_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='sum_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=20),
        ),
    ]

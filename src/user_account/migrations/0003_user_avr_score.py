# Generated by Django 2.2.13 on 2020-07-11 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0002_user_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avr_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=6),
        ),
    ]

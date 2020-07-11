# Generated by Django 2.2.13 on 2020-07-11 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_account', '0007_user_sum_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='sum_score',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
    ]

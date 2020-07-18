import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


class User(AbstractUser):
    image = models.ImageField(default='default.jpg', upload_to='pics')
    avr_score = models.DecimalField(decimal_places=2, max_digits=6, default=0.0, blank=True)
    birth_date = models.DateField(null=True, blank=True, default=datetime.date.today)
    last_run = models.DateField(null=True, blank=True)
    sum_score = models.DecimalField(decimal_places=2, max_digits=5, default=0.0, blank=True)

    def score(self):
        self.avr_score = self.test_results.aggregate(points=Sum('avr_score')).get('points', 0.0) / self.test_results.count()


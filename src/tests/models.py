from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Topic(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return f'{self.title}'


class Test (models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 20
    LEVEL_CHOICES = (
        (1, 'Basic'),
        (2, 'Middle'),
        (3, 'Advanced'),
    )
    topic = models.ForeignKey(to=Topic, related_name='test', null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=1024, null=True, blank=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=2)
    image = models.ImageField(default='default.png', upload_to='covers')

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    MIN_LIMIT = 3
    MAX_LIMIT = 6
    number = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(MAX_LIMIT)]
    )
    test = models.ForeignKey(to=Test, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=64)
    description = models.TextField(max_length=512, null=True, blank=True)

    def __str__(self):
        return f'{self.text}'


class Variant(models.Model):
    text = models.CharField(max_length=64)
    question = models.ForeignKey(to=Question, related_name='variants', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.text}'


class TestResult(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='test_result', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name='test_result', on_delete=models.CASCADE)
    avr_score = models.DecimalField(max_digits=6, decimal_places=2)


class TestResultDetail(models.Model):
    test_result = models.ForeignKey(to=TestResult, related_name='test_result_details', on_delete=models.CASCADE)
    question = models.ForeignKey(to=Question, related_name='test_result_details', null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(to=Variant, related_name='test_result_details', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)

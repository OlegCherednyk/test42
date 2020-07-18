import datetime

from django.core.management import call_command
from django.test import TestCase

from tests.models import Test, Question


class TestModelTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'global_tests/fixtures/account.json', verbosity=0)
        call_command('loaddata', 'global_tests/fixtures/test.json', verbosity=0)


    def test_questions_count(self):
        test = Test.objects.create(title='Test title')
        questions = Question.objects.create(
            test=test,
            number=1,
            text='text'
        )

        self.assertEqual(test.questions_count(), 1)

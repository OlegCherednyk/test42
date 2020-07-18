from django.core.management import call_command
from django.test import Client
from django.test import TestCase
from django.urls import reverse

from tests.models import Test, Question, TestResult

PK = 1

class BaseFlowTest(TestCase):

    def setUp(self):
        call_command('loaddata', 'global_tests/fixtures/account.json', verbosity=0)
        call_command('loaddata', 'global_tests/fixtures/test.json', verbosity=0)

        self.client = Client()
        self.client.login(username='admin', password='oleg2759064')

    def test_basic_flow(self):
        response = self.client.get(reverse('start', kwargs={'pk': PK}))
        assert response.status_code == 200
        assert 'START' in response.content.decode()

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('next', kwargs={'pk': PK})

        for step in range(1, questions_count+1):
            response = self.client.get(url)
            assert response.status_code == 200
            assert 'Submit' in response.content.decode()
            response = self.client.post(
                path=url,
                data={
                    'answer_1': "1"
                }
            )
            if step < questions_count:
                self.assertRedirects(response, url)
            else:
                assert response.status_code == 200

        assert 'START ANOTHER TEST ▶️' in response.content.decode()

    def test_correct_points(self):
        response = self.client.get(reverse('start', kwargs={'pk': PK}))

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('next', kwargs={'pk': PK})

        for step in range(1, questions_count+1):
            response = self.client.get(url)
            questions = Question.objects.get(number=step)
            variants = [
                variants
                for variants in questions.variants.all()
            ]
            data = {}
            for i, ans in enumerate(variants):
                if ans.is_correct:
                    data[f'answer_{i + 1}'] = "1"

            response = self.client.post(
                path=url,
                data=data
            )
            print(data)

        avr_score_user = TestResult.objects.last().avr_score

        self.assertEqual(questions_count, float(avr_score_user))

    def test_uncorrect_points(self):
        response = self.client.get(reverse('start', kwargs={'pk': PK}))

        test = Test.objects.get(pk=PK)
        questions_count = test.questions_count()
        url = reverse('next', kwargs={'pk': PK})

        for step in range(1, questions_count+1):
            response = self.client.get(url)
            questions = Question.objects.get(number=step)
            variants = [
                variants
                for variants in questions.variants.all()
            ]
            data = {}
            for i, ans in enumerate(variants):
                if not ans.is_correct:
                    data[f'answer_{i + 1}'] = "1"

            response = self.client.post(
                path=url,
                data=data
            )
            print(data)

        avr_score_user = TestResult.objects.last().avr_score

        assert float(avr_score_user) < questions_count

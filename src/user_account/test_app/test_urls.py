from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from django.test import Client


class UrlsAvailabilityTests(TestCase):

    def setUp(self):
        call_command('loaddata', 'global_tests/fixtures/account.json', verbosity=0)
        self.client = Client()

    def test_public_url(self):
        urls = [
            (reverse('index'), 'Login'),
            (reverse('index'), 'Register'),
            (reverse('registration'), 'REGISTER'),
            (reverse('login'), 'Login'),
        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()

    def test_private_urls(self):

        self.client.login(username='admin', password='oleg2759064')

        urls = [
            (reverse('index'), 'Logout'),
            (reverse('index'), 'Profile'),
            (reverse('profile'), 'Profile'),
            (reverse('logout'), 'Logout'),

        ]
        for url, content in urls:
            response = self.client.get(url)
            assert response.status_code == 200
            assert content in response.content.decode()

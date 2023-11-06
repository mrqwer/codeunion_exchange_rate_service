from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class ApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.superUser = User.objects.create_superuser(username="test_admin", password="test_admin")

    def get_tokens(self, username, password):
        url = "http://localhost:8080/auth/jwt/create"
        data = {
            'username': username,
            'password': password
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        tokens = response.data
        return tokens

    def test_authenticated_api_call(self):
        tokens = self.get_tokens('testuser', 'testpassword')

        access_token = tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(reverse("currency-list"))
        self.assertEqual(response.status_code, 200)

    def test_admin_scenario(self):
        tokens = self.get_tokens('test_admin', 'test_admin')
        access_token = tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(reverse("currency-list"))
        self.assertEqual(response.status_code, 200)

    def test_detail_api_call(self):
        tokens = self.get_tokens('testuser', 'testpassword')
        access_token = tokens['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        response = self.client.get(reverse('currency-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

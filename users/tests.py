from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserTests(APITestCase):
    def test_create_user(self):
        url = reverse('user_register')
        data = {"username": "testuser", "balance": "1000.00"}
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "testuser")

    def test_get_user(self):
        user = User.objects.create(username="testuser", balance="1000.00")
        url = reverse('user_detail', args=[user.username])
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "testuser")

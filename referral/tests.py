# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import UserProfile

class UserRegistrationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'password'
        }
        response = self.client.post('/api/user/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

class UserDetailsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test_user', email='test@example.com', password='password')

    def test_user_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/user/details/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test User')
        self.assertEqual(response.data['email'], 'test@example.com')

class ReferralsTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', email='user1@example.com', password='password1')
        self.user2 = User.objects.create_user(username='user2', email='user2@example.com', password='password2')
        self.user2.profile.referred_by = self.user1.profile
        self.user2.profile.save()

    def test_referrals(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get('/api/user/referrals/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

# models.py
from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=20)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

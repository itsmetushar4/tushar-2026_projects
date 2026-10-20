from django.test import TestCase
from rest_framework.test import APIClient
from .models import User

class AuthHealthTests(TestCase):
    def test_health_endpoint_is_public(self):
        response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")

class UserModelTests(TestCase):
    def test_user_defaults_to_patient_role(self):
        user = User.objects.create_user(username="demo-user", password="SafeDemoPass123!")
        self.assertEqual(user.role, User.Role.PATIENT)

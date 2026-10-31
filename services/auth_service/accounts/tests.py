from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from .models import User
import unittest

class AuthHealthTests(TestCase):
    def test_health_endpoint_is_public(self):
        response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")

class UserModelTests(TestCase):
    def test_user_defaults_to_patient_role(self):
        user = User.objects.create_user(username="demo-user", password="SafeDemoPass123!")
        self.assertEqual(user.role, User.Role.PATIENT)

    def test_superuser_defaults_to_admin_role(self):
        user = User.objects.create_superuser(
            username="root-user", email="root@hms.local", password="SafeDemoPass123!"
        )
        self.assertEqual(user.role, User.Role.ADMIN)

@unittest.skipUnless(settings.API_DOCS_ENABLED, "API docs are only routed when API_DOCS_ENABLED=1")
class ApiDocsTests(TestCase):
    def test_schema_contains_auth_paths_and_bearer_scheme(self):
        response = APIClient().get("/api/schema/", HTTP_ACCEPT="application/vnd.oai.openapi+json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("BearerAuth", response.data["components"]["securitySchemes"])
        self.assertIn("/api/auth/token/", response.data["paths"])

    def test_swagger_ui_is_served(self):
        response = APIClient().get("/api/docs/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "swagger-ui")


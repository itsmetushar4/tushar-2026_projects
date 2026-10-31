import time
import unittest
import uuid

import jwt as pyjwt
from django.conf import settings
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from .models import Patient

API = "/api/patients/"


def bearer(role=None, user_id=None, username="tester", secret=None):
    user_id = str(user_id or uuid.uuid4())
    if secret is not None:
        payload = {
            "token_type": "access",
            "exp": int(time.time()) + 300,
            "jti": "test-jti",
            "user_id": user_id,
            "username": username,
        }
        if role:
            payload["role"] = role
        token = pyjwt.encode(payload, secret, algorithm="HS256")
    else:
        token = AccessToken()
        token["user_id"] = user_id
        token["username"] = username
        if role:
            token["role"] = role
        token = str(token)
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


class HealthTests(TestCase):
    def test_health_endpoint_is_public(self):
        response = APIClient().get("/api/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "ok")


class AuthenticationTests(TestCase):
    def test_request_without_token_is_unauthorized(self):
        response = APIClient().get(API)
        self.assertEqual(response.status_code, 401)

    def test_missing_token_response_explains_how_to_authenticate(self):
        response = APIClient().post(API, {}, format="json")
        self.assertEqual(response.status_code, 401)
        self.assertIn("Authorization: Bearer", response.data["detail"])

    def test_token_without_role_claim_is_rejected(self):
        response = APIClient().get(API + "me/", **bearer(role=None))
        self.assertEqual(response.status_code, 401)

    def test_token_signed_with_wrong_secret_is_rejected(self):
        headers = bearer(role="receptionist", secret="some-other-secret")
        response = APIClient().get(API, **headers)
        self.assertEqual(response.status_code, 401)


class StaffAuthorizationTests(TestCase):
    def test_receptionist_creates_patient_with_generated_mrn(self):
        response = APIClient().post(
            API,
            {"first_name": "Asha", "last_name": "Kumar", "phone": "+911234567890"},
            format="json",
            **bearer(role="receptionist"),
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data["medical_record_number"].startswith("MRN-"))
        self.assertIsNotNone(response.data["id"])

    def test_each_patient_gets_a_unique_mrn(self):
        client = APIClient()
        headers = bearer(role="receptionist")
        first = client.post(API, {"first_name": "A", "last_name": "B"}, format="json", **headers)
        second = client.post(API, {"first_name": "C", "last_name": "D"}, format="json", **headers)
        self.assertNotEqual(
            first.data["medical_record_number"], second.data["medical_record_number"]
        )

    def test_patient_role_cannot_list_or_create(self):
        client = APIClient()
        headers = bearer(role="patient")
        self.assertEqual(client.get(API, **headers).status_code, 403)
        self.assertEqual(
            client.post(API, {"first_name": "X", "last_name": "Y"}, format="json", **headers).status_code,
            403,
        )

    def test_doctor_can_list(self):
        response = APIClient().get(API, **bearer(role="doctor"))
        self.assertEqual(response.status_code, 200)

    def test_invalid_phone_is_rejected(self):
        response = APIClient().post(
            API,
            {"first_name": "Bad", "last_name": "Phone", "phone": "not-a-number"},
            format="json",
            **bearer(role="receptionist"),
        )
        self.assertEqual(response.status_code, 400)


class OwnerAccessTests(TestCase):
    def setUp(self):
        self.owner_id = uuid.uuid4()
        self.other_id = uuid.uuid4()
        self.mine = Patient.objects.create(
            first_name="Mine", last_name="Owner", auth_user_id=self.owner_id
        )
        self.theirs = Patient.objects.create(
            first_name="Their", last_name="Record", auth_user_id=self.other_id
        )

    def test_owner_can_read_own_record(self):
        response = APIClient().get(f"{API}{self.mine.id}/", **bearer(role="patient", user_id=self.owner_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.mine.id))

    def test_owner_cannot_read_other_record(self):
        response = APIClient().get(f"{API}{self.theirs.id}/", **bearer(role="patient", user_id=self.owner_id))
        self.assertEqual(response.status_code, 403)

    def test_owner_cannot_edit_own_record(self):
        response = APIClient().patch(
            f"{API}{self.mine.id}/",
            {"first_name": "Hacked"},
            format="json",
            **bearer(role="patient", user_id=self.owner_id),
        )
        self.assertEqual(response.status_code, 403)

    def test_me_resolves_linked_profile(self):
        response = APIClient().get(API + "me/", **bearer(role="patient", user_id=self.owner_id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], str(self.mine.id))

    def test_me_returns_404_when_no_profile_is_linked(self):
        response = APIClient().get(API + "me/", **bearer(role="patient"))
        self.assertEqual(response.status_code, 404)

    def test_owner_cannot_read_own_record_after_deactivation(self):
        self.mine.is_active = False
        self.mine.save()
        response = APIClient().get(f"{API}{self.mine.id}/", **bearer(role="patient", user_id=self.owner_id))
        self.assertEqual(response.status_code, 403)


class DeactivateTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(first_name="Temp", last_name="Record")

    def test_receptionist_deactivates_patient(self):
        response = APIClient().post(
            f"{API}{self.patient.id}/deactivate/", **bearer(role="receptionist")
        )
        self.assertEqual(response.status_code, 200)
        self.patient.refresh_from_db()
        self.assertFalse(self.patient.is_active)

    def test_doctor_cannot_deactivate(self):
        response = APIClient().post(
            f"{API}{self.patient.id}/deactivate/", **bearer(role="doctor")
        )
        self.assertEqual(response.status_code, 403)

    def test_deactivating_twice_returns_404(self):
        client = APIClient()
        client.post(f"{API}{self.patient.id}/deactivate/", **bearer(role="admin"))
        response = client.post(f"{API}{self.patient.id}/deactivate/", **bearer(role="admin"))
        self.assertEqual(response.status_code, 404)


class QueryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.headers = bearer(role="receptionist")
        self.asha = Patient.objects.create(first_name="Asha", last_name="Kumar")
        self.ravi = Patient.objects.create(first_name="Ravi", last_name="Sharma")

    def test_search_by_mrn_returns_single_match(self):
        response = self.client.get(
            f"{API}?search={self.asha.medical_record_number}", **self.headers
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], str(self.asha.id))

    def test_inactive_patients_are_hidden_by_default(self):
        self.asha.is_active = False
        self.asha.save()
        response = self.client.get(API, **self.headers)
        self.assertEqual(response.data["count"], 1)
        response = self.client.get(API + "?include_inactive=true", **self.headers)
        self.assertEqual(response.data["count"], 2)

    def test_auth_user_id_filter_returns_linked_profile(self):
        owner = uuid.uuid4()
        self.ravi.auth_user_id = owner
        self.ravi.save()
        response = self.client.get(f"{API}?auth_user_id={owner}", **self.headers)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], str(self.ravi.id))

    def test_invalid_auth_user_id_returns_no_results(self):
        response = self.client.get(f"{API}?auth_user_id=not-a-uuid", **self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 0)


@unittest.skipUnless(settings.API_DOCS_ENABLED, "API docs are only routed when API_DOCS_ENABLED=1")
class ApiDocsTests(TestCase):
    def test_schema_contains_patient_paths_and_bearer_scheme(self):
        response = APIClient().get("/api/schema/", HTTP_ACCEPT="application/vnd.oai.openapi+json")
        self.assertEqual(response.status_code, 200)
        self.assertIn("BearerAuth", response.data["components"]["securitySchemes"])
        self.assertIn("/api/patients/", response.data["paths"])

    def test_swagger_ui_is_served(self):
        response = APIClient().get("/api/docs/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "swagger-ui")


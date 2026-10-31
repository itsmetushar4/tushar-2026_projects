import uuid

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class TokenUser:
    """Principal built from JWT claims only; no database lookup."""

    def __init__(self, payload):
        self.payload = payload
        # JWT claims are JSON strings; model UUID fields are uuid.UUID.
        raw_id = payload.get("user_id")
        try:
            self.id = uuid.UUID(str(raw_id))
        except (ValueError, TypeError):
            self.id = raw_id
        self.pk = self.id
        self.username = payload.get("username", "")
        self.role = payload.get("role")
        self.is_active = True
        self.is_authenticated = True

    def __str__(self):
        return str(self.username)


class SharedSecretJWTAuthentication(JWTAuthentication):
    """Validates HS256 tokens signed with the shared DJANGO_SECRET_KEY.

    The users table lives in the auth service's database, so instead of
    the default database lookup, the principal is built from token claims.
    """

    def get_user(self, validated_token):
        if not validated_token.payload.get("role"):
            raise AuthenticationFailed("Token has no role claim; log in again.")
        return TokenUser(validated_token.payload)

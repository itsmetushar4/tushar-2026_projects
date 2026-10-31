from drf_spectacular.extensions import OpenApiAuthenticationExtension


class SharedSecretJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "patients.authentication.SharedSecretJWTAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Access token from POST /api/auth/token/ on the auth service.",
        }

from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.views import exception_handler

HINT = (
    " Send 'Authorization: Bearer <access token>' - get one from "
    "POST http://localhost:8001/api/auth/token/ (copy the 'access' value, not 'refresh')."
)


def hms_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None and isinstance(exc, (NotAuthenticated, AuthenticationFailed)):
        detail = response.data.get("detail")
        if isinstance(detail, str) and "Authorization" not in detail:
            response.data["detail"] = detail + HINT
    return response

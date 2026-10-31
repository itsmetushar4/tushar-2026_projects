from django.conf import settings
from django.urls import include, path
from drf_spectacular.utils import extend_schema, inline_serializer
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

HealthResponse = inline_serializer(
    "HealthResponse",
    {"service": serializers.CharField(), "status": serializers.CharField()},
)


@extend_schema(responses=HealthResponse, auth=[])
@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    return Response({"service": "patient", "status": "ok"})


urlpatterns = [
    path("api/health/", health, name="health"),
    path("api/", include("patients.urls")),
]

if settings.API_DOCS_ENABLED:
    urlpatterns += [
        path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
        path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
        path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    ]

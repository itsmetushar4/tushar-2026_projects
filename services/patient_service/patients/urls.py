from django.urls import path

from . import views

urlpatterns = [
    path("patients/", views.PatientListCreateView.as_view(), name="patient-list"),
    path("patients/me/", views.PatientMeView.as_view(), name="patient-me"),
    path("patients/<uuid:pk>/", views.PatientDetailView.as_view(), name="patient-detail"),
    path("patients/<uuid:pk>/deactivate/", views.PatientDeactivateView.as_view(), name="patient-deactivate"),
]

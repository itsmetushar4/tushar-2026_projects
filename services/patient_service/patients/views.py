import uuid

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient
from .permissions import IsAdminOrReceptionist, IsHospitalStaff, IsStaffOrOwner
from .serializers import PatientCreateSerializer, PatientSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    permission_classes = [IsHospitalStaff]
    filter_backends = [SearchFilter]
    search_fields = ["first_name", "last_name", "medical_record_number", "phone"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return PatientCreateSerializer
        return PatientSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        auth_user_id = self.request.query_params.get("auth_user_id")
        if auth_user_id:
            try:
                uuid.UUID(auth_user_id)
            except ValueError:
                return qs.none()
            qs = qs.filter(auth_user_id=auth_user_id)
        if self.request.query_params.get("include_inactive") != "true":
            qs = qs.filter(is_active=True)
        return qs


class PatientDetailView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated, IsStaffOrOwner]


class PatientMeView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Patient, auth_user_id=self.request.user.id, is_active=True)


class PatientDeactivateView(APIView):
    permission_classes = [IsAdminOrReceptionist]

    @extend_schema(request=None, responses=PatientSerializer)
    def post(self, request, pk):
        patient = get_object_or_404(Patient, pk=pk, is_active=True)
        patient.is_active = False
        patient.save(update_fields=["is_active", "updated_at"])
        return Response(PatientSerializer(patient).data)

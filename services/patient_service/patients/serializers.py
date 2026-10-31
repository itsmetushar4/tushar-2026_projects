from rest_framework import serializers

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id", "medical_record_number", "auth_user_id",
            "first_name", "last_name", "date_of_birth", "gender",
            "phone", "email", "address", "blood_group",
            "emergency_contact_name", "emergency_contact_phone",
            "is_active", "created_at", "updated_at",
        )
        read_only_fields = ("id", "medical_record_number", "created_at", "updated_at")

    def validate_phone(self, value):
        if value:
            cleaned = value.replace(" ", "").replace("-", "")
            if not cleaned.startswith("+") or not cleaned[1:].isdigit() or len(cleaned) < 8:
                raise serializers.ValidationError(
                    "Phone must look like '+911234567890' (digits, optional leading +)."
                )
        return value


class PatientCreateSerializer(PatientSerializer):
    pass

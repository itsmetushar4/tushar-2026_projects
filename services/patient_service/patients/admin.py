from django.contrib import admin

from .models import Patient


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("medical_record_number", "first_name", "last_name", "phone", "is_active")
    search_fields = ("medical_record_number", "first_name", "last_name", "phone")
    list_filter = ("is_active", "gender", "blood_group")

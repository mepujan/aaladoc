from rest_framework.serializers import ModelSerializer
from Doctor.models import BasicInfo
from .models import Information, Prescription
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientInformationSerializers(ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"


class DoctorPrescriptionSerializer(ModelSerializer):
    class Meta:
        model = Prescription
        fields = (
            "user_id",
            "doctor_id",
            "prescription",
            "prescribed_date",
            "image",
            "is_prescribed",
        )


class DoctorPrescriptionListSerializers(ModelSerializer):
    class Meta:
        model = Prescription
        fields = "__all__"

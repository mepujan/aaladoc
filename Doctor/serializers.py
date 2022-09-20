from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from SiteContents.serializers import PaymentSerializer

from .models import (
    City,
    Degree,
    Institution,
    BasicInfo,
    Specialization,
    RegistrationCouncil,
    DoctorRating,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class CitiesSerializers(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class DegreeSerializers(ModelSerializer):
    class Meta:
        model = Degree
        fields = "__all__"


class SpecializationSerializers(ModelSerializer):
    class Meta:
        model = Specialization
        fields = "__all__"


class InstitutionSerializers(ModelSerializer):
    class Meta:
        model = Institution
        fields = "__all__"


class RegistrationCouncilSerializers(ModelSerializer):
    class Meta:
        model = RegistrationCouncil
        fields = "__all__"


class DoctorInfoSerializers(ModelSerializer):
    profile_pic = serializers.ImageField()
    call_to_doctor = PaymentSerializer(many=True)

    class Meta:
        model = BasicInfo
        fields = [
            "id",
            "user",
            "name",
            "first_name",
            "last_name",
            "username",
            "phone",
            "specialization",
            "registration_no",
            "reg_council",
            "reg_year",
            "gender",
            "degree",
            "institution",
            "degree_year",
            "experience",
            "address",
            "dob",
            "short_bio",
            "is_online",
            "avg_rating",
            "call_to_doctor",
            "profile_pic"
        ]


class DoctorMedicalNumberChecker(serializers.Serializer):
    full_name = serializers.CharField(max_length=200, required=True)
    medical_number = serializers.CharField(max_length=200, required=True)


class DoctorRatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = DoctorRating
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "address", "phone")


class DoctorProfileSerializers(ModelSerializer):
    profile_pic = serializers.ImageField()

    class Meta:
        model = BasicInfo
        fields = [
            "doctor_id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "address",
            "blood_group",
            "profile_pic",
            "dob",
            "gender",
            "specialization",
            "registration_no",
            "reg_council",
            "reg_year",
            "degree",
            "institution",
            "degree_year",
            "experience",
            "short_bio",
            "is_online",
            "is_staff",
            "doctor_uuid",
        ]


class DoctorProfileUpdate(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=200)
    last_name = serializers.CharField(max_length=200)
    address = serializers.CharField(max_length=200)
    phone = serializers.CharField(max_length=20)
    profile_pic = serializers.ImageField(required=False)
    blood_group = serializers.CharField(max_length=10)
    gender = serializers.CharField(max_length=10)
    dob = serializers.DateField()

    class Meta:
        model = BasicInfo
        fields = (
            "first_name",
            "last_name",
            "address",
            "phone",
            "profile_pic",
            "blood_group",
            "gender",
            "dob",
            "short_bio",
        )


class CallEndingSerializer(serializers.Serializer):
    doctor = serializers.CharField(max_length=50)
    user = serializers.CharField(max_length=50)
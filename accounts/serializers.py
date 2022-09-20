from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer

from .models import *
from Doctor.models import *
User = get_user_model()

login_pages = (("patient", "patient"), ("doctor", "doctor"))

class DoctorInfosSerializers(ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = "__all__"

class UserRegistrationSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "address",
            "district",
            "dob",
            "phone",
            "profile_pic",
            "blood_group",
            "gender",
            "height",
            "weight",
            "is_available",
            "is_staff",
            
        ]
        extra_kwargs = {"password": {"write_only": True},"id":{"read_only":True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            address=validated_data["address"],
            district = validated_data["district"],
            dob=validated_data["dob"],
            phone=validated_data["phone"],
            blood_group=validated_data["blood_group"],
            gender=validated_data["gender"],
            profile_pic=validated_data["profile_pic"],
            password=validated_data["password"],
            height = validated_data["height"],
            weight = validated_data['weight'],
            is_active=True,
            is_staff=validated_data['is_staff'],
            is_available=validated_data["is_available"],
        )
        user.save()
        Token.objects.create(user=user)
        return user


class UserUpdateSerialiazers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "address",
            "district",
            "dob",
            "phone",
            "profile_pic",
            "date_joined",
            "blood_group",
            "gender",
            "height",
            "weight",
            "is_available",
        ]


class UserValidationSerializers(ModelSerializer):
    class Meta:
        model = ValidateUser
        fields = [
            "email",
        ]

    # def create(self, validated_data):
    #     user = ValidateUser.objects.create(email=validated_data["email"], code=1234)
    #     user.save()
    #     return user


class CodeValidationSerializers(ModelSerializer):
    class Meta:
        model = ValidateUser
        fields = ["email", "code"]


class DoctorRegistrationSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "phone",
            "profile_pic",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            username=validated_data["username"],
            email=validated_data["email"],
            phone=validated_data["phone"],
            profile_pic=validated_data["profile_pic"],
        )
        user.set_password(validated_data["password"])
        user.is_active = True
        user.is_staff = True
        user.save()
        Token.objects.create(user=user)
        return user


class UserLoginSerializers(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)
    fcm_token = serializers.CharField(max_length=500)
    status = serializers.CharField(max_length=10)


class LastLoginSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "last_login"]


class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == "password":
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class BloodDonorInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "address",
            "district",
            "age",
            "phone",
            "profile_pic",
            "blood_group",
            "gender",
            "is_available",
            "search_keyword",
        ]


class ResetPasswordSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "password",
        )


class UserFCMTokenSerializer(ModelSerializer):
    class Meta:
        model = UserFCMToken
        fields = ("fcm_token",)

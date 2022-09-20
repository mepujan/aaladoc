from rest_framework import serializers
from .models import (
    Carousel,
    Notification,
    GeneralSetting,
    Payment,
    Properties,
    CallDetail,
    ContactInformation,
    Privacy_Policy,
    AboutUs,
    PaymentMethod,
)


class CarouselSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carousel
        fields = "__all__"


#
# class NotificationTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = NotificationType
#         fields = "__all__"

# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = "__all__"


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class GeneralSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralSetting
        fields = "__all__"


class CallDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CallDetail
        fields = "__all__"

class AddPaymentMethodSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("doctor","user","image","remarks","is_verified","call_to_doctor","call_successful")


class PropertiesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = "__all__"


class ContactInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = ContactInformation
        fields = "__all__"


class PrivcyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = Privacy_Policy
        fields = "__all__"

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = "__all__"
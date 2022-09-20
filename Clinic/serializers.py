from rest_framework.serializers import ModelSerializer
from .models import City, Locality, ClinicInfo


class CitySerializers(ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class LocalitySerializers(ModelSerializer):
    class Meta:
        model = Locality
        fields = "__all__"


class ClinicSerializers(ModelSerializer):
    class Meta:
        model = ClinicInfo
        fields = "__all__"

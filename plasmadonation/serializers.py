from rest_framework.serializers import ModelSerializer

from .models import PlasmaDonorsInformation


class PlasmaDonorSerializers(ModelSerializer):
    class Meta:
        model = PlasmaDonorsInformation
        fields = "__all__"

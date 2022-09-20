from rest_framework.viewsets import ModelViewSet

from .models import PlasmaDonorsInformation
from .serializers import PlasmaDonorSerializers


class PlasmaDonorAPIView(ModelViewSet):
    serializer_class = PlasmaDonorSerializers
    queryset = PlasmaDonorsInformation.objects.all()
    filterset_fields = ("district", "blood_type")

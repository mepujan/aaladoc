from rest_framework.serializers import ModelSerializer

from .models import Schedule, DoctorAppointment


class ScheduleSerializers(ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class DoctorAppointmentSerializers(ModelSerializer):
    class Meta:
        model = DoctorAppointment
        fields = "__all__"


# class DoctorAppointmentSerializer(Model)

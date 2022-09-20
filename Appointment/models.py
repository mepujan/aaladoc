from Doctor.models import BasicInfo
from django.conf import settings
from django.db import models
from .utils import get_code
import recurrence.fields

days = (
    ("Sunday", "Sunday"),
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
)
appointment_types = (("New", "New"), ("Followup", "Followup"))


class Schedule(models.Model):
    doctor = models.ForeignKey(
        BasicInfo, on_delete=models.CASCADE, related_name="doctor_schedule"
    )
    available_day = models.CharField(max_length=10, choices=days, null=True)
    available_from_date_time = models.DateTimeField(null=True)
    available_to_date_time = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # recurrences = recurrence.fields.RecurrenceField(null=True)

    def __str__(self):
        return f"{self.doctor.user.username} ------>>>> {self.available_date_time.strftime('%d-%m-%Y %I: %m: %S %p')} "

    def doctor_username(self):
        return self.doctor.user.username


class DoctorAppointment(models.Model):
    appointment_id = models.CharField(max_length=10, blank=True)
    doctor = models.ForeignKey(
        BasicInfo, on_delete=models.CASCADE, related_name="appointment"
    )
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    appointment_type = models.CharField(
        max_length=10, choices=appointment_types, default="New"
    )
    appointment_time = models.ForeignKey(
        Schedule, on_delete=models.DO_NOTHING, null=True
    )
    pending = models.BooleanField(default=True)
    approved = models.BooleanField(default=False)
    attended = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.patient.username} has send an appointment for {self.doctor.user.username} with appointment id of {self.appointment_id}"

    def save(self, *args, **kwargs):
        if self.appointment_id == "":
            self.appointment_id = get_code()
        return super().save(*args, **kwargs)

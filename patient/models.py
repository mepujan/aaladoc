from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from Doctor.models import BasicInfo

User = get_user_model()

blood_group = (
    ("O +ve", "O +ve"),
    ("O -ve", "O -ve"),
    ("A +ve", "A +ve"),
    ("A -ve", "A -ve"),
    ("B +ve", "B +ve"),
    ("B -ve", "B -ve"),
    ("AB +ve", "AB +ve"),
    ("AB -ve", "AB -ve"),
)


class Information(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    sex = models.CharField(
        max_length=50,
        choices=(("Male", "Male"), ("Female", "Female"), ("Others", "Others")),
    )
    image = models.ImageField(upload_to="media", null=True)
    address = models.TextField()
    blood_group = models.CharField(max_length=6, choices=blood_group)
    covid_status = models.BooleanField(default=False)
    is_ready_to_donate_blood = models.BooleanField(default=True)

    def __self__(self):
        return self.user.name


class Prescription(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True)
    doctor_id = models.ForeignKey(BasicInfo, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=255, blank=True)
    # medicine_name = models.CharField(max_length=200)
    # medicine_type = models.CharField(max_length=200)
    # days_of_treatment = models.IntegerField()
    # pills_per_day = models.IntegerField()
    prescription = models.TextField(blank = True)
    prescribed_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to="media", null=True)
    is_prescribed = models.BooleanField(default=False)

    def __str__(self):
        return self.user_id.username

    class Meta:
        ordering = ("-prescribed_date",)

    def save(self, *args, **kwargs):

        self.username = self.user_id.username
        self.doctor_name = self.doctor_id.name

        return super().save(*args, **kwargs)

from django.db import models

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


class PlasmaDonorsInformation(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    district = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    dob = models.DateField()
    blood_type = models.CharField(max_length=6, choices=blood_group)
    profile_picture = models.ImageField(upload_to="media")

    def __str__(self):
        return str(self.email)

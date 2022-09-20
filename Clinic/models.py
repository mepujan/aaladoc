from django.db import models


# Create your models here.
class City(models.Model):
    address = models.TextField(primary_key=True)
    district = models.TextField()

    def __str__(self):
        return self.address


class Locality(models.Model):
    address = models.ForeignKey(City, on_delete=models.CASCADE)
    local_address = models.TextField(primary_key=True)

    def __str__(self):
        return self.local_address


class ClinicInfo(models.Model):
    name = models.TextField(unique=True)
    clinic_id = models.CharField(max_length=100, primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE)
    phone = models.CharField(max_length=500)
    website = models.TextField()
    image = models.TextField()

    def __str__(self):
        return self.name

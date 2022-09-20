from django.conf import settings
from django.db import models
from django.urls import reverse

GENDER = (("male", "male"), ("female", "female"), ("others", "others"))


class City(models.Model):
    name = models.CharField(max_length=300)
    district = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=200, unique=True, primary_key=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name


class RegistrationCouncil(models.Model):
    name = models.CharField(max_length=300, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=300, unique=True, primary_key=True)

    def __str__(self):
        return self.name


class BasicInfo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE,null = True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE,null = True)
    degree_year = models.DateField(null = True)
    specialization = models.ForeignKey(
        Specialization, on_delete=models.DO_NOTHING, default = "ENT"
    )
    registration_no = models.CharField(max_length=200)
    reg_council = models.ForeignKey(RegistrationCouncil, on_delete=models.CASCADE,null = True)
    reg_year = models.DateField(null = True)
    experience = models.CharField(max_length=10, blank=True,null = True)
    registration_verification = models.BooleanField(default=False)
    degree_verification = models.BooleanField(default=False)
    photo_verification = models.BooleanField(default=False)
    final_verification = models.BooleanField(default=False)
    short_bio = models.TextField(blank=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def doctor_id(self):
        return self.id
        
    def profile_pic(self):
        return self.user.profile_pic

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def name(self):
        return str(self.user.first_name + " " + self.user.last_name)

    def username(self):
        return self.user.username

    def email(self):
        return self.user.email

    def phone(self):
        return self.user.phone

    def profile_pic(self):
        return self.user.profile_pic

    def address(self):
        return self.user.address

    def blood_group(self):
        return self.user.blood_group

    def dob(self):
        return self.user.dob

    def gender(self):
        return self.user.gender

    def is_staff(self):
        return self.user.is_staff

    def doctor_uuid(self):
        return self.user.uuid

    def get_absolute_url(self):
        return reverse("Doctor:details", kwargs={"doctor_id": self.doctor_id})

    def get_appointment_url(self):
        return reverse("Appointment:timing", kwargs={"doctor_id": self.doctor_id})


    def avg_rating(self):
        ratings = self.doctor_rating.all()
        total_rating = self.doctor_rating.all().count()
        if total_rating == 0:
            return total_rating
        else:
            avg = 0.0
            total = 0

            for rating_ in ratings:
                total += rating_.rating
            avg = total // total_rating
            return avg

    @property
    def call_to_doctor(self):
        datas = self.payment.all()
        return datas

class DoctorRating(models.Model):
    doctor = models.ForeignKey(
        BasicInfo, related_name="doctor_rating", on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(help_text="Enter number between 1 to 5")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rating of {self.doctor.name} is {self.rating}"

    def save(self, *args, **kwargs):
        if self.rating in range(1, 6):
            return super().save(*args, **kwargs)
        else:
            return NotImplementedError("Rating should be in range 1 to 5")

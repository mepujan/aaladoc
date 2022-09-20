from django.contrib.auth.models import AbstractUser
from django.db import models
from .utils import generateUUID
from django.conf import settings
from datetime import date, timedelta
import random

blood = (
    ("A+", "A+"),
    ("B+", "B+"),
    ("B-", "B-"),
    ("A-", "A-"),
    ("AB+", "AB+"),
    ("AB-", "AB-"),
    ("O+", "O+"),
    ("O-", "O-"),
)
GENDER = (("male", "male"), ("female", "female"))


class User(AbstractUser):
    uuid = models.CharField(max_length=50, blank=True)
    address = models.CharField(max_length=200, blank=True,null=True)
    phone = models.CharField(max_length=100, default=None, null=True)
    district = models.CharField(max_length=100,default="morang")
    profile_pic = models.ImageField(upload_to="media", default = "userlogo.jpg")
    blood_group = models.CharField(choices=blood, max_length=200, blank=True)
    gender = models.CharField(choices=GENDER, max_length=200, blank=True)
    dob = models.DateField(null=True,blank=True)
    age = models.PositiveIntegerField(blank=True,null=True)
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    is_available = models.BooleanField(default=False)
    search_keyword = models.CharField(max_length=3, blank=True)

    def save(self, *args, **kwargs):
        if self.uuid == "":
            self.uuid = generateUUID()

        if self.blood_group == "A+" or self.blood_group == "A-":
            self.search_keyword = "a"
        elif self.blood_group == "B+" or self.blood_group == "B-":
            self.search_keyword = "b"
        elif self.blood_group == "AB+" or self.blood_group == "AB-":
            self.search_keyword = "ab"
        elif self.blood_group == "O+" or self.blood_group == "O-":
            self.search_keyword = "o"
        if self.dob:
            self.age = (date.today() - self.dob) // timedelta(days=365.2425)
        return super().save(*args, **kwargs)


class ValidateUser(models.Model):
    email = models.EmailField(max_length=300)
    code = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        numbers = [num for num in range(0, 10)]
        code = []
        for _ in range(4):
            num = random.choice(numbers)
            code.append(num)

        code_str = "".join(str(num) for num in code)
        self.code = code_str
        return super().save(*args, **kwargs)


class UserFCMToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fcm_token = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.email)

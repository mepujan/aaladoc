from django.conf import settings
from django.db import models
from Doctor.models import BasicInfo


class Carousel(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media")

    def __str__(self):
        return self.title


class GeneralSetting(models.Model):
    settingName = models.CharField(max_length=30)
    settingsURL = models.URLField()

    def __str__(self):
        return self.settingName


class NotificationType(models.Model):
    name = models.CharField(max_length=100, unique=True, primary_key=True)
    colorCode = models.CharField(max_length=16)

    def __str__(self):
        return self.name


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    body = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.name)


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    doctor = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, null=True,related_name="payment")
    image = models.ImageField(upload_to="media")
    remarks = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    call_to_doctor = models.BooleanField(default=False)
    call_successful = models.BooleanField(default=False)
    appointment_date_time = models.DateTimeField(blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user.username)

class AddPayment(models.Model):
    name = models.CharField(max_length = 500)
    account_no = models.CharField(max_length = 500,blank = True)
    image = models.ImageField(null = True)

    def __str__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length = 500)
    logo = models.ImageField(upload_to = "media")
    account_no = models.CharField(max_length = 500)
    phone_no = models.CharField(max_length = 500)

    def __str__(self):
        return self.name



class Properties(models.Model):
    logo = models.ImageField(upload_to="media", null=True)
    app_name = models.CharField(max_length=400)

    def __str__(self):
        return self.app_name


class CallDetail(models.Model):
    sender_id = models.PositiveIntegerField()
    receiver_id = models.PositiveIntegerField()
    call_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Call Details of user id {self.receiver_id}"


class ContactInformation(models.Model):
    name = models.CharField(max_length=200,null=True,blank = True)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    logo = models.ImageField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.email} ---> contact info created at {self.created} "

    class Meta:
        ordering =('-created',)


class Privacy_Policy(models.Model):
    policy_url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.policy_url} has been created at {self.created}"

    class Meta:
        verbose_name_plural = "Privacy Policies"
        ordering =('-created',)


class AboutUs(models.Model):
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.url)

    class Meta:
        verbose_name_plural = "About Us"
        ordering = ("-created",)

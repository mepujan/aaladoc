from django.db import models


class Service(models.Model):
    title = models.CharField(max_length=100)
    sub_title = models.CharField(max_length=100)
    title_description = models.TextField()
    sub_title_description = models.TextField()
    image = models.ImageField(upload_to='services')
    icons = models.ImageField(upload_to='services_icon')

    def __str__(self):
        return self.title

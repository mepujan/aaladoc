from django.contrib import admin
from .models import *

# Register your models here.
admin.site.site_title = "AlaDoc Admin"
admin.site.site_header = "AlaDoc Application SuperAdmin"
admin.site.register(Schedule)
admin.site.register(DoctorAppointment)

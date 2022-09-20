from django.contrib import admin

from .models import *


class basicinfo(admin.ModelAdmin):
    list_display = ("id", "registration_no", "final_verification", "reg_council")
    search_fields = ("specialization", "registration_no", "final_verification")
    list_filter = ("specialization", "reg_council", "final_verification")
    list_per_page = 20


admin.site.register(BasicInfo, basicinfo)
admin.site.register(City)
admin.site.register(Degree)
admin.site.register(Institution)
admin.site.register(RegistrationCouncil)
admin.site.register(Specialization)
admin.site.register(DoctorRating)

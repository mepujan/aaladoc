from django.contrib import admin
from .models import *

# Register your models here.
class information(admin.ModelAdmin):
    list_display = ("user", "sex", "address")
    search_fields = ("user", "address")
    list_per_page = 20


admin.site.register(Information, information)

admin.site.register(Prescription)

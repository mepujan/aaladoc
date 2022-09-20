from django.contrib import admin
from .models import User, ValidateUser, UserFCMToken


class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


admin.site.register(User, UserAdmin)
admin.site.register(ValidateUser)
admin.site.register(UserFCMToken)

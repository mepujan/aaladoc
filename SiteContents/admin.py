from django.contrib import admin
from .models import PaymentMethod,Carousel,GeneralSetting,Payment,Notification,Properties,CallDetail,ContactInformation,Privacy_Policy,AboutUs


admin.site.register(Carousel)
admin.site.register(GeneralSetting)
admin.site.register(Payment)
admin.site.register(Notification)
# admin.site.register(NotificationType)
admin.site.register(Properties)
admin.site.register(CallDetail)
admin.site.register(PaymentMethod)
admin.site.register((ContactInformation,Privacy_Policy,AboutUs))


from django.urls import path

from .views import *

app_name = "Appointment"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("pagenotfound/", PageNotFound.as_view(), name="404error"),
    path("timing/<doctor_id>", AppointmentTimingView.as_view(), name="timing"),
    path("contact/", ContactPage.as_view(), name="contact"),
    path("privacy/", PrivacyView.as_view(), name="privacy"),
]

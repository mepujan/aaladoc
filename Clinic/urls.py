from django.urls import path
from .views import *

app_name = 'Clinic'

urlpatterns = [
    path('',ClinicHomeView.as_view(),name = "Doctor"),
]
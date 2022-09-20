from django.urls import path

from .views import *

app_name = 'Doctor'

urlpatterns = [
    path('', DoctorHomeView.as_view(), name="doctor"),
    path('details/<doctor_id>', DoctorInfoView.as_view(), name="details"),
    path('timetable', TimeTable.as_view(), name='time_table')
]

from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View

from .models import *


class BaseView(View):
    views = {}


class HomeView(BaseView):
    def get(self, request):
        return render(self.request, "index.html")
        

class PrivacyView(BaseView):
    def get(self, request):
        return render(self.request, "privacy.html")


class AppointmentTimingView(BaseView):
    def get(self, request, doctor_id):
        self.views["timings"] = Schedule.objects.filter(doctor_id=doctor_id)
        return render(self.request, "appoinmenttime.html")


class PageNotFound(BaseView):
    def get(self, request):
        return render(self.request, "404.html")


class ContactPage(BaseView):
    def get(self, request):
        return render(request, "contact.html")

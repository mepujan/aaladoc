from django.shortcuts import render

from Appointment.views import BaseView
from .models import Service


class ServicePage(BaseView):
    def get(self, request):
        self.views['services'] = Service.objects.all()
        return render(request, 'services.html', self.views)


class SingleServicePage(BaseView):
    def get(self, request, id):
        self.views['service_descriptions'] = Service.objects.filter(id=id)

        return render(request, 'single-service.html', self.views)


class AboutUsView(BaseView):
    def get(self, request):
        return render(request, 'about.html')

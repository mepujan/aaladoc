# Create your views here.
from Appointment.views import *


# Create your views here.
class ClinicHomeView(BaseView):
    def get(self, request):
        self.views["clinic_info"] = ClinicInfo.objects.all()
        self.views["clinic_location"] = Locality.objects.all()
        return render(self.request, "clinics.html", self.views)

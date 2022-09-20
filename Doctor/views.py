from Appointment.views import *


class DoctorHomeView(BaseView):
    def get(self, request):
        self.views["doc_info"] = BasicInfo.objects.all()
        self.views["specialization"] = Specialization.objects.all()
        return render(self.request, "doctors.html", self.views)


class DoctorInfoView(BaseView):
    def get(self, request, doctor_id):
        self.views["doc_details"] = BasicInfo.objects.filter(doctor_id=doctor_id)
        return render(self.request, "doctor-details.html", self.views)


class TimeTable(BaseView):
    def get(self, request):
        return render(request, "time-table.html")

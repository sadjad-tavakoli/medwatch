from django.views.generic.list import ListView

from schedule.models import Appointment


class AppointmentsList(ListView):
    template_name = 'member/appointments_list.html'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.member)

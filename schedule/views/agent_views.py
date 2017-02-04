from django.views.generic.list import ListView

from schedule.models import Appointment


class AgentAppointmentsList(ListView):
    template_name = 'agent/appointment_list.html'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.access_level.doctor)

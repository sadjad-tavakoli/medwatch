import datetime
from django.core.urlresolvers import reverse
from django.views.generic.list import ListView

from med_watch.permissions import AgentPermissionMixin
from schedule.models import Appointment
from schedule.views.member_views import EditAppointmentView


class AgentAppointmentsList(AgentPermissionMixin, ListView):
    template_name = 'agent/appointment_list.html'

    def get_queryset(self):
        return Appointment.objects.filter(doctor=self.request.access_level.doctor)


class AgentEditAppointmentView(AgentPermissionMixin, EditAppointmentView):
    def get_object(self, queryset=None):
        appointment_id = self.kwargs.get('appointment_id', None)
        return Appointment.objects.get(doctor=self.request.access_level.doctor, id=appointment_id)

    def form_valid(self, form):
        last_time = self.get_object().start_time
        instance = form.save(commit=False)
        new_time = instance.start_time
        time_delta = datetime.timedelta(days=0, hours=new_time.hour - last_time.hour,
                                        minutes=new_time.minute - last_time.minute,
                                        seconds=new_time.second - last_time.second)
        for appointment in Appointment.objects.all():
            appointment.update_start_time(total_seconds=int(time_delta.total_seconds()))

        return super(AgentEditAppointmentView, self).form_valid(form)

    def get_success_url(self):
        return reverse('members:agent:appointment-list')

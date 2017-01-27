from django.contrib.gis.geos.mutable_list import ListMixin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from member.forms.profile_forms import EditProfileForm
from schedule.forms import EditAppointmentForm
from schedule.models import Appointment


class AppointmentsList(ListView):
    template_name = 'member/appointments_list.html'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user.member)


class CancelAppointments(View):
    def get(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get('appointment_id', None)
        appointment = Appointment.objects.get(patient=self.request.user.member, id=appointment_id)
        appointment.cancel()
        return redirect(reverse('members:patient:appointment-list'))


class EditAppointmentView(UpdateView):
    template_name = 'member/edit_appointment.html'
    model = Appointment
    form_class = EditAppointmentForm

    def get_object(self, queryset=None):
        appointment_id = self.kwargs.get('appointment_id', None)
        return Appointment.objects.get(patient=self.request.user.member, id=appointment_id)
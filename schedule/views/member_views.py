from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from med_watch.permissions import MemberPermissionMixin
from schedule.forms import EditAppointmentForm
from schedule.models import Appointment


class AppointmentsList(MemberPermissionMixin, ListView):
    template_name = 'member/appointments_list.html'

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.access_level.member)


class CancelAppointments(MemberPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        appointment_id = self.kwargs.get('appointment_id', None)
        appointment = Appointment.objects.get(patient=self.request.access_level.member,
                                              id=appointment_id)
        appointment.cancel()
        return redirect(reverse('members:patient:appointment-list'))


class EditAppointmentView(MemberPermissionMixin, UpdateView):
    template_name = 'member/edit_appointment.html'
    model = Appointment
    form_class = EditAppointmentForm

    def get_object(self, queryset=None):
        appointment_id = self.kwargs.get('appointment_id', None)
        return Appointment.objects.get(patient=self.request.access_level.member, id=appointment_id)

    def get_success_url(self):
        return reverse('members:member:appointment-list')

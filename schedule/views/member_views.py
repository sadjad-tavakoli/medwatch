from collections import defaultdict
from datetime import date, timedelta, datetime, time

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View, TemplateView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView

from med_watch.permissions import MemberPermissionMixin
from member.models import DoctorMember
from schedule.forms import EditAppointmentForm
from schedule.models import Appointment, DoctorSchedule, APS_ACCEPTED, AppointmentRequest, APS_REQUESTED


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


class RequestAppointmentView(MemberPermissionMixin, TemplateView):
    template_name = 'member/request_appointment.html'

    def get_context_data(self, **kwargs):
        context = super(RequestAppointmentView, self).get_context_data(**kwargs)
        doctor_id = self.kwargs.get('doctor_id', None)
        doctor = DoctorMember.objects.get(id=doctor_id)

        doctor_schedule = DoctorSchedule.get_by_doctor(doctor)

        today = date.today()

        request_range = [today + timedelta(i) for i in range(1, 11)]
        appointments = doctor.appointmentrequest_set.filter(state=APS_ACCEPTED, date__in=request_range)

        available_ranges = defaultdict(list)

        for day in request_range:
            daily_schedule = doctor_schedule.get_daily_schedule(day)
            st = daily_schedule.start_time
            end_of_session = lambda x: (
                datetime.combine(date(1, 1, 1), x) + timedelta(minutes=doctor_schedule.session_interval)).time()
            et = end_of_session(st)
            while st < et < daily_schedule.end_time:
                time_full = any(
                    (ap.start_time <= st < end_of_session(ap.start_time) and ap.date == day) for ap in appointments)
                available_ranges[day].append((st, time_full))
                st = et
                et = (datetime.combine(date(1, 1, 1), st) + timedelta(minutes=doctor_schedule.session_interval)).time()

        available_ranges = sorted((k, sorted(v)) for k, v in available_ranges.items())

        context.update({
            'available_ranges': available_ranges,
            'session_interval': doctor_schedule.session_interval,
        })
        return context


class GetAppointmentView(MemberPermissionMixin, View):
    def get(self, *args, **kwargs):
        doctor_id = int(self.kwargs.get('doctor_id', None))
        day_ordinal = int(self.kwargs.get('day', None))
        hour = int(self.kwargs.get('hour', None))
        minute = int(self.kwargs.get('minute', None))
        AppointmentRequest.objects.create(doctor_id=doctor_id, patient=self.request.access_level.member,
                                          date=date.fromordinal(day_ordinal), start_time=time(hour=hour, minute=minute),
                                          state=APS_REQUESTED)
        return redirect(reverse('members:show_dr_page', args=[doctor_id]))

from datetime import date, timedelta

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from extra_views.advanced import UpdateWithInlinesView

from schedule.forms import DoctorScheduleForm, DailyScheduleInline
from schedule.models import DoctorSchedule, AppointmentRequest, APS_REQUESTED, Appointment


class ScheduleView(UpdateWithInlinesView):
    model = DoctorSchedule
    form_class = DoctorScheduleForm
    inlines = [DailyScheduleInline, ]
    template_name = 'doctor/schedule.html'
    success_url = '.'

    def get_object(self, queryset=None):
        doctor = self.request.access_level.doctor
        return DoctorSchedule.get_by_doctor(doctor)


class AppointmentRequestsView(TemplateView):
    template_name = 'appointment_requests.html'

    def get_context_data(self, **kwargs):
        context_data = super(AppointmentRequestsView, self).get_context_data(**kwargs)

        doctor = self.request.access_level.doctor
        doctor_schedule = DoctorSchedule.get_by_doctor(doctor)
        today = date.today()
        appointment_requests = AppointmentRequest.objects.filter(state=APS_REQUESTED,
                                                                 doctor=doctor, date__gt=today). \
            order_by('created')
        current_appointments = Appointment.objects.filter(doctor=doctor, date__gt=today).order_by(
            'start_time')
        session_interval = doctor_schedule.get_session_interval()

        for ap_req in appointment_requests:
            day_appointments = filter(lambda x: x.date == ap_req.date, current_appointments)
            daily_schedule = doctor_schedule.get_daily_schedule(ap_req.date)
            if ((ap_req.start_time > daily_schedule.end_time - timedelta(
                    minutes=session_interval)) or (
                        ap_req.start_time < daily_schedule.start_time)
                or (any(abs((ap_req.start_time - other_ap.start_time).total_seconds())
                            < session_interval * 60))
                for other_ap in day_appointments):
                ap_req.acceptable = False
            else:
                ap_req.acceptable = True

        context_data['appointment_requests'] = appointment_requests

        message = self.request.GET.get('message', None)
        context_data['message'] = message

        return context_data


class AppointmentRequestResolvingView(View):
    def get(self, request, *args, **kwargs):
        request_id = request.GET-['request_id']
        action = request.GET.get('action', 'accept')
        appointment_request = AppointmentRequest.objects.get(id=request_id)

        doctor = self.request.access_level.doctor
        doctor_schedule = DoctorSchedule.get_by_doctor(doctor)
        daily_schedule = doctor_schedule.get_daily_schedule(appointment_request.date)
        session_interval = doctor_schedule.get_session_interval()

        overlapping_appointments = Appointment.objects.filter(doctor=doctor,
                                                              date=appointment_request.date,
                                                              start_time__gt=appointment_request.start_time - timedelta(
                                                                  session_interval),
                                                              start_time__lt=appointment_request.start_time + timedelta(
                                                                  session_interval))

        if appointment_request.state != APS_REQUESTED or appointment_request.doctor != doctor:
            message = "Operation not permitted!"
        elif action == 'accept' and (
                        overlapping_appointments.exists() or
                            appointment_request.start_time > daily_schedule.end_time - timedelta(
                            minutes=session_interval) or appointment_request.start_time < daily_schedule.start_time):
            message = "Appointment doesn't fit in schedule!"
        else:
            message = appointment_request.resolve(action)

        return HttpResponseRedirect(
            "{}?message={}".format(reverse('schedule:requests'), message))

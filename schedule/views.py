from extra_views.advanced import UpdateWithInlinesView

from schedule.forms import DoctorScheduleForm, DailyScheduleInline
from schedule.models import DoctorSchedule, DailySchedule


class DoctorScheduleView(UpdateWithInlinesView):
    model = DoctorSchedule
    form_class = DoctorScheduleForm
    inlines = [DailyScheduleInline, ]
    template_name = 'schedule.html'
    success_url = '.'

    def get_object(self, queryset=None):
        doctor = self.request.access_level.doctor
        return DoctorSchedule.get_by_doctor(doctor)

from django import forms
from extra_views.advanced import InlineFormSet

from schedule.models import DailySchedule, DoctorSchedule


class DailyScheduleInline(InlineFormSet):
    model = DailySchedule
    max_num = 7

    can_delete = False
    fields = ('start_time', 'end_time')


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ('session_interval', )

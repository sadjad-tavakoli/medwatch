from django import forms
from django.forms.widgets import ChoiceInput
from extra_views.advanced import InlineFormSet
from schedule.models import DailySchedule, DoctorSchedule, Appointment


class DailyScheduleInline(InlineFormSet):
    model = DailySchedule
    max_num = 7

    can_delete = False
    fields = ('start_time', 'end_time')


class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = ('session_interval',)


class EditAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('doctor', 'date', 'start_time')

    def __init__(self, *args, **kwargs):
        super(EditAppointmentForm, self).__init__(*args, **kwargs)
        self.fields['doctor'].widget.attrs['class'] = 'ui searach dropdown'

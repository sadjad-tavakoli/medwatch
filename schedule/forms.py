from types import MethodType

from django import forms
from extra_views.advanced import InlineFormSet

from schedule.models import DailySchedule, DoctorSchedule, Appointment

DAYS = [
    'Saturday',
    'Sunday',
    'Monday',
    'Thursday',
    'Wednesday',
    'Thursday',
    'Friday',
]


class DailyScheduleInline(InlineFormSet):
    model = DailySchedule
    max_num = 7

    can_delete = False
    fields = ('start_time', 'end_time')

    def __init__(self, *args, **kwargs):
        super(DailyScheduleInline, self).__init__(*args, **kwargs)

    def construct_formset(self, **kwargs):
        formset = super(DailyScheduleInline, self).construct_formset(**kwargs)

        def clean(self):
            cleaned_data = super(type(self), self).clean()
            if cleaned_data['start_time'] > cleaned_data['end_time']:
                raise forms.ValidationError("Start time should be less than or equal to end time")
            return cleaned_data

        for i, form in enumerate(list(formset.forms)):
            form.day = DAYS[i]
            form.clean = MethodType(clean, form)
        return formset


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

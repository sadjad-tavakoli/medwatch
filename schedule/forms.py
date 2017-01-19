from datetime import time

from django import forms
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory, BaseModelFormSet

from schedule.models import TimeSlot, DailySchedule


class TimeSlotForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('instance') is None and self.daily_schedule is None:
            raise ValueError("daily_schedule param should be set when instance is not provided")
        if kwargs.get('instance') is not None and self.daily_schedule is not None:
            raise ValueError("daily_schedule param shouldn't be set when instance is provided")

        self.daily_schedule = kwargs.pop('daily_schedule', None)

        super(TimeSlotForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super(TimeSlotForm, self).save(commit=False)

        if instance.daily_schedule is None:
            instance.daily_schedule = self.daily_schedule

        if commit:
            instance.save()

        return instance

    class Meta:
        model = TimeSlot
        fields = ('start_time', 'end_time')


class BaseTimeSlotFormSet(BaseModelFormSet):
    def clean(self):
        super(BaseTimeSlotFormSet, self).clean()
        max_time = time()

        for form in self.forms:
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            if start_time < max_time:
                raise forms.ValidationError('Interchengin')

            # update the instance value.
            form.instance.name = name


TimeSlotFormSet = modelformset_factory(TimeSlot, form=TimeSlotForm, formset=BaseTimeSlotFormSet)

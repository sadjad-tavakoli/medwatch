from django.views.generic.base import TemplateView, View

from schedule.forms import TimeSlotFormSet


class ScheduleTemplateView(TemplateView):
    template_name = 'schedule.html'

    def get_object(self):
        obj = self.request.user.member
        return obj

    def get_context_data(self, **kwargs):
        context_data = super(ScheduleTemplateView, self).get_context_data(**kwargs)
        return context_data

    def get_formsets(self):
        self.daily_forms = {}
        for day in range(7):
            self.daily_forms[self.get_prefix(day)] = TimeSlotFormSet(**self.get_form_kwargs(day))
        return self.daily_forms

    def get_prefix(self, day):
        return 'day{}_'.format(day)

    def get_form_kwargs(self, day):
        kwargs = {
            'prefix': self.get_prefix(day),
        }

        doctor = self.request.access_level.doctor
        daily_schedule = doctor.doctorschedule.dailyschedule_set.get(day_of_week=day)

        kwargs.update({'queryset': daily_schedule.timeslot_set.order_by('start_time'),
                       'daily_schedule': daily_schedule})

        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES,
            })
        return kwargs

    def get(self, request, *args, **kwargs):
        pass

    def post(self):
        pass


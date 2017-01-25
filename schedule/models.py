from datetime import datetime, time

from django.db import models


class DoctorSchedule(models.Model):
    doctor = models.OneToOneField('member.DoctorMember', null=False)
    session_interval = models.PositiveIntegerField(default=30)

    def __init__(self, *args, **kwargs):
        super(DoctorSchedule, self).__init__(*args, **kwargs)
        self.weekly_schedule_cache = None

    def get_weekly_schedule(self):
        if self.weekly_schedule_cache is None:
            self.weekly_schedule_cache = self.dailyschedule_set.order_by('day_of_week')
        return self.weekly_schedule_cache

    def get_daily_schedule(self, day):
        day_of_week = (day.weekday() + 2) % 7  # datetime starts week with monday
        weekly_schedule = self.get_weekly_schedule()
        return weekly_schedule[day_of_week]

    def get_session_interval(self):
        return self.session_interval

    @staticmethod
    def get_by_doctor(doctor):
        doctor_schedule, created = DoctorSchedule.objects.get_or_create(doctor=doctor)

        if created:
            for day in range(7):
                DailySchedule.objects.create(day_of_week=day, doctor_schedule=doctor_schedule)

        return doctor_schedule


class DailySchedule(models.Model):
    day_of_week = models.SmallIntegerField()
    doctor_schedule = models.ForeignKey(DoctorSchedule, null=False)
    start_time = models.TimeField(default=time(hour=9))
    end_time = models.TimeField(default=time(hour=17))


APS_REQUESTED = 'N'  # New
APS_ACCEPTED = 'A'
APS_REJECTED = 'R'


class AppointmentRequest(models.Model):
    APPOINTMENT_STATES = (
        (APS_REQUESTED, 'Requested'),
        (APS_ACCEPTED, 'Accepted'),
        (APS_REJECTED, 'Rejected'),
    )

    patient = models.ForeignKey('member.Member', null=False)
    doctor = models.ForeignKey('member.DoctorMember', null=False)
    start_time = models.TimeField()
    date = models.DateField()
    state = models.CharField(choices=APPOINTMENT_STATES, default=APS_REQUESTED, max_length=1)
    created = models.DateTimeField(default=datetime.now())

    def resolve(self, action):
        if action == 'accept':
            self.state = APS_ACCEPTED
            message = 'Appointment Accepted'
        else:
            self.state = APS_REJECTED
            message = 'Appointment Rejected'
        self.save()
        return message


class AppointmentManager(models.Manager):
    def get_queryset(self):
        return super(AppointmentManager, self).get_queryset().filter(state=APS_ACCEPTED)

    def create(self, **kwargs):
        kwargs['state'] = APS_ACCEPTED
        return super(AppointmentManager, self).create(**kwargs)


class Appointment(AppointmentRequest):
    objects = AppointmentManager()

    class Meta:
        proxy = True

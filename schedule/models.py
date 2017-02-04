import datetime

from datetime import time
from django.db import models
from med_watch.services import mail_service


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

    def get_first_free_time(self):
        # Todo
        pass

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
APS_CANCELED = 'C'
APS_POSTPONED = 'P'


class AppointmentRequest(models.Model):
    APPOINTMENT_STATES = (
        (APS_REQUESTED, 'Requested'),
        (APS_ACCEPTED, 'Accepted'),
        (APS_REJECTED, 'Rejected'),
        (APS_CANCELED, 'Canceled'),
        (APS_POSTPONED, 'Postponed'),
    )

    patient = models.ForeignKey('member.Member', null=False)
    doctor = models.ForeignKey('member.DoctorMember', null=False)
    start_time = models.TimeField()
    date = models.DateField()
    state = models.CharField(choices=APPOINTMENT_STATES, default=APS_REQUESTED, max_length=1)
    created = models.DateTimeField(default=datetime.datetime.now())

    # state = FSMField(protected=True, default=STATE_NEW)
    # should use fsm ******* @MohammadReza

    def resolve(self, action):
        if action == 'accept':
            self.state = APS_ACCEPTED
            message = 'Appointment Accepted'
        else:
            self.state = APS_REJECTED
            message = 'Appointment Rejected'
        self.save()
        return message

    # Appointment got canceled by user
    def cancel(self):
        self.state = APS_CANCELED
        message = 'Appointment Canceled'
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

    # Appointment got canceled by doctor
    def postpone(self, reschedule=True):
        assert self.state == APS_ACCEPTED
        self.state = APS_POSTPONED
        self.save()

        reschedule_message = ''
        if reschedule:
            doctor_schedule = DoctorSchedule.get_by_doctor(self.doctor)
            first_free_time = doctor_schedule.get_first_free_time()
            new_appointment = Appointment.objects.create(patient=self.patient,
                                                         doctor=self.doctor,
                                                         date=first_free_time.date(),
                                                         time=first_free_time.time())
            mail_service.send_mail(template='appointment_reschedule', context={
                'appointment': self,
                'new_appointment': new_appointment,
            })
            message = 'Appointment Postponed to {}'.format(first_free_time)
        else:
            mail_service.send_mail(template='appointment_cancel', context={
                'appointment': self,
            })
            message = 'Appointment Canceled by Doctor'
        return message

    class Meta:
        proxy = True

    def update_start_time(self, total_seconds):
        hours, seconds = divmod(total_seconds, 3600)
        minutes, seconds = divmod(seconds, 60)
        print(seconds)
        print(minutes)
        print(hours)
        print(self.start_time)
        hour = self.start_time.hour + hours
        minute = self.start_time.minute + minutes
        second = self.start_time.second + seconds
        tmp_min, second = divmod(second, 60)
        minute += tmp_min
        tmp_hour, minute = divmod(minute, 60)
        hour += tmp_hour
        day, hour = divmod(hour, 24)
        new_time = datetime.time(hour=hour,
                                 minute=minute,
                                 second=second)
        self.start_time = new_time
        self.save()

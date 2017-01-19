from django.db import models


class DoctorSchedule(models.Model):
    doctor = models.OneToOneField('member.DoctorMember', null=False)
    session_interval = models.PositiveIntegerField()

    def __init__(self, *args, **kwargs):
        super(DoctorSchedule, self).__init__(*args, **kwargs)
        self.weekly_schedule_cache = None

    def get_weekly_schedule(self):
        if self.weekly_schedule_cache is None:
            self.weekly_schedule_cache = self.dailyschedule_set.prefetch_related('timeslots').order_by('day_of_week')
        return self.weekly_schedule_cache

    def get_session_interval(self):
        return self.session_interval

    def get_time_slots(self, range_start, range_end):
        weekly_schedule = self.get_weekly_schedule()


class DailySchedule(models.Model):
    day_of_week = models.SmallIntegerField()
    doctor_schedule = models.ForeignKey(DoctorSchedule, null=False)


class TimeSlot(models.Model):
    daily_schedule = models.ForeignKey(DailySchedule, null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()


class AppointmentRequest(models.Model):
    patient = models.ForeignKey('member.Member', null=False)
    doctor = models.ForeignKey('member.DoctorMember', null=False)
    start_time = models.TimeField()
    end_time = models.TimeField()

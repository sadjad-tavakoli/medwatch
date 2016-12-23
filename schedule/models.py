from django.db import models


class DoctorSchedule(models.Model):
    doctor = models.OneToOneField('member.DoctorMember')
    session_interval = models.PositiveIntegerField()


class DailySchedule(models.Model):
    DAYS_OF_WEEK = (
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WEN', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    )
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    doctor_schedule = models.ForeignKey(DoctorSchedule)


class TimeRange(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    daily_schedule = models.ForeignKey(DailySchedule)

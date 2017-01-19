
from django.contrib import admin

# Register your models here.
from schedule.models import DoctorSchedule, DailySchedule, AppointmentRequest

admin.site.register(DoctorSchedule)
admin.site.register(DailySchedule)
admin.site.register(AppointmentRequest)

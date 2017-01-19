from django.conf.urls import url, include

from schedule.views import DoctorScheduleView

urlpatterns = [
    url(r'^schedule/', DoctorScheduleView.as_view(), name='schedule')
]

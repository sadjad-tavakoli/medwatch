from django.conf.urls import url, include

from schedule.views.doctor import ScheduleView, AppointmentRequestsView

urlpatterns = [
    url(r'^schedule/$', ScheduleView.as_view(), name='schedule'),
    url(r'^requests/$', AppointmentRequestsView.as_view(), name='requests'),
    url(r'^requests/accept/$', AppointmentRequestsView.as_view(), name='requests-accept'),
]

from django.conf.urls import url

from schedule.views.doctor_views import ScheduleView, AppointmentRequestsView, \
    AppointmentRequestResolvingView

urlpatterns = [
    url(r'^doctor/schedule/$', ScheduleView.as_view(), name='schedule'),
    url(r'^requests/$', AppointmentRequestsView.as_view(), name='requests'),
    url(r'^requests/accept/$', AppointmentRequestResolvingView.as_view(), name='requests-accept'),
]

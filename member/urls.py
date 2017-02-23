from django.conf.urls import url, include

from member.views.agents import DefineAgents, RemoveAgents
from member.views.join_views import JoinView, DoctorJoinView, download_contract
from member.views.login_views import LoginView, LogoutView
from member.views.member_views import search_in_doctors, show_doctor_page
from member.views.profile_views import EditProfileView, ProfileView, DrEditProfile
from schedule.views.agent_views import AgentAppointmentsList, AgentEditAppointmentView, \
    AgentCancelAppointments
from schedule.views.member_views import AppointmentsList, CancelAppointments, EditAppointmentView, \
    RequestAppointmentView, GetAppointmentView

profile_url_patterns = [
    url(r'^@(?P<username>\w+)/$', ProfileView.as_view(), name='edit'),
    url(r'^edit/$', EditProfileView.as_view(), name='edit'),
]
patient_url_patterns = [
    url(r'^appointments_list/$', AppointmentsList.as_view(), name='appointment-list'),
    url(r'^search_doctor/$', search_in_doctors, name='search-in-dr'),

    url(r'^cancel_appointment/(?P<appointment_id>\d+)/$', CancelAppointments.as_view(),
        name='cancel-appointment'),
    url(r'^edit_appointment/(?P<appointment_id>\d+)/$', EditAppointmentView.as_view(),
        name='edit-appointment'),

]
agent_url_patterns = [
    url(r'^appointments_list/$', AgentAppointmentsList.as_view(), name='appointment-list'),
    url(r'^cancel_appointment/(?P<appointment_id>\d+)/$', AgentCancelAppointments.as_view(),
        name='cancel-appointment'),
    url(r'^edit_appointment/(?P<appointment_id>\d+)/$', AgentEditAppointmentView.as_view(),
        name='edit-appointment'),

]
doctor_url_patterns = [
    url(r'^agents/$', DefineAgents.as_view(), name='agents-manger'),
    url(r'^remove_agents/(?P<agent_id>\d+)/$', RemoveAgents.as_view(),
        name='remove-agent'),
    url(r'^edit_appointment/(?P<appointment_id>\d+)/$', EditAppointmentView.as_view(),
        name='edit-appointment'),

]
urlpatterns = [
    url(r'^join/$', JoinView.as_view(), name='join'),
    url(r'^dr-join/$', DoctorJoinView.as_view(), name='dr_join'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/', include(profile_url_patterns, namespace='profile')),
    url(r'^patient/', include(patient_url_patterns, namespace='patient')),
    url(r'^doctors/', include(doctor_url_patterns, namespace='doctor')),
    url(r'^agent/', include(agent_url_patterns, namespace='agent')),
    url(r'^contract-download/', download_contract, name='contraction'),
    url(r'^dr-edit-profile/', DrEditProfile.as_view(), name='dr_edit_profile'),
    url(r'^doctors/([0-9]*)/$', show_doctor_page, name='show_dr_page'),
    url(r'^doctors/(?P<doctor_id>[0-9]*)/request/$', RequestAppointmentView.as_view(),
        name='request_appointment'),
    url(
        r'^doctors/(?P<doctor_id>[0-9]*)/request/(?P<day>[0-9]*)_(?P<hour>[0-9]*)_(?P<minute>[0-9]*)/$',
        GetAppointmentView.as_view()),
]

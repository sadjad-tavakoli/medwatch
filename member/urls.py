from django.conf.urls import url, include

from member.views.join_views import JoinView, DoctorJoinView
from member.views.login_views import LoginView, LogoutView
from member.views.profile_views import EditProfileView, ProfileView, DrEditProfile
from schedule.views.member_views import AppointmentsList

profile_url_patterns = [
    url(r'^@(?P<username>\w+)/$', ProfileView.as_view(), name='edit'),
    url(r'^edit/$', EditProfileView.as_view(), name='edit'),

]
patient_url_patterns = [
    url(r'^appointments_list/$', AppointmentsList.as_view(), name='appointment-list'),

]
urlpatterns = [
    url(r'^join/$', JoinView.as_view(), name='join'),
    url(r'^dr-join/$', DoctorJoinView.as_view(), name='dr_join'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/', include(profile_url_patterns, namespace='profile')),
    url(r'^patient/', include(patient_url_patterns, namespace='patient')),

    url(r'^dr-edit-profile/', DrEditProfile.as_view(), name='dr_edit_profile'),
    # url(r'^admin/', include(admin.site.urls)),
]

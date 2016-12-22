from django.conf.urls import url, include

from member.views.join_views import JoinView
from member.views.login_views import LoginView, LogoutView
from member.views.profile_views import EditProfileView, ProfileView

profile_url_patterns = [
    url(r'^@(?P<username>\w+)/$', ProfileView.as_view(), name='edit'),
    url(r'^edit/$', EditProfileView.as_view(), name='edit'),

]
urlpatterns = [
    url(r'^join/$', JoinView.as_view(), name='join'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/', include(profile_url_patterns, namespace='profile'))

]

from django.conf.urls import url

from member.views.join_views import JoinView
from member.views.login_views import LoginView, LogoutView

urlpatterns = [
    url(r'^join/$', JoinView.as_view(), name='join'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),


]

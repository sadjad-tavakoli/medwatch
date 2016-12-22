from django.conf.urls import url

from member.views.join_views import JoinView

urlpatterns = [
    url(r'^join/$', JoinView.as_view(), name='join')

]

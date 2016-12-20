from django.conf.urls import url

from member.views.join_views import SignUpView

urlpatterns = [
    url(r'^sign_up/$', SignUpView.as_view(), name='sign-up')

]

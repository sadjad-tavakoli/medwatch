from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, resolve_url
from django.views.generic import FormView
from django.views.generic.base import View

from med_watch.settings import HOME_REDIRECT_URL
from member.forms.login_forms import LoginForm
from member.models import AbstractMember


class LoginView(FormView):
    template_name = 'member/login.html'
    form_class = LoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(resolve_url(HOME_REDIRECT_URL))
        return super(LoginView, self).get(self, request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        # member = Member.get_member_by_email_username(data['username'])
        user = AbstractMember.get_abstractMember_by_email_username
        user = authenticate(
            username=member.primary_user.username, password=data['password'])
        login(self.request, user)
        return redirect(resolve_url(HOME_REDIRECT_URL))


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(resolve_url(HOME_REDIRECT_URL))

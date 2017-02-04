from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from med_watch.permissions import DoctorPermissionMixin, AgentPermissionMixin
from member.forms.profile_forms import EditProfileForm, DrEditProfileForm
from member.models import Member, DoctorMember


class ProfileView(AgentPermissionMixin, DetailView):
    template_name = 'member/profile.html'
    context_object_name = 'member'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        member = Member.objects.get(primary_user__username=username)
        return member


class DrEditProfile(DoctorPermissionMixin, SuccessMessageMixin, UpdateView):
    model = DoctorMember
    template_name = 'doctor/dr_edit_profile.html'
    form_class = DrEditProfileForm

    def get_object(self, queryset=None):
        obj = self.request.user.doctor_member
        return obj

    def get_initial(self):
        initial = super(DrEditProfile, self).get_initial()
        user = self.object.primary_user
        if user != self.request.user:
            raise SuspiciousOperation()
        initial.update({'username': user.username, 'email': user.email})
        return initial

    def get_success_url(self):
        return reverse('home')

    def form_valid(self, form):
        data = form.cleaned_data

        user = self.request.user
        password = data.get('password', None)
        old_password = data.get('old_password', None)
        if old_password is not None and password is not None:
            if old_password != '' and password != '':
                user.set_password(password)
                user.save()

        return super(DrEditProfile, self).form_valid(form)


class EditProfileView(SuccessMessageMixin, UpdateView):
    model = Member
    template_name = 'member/edit_profile.html'
    form_class = EditProfileForm

    def get_object(self, queryset=None):
        obj = self.request.user.member
        return obj

    def get_initial(self):
        initial = super(EditProfileView, self).get_initial()
        user = self.object.primary_user
        if user != self.request.user:
            raise SuspiciousOperation()
        initial.update({'username': user.username, 'email': user.email})
        return initial

    def get_success_url(self):
        return reverse('members:profile:edit')

    def form_valid(self, form):
        data = form.cleaned_data

        user = self.request.user
        password = data.get('password', None)
        old_password = data.get('old_password', None)
        if old_password is not None and password is not None:
            if old_password != '' and password != '':
                user.set_password(password)
                user.save()

        return super(EditProfileView, self).form_valid(form)


class HomeView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_anonymous():
            return redirect(reverse('members:login'))
        return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_template_names(self):
        self.template_name = self.get_user_template(self.request)
        return super(HomeView, self).get_template_names()

    @staticmethod
    def get_user_template(request):
        if request.access_level.is_doctor():
            return 'home_doctor.html'
        if request.access_level.is_agent():
            return 'home_agent.html'
        if request.access_level.is_member():
            return 'home_member.html'

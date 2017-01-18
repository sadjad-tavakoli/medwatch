from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView

from member.forms.profile_forms import EditProfileForm, DrEditProfileForm
from member.models import Member


class ProfileView(DetailView):
    template_name = 'member/profile.html'
    context_object_name = 'member'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username', None)
        member = Member.objects.get(primary_user__username=username)
        return member


def DrEditProfile(request):
    if request.method == "POST":
        form = DrEditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'doctor/dr_edit_profile.html', {'form': form, 'user': request.user})
    else:
        form = DrEditProfileForm
    return render(request, 'doctor/dr_edit_profile.html', {'form': form, 'user': request.user},
                  context_instance=RequestContext(request))


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

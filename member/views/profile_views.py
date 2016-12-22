from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse
from django.views.generic.edit import UpdateView

from member.forms.profile_forms import EditProfileForm
from member.models import Member


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

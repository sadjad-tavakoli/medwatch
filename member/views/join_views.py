from django.views.generic.edit import CreateView

from member.forms.join_forms import SignUpForm
from member.models import Member


class SignUpView(CreateView):
    template_name = 'member/sign_up.html'
    model = Member
    form_class = SignUpForm

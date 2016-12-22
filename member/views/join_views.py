from django.views.generic.edit import CreateView

from member.forms.join_forms import JoinForm
from member.models import Member


class JoinView(CreateView):
    template_name = 'member/join.html'
    model = Member
    form_class = JoinForm

from django.views.generic.list import ListView

from member.models import Agent, DoctorMember


class AgentsListView(ListView):

    template_name = 'member/agents_list.html'

    def __init__(self, *args, **kwargs):
        self.doctor = None
        super(AgentsListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        current_doctor_user = DoctorMember.objects.filter(primary_user=self.request.user).first()

        self.doctor = current_doctor_user

        if current_doctor_user is None:
            return []

        return Agent.objects.filter(doctor=current_doctor_user)

from django.core.urlresolvers import reverse
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from member.models import Agent, Member


class AgentsListView(ListView):
    template_name = 'member/agents_list.html'

    def __init__(self, *args, **kwargs):
        super(AgentsListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if not self.request.access_level.is_doctor():
            return []

        return self.request.access_level.doctor.agent_set.all()


class DefineAgents(CreateView):
    template_name = 'doctor/define_agent.html'
    model = Agent
    fields = ('member',)

    def get_success_url(self):
        return reverse('members:doctor:agents-manger')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.doctor = self.request.user.doctor_member
        instance.save()
        return super(DefineAgents, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DefineAgents, self).get_context_data(**kwargs)
        context['agents'] = self.request.user.doctor_member.agents.all()
        # context['members'] = Member.objects.all()
        return context

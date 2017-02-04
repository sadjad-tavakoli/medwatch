from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.generic.base import View
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from med_watch.permissions import DoctorPermissionMixin
from member.models import Agent, Member


class AgentsListView(ListView):
    template_name = 'member/agents_list.html'

    def __init__(self, *args, **kwargs):
        super(AgentsListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if not self.request.access_level.is_doctor():
            return []

        return self.request.access_level.doctor.agent_set.all()


class DefineAgents(DoctorPermissionMixin, CreateView):
    template_name = 'doctor/define_agent.html'
    model = Agent
    fields = ('member',)

    def get_success_url(self):
        return reverse('members:doctor:agents-manger')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.doctor = self.request.access_level.doctor
        instance.save()
        return super(DefineAgents, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(DefineAgents, self).get_context_data(**kwargs)
        context['agents'] = self.request.access_level.doctor.agents.all()
        return context


class RemoveAgents(DoctorPermissionMixin, View):
    def get(self, request, *args, **kwargs):
        agent_id = self.kwargs.get('agent_id', None)
        agent = Agent.objects.get(id=agent_id)
        agent.delete()
        return redirect('members:doctor:agents-manger')

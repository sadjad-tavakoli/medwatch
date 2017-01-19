from django.views.generic.list import ListView


class AgentsListView(ListView):
    template_name = 'member/agents_list.html'

    def __init__(self, *args, **kwargs):
        super(AgentsListView, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if not self.request.access_level.is_doctor():
            return []

        return self.request.access_level.doctor.agent_set.all()

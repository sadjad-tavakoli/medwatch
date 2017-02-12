from django.shortcuts import redirect


class AgentPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.access_level.is_agent():
            return super(AgentPermissionMixin, self).dispatch(request, *args, **kwargs)
        return redirect('home')


class DoctorPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.access_level.is_doctor():
            return super(DoctorPermissionMixin, self).dispatch(request, *args, **kwargs)
        return redirect('home')


class MemberPermissionMixin:
    def dispatch(self, request, *args, **kwargs):
        if self.request.access_level.is_member():
            return super(MemberPermissionMixin, self).dispatch(request, *args, **kwargs)
        return redirect('home')

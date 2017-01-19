from abc import ABCMeta, abstractmethod

from member.models import DoctorMember, Agent


class AbstractAccessLevel(metaclass=ABCMeta):
    def is_member(self):
        return False

    def is_doctor(self):
        return False

    def is_agent(self):
        return False

    def has_doctor_privilages(self):
        return False


class AnonymousAccessLevel(AbstractAccessLevel):
    pass


class MemberAccessLevel(AbstractAccessLevel):
    def __init__(self, member):
        self.member = member

    def is_member(self):
        return True


class DoctorAccessLevel(AbstractAccessLevel):
    def __init__(self, doctor):
        self.doctor = doctor

    def is_doctor(self):
        return True

    def has_doctor_privilages(self):
        return True


class AgentAccessLevel(AbstractAccessLevel):
    def __init__(self, agent):
        self.agent = agent
        self.doctor = agent.doctor

    def is_member(self):
        return True

    def is_agent(self):
        return True

    def has_doctor_privilages(self):
        return True


class MemberMiddleware(object):
    def process_request(self, request):
        if request.user.is_anonymous():
            request.access_level = AnonymousAccessLevel()
            return

        doctor_member = DoctorMember.objects.filter(primary_user=request.user).first()
        if doctor_member is not None:
            request.access_level = DoctorAccessLevel(doctor=doctor_member)
            return

        agent = Agent.objects.filter(member__primary_user=request.user).first()
        if agent is not None:
            request.access_level = AgentAccessLevel(agent=agent)
            return

        if hasattr(request.user, 'member'):
            request.access_level = MemberAccessLevel(member=request.user.member)

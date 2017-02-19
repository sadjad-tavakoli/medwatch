from django.core.urlresolvers import reverse
from django.test.client import Client
from django_webtest import WebTest

from member.models import DoctorMember, Agent, Member
from member.tests.test_member_views import TestMixin


class AgentLoginTest(TestMixin, WebTest):
    def setUp(self):
        super(AgentLoginTest, self).setUp()
        self.doctor_join_data.pop('re_password')
        self.doctor = DoctorMember.objects.create(**self.doctor_join_data)
        self.client = Client()
        self.client.login(username=self.doctor_join_data['username'],
                          password=self.doctor_join_data['password'])

    def test_agent_login(self):
        self.join(self.join_data)
        self.member = Member.objects.get(primary_user__username=self.join_data['username'])
        self.client.post(reverse('members:doctor:agents-manger'),
                         data={'member': [self.member.id]})
        self.agent = Agent.objects.get(member=self.member)
        response = self.login(
            data={'username': self.join_data['username'], 'password': self.join_data['password']})
        self.assertTemplateUsed(response, 'home_agent.html')


class AppointmentTest(TestMixin, WebTest):
    def setUp(self):
        super(AppointmentTest, self).setUp()

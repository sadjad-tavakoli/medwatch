from django.test.client import Client
from django_webtest import WebTest
from member.models import DoctorMember, Agent, Member
from member.tests.test_member_views import TestMixin


class DefineAgentTest(TestMixin, WebTest):
    def setUp(self):
        super(DefineAgentTest, self).setUp()
        self.doctor = DoctorMember.objects.create(**self.doctor_join_data)
        self.client = Client()
        self.client.login(username=self.doctor_join_data['username'],
                          password=self.doctor_join_data['password'])

        # def test_define_client(self):
        #     self.join(self.join_data)
        #     self.member = Member.objects.get(primary_user__username=self.join_data['username'])
        #     self.assertEqual(Agent.objects.count(), 0)
        #     form = self.app.get(reverse('members:doctor:agents-manger'),
        #                         user=self.doctor.primary_user).form
        #     form['member'] = self.member
        #     print(response.content)
        #     self.assertEqual(response.status_code, 200)
        # self.assertEqual(Agent.objects.count(), 1)
        # self.assertEqual(Agent.objects.first().member, self.member)

    def test_agent_login(self):
        self.join(self.join_data)
        self.member = Member.objects.last()
        Agent.objects.create(doctor=self.doctor, member=self.member)
        response = self.login(
            data={'username': self.join_data['username'], 'password': self.join_data['password']})
        self.assertTemplateUsed(response, 'agent_member.html')


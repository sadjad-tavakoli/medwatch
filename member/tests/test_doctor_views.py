from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django_webtest import WebTest

from member.models import DoctorMember, Member, Agent
from member.tests.test_member_views import TestMixin


class DoctorJoinLoginTest(TestMixin, WebTest):
    def setUp(self):
        super(DoctorJoinLoginTest, self).setUp()
        self.client = Client()

    def test_join_dr_member_current_data(self):
        last_member_num = DoctorMember.objects.count()
        response = self.client.post(reverse('members:dr_join'), data=self.doctor_join_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(last_member_num + 1, DoctorMember.objects.count())
        self.assertEqual(DoctorMember.objects.last().primary_user.username,
                         self.doctor_join_data['username'])
        self.assertRedirects(response, reverse('members:login'))

    def test_join_member_wrong_username(self):
        last_member_num = DoctorMember.objects.count()
        self.doctor_join_data['username'] = 'sad'
        response = self.client.post(reverse('members:dr_join'), data=self.doctor_join_data)
        self.assertEqual(last_member_num, DoctorMember.objects.count())
        self.assertContains(response, 'Username should be at least 6 characters long.')
        self.doctor_join_data['username'] = 'sa.-.*'
        response = self.client.post(reverse('members:dr_join'), data=self.doctor_join_data)
        self.assertEqual(last_member_num, DoctorMember.objects.count())
        self.assertContains(response,
                            'Valid characters are numbers, lowercase letters and dashes.')

    def test_blank_fields(self):
        response = self.client.get(reverse('members:dr_join'))
        self.assertEqual(response.status_code, 200)
        mem_count = DoctorMember.objects.count()
        self.doctor_join_data.update({'username': ""})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertFormError(response, 'form', 'username', ['This field is required.'])
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.doctor_join_data.update({'username': "medwatch"})
        response = self.client.post(reverse('members:dr_join'), data=self.doctor_join_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mem_count + 1, DoctorMember.objects.count())
        self.assertEqual(DoctorMember.objects.last().primary_user.username,
                         self.doctor_join_data['username'])

        User.objects.last().delete()
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.doctor_join_data.update({'password': ""})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.assertFormError(response, 'form', 'password', ['This field is required.'])
        self.doctor_join_data.update({'password': "medwatch123"})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mem_count + 1, DoctorMember.objects.count())
        self.assertEqual(DoctorMember.objects.last().primary_user.username,
                         self.doctor_join_data['username'])
        User.objects.last().delete()
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.doctor_join_data.update({'password': "", 'first_name': "", 'last_name': "",
                                      'national_id': ""})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.assertFormError(response, 'form', 'password', ['This field is required.'])
        self.assertFormError(response, 'form', 'national_id', ['This field is required.'])

    def test_password_matching(self):
        response = self.client.get(reverse('members:dr_join'))
        self.assertEqual(response.status_code, 200)
        mem_count = DoctorMember.objects.count()
        password = self.doctor_join_data['password']
        self.doctor_join_data.update({'password': 'nomatching'})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertContains(response, 'Passwords not match.')
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.doctor_join_data.update({'password': ''})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertNotContains(response, 'Passwords not match.')
        self.assertFormError(response, 'form', 'password', ['This field is required.'])
        self.assertEqual(mem_count, DoctorMember.objects.count())
        self.doctor_join_data.update({'password': password, 're_password': ""})
        response = self.client.post(reverse('members:dr_join'),
                                    data=self.doctor_join_data)
        self.assertNotContains(response, 'Passwords not match.')
        self.assertFormError(response, 'form', 're_password', ['This field is required.'])
        self.assertEqual(mem_count, DoctorMember.objects.count())

    def test_duplicate_username_or_email(self):
        self.client.post(reverse('members:dr_join'), data=self.doctor_join_data, follow=True)
        email = self.doctor_join_data['email']
        self.doctor_join_data.update({'email': 'sadkad@adad.com'})
        username_response = self.client.post(reverse('members:dr_join'), self.doctor_join_data,
                                             follow=True)
        self.assertContains(username_response, 'Your username already exists')
        self.doctor_join_data.update({'username': 'sasasasasa', 'email': email})
        email_response = self.client.post(reverse('members:dr_join'), self.doctor_join_data,
                                          follow=True)
        self.assertContains(
            email_response, 'Your email address already exists')

        self.join(data=self.join_data)
        self.doctor_join_data.update({'email': self.join_data['email']})
        response = self.doctor_join(data=self.doctor_join_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(DoctorMember.objects.last().primary_user.username,
                         self.doctor_join_data['username'])

    def test_login_user(self):
        self.client.post(reverse('members:dr_join'), data=self.doctor_join_data)
        response = self.client.post(reverse('members:login'), data=self.doctor_login_data,
                                    follow=True)
        self.assertTemplateUsed(response, 'home_doctor.html')
        response = self.client.get(reverse('members:login'))
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.assertNotIn(container=self.client.session, member='_auth_user_id')
        response = self.client.post(reverse('members:login'), data=self.doctor_login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertIn(container=self.client.session, member='_auth_user_id')
        self.client.logout()
        self.assertNotIn(container=self.client.session, member='_auth_user_id')
        password = self.doctor_join_data['password']
        self.doctor_login_data.update({'password': 'passqalat'})
        response = self.client.post(reverse('members:login'),
                                    data=self.doctor_login_data)
        self.assertContains(response, 'Username or Password is incorrect')
        response = self.client.get(path=reverse('members:login'))
        self.assertEqual(response.status_code, 200)
        self.doctor_login_data.update({'password': password})
        response = self.client.post(reverse('members:login'), data=self.doctor_login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertIn(container=self.client.session, member='_auth_user_id')
        response = self.client.get(path=reverse('members:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))


class DefineAgentsTest(TestMixin, WebTest):
    def setUp(self):
        super(DefineAgentsTest, self).setUp()
        self.doctor_join_data.pop('re_password')
        self.doctor = DoctorMember.objects.create(**self.doctor_join_data)
        self.client = Client()
        self.client.login(username=self.doctor_join_data['username'],
                          password=self.doctor_join_data['password'])

    def test_define_agent(self):
        self.join(self.join_data)
        self.member = Member.objects.get(primary_user__username=self.join_data['username'])
        self.assertEqual(Agent.objects.count(), 0)
        response = self.client.post(reverse('members:doctor:agents-manger'),
                                    data={'member': [self.member.id]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Agent.objects.count(), 1)
        self.assertEqual(Agent.objects.first().member, self.member)

    def test_delete_agent(self):
        self.join(self.join_data)
        self.member1 = Member.objects.get(primary_user__username=self.join_data['username'])
        self.join_data.update({'username': 'user22', 'email': 'enmail22@dsf.com'})
        self.join(self.join_data)
        self.member2 = Member.objects.get(primary_user__username=self.join_data['username'])
        self.client.post(reverse('members:doctor:agents-manger'),
                         data={'member': [self.member1.id]})
        self.client.post(reverse('members:doctor:agents-manger'),
                         data={'member': [self.member2.id]})
        self.assertEqual(self.doctor.agents.count(), 2)
        self.agent1 = Agent.objects.get(member=self.member1)

        response = self.client.get(
            reverse('members:doctor:remove-agent', kwargs={'agent_id': self.agent1.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.doctor.agents.count(), 1)
        self.assertEqual(self.doctor.agents.first().member, self.member2)

    def test_define_assign_agents(self):
        self.join(self.join_data)
        self.member1 = Member.objects.get(primary_user__username=self.join_data['username'])
        self.join_data.update({'username': 'user22', 'email': 'enmail22@dsf.com'})
        self.join(self.join_data)
        self.member2 = Member.objects.get(primary_user__username=self.join_data['username'])
        self.doctor_join_data.update({'username': 'docotr22', 'email': 'emailjadid@ad.ad'})
        self.doctor_join_data['re_password'] = self.doctor_join_data['password']
        self.doctor_join(self.doctor_join_data)
        self.doctor2 = DoctorMember.objects.get(primary_user__username='docotr22')
        self.client.post(reverse('members:doctor:agents-manger'),
                         data={'member': [self.member1.id]})
        self.assertEqual(self.doctor.agents.count(), 1)
        self.client.logout()
        self.login(
            {'username': 'docotr22', 'password': self.doctor_join_data['password']})
        response = self.client.post(reverse('members:doctor:agents-manger'),
                                    data={'member': [self.member1.id]})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Agent with this Member already exists.')
        self.assertEqual(self.doctor2.agents.count(), 0)
        self.assertEqual(self.doctor.agents.count(), 1)
        self.assertEqual(self.doctor.agents.last().member, self.member1)
        response = self.client.post(reverse('members:doctor:agents-manger'),
                                    data={'member': [self.member2.id]})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.doctor2.agents.count(), 1)
        self.assertEqual(self.doctor.agents.count(), 1)
        self.assertEqual(self.doctor.agents.last().member, self.member1)
        self.assertEqual(self.doctor2.agents.last().member, self.member2)

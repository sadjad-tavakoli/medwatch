from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client
from django_webtest import WebTest
from member.models import Member


class JoinTest(WebTest):
    def setUp(self):
        self.client = Client()
        self.join_data = {
            'first_name': 'sadjad',
            'last_name': 'tavakoli',
            'email': 'tavakoli@gmail.com',
            'national_id': '2138888888',
            'username': 'sadjad',
            'password': 'sadjad123',
            're_password': 'sadjad123',
        }
        self.login_data = {
            'username': 'sadjad',
            'password': 'sadjad123'
        }

    def test_join_member_current_data(self):
        last_member_num = Member.objects.count()
        response = self.client.post(reverse('members:join'), data=self.join_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(last_member_num + 1, Member.objects.count())
        self.assertEqual(Member.objects.last().primary_user.username, self.join_data['username'])
        self.assertRedirects(response, reverse('members:login'))

    def test_join_member_wrong_username(self):
        last_member_num = Member.objects.count()
        self.join_data['username'] = 'sad'
        response = self.client.post(reverse('members:join'), data=self.join_data)
        self.assertEqual(last_member_num, Member.objects.count())
        self.assertContains(response, 'Username should be at least 6 characters long.')
        self.join_data['username'] = 'sa.-.*'
        response = self.client.post(reverse('members:join'), data=self.join_data)
        self.assertEqual(last_member_num, Member.objects.count())
        self.assertContains(response,
                            'Valid characters are numbers, lowercase letters and dashes.')

    def test_blank_fields(self):
        response = self.client.get(reverse('members:join'))
        self.assertEqual(response.status_code, 200)
        mem_count = Member.objects.count()
        self.join_data.update({'username': ""})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertFormError(response, 'form', 'username', ['This field is required.'])
        self.assertEqual(mem_count, Member.objects.count())
        self.join_data.update({'username': "sadjad"})
        response = self.client.post(reverse('members:join'), data=self.join_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mem_count + 1, Member.objects.count())
        self.assertEqual(Member.objects.last().primary_user.username, self.join_data['username'])

        User.objects.last().delete()
        self.assertEqual(mem_count, Member.objects.count())
        self.join_data.update({'password': ""})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mem_count, Member.objects.count())
        self.assertFormError(response, 'form', 'password', ['This field is required.'])
        self.join_data.update({'password': "sadjad123"})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(mem_count + 1, Member.objects.count())
        self.assertEqual(Member.objects.last().primary_user.username, self.join_data['username'])
        User.objects.last().delete()
        self.assertEqual(mem_count, Member.objects.count())
        self.join_data.update({'password': "", 'first_name': "", 'last_name': "",
                               'national_id': ""})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(mem_count, Member.objects.count())
        self.assertFormError(response, 'form', 'password', ['This field is required.'])
        self.assertFormError(response, 'form', 'national_id', ['This field is required.'])

    def test_password_matching(self):
        response = self.client.get(reverse('members:join'))
        self.assertEqual(response.status_code, 200)
        mem_count = Member.objects.count()
        password = self.join_data['password']
        self.join_data.update({'password': 'nomatching'})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertContains(response, 'Passwords not match.')
        self.assertEqual(mem_count, Member.objects.count())
        self.join_data.update({'password': ''})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertNotContains(response, 'Passwords not match.')
        self.assertFormError(response, 'form', 'password', ['This field is required.'])
        self.assertEqual(mem_count, Member.objects.count())
        self.join_data.update({'password': password,'re_password': ""})
        response = self.client.post(reverse('members:join'),
                                    data=self.join_data)
        self.assertNotContains(response, 'Passwords not match.')
        self.assertFormError(response, 'form', 're_password', ['This field is required.'])
        self.assertEqual(mem_count, Member.objects.count())

    def test_duplicate_username_or_email(self):
        self.client.post(reverse('members:join'), data=self.join_data, follow=True)
        email = self.join_data['email']
        self.join_data.update({'email': 'sadkad@adad.com'})
        username_response = self.client.post(reverse('members:join'), self.join_data, follow=True)
        self.assertContains(username_response, 'Your username already exists')
        self.join_data.update({'username': 'sasasasasa', 'email': email})
        email_response = self.client.post(reverse('members:join'), self.join_data, follow=True)
        self.assertContains(
            email_response, 'Your email address already exists')

    def test_login_user(self):
        self.client.post(reverse('members:join'), data=self.join_data)
        self.client.post(reverse('members:login'), data=self.login_data)

        response = self.client.get(reverse('members:login'))
        self.assertEqual(response.status_code, 302)
        self.client.logout()
        self.assertNotIn(container=self.client.session, member='_auth_user_id')
        response = self.client.post(reverse('members:login'), data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertIn(container=self.client.session, member='_auth_user_id')
        self.client.logout()
        self.assertNotIn(container=self.client.session, member='_auth_user_id')
        password = self.join_data['password']
        self.login_data.update({'password': 'passqalat'})
        response = self.client.post(reverse('members:login'),
                                    data=self.login_data)
        self.assertContains(response, 'Username or Password is incorrect')
        response = self.client.get(path=reverse('members:login'))
        self.assertEqual(response.status_code, 200)
        self.login_data.update({'password': password})
        response = self.client.post(reverse('members:login'), data=self.login_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))
        self.assertIn(container=self.client.session, member='_auth_user_id')
        response = self.client.get(path=reverse('members:login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('home'))

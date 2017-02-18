from django import forms
from django.forms import Form
from member.models import AbstractMember


class LoginForm(Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        data = self.cleaned_data
        username_or_email = data.get('username', None)
        member, is_doctor = AbstractMember.get_member_by_email_username(username_or_email)
        if member is None:
            raise forms.ValidationError("username not valid")
        password = data.get('password', None)
        if not member.primary_user.check_password(password):
            raise forms.ValidationError('Username or Password is incorrect')
        return password

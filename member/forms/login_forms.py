from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _

from member.models import Member


class LoginForm(Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        data = self.cleaned_data
        username_or_email = data.get('username', None)
        member = Member.get_member_by_email_username(username_or_email)
        if member is None:
            raise forms.ValidationError(_("نام کاربری یا گذرواژه نادرست است"))
        password = data.get('password', None)
        if not member.primary_user.check_password(password):
            raise forms.ValidationError(_("نام کاربری یا گذرواژه نادرست است"))
        return password
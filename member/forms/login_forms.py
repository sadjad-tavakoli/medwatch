from django import forms
from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from member.models import Member, AbstractMember


class LoginForm(Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        data = self.cleaned_data
        username_or_email = data.get('username', None)
        print(AbstractMember.get_member_by_email_username(username_or_email))
        member, is_doctor = AbstractMember.get_member_by_email_username(username_or_email)
        if member is None:
            raise forms.ValidationError(_("username not valid"))
        password = data.get('password', None)
        if not member.primary_user.check_password(password):
            raise forms.ValidationError(_("username or password not correct"))
        return password

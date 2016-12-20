from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms.models import fields_for_model

from member.models import Member

username_regex = RegexValidator(regex=r'^[-a-z0-9_]+\Z',
                                message='Valid characters are numbers, lowercase '
                                        'letters and dashes.')


class SignUpForm(forms.ModelForm):
    username = fields_for_model(User)['username']
    email = fields_for_model(User)['email']
    password = fields_for_model(User)['password']
    re_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['email'].required = True
        self.fields['username'].validators = [username_regex]

    class Meta:
        model = Member
        exclude = ('primary_user',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            Member.objects.get(primary_user__email=email)
            raise forms.ValidationError('Your email address already exists')
        except Member.DoesNotExist:
            return email

    def clean(self):
        password = self.cleaned_data.get('password')
        re_password = self.cleaned_data.get('re_password')
        if re_password is not None and password is not None:
            if password != re_password:
                raise forms.ValidationError('Passwords not match.')
        return self.cleaned_data

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) < 6:
            raise forms.ValidationError(
                'Username should be at least 6 characters long.'
            )
        try:
            Member.objects.get(primary_user__username=username)
            raise forms.ValidationError('Your username already exists')
        except Member.DoesNotExist:
            pass
        return username

    def save(self, commit=True):
        data = self.cleaned_data
        member = Member.objects.create(username=data['username'],
                                       password=data['password'],
                                       national_id=data['national_id'],
                                       email=data['email'])
        return member

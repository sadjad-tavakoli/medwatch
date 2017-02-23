from django import forms
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.models import User
from django.forms.models import fields_for_model

from med_watch.model_mixins import username_regex
from member.models import Member, DoctorMember, AbstractMember


class JoinForm(forms.ModelForm):
    username = fields_for_model(User)['username']
    email = fields_for_model(User)['email']
    password = fields_for_model(User)['password']
    re_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(JoinForm, self).__init__(*args, **kwargs)
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
        except DoctorMember.DoesNotExist:
            pass
        except Member.DoesNotExist:
            pass
        return username

    def save(self, commit=True):
        data = self.cleaned_data
        member = Member.objects.create(username=data['username'],
                                       password=data['password'],
                                       national_id=data['national_id'],
                                       email=data['email'],
                                       first_name=data['first_name'],
                                       last_name=data['last_name'],
                                       )
        return member


class DoctorJoinForm(forms.ModelForm):
    username = fields_for_model(User)['username']
    email = fields_for_model(User)['email']
    password = fields_for_model(User)['password']
    re_password = forms.CharField(widget=forms.PasswordInput())
    contraction = forms.FileField(widget=AdminFileWidget, required=False)

    def __init__(self, *args, **kwargs):
        super(DoctorJoinForm, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['email'].required = True
        self.fields['username'].validators = [username_regex]

    class Meta:
        model = DoctorMember
        exclude = ('primary_user',)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            DoctorMember.objects.get(primary_user__email=email)
            raise forms.ValidationError('Your email address already exists')
        except DoctorMember.DoesNotExist:
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
            DoctorMember.objects.get(primary_user__username=username)
            raise forms.ValidationError('Your username already exists')
        except AbstractMember.DoesNotExist or Member.DoesNotExist:
            pass
        return username

    def save(self, commit=True):
        data = self.cleaned_data
        member = DoctorMember.objects.create(username=data['username'],
                                             password=data['password'],
                                             degree=data['degree'],
                                             university=data['university'],
                                             graduate_year=data['graduate_year'],
                                             profile_picture=data['profile_picture'],
                                             contraction=data['contraction'],
                                             national_id=data['national_id'],
                                             email=data['email'],
                                             first_name=data['first_name'],
                                             last_name=data['last_name'],
                                             address=data['address'])
        return member

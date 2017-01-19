from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm, fields_for_model
from django.forms.widgets import PasswordInput
from django.utils.translation import ugettext_lazy as _

from member.models import Member, DoctorMember


class EditProfileForm(ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        max_length=fields_for_model(User)['username'].max_length,
        label=_('Username')
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'readonly': 'readonly'}),
        max_length=fields_for_model(User)['email'].max_length,
        label=_('Email')
    )
    old_password = forms.CharField(
        widget=PasswordInput(),
        max_length=fields_for_model(User)['password'].max_length,
        required=False,
        label=_('Old Password')
    )
    password = forms.CharField(
        widget=PasswordInput(),
        max_length=fields_for_model(User)['password'].max_length,
        required=False,
        label=_('New Password')
    )
    confirm_password = forms.CharField(
        widget=PasswordInput(),
        max_length=fields_for_model(User)['password'].max_length,
        required=False,
        label=_('Confirm Password')
    )
    profile_picture = forms.ImageField(
        required=False,
        error_messages={
            'invalid': _("Image files only")},
        label=_('Profile Picture')
    )

    class Meta:
        model = Member
        fields = (
            'username', 'email', 'old_password', 'password', 'confirm_password', 'first_name',
            'last_name', 'profile_picture')

    def clean(self):
        data = self.cleaned_data
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        old_password = data.get('old_password', None)

        if not data.get('profile_picture'):
            data['profile_picture'] = None

        if old_password is not None and password is not None:
            if old_password != '' and password != '':
                user = authenticate(
                    username=data.get('username', None), password=old_password)
                if user is None or not user.is_active:
                    raise forms.ValidationError(_('Old password is incorrect'))
                if password != confirm_password:
                    raise ValidationError(
                        _('Password does not match the confirmed password'))


class DrEditProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorMember
        fields = ['first_name', 'last_name', 'degree', 'university', 'graduate_year']

    def clean_first_name(self):
        data = self.cleaned_data.get('first_name', '')
        if len(data) == 0:
            raise forms.ValidationError("Your first name can't be empty.")
        return data

    def clean_last_name(self):
        data = self.cleaned_data.get('last_name', '')
        if len(data) == 0:
            raise forms.ValidationError("Your last name can't be empty.")
        return data

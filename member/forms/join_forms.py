from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.forms.models import fields_for_model
from member import models
from member.models import Member, DoctorMember, AbstractMember

username_regex = RegexValidator(regex=r'^[-a-z0-9_]+\Z',
                                message='Valid characters are numbers, lowercase '
                                        'letters and dashes.')


class DrJoinForm(forms.Form):
    firstName = forms.CharField(max_length=100, required=True,
                                widget=forms.TextInput(
                                    attrs={'class': 'input-field', 'placeholder': 'نام'}))
    lastName = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'input-field', 'placeholder': 'نام خانوادگی'}))
    national_id = forms.IntegerField(max_value=9999999999, required=True,
                                     widget=forms.TextInput(
                                         attrs={'class': 'input-field', 'placeholder': 'کد ملی'}))

    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'input-field', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'رمز عبور', 'class': 'input-field'}),
        required=True)
    passwordRepeat = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'تکرار رمز عبور', 'class': 'input-field'}), required=True)
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'پست الکترونیک'}))
    degree = forms.CharField(max_length=100, required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'input-field', 'placeholder': 'مدرک تحصیلی'}))
    university = forms.CharField(max_length=100, required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'input-field',
                                            'placeholder': 'دانشگاه فارغ التحصیلی'}))
    graduate_year = forms.IntegerField(required=True,
                                       widget=forms.TextInput(
                                           attrs={'class': 'input-field',
                                                  'placeholder': 'سال اخذ مدرک'}))

    def clean(self):
        cleaned = super(DrJoinForm, self).clean()
        password = cleaned.get('password')
        passwordRepeat = cleaned.get('passwordRepeat')
        email = cleaned.get('email')
        username = cleaned.get('username')
        firstName = cleaned.get('firstName')
        lastName = cleaned.get('lastName')
        user = models.User(username=username)
        try:
            user = DoctorMember.objects.get(primary_user=user)
            self.errors['username'] = 'نام کاربری تکراری است'
            return
        except DoctorMember.DoesNotExist:
            if password != passwordRepeat:
                self.errors['passwordRepeat'] = 'رمز عبور همخوانی ندارد'
                return
            if email is None:
                self.errors['email'] = 'پست الکترونیکی اشتباه است'
                return
            if firstName is None:
                self.errors['firstName'] = 'نام خود را وارد کنید'
                return
            if lastName is None:
                self.errors['lastName'] = 'نام خود را وارد کنید'
                return
        return


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
            DoctorMember.objects.get(primary_user__username=username)
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
                                       email=data['email'])
        return member


class DoctorJoinForm(forms.ModelForm):
    username = fields_for_model(User)['username']
    email = fields_for_model(User)['email']
    password = fields_for_model(User)['password']
    re_password = forms.CharField(widget=forms.PasswordInput())

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
            Member.objects.get(primary_user__username=username)
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
                                             national_id=data['national_id'],
                                             email=data['email'])
        return member

from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from member import models
from member.forms.join_forms import JoinForm, DrJoinForm, DoctorJoinForm
from member.models import Member, DoctorMember


class JoinView(CreateView):
    template_name = 'member/join.html'
    model = Member
    form_class = JoinForm

    def get_success_url(self):
        return reverse('home')


class DoctorJoinView(CreateView):
    template_name = 'member/join.html'
    model = DoctorMember
    form_class = DoctorJoinForm

    def get_success_url(self):
        return reverse('home')


def DrJoinView(request):
    if request.method == 'POST':
        register_form = DrJoinForm(request.POST)
        if register_form.is_valid():
            register_form.clean()
            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password']
            firstName = register_form.cleaned_data['firstName']
            lastName = register_form.cleaned_data['lastName']
            national_id = register_form.cleaned_data['national_id']
            email = register_form.cleaned_data['email']
            degree = register_form.cleaned_data['degree']
            university = register_form.cleaned_data['university']
            graduate_year = register_form.cleaned_data['graduate_year']
            user = models.User()
            user.username = username
            user.set_password(password)
            user.first_name = firstName
            user.last_name = lastName
            user.email = email
            user.save()
            # login(request, new_user)
            doctor = models.DoctorMember.objects.create(primary_user=user, national_id=national_id,
                                                        degree=degree,
                                                        university=university,
                                                        graduate_year=graduate_year)
            doctor.first_name = firstName
            doctor.last_name = lastName
            doctor.save()

            return HttpResponseRedirect('/register-done/')
    else:
        register_form = DrJoinForm()
    return render(request, 'doctor/dr_join.html',
                  {'form': register_form, 'form_title': 'ثبت نام پزشک', 'submit_value': 'ثبت نام'})


def register_done(request):
    return render(request, 'doctor/dr_edit_profile.html')

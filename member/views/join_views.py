import os
from django.core.urlresolvers import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from member import models
from member.forms.join_forms import JoinForm, DoctorJoinForm
from member.models import Member, DoctorMember
from django.views.static import serve


class JoinView(CreateView):
    template_name = 'member/join.html'
    model = Member
    form_class = JoinForm

    def get_success_url(self):
        print("sasasaasas")
        return reverse('members:login')


class DoctorJoinView(CreateView):
    template_name = 'member/dr_join.html'
    model = DoctorMember
    form_class = DoctorJoinForm

    def get_success_url(self):
        return reverse('members:login')


def download_contract(request):
    url = 'member/static/used/agreement_Template.doc'
    return serve(request, os.path.basename(url), os.path.dirname(url))

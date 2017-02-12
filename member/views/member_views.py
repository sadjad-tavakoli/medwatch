from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import render

# from member
from member import models

def SearchInDoctors(request):

    name = request.POST.get('name_search', "")
    str = name.split(" ")
    result_doctors = []
    for item in str:
        # if models.DoctorMember.objects.filter(Q(first_name=item) | Q(last_name=item)):
            models.DoctorMember.objects.filter()
            print("appendid")
            result_doctors.append(models.DoctorMember.objects.filter(Q(first_name=item) | Q(last_name=item)))

    print(result_doctors)


    return render(request, 'member/search_in_doctors.html', {'result_doctors': result_doctors})
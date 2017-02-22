from django.views.generic.base import View
from django.db.models import Q
from django.shortcuts import render

# from member
from member import models

def SearchInDoctors(request):

    result_doctors = []
    if request.method == "POST":
        name = request.POST.get('name_search', "")
        address = request.POST.get('address_search', "")
        name_words = name.split(" ")
        result_doctors = models.DoctorMember.objects.filter(Q(first_name__in=name_words) | Q(last_name__in=name_words) | Q(address=address)
                                                            | Q(address__icontains=address))

    return render(request, 'member/search_in_doctors.html', {'result_doctors': result_doctors})

def ShowDoctorPage(request, dr_id):
    doctor = models.DoctorMember.objects.get(pk=dr_id)
    agents = models.Agent.objects.filter(doctor=doctor)
    return render(request, 'doctor/show_dr_page.html', {'doctor': doctor, 'agents': agents })


def DoctorsInNeighbourhood(request):

    return render(request, 'member/dr_in_neighbourhood.html')

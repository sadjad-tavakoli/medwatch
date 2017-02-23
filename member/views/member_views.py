from django.shortcuts import render

from member import models


def search_in_doctors(request):
    result_doctors = []
    if request.method == "POST":
        name = request.POST.get('name_search', "")
        address = request.POST.get('address_search', "")
        address_words = address.split(" ")
        name_words = name.split(" ")
        result_doctors = []
        for doctor in models.DoctorMember.objects.all():
            if name.strip() != "" and address.strip() != "":
                for name_word in name_words:
                    if doctor.first_name is not None:
                        doctor_name_words = doctor.first_name.split(" ")
                        for doctor_name_word in doctor_name_words:
                            if doctor_name_word.lower().__contains__(name_word):
                                result_doctors.append(doctor)
                    if doctor.last_name is not None:
                        doctor_name_words = doctor.last_name.split(" ")
                        for doctor_name_word in doctor_name_words:
                            if doctor_name_word.lower().__contains__(name_word):
                                result_doctors.append(doctor)
                    if doctor.primary_user.username.__contains__(name_word):
                            result_doctors.append(doctor)

                for address_word in address_words:
                    if doctor.address is not None:
                        doctor_address_words = doctor.address.split(" ")
                        for doctor_address_word in doctor_address_words:
                            if not doctor_address_word.lower().__contains__(address_word):
                                if result_doctors.__contains__(doctor):
                                    result_doctors.remove(doctor)
            if name.strip() != "" and address.strip() == "":
                for name_word in name_words:
                    if doctor.first_name is not None:
                        doctor_name_words = doctor.first_name.split(" ")
                        for doctor_name_word in doctor_name_words:
                            if doctor_name_word.lower().__contains__(name_word):
                                result_doctors.append(doctor)
                    if doctor.last_name is not None:
                        doctor_name_words = doctor.last_name.split(" ")
                        for doctor_name_word in doctor_name_words:
                            if doctor_name_word.lower().__contains__(name_word):
                                result_doctors.append(doctor)
                    if doctor.primary_user.username.__contains__(name_word):
                        result_doctors.append(doctor)

            if name.strip() == "" and address.strip() != "":
                for address_word in address_words:
                    if doctor.address is not None:
                        doctor_address_words = doctor.address.split(" ")
                        for doctor_address_word in doctor_address_words:
                            if doctor_address_word.lower().__contains__(address_word):
                                result_doctors.append(doctor)
            if name.strip() == "" and address.strip() == "":
                result_doctors.append(doctor)

        result_doctors = set(result_doctors)

    return render(request, 'member/search_in_doctors.html', {'result_doctors': result_doctors})


def show_doctor_page(request, dr_id):
    doctor = models.DoctorMember.objects.get(pk=dr_id)
    agents = models.Agent.objects.filter(doctor=doctor)
    return render(request, 'doctor/show_dr_page.html', {'doctor': doctor, 'agents': agents})

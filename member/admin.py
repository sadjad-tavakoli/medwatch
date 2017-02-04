from django.contrib import admin

from member.models import AbstractMember, DoctorMember, Member, Agent

admin.site.register(AbstractMember)
admin.site.register(DoctorMember)
admin.site.register(Member)
admin.site.register(Agent)

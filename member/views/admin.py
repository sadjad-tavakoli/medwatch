from django.contrib import admin
from django.contrib.auth.models import User

from member.models import Member

admin.site.register(User)
admin.site.register(Member)

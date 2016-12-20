from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import ImageField
from polymorphic.models import PolymorphicModel


class AbstractMember(PolymorphicModel):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    national_id = models.IntegerField()
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = ImageField(upload_to='profile_pictures/', null=True, blank=True)


class DoctorMember(AbstractMember):
    primary_user = models.OneToOneField(User, related_name='doctor_member')


class MemberManager(models.Manager):
    @staticmethod
    def create_member_for_user(primary_user, **kwargs):
        member = Member(primary_user=primary_user, **kwargs)
        member.save()
        return member

    @staticmethod
    def create(username=None, national_id=None, password=None, email=None, primary_user=None,
               birth_date=None, profile_picture=None,
               first_name=None, last_name=None):
        if primary_user is not None:
            username = primary_user.get('username', username)
            password = primary_user.get('password', password)
            email = primary_user.get('email', email)
        primary_user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email)

        member = MemberManager.create_member_for_user(primary_user=primary_user,
                                                      birth_date=birth_date,
                                                      profile_picture=profile_picture,
                                                      first_name=first_name,
                                                      last_name=last_name,
                                                      national_id=national_id)

        return member


class Member(AbstractMember):
    primary_user = models.OneToOneField(User, related_name='member')
    objects = MemberManager()

    @staticmethod
    def get_member_by_email_username(email_username):
        try:
            if '@' in email_username:
                kwargs = {'email': email_username}
            else:
                kwargs = {'username': email_username}
            user = User.objects.get(**kwargs)
            if user.is_superuser and not hasattr(user, 'member'):
                Member.objects.create_member_for_user(primary_user=user, is_verify=True)
            return user.member
        except(TypeError, User.DoesNotExist, User.MultipleObjectsReturned):
            return None

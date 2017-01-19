from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import ImageField
from polymorphic.models import PolymorphicModel


class AbstractMember(PolymorphicModel):
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    national_id = models.IntegerField()
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return '{} - {} - {} '.format(self.first_name, self.last_name, self.national_id)

    @staticmethod
    def get_member_by_email_username(email_username):
        try:
            if '@' in email_username:
                kwargs = {'email': email_username}
            else:
                kwargs = {'username': email_username}
            user = User.objects.get(**kwargs)
            if hasattr(user, 'member'):
                return user.member, False
            if hasattr(user, 'doctor_member'):
                return user.doctor_member, True
        except(TypeError, User.DoesNotExist, User.MultipleObjectsReturned):
            return None, None


class DoctorMemberManager(models.Manager):
    @staticmethod
    def create_doctor_member_for_user(primary_user, **kwargs):
        member = DoctorMember(primary_user=primary_user, **kwargs)
        member.save()
        return member

    @staticmethod
    def create(username=None, national_id=None, password=None, email=None, primary_user=None,
               birth_date=None, university=None, graduate_year=None, degree=None, first_name=None,
               last_name=None):
        if primary_user is not None:
            username = primary_user.get('username', username)
            password = primary_user.get('password', password)
            email = primary_user.get('email', email)
        primary_user = User.objects.create_user(username=username,
                                                password=password,
                                                email=email)

        member = DoctorMemberManager.create_doctor_member_for_user(primary_user=primary_user,
                                                                   birth_date=birth_date,
                                                                   first_name=first_name,
                                                                   degree=degree,
                                                                   university=university,
                                                                   graduate_year=graduate_year,
                                                                   last_name=last_name,
                                                                   national_id=national_id)

        return member


class DoctorMember(AbstractMember):
    primary_user = models.OneToOneField(User, related_name='doctor_member')
    degree = models.CharField(choices='DEGREECHOICES', max_length=40, null=False, default='g')
    university = models.CharField(max_length=50, null=False, blank=True)
    graduate_year = models.IntegerField(default=1360)
    objects = DoctorMemberManager()

    def __str__(self):
        return '{} - {} - {} - {}'.format(self.primary_user, self.degree, self.university,
                                          self.graduate_year)


#
DEGREECHOICES = (
    ('g', 'general practitioner'),
    ('s', 'specialist'),
    ('e', 'expert')
)


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


class Agent(models.Model):
    doctor = models.ForeignKey(DoctorMember, null=False)
    member = models.ForeignKey(Member, null=False)

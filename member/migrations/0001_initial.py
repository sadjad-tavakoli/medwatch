# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2017-02-23 09:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AbstractMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='/profile_pictures/')),
                ('national_id', models.IntegerField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='DoctorMember',
            fields=[
                ('abstractmember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='member.AbstractMember')),
                ('degree', models.CharField(choices=[('g', 'general practitioner'), ('s', 'specialist'), ('e', 'expert')], default='g', max_length=40)),
                ('university', models.CharField(blank=True, max_length=50)),
                ('graduate_year', models.IntegerField(default=1360)),
                ('contraction', models.FileField(blank=True, null=True, upload_to='contractions/')),
                ('address', models.CharField(default='', max_length=200)),
                ('primary_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('member.abstractmember',),
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('abstractmember_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='member.AbstractMember')),
                ('primary_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('member.abstractmember',),
        ),
        migrations.AddField(
            model_name='abstractmember',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_member.abstractmember_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='agent',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='agents', to='member.DoctorMember'),
        ),
        migrations.AddField(
            model_name='agent',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='member.Member'),
        ),
    ]

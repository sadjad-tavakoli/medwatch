# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='abstractmember',
            name='birth_date',
        ),
        migrations.AddField(
            model_name='doctormember',
            name='contraction',
            field=models.FileField(default=None, upload_to='contractions/'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='abstractmember',
            name='profile_picture',
            field=models.ImageField(upload_to='profile_pictures/'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='doctor',
            field=models.ForeignKey(related_name='agents', to='member.DoctorMember'),
        ),
        migrations.AlterField(
            model_name='agent',
            name='member',
            field=models.OneToOneField(to='member.Member'),
        ),
        migrations.AlterField(
            model_name='doctormember',
            name='degree',
            field=models.CharField(max_length=40, default='g', choices=[('g', 'general practitioner'), ('s', 'specialist'), ('e', 'expert')]),
        ),
    ]

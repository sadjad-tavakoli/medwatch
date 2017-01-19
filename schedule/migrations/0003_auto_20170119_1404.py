# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0002_dailyschedule_doctor_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('schedule.appointmentrequest',),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='state',
            field=models.CharField(max_length=1, default='N', choices=[('N', 'Requested'), ('A', 'Accepted'), ('R', 'Rejected')]),
        ),
        migrations.AlterField(
            model_name='dailyschedule',
            name='end_time',
            field=models.TimeField(default=datetime.time(17, 0)),
        ),
        migrations.AlterField(
            model_name='dailyschedule',
            name='start_time',
            field=models.TimeField(default=datetime.time(9, 0)),
        ),
    ]

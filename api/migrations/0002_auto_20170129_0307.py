# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-29 03:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='start_time',
            field=models.BigIntegerField(default=1485659234930),
        ),
    ]

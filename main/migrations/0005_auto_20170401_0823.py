# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-01 08:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20170327_1801'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient_name',
            field=models.CharField(default='John Kurian', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consultation',
            name='patient_name',
            field=models.CharField(default='John Kurian', max_length=100),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20160715_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='accept_reject',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='position',
            name='report',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='position',
            name='spread_KPI',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='position',
            name='spread_budget',
            field=models.BooleanField(default=False),
        ),
    ]
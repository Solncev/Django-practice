# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-21 13:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0010_auto_20160721_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignedkpi',
            name='assigner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

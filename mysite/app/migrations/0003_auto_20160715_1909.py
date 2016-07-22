# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160715_1845'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='sender',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='senders', to='app.UserProfile'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='kpi',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app.AssignedKPI'),
        ),
    ]

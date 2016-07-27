# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-26 20:45
from __future__ import unicode_literals

import app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160726_2335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignedkpi',
            name='complete',
            field=models.IntegerField(default=0, validators=[app.validators.validate_non_negative]),
        ),
    ]

from __future__ import unicode_literals

from datetime import date

from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    third_name = models.CharField(max_length=30)
    birth_date = models.DateField('birth date')

    def __str__(self):
        return self.user.username


class Department(models.Model):
    name = models.CharField(max_length=50)
    head = models.OneToOneField(UserProfile, related_name="head_of_department")
    subordinate = models.OneToOneField(
        'Department',
        related_name="subordinate_to_this_department",
        blank=True,
        null=True,
    )
    superior = models.ForeignKey(
        'Department',
        related_name="superior_of_this_department",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


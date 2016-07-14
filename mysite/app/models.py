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
# <<<<<<< HEAD
# =======
    type = models.ForeignKey(
        'Type',
        related_name='departments'
    )
    KPI = models.ManyToManyField(
        'KPI',
        through='AssignedKPI',
        through_fields=('department', 'kpi')
    )
# >>>>>>> 39f5a913329fc1904cd8450c52e8e358d86c0b65

    def __str__(self):
        return self.name

# <<<<<<< HEAD
# =======

class KPI(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
            return self.name


class Type(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AssignedKPI(models.Model):
    kpi = models.ForeignKey(KPI)
    department = models.ForeignKey(Department)
    amount = models.IntegerField
    complete = models.IntegerField(
        blank=True,
        null=True
    )

    # There must be a Cheif
# >>>>>>> 39f5a913329fc1904cd8450c52e8e358d86c0b65

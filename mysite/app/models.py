from __future__ import unicode_literals


from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    third_name = models.CharField(max_length=30)
    birth_date = models.DateField('birth date')
    position = models.ForeignKey('Position', related_name='users', blank=True, null=True)
    department = models.OneToOneField('Department', related_name='users', blank=True, null=True)

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
    budget = models.IntegerField(
        blank=True,
        null=True
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
    kpi = models.ForeignKey('KPI')
    department = models.ForeignKey('Department')
    amount = models.IntegerField(null=True)
    complete = models.IntegerField(
        blank=True,
        null=True
    )
# >>>>>>> 39f5a913329fc1904cd8450c52e8e358d86c0b65


class Position(models.Model):
    name = models.CharField(max_length=50)
    accept_reject = models.BooleanField(default=False)
    spread_KPI = models.BooleanField(default=False)
    report = models.BooleanField(default=False)
    spread_budget = models.BooleanField(default=False)

    def __str__(self):
        return self.name
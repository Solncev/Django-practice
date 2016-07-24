from __future__ import unicode_literals


from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    third_name = models.CharField(max_length=30)
    birth_date = models.DateField('birth date')
    position = models.ForeignKey('Position', related_name='users', blank=True, null=True)

    department = models.ForeignKey('Department', related_name='users', blank=True, null=True)


    def __str__(self):
        return self.user.username


class Department(models.Model):
    name = models.CharField(max_length=50)
    head = models.OneToOneField(User, related_name="head_of_department")
    superior = models.ForeignKey(
        'Department',
        related_name="superior_of_this_department",
        blank=True,
        null=True,
    )
    DEPARTMENT_TYPE_CHOICES = (
        ('0', "Направление"),
        ('1', "Кафедра"),
        ('2', "Научная группа"),
        ('3', "Лаборатория"),
    )
    type = models.CharField(max_length=1, choices=DEPARTMENT_TYPE_CHOICES)
    KPI = models.ManyToManyField(
        'KPI',
        through='AssignedKPI',
        through_fields=('department', 'kpi')
    )

    def __str__(self):
        return self.name

class KPI(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AssignedKPI(models.Model):
    assigner = models.ForeignKey(User, null=True)
    kpi = models.ForeignKey('KPI', verbose_name="KPI")
    department = models.ForeignKey('Department')

    amount = models.FloatField(default=0.0)
    complete = models.FloatField(
        blank=True, default=0.0

    )
    datetime = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    budget = models.IntegerField(default=0, blank=True)
    report = models.CharField(max_length=500, blank=True)
    accepted = models.NullBooleanField(null=True, blank=True)
    datetimeaccept = models.DateTimeField(null=True, blank=True)

    def to_percent(self):
        percent = (float)(self.complete) / (float)(self.amount) * 100.0
        return round(percent, 1)

    def __str__(self):
        return self.kpi.name


class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comments(models.Model):
    sender = models.ForeignKey('UserProfile', related_name='senders')
    text = models.CharField(default='', max_length=500, blank=True)
    kpi = models.ForeignKey('AssignedKPI')
    datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sender.user.username


class Budget(models.Model):
    budget = models.IntegerField(default=0)
    datetime = models.DateTimeField(null=True, blank=True)
    assigner = models.ForeignKey(User, null=True)
    department = models.OneToOneField('Department', null=True)



from __future__ import unicode_literals


from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    third_name = models.CharField(max_length=30)
    birth_date = models.DateField('birth date')
    position = models.ForeignKey('Position', related_name='users', blank=True, null=True)

    department = models.ForeignKey('Department', related_name='users', blank=True, null=True)

    def has_access(self, d,):
        return self.department in d.get_superiors()

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
        ('0', "Ректорат"),
        ('1', "Направление"),
        ('2', "Кафедра"),
        ('3', "Научная группа"),
        ('4', "Лаборатория"),
    )
    type = models.CharField(max_length=1, choices=DEPARTMENT_TYPE_CHOICES)
    KPI = models.ManyToManyField(
        'KPI',
        through='AssignedKPI',
        through_fields=('department', 'kpi')
    )

    def __str__(self):
        return self.name

    def get_superiors(self, *superiors):
        superiors = list(superiors)
        if self.superior is not None:
            superiors.append(self.superior,)
            return self.superior.get_superiors(*superiors,)
        else:
            return superiors


class KPI(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class AssignedKPI(models.Model):
    assigner = models.ForeignKey(User, null=True)
    kpi = models.ForeignKey('KPI', verbose_name="KPI")
    department = models.ForeignKey('Department')

    amount = models.IntegerField(default=0)
    complete = models.IntegerField(
        blank=True, default=0

    )
    datetime = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True, verbose_name="Комментарий")
    deadline = models.DateTimeField(null=True, blank=True)
    budget = models.IntegerField(default=0, blank=True)
    report = models.CharField(max_length=500, blank=True)
    accepted = models.NullBooleanField(null=True, blank=True)
    datetimeaccept = models.DateTimeField(null=True, blank=True)

    def to_percent(self):
        percent = (float)(self.complete) / (float)(self.amount) * 100
        return round(percent, 1)

    def __str__(self):
        return self.kpi.name


class Position(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Comments(models.Model):
    sender = models.ForeignKey(User, related_name='senders')
    text = models.TextField(default='', max_length=500, blank=True, verbose_name="")
    kpi = models.ForeignKey('AssignedKPI')
    datetime = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.sender.username


class Budget(models.Model):
    assigned_budget = models.IntegerField(default=0, verbose_name="Количество")
    assigner = models.ForeignKey(User, null=True)
    department = models.OneToOneField('Department', null=True)



from django.forms import forms, ModelForm, BaseModelFormSet, HiddenInput
from django import forms
from app.models import AssignedKPI, KPI, Department


class AssignKPIform(ModelForm):
    class Meta:
        model = AssignedKPI
        exclude = ['complete', 'budget', 'report',]
        widgets = {
            'assigner': HiddenInput,
            'datetime': HiddenInput,
        }


class KPICreationForm(ModelForm):
    class Meta:
        model = KPI
        fields = ['name']
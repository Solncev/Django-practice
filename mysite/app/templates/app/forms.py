from django.forms import forms, ModelForm, BaseModelFormSet, HiddenInput
from django import forms
from app.models import AssignedKPI, KPI, Department, Budget, Comments


class AssignKPIform(ModelForm):
    class Meta:
        model = AssignedKPI
        exclude = ['complete', 'budget', 'report', 'accepted', 'datetimeaccept']
        widgets = {
            'assigner': HiddenInput,
            'datetime': HiddenInput,
            'department': HiddenInput,
        }


class KPICreationForm(ModelForm):
    class Meta:
        model = KPI
        fields = ['name']


class KPIReportForm(forms.Form):
    complete = forms.FloatField(max_value=1000000000000000)
    budget = forms.IntegerField(max_value=1000000000000000)
    report = forms.CharField(max_length=100)


class CommentCreationForm(ModelForm):
    class Meta:
        model = Comments
        fields = {
            'text', 'sender', 'kpi', 'datetime',
        }
        widgets = {
            'sender': HiddenInput,
            'kpi': HiddenInput,
            'datetime': HiddenInput,
        }


class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = {'assigned_budget', 'assigner', 'department'}
        widgets = {
            'assigner': HiddenInput,
            'department': HiddenInput,
        }
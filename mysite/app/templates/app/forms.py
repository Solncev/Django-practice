from django.forms import forms, ModelForm, BaseModelFormSet, HiddenInput
from django import forms
from app.models import AssignedKPI, KPI, Department, Budget, Comments
from app.validators import validate_non_negative


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
    complete = forms.IntegerField(max_value=1000000000000000, validators=[validate_non_negative,])
    budget = forms.IntegerField(max_value=1000000000000000, validators=[validate_non_negative],)
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
        fields = {'assigned_budget', 'assigner', }
        widgets = {
            'assigner': HiddenInput,
        }

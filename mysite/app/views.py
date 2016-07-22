from datetime import datetime

from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.contrib import auth
from django.http import HttpResponseRedirect
from app.models import UserProfile, AssignedKPI, KPI, Department
from app.templates.app.forms import AssignKPIform, KPICreationForm


def login(request):
    args = {}
    args.update(csrf(request))
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                args['login_error'] = "Пользователь не найден"
                return render(request, 'app/login.html', args)
            auth.login(request, user)
            return redirect('/app/profile/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request,'app/login.html', args)
    else:
        return render(request,'app/login.html', args)

def profile(request):
    profile = UserProfile.objects.get(user=auth.get_user(request))
    return render_to_response('app/profile.html', {'profile': profile})

def assign_kpi(request):
    args = {}
    args.update(csrf(request))
    assigned_kpi = AssignedKPI(assigner=request.user, datetime=datetime.now())
    args['form'] = AssignKPIform(instance=assigned_kpi)
    args['creation_form'] = KPICreationForm()
    if request.method == "POST":
        form = AssignKPIform(request.POST)
        creation_form = KPICreationForm(request.POST)
        args['form'] = AssignKPIform(instance=assigned_kpi)
        if creation_form.is_valid():
            creation_form.save()
            args['creation_form'] = KPICreationForm()
            return render(request,'app/assign_kpi.html', args)
        if form.is_valid():
            form.save()
            return render(request, 'app/assign_kpi.html', args)
        else:
            args['form_error'] = "Данные введены неверно"
            return render(request, 'app/assign_kpi.html', args)
    else:
        return render(request, 'app/assign_kpi.html', args)

def logout(request):
    auth.logout(request)
    return redirect('login')

def personal_information(request):
    personal_information = UserProfile.objects.get(user=auth.get_user(request))
    return render_to_response('app/personal_information.html', {'personal_information': personal_information})
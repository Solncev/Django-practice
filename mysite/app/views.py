from datetime import datetime

from django.forms import formset_factory
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.contrib import auth
from app.models import UserProfile, AssignedKPI, Department
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
            return redirect('/app/main/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request,'app/login.html', args)
    else:
        return render(request,'app/login.html', args)

def main(request):
    profile = UserProfile.objects.get(user=auth.get_user(request))
    set = Department.objects.filter(superior=profile.department)
    # Получаем все AssignesKPI, назначенные структурному подразделению, которому принадлежит данный пользователь
    profile_set = AssignedKPI.objects.filter(department=profile.department)
    # Высчитываем процент выполнения KPI
    percent = {}
    i = 0
    for x in profile_set:
        if x.complete != 0:
            percent[i] = x.complete / x.amount * 100
        else:
            percent[i] = 0
        i = i + 1
    return render_to_response('app/main.html', {'profile': profile,'set':set, 'profile_set':profile_set, 'percent':percent})

# Без значения id_department в url в это представление попасть НЕЛЬЗЯ
def assign_kpi(request, id_department):
    args = {}
    args.update(csrf(request))
    id_department = id_department
    assigned_kpi = AssignedKPI(assigner=request.user, datetime=datetime.now(), department=Department.objects.get(id=id_department))
    # Форма для назначения KPI, instance - установление дефолтных значений обязательных полей
    args['form'] = AssignKPIform(instance=assigned_kpi)
    # Форма для создания KPI
    args['creation_form'] = KPICreationForm()
    args['department'] = Department.objects.get(id=id_department)
    args['id_department'] = id_department
    # Получаем все AssignesKPI, назначенные выбранному структурному подразделению
    args['department_set'] = AssignedKPI.objects.filter(department=args['department'], assigner=request.user)
    # Высчитываем процент выполнения KPI
    percent = {}
    i = 0
    for x in args['department_set']:
        if x.complete != 0:
            percent[i] = x.complete / x.amount * 100
        else:
            percent[i] = 0
        i = i + 1
    # Попадаем сюда при отправке форм
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
            return redirect('main')
        else:
            args['form_error'] = "Данные введены неверно."
            return render(request, 'app/assign_kpi.html', args)
    else:
        return render(request, 'app/assign_kpi.html', args)


def logout(request):
    auth.logout(request)
    return redirect('login')


def personal_information(request):
    personal_information = UserProfile.objects.get(user=auth.get_user(request))
    return render_to_response('app/personal_information.html', {'personal_information': personal_information})


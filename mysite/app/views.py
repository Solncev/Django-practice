from datetime import datetime

from django.forms import formset_factory
from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.contrib import auth
from app.models import UserProfile, AssignedKPI, Department, KPI, Comments, Budget
from app.templates.app.forms import AssignKPIform, KPICreationForm, KPIReportForm, BudgetForm, CommentCreationForm


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
    if not request.user.is_authenticated():
        return redirect('login')
    profile = UserProfile.objects.get(user=auth.get_user(request))
    set = Department.objects.filter(superior=profile.department)
    # Получаем все AssignesKPI, назначенные структурному подразделению, которому принадлежит данный пользователь
    accepted_kpis = AssignedKPI.objects.filter(department=profile.department, accepted=True,
                                               deadline__gt=datetime.now())
    not_accepted_kpis = AssignedKPI.objects.filter(department=profile.department, accepted=None,
                                                   deadline__gt=datetime.now())
    # Высчитываем процент выполнения KPI
    percent = []
    for x in accepted_kpis:
        if x.complete is not 0:
            percent.append(round(x.to_percent(), 1))
        else:

            percent.append(0)
    return render_to_response('app/main.html', {'profile': profile,'set':set, 'accepted_kpis':accepted_kpis,
                                                'percent':percent, 'not_accepted_kpis': not_accepted_kpis})


# Без значения id_department в url в это представление попасть НЕЛЬЗЯ
def assign_kpi(request, id_department):
    if not request.user.is_authenticated():
        return redirect('login')
    args = {}
    args.update(csrf(request))
    id_department = id_department
    try:
        department = Department.objects.get(id=id_department)
    except Department.DoesNotExist:
        access_error = "Данного структурного подразделения не существует"
        return render(request, 'app/access_error.html', {'access_error':access_error})
    profile = UserProfile.objects.get(user=request.user)
    if department.superior != profile.department:
        access_error = "Вы не можете назначать KPI этому структурному подразделению."
        return render(request, 'app/access_error.html', {'access_error':access_error})
    args['department'] = department
    args['profile'] = profile
    assigned_kpi = AssignedKPI(assigner=request.user, datetime=datetime.now(),
                               department=Department.objects.get(id=id_department))

    # Форма для назначения KPI, instance - установление дефолтных значений обязательных полей

    args['form'] = AssignKPIform(instance=assigned_kpi)

    # Форма для создания KPI
    args['creation_form'] = KPICreationForm()
    args['id_department'] = id_department

    # Получаем все AssignedKPI, назначенные выбранному структурному подразделению
    args['department_set'] = AssignedKPI.objects.filter(department=args['department'], assigner=request.user,
                                                        deadline__gt=datetime.now())

    # Высчитываем процент выполнения KPI
    percent = []
    for x in args['department_set']:
        if x.complete is not 0:
            percent.append(x.to_percent())
        else:
            percent.append(0)

    # Попадаем сюда при отправке форм
    if request.method == "POST":
        form = AssignKPIform(request.POST)
        creation_form = KPICreationForm(request.POST)
        args['form'] = AssignKPIform(instance=assigned_kpi)
        name = request.POST.get('name')
        try:
            KPI.objects.get(name=name)
        except KPI.DoesNotExist:
            if creation_form.is_valid():
                creation_form.save()
                args['creation_form'] = KPICreationForm()
                return render(request,'app/assign_kpi.html', args)
        if form.is_valid():
            assigned_kpi.deadline = form.cleaned_data.get('deadline')
            assigned_kpi.amount = form.cleaned_data.get('amount')
            assigned_kpi.comment = form.cleaned_data.get('comment')
            assigned_kpi.kpi = form.cleaned_data.get('kpi')
            assigned_kpi.check_kpi_unique()
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

    if not request.user.is_authenticated():
        return redirect('login')
    personal_information = UserProfile.objects.get(user=auth.get_user(request))
    return render_to_response('app/personal_information.html', {'personal_information': personal_information})

def accept(request, flag, id_assigned_kpi):
    if not request.user.is_authenticated():
        return redirect('login')
    try:
        assigned_kpi = AssignedKPI.objects.get(id=id_assigned_kpi)
    except AssignedKPI.DoesNotExist:
        access_error = "Данного KPI не существует"
        return render(request, 'app/access_error.html', {'access_error': access_error})
    profile = UserProfile.objects.get(user=request.user)
    if assigned_kpi.department != profile.department:
        access_error = "Вы не имеете права принять/отклонить этот KPI"
        return render(request, 'app/access_error.html', {'access_error': access_error})
    if assigned_kpi.accepted is not None:
        access_error = "Задание уже принято/отклонено."
        return render(request, 'app/access_error.html', {'access_error': access_error})
    if flag == 'accept':
        assigned_kpi.accepted = True
    else:
        assigned_kpi.accepted = False
    assigned_kpi.datetime = datetime.now()
    assigned_kpi.save()
    return redirect('main')


def report(request, id_assigned_kpi):
    if not request.user.is_authenticated():
        return redirect('login')
    try:
        assigned_kpi = AssignedKPI.objects.get(id=id_assigned_kpi)
    except AssignedKPI.DoesNotExist:
        access_error = "Данного KPI не существует"
        return render(request, 'app/access_error.html', {'access_error': access_error})
    profile = UserProfile.objects.get(user=request.user)
    if assigned_kpi.department != profile.department:
        access_error = "Вы не имеете права докладывать об этом KPI"
        return render(request, 'app/access_error.html', {'access_error': access_error})
    if assigned_kpi.accepted is not True:
        access_error = "Задание не принято или отклонено"
        return render(request, 'app/access_error.html', {'access_error': access_error})
    if request.method == "POST":
        form = KPIReportForm(request.POST)
        if form.is_valid():
            assigned_kpi.budget = assigned_kpi.budget + form.cleaned_data.get('budget')
            if assigned_kpi.budget > profile.department.budget.assigned_budget:
                access_error = "Вы не можете превысить бюджет своего структурного подразделения."
                return render(request, 'app/access_error.html', {'access_error': access_error})
            assigned_kpi.complete = assigned_kpi.complete + form.cleaned_data.get('complete')
            assigned_kpi.send_complete_to_superiors(form.cleaned_data.get('complete'))
            assigned_kpi.report = request.POST.get('report', '')
            assigned_kpi.save()
            return redirect('main')
        else:
            access_error = "Данные введены неверно."
            return render(request, 'app/access_error.html', {'access_error': access_error})
    else:
        return redirect('main')


def kpi(request, id_assigned_kpi):
    if not request.user.is_authenticated():
        return redirect('login')
    try:
        assigned_kpi = AssignedKPI.objects.get(id=id_assigned_kpi)
    except AssignedKPI.DoesNotExist:
        access_error = "Такого KPI не существует."
        return render(request, 'app/access_error.html', {'access_error': access_error})
    profile = UserProfile.objects.get(user=request.user)
    department = assigned_kpi.department
    args = {}
    args.update(csrf(request))
    args['access_flag']= profile.has_access(department)
    if department == profile.department or args['access_flag']:
        args.update(csrf(request))
        args['profile'] = profile
        args['assigned_kpi'] = assigned_kpi
        args['percent'] = assigned_kpi.to_percent()

        comment = Comments(sender=request.user, kpi=assigned_kpi, datetime=datetime.now())
        args['comment_form'] = CommentCreationForm(instance=comment)
        args['comments_set'] = Comments.objects.filter(kpi=assigned_kpi)
        if assigned_kpi.accepted is None:
            return render(request, 'app/kpi.html', args)
        if assigned_kpi.accepted == True:
            if args['access_flag'] is False:
                args['form'] = KPIReportForm()
            return render(request, 'app/kpi.html', args)
        else:
            args['access_error'] = "Задание отклонено"
            return render(request, 'app/access_error.html', args)
    else:
        access_error = "Вы не имеете доступа к данному KPI"
        return render(request, 'app/access_error.html', {'access_error': access_error})


def send_comment(request):
    if request.method == "POST":
        form = CommentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('main')


def redirectpage(request):
    if not request.user.is_authenticated():
        return redirect('/app/login/')
    else:
        return redirect('/app/main/')


def budget(request, id_department):
    if not request.user.is_authenticated():
        return redirect('login')
    args = {}
    args.update(csrf(request))
    id_department = id_department
    try:
        department = Department.objects.get(id=id_department)
    except Department.DoesNotExist:
        access_error = "Данного структурного подразделения не существует"
        return render(request, 'app/access_error.html', {'access_error':access_error})
    profile = UserProfile.objects.get(user=request.user)
    if department.superior != profile.department:
        access_error = "Вы не можете выделять средства этому структурному подразделению."
        return render(request, 'app/access_error.html', {'access_error':access_error})
    args['department'] = department
    args['profile'] = profile
    budget = Budget(assigner=request.user,  department=Department.objects.get(id=id_department))

    args['form'] = BudgetForm(instance=budget)

    if request.method == "POST":
        form = BudgetForm(request.POST)
        args['form'] = BudgetForm(instance=budget)
        if form.is_valid():
            try:
                bud=Budget.objects.get(department=department)
            except Budget.DoesNotExist:
                form.save()
                return redirect('main')
            bud.assigned_budget += form.cleaned_data.get('assigned_budget', '')
            bud.save()
            return redirect('main')
        else:
            args['form_error'] = "Данные введены неверно."
            return render(request, 'app/budget.html', args)

    else:
        return render(request, 'app/budget.html', args)
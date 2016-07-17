from django.shortcuts import render, redirect, render_to_response

# Create your views here.
from django.template.context_processors import csrf
from django.contrib import auth

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/auth/profile')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('app/login.html', args)
    else:
        return render_to_response('app/login.html', args)

def profile(request):
        return render_to_response('app/profile.html', {'username':auth.get_user(request).username})
def logout(request):
    auth.logout(request)
    return redirect('login')
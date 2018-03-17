from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponse


def acc_login(request):
    errors = []
    if request.method == 'POST':
        _email = request.POST.get('email')
        _password = request.POST.get('password')
        user = authenticate(username=_email, password=_password)

        if user:
            login(request, user)
            next_url = request.GET.get('next','/crm/')
            return redirect(next_url)
        else:
            errors = ['邮箱或密码错误']
    return render(request,'login.html',{'errors': errors})


def acc_logout(request):
    logout(request)
    return redirect('/account/login')

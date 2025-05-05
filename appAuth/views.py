from django.shortcuts import redirect, render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

from .forms import LoginForm, RegisterForm



def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            userData = form.clean()
            newUser = User.objects.create_user(userData['username'], " ", userData['password'])
            newUser.save()

            return HttpResponseRedirect("/auth/successfulLogin")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

def successfulLogin(request):
    return render(request, 'successfulLogin.html')

def fail(request):
    return render(request, 'fail.html')

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user) 
                if user.is_superuser:
                    return redirect('/admin/')
                else:
                    return redirect('home')
            else:
                form.add_error(None, "fail")
    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})
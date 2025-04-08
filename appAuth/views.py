from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from .forms import LoginForm, RegisterForm



def register(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = RegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            userData = form.clean()
            newUser = User.objects.create_user(userData['username'], " ", userData['password'])
            newUser.save()

            # redirect to a new URL:
            return HttpResponseRedirect("/successfulLogin")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})

def successfulLogin(request):
    return render(request, 'successfulLogin.html')

def fail(request):
    return render(request, 'fail.html')

def login(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                form.add_error(None, "success")
            else:
                form.add_error(None, "fail")

    else:
        form = LoginForm()

    return render(request, "registration/login.html", {"form": form})
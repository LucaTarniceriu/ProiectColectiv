from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegisterForm, LoginForm
from userProfile.models import UserProfile
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from .forms import RegisterForm
from userProfile.models import UserProfile
from django.db import IntegrityError, DatabaseError

def register(request):
    errors = []

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_type = form.cleaned_data['user_type']
            print(f"User Type in View: {user_type}") #debug

            try:
                if User.objects.filter(username=username).exists():
                    form.add_error('username', "A user with that username already exists.")
                    return render(request, 'registration/register.html', {"form": form, "errors": errors})

                user = User.objects.create_user(username=username, password=password)

                try:
                    user_profile = UserProfile.objects.get(user=user)
                    print(f"Before Update: {user_profile.user_type}")  #debug
                    user_profile.user_type = user_type
                    user_profile.save()

                    print(f"After Update: {user_profile.user_type}") 

                except UserProfile.DoesNotExist:
                    UserProfile.objects.create(user=user, user_type=user_type)

                auth_login(request, user)
                return redirect('profile')

            except IntegrityError as e:
                errors.append(f"Integrity error: {str(e)}")
            except DatabaseError as e:
                errors.append(f"Database error: {str(e)}")
            except Exception as e:
                errors.append(f"Unexpected error: {str(e)}")

    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {"form": form, "errors": errors})




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
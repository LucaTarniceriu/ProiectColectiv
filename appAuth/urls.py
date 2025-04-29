from django.urls import include, path
from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("successfulLogin/", views.successfulLogin, name="success"),
    path("fail/", views.fail, name="fail"),
]




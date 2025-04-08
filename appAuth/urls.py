from django.urls import path
from setuptools.extern import names
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register/", views.register, name="register"),
    path("successfulLogin/", views.successfulLogin, name="success"),
    path("fail/", views.fail)
]




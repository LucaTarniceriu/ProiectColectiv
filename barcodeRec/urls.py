from django.urls import path
# from setuptools.extern import names

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("scanBook/", views.scanCode, name="scan"),
    path("bookDetails/", views.bookDetails, name="details")
]




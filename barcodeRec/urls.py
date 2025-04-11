from django.urls import path
from setuptools.extern import names

from . import views

urlpatterns = [
    path("bookDetails/", views.bookDetails, name="details")
]




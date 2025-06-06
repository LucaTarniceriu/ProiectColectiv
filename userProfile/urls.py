from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile_view, name='profile'),
    path('saved-books/', views.saved_books_view, name='saved_books'),
    path('my-ratings/', views.my_ratings_view, name='my_ratings'),
]

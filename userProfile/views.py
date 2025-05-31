import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from userProfile.decorators import user_type_required
from .models import UserProfile
from barcodeRec.models import Rating, Book
import random
from isbnlib import *


@login_required
def profile_view(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = request.user.userprofile
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile')  
    return render(request, "userProfile/profile.html", {'random_number': random.randint(0, 7)})

@login_required
@user_type_required('User')
def saved_books_view(request):
    if request.method == 'POST':
        searchTitle = request.POST['search']
        if searchTitle:
            user_books = Book.objects.filter(user=request.user, title__icontains=searchTitle).order_by('title')
        else:
            user_books = Book.objects.filter(user=request.user).order_by('title')
    else:
        user_books = Book.objects.filter(user=request.user).order_by('title')

    return render(request, 'userProfile/myBooks.html', {'books': user_books, 'random_number': random.randint(0, 7)})

@login_required
@user_type_required('User')
def my_ratings_view(request):

    if request.method == 'POST':
        searchTitle = request.POST['search']
        if searchTitle:
            user_ratings = Rating.objects.filter(user=request.user, title__icontains=searchTitle).order_by('-rated_at')
        else:
            user_ratings = Rating.objects.filter(user=request.user).order_by('-rated_at')
    else:
        user_ratings = Rating.objects.filter(user=request.user).order_by('-rated_at')

    return render(request, 'userProfile/myRatings.html', {'ratings': user_ratings, 'random_number': random.randint(0, 7)})

@login_required
@user_type_required('Librarie')
def manage_books(request):

    books = Book.objects.all().order_by('title')

    # books = Book.objects.all().order_by('-scanned_at')  # or just '-id'
    return render(request, 'userProfile/manageBooks.html', {
        'books': books,
        'random_number': random.randint(0, 7)
    })
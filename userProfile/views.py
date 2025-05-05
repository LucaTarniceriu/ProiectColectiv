from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from barcodeRec.models import Rating


@login_required
def profile_view(request):
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        profile = request.user.userprofile
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        return redirect('profile')  
    return render(request, "userProfile/profile.html")

@login_required
def saved_books_view(request):
    return render(request, 'userProfile/saved_books.html')

@login_required
def wishlist_view(request):
    return render(request, 'userProfile/wishlist.html')

@login_required
def my_ratings_view(request):
    user_ratings = Rating.objects.filter(user=request.user).order_by('-rated_at')
    return render(request, 'userProfile/myRatings.html', {'ratings': user_ratings})
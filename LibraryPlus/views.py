from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from userProfile.models import UserProfile
import random

@require_POST
def updateMode(request):
    if request.method == 'POST':
        profile = request.user.userprofile
        profile.display_mode = request.POST['mode']
        profile.save()

    return redirect(request.META.get('HTTP_REFERER', '/'), {'random_number': random.randint(0, 7)})
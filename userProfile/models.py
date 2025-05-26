from django.db import models
from django.contrib.auth.models import User
from .choices import USER_TYPE_CHOICES

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='User')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    display_mode = models.CharField(max_length=6, default='light')

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

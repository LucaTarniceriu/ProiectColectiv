from django.db import models
import os
from django.contrib.auth.models import User

def upload_to_fixed_name(instance, filename):
    return 'uploads/code.jpg'  

class Photo(models.Model):
    image = models.ImageField(upload_to=upload_to_fixed_name)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.pk:
            try:
                old_image = Photo.objects.get(pk=self.pk).image
                if old_image and old_image.name != self.image.name and os.path.exists(old_image.path):
                    os.remove(old_image.path)
            except Photo.DoesNotExist:
                pass
        super().save(*args, **kwargs)

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20)
    cover = models.CharField(max_length=255, default="/static/missingCover.png")
    scanned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.isbn}) of {self.user.username}"

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="None")
    isbn = models.CharField(max_length=20)
    rating = models.IntegerField()
    total_rating = models.FloatField(default=0)
    number_of_ratings = models.IntegerField(default=0)
    rated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'isbn')

    def __str__(self):
        return f"{self.user.username} rated {self.isbn} as {self.rating}★"
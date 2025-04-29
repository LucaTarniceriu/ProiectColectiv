from django.db import models
import os

def upload_to_fixed_name(instance, filename):
    return 'uploads/code.jpg'  # Fixed filename



# Create your models here.

class Photo(models.Model):
    image = models.ImageField(upload_to=upload_to_fixed_name)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # delete the old file if it exists
        if self.pk:
            try:
                old_image = Photo.objects.get(pk=self.pk).image
                if old_image and old_image.name != self.image.name and os.path.exists(old_image.path):
                    os.remove(old_image.path)
            except Photo.DoesNotExist:
                pass
        super().save(*args, **kwargs)
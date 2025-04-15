from django import forms
from .models import Photo

class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image']
        widgets = {
            'image': forms.ClearableFileInput(attrs={
                'accept': 'image/*',         # Accept only images
                'capture': 'environment'     # Use camera if available
            }),
            
        }
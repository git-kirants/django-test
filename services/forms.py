from django import forms
from .models import Service, ServiceImage

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'duration', 'category', 'is_available', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ServiceImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = ServiceImage
        fields = ('image',)

# For handling multiple images in one form
ServiceImageFormSet = forms.inlineformset_factory(
    Service, ServiceImage, form=ServiceImageForm,
    extra=3, can_delete=False
) 
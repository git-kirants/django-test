from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProviderApplication, ProviderProfile

class CustomerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProviderApplicationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = ProviderApplication
        fields = ('username', 'email', 'business_name', 'phone', 'address')

class ProviderProfileForm(forms.ModelForm):
    class Meta:
        model = ProviderProfile
        fields = ['business_name', 'phone', 'address', 'description', 
                 'services_offered', 'years_of_experience', 'website', 'logo']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full rounded-lg border-gray-300'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'w-full rounded-lg border-gray-300'}),
            'logo': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
            'business_name': forms.TextInput(attrs={'class': 'w-full rounded-lg border-gray-300'}),
            'phone': forms.TextInput(attrs={'class': 'w-full rounded-lg border-gray-300'}),
            'services_offered': forms.TextInput(attrs={'class': 'w-full rounded-lg border-gray-300'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'w-full rounded-lg border-gray-300'}),
            'website': forms.URLInput(attrs={'class': 'w-full rounded-lg border-gray-300'}),
        }
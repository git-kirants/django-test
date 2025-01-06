# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProviderApplication, ProviderProfile

class CustomerRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.CUSTOMER
        user.is_approved = True  # Customers are automatically approved
        if commit:
            user.save()
        return user

class ProviderRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    business_name = forms.CharField(max_length=100)
    business_description = forms.CharField(widget=forms.Textarea)
    experience_years = forms.IntegerField(min_value=0)
    certifications = forms.CharField(widget=forms.Textarea, required=False)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'business_name', 
                 'business_description', 'experience_years', 'certifications']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Common style classes for all fields
        base_input_classes = (
            "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 "
            "rounded-md shadow-sm focus:outline-none focus:ring-2 "
            "focus:ring-green-500 focus:border-green-500 sm:text-sm"
        )
        
        textarea_classes = (
            "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 "
            "rounded-md shadow-sm focus:outline-none focus:ring-2 "
            "focus:ring-green-500 focus:border-green-500 sm:text-sm"
        )
        
        # Add Tailwind CSS classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Choose a username',
        })
        
        self.fields['email'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'you@example.com',
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Create a password',
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Repeat your password',
        })
        
        self.fields['business_name'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Your business name',
        })
        
        self.fields['business_description'].widget.attrs.update({
            'class': textarea_classes,
            'rows': '4',
            'placeholder': 'Describe your gardening business...',
        })
        
        self.fields['experience_years'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Years of experience',
            'min': '0',
        })
        
        self.fields['certifications'].widget.attrs.update({
            'class': textarea_classes,
            'rows': '3',
            'placeholder': 'List any relevant certifications (optional)',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'PROVIDER'
        if commit:
            user.save()
            ProviderApplication.objects.create(
                user=user,
                business_name=self.cleaned_data['business_name'],
                business_description=self.cleaned_data['business_description'],
                experience_years=self.cleaned_data['experience_years'],
                certifications=self.cleaned_data['certifications']
            )
        return user

class ProviderProfileForm(forms.ModelForm):
    DAYS_OF_WEEK = [
        ('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'), ('friday', 'Friday'), 
        ('saturday', 'Saturday'), ('sunday', 'Sunday')
    ]

    available_days = forms.MultipleChoiceField(
        choices=DAYS_OF_WEEK,
        widget=forms.CheckboxSelectMultiple
    )
    start_time = forms.TimeField()
    end_time = forms.TimeField()
    specialties = forms.MultipleChoiceField(
        choices=[('lawn_care', 'Lawn Care'), ('landscaping', 'Landscaping'),
                ('tree_service', 'Tree Service'), ('garden_design', 'Garden Design')],
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = ProviderProfile
        fields = ['business_license', 'insurance_info', 'service_radius']

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
            # Save available hours as JSON
            available_hours = {
                day: {
                    'start': self.cleaned_data['start_time'].strftime('%H:%M'),
                    'end': self.cleaned_data['end_time'].strftime('%H:%M')
                } for day in self.cleaned_data['available_days']
            }
            profile.user.available_hours = available_hours
            profile.user.specialties = self.cleaned_data['specialties']
            profile.user.save()
        return profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Common style classes for all fields
        base_input_classes = (
            "mt-1 block w-full px-3 py-2 bg-white border border-gray-300 "
            "rounded-md shadow-sm focus:outline-none focus:ring-2 "
            "focus:ring-green-500 focus:border-green-500 sm:text-sm"
        )
        
        # Add Tailwind CSS classes to form fields
        self.fields['username'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Choose a username',
        })
        
        self.fields['email'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'you@example.com',
        })
        
        self.fields['password1'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Create a password',
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': base_input_classes,
            'placeholder': 'Repeat your password',
        })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
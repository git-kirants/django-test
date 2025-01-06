# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        CUSTOMER = 'CUSTOMER', 'Customer'
        PROVIDER = 'PROVIDER', 'Provider'
    
    role = models.CharField(
        max_length=50,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    is_approved = models.BooleanField(default=False)
    company_website = models.URLField(blank=True)
    service_area = models.CharField(max_length=200, blank=True)
    available_hours = models.JSONField(default=dict, blank=True, null=True)
    specialties = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class ProviderApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100)
    business_description = models.TextField()
    experience_years = models.IntegerField()
    certifications = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} - {self.status}"

    class Meta:
        ordering = ['-submitted_at']

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_profile_completed = models.BooleanField(default=False)
    business_license = models.FileField(upload_to='licenses/', blank=True)
    insurance_info = models.TextField(blank=True)
    payment_details = models.JSONField(default=dict, blank=True, null=True)
    service_radius = models.IntegerField(default=20)  # in kilometers

    def profile_completion_percentage(self):
        fields = ['business_license', 'insurance_info', 'payment_details', 'service_radius']
        completed = sum(1 for field in fields if getattr(self, field))
        return (completed / len(fields)) * 100
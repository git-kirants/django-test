from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator

class User(AbstractUser):
    ADMIN = 'ADMIN'
    PROVIDER = 'PROVIDER'
    CUSTOMER = 'CUSTOMER'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (PROVIDER, 'Service Provider'),
        (CUSTOMER, 'Customer'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CUSTOMER)
    email = models.EmailField(unique=True)

class ProviderApplication(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending'),
        (STATUS_APPROVED, 'Approved'),
        (STATUS_REJECTED, 'Rejected'),
    ]

    username = models.CharField(max_length=150)
    email = models.EmailField()
    password = models.CharField(max_length=128)  # Will store hashed password
    business_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.business_name} - {self.status}"

class ProviderProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    business_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
    ])
    address = models.TextField(blank=True)
    description = models.TextField(blank=True)
    services_offered = models.CharField(max_length=200, blank=True)
    years_of_experience = models.PositiveIntegerField(null=True, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(
        upload_to='provider_logos/',
        null=True,
        blank=True,
        help_text="Upload your business logo"
    )

    def __str__(self):
        return f"{self.user.username}'s Provider Profile"

    @property
    def profile_completion(self):
        fields = ['business_name', 'phone', 'address', 'description', 
                 'services_offered', 'years_of_experience', 'website', 'logo']
        filled_fields = sum(1 for field in fields if getattr(self, field))
        return int((filled_fields / len(fields)) * 100)

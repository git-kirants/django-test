# services/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db.models import Avg

class Service(models.Model):
    CATEGORY_CHOICES = [
        ('lawn_care', 'Lawn Care'),
        ('landscaping', 'Landscaping'),
        ('tree_service', 'Tree Service'),
        ('garden_design', 'Garden Design'),
        ('maintenance', 'Garden Maintenance'),
        ('pest_control', 'Pest Control'),
    ]

    gardener = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='services/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    def get_average_rating(self):
        avg = self.booking_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0

    def get_total_ratings(self):
        return self.booking_set.exclude(rating__isnull=True).count()


class ServiceImage(models.Model):
    service = models.ForeignKey(Service, related_name='additional_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='services/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']


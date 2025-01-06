from rest_framework import serializers
from .models import Booking
from services.models import Service
from django.contrib.auth import get_user_model

User = get_user_model()

class BookingSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source='service.title', read_only=True)
    gardener_name = serializers.CharField(source='service.gardener.username', read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'service', 'service_title', 'gardener_name', 'customer_name', 
                 'booking_date', 'status', 'created_at', 'special_requests']
        read_only_fields = ['customer', 'status'] 
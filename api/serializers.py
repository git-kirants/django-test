from rest_framework import serializers
from .models import Booking
from services.models import Service

class BookingSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source='service.title', read_only=True)
    customer_name = serializers.CharField(source='customer.username', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'service', 'service_title', 'customer_name', 
                 'booking_date', 'status', 'special_requests', 
                 'created_at', 'updated_at']
        read_only_fields = ['status', 'customer'] 
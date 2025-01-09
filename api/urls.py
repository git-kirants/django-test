from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'bookings', views.BookingViewSet, basename='booking')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('customer/bookings/', 
         views.BookingViewSet.as_view({'get': 'list'}), 
         name='customer_bookings'),
    path('provider/bookings/', 
         views.BookingViewSet.as_view({'get': 'list'}), 
         name='provider_bookings'),
    path('bookings/<int:booking_id>/<str:action>/', views.update_booking_status, name='update_booking_status'),
] 
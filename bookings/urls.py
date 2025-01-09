from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:service_id>/', views.booking_create, name='create'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('requests/', views.booking_requests, name='requests'),
    path('status/', views.booking_status, name='status'),
    path('rate/<int:booking_id>/', views.rate_booking, name='rate_booking'),
]

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from users.models import User, ProviderApplication  # Add ProviderApplication import
from services.models import Service  # Import your service model
from api.models import Booking  # Changed from bookings.models to api.models
from community.models import Post  # Adjust if you have different models

@staff_member_required
def admin_dashboard(request):
    # Time-based filters
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # User Statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    new_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    
    # Service Statistics
    total_services = Service.objects.count()
    active_services = Service.objects.filter(is_available=True).count()
    
    # Booking Statistics
    total_bookings = Booking.objects.count()
    recent_bookings = Booking.objects.filter(
        created_at__gte=thirty_days_ago
    ).count()
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Community Statistics
    total_posts = Post.objects.count()
    recent_posts = Post.objects.filter(
        created__gte=thirty_days_ago
    ).count()
    
    # Recent Activity
    latest_bookings = Booking.objects.order_by('-created_at')[:5]
    latest_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        # User stats
        'total_users': total_users,
        'active_users': active_users,
        'new_users': new_users,
        
        # Service stats
        'total_services': total_services,
        'active_services': active_services,
        
        # Booking stats
        'total_bookings': total_bookings,
        'recent_bookings': recent_bookings,
        'pending_bookings': pending_bookings,
        
        # Community stats
        'total_posts': total_posts,
        'recent_posts': recent_posts,
        
        # Recent activity
        'latest_bookings': latest_bookings,
        'latest_users': latest_users,
        
        # Add this to your context
        'pending_applications': ProviderApplication.objects.filter(
            status=ProviderApplication.STATUS_PENDING
        ),
    }
    
    return render(request, 'admin_dashboard.html', context)

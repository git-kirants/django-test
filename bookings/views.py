from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from services.models import Service
from api.models import Booking
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def booking_create(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.user.role == 'PROVIDER':
        messages.error(request, "Providers cannot make bookings.")
        return redirect('services:list')
    
    context = {
        'service': service,
    }
    return render(request, 'bookings/booking_form.html', context)

@login_required
def booking_status(request):
    return render(request, 'bookings/booking_status.html')

@login_required
def my_bookings(request):
    if request.user.role == 'PROVIDER':
        return redirect('bookings:requests')
    
    bookings = Booking.objects.filter(
        customer=request.user
    ).select_related('service').order_by('-created_at')
    
    context = {
        'bookings': bookings
    }
    return render(request, 'bookings/my_bookings.html', context)

@login_required
def booking_requests(request):
    if request.user.role != 'PROVIDER':
        messages.error(request, "Only providers can access this page.")
        return redirect('core:home')
    
    # Get all bookings for this provider
    active_requests = Booking.objects.filter(
        service__gardener=request.user
    ).select_related('service', 'customer').order_by('-created_at')
    
    context = {
        'active_requests': active_requests,
    }
    return render(request, 'bookings/booking_requests.html', context)

@require_POST
def rate_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, customer=request.user)
    
    if not booking.can_be_rated():
        return JsonResponse({
            'success': False,
            'message': 'This booking cannot be rated'
        }, status=400)
    
    try:
        rating = int(request.POST.get('rating', 0))
        if not (1 <= rating <= 5):
            raise ValueError('Invalid rating value')
        
        review = request.POST.get('review', '').strip()
        
        booking.rating = rating
        booking.review = review
        booking.rated_at = timezone.now()
        booking.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Thank you for your rating!'
        })
        
    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'message': 'Invalid rating value'
        }, status=400)

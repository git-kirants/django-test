from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from django.shortcuts import get_object_or_404
from services.models import Service
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Booking.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PROVIDER':
            return Booking.objects.filter(service__gardener=user).order_by('-created_at')
        return Booking.objects.filter(customer=user).order_by('-created_at')

    def perform_create(self, serializer):
        service = get_object_or_404(Service, id=self.request.data.get('service'))
        serializer.save(customer=self.request.user)

    @action(detail=True, methods=['post'])
    def accept(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.service.gardener:
            return Response(
                {'error': 'Not authorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        booking.status = 'accepted'
        booking.save()
        return Response({'status': 'booking accepted'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.service.gardener:
            return Response(
                {'error': 'Not authorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        booking.status = 'rejected'
        booking.save()
        return Response({'status': 'booking rejected'})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        booking = self.get_object()
        if request.user != booking.customer:
            return Response(
                {'error': 'Not authorized'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        booking.status = 'cancelled'
        booking.save()
        return Response({'status': 'booking cancelled'})

@login_required
@require_POST
def update_booking_status(request, booking_id, action):
    booking = get_object_or_404(Booking, id=booking_id)
    
    # Verify that the user is the service provider
    if request.user != booking.service.gardener:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    valid_actions = {
        'accept': 'accepted',
        'reject': 'rejected',
        'complete': 'completed'
    }
    
    if action not in valid_actions:
        return JsonResponse({'error': 'Invalid action'}, status=400)
    
    if action == 'complete' and booking.status != 'accepted':
        return JsonResponse({'error': 'Only accepted bookings can be completed'}, status=400)
    
    booking.status = valid_actions[action]
    booking.save()
    
    return JsonResponse({
        'status': 'success',
        'message': f'Booking {valid_actions[action]} successfully'
    })

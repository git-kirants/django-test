from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Booking
from .serializers import BookingSerializer
from django.shortcuts import get_object_or_404
from services.models import Service

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'PROVIDER':
            return Booking.objects.filter(service__gardener=user)
        return Booking.objects.filter(customer=user)

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

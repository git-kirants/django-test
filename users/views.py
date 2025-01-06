# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView, UpdateView, TemplateView
from django.urls import reverse_lazy
from .forms import CustomerRegistrationForm, ProviderRegistrationForm, ProviderProfileForm, UserRegistrationForm
from .models import User, ProviderApplication, ProviderProfile
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from services.models import Service
from api.models import Booking
from django.db.models import Avg

def customer_register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def provider_register(request):
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(
                request, 
                'Your provider application has been submitted and is pending review.'
            )
            return redirect('users:login')
    else:
        form = ProviderRegistrationForm()
    return render(request, 'users/provider_register.html', {'form': form})

@user_passes_test(lambda u: u.is_staff)
def provider_applications(request):
    applications = ProviderApplication.objects.filter(status='pending').order_by('-submitted_at')
    return render(request, 'users/provider_applications.html', {
        'applications': applications
    })

@user_passes_test(lambda u: u.is_superuser)
def approve_provider(request, application_id):
    application = ProviderApplication.objects.get(id=application_id)
    user = application.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            user.is_approved = True
            application.status = 'approved'
            messages.success(request, f'Provider {user.username} has been approved.')
        elif action == 'reject':
            application.status = 'rejected'
            messages.warning(request, f'Provider {user.username} has been rejected.')
        
        user.save()
        application.admin_notes = request.POST.get('admin_notes', '')
        application.save()
        
    return redirect('users:provider_applications')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('core:home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'users/login.html')

class ProviderProfileView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ProviderProfile
    form_class = ProviderProfileForm
    template_name = 'users/provider_profile.html'
    success_url = reverse_lazy('users:provider_dashboard')

    def test_func(self):
        return self.request.user.role == User.Role.PROVIDER

    def get_object(self):
        profile, created = ProviderProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_profile_completed = True
        self.object.save()
        messages.success(self.request, 'Profile updated successfully!')
        return response

class ProviderDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/provider_dashboard.html'

    def test_func(self):
        return self.request.user.role == User.Role.PROVIDER

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        context['total_services'] = Service.objects.filter(gardener=user).count()
        context['total_bookings'] = Booking.objects.filter(
            service__gardener=user
        ).count()
        context['recent_bookings'] = Booking.objects.filter(
            service__gardener=user
        ).order_by('-created_at')[:5]
        context['profile_completion'] = user.providerprofile.profile_completion_percentage()
        
        reviews = Review.objects.filter(service__gardener=user)
        context['total_reviews'] = reviews.count()
        context['average_rating'] = reviews.aggregate(
            Avg('rating')
        )['rating__avg'] or 0
        
        return context

def check_application_status(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to check your application status.')
        return redirect('users:login')
    
    try:
        application = ProviderApplication.objects.get(user=request.user)
        return render(request, 'users/application_status.html', {
            'application': application
        })
    except ProviderApplication.DoesNotExist:
        messages.info(request, 'You have not submitted a provider application yet.')
        return redirect('users:provider_register')  # Redirect to provider registration instead of home

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'users/register.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('core:home')
    return redirect('core:home')  # If someone tries to GET the logout URL
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CustomerRegistrationForm, ProviderApplicationForm, ProviderProfileForm
from .models import ProviderApplication, User, ProviderProfile
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages
from services.models import Service
from django.db.models import Avg, Prefetch
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate user until email is verified
            user.save()

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.send()

            messages.success(request, 'Please check your email to complete the registration.')
            return redirect('users:login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def provider_register(request):
    if request.method == 'POST':
        form = ProviderApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.password = make_password(form.cleaned_data['password'])
            application.is_active = False  # Deactivate until email is verified
            application.save()

            # Send verification email
            current_site = get_current_site(request)
            mail_subject = 'Verify your email for provider application'
            message = render_to_string('users/provider_activation_email.html', {
                'application': application,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(application.pk)),
                'token': account_activation_token.make_token(application),
            })
            email = EmailMessage(
                mail_subject, message, to=[application.email]
            )
            email.send()

            messages.success(request, 'Please check your email to verify your application.')
            return redirect('users:provider-pending')
    else:
        form = ProviderApplicationForm()
    return render(request, 'users/register_provider.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.role == User.ADMIN)
def provider_applications(request):
    applications = ProviderApplication.objects.filter(status=ProviderApplication.STATUS_PENDING)
    return render(request, 'users/provider_applications.html', {'applications': applications})

def is_admin(user):
    return user.role == User.ADMIN

@login_required
@user_passes_test(is_admin)
def approve_provider(request, application_id):
    if request.method == 'POST':
        application = get_object_or_404(ProviderApplication, id=application_id, status=ProviderApplication.STATUS_PENDING)
        try:
            # Create user account with properly hashed password
            user = User.objects.create_user(
                username=application.username,
                email=application.email,
                role=User.PROVIDER
            )
            # Set the password separately to ensure proper hashing
            user.set_password(application.password)
            user.save()
            
            # Update application status
            application.status = ProviderApplication.STATUS_APPROVED
            application.save()
            
            messages.success(request, f'Provider application for {application.business_name} has been approved.')
        except Exception as e:
            messages.error(request, f'Error approving provider: {str(e)}')
        
        return redirect('dashboard:admin_dashboard')

@login_required
@user_passes_test(lambda u: u.role == User.PROVIDER)
def provider_dashboard(request):
    profile, created = ProviderProfile.objects.get_or_create(user=request.user)
    
    # Get provider's services and filter active ones
    services = Service.objects.filter(gardener=request.user)
    active_services = services.filter(is_available=True)
    
    # Calculate average rating from bookings
    average_rating = (services
        .annotate(avg_rating=Avg('booking__rating'))
        .aggregate(total_avg=Avg('avg_rating'))['total_avg'])
    
    # Calculate profile completion percentage
    total_fields = 7
    filled_fields = sum(bool(getattr(profile, field)) for field in 
                       ['business_name', 'phone', 'address', 'description', 
                        'services_offered', 'years_of_experience', 'website'])
    profile_completion = int((filled_fields / total_fields) * 100)

    context = {
        'profile': profile,
        'profile_completion': profile_completion,
        'total_services': services.count(),
        'active_services': active_services.count(),
        'services': services,
        'total_bookings': 0,  # Placeholder until bookings implemented
        'average_rating': average_rating or 0,  # Default to 0 if no ratings
        'recent_bookings': [], # Placeholder until bookings implemented
    }
    return render(request, 'users/provider_dashboard.html', context)

@login_required
def provider_profile(request):
    profile, created = ProviderProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProviderProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:provider-dashboard')
    else:
        form = ProviderProfileForm(instance=profile)
    
    return render(request, 'users/provider_profile.html', {'form': form})

def provider_details(request, provider_id):
    User = get_user_model()
    provider = get_object_or_404(User, id=provider_id, role='PROVIDER')
    services = Service.objects.filter(gardener=provider, is_available=True)
    
    context = {
        'provider': provider,
        'services': services,
    }
    return render(request, 'users/provider_details.html', context)

def provider_list(request):
    User = get_user_model()
    providers = User.objects.filter(
        role='PROVIDER', 
        is_active=True
    ).prefetch_related(
        'providerprofile',
        'service_set'
    )
    
    context = {
        'providers': providers
    }
    return render(request, 'users/provider_list.html', context)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Thank you for confirming your email. You can now login.')
        return redirect('users:login')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('users:register')

def activate_provider(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        application = ProviderApplication.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, ProviderApplication.DoesNotExist):
        application = None

    if application is not None and account_activation_token.check_token(application, token):
        application.is_active = True
        application.save()
        messages.success(request, 'Thank you for verifying your email. Your application will be reviewed by an admin.')
        return redirect('users:provider-pending')
    else:
        messages.error(request, 'Activation link is invalid or has expired!')
        return redirect('users:provider-register')

@never_cache
@require_http_methods(["POST"])
def logout_view(request):
    logout(request)
    response = redirect('core:home')  # Adjust the namespace if needed
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

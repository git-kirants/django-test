from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('register/provider/', views.provider_register, name='provider-register'),
    path('provider-pending/', TemplateView.as_view(template_name='users/provider_pending.html'), name='provider-pending'),
    path('provider-applications/', views.provider_applications, name='provider-applications'),
    path('approve-provider/<int:application_id>/', views.approve_provider, name='approve-provider'),
    path('provider/dashboard/', views.provider_dashboard, name='provider-dashboard'),
    path('provider/profile/', views.provider_profile, name='provider-profile'),
    path('provider/<int:provider_id>/', views.provider_details, name='provider-details'),
    path('providers/', views.provider_list, name='provider-list'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('approve-provider/<int:provider_id>/', views.approve_provider, name='approve_provider'),
    path('activate-provider/<uidb64>/<token>/', views.activate_provider, name='activate-provider'),
    path('reject-provider/<int:application_id>/', views.reject_provider, name='reject_provider'),
]
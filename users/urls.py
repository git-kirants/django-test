# users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('register/provider/', views.provider_register, name='provider_register'),
    path('provider/profile/', views.ProviderProfileView.as_view(), name='provider_profile'),
    path('provider/dashboard/', views.ProviderDashboardView.as_view(), name='provider_dashboard'),
    path('provider/applications/', views.provider_applications, name='provider_applications'),
    path('provider/application-status/', views.check_application_status, name='application_status'),
    path('provider/approve/<int:pk>/', views.approve_provider, name='approve_provider'),
    path('logout/', views.logout_view, name='logout'),
]
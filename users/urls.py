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
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='users/password_reset.html',
             email_template_name='users/password_reset_email.html',
             subject_template_name='users/password_reset_subject.txt',
             success_url='/users/password-reset/done/'
         ),
         name='password_reset'),
         
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'
         ),
         name='password_reset_done'),
         
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='users/password_reset_confirm.html',
             success_url='/users/password-reset-complete/'
         ),
         name='password_reset_confirm'),
         
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
"""
URL configuration for gardening project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admink/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('core.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('services/', include('services.urls')),
    path('community/', include('community.urls')),
    path('bookings/', include('bookings.urls')),
    path('api/', include('api.urls')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', include('users.urls', namespace='admin')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add custom 404 handler
handler404 = 'gardening.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

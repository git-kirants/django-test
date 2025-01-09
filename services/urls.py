from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('create/', views.ServiceCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ServiceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='delete'),
    path('services/<int:service_id>/details/', views.service_details, name='service-details'),
    path('toggle-availability/<int:service_id>/', views.toggle_availability, name='toggle-availability'),
    path('search/', views.service_search, name='service-search'),
]
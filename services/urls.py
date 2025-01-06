from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.ServiceListView.as_view(), name='list'),
    path('create/', views.ServiceCreateView.as_view(), name='create'),
    path('<int:pk>/update/', views.ServiceUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='delete'),
]
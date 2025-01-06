# urls.py for community app
from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
]
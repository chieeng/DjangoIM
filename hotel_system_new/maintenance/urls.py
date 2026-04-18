from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('requests/', views.maintenance_requests, name='maintenance_requests'),
]

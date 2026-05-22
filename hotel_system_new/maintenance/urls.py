from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_index, name='index'),
    path('addNewMaintenanceRequest/', views.add_maintenance_request, name='add_maintenance_request'),
]
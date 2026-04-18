from django.urls import path
from . import views

app_name = 'services' 

urlpatterns = [
    path('', views.index, name='index'),
    path('', views.service_list, name='service_list'),
    path('addService/', views.add_service, name='add_service'),
    path('addServiceCategory/', views.add_service_category, name='add_service_category'),
    path('addServiceRequest/', views.add_service_request, name='add_service_request'),
]
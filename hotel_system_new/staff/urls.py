from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('', views.staff_index, name='index'),
    path('addNewStaffAssignment/', views.add_staff_assignment, name='add_staff_assignment'),
]
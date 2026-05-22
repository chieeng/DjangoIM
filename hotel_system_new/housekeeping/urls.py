from django.urls import path
from . import views

app_name = 'housekeeping'

urlpatterns = [
    path('', views.housekeeping_index, name='index'),
    path('addNewHousekeeping/', views.add_housekeeping, name='add_housekeeping'),
]
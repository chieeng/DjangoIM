from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('bookings/', views.my_bookings, name='my_bookings'),
]

from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('create/', views.create_reservation, name='create_reservation'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('<int:pk>/cancel/', views.cancel_reservation, name='cancel_reservation'),
    path('<int:pk>/confirm/', views.confirm_reservation, name='confirm_reservation'),
]

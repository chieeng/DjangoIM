from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('reserve/', views.reservation_details, name='reservation_details'),
    path('create/', views.create_booking, name='create_booking'),
    path('list/', views.booking_list, name='booking_list'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
]

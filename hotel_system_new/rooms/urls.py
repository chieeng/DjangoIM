from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # Index page
    path('', views.index, name='index'),
    
    # List and detail views
    path('list/', views.room_list, name='room_list'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    
    # Add new records
    path('addNewRoom/', views.add_room, name='add_room'),
    path('addNewRoomType/', views.add_room_type, name='add_room_type'),
    path('addNewReservation/', views.add_reservation, name='add_reservation'),
    path('addNewRoomAssignment/', views.add_room_assignment, name='add_room_assignment'),
]

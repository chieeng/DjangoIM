from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # Dashboard
    path('', views.index, name='index'),

    # List and detail views
    path('list/', views.room_list, name='room_list'),
    path('types/', views.room_type_list, name='room_type_list'),
    path('<int:pk>/', views.room_detail, name='room_detail'),

    # Add new records
    path('addNewRoom/', views.add_room, name='add_room'),
    path('addNewRoomType/', views.add_room_type, name='add_room_type'),
    path('addNewReservation/', views.add_reservation, name='add_reservation'),
    path('addNewRoomAssignment/', views.add_room_assignment, name='add_room_assignment'),

    # Edit records
    path('edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('type/edit/<int:pk>/', views.edit_room_type, name='edit_room_type'),

    # Delete records
    path('delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('type/delete/<int:pk>/', views.delete_room_type, name='delete_room_type'),

    # Quick status update
    path('status/<int:pk>/', views.update_room_status, name='update_room_status'),
]

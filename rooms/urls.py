from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.index, name='index'),
    path('list/', views.room_list, name='room_list'),
    path('types/', views.room_type_list, name='room_type_list'),
    path('<int:pk>/', views.room_detail, name='room_detail'),
    path('addNewRoom/', views.add_room, name='add_room'),
    path('addNewRoomType/', views.add_room_type, name='add_room_type'),
    path('addNewReservation/', views.add_reservation, name='add_reservation'),
    path('addNewRoomAssignment/', views.add_room_assignment, name='add_room_assignment'),
    path('edit/<int:pk>/', views.edit_room, name='edit_room'),
    path('type/edit/<int:pk>/', views.edit_room_type, name='edit_room_type'),
    path('delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('type/delete/<int:pk>/', views.delete_room_type, name='delete_room_type'),
    path('status/<int:pk>/', views.update_room_status, name='update_room_status'),
]

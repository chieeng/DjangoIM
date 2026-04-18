from django.contrib import admin
from .models import Room, RoomType, RoomAssignment


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'capacity', 'price_per_night')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor_number', 'room_type', 'status')
    list_filter = ('status', 'floor_number', 'room_type')
    search_fields = ('room_number',)


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'room', 'assigned_date')

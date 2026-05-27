from django.contrib import admin
from .models import Room, RoomType, RoomAssignment


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('type_name', 'max_capacity', 'price_per_night')
    search_fields = ('type_name',)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'floor_number', 'room_type', 'status', 'price_per_night')
    list_filter = ('status', 'floor_number', 'room_type')
    search_fields = ('room_number',)
    list_editable = ('status',)


@admin.register(RoomAssignment)
class RoomAssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_id', 'reservation', 'room', 'assigned_date', 'check_in_time', 'check_out_time')
    search_fields = ('room__room_number',)

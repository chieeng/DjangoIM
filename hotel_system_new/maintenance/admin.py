from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('maintenance_id', 'room', 'housekeeping', 'status', 'report_date')
    list_filter = ('status', 'report_date')
    search_fields = ('room__room_number', 'issue_description')

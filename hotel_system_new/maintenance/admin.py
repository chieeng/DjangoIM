from django.contrib import admin
from .models import MaintenanceRequest


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('maintenance_id', 'room', 'priority', 'status', 'report_date')
    list_filter = ('status', 'priority', 'report_date')
    search_fields = ('room__room_number', 'issue_description')

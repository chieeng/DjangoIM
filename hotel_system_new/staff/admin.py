from django.contrib import admin
from .models import StaffAssignment


@admin.register(StaffAssignment)
class StaffAssignmentAdmin(admin.ModelAdmin):
    list_display = ('staff', 'assigned_date', 'assignment_status')
    list_filter = ('assignment_status', 'assigned_date')

from django.contrib import admin
from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_date', 'total_bookings', 'revenue', 'occupancy_rate')
    list_filter = ('report_date',)
    search_fields = ('notes',)

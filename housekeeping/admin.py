from django.contrib import admin
from .models import Housekeeping


@admin.register(Housekeeping)
class HousekeepingAdmin(admin.ModelAdmin):
    list_display = ('housekeeping_id', 'room', 'cleaning_date', 'status')
    list_filter = ('status', 'cleaning_date')
    search_fields = ('room__room_number',)

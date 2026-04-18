from django.contrib import admin
from .models import Service, ServiceCategory, ServiceRequest


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'category', 'price')
    list_filter = ('category',)


@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('request_id', 'service', 'request_date', 'status')
    list_filter = ('status', 'request_date')

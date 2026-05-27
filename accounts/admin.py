from django.contrib import admin
from .models import CustomUser, CustomerProfile, AdminProfile, StaffProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role_type', 'status', 'created_at')
    list_filter = ('role_type', 'status', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'id_type', 'loyalty_points')
    search_fields = ('user__username', 'user__email', 'id_number')


@admin.register(AdminProfile)
class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_level', 'department')
    list_filter = ('admin_level',)


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'staff_role', 'hire_date', 'salary')
    list_filter = ('staff_role', 'hire_date')

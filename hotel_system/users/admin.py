from django.contrib import admin
from .models import User, Customer, Staff, Admin

admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Staff)
admin.site.register(Admin)
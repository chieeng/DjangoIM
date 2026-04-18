from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('review_id', 'customer', 'room', 'rating', 'review_date')
    list_filter = ('rating', 'review_date')
    search_fields = ('customer__username', 'room__room_number')

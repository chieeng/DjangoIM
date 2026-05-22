from django.db import models
from django.conf import settings
from rooms.models import Room


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='booking_records',
        null=True,
        blank=True,
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        related_name='booking_requests',
        null=True,
        blank=True,
    )
    customer_name = models.CharField(max_length=100)
    room_name = models.CharField(max_length=100, blank=True)
    room_number = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        verbose_name = 'Booking Request'
        verbose_name_plural = 'Booking Requests'
        ordering = ['-created_at', '-id']

    def __str__(self):
        room_label = self.room_name or f"Room {self.room_number}"
        return f"{self.customer_name} - {room_label}"

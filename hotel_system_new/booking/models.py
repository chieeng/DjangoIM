from django.db import models
from django.conf import settings


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
    customer_name = models.CharField(max_length=100)
    room_number = models.CharField(max_length=20)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['-created_at', '-id']

    def __str__(self):
        return f"{self.customer_name} - Room {self.room_number}"

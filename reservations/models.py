from django.db import models
from accounts.models import CustomUser
from rooms.models import Room


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    reservation_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservations'
    )
    reservation_date = models.DateField(auto_now_add=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField()
    reservation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    special_request = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        db_table = 'reservations'

    def __str__(self):
        return f"Reservation #{self.reservation_id} — {self.customer.username}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        related_name='booking'
    )
    booking_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'
        db_table = 'bookings'

    def __str__(self):
        return f"Booking #{self.booking_id} — ${self.total_amount}"

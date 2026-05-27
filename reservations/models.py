from django.db import models
from accounts.models import CustomUser
from rooms.models import Room


class Reservation(models.Model):
    """
    RESERVATION — records a guest's booking request for a room.

    FK rules (IM2):
      - customer → USER: CASCADE
        If a user account is deleted, all their reservations are deleted.
        A reservation cannot exist without an owner.

      - room → ROOM: SET_NULL
        If a room record is removed (e.g., room decommissioned),
        the historical reservation is kept for records but the room
        reference is set to null. History is preserved.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]

    reservation_id = models.AutoField(primary_key=True)
    # CASCADE: reservation belongs to a user; user deleted = reservations deleted
    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    # SET_NULL: preserve reservation history even if the room is removed
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
    """
    BOOKING — financial record tied to a confirmed reservation.

    FK rules (IM2):
      - reservation → RESERVATION: CASCADE
        A booking cannot exist without a reservation.
        If the reservation is deleted, the booking is deleted too.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    booking_id = models.AutoField(primary_key=True)
    # CASCADE: booking is a child of reservation
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

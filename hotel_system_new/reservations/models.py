from django.db import models
from accounts.models import CustomUser
from rooms.models import Room


class Reservation(models.Model):
    """Reservation model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    
    reservation_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    reservation_date = models.DateField(auto_now_add=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField()
    reservation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_request = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f"Reservation {self.reservation_id} - {self.customer.username}"

    def get_number_of_nights(self):
        """Calculate number of nights for this reservation"""
        if self.check_in_date and self.check_out_date:
            return (self.check_out_date - self.check_in_date).days
        return 0

    def get_room_price(self):
        """Get the nightly rate for the reserved room"""
        if self.room:
            return self.room.price_per_night
        return 0

    def calculate_total_amount(self):
        """Calculate total amount based on room price and number of nights"""
        nights = self.get_number_of_nights()
        room_price = self.get_room_price()
        return nights * room_price if nights > 0 else 0


class Booking(models.Model):
    """Booking model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    booking_id = models.AutoField(primary_key=True)
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='booking')
    booking_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f"Booking {self.booking_id} - ₱{self.total_amount}"

    def save(self, *args, **kwargs):
        """Auto-calculate total_amount if not provided"""
        if self.reservation and (not self.total_amount or self.total_amount == 0):
            self.total_amount = self.reservation.calculate_total_amount()
        super().save(*args, **kwargs)

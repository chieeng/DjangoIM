from django.db import models
from django.utils import timezone

from accounts.models import Customer


class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    booking_date = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booking_status = models.CharField(max_length=20, default='Pending')

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    def __str__(self):
        return str(self.booking_id)

class RoomType(models.Model):
    room_type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    max_capacity = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    room_number = models.CharField(max_length=20)
    floor_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='Available')
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    reservation_date = models.DateTimeField(default=timezone.now)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField(default=1)
    reservation_status = models.CharField(max_length=20, default='Pending')
    special_request = models.TextField(blank=True, null=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class RoomAssignment(models.Model):

    assignment_id = models.AutoField(primary_key=True)
    assigned_date = models.DateTimeField(default=timezone.now)
    check_in_time = models.TimeField(blank=True, null=True)
    check_out_time = models.TimeField(blank=True, null=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

class Invoice(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    issue_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    invoice_status = models.CharField(max_length=20, default='Unpaid')

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField(default=timezone.now)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20, default='Pending')
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Discount(models.Model):
    discount_id = models.AutoField(primary_key=True)
    discount_name = models.CharField(max_length=100)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

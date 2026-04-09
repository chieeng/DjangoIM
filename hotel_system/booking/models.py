from django.db import models
from users.models import Customer

class RoomType(models.Model):
    name = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.IntegerField()

class Booking(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
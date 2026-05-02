from django.db import models

class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    room_number = models.IntegerField()
    check_in_date = models.DateField()
    check_out_date = models.DateField()

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RoomType(models.Model):
    room_type_id = models.AutoField(primary_key=True, db_column='room_type_id')
    type_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    max_capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Room Type'
        verbose_name_plural = 'Room Types'
        db_table = 'room_types'
        ordering = ['price_per_night']

    def __str__(self):
        return f"{self.type_name} (max {self.max_capacity} guests) — ${self.price_per_night:.2f}/night"


class Room(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
        ('cleaning', 'Cleaning In Progress'),
    ]

    room_id = models.AutoField(primary_key=True, db_column='room_id')
    room_number = models.CharField(max_length=20, unique=True)
    floor_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)]
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.PROTECT,
        null=True,
        related_name='rooms'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available'
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        db_table = 'rooms'
        ordering = ['floor_number', 'room_number']

    def __str__(self):
        return f"Room {self.room_number} (Floor {self.floor_number}) — {self.get_status_display()}"

    @property
    def is_available(self):
        return self.status == 'available'


class RoomAssignment(models.Model):
    assignment_id = models.AutoField(primary_key=True, db_column='assignment_id')
    reservation = models.ForeignKey(
        'reservations.Reservation',
        on_delete=models.CASCADE,
        related_name='room_assignments'
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    assigned_date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Room Assignment'
        verbose_name_plural = 'Room Assignments'
        db_table = 'room_assignments'
        ordering = ['-assigned_date']

    def __str__(self):
        return (
            f"Assignment #{self.assignment_id} — "
            f"Room {self.room.room_number} / "
            f"Reservation #{self.reservation.reservation_id}"
        )

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class RoomType(models.Model):
    """
    ROOMTYPE — defines room categories.

    FK rules (IM2):
      - No FK outgoing from this table.
      - Rooms reference this table with PROTECT (see Room.room_type).
    """
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
    """
    ROOM — individual hotel rooms.

    FK rules (IM2):
      - room_type → ROOMTYPE: PROTECT
        A room type cannot be deleted while rooms still reference it.
        This preserves referential integrity — a room must always have
        a valid classification.
    """
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
    # PROTECT: cannot delete a RoomType that rooms are still using
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
    """
    ROOM ASSIGNMENT — records the actual check-in/check-out of a guest
    against a confirmed reservation.

    FK rules (IM2):
      - reservation → RESERVATION: CASCADE
        An assignment only exists as part of a reservation.
        If the reservation is deleted, the assignment is deleted too.

      - room → ROOM: CASCADE
        If the room record is removed, the assignment is invalid
        and is deleted as well.
    """
    assignment_id = models.AutoField(primary_key=True, db_column='assignment_id')
    # CASCADE: assignment is meaningless without its reservation
    reservation = models.ForeignKey(
        'reservations.Reservation',
        on_delete=models.CASCADE,
        related_name='room_assignments'
    )
    # CASCADE: assignment is meaningless without its room
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

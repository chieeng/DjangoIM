from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class RoomType(models.Model):
    """
    RoomType Model - Represents different room categories in the hotel
    
    This model defines room categories with their characteristics and pricing.
    Used for classification and dynamical pricing structure.
    
    Author: Information Management Student
    Date Created: April 2026
    """
    
    room_type_id = models.AutoField(primary_key=True, db_column='room_type_id')
    type_name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique identifier for room type (e.g., Single, Double, Suite, Deluxe, Penthouse, Presidential, etc.)"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of room amenities and features"
    )
    capacity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Maximum number of guests this room can accommodate"
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Base price per night (in USD)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Active room type status")

    class Meta:
        verbose_name = 'Room Type'
        verbose_name_plural = 'Room Types'
        db_table = 'room_types'
        ordering = ['price_per_night']
        indexes = [
            models.Index(fields=['type_name']),
            models.Index(fields=['price_per_night']),
        ]
        permissions = [
            ('can_manage_room_types', 'Can manage room types'),
            ('can_view_pricing', 'Can view pricing information'),
        ]

    def __str__(self):
        return f"{self.type_name} - ${self.price_per_night:.2f}/night"
    
    def __repr__(self):
        return f"<RoomType: {self.type_name}>"


class Room(models.Model):
    """
    Room Model - Represents individual rooms in the hotel inventory
    
    Maintains information about each room including location, type, and current status.
    Tracks room availability and maintenance status.
    """
    
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
        ('cleaning', 'Cleaning In Progress'),
    ]
    
    room_id = models.AutoField(primary_key=True, db_column='room_id')
    room_number = models.CharField(
        max_length=20,
        unique=True,
        help_text="Room number/identifier (e.g., 101, 202A)"
    )
    floor_number = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="Floor number where room is located"
    )
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.SET_NULL,
        null=True,
        related_name='rooms',
        help_text="Type/category of this room"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        help_text="Current occupancy status"
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Nightly rate for this specific room (may differ from room type)"
    )
    last_occupied = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'
        db_table = 'rooms'
        ordering = ['floor_number', 'room_number']
        indexes = [
            models.Index(fields=['room_number']),
            models.Index(fields=['floor_number']),
            models.Index(fields=['status']),
            models.Index(fields=['room_type', 'status']),
        ]
        permissions = [
            ('can_manage_rooms', 'Can add/edit/delete rooms'),
            ('can_update_room_status', 'Can update room status'),
            ('can_view_occupancy', 'Can view occupancy reports'),
        ]
        constraints = [ models.CheckConstraint( condition=models.Q(floor_number__gte=1), name='valid_floor_number' ),
]

    def __str__(self):
        return f"Room {self.room_number} (Floor {self.floor_number}) - {self.get_status_display()}"
    
    def __repr__(self):
        return f"<Room: {self.room_number}>"
    
    @property
    def is_available(self):
        """Check if room is available for booking"""
        return self.status == 'available'


class RoomAssignment(models.Model):
    """
    RoomAssignment Model - Tracks room assignments to guests/reservations
    
    Records when a room is assigned to a guest, including check-in/check-out times.
    Used for occupancy management and housekeeping coordination.
    """
    
    ASSIGNMENT_STATUS = [
        ('pending', 'Pending Check-In'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ]
    
    assignment_id = models.AutoField(primary_key=True, db_column='assignment_id')
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='assignments',
        help_text="Room being assigned"
    )
    assigned_date = models.DateField(auto_now_add=True)
    check_in_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Actual check-in time"
    )
    check_out_time = models.TimeField(
        null=True,
        blank=True,
        help_text="Actual check-out time"
    )
    status = models.CharField(
        max_length=20,
        choices=ASSIGNMENT_STATUS,
        default='pending',
        help_text="Current assignment status"
    )
    notes = models.TextField(blank=True, help_text="Additional notes for housekeeping")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Room Assignment'
        verbose_name_plural = 'Room Assignments'
        db_table = 'room_assignments'
        ordering = ['-assigned_date']
        indexes = [
            models.Index(fields=['room', 'assigned_date']),
            models.Index(fields=['status']),
        ]
        permissions = [
            ('can_assign_rooms', 'Can assign rooms to guests'),
            ('can_update_assignment_status', 'Can update assignment status'),
        ]

    def __str__(self):
        return f"Assignment {self.assignment_id} - {self.room} ({self.get_status_display()})"
    
    def __repr__(self):
        return f"<RoomAssignment: Room {self.room.room_number}>"

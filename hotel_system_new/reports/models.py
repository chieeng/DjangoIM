from django.db import models
from datetime import date


class Report(models.Model):
    report_date = models.DateField('Report Date')
    total_bookings = models.PositiveIntegerField('Total Bookings', default=0, editable=False)
    revenue = models.DecimalField('Total Revenue', max_digits=12, decimal_places=2, default=0, editable=False)
    occupancy_rate = models.DecimalField(
        'Occupancy Rate (%)',
        max_digits=5,
        decimal_places=2,
        help_text='Automatically calculated from room occupancy',
        default=0,
        editable=False,
    )
    notes = models.TextField('Notes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-report_date']
        verbose_name = 'Booking Report'
        verbose_name_plural = 'Booking Reports'
        constraints = [
            models.UniqueConstraint(fields=['report_date'], name='unique_report_date'),
        ]

    def __str__(self):
        return f'Report for {self.report_date}'

    def calculate_data(self):
        """Calculate all report data from database records for the report_date"""
        from reservations.models import Booking, Reservation
        from rooms.models import Room
        from django.db.models import Sum, Count, Q

        # Get all bookings for this date (from booking_date)
        bookings = Booking.objects.filter(
             reservation__check_in_date=self.report_date,
             booking_status__in=['confirmed', 'completed']
        )

        # Calculate total bookings
        self.total_bookings = bookings.count()

        # Calculate total revenue from bookings on this date
        total_revenue = bookings.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        self.revenue = total_revenue

        # Calculate occupancy rate
        # Count rooms that are occupied on this date (have active reservations where check_in_date <= report_date < check_out_date)
        occupied_rooms = Reservation.objects.filter(
            Q(check_in_date__lte=self.report_date) &
            Q(check_out_date__gt=self.report_date) &
            Q(reservation_status__in=['checked_in', 'checked_out', 'confirmed']) &
            Q(room__isnull=False)
        ).values('room').distinct().count()

        total_rooms = Room.objects.count()
        if total_rooms > 0:
            self.occupancy_rate = (occupied_rooms / total_rooms) * 100
        else:
            self.occupancy_rate = 0

        return self

    def save(self, *args, **kwargs):
        """Save the report - data is only calculated when bookings are created/updated"""
        super().save(*args, **kwargs)

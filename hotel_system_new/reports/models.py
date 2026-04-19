from django.db import models


class Report(models.Model):
    report_date = models.DateField('Report Date')
    total_bookings = models.PositiveIntegerField('Total Bookings', default=0)
    revenue = models.DecimalField('Total Revenue', max_digits=12, decimal_places=2, default=0)
    occupancy_rate = models.DecimalField(
        'Occupancy Rate (%)',
        max_digits=5,
        decimal_places=2,
        help_text='Enter occupancy percentage as a number, for example 75.00',
        default=0,
    )
    notes = models.TextField('Notes', blank=True)

    class Meta:
        ordering = ['-report_date']
        verbose_name = 'Booking Report'
        verbose_name_plural = 'Booking Reports'

    def __str__(self):
        return f'Report for {self.report_date}'

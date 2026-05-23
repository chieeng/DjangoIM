from django.db import models
from rooms.models import Room


class MaintenanceRequest(models.Model):
    """Maintenance Request — ERD: maintenance_ID, issue_description, report_date, resolved_date, status."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    maintenance_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name='maintenance_requests',
    )
    housekeeping = models.ForeignKey(
        'housekeeping.Housekeeping',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='maintenance_requests',
    )
    issue_description = models.TextField()
    report_date = models.DateField(auto_now_add=True)
    resolved_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = 'Maintenance Request'
        verbose_name_plural = 'Maintenance Requests'

    def __str__(self):
        return f"Maintenance {self.maintenance_id} - {self.room} ({self.get_status_display()})"

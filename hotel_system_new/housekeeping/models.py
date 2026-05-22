from django.db import models
from accounts.models import CustomUser
from rooms.models import Room


class Housekeeping(models.Model):
    """Housekeeping model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    housekeeping_id = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='housekeeping_tasks')
    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role_type': 'staff'},
    )
    cleaning_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Housekeeping'
        verbose_name_plural = 'Housekeeping Tasks'

    def __str__(self):
        return f"Housekeeping {self.housekeeping_id} - {self.room} ({self.get_status_display()})"

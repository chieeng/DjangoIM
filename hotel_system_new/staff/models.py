from django.db import models
from accounts.models import CustomUser


class StaffAssignment(models.Model):
    """Staff Assignment — ERD: staff_assignment_ID, assigned_date, completion_date, assignment_status."""
    STATUS_CHOICES = [
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    staff_assignment_id = models.AutoField(primary_key=True)
    staff = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role_type': 'staff'},
    )
    maintenance_request = models.ForeignKey(
        'maintenance.MaintenanceRequest',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='staff_assignments',
    )
    assigned_date = models.DateField(auto_now_add=True)
    completion_date = models.DateField(null=True, blank=True)
    assignment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='assigned')
    order = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = 'Staff Assignment'
        verbose_name_plural = 'Staff Assignments'

    def __str__(self):
        return f"Assignment {self.staff_assignment_id} - {self.staff.username}"

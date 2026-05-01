from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

ROLE_CHOICES = [
    ('customer', 'Customer'),
    ('staff', 'Staff'),
    ('admin', 'Admin'),
]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
]

class CustomUser(AbstractUser):
    """Custom User model representing the USER entity from ERD"""
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Phone number must be between 9 and 15 digits.'
    )
    
    user_id = models.AutoField(primary_key=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    role_type = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_custom = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class CustomerProfile(models.Model):
    """Customer Profile - extends CustomUser for customer-specific data"""
    ID_TYPE_CHOICES = [
        ('passport', 'Passport'),
        ('drivers_license', "Driver's License"),
        ('national_id', 'National ID'),
        ('other', 'Other'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    address = models.TextField(blank=True)
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES, blank=True)
    id_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    loyalty_points = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Customer Profile'
        verbose_name_plural = 'Customer Profiles'

    def __str__(self):
        return f"Customer: {self.user.username}"


class AdminProfile(models.Model):
    """Admin Profile - extends CustomUser for admin-specific data"""
    ADMIN_LEVEL_CHOICES = [
        ('super', 'Super Admin'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')
    admin_level = models.CharField(max_length=20, choices=ADMIN_LEVEL_CHOICES)
    department = models.CharField(max_length=100, blank=True)
    permissions = models.TextField(help_text="Comma-separated permissions")

    class Meta:
        verbose_name = 'Admin Profile'
        verbose_name_plural = 'Admin Profiles'

    def __str__(self):
        return f"Admin: {self.user.username}"


class StaffProfile(models.Model):
    """Staff Profile - extends CustomUser for staff-specific data"""
    STAFF_ROLE_CHOICES = [
        ('receptionist', 'Receptionist'),
        ('housekeeper', 'Housekeeper'),
        ('chef', 'Chef'),
        ('manager', 'Manager'),
        ('maintenance', 'Maintenance'),
        ('security', 'Security'),
    ]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='staff_profile')
    staff_role = models.CharField(max_length=20, choices=STAFF_ROLE_CHOICES)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    staff_schedule = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = 'Staff Profile'
        verbose_name_plural = 'Staff Profiles'

    def __str__(self):
        return f"Staff: {self.user.username} - {self.get_staff_role_display()}"

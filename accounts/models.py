from django.db import models
from django.utils import timezone

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    password_hash = models.CharField(max_length=255)
    role_type = models.CharField(max_length=20)
    status = models.CharField(max_length=20, default='Active')
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    address = models.TextField(blank=True, null=True)
    id_type = models.CharField(max_length=50)
    id_number = models.CharField(max_length=50)
    loyalty_points = models.PositiveIntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.customer_id)


class Admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_level = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    permissions = models.TextField(blank=True, null=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_role = models.CharField(max_length=50)
    hire_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    shift_schedule = models.CharField(max_length=100)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
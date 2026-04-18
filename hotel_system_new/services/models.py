from django.db import models


class ServiceCategory(models.Model):
    """Service Category model"""
    service_category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Service Category'
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.category_name


class Service(models.Model):
    """Service model"""
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    category = models.ForeignKey(ServiceCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'

    def __str__(self):
        return f"{self.service_name} - ${self.price}"


class ServiceRequest(models.Model):
    """Service Request model"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    request_id = models.AutoField(primary_key=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    quantity = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Service Request'
        verbose_name_plural = 'Service Requests'

    def __str__(self):
        return f"Service Request {self.request_id} - {self.service.service_name}"

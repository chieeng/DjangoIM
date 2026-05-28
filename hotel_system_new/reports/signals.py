from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datetime import datetime
from reservations.models import Booking
from .models import Report


@receiver(post_save, sender=Booking)
def update_report_on_booking_create(sender, instance, created, **kwargs):
    """Auto-update or create report when a booking is created or updated"""
    booking_date = instance.booking_date
    
    # Get or create report for this date
    report, _ = Report.objects.get_or_create(report_date=booking_date)
    
    # Calculate data and save
    report.calculate_data()
    report.save()


@receiver(post_delete, sender=Booking)
def update_report_on_booking_delete(sender, instance, **kwargs):
    """Auto-update report when a booking is deleted"""
    booking_date = instance.booking_date
    
    try:
        report = Report.objects.get(report_date=booking_date)
        # Recalculate the data
        report.calculate_data()
        report.save()
    except Report.DoesNotExist:
        pass

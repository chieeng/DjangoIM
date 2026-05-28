"""
Test script to verify the Booking to Report Sync system works correctly.
Run this with: python manage.py shell < test_booking_sync.py
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_system.settings')
django.setup()

from django.db import transaction
from reservations.models import Reservation, Booking
from rooms.models import Room, RoomType
from accounts.models import CustomUser
from reports.models import Report

print("=" * 80)
print("BOOKING TO REPORT SYNC TEST")
print("=" * 80)

try:
    with transaction.atomic():
        # Step 1: Create test data
        print("\n[1] Creating test data...")
        
        # Create or get a room type
        room_type, _ = RoomType.objects.get_or_create(
            type_name='Test Suite',
            defaults={'capacity': 2, 'price_per_night': 150.00}
        )
        print(f"✓ Room Type: {room_type.type_name}")
        
        # Create or get a room
        room, created = Room.objects.get_or_create(
            room_number='TEST-101',
            defaults={
                'floor_number': 1,
                'room_type': room_type,
                'status': 'available',
                'price_per_night': 150.00
            }
        )
        print(f"✓ Room: {room.room_number}")
        
        # Create or get a customer
        customer, created = CustomUser.objects.get_or_create(
            username='testcustomer',
            defaults={'email': 'test@example.com', 'role_type': 'customer', 'first_name': 'Test', 'last_name': 'Customer'}
        )
        print(f"✓ Customer: {customer.username}")
        
        # Step 2: Create a reservation
        print("\n[2] Creating reservation...")
        test_date = date.today()
        reservation = Reservation.objects.create(
            customer=customer,
            room=room,
            check_in_date=test_date,
            check_out_date=test_date + timedelta(days=2),
            number_of_guests=2,
            reservation_status='confirmed'
        )
        print(f"✓ Reservation created: ID {reservation.reservation_id}")
        print(f"  - Check-in: {reservation.check_in_date}")
        print(f"  - Check-out: {reservation.check_out_date}")
        
        # Step 3: Create a booking (this triggers the signal)
        print("\n[3] Creating booking (this will trigger report sync)...")
        booking = Booking.objects.create(
            reservation=reservation,
            total_amount=300.00,
            booking_status='confirmed'
        )
        print(f"✓ Booking created: ID {booking.booking_id}")
        print(f"  - Amount: ₱{booking.total_amount}")
        print(f"  - Booking Date: {booking.booking_date}")
        
        # Step 4: Check if report was automatically created/updated
        print("\n[4] Verifying report sync...")
        report = Report.objects.get(report_date=booking.booking_date)
        print(f"✓ Report found for date: {report.report_date}")
        print(f"\n   📊 REPORT DATA:")
        print(f"   - Total Bookings: {report.total_bookings}")
        print(f"   - Total Revenue: ₱{report.revenue:.2f}")
        print(f"   - Occupancy Rate: {report.occupancy_rate:.2f}%")
        
        # Step 5: Verify calculations
        print("\n[5] Verification Results...")
        assert report.total_bookings >= 1, "Total bookings should be at least 1"
        assert report.revenue >= 300.00, "Revenue should be at least $300"
        assert report.occupancy_rate > 0, "Occupancy rate should be greater than 0"
        print("✓ All calculations verified!")
        
        print("\n" + "=" * 80)
        print("✅ TEST PASSED: Booking to Report Sync is working correctly!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Go to http://127.0.0.1:8000/admin/")
        print("2. Log in with your superuser credentials (admin1 / your_password)")
        print("3. Click on 'Booking Reports' to see the generated report")
        print("4. Try creating more bookings and watch the reports update in real-time")
        print("=" * 80)

except Exception as e:
    print(f"\n❌ TEST FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    print("=" * 80)

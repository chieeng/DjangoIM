#!/usr/bin/env python
"""
Create sample reservations for demonstration
Run from: python create_sample_reservations.py
"""
import os
import sys
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from rooms.models import Room
from reservations.models import Reservation
from accounts.models import CustomUser

def create_sample_reservations():
    print("Creating sample reservations...\n")
    
    # Get or create a customer user for reservations
    customer, created = CustomUser.objects.get_or_create(
        username='guest_user',
        defaults={
            'email': 'guest@hotel.com',
            'first_name': 'Guest',
            'last_name': 'User',
            'role_type': 'customer',
            'is_active': True,
        }
    )
    if created:
        customer.set_password('123456')
        customer.save()
        print(f"✓ Created guest user: {customer.username}")
    
    # Sample reservation data
    today = datetime.now().date()
    reservations_data = [
        {
            'room_number': '301',
            'check_in': today + timedelta(days=1),
            'check_out': today + timedelta(days=3),
            'number_of_guests': 2,
            'reservation_status': 'confirmed',
            'special_request': 'High floor preferred',
        },
        {
            'room_number': '202',
            'check_in': today + timedelta(days=5),
            'check_out': today + timedelta(days=7),
            'number_of_guests': 1,
            'reservation_status': 'confirmed',
            'special_request': 'Early check-in requested',
        },
        {
            'room_number': '103',
            'check_in': today + timedelta(days=10),
            'check_out': today + timedelta(days=12),
            'number_of_guests': 3,
            'reservation_status': 'pending',
            'special_request': 'Honeymoon suite requested',
        },
        {
            'room_number': '401',
            'check_in': today + timedelta(days=15),
            'check_out': today + timedelta(days=18),
            'number_of_guests': 4,
            'reservation_status': 'confirmed',
            'special_request': 'Business meeting setup needed',
        },
        {
            'room_number': '203',
            'check_in': today + timedelta(days=20),
            'check_out': today + timedelta(days=22),
            'number_of_guests': 2,
            'reservation_status': 'confirmed',
            'special_request': 'Non-smoking room',
        },
    ]
    
    for res_data in reservations_data:
        # Get the room
        try:
            room = Room.objects.get(room_number=res_data['room_number'])
            
            # Create or get reservation
            reservation, created = Reservation.objects.get_or_create(
                customer=customer,
                room=room,
                check_in_date=res_data['check_in'],
                defaults={
                    'check_out_date': res_data['check_out'],
                    'number_of_guests': res_data['number_of_guests'],
                    'reservation_status': res_data['reservation_status'],
                    'special_request': res_data['special_request'],
                }
            )
            
            if created:
                status = "✓ Created"
            else:
                status = "⚠ Already exists"
            
            print(f"{status}: Reservation for Room {room.room_number} ({res_data['check_in']} to {res_data['check_out']})")
        except Room.DoesNotExist:
            print(f"✗ Room {res_data['room_number']} not found")
    
    print("\n" + "="*60)
    print(f"\n✅ Sample Reservations Created!")
    print(f"   • Total Reservations: {Reservation.objects.count()}")
    print(f"   • Guest User: {customer.username}")

if __name__ == '__main__':
    try:
        create_sample_reservations()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python
"""
Create sample rooms and room types for the hotel system
Run from: python create_sample_rooms.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_system.settings')
sys.path.insert(0, os.path.dirname(__file__))
django.setup()

from rooms.models import RoomType, Room

def create_sample_rooms():
    print("Creating sample room types and rooms...\n")
    
    # Create Room Types
    room_types_data = [
        {
            'type_name': 'Single Room',
            'description': 'Cozy room for solo travelers with single bed',
            'capacity': 1,
            'price_per_night': 4900.00,
            'is_active': True,
        },
        {
            'type_name': 'Double Room',
            'description': 'Comfortable room for couples with queen-size bed',
            'capacity': 2,
            'price_per_night': 7100.00,
            'is_active': True,
        },
        {
            'type_name': 'Twin Room',
            'description': 'Room with two single beds, perfect for friends',
            'capacity': 2,
            'price_per_night': 6500.00,
            'is_active': True,
        },
        {
            'type_name': 'Suite',
            'description': 'Spacious suite with living area and bedroom',
            'capacity': 3,
            'price_per_night': 10400.00,
            'is_active': True,
        },
        {
            'type_name': 'Deluxe Room',
            'description': 'Premium room with modern amenities and balcony',
            'capacity': 4,
            'price_per_night': 13700.00,
            'is_active': True,
        },
        {
            'type_name': 'Penthouse',
            'description': 'Luxury penthouse with spectacular views',
            'capacity': 6,
            'price_per_night': 27500.00,
            'is_active': True,
        },
    ]
    
    room_types = {}
    for rt_data in room_types_data:
        rt, created = RoomType.objects.get_or_create(
            type_name=rt_data['type_name'],
            defaults={
                'description': rt_data['description'],
                'capacity': rt_data['capacity'],
                'price_per_night': rt_data['price_per_night'],
                'is_active': rt_data['is_active'],
            }
        )
        room_types[rt_data['type_name']] = rt
        status = "✓ Created" if created else "⚠ Already exists"
        print(f"{status}: {rt_data['type_name']} - ₱{rt_data['price_per_night']:.2f}/night")
    
    print("\n" + "="*60)
    print("Creating sample rooms...\n")
    
    # Create Rooms
    rooms_data = [
        # Ground Floor (101-110)
        {'room_number': '101', 'floor_number': 1, 'room_type': 'Single Room', 'price_per_night': 4900.00},
        {'room_number': '102', 'floor_number': 1, 'room_type': 'Single Room', 'price_per_night': 4900.00},
        {'room_number': '103', 'floor_number': 1, 'room_type': 'Double Room', 'price_per_night': 7100.00},
        {'room_number': '104', 'floor_number': 1, 'room_type': 'Double Room', 'price_per_night': 7100.00},
        {'room_number': '105', 'floor_number': 1, 'room_type': 'Twin Room', 'price_per_night': 6500.00},
        
        # Second Floor (201-210)
        {'room_number': '201', 'floor_number': 2, 'room_type': 'Single Room', 'price_per_night': 4900.00},
        {'room_number': '202', 'floor_number': 2, 'room_type': 'Double Room', 'price_per_night': 7100.00},
        {'room_number': '203', 'floor_number': 2, 'room_type': 'Suite', 'price_per_night': 10400.00},
        {'room_number': '204', 'floor_number': 2, 'room_type': 'Twin Room', 'price_per_night': 6500.00},
        {'room_number': '205', 'floor_number': 2, 'room_type': 'Double Room', 'price_per_night': 7100.00},
        
        # Third Floor (301-310)
        {'room_number': '301', 'floor_number': 3, 'room_type': 'Deluxe Room', 'price_per_night': 13700.00},
        {'room_number': '302', 'floor_number': 3, 'room_type': 'Suite', 'price_per_night': 10400.00},
        {'room_number': '303', 'floor_number': 3, 'room_type': 'Deluxe Room', 'price_per_night': 13700.00},
        {'room_number': '304', 'floor_number': 3, 'room_type': 'Double Room', 'price_per_night': 7100.00},
        {'room_number': '305', 'floor_number': 3, 'room_type': 'Suite', 'price_per_night': 10400.00},
        
        # Fourth Floor (401-405)
        {'room_number': '401', 'floor_number': 4, 'room_type': 'Penthouse', 'price_per_night': 27500.00},
        {'room_number': '402', 'floor_number': 4, 'room_type': 'Deluxe Room', 'price_per_night': 13700.00},
    ]
    
    total = 0
    for room_data in rooms_data:
        room_type = room_types[room_data['room_type']]
        room, created = Room.objects.get_or_create(
            room_number=room_data['room_number'],
            defaults={
                'floor_number': room_data['floor_number'],
                'room_type': room_type,
                'status': 'available',
                'price_per_night': room_data['price_per_night'],
            }
        )
        if created:
            total += 1
            print(f"✓ Created: Room {room_data['room_number']} ({room_data['room_type']}) - ₱{room_data['price_per_night']:.2f}/night")
        else:
            print(f"⚠ Already exists: Room {room_data['room_number']}")
    
    print("\n" + "="*60)
    print(f"\n✅ Sample Data Created Successfully!")
    print(f"   • Room Types: {len(room_types_data)}")
    print(f"   • New Rooms: {total}/{len(rooms_data)}")
    print(f"   • Total Rooms: {Room.objects.count()}")
    print("\nTest Credentials:")
    print("   • Admin: eragritchiegg@gmail.com / 123")
    print("   • Staff: ritchieerag@gmail.com / 123")

if __name__ == '__main__':
    try:
        create_sample_rooms()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

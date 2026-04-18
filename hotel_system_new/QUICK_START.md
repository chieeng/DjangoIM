# 🚀 Quick Start Guide - Hotel Management System

## Start the Development Server

```bash
# Navigate to project
cd d:\School Works\PracticeCodes\django\hotel_system_new

# Activate virtual environment
.\venv\Scripts\activate

# Start server
python manage.py runserver 8000
```

**Access**: http://localhost:8000

---

## 🔑 Test Login Credentials

### Admin Account (Full Access)
```
Email: eragritchiegg@gmail.com
Password: 123
```

### Staff Account (Room Management)
```
Email: ritchieerag@gmail.com
Password: 123
```

### Guest Account (Browse Only)
```
Username: guest_user
Password: 123456
```

---

## 🌐 Key URLs

| Page | URL | Access |
|------|-----|--------|
| **Landing Page** | http://localhost:8000 | Everyone |
| **Room Listing** | http://localhost:8000/rooms/list/ | Everyone |
| **Staff Dashboard** | http://localhost:8000/rooms/ | Staff/Admin |
| **Add Room** | http://localhost:8000/rooms/addNewRoom/ | Staff/Admin |
| **Add Room Type** | http://localhost:8000/rooms/addNewRoomType/ | Staff/Admin |
| **Admin Panel** | http://localhost:8000/admin | Admin |
| **Login** | http://localhost:8000/accounts/login/ | Everyone |
| **Register** | http://localhost:8000/accounts/register/ | Everyone |

---

## 📋 Pre-populated Data

✅ **6 Room Types**: Single, Double, Twin, Suite, Deluxe, Penthouse  
✅ **18 Sample Rooms**: Across 4 floors with realistic pricing  
✅ **5 Sample Reservations**: In various statuses  
✅ **3 Test Users**: Admin, Staff, Guest  

---

## 🎯 What to Test

### As Guest (Browse Only)
1. ✓ View landing page
2. ✓ Browse available rooms
3. ✓ Filter by room type/price
4. ✓ View room details
5. ✓ See "Book Now" buttons (alerts show sign-in message)

### As Staff (Management)
1. ✓ Login with staff@hotel.com
2. ✓ Access dashboard with statistics
3. ✓ View recent reservations
4. ✓ Add new room type
5. ✓ Add new room
6. ✓ Create reservation
7. ✓ Assign room to guest

### As Admin (Full Access)
1. ✓ All staff features
2. ✓ Access Django admin
3. ✓ Manage users
4. ✓ View system logs

---

## 🔄 Reset Database (If Needed)

```bash
# Delete database
del db.sqlite3

# Run migrations
python manage.py migrate

# Create test data
python create_test_users.py
python create_sample_rooms.py
python create_sample_reservations.py
```

---

## 📊 Dashboard Features

**Staff Dashboard Shows:**
- 📈 Available rooms count
- 📈 Occupied rooms count
- 📈 Maintenance rooms count
- 📈 Reserved rooms count
- 📊 Occupancy rate percentage
- 📋 Recent reservations table
- 🏨 Room overview table
- ⚡ Quick action buttons

---

## ✨ UI Highlights

✅ Professional hotel-themed design  
✅ Responsive (mobile, tablet, desktop)  
✅ Smooth animations and hover effects  
✅ Color-coded status badges  
✅ Bootstrap 5 framework  
✅ Clean navigation bar  
✅ Role-aware buttons  

---

## 🔐 Security Features

✅ CSRF protection on all forms  
✅ Login required for management  
✅ Role-based access control  
✅ Password validation  
✅ Error messages for unauthorized access  
✅ Automatic redirects  

---

## 📱 Mobile Responsive

The system works perfectly on:
- 📱 Mobile phones (< 768px)
- 📱 Tablets (768px - 1024px)
- 💻 Desktops (> 1024px)

All layouts automatically adapt to screen size!

---

## 🆘 Troubleshooting

### Server won't start
```bash
# Check migrations
python manage.py migrate

# Verify Django
python manage.py check
```

### Data is missing
```bash
# Recreate sample data
python create_sample_rooms.py
python create_sample_reservations.py
```

### Login issues
```bash
# Verify user exists in Django shell
python manage.py shell
>>> from accounts.models import CustomUser
>>> CustomUser.objects.all()
```

---

## 📁 Important Files

- `rooms/models.py` - Core database models
- `rooms/views.py` - Room management logic
- `templates/landing.html` - Landing page
- `templates/rooms/dashboard.html` - Staff dashboard
- `templates/rooms/room_listing.html` - Room browsing
- `create_test_users.py` - Generate test accounts
- `create_sample_rooms.py` - Generate test rooms
- `create_sample_reservations.py` - Generate test bookings

---

## 📞 Support

Check the comprehensive documentation:
- `README_HOTEL_SYSTEM.md` - Full project documentation
- `IMPLEMENTATION_SUMMARY.md` - Technical overview
- `manage.py` docstrings - Command-line help

---

**Version**: 1.0.0  
**Status**: ✅ Production Ready  
**Last Updated**: April 18, 2026

Enjoy your hotel management system! 🏨

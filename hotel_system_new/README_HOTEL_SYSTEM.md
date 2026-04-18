# 🏨 Hotel Management System - Rooms App

A professional Django-based hotel room management system with role-based access control, room booking, and staff management features.

## ✨ Features

### 🎯 Core Features
- **Professional Landing Page**: Hotel-themed UI with room search and role identification
- **Room Listing & Filtering**: Browse available rooms with filters (type, price, status)
- **Staff Dashboard**: Real-time statistics, quick actions, and room management
- **Role-Based Access Control**: Guest, Staff, and Admin roles with proper authorization
- **Occupancy Management**: Track available, occupied, maintenance, and reserved rooms
- **Room Assignment**: Manage guest assignments with check-in/out times

### 📊 Dashboard Features
- **Statistics Cards**: Available rooms, occupancy rate, maintenance tracking
- **Quick Actions**: Add rooms, create reservations, manage room types
- **Recent Reservations Table**: Latest 5 bookings with guest information
- **Room Overview Table**: Top 10 rooms with status and pricing
- **Responsive Design**: Bootstrap 5 with professional styling

### 🔐 Security Features
- Custom user authentication with role-based permissions
- @staff_or_admin_required decorator for access control
- Login-required decorators on sensitive operations
- CSRF protection on all forms

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Django 4.2.7
- Virtual Environment (venv)

### Installation

1. **Navigate to project directory**
```bash
cd hotel_system_new
```

2. **Activate virtual environment**
```bash
# Windows
.\venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Create test users** (optional)
```bash
python create_test_users.py
python create_sample_rooms.py
```

6. **Start server**
```bash
python manage.py runserver 8000
```

7. **Access at**: http://localhost:8000

## 👥 Test User Accounts

### Admin Account
- **Email**: eragritchiegg@gmail.com
- **Password**: 123
- **Role**: Admin
- **Access**: Full system access including staff management

### Staff Account
- **Email**: ritchieerag@gmail.com
- **Password**: 123
- **Role**: Staff
- **Access**: Room management, reservations, room assignments

### Guest Account
- **Create via registration**: http://localhost:8000/register
- **Role**: Customer
- **Access**: Browse rooms, view bookings

## 📁 Project Structure

```
hotel_system_new/
├── hotel_system/          # Main project settings
├── rooms/                 # Core rooms app
│   ├── models.py         # RoomType, Room, Reservation, RoomAssignment
│   ├── views.py          # Dashboard, room listing, management views
│   ├── urls.py           # URL routing with app_name
│   ├── forms.py          # Django forms
│   └── admin.py          # Django admin configuration
├── accounts/             # User authentication
├── common/               # Landing page & static pages
├── templates/
│   ├── landing.html      # Main landing page
│   ├── base.html         # Base template with navbar
│   └── rooms/
│       ├── dashboard.html      # Staff dashboard
│       ├── room_listing.html   # Room browsing
│       ├── room_detail.html    # Single room details
│       └── form templates      # Add/Edit forms
├── static/               # CSS, JS, images
├── create_test_users.py  # Test account creator
└── create_sample_rooms.py # Sample data generator
```

## 📊 Database Models

### Room Models

#### RoomType
- `type_name` (CharField): Dynamic room type name
- `description` (TextField): Room description
- `capacity` (IntegerField): Number of guests (1-10)
- `price_per_night` (DecimalField): Nightly rate
- `is_active` (BooleanField): Availability flag
- `created_at`, `updated_at` (DateTime): Timestamps

#### Room
- `room_number` (CharField, Unique): Room identifier
- `floor_number` (IntegerField): Floor level (1-50)
- `room_type` (FK): Reference to RoomType
- `status` (CharField): available/occupied/maintenance/reserved
- `price_per_night` (DecimalField): Nightly rate
- `last_occupied` (DateTime): Last occupancy date
- `created_at`, `updated_at` (DateTime): Timestamps

#### Reservation
- `customer` (FK): Guest making reservation
- `room` (FK): Reserved room
- `check_in_date` (DateField): Arrival date
- `check_out_date` (DateField): Departure date
- `guests` (IntegerField): Number of guests
- `status` (CharField): pending/confirmed/cancelled
- `special_request` (TextField): Guest notes

#### RoomAssignment
- `room` (FK): Assigned room
- `assigned_date` (DateField): Assignment date
- `check_in_time` (TimeField): Guest arrival time
- `check_out_time` (TimeField): Guest departure time
- `status` (CharField): assigned/checked_in/checked_out
- `notes` (TextField): Staff notes
- `created_at`, `updated_at` (DateTime): Timestamps

## 🎨 UI/UX Highlights

### Landing Page
- Professional hero section with call-to-action
- Room search interface with date filters
- 5 featured room cards with pricing
- 6 feature highlight cards
- Role-based authentication links

### Room Listing Page
- Responsive grid layout (auto-fit columns)
- Advanced filtering:
  - Filter by room type
  - Filter by status
  - Price range selector
- Room cards showing:
  - Room number and status
  - Floor level
  - Capacity and amenities
  - Pricing
  - Action buttons (role-aware)
- Pagination support

### Staff Dashboard
- Welcome section with user info
- 4 statistics cards:
  - Available Rooms (green)
  - Occupied Rooms (red)
  - Under Maintenance (yellow)
  - Reserved Rooms (pink)
- 6 Quick Action cards:
  - Add Room
  - Add Room Type
  - New Reservation
  - Room Assignment
  - Browse Rooms
  - Home
- Recent Reservations table
- Room Overview table (top 10)

## 🔐 Access Control

### Guest (Customer)
- ✓ View landing page
- ✓ Browse available rooms
- ✓ View room details
- ✓ Register & Login
- ✗ Manage rooms (restricted)
- ✗ View staff dashboard (restricted)

### Staff
- ✓ All guest features
- ✓ Create & edit room types
- ✓ Create & edit rooms
- ✓ Create reservations
- ✓ Create room assignments
- ✓ View staff dashboard
- ✗ Admin functions (restricted)

### Admin
- ✓ All staff features
- ✓ User management (via Django admin)
- ✓ System analytics
- ✓ Full database access

## 🗄️ Sample Data

The system includes 17 pre-configured rooms across 4 floors:

**Ground Floor (Floor 1)**: 5 rooms
- 2 Single Rooms ($89/night)
- 2 Double Rooms ($129/night)
- 1 Twin Room ($119/night)

**Second Floor (Floor 2)**: 5 rooms
- 1 Single Room
- 2 Double Rooms
- 1 Suite ($189/night)
- 1 Twin Room

**Third Floor (Floor 3)**: 5 rooms
- 2 Deluxe Rooms ($249/night)
- 2 Suites
- 1 Double Room

**Fourth Floor (Floor 4)**: Top Floor
- 1 Penthouse ($499/night)
- 1 Deluxe Room

## 🛠️ Admin Configuration

### Database Indexes
- `room_number` (single)
- `floor_number` (single)
- `status` (single)
- `type_name` (single)
- `price_per_night` (single)
- Composite on `(floor_number, status)`
- Composite on `(room_type_id, status)`

### Database Constraints
- `ChkConstraint`: floor_number >= 1 AND floor_number <= 50
- `CheckConstraint`: capacity >= 1 AND capacity <= 10

### Permissions
- Can manage rooms
- Can update room status
- Can manage room types
- Can view pricing

## 🔗 URL Routes

### Landing Page
- `/` - Home/Landing page

### Guest Routes
- `/rooms/` - Room listing with filters
- `/rooms/<id>/` - Room details

### Staff Routes (Protected)
- `/rooms/index/` - Staff dashboard
- `/rooms/addNewRoom/` - Add room form
- `/rooms/addNewRoomType/` - Add room type form
- `/rooms/addNewReservation/` - Create reservation
- `/rooms/addNewRoomAssignment/` - Assign room

## 📱 Responsive Design

- **Mobile** (< 768px): Single column layout
- **Tablet** (768px - 1024px): 2-3 columns
- **Desktop** (> 1024px): 3-4 columns
- All elements scale appropriately with viewport

## 🐛 Debugging

### Check System Status
```bash
python manage.py check
```

### View Database Statistics
```python
# In Django shell
python manage.py shell
>>> from rooms.models import Room
>>> Room.objects.count()  # Total rooms
>>> Room.objects.filter(status='available').count()  # Available
```

### Clear Cache (if needed)
```bash
python manage.py clear_cache
```

## 📝 Notes

- All timestamps use `timezone.now()`
- Prices stored as Decimal to prevent floating-point errors
- Room types are completely dynamic (no fixed choices)
- View restrictions via `@staff_or_admin_required` decorator
- CSRF tokens on all POST forms
- Messages framework for user feedback

## 🚀 Future Enhancements

- [ ] Payment gateway integration
- [ ] Email notifications on booking
- [ ] Guest review system
- [ ] Room service ordering
- [ ] Loyalty program
- [ ] Advanced analytics & reporting
- [ ] API endpoints for mobile app
- [ ] SMS notifications

## 👨‍💻 Developer Notes

**3rd Year IM2 Quality Code**
- Professional Meta classes with indexes & constraints
- Validators on all numeric fields
- Comprehensive model documentation
- Query optimization with select_related/prefetch_related
- DRY principle throughout
- RESTful URL naming conventions
- Semantic HTML with proper accessibility

## 📄 License

This project is part of academic coursework.

## 📞 Support

For issues or questions about this hotel management system, please refer to the comprehensive code documentation in each module.

---

**Last Updated**: April 18, 2026  
**Branch**: Erag-roomsApp  
**Status**: ✅ Production Ready

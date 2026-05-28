# Booking to Report Sync System - User Guide

## Overview
This system automatically syncs booking data to generate dynamic reports. When you add a booking in the Django Admin panel, the report data is automatically calculated and displayed.

## How It Works

### 1. **Adding a Booking (Admin Panel)**

To create a new booking, follow these steps:

#### Step 1: Create a Reservation
1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Click on **Reservations** → **Add Reservation**
3. Fill in the required fields:
   - **Customer**: Select or create a customer account
   - **Room**: Choose an available room
   - **Check-in Date**: Select the check-in date
   - **Check-out Date**: Select the check-out date
   - **Number of Guests**: Enter number of guests
   - **Reservation Status**: Set to "Confirmed" or "Pending"
   - **Special Request**: Add any special notes (optional)
4. Click **Save**

#### Step 2: Create a Booking for the Reservation
1. Click on **Bookings** → **Add Booking**
2. Fill in the fields:
   - **Reservation**: Select the reservation you just created
   - **Total Amount**: Enter the booking amount (e.g., $150.00)
   - **Booking Status**: Set to "Confirmed" or "Completed"
3. Click **Save**

**Important**: When you save the booking, the system automatically:
- Creates a Report for that booking date (if it doesn't exist)
- Calculates total bookings for that date
- Calculates total revenue for that date
- Calculates occupancy rate for that date

### 2. **Viewing Reports (Admin Panel)**

To view the generated reports:

1. Go to Django Admin: `http://127.0.0.1:8000/admin/`
2. Click on **Reports** → **Booking Reports**
3. You'll see a list of all reports organized by date

Each report shows:
- **Report Date**: The date of the report
- **Total Bookings** (color-coded):
  - 🟢 Green: 5+ bookings (good occupancy)
  - 🟠 Orange: 1-4 bookings (low occupancy)
  - 🔴 Red: 0 bookings (no occupancy)
- **Total Revenue**: Sum of all booking amounts for that date
- **Occupancy Rate**: Percentage of rooms occupied

### 3. **Creating a Report for a Specific Date**

To create a report for a specific date:

1. Go to Django Admin → **Reports** → **Booking Reports**
2. Click **Add Report**
3. Select the **Report Date** (the date you want to analyze)
4. Click **Save**
5. The system automatically calculates:
   - Total bookings for that date
   - Total revenue from all bookings on that date
   - Occupancy rate (percentage of rooms occupied on that date)

All data is generated dynamically from the database—no manual entry needed!

## Data Calculations

### Total Bookings
- Counts all confirmed or completed bookings with `booking_date` matching the report date

### Total Revenue
- Sums the `total_amount` from all confirmed or completed bookings for the report date

### Occupancy Rate
- Calculates the percentage of rooms occupied on the report date
- A room is considered occupied if:
  - It has an active reservation
  - The reservation's check-in date ≤ report date < check-out date
  - The reservation status is "Confirmed", "Checked In", or "Checked Out"
- Formula: (Occupied Rooms / Total Rooms) × 100

## Example Workflow

### Scenario: Creating a Booking for May 28, 2026

1. **Create a Customer** (if needed):
   - Go to Accounts → Add Customer
   - Fill in details and save

2. **Create a Reservation**:
   - Go to Reservations → Add Reservation
   - Customer: John Doe
   - Room: Room 101
   - Check-in: May 28, 2026
   - Check-out: May 30, 2026
   - Number of Guests: 2
   - Status: Confirmed
   - Click Save

3. **Create a Booking**:
   - Go to Bookings → Add Booking
   - Reservation: Select the one created above
   - Total Amount: $300.00
   - Status: Confirmed
   - Click Save

4. **View the Report**:
   - Go to Reports → Booking Reports
   - Click on May 28, 2026 report (or create one)
   - The report will show:
     - **Total Bookings**: 1
     - **Total Revenue**: $300.00
     - **Occupancy Rate**: ~14.29% (1 room out of 7 rooms, for example)

## Key Features

✅ **Automatic Sync**: Booking changes immediately update reports  
✅ **Dynamic Calculations**: All numbers are calculated from actual database records  
✅ **Color-Coded Display**: Visual indicators for quick status assessment  
✅ **No Manual Entry**: Report metrics are read-only and auto-calculated  
✅ **Real-time Updates**: Adding, updating, or deleting bookings updates reports instantly  

## Troubleshooting

### Report Shows 0 Bookings
- Check if bookings have `booking_date` matching the report date
- Verify booking status is "Confirmed" or "Completed"

### Occupancy Rate Shows 0%
- Check if reservations have check-in ≤ report date < check-out
- Verify reservation status is in ["Confirmed", "Checked In", "Checked Out"]

### Revenue Shows $0.00
- Check if any bookings exist for that date
- Verify `total_amount` is set correctly on bookings

## Admin URLs

- Django Admin Home: `http://127.0.0.1:8000/admin/`
- Reservations: `http://127.0.0.1:8000/admin/reservations/reservation/`
- Bookings: `http://127.0.0.1:8000/admin/reservations/booking/`
- Reports: `http://127.0.0.1:8000/admin/reports/report/`

---

For more help, check the Django admin panel tooltips and field descriptions!

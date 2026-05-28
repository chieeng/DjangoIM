# Hotel Booking System - Automatic Price Calculation Guide

## Overview
The system now automatically calculates booking amounts based on room prices and reservation dates. No manual price entry needed!

## Complete Workflow

### Step 1: Create a Room Type (Admin Setup)
1. Go to **Rooms** → **Room Types** → **Add Room Type**
2. Enter room type name (e.g., "Deluxe Suite")
3. Set **Price per night** (e.g., $150.00)
4. Save

### Step 2: Create a Room
1. Go to **Rooms** → **Rooms** → **Add Room**
2. Fill in:
   - **Room Number**: e.g., "101"
   - **Floor Number**: e.g., "1"
   - **Room Type**: Select the type created above
   - **Status**: "Available"
   - **Price per night**: $150.00 (auto-fills from room type or override)
3. Save

### Step 3: Create a Reservation (Auto Price Display)
1. Go to **Reservations** → **Add Reservation**
2. Fill in:
   - **Customer**: Select a customer
   - **Room**: Select a room ⭐ **Room price is now displayed!**
   - **Check-in Date**: e.g., May 28, 2026
   - **Check-out Date**: e.g., May 30, 2026
   - **Number of Guests**: 2
   - **Reservation Status**: "Confirmed"
3. **Room Details section shows:**
   - Room number
   - Room type
   - Price per night (from the room)
   - Floor number

4. **Calculated Total Amount section shows:**
   - Number of nights: 2
   - Rate per night: $150.00
   - **TOTAL: $300.00** ← Used for booking

5. Save reservation

### Step 4: Create a Booking (Auto Total Amount)
1. Go to **Bookings** → **Add Booking**
2. Fill in:
   - **Reservation**: Select the reservation created above
   - **Booking Status**: "Confirmed" or "Pending"
   - **Total Amount**: ⭐ **READ-ONLY - Auto-calculated!**

3. The system automatically displays:
   - **Cost Breakdown** section showing:
     - Room: 101
     - Nightly Rate: $150.00
     - Number of Nights: 2
     - **TOTAL: $300.00** ← Auto-filled!

4. Save booking

⚠️ **Important:** When you save the booking, it automatically:
- ✅ Calculates total_amount (no need to enter manually)
- ✅ Triggers the signal to update the Report
- ✅ Report for that date gets generated with all metrics

### Step 5: View the Report
1. Go to **Reports** → **Booking Reports**
2. Click on the report for May 28, 2026
3. See the auto-populated data:
   - **Total Bookings**: 1
   - **Total Revenue**: $300.00
   - **Occupancy Rate**: Calculated based on occupied rooms

---

## Key Features

✅ **Automatic Room Price Fetching**
- Select a room → Price automatically displayed
- Room price data comes from the Rooms table

✅ **Automatic Total Amount Calculation**
- Reservation shows: (Check-out - Check-in) × Room Price
- Booking inherits this calculated amount
- No manual price entry needed

✅ **Read-only Total Amount in Bookings**
- Prevents accidental manual entry
- Always matches reservation calculation

✅ **Real-time Report Updates**
- When booking is created/updated → Report updates automatically
- Reports use actual booking data, not user input

✅ **Cost Breakdown Display**
- Beautiful formatted breakdown in booking form
- Shows calculation: Nights × Rate = Total

---

## Example Calculation

**Room**: Room 101  
**Room Type**: Deluxe Suite  
**Price**: $150.00/night  

**Reservation**:
- Check-in: May 28, 2026
- Check-out: May 30, 2026  
- Number of nights: 2 days
- **Calculated total: 2 × $150 = $300.00**

**Booking**:
- When you select this reservation
- Total Amount auto-fills: **$300.00** ✅

**Report** (May 28, 2026):
- Total Bookings: 1
- Total Revenue: $300.00
- Occupancy Rate: ~14.29% (1 room occupied out of 7)

---

## Troubleshooting

### Total Amount shows $0
- Check if room has a price per night set
- Verify check-out date is after check-in date
- Save the reservation first, then create booking

### Room price not showing
- Make sure room is assigned to a room type
- Room Type must have a price set
- Or room itself must have price_per_night set

### Report not updating
- Create the booking with status "Confirmed" or "Completed"
- Check if report exists for that date
- If not, create a placeholder report first, then create booking

---

## Tips

💡 **Best Practice**: Always ensure:
1. Room Types have prices
2. Rooms are assigned to Room Types
3. Reservations have check-in and check-out dates
4. Bookings are created AFTER reservations

This ensures all automatic calculations work smoothly!

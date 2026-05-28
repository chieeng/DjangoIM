from datetime import date, time

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.db.models import Exists, OuterRef
from django.db import transaction

from accounts.models import Customer, User

from .forms import ReservationDetailsForm
from decimal import Decimal

from .models import Booking, Discount, Invoice, Payment, Reservation, Room


def landing(request):
    # Template lives at booking/templates/booking/landing.html
    return render(request, 'booking/landing.html')


def reservation_details(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("accounts:login")

    reservation_id = request.GET.get("reservation_id")
    if reservation_id:
        reservation = get_object_or_404(
            Reservation.objects.select_related("room", "room__room_type", "booking", "booking__customer"),
            reservation_id=reservation_id,
        )
        # Basic ownership check: reservation must belong to current logged-in user.
        user = get_object_or_404(User, user_id=user_id)
        customer = get_object_or_404(Customer, user=user)
        if reservation.booking.customer_id != customer.customer_id:
            messages.error(request, "You do not have access to that reservation.")
            return redirect("accounts:customer_dashboard")

        invoice = Invoice.objects.filter(booking=reservation.booking).order_by("-issue_date").first()
        discount = Discount.objects.filter(booking=reservation.booking).order_by("-discount_id").first()

        # Recompute original/discount/final for display (Invoice stores final total_amount).
        nights = max(1, (reservation.check_out_date - reservation.check_in_date).days)
        original_amount = reservation.room.price_per_night * nights
        discount_pct = (discount.percentage if discount else Decimal("0")) / Decimal("100")
        discount_amount = (original_amount * discount_pct) if discount else Decimal("0")
        final_total = original_amount - discount_amount

        return render(
            request,
            "booking/reservation_details.html",
            {
                "room": reservation.room,
                "check_in_date": reservation.check_in_date,
                "check_out_date": reservation.check_out_date,
                "check_in_time": time(12, 0),
                "check_out_time": time(12, 0),
                "form": None,
                "reservation": reservation,
                "invoice": invoice,
                "discount": discount,
                "original_amount": original_amount,
                "discount_amount": discount_amount,
                "final_total": final_total,
            },
        )

    room_id = request.GET.get("room_id") if request.method == "GET" else request.POST.get("room_id")
    check_in_date_raw = request.GET.get("check_in_date") if request.method == "GET" else request.POST.get("check_in_date")
    check_out_date_raw = request.GET.get("check_out_date") if request.method == "GET" else request.POST.get("check_out_date")

    if not (room_id and check_in_date_raw and check_out_date_raw):
        messages.error(request, "Missing reservation details.")
        return redirect("accounts:customer_dashboard")

    try:
        check_in_date = date.fromisoformat(check_in_date_raw)
        check_out_date = date.fromisoformat(check_out_date_raw)
    except ValueError:
        messages.error(request, "Invalid date format.")
        return redirect("accounts:customer_dashboard")

    if check_out_date < check_in_date:
        messages.error(request, "Check-out date must be on or after check-in date.")
        return redirect("accounts:customer_dashboard")

    room = get_object_or_404(Room, room_id=room_id)

    # Defensive re-check: room must still be available for the range.
    overlap_qs = Reservation.objects.filter(
        room_id=OuterRef("room_id"),
        check_in_date__lte=check_out_date,
        check_out_date__gte=check_in_date,
    ).exclude(reservation_status__iexact="Cancelled")

    still_available = (
        Room.objects.filter(room_id=room.room_id, status__iexact="Available")
        .annotate(_has_overlap=Exists(overlap_qs))
        .filter(_has_overlap=False)
        .exists()
    )

    if not still_available:
        messages.error(request, "Sorry, that room is no longer available for that date range.")
        return redirect("accounts:customer_dashboard")

    form = ReservationDetailsForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = get_object_or_404(User, user_id=user_id)
        customer = get_object_or_404(Customer, user=user)

        adults = form.cleaned_data["adults"]
        kids = form.cleaned_data["kids"]
        seniors = form.cleaned_data["seniors"]
        total = adults + kids + seniors

        booking = Booking.objects.create(
            customer=customer,
            booking_date=timezone.now(),
            booking_status="Pending",
            total_amount=0,
        )

        reservation = Reservation.objects.create(
            booking=booking,
            room=room,
            reservation_date=timezone.now(),
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=total,
            reservation_status="Pending",
        )

        # Store the fixed times (12:00 PM) via RoomAssignment for later use if needed.
        try:
            from .models import RoomAssignment

            RoomAssignment.objects.create(
                booking=booking,
                room=room,
                assigned_date=timezone.now(),
                check_in_time=time(12, 0),
                check_out_time=time(12, 0),
            )
        except Exception:
            # Keep reservation creation successful even if RoomAssignment isn't desired/available.
            pass

        # Senior discount is not applied here; we just persist seniors count for later invoice/payment logic.
        # Create a draft invoice for display.
        nights = max(1, (check_out_date - check_in_date).days)
        original_amount = room.price_per_night * nights

        discount = None
        discount_amount = Decimal("0")
        if seniors and int(seniors) > 0:
            discount = Discount.objects.create(
                booking=booking,
                discount_name="Senior Discount",
                percentage=Decimal("20.00"),
                start_date=check_in_date,
                end_date=check_out_date,
                description="20% discount applied when at least one senior guest is included.",
            )
            discount_amount = (original_amount * Decimal("0.20"))

        final_total = original_amount - discount_amount
        booking.total_amount = final_total
        booking.save(update_fields=["total_amount"])

        issue_dt = timezone.now()
        Invoice.objects.create(
            booking=booking,
            issue_date=issue_dt,
            due_date=check_in_date,
            total_amount=final_total,
            invoice_status="Unpaid",
        )

        messages.success(request, "Reservation created (Pending).")
        return redirect(f"{request.path}?reservation_id={reservation.reservation_id}")

    return render(
        request,
        "booking/reservation_details.html",
        {
            "room": room,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "check_in_time": time(12, 0),
            "check_out_time": time(12, 0),
            "form": form,
        },
    )


def create_booking(request):
    # Backwards-compatible endpoint: keep it as a redirect target.
    return redirect("accounts:customer_dashboard")


def booking_list(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, user_id=user_id)
    customer = get_object_or_404(Customer, user=user)

    reservations = (
        Reservation.objects.select_related("room", "booking", "room__room_type")
        .filter(booking__customer=customer)
        .order_by("-reservation_date")
    )

    return render(request, "booking/booking_list.html", {"reservations": reservations})


def payment_page(request, booking_id: int):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("accounts:login")

    user = get_object_or_404(User, user_id=user_id)
    customer = get_object_or_404(Customer, user=user)

    booking = get_object_or_404(Booking, booking_id=booking_id, customer=customer)
    invoice = Invoice.objects.filter(booking=booking).order_by("-issue_date").first()
    discount = Discount.objects.filter(booking=booking).order_by("-discount_id").first()

    if request.method == "POST":
        if invoice is None:
            messages.error(request, "No invoice found for this booking.")
            return redirect("booking:payment_page", booking_id=booking.booking_id)

        with transaction.atomic():
            # Create or update a Payment row.
            payment, _created = Payment.objects.get_or_create(
                booking=booking,
                defaults={
                    "payment_date": timezone.now(),
                    "amount_paid": invoice.total_amount,
                    "payment_method": "Cash",
                    "payment_status": "Paid",
                },
            )
            if payment.payment_status != "Paid":
                payment.payment_status = "Paid"
                payment.amount_paid = invoice.total_amount
                payment.payment_date = timezone.now()
                payment.save(update_fields=["payment_status", "amount_paid", "payment_date"])

            # Update invoice/booking/reservation/room statuses.
            if invoice.invoice_status != "Paid":
                invoice.invoice_status = "Paid"
                invoice.save(update_fields=["invoice_status"])

            if booking.booking_status != "Confirmed":
                booking.booking_status = "Confirmed"
                booking.save(update_fields=["booking_status"])

            Reservation.objects.filter(booking=booking).exclude(reservation_status__iexact="Cancelled").update(
                reservation_status="Confirmed"
            )

            # Mark rooms as occupied for any reservation under this booking.
            room_ids = Reservation.objects.filter(booking=booking).values_list("room_id", flat=True)
            Room.objects.filter(room_id__in=room_ids).update(status="Occupied")

        messages.success(request, "Payment recorded. Booking confirmed.")
        return redirect("booking:payment_page", booking_id=booking.booking_id)

    return render(
        request,
        "booking/payment.html",
        {
            "booking": booking,
            "invoice": invoice,
            "discount": discount,
        },
    )

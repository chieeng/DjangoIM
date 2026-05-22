from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import BookingForm
from .models import Booking
from rooms.models import Room, RoomType


class BookingDashboardTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.customer = User.objects.create_user(
            username='customer@example.com',
            email='customer@example.com',
            password='Testpass123!',
            first_name='Test',
            last_name='Customer',
        )
        self.admin = User.objects.create_user(
            username='admin@example.com',
            email='admin@example.com',
            password='Adminpass123!',
            is_staff=True,
            role_type='admin',
        )
        self.room_type = RoomType.objects.create(
            type_name='Deluxe',
            description='A deluxe test room',
            capacity=2,
            price_per_night=120,
        )
        self.room = Room.objects.create(
            room_number='301',
            floor_number=3,
            room_type=self.room_type,
            status='available',
            price_per_night=120,
        )
        self.booking = Booking.objects.create(
            customer=self.customer,
            customer_name='Test Customer',
            room_number='101',
            check_in_date=timezone.localdate() + timedelta(days=3),
            check_out_date=timezone.localdate() + timedelta(days=5),
        )

    def test_customer_dashboard_shows_own_pending_booking(self):
        self.client.login(username='customer@example.com', password='Testpass123!')

        response = self.client.get(reverse('booking:dashboard'))

        self.assertContains(response, 'Bookings Dashboard')
        self.assertContains(response, 'Room 101')
        self.assertContains(response, 'Pending')

    def test_staff_can_approve_pending_booking(self):
        self.client.login(username='admin@example.com', password='Adminpass123!')

        response = self.client.post(reverse('booking:approve_booking', args=[self.booking.id]))
        self.booking.refresh_from_db()

        self.assertRedirects(response, reverse('booking:admin_dashboard'))
        self.assertEqual(self.booking.booking_status, 'confirmed')

    def test_customer_cannot_open_admin_dashboard(self):
        self.client.login(username='customer@example.com', password='Testpass123!')

        response = self.client.get(reverse('booking:admin_dashboard'))

        self.assertEqual(response.status_code, 302)

    def test_duplicate_room_and_dates_are_rejected_as_overlap(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_in_date,
            'check_out_date': self.booking.check_out_date,
        })

        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)
        self.assertIn('overlaps', form.errors['room_number'][0])

    def test_overlapping_room_date_range_is_rejected(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': timezone.localdate() + timedelta(days=4),
            'check_out_date': timezone.localdate() + timedelta(days=6),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)
        self.assertIn('overlaps', form.errors['room_number'][0])

    def test_new_check_in_inside_existing_booking_is_rejected(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_in_date + timedelta(days=1),
            'check_out_date': self.booking.check_out_date + timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)
        self.assertIn('overlaps', form.errors['room_number'][0])

    def test_new_check_out_inside_existing_booking_is_rejected(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_in_date - timedelta(days=1),
            'check_out_date': self.booking.check_out_date - timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)
        self.assertIn('overlaps', form.errors['room_number'][0])

    def test_new_booking_that_contains_existing_booking_is_rejected(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_in_date - timedelta(days=1),
            'check_out_date': self.booking.check_out_date + timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('room_number', form.errors)
        self.assertIn('overlaps', form.errors['room_number'][0])

    def test_same_checkout_and_next_check_in_is_allowed(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_out_date,
            'check_out_date': self.booking.check_out_date + timedelta(days=2),
        })

        self.assertTrue(form.is_valid())

    def test_new_checkout_touching_existing_check_in_is_allowed(self):
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_in_date - timedelta(days=2),
            'check_out_date': self.booking.check_in_date,
        })

        self.assertTrue(form.is_valid())

    def test_cancelled_booking_does_not_block_same_room_and_dates(self):
        self.booking.booking_status = 'cancelled'
        self.booking.save(update_fields=['booking_status'])
        form = BookingForm(data={
            'room_number': '101',
            'check_in_date': self.booking.check_in_date,
            'check_out_date': self.booking.check_out_date,
        })

        self.assertTrue(form.is_valid())

    def test_check_in_after_check_out_is_rejected(self):
        form = BookingForm(data={
            'room_number': '102',
            'check_in_date': timezone.localdate() + timedelta(days=5),
            'check_out_date': timezone.localdate() + timedelta(days=4),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Check-out date must be after check-in date.', form.errors['check_out_date'])

    def test_check_in_in_the_past_is_rejected(self):
        form = BookingForm(data={
            'room_number': '102',
            'check_in_date': timezone.localdate() - timedelta(days=1),
            'check_out_date': timezone.localdate() + timedelta(days=1),
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Check-in date cannot be in the past.', form.errors['check_in_date'])

    def test_required_booking_fields_are_rejected_when_empty(self):
        form = BookingForm(data={
            'room_number': '',
            'check_in_date': '',
            'check_out_date': '',
        })

        self.assertFalse(form.is_valid())
        self.assertIn('Room number is required.', form.errors['room_number'])
        self.assertIn('Check-in date is required.', form.errors['check_in_date'])
        self.assertIn('Check-out date is required.', form.errors['check_out_date'])

    def test_booking_status_defaults_to_pending(self):
        form = BookingForm(data={
            'room_number': '204',
            'check_in_date': timezone.localdate() + timedelta(days=8),
            'check_out_date': timezone.localdate() + timedelta(days=10),
        })

        self.assertTrue(form.is_valid())
        booking = form.save(commit=False)

        self.assertEqual(booking.booking_status, 'pending')

    def test_selected_room_booking_page_auto_fills_room_name(self):
        self.client.login(username='customer@example.com', password='Testpass123!')

        response = self.client.get(reverse('booking:book_room', args=[self.room.pk]))

        self.assertContains(response, 'Deluxe is selected')
        self.assertContains(response, 'value="Deluxe"')

    def test_selected_room_post_saves_selected_room_number(self):
        self.client.login(username='customer@example.com', password='Testpass123!')

        response = self.client.post(reverse('booking:book_room', args=[self.room.pk]), {
            'check_in_date': timezone.localdate() + timedelta(days=8),
            'check_out_date': timezone.localdate() + timedelta(days=10),
        })

        self.assertRedirects(response, reverse('booking:index'))
        self.assertTrue(Booking.objects.filter(
            customer=self.customer,
            room=self.room,
            room_name='Deluxe',
            room_number='301',
            booking_status='pending',
        ).exists())

    def test_room_listing_book_now_opens_room_detail_before_booking_form(self):
        self.client.login(username='customer@example.com', password='Testpass123!')

        listing_response = self.client.get(reverse('rooms:room_list'))
        detail_url = reverse('rooms:room_detail', args=[self.room.pk])
        booking_url = reverse('booking:book_room', args=[self.room.pk])

        self.assertContains(listing_response, f'href="{detail_url}" class="btn-book">Book Now</a>')

        detail_response = self.client.get(detail_url)

        self.assertContains(detail_response, 'Room 301')
        self.assertContains(detail_response, f'href="{booking_url}"')

    def test_landing_book_now_does_not_link_to_booking_dashboard(self):
        self.client.login(username='customer@example.com', password='Testpass123!')

        response = self.client.get(reverse('index'))

        self.assertContains(response, f'href="{reverse("booking:book_room", args=[self.room.pk])}" class="book-btn">Book Now</a>')
        self.assertNotContains(response, f'href="{reverse("booking:index")}" class="book-btn">Book Now</a>')

    def test_login_next_redirect_can_return_to_room_detail(self):
        detail_url = reverse('rooms:room_detail', args=[self.room.pk])

        response = self.client.post(f'{reverse("accounts:login")}?next={detail_url}', {
            'username': 'customer@example.com',
            'password': 'Testpass123!',
            'next': detail_url,
        })

        self.assertRedirects(response, detail_url)

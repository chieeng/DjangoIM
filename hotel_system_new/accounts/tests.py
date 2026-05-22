from django.test import TestCase
from django.urls import reverse

from .models import CustomUser, CustomerProfile
from booking.models import Booking


class AccountFlowTests(TestCase):
    def test_register_creates_user_and_profile_and_redirects_to_login(self):
        response = self.client.post(
            reverse('accounts:register'),
            {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane@example.com',
                'phone': '+12345678901',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('accounts:login'))
        user = CustomUser.objects.get(email='jane@example.com')
        self.assertEqual(user.username, 'jane@example.com')
        profile = CustomerProfile.objects.get(user=user)
        self.assertEqual(profile.id_number, CustomerProfile.generate_pending_id_number(user.user_id))

    def test_register_shows_duplicate_email_error(self):
        CustomUser.objects.create_user(
            username='jane@example.com',
            email='jane@example.com',
            password='StrongPass123!',
        )

        response = self.client.post(
            reverse('accounts:register'),
            {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane@example.com',
                'phone': '+12345678901',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'An account with this email already exists.')

    def test_login_accepts_email_credential(self):
        CustomUser.objects.create_user(
            username='jane@example.com',
            email='jane@example.com',
            password='StrongPass123!',
            first_name='Jane',
        )

        response = self.client.post(
            reverse('accounts:login'),
            {
                'username': 'jane@example.com',
                'password': 'StrongPass123!',
            },
        )

        self.assertRedirects(response, reverse('index'))
        self.assertIn('_auth_user_id', self.client.session)

    def test_booking_pages_require_login(self):
        response = self.client.get(reverse('booking:index'))
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('booking:index')}")

    def test_booking_index_shows_only_logged_in_user_bookings(self):
        user = CustomUser.objects.create_user(
            username='jane@example.com',
            email='jane@example.com',
            password='StrongPass123!',
            first_name='Jane',
        )
        other_user = CustomUser.objects.create_user(
            username='john@example.com',
            email='john@example.com',
            password='StrongPass123!',
            first_name='John',
        )
        Booking.objects.create(
            customer=user,
            customer_name='Jane',
            room_number='101',
            check_in_date='2026-05-10',
            check_out_date='2026-05-12',
        )
        Booking.objects.create(
            customer=other_user,
            customer_name='John',
            room_number='202',
            check_in_date='2026-05-11',
            check_out_date='2026-05-13',
        )

        self.client.force_login(user)
        response = self.client.get(reverse('booking:index'))

        self.assertContains(response, 'Room 101')
        self.assertNotContains(response, 'Room 202')

    def test_register_creates_unique_pending_id_numbers(self):
        first_response = self.client.post(
            reverse('accounts:register'),
            {
                'first_name': 'Jane',
                'last_name': 'Doe',
                'email': 'jane1@example.com',
                'phone': '+12345678901',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )
        second_response = self.client.post(
            reverse('accounts:register'),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john1@example.com',
                'phone': '+12345678902',
                'password1': 'StrongPass123!',
                'password2': 'StrongPass123!',
            },
        )

        self.assertRedirects(first_response, reverse('accounts:login'))
        self.assertRedirects(second_response, reverse('accounts:login'))
        id_numbers = list(
            CustomerProfile.objects.order_by('user__email').values_list('id_number', flat=True)
        )
        self.assertEqual(len(id_numbers), 2)
        self.assertEqual(len(set(id_numbers)), 2)

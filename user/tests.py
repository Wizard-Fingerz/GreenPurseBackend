from django.test import TestCase
from .models import *

# Create your tests here.

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')

    def test_user_creation(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'test@example.com')

    def test_profile_creation(self):
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(self.user.profile.bio, '')

    def test_address_creation(self):
        address = Address.objects.create(
            user=self.user,
            address_type=Address.BILLING,
            default=True,
            country='Country',
            city='City',
            street_address='Street Address',
            apartment_address='Apartment Address',
            postal_code='12345'
        )
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.user, self.user)
        self.assertEqual(address.address_type, Address.BILLING)
        self.assertTrue(address.default)

class SignalTestCase(TestCase):
    def test_profile_created_signal(self):
        user = User.objects.create(email='signaltest@example.com')
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(user.profile.bio, '')

    def test_address_created_signal(self):
        user = User.objects.create(email='signaltest@example.com')
        address = Address.objects.create(
            user=user,
            address_type=Address.BILLING,
            default=True,
            country='Country',
            city='City',
            street_address='Street Address',
            apartment_address='Apartment Address',
            postal_code='12345'
        )
        self.assertEqual(Address.objects.count(), 1)
        self.assertEqual(address.user, user)
        self.assertEqual(address.address_type, Address.BILLING)
        self.assertTrue(address.default)


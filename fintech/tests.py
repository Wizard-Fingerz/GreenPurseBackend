from django.test import TestCase
from user.models import User
from .models import Transaction

class TransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.transaction = Transaction.objects.create(
            reference='REF123',
            account='Account123',
            date='2023-08-15',
            amount='100.00',
            type=Transaction.TransactionType.inflow,
            category='Category1',
            user=self.user
        )

    def test_transaction_creation(self):
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(self.transaction.reference, 'REF123')
        self.assertEqual(self.transaction.account, 'Account123')
        self.assertEqual(str(self.transaction.date), '2023-08-15')
        self.assertEqual(self.transaction.amount, '100.00')
        self.assertEqual(self.transaction.type, Transaction.TransactionType.inflow)
        self.assertEqual(self.transaction.category, 'Category1')
        self.assertEqual(self.transaction.user, self.user)

    def test_transaction_type_choices(self):
        choices = [choice[0] for choice in Transaction.TransactionType.choices]
        self.assertIn('inflow', choices)
        self.assertIn('outflow', choices)

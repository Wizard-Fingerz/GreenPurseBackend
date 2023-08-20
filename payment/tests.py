from django.test import TestCase
from user.models import *
from commerce.models import *
from .models import *

class PaymentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.order = Order.objects.create(buyer=self.user)
        self.payment = Payment.objects.create(
            status=Payment.COMPLETED,
            payment_option=Payment.PAYPAL,
            order=self.order
        )

    def test_payment_creation(self):
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(self.payment.status, Payment.COMPLETED)
        self.assertEqual(self.payment.payment_option, Payment.PAYPAL)
        self.assertEqual(self.payment.order, self.order)

class WalletModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.wallet = Wallet.objects.create(
            user=self.user,
            balance='100.00',
            account_name='Test Account',
            account_number='1234567890',
            bank='Test Bank',
            phone_number='1234567890',
            password='test_password'
        )

    def test_wallet_creation(self):
        self.assertEqual(Wallet.objects.count(), 1)
        self.assertEqual(self.wallet.user, self.user)
        # self.assertEqual(str(self.wallet), str(self.user))
        self.assertEqual(str(self.wallet), self.wallet.account_number)

class WalletTransactionModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='test@example.com')
        self.wallet = Wallet.objects.create(
            user=self.user,
            balance='100.00',
            account_name='Test Account',
            account_number='1234567890',
            bank='Test Bank',
            phone_number='1234567890',
            password='test_password'
        )
        self.wallet_transaction = WalletTransaction.objects.create(
            transaction_id='TX123',
            status=WalletTransaction.STATUS.PENDING,
            transaction_type=WalletTransaction.TransactionType.BANK_TRANSFER_FUNDING,
            wallet=self.wallet,
            amount='50.00',
            date='2023-08-15'
        )

    def test_wallet_transaction_creation(self):
        self.assertEqual(WalletTransaction.objects.count(), 1)
        self.assertEqual(self.wallet_transaction.transaction_id, 'TX123')
        self.assertEqual(self.wallet_transaction.status, WalletTransaction.STATUS.PENDING)
        self.assertEqual(self.wallet_transaction.transaction_type, WalletTransaction.TransactionType.BANK_TRANSFER_FUNDING)
        self.assertEqual(self.wallet_transaction.wallet, self.wallet)
        self.assertEqual(self.wallet_transaction.amount, '50.00')
        self.assertEqual(self.wallet_transaction.date, '2023-08-15')


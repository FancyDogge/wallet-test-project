from django.contrib.auth.models import User
from wallet.models import Wallet
from transactions.models import Transaction
from django.test import TestCase, Client
import decimal


class TestTransactions(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="TestUser1")
        self.user1.set_password("123456789")
        self.user1.save()

        self.user2 = User.objects.create(username="TestUser2")
        self.user2.set_password("123456789")
        self.user2.save()

        # Wallet RUB for TestUser1
        self.wallet1 = Wallet.objects.create(
            type=Wallet.CardType.VISA,
            currency=Wallet.Currency.RUB,
            balance=100,
            owner=self.user1,
        )

        # Wallet RUB for TestUser2
        self.wallet2 = Wallet.objects.create(
            type=Wallet.CardType.VISA,
            currency=Wallet.Currency.RUB,
            balance=100,
            owner=self.user2,
        )

        # Wallet USD for TestUser2
        self.wallet3 = Wallet.objects.create(
            type=Wallet.CardType.VISA,
            currency=Wallet.Currency.USD,
            balance=20,
            owner=self.user2,
        )

        # Client
        self.client = Client()
        self.user_login = self.client.login(username="TestUser1", password="123456789")

    def test_GET_transactions_while_logged(self):
        response = self.client.get("/transactions/")
        self.assertEquals(response.status_code, 200)

    def test_GET_transactions_not_logged(self):
        self.client.logout()
        response = self.client.get("/transactions/")
        self.assertEquals(response.status_code, 401)

    def test_POST_transactions_to_same_wallet(self):
        response = self.client.post(
            "/transactions/",
            data={
                "sender": self.wallet1.name,
                "receiver": self.wallet1.name,
                "transfer_amount": "25.00",
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Transaction.objects.all().count(), 1)
        self.assertEquals(Transaction.objects.get(id=1).status, "FAILED")

    def test_POST_transactions_to_wallet_with_same_currency(self):
        response = self.client.post(
            "/transactions/",
            data={
                "sender": self.wallet1.name,
                "receiver": self.wallet2.name,
                "transfer_amount": 10,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Transaction.objects.all().count(), 1)
        self.assertEquals(Transaction.objects.get(id=1).status, "PAID")
        self.assertEquals(
            Transaction.objects.get(id=1).commision, decimal.Decimal("1.00")
        )

    def test_POST_transactions_to_wallet_with_different_currency(self):
        response = self.client.post(
            "/transactions/",
            data={
                "sender": self.wallet1.name,
                "receiver": self.wallet3.name,
                "transfer_amount": 10,
            },
        )
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Transaction.objects.all().count(), 0)

    def test_POST_transactions_sender_is_not_current_user(self):

        response = self.client.post(
            "/transactions/",
            data={
                "sender": self.wallet2.name,
                "receiver": self.wallet1.name,
                "transfer_amount": 10,
            },
        )
        self.assertEquals(response.data["error"], "wrong sender wallet!")
        self.assertEquals(response.status_code, 400)
        self.assertEquals(Transaction.objects.all().count(), 0)

    def test_POST_transactions_not_enough_wallet_funds(self):

        response = self.client.post(
            "/transactions/",
            data={
                "sender": self.wallet1.name,
                "receiver": self.wallet2.name,
                "transfer_amount": 123,
            },
        )
        self.assertEquals(response.status_code, 201)
        self.assertEquals(Transaction.objects.all().count(), 1)
        self.assertEquals(Transaction.objects.get(id=1).status, "FAILED")

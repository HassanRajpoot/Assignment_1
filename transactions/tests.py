from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from stocks.models import StockData
from users.models import User
from .models import Transaction
from django.utils import timezone
from datetime import timedelta

class TransactionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", balance="1000.00")
        self.stock = StockData.objects.create(
            ticker="AAPL",
            open_price="150.00",
            close_price="155.00",
            high="156.00",
            low="149.00",
            volume=1000,
            timestamp="2023-11-01T10:00:00Z"
        )

    def test_create_transaction(self):
        url = reverse('transaction_create')
        data = {
            "user": self.user.user_id,
            "ticker": "AAPL",
            "transaction_type": "buy",
            "transaction_volume": 5
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.get()
        self.assertEqual(transaction.user.user_id, self.user.user_id)
        self.assertEqual(transaction.ticker, "AAPL")
        self.assertEqual(transaction.transaction_type, "buy")
        self.assertEqual(transaction.transaction_volume, 5)

    def test_get_user_transactions(self):
        transaction = Transaction.objects.create(
            user=self.user,
            ticker="AAPL",
            transaction_type="buy",
            transaction_volume=5,
            transaction_price=155.00 * 5
        )
        url = reverse('user_transactions', args=[self.user.user_id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ticker'], "AAPL")
    def test_get_user_transactions_by_date(self):
        transaction = Transaction.objects.create(
            user=self.user,
            ticker="AAPL",
            transaction_type="buy",
            transaction_volume=5,
            transaction_price=155.00 * 5,
            )
        start_timestamp = transaction.timestamp
        end_timestamp = start_timestamp + timedelta(hours=3)
        url = reverse('user_transactions_by_date', args=[self.user.user_id, start_timestamp, end_timestamp])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['ticker'], "AAPL")


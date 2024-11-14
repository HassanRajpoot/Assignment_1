from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import StockData

class StockDataTests(APITestCase):
    def test_create_stock(self):
        url = reverse('stock_ingest')
        data = {
            "ticker": "AAPL",
            "open_price": "150.00",
            "close_price": "155.00",
            "high": "156.00",
            "low": "149.00",
            "volume": 1000,
            "timestamp": "2023-11-01T10:00:00Z"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(StockData.objects.count(), 1)

    def test_get_stock(self):
        stock = StockData.objects.create(
            ticker="AAPL",
            open_price="150.00",
            close_price="155.00",
            high="156.00",
            low="149.00",
            volume=1000,
            timestamp="2023-11-01T10:00:00Z"
        )
        url = reverse('stock_detail', args=[stock.ticker])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["ticker"], "AAPL")

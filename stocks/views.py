from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import StockData
from .serializers import StockDataSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter

class StockIngestView(APIView):
    @extend_schema(
        request=StockDataSerializer,
        responses={201: StockDataSerializer, 400: "Bad Request"},
        description="Ingest new stock data.",
        summary="Stock Data Ingestion",
    )
    def post(self, request):
        serializer = StockDataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StockListView(APIView):
    @extend_schema(
        responses={200: StockDataSerializer(many=True)},
        description="Retrieve all stock data with caching.",
        summary="List All Stocks",
    )
    def get(self, request):
        cached_stocks = cache.get("all_stocks")
        if cached_stocks:
            return Response(cached_stocks, status=status.HTTP_200_OK)

        stocks = StockData.objects.all()
        serializer = StockDataSerializer(stocks, many=True)
        cache.set("all_stocks", serializer.data, timeout=300)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StockDetailView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter("ticker", description="Ticker symbol of the stock", required=True, type=str, location="path")
        ],
        responses={200: StockDataSerializer, 404: {"error": "Stock data not found"}},
        description="Retrieve the latest data for a specific stock by ticker with caching.",
        summary="Retrieve Stock by Ticker",
    )
    def get(self, request, ticker):
        cached_stock = cache.get(f"stock_{ticker}")
        if cached_stock:
            return Response(cached_stock, status=status.HTTP_200_OK)

        try:
            stock = StockData.objects.filter(ticker=ticker).latest("timestamp")
            serializer = StockDataSerializer(stock)
            cache.set(f"stock_{ticker}", serializer.data, timeout=300)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StockData.DoesNotExist:
            return Response({"error": "Stock data not found"}, status=status.HTTP_404_NOT_FOUND)
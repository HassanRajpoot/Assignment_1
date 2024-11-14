from django.urls import path
from .views import StockIngestView, StockListView, StockDetailView

urlpatterns = [
    path('', StockIngestView.as_view(), name='stock_ingest'),
    path('all/', StockListView.as_view(), name='stock_list'),
    path('<str:ticker>/', StockDetailView.as_view(), name='stock_detail'),
]


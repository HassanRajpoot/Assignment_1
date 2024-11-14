from django.urls import path
from .views import TransactionCreateView, UserTransactionsView, UserTransactionsByDateView

urlpatterns = [
    path('', TransactionCreateView.as_view(), name='transaction_create'),
    path('<int:user_id>/', UserTransactionsView.as_view(), name='user_transactions'),
    path('<int:user_id>/<str:start_timestamp>/<str:end_timestamp>/', UserTransactionsByDateView.as_view(), name='user_transactions_by_date'),
]

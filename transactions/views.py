from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from drf_spectacular.utils import extend_schema
from .models import Transaction
from .serializers import TransactionSerializer
from users.models import User
from stocks.models import StockData
from .tasks import process_transaction


class TransactionCreateView(APIView):
    """
    Handles the creation of a new transaction.
    """

    @extend_schema(
        request=TransactionSerializer,
        responses={202: {"message": "Transaction is being processed"}, 404: "User or Stock data not found"},
        description="Create a new transaction for a user.",
        summary="Create Transaction",
    )
    def post(self, request):
        user_id = request.data.get("user")
        ticker = request.data.get("ticker")
        transaction_type = request.data.get("transaction_type")
        transaction_volume = request.data.get("transaction_volume")

        try:
            user = User.objects.get(user_id=user_id)
            stock = StockData.objects.filter(ticker=ticker).latest("timestamp")

            transaction_price = stock.close_price * transaction_volume

            transaction = Transaction.objects.create(
                user=user,
                ticker=ticker,
                transaction_type=transaction_type,
                transaction_volume=transaction_volume,
                transaction_price=transaction_price,
            )
            process_transaction.delay(transaction.transaction_id)

            return Response(
                {"message": "Transaction is being processed"}, status=status.HTTP_202_ACCEPTED
            )

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except StockData.DoesNotExist:
            return Response({"error": "Stock data not found"}, status=status.HTTP_404_NOT_FOUND)


class UserTransactionsView(APIView):
    """
    Retrieves all transactions for a specified user.
    """

    @extend_schema(
        responses={200: TransactionSerializer(many=True), 404: "User not found"},
        description="Retrieve all transactions for a specified user.",
        summary="Retrieve User Transactions",
    )
    def get(self, user_id):
        """
        Retrieves all transactions for the given user.
        """
        try:
            transactions = Transaction.objects.filter(user_id=user_id)
            serializer = TransactionSerializer(transactions, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class UserTransactionsByDateView(APIView):
    """
    Retrieves transactions for a user within a specified date range.
    """

    @extend_schema(
        responses={200: TransactionSerializer(many=True), 404: "User not found", 400: "Invalid date format"},
        description="Retrieve user transactions within a specified date range.",
        summary="Retrieve User Transactions by Date",
    )
    def get(self, request, user_id, start_timestamp, end_timestamp):
        """
        Retrieves user transactions within a specified date range.
        """
        try:
            transactions = Transaction.objects.filter(
                user_id=user_id,
                timestamp__range=(start_timestamp, end_timestamp)
            )
            serializer = TransactionSerializer(transactions, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['transaction_id', 'user', 'ticker', 'transaction_type', 'transaction_volume', 'transaction_price', 'timestamp']

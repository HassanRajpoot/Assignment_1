from celery import shared_task
from .models import Transaction
from stocks.models import StockData

@shared_task
def process_transaction(transaction_id):
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    stock = StockData.objects.filter(ticker=transaction.ticker).latest('timestamp')
    user = transaction.user
    total_price = transaction.transaction_volume * stock.close_price
    if transaction.transaction_type == 'buy':
        if user.balance >= total_price:
            user.balance -= total_price
            user.save()
            transaction.transaction_price = stock.close_price
            transaction.save()
        else:
            transaction.delete()
    elif transaction.transaction_type == 'sell':
        user.balance += total_price
        user.save()
        transaction.transaction_price = stock.close_price
        transaction.save()
from django.db import models
from users.models import User

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    transaction_type = models.CharField(max_length=4, choices=[('buy', 'Buy'), ('sell', 'Sell')])
    transaction_volume = models.PositiveIntegerField()
    transaction_price = models.DecimalField(max_digits=20, decimal_places=4)
    timestamp = models.DateTimeField(auto_now_add=True)

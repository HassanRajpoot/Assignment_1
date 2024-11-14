from django.db import models

class StockData(models.Model):
    ticker = models.CharField(max_length=10)
    open_price = models.DecimalField(max_digits=10, decimal_places=2)
    close_price = models.DecimalField(max_digits=10, decimal_places=2)
    high = models.DecimalField(max_digits=10, decimal_places=2)
    low = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.BigIntegerField()
    timestamp = models.DateTimeField()

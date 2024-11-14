from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

from django.db import models


class Item(models.Model):
    CURRENCY = [
        ('EUR', 'eur'),
        ('USD', 'usd'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(choices=CURRENCY, default='usd')

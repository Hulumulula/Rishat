from django.db import models


class Item(models.Model):
    CURRENCY = (
        ()
    )
    name = models.CharField()
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(choices=CURRENCY)
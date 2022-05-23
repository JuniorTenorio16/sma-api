from sqlite3 import Timestamp
from django.db import models


class Sma(models.Model):
    pair = models.CharField(max_length=6, blank=False, default='BRLBTC')
    timestamp = models.DateField()
    close = models.DecimalField(max_digits=19, decimal_places=10)
    sma_20 = models.DecimalField(max_digits=19, decimal_places=10)
    sma_50 = models.DecimalField(max_digits=19, decimal_places=10)
    sma_200 = models.DecimalField(max_digits=19, decimal_places=10)
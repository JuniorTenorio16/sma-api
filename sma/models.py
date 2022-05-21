from sqlite3 import Timestamp
from django.db import models


class Sma(models.Model):
    pair = models.CharField(max_length=6, blank=False, default='BRLBTC')
    timestamp = models.DateField()
    sma_20 = models.FloatField()
    sma_50 = models.FloatField()
    sma_200 = models.FloatField()
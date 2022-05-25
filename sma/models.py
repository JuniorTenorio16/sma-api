from sqlite3 import Timestamp
from django.db import models


class Sma(models.Model):
    pair = models.CharField(max_length=6, blank=False, default='BRLBTC')
    timestamp = models.IntegerField()
    close = models.FloatField(blank=True)
    sma_20 = models.FloatField(null=True)
    sma_50 = models.FloatField(null=True)
    sma_200 = models.FloatField(null=True)


class RecordMissing(models.Model):
    timestamp = models.IntegerField()
    pair = models.CharField(max_length=6, blank=False, default='BRLBTC')
    status = models.BooleanField(default=True)
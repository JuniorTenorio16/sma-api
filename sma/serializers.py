from dataclasses import fields
from pyexpat import model
from sqlite3 import Timestamp
from rest_framework import serializers
from sma.models import Sma


class SmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sma
        fields = ('pair', 'timestamp', 'close', 'sma_20', 'sma_50', 'sma_200')


class CandlesSerializer(serializers.Serializer):
    close = serializers.DecimalField(max_digits=19, decimal_places=10)
    high = serializers.DecimalField(max_digits=19, decimal_places=10)
    low = serializers.DecimalField(max_digits=19, decimal_places=10)
    open = serializers.DecimalField(max_digits=19, decimal_places=10)
    timestamp = serializers.IntegerField()
    volume = serializers.DecimalField(max_digits=19, decimal_places=10)
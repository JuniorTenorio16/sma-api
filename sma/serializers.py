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
    close = serializers.FloatField()
    high = serializers.FloatField()
    low = serializers.FloatField()
    open = serializers.FloatField()
    timestamp = serializers.IntegerField()
    volume = serializers.FloatField()
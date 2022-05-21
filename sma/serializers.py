from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from sma.models import Sma

class SmaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sma
        fields=('pair', 'timestamp', 'sma_20', 'sma_50', 'sma_200')
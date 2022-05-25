from sqlite3 import Timestamp
from django.forms import ValidationError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from datetime import datetime

from sma.models import Sma
from sma.serializers import SmaSerializer
# Create your views here.


def validateDateFromTo(from_date, to_date):
    from_date = datetime.fromtimestamp(from_date)
    to_date = datetime.fromtimestamp(to_date)
    diff_date = (to_date-from_date).days

    if (datetime.now().date()-to_date.date()).days < 1:
        return False
    
    if diff_date < 1 and diff_date > 365:
        return False
    
    return True


def validateRange(range):
    range_valid = [20, 50, 200]
    if range not in range_valid:
        return False
    return True



@csrf_exempt
def smaApi(request, pair):
    if request.method=='GET':
        print(pair)
        sma_body = JSONParser().parse(request)
        if not validateDateFromTo(sma_body.get('from'), sma_body.get('to')):
            JsonResponse({
                    'status': 'false', 
                    'message': 'Date format or values ​​is invalid'
                }, 
                status=422)
        if validateRange(sma_body.get('range')):
            try:
                sma = Sma.objects.filter(timestamp__range=(sma_body.get('from'), sma_body.get('to')))
                sma_serializer = SmaSerializer(sma, many=True)
            except ValidationError as err:
                raise serializers.ValidationError('Error request mongo: %s'%err)
        else:
            JsonResponse({
                    'status': 'false', 
                    'message': 'Range value is invalid'
                }, 
                status=422)
    return JsonResponse(sma_serializer, safe=False)
    
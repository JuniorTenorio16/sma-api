from django.forms import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from datetime import datetime
import json

from sma.models import Sma
from sma.serializers import SmaSerializer


def validateDateFromTo(from_date, to_date):
    from_date = datetime.fromtimestamp(from_date)
    to_date = datetime.fromtimestamp(to_date)
    diff_date = (to_date-from_date).days

    if (datetime.now().date()-to_date.date()).days < 1:
        return False

    if diff_date < 1 or diff_date > 365:
        return False
    
    return True


def validateRange(range):
    range_valid = [20, 50, 200]
    if range not in range_valid:
        return False
    return True


def buildBodyResponse(data, range):
    body = []
    for sma in data:
        body.append({
            'timestamp': sma.get('timestamp'),
            'mms': sma.get('sma_%s'%range)
        })
    return body


def validateJsonRequest(data):
    if "to" not in data:
        return False
    if "from" not in data:
        return False
    if "range" not in data:
        return False
    return True


@csrf_exempt
def smaApi(request, pair):
    try:
        sma_body = JSONParser().parse(request)  
    except:
        return JsonResponse({
            'status': 'false', 
            'message': 'Json is invalid'
        })
    if validateJsonRequest(sma_body) is False:
        return JsonResponse({
                    'status': 'false', 
                    'message': 'Body request is invalid'
                }, 
                status=422)
    if request.method=='GET':
        if not validateDateFromTo(sma_body.get('from'), sma_body.get('to')):
            return JsonResponse({
                    'message': 'Either date format or values is invalid'
                }, 
                status=422)
        if validateRange(sma_body.get('range')):
            try:
                sma = Sma.objects.filter(timestamp__range=(sma_body.get('from'), sma_body.get('to')))
                sma_serializer = SmaSerializer(sma, many=True)
                sma_body_resp = buildBodyResponse(sma_serializer.data, sma_body.get('range'))
                return JsonResponse(sma_body_resp, safe=False)
            except ValidationError as err:
                return JsonResponse({
                    'status': 'false', 
                    'message': 'Error request mongo: %s'%err
                    }, status=422)
        else:
            return JsonResponse({
                    'status': 'false', 
                    'message': 'Range value is invalid'
                }, 
                status=422)
from django.forms import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from sma.models import Sma
from sma.serializers import SmaSerializer
from sma.utils import buildBodyResponse,\
     validateDateFromTo, validateJsonRequest, validateRange 


@csrf_exempt
def smaApi(request, pair):
    try:
        sma_body = JSONParser().parse(request)  
    except:
        return JsonResponse({
            'status': 'false', 
            'message': 'Json is invalid'
        },status=422)
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
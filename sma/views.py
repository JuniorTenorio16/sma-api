from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from sma.models import Sma
from sma.serializers import SmaSerializer
# Create your views here.

@csrf_exempt
def smaApi(request):
    if request.method=='GET':
        sma = Sma.objects.all()
        sma_serializer = SmaSerializer(sma, many=True)
        return JsonResponse(sma_serializer.data, safe=False)
    if request.method=='POST':
        sma_data = JSONParser().parse(request)
        sma_serializer = SmaSerializer(data=sma_data)
        if sma_serializer.is_valid():
            sma_serializer.save()
            return JsonResponse('Added Successfully', safe=False)
        return JsonResponse('Failed to Add', safe=False)
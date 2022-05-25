from asyncio import exceptions
from http import client
import imp
from itertools import count
import json
from datetime import datetime, timedelta
import httplib2
import sys

from sma.models import Sma
from sma.serializers import SmaSerializer, RecordMissingSerializer

presentday = datetime.now()
yesterday = presentday - timedelta(1)
lastyear = yesterday - timedelta(365) 

print(yesterday)
print(lastyear)


def getIntervalDate():
    presentday = datetime.now()
    yesterday = presentday - timedelta(1)
    lastyear = yesterday - timedelta(365)
    
    return int(round(yesterday.timestamp())), int(round(lastyear.timestamp()))


def calcSma(data, interval):
    smaInterval = 0
    if len(data) < interval:
        return None
    for sma in data[-interval:]:
        smaInterval += sma.get('close')
    smaInterval = smaInterval/interval
    return smaInterval


def insertRecordMissing(data):
    try:
        missing_serializer = RecordMissingSerializer(data=data)
        if missing_serializer.is_valid(raise_exception=True):
            missing_serializer.save()
    except Exception as err:
        print("Failed save new record : %s"%err)

def checkResponse(data):
    count = 0
    data.pop(53)
    if len(data) < 365:
        for sma in data:
            present = datetime.fromtimestamp(sma.get('timestamp'))
            tomorrow = datetime.fromtimestamp(data[count+1].get('timestamp'))
            diff = (tomorrow - present).days
            if diff > 1:
                day = 1
                while diff > day:
                    date_request = int(round((present + timedelta(day)).timestamp()))
                    missing = {
                        'timestamp': date_request,
                        'pair': 'BRLBTC',
                        'status': True
                    }
                    insertRecordMissing(missing)
                    day += 1
            count += 1
            if count == len(data)-1:
                break
    return True



def insertCandles(data):
    bulk_sma = []
    for candle in data:
        try:
            bulk_sma.append(candle)
            sma = {
                'pair': 'BRLBTC',
                'timestamp': candle.get('timestamp'),
                'close': candle.get('close'),
                'sma_20': calcSma(bulk_sma, 20),
                'sma_50': calcSma(bulk_sma, 50),
                'sma_200': calcSma(bulk_sma, 200)
            }
        except Exception as e:
            print("Error get values data : %s"%e)
            raise
        try:
            sma_serializer = SmaSerializer(data=sma)
            if sma_serializer.is_valid(raise_exception=True):
                print('x')
                # sma_serializer.save()
        except Exception as e:
            print("Failed save new record : %s"%e)

def getCandles():
    yesterday, lastyear = getIntervalDate()
    url = "https://mobile.mercadobitcoin.com.br/v4/BRLBTC/candle?from=%s&to=%s&precision=1d"%(lastyear, yesterday)
    try:
        http = httplib2.Http()
        resp = http.request(url)
        data = json.loads(resp[1])
    except ValueError as err:
        print('Error request url(%s) : %s'%(url, err))
        raise 
    candles = data.get('candles')
    
    checkResponse(candles)
    return data

getCandles()
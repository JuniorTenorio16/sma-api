from asyncio import exceptions
from http import client
import imp
import json
from datetime import datetime, timedelta
import httplib2
from sma.models import Sma
from sma.serializers import SmaSerializer, CandlesSerializer

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
            print(sma)
        except Exception as e:
            print ("Error get values data : %s"%e)
            raise
        try:
            sma_serializer = SmaSerializer(data=sma)
            if sma_serializer.is_valid(raise_exception=True):
                print('to aqui')
                sma_serializer.save()
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
    
    insertCandles(candles)
    return data

getCandles()
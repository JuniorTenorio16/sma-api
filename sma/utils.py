from datetime import datetime
import json

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
from datetime import datetime
from dateutil import tz
import time, sys
import csv

def retry(func, loops, erro, **kwargs):
    for _ in range(loops):
        try:
            result=func(kwargs)
            if result !=erro: return result
        except: 
            pass
    return False

def timestamp_converter(x): 
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]  

def time_now():
    #return (datetime.now().hour*3600)+datetime.now().minute*60+datetime.now().second
    return datetime.now().strftime('%H:%M:%S')

def contador():
    while True:
        sys.stdout.write(f'\r{time_now()}')
        sys.stdout.flush()
        time.sleep(1)

def into_clock(clocks, dif):
    if clocks==False:
        return True

    day = int(datetime.now().strftime("%w"))
    const_time = (datetime.now().hour*60)+datetime.now().minute

    if not day in clocks:
        return False

    zonas=clocks[day]

    for zona in zonas:
        if zona[0] < const_time < zona[1] - dif:
            return True
    return False

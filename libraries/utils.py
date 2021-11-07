from datetime import datetime
from dateutil import tz
import time, sys

def retry(func, loops, erro, **kwargs):
    for _ in range(loops):
        try:
            result=func(kwargs)
            if result !=erro: return result
        except: 
            pass
    return False

def time_now(formato='%H:%M:%S'):
    return datetime.now().strftime(formato)

def timestamp_converter(x): 
	hora = datetime.strptime(datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
	hora = hora.replace(tzinfo=tz.gettz('GMT'))
	
	return str(hora)[:-6]  

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

def to_json_js(dic):
    dic = str(dic).replace("'", '"')
    return dic

def calculate_pavio(vela):
    if vela[-1]==1 or vela[-1]==0:
        pavio_top = vela[2] - vela[4]
        pavio_bot = vela[1] - vela[3]
    elif vela[-1]==-1:
        pavio_top = vela[2] - vela[1]
        pavio_bot = vela[4] - vela[3]
    
    return pavio_top, pavio_bot

from datetime import datetime
from dateutil import tz
import time, sys
import win32com.client as comctl
import socket
from psutil import process_iter


wsh = comctl.Dispatch("WScript.Shell")

def check_port(port):
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == port:
                return True
    return False
    
def check_net():
    confiaveis = ['www.google.com', 'www.yahoo.com', 'www.bb.com.br']

    for host in confiaveis:
        a=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a.settimeout(.5)
        try:
            b=a.connect_ex((host, 80))
            if b==0: #ok, conectado
                return True
        except:
            pass
        a.close()
    return False

def press():
    global wsh
    wsh.SendKeys("{F15}")

def not_hibernate():
    global wsh
    while True:
        time.sleep(60)
        wsh.SendKeys("{F15}")

def force_error():
    return 5/0

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

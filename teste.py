from psutil import process_iter
from signal import SIGTERM 

def check_port(port):
    for proc in process_iter():
        for conns in proc.connections(kind='inet'):
            if conns.laddr.port == port:
                return True
    return False
check_port(8000)
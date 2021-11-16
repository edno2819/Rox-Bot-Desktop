from libraries.utils import calculate_pavio
from datetime import datetime
import time



def media_movel(velas, step):
    velas=[vela[4] for vela in velas]
    i = 0
    medias_moveis=[]

    while i < len(velas) - step + 1:
        grupo = velas[i : i + step]
        media_grupo = sum(grupo) / step
        medias_moveis.append(media_grupo)
        i +=1
    return medias_moveis

def wait_time(times):
    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    return True if minutos in times  else False

def filter_doji(velas:list):
    velas.reverse()
    try:
        while True:
            velas.remove(0)
    except ValueError: return velas
    
def RSI(nivel):...

class Strategy:
    SEGMENTO, time = 0, 0
    TIMES = {
        1:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        5:[4, 9],
        15:[4, 9],
    }

    def __init__(self, iq) -> None:
        self.iq=iq        
    
    def set_delay(self, delay:int):
        delay_seconds = ((60 + delay)/100)
        for key in self.TIMES.keys():
            self.TIMES[key] = [value + delay_seconds for value in self.TIMES[key]]
    
    def get_vela_for_time(self, velas, minute):
        for vela in velas:
            if vela[0][15]==minute:
                return vela

        return velas[-1]
            


    def modo(self, par, taxa_dif_vela=0.1) -> str:
            while True:
                time.sleep(0.2)
                if wait_time(self.TIMES[self.time]):
                    
                    minute = ((datetime.now()).strftime('%M'))[1:]
                    velas_=self.iq.get_velas(par, 2, self.time)
                    vela = self.get_vela_for_time(velas_, minute)

                    pavio_top, pavio_bot = calculate_pavio(vela)
                    direc = 1 if pavio_top>pavio_bot else -1
                    
                    '''PAVIOS TECNICAMENTE EMPATADOS'''
                    if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa_dif_vela:
                        direc = vela[-1]

                    if direc==1:
                        return 'CALL'
                    elif direc==-1:
                        return 'PUT'
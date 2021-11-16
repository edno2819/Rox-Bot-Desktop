from datetime import datetime
from libraries.iq_api import IqOption
from libraries.utils import calculate_pavio
import time
from main import send_infos_bet
from libraries.thread_class import Thread



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
                            


class MainOperation:

    def __init__(self, iq_instance) -> None:
        self.strategy = Strategy(iq_instance)
        self.iq = iq_instance
        self.configs = {'TIME_OPERATION': 1, 'delay': -2, 'entrada': 15, 'type_stop': 'porcent', 'ASSET': 'NZDUSD-OTC', 'type_operation': 'PRACTICE', 'stop_win': 5.0, 'LEVEL': 1, 'stop_loss': -9.0, 'BINA_DINA': 'DIGITAL'}

    def set_configs(self, configs):
        self.configs = {k: self.configs.get(k, 0) + configs.get(k, 0) for k in set(self.configs) | set(configs)}

    def set_init(self):
        self.iq.change_balance(self.configs['type_operation'])
        self.valor_entrada = self.configs['entrada']
        self.delay = self.configs['delay']
        self.asset = self.configs['ASSET']
        self.bina_dina = self.configs['BINA_DINA']
        self.level = self.configs['LEVEL']
        self.set_stops()
        self.strategy.set_delay(self.delay)
        self.strategy.time = self.configs['TIME_OPERATION']
        self.saldo = 0
    
    def set_stops(self):
        if self.configs['type_stop']=='porcent':
            saldo = self.iq.saldo()
            self.stop_loss = round(self.configs['stop_loss'] *  (saldo/100),2)
            self.stop_win = round(self.configs['stop_win'] * (saldo/100),2)
        else:
            self.stop_loss = self.configs['stop_loss']
            self.stop_win = self.configs['stop_win']
        
    def make_bet(self, direc):
        pass

    def check_result(self, id):
        pass

    def send_bet_to_gui(self, direc, level):
        def format_sinal():
            clock = datetime.now().strftime('%H:%M:%S')
            send_infos_bet({'clock':clock, 'direc':direc, 'level':level})

        #Thread(target=format_sinal).start()
        

        
    def run(self):
        for level in range(self.level):
            direc = self.strategy.modo(self.asset)
            self.make_bet(direc, level)
            self.send_bet_to_gui(direc, level)
            result = self.check_result()

            if result=='Loss':...
            
            elif result=='win':...
            
            elif result=='empate':...
            
            else:
                print('tratar erro')

        

# {'0': 29, '1': 16, '2': 3, '3': 3, '4': 0, '-1': 3, 
# 'ENTRADAS': ['2021-11-16 00:00:00', '2021-11-16 00:05:00', '2021-11-16 00:20:00', '2021-11-16 00:35:00', '2021-11-16 00:40:00', '2021-11-16 00:45:00', '2021-11-16 01:00:00', '2021-11-16 01:05:00', '2021-11-16 01:10:00', ...], 
# 'DIR': [1, 1, -1, -1, -1, -1, -1, -1, -1, ...], 'GALE': [0, 1, 1, 0, 0, 1, 0, 0, 1, ...], 'Derrota': 3, 'RESULTS': [29, 16, 3, 3, 0, 3], 
# 'COLS': ['0', '1', '2', '3', '4', 'Loss']}

#{'TIME_OPERATION': 1, 'delay': None, 'entrada': '15', 'type_stop': 'porcent', 'ASSET': 'NZDUSD-OTC', 
# 'type_operation': 'PRACTICE', 'stop_win': 5.0, 'LEVEL': 1, 'stop_loss': -9.0, 'BINA_DINA': 'DIGITAL'}

a = IqOption()
a.conect('edno28@hotmail.com', '99730755ed')
b = MainOperation(a)
b.set_init()
b.run()


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
    SEGMENTO=0

    def __init__(self, iq) -> None:
        self.iq=iq
        self.STRATEGYS={'MODO SEGMENTO': self.modo_segmento }

    def modo_segmento(self, par) -> tuple:
        if self.SEGMENTO==0:
            self.SEGMENTO+=1
            while True:
                time.sleep(0.2)
                if wait_time([1.59, 2.59, 3.59, 4.59, 5.59, 6.59, 7.59, 8.59, 9.59]):

                    velas_=self.iq.get_velas(par, 6, 1)
                    velas=filter_doji([vela[-1] for vela in velas_])
                    velas=[velas[0]]

                    if sum(velas)==1:
                        return 'CALL','GREEN'
                    elif sum(velas)==-1:
                        return 'PUT', 'RED'
        else:
            second = float(((datetime.now()).strftime('%S')))
            dif_time=60-second
            
            if second==0:
                time.sleep(1)

            elif dif_time<3:
                time.sleep(dif_time)

            velas_=self.iq.get_velas(par, 6, 1)
            if int(velas_[-1][0].split(':')[1]) == int(((datetime.now()).strftime('%M'))):
                velas_.pop(-1)

            if configs['DEBUG'] == 'True':
                print(second,velas_)

            velas=filter_doji([vela[-1] for vela in velas_])
            velas=[velas[0]]

            if sum(velas)==1:
                return 'CALL','GREEN'
            elif sum(velas)==-1:
                return 'PUT', 'RED'


class MainOperation:

    def __init__(self, iq_instance) -> None:
        self.iq = iq_instance
        self.manager = Management()
        self.configs = {}
    
    def set_configs(self, configs):
        self.configs = {k: self.configs.get(k, 0) + configs.get(k, 0) for k in set(self.configs) | set(configs)}

    def set_init(self):
        self.iq.MAIN.change_balance(self.configs['type_operation'])
        self.valor_entrada = self.configs['entrada']
        self.delay = self.configs['delay']
        self.asset = self.configs['ASSET']
        self.bina_dina = self.configs['BINA_DINA']
        self.level = self.configs['LEVEL']
        self.set_stops()
        self.saldo = 0
    
    def set_stops(self):
        if self.configs['type_stop']=='porcent':
            saldo = round(float(self.iq.MAIN.API.get_profile_ansyc()['balance'],2))
            self.stop_loss = (self.configs['stop_loss']/100) *  saldo
            self.stop_win = (self.configs['stop_win']/100) * saldo
        else:
            self.stop_loss = self.configs['stop_loss']
            self.stop_win = self.configs['stop_win']
    

        
    def run(self):



#{'TIME_OPERATION': 1, 'delay': None, 'entrada': '15', 'type_stop': 'porcent', 'ASSET': 'NZDUSD-OTC', 'type_operation': 'PRACTICE', 'stop_win': 5.0, 'LEVEL': 1, 'stop_loss': -9.0, 'BINA_DINA': 'DIGITAL'}
b = MainOperation()
b.setup_start()
b.run()


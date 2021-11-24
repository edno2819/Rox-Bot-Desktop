from libraries.managementes import Management
from libraries.thread_class import Thread
from libraries.strategys import Strategy
from datetime import datetime
import json
import eel


class GereBet:

    def empate(empates, level):
        empates+=1
        level-=1
        return level, empates

    def not_result(empates, level):
        empates+=1
        level-=1
        return level, empates   



class MainOperation:

    def __init__(self, iq_instance) -> None:
        self.strategy = Strategy(iq_instance)
        self.manage = Management()
        self.iq = iq_instance
        self.configs = {}


    def set_configs(self, configs):
        self.configs = {k: configs[k] if k in configs.keys() else self.configs[k] for k in set(self.configs) | set(configs)}


    def set_stops(self):
        if self.configs['type_stop']=='porcent':
            saldo = self.iq.saldo()
            self.stop_loss = round(self.configs['stop_loss'] *  (saldo/100),2)
            self.stop_win = round(self.configs['stop_win'] * (saldo/100),2)
        else:
            self.stop_loss = self.configs['stop_loss']
            self.stop_win = self.configs['stop_win']


    def set_functions(self):
        types = {'DIGITAL': self.iq.bet_digital, 'BINARIA': self.iq.bet_binaria}
        self.make_bet = types[self.configs['BINA_DINA']]


    def set_init(self):
        self.iq.change_balance(self.configs['type_operation'])
        self.valor_entrada = self.configs['ENTRADA']
        self.delay = self.configs['DELAY']
        self.asset = self.configs['ASSET']
        self.level = self.configs['LEVEL']
        self.strategy.set_delay(self.delay)
        self.time_operation = self.configs['TIME_OPERATION']
        self.strategy.time = self.time_operation
        self.values_bet = self.manage.martingale_fixo(self.valor_entrada, self.level, mult=2.5)
        self.set_functions()
        self.set_stops()
        self.saldo = 0


    def run(self):
        wait = True
        msg = False
        while self.saldo < self.stop_win and self.saldo > self.stop_loss:

            try:
                direc = self.strategy.rox(self.asset, wait=wait)
                wait = self.making_bet_martingale(direc)
            except:
                msg = 'Operação Parada!'
                break

        self.send_finally_to_gui(msg)


    def beting_martin(self, bet, direc, lucro):
        clock = datetime.now().strftime('%H:%M:%S')
        result = self.make_bet(self.asset, bet, direc, self.time_operation)
        lucro += result
        return result, clock, lucro


    def making_bet_martingale(self, direc):
        level, lucro, empates = (0, 0, 0)
        result, time_bet, lucro = self.beting_martin(self.values_bet[0], direc, lucro)
        self.saldo += result

        self.send_bet_to_gui(time_bet, direc, self.values_bet[0], level, result)

        result = False if result==0 else result

        if not result: return True

        for level in range(1, 20):
            level = level-empates

            if result==0:
                level, empates = GereBet.empate(empates, level)

            elif not result: 
                level, empates = GereBet.not_result(empates, level)

            elif result>0:
                wait =  False if level==1 else True
                return wait
            
            if level>self.level: 
                return True
                
            if level==-1: 
                level=0

            
            bet_value = self.values_bet[level]
            result, time_bet, lucro = self.beting_martin(bet_value, direc, lucro)  
            self.saldo += result
            self.send_bet_to_gui(time_bet, direc, self.values_bet[level], level, result)


    def send_bet_to_gui(self, time_bet, direc, value_bet, level, result):
        if not result:
            result = 'O.N.R'
            
        def format_sinal():
            infos = {'time_bet':time_bet, 'direc':direc, 'level':level, 'value_bet':value_bet, 'result':result,'saldo':round(self.saldo,2)}
            eel.refresh_operation(json.dumps(infos))
            
        Thread(target=format_sinal).start()


    def send_finally_to_gui(self, msg):
        if not msg:
            msg = 'Stop Loss Atingido!' if self.saldo<0 else 'Stop Win Atingido!'
            
        def send_alert():
            infos = {'msg':msg}
            eel.alert_stop_goal(json.dumps(infos))
            
        Thread(target=send_alert).start()
import libraries.utils  as utils
from libraries.strategys import Strategy
from libraries.managementes import Management
from datetime import datetime
from libraries.utils import to_json_js
import eel
import time
from libraries.thread_class import Thread



class MainOperation2:

    def __init__(self, iq_instance) -> None:
        self.iq = iq_instance
        self.strategy = Strategy(self.iq)
        self.manager = Management()
        self.configs = {}
    
    def set_configs(self, configs):
        self.configs = {k: configs[k] if k in configs.keys() else self.configs[k]  for k in set(self.configs) | set(configs)}

    def setup_start(self) -> None:
        self.sets_functions()
        self.time_operation = int(self.configs['TIME_OPERATION'])
        self.saldo = 0
        
    def sets_functions(self):
        types = {'DIGITAL': self.iq.bet_digital, 'BINARIA': self.iq.bet_binaria}
        manages = {1: self.making_bet, 2: self.making_bet, 3: self.making_bet_segment}

        self.make_bet = types[self.configs['type_operactin']]
        self.sets_bet = manages[self.manager_value]
        
    def run(self):
        LAST_OPERATION = True
        warn_py= True
        warn_time= True

        while self.saldo < self.configs['stop_win'] and self.saldo > self.configs['stop_loss']*-1:
            clock_ok = utils.into_clock(self.clocks_run, int(self.configs['STOP_BEFORE_CLOSE_ASSET']))

            if clock_ok or LAST_OPERATION:
                self.atualizar_entradas()

                if self.payout < int(self.configs['PAUOUT_MIN']):
                    if warn_py: 
                        print(f'\nPausa por Payout! Payout: {self.payout}') 
                        warn_py = False

                    time.sleep(int(self.configs['TIME_WAIT']))

                else:
                    direc, major = self.strategy.STRATEGYS[self.configs['strategy']](self.configs['par'])
                    self.prints.operation_opportunity(self.configs['strategy'], major)
                    self.sets_bet(direc)

                    LAST_OPERATION = False if clock_ok == False else True
                    warn_py = True
                    warn_time = True
            else:
                if warn_time: 
                    print('\nPausa por horário de fechamento!')
                    warn_time = False

                time.sleep(int(self.configs['TIME_WAIT']))

        self.prints.stop_bot_saldo(self.saldo)

    def fist_operation(self, direc):
        level, lucro, empates = (0, 0, 0)
        result=self.make_bet(self.configs['par'], self.leveis[0], direc, self.time_operation, self.prints.operation_status)
        lucro+=result
        self.saldo+=result
        self.prints.operation_result(self.leveis[0], lucro)

        result = False if result==0 else result

        return result, level, lucro, empates

    def atualizar_entradas(self):
        self.payout = self.iq.payout(self.configs['par'], self.type_operation)
        self.leveis = self.manager.operation(self.type_gerenciamento, self.configs['bet_value'], self.payout)
        self.leveis = self.leveis[:self.configs['level']]

    def print_results(self, lucro, result, bet, level, time_bet, direc):
        self.saldo+=result
        self.prints.operation_result_gale(result, f'{bet:.02f}', f'{lucro:.02f}', self.name_gere, level, time_bet, direc)

    def empate(self, empates, level):
        empates+=1
        level-=1
        return level, empates
    
    def not_result(self, empates, level):
        self.prints.operation_status(False)
        self.manager.quatro_por_um(True, 5)
        empates+=1
        level-=1
        return level, empates     

    def beting_martin(self, bet, direc, lucro):
        time_bet= utils.time_now()
        result=self.make_bet(self.configs['par'], bet, direc, self.time_operation)
        lucro+=result
        return result, time_bet, lucro
    
    def making_bet(self, direc):
        result, level, lucro, empates = self.fist_operation(direc)
        if not result:
            return 

        for level in range(1,20):
            level = level-empates

            if result==0:#EMPATEs
                level, empates = self.empate(empates, level)
           
            elif not result: 
                level, empates = self.not_result(empates, level)

            elif result<0:#DERROTA
                self.manager.quatro_por_um(self.quatro_por_um, level)

            elif result>0:#VITORIA 
                return

            if level>=len(self.leveis): 
                print(f'Fim de ciclo!')
                return 
                
            if level==-1: 
                level=0
                
            bet=self.leveis[level]    
            result, time_bet, lucro = self.beting_martin(bet, direc, lucro)       
            self.print_results(lucro, result, bet, level, time_bet, direc)

    def making_bet_segment(self, direc):
        result, level, lucro, empates = self.fist_operation(direc)
        if not result:
            return 

        for level in range(1,20):
            level = level-empates

            if result==0:#EMPATEs
                level, empates = self.empate(empates, level)

            elif not result: 
                level, empates = self.not_result(empates, level)


            elif result<0:#DERROTA
                self.manager.quatro_por_um(self.quatro_por_um, level)
                    
            elif result>0:#VITORIA 
                return
            
            if level>=len(self.leveis): 
                return 
                
            if level==-1: 
                level=0

            direc, _ = self.strategy.modo_segmento(self.configs['par'])

            bet=self.leveis[level]
            result, time_bet, lucro = self.beting_martin(bet, direc, lucro)       
            self.print_results(lucro, result, bet, level, time_bet, direc)


class MainOperation:

    def __init__(self, iq_instance) -> None:
        self.strategy = Strategy(iq_instance)
        self.iq = iq_instance
        self.configs = {}

    def set_configs(self, configs):
        self.configs = {k: configs[k] if k in configs.keys() else self.configs[k] for k in set(self.configs) | set(configs)}

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
        
    def make_bet(self, direc, level):
        pass

    def check_result(self, id):
        pass

    def send_bet_to_gui(self, direc, level, n, amount):
        @eel.expose
        def format_sinal():
            clock = datetime.now().strftime('%H:%M:%S')
            infos = {'n':n, 'clock':clock, 'direc':direc, 'level':level}
            eel.refresh_operation(to_json_js(infos))
            
        Thread(target=format_sinal).start()
        

        
    def run(self):
        n=0
        for level in range(self.level):
            direc = self.strategy.modo(self.asset)
            amount = 0
            self.make_bet(direc, level)
            self.send_bet_to_gui(direc, level, n, amount)
            result = self.check_result(level)

            if result=='Loss':...
            
            elif result=='win':...
            
            elif result=='empate':...
            
            else:
                print('tratar erro')
            n+=1
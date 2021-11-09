import libraries.utils  as utils
from libraries.strategys import Strategy
from libraries.managementes import Management
import time


class MainOperation:

    def __init__(self, iq_instance) -> None:
        self.iq = iq_instance
        self.strategy = Strategy(self.iq)
        self.manager = Management()
        self.configs = {}
    
    def set_configs(self, configs):
        self.configs = {k: self.configs.get(k, 0) + configs.get(k, 0) for k in set(self.configs) | set(configs)}

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



# b = MainOperation()
# b.setup_start()
# b.run()


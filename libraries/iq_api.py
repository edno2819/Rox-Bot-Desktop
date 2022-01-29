from iqoptionapi.stable_api import IQ_Option
import libraries.utils as utils
import time


class IqOption:        
    def conect(self, conta, senha):
        self.API = IQ_Option(conta, senha)
        self.API.connect()
        self.type ='PRACTICE'
        
        if self.API.check_connect(): 
            return True
        else: 
            return False

    def reconnect(self):
        if not self.API.check_connect(): 
            self.API.connect()
            self.API.change_balance(self.type)
            return self.API.check_connect()

    def change_balance(self, type='PRACTICE'):
        '''PRACTICE / REAL'''
        self.type = type
        self.API.change_balance(type)
        
    def saldo(self):
        self.perfil = self.API.get_profile_ansyc()
        saldo = self.perfil['balances'][1]['amount'] if self.type =='PRACTICE' else self.perfil['balances'][0]['amount']
        return saldo

    def get_assets_open(self):
        bina=[]
        digi=[]
        pares = self.API.get_all_open_time()
        for paridade in pares['turbo']:
            if pares['turbo'][paridade]['open']==True:
                bina.append(paridade)

        for paridade in pares['digital']:
            if pares['digital'][paridade]['open']==True:
                digi.append(paridade)
        return bina, digi

    def payout_all(self):
        bina, digi = self.get_assets_open()
        pares = self.API.get_all_profit()
        bina_dict = {}
        digi_dict = {}

        for par in bina:
            bina_dict[par] = int(100 * pares[par]['turbo'])

        for par in digi:
            digi_dict[par]= self.API.get_digital_payout(par)

        return bina_dict, digi_dict

    def payout(self, par, tipo):
        if tipo == 'BINARIA':
            pares = self.API.get_all_profit()
            return int(100 * pares[par]['turbo'])
            
        elif tipo == 'DIGITAL':
            return self.API.get_digital_payout(par)

    def get_velas(self, par, step:int, time_frame:int):
        result=[]
        velas = self.API.get_candles(par, time_frame*60, step+1, time.time())
        for vela in velas:
            direct= (1 if vela['open']<vela['close'] else -1) if vela['open']!=vela['close'] else 0
            vela_convert=[str(utils.timestamp_converter(vela['from'])),vela['open'],vela['max'],vela['min'],vela['close'], direct]
            result.append(vela_convert)
        return result

    def get_velas_complete(self, par, step:int, time_frame:int):
        result=[]
        velas = self.API.get_candles(par, time_frame*60, step+1, time.time())
        for vela in velas:
            direct= (1 if vela['open']<vela['close'] else -1) if vela['open']!=vela['close'] else 0
            vela_convert=[str(utils.timestamp_converter(vela['from'])),vela['open'],vela['max'],vela['min'],vela['close'], direct]
            result.append(vela_convert)
        return result

    def get_velas_live(self, par, step:int, time_frame:int):
        '''size= 1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all" em segundos'''

        self.API.start_candles_stream(par, time_frame*60, step)
        velas=self.API.get_realtime_candles(par,time_frame)
        for item in velas:
            clock=utils.timestamp_converter(item)
            vela = velas[item]
            vela_convert=[str(utils.timestamp_converter(vela['from'])),vela['open'],vela['max'],vela['min'],vela['close'],vela['volume']]
        self.API.stop_candles_stream(par,time_frame)

    def bet_binaria(self, par:str, amount:float, action:str, time_frame:int, func=''):
        status, id = self.API.buy(amount, par, action, time_frame)
        func(status, action) if func!='' else ...

        if status:
            status2,lucro=self.API.check_win_v4(id)
            if status2:
                return round(lucro, 2)
        else: return False

    def bet_digital(self, par:str, amount:float, action:str, time_frame:int, func=''):
        '''action = CALL/PUT'''

        _, id = self.API.buy_digital_spot_v2(par, amount, action, time_frame)
        status = True if id != "error" else False

        func(status, action) if func!='' else ...

        if id != "error":
            while True:
                time.sleep(0.1)
                check , win = self.API.check_win_digital_v2(id)
                if check==True: 
                    return  round(win,2)

        else: return False

    def close(self):
        self.API.api.close()


if __name__ == 'main':
    iq = IqOption()
    iq.conect('edno@hotmail.com', '99730755ed')
    iq.change_balance()
    assets = iq.payout_all()
    par = 'EURUSD-OTC'
    time = 1
    iq.bet_digital(par , 2, 'CALL', 1)
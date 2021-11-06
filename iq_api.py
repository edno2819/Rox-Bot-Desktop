from iqoptionapi.stable_api import IQ_Option
import libraries.utils as utils
import time


class IqOption:
        
    def conect(self, conta, senha):
        self.API = IQ_Option(conta, senha)
        self.API.connect()
        if self.API.check_connect(): return True
        else: return False

    def change_balance(self, type='PRACTICE'):
        '''PRACTICE / REAL'''
        self.type=type
        self.API.change_balance(type)
        
    def saldo(self):
        self.perfil=self.API.get_profile_ansyc()
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

    def get_velas_live(self, par, step:int, time_frame:int):
        #size=[1,5,10,15,30,60,120,300,600,900,1800,3600,7200,14400,28800,43200,86400,604800,2592000,"all"] em segundos
        self.API.start_candles_stream(par, time_frame*60, step)
        velas=self.API.get_realtime_candles(par,time_frame)
        for item in velas:
            clock=utils.timestamp_converter(item)
            vela=velas[item]
            vela_convert=[str(utils.timestamp_converter(vela['from'])),vela['open'],vela['max'],vela['min'],vela['close'],vela['volume']]
        self.API.stop_candles_stream(par,time_frame)

    def bet_binaria(self, par:str, amount:float, action:str, time_frame:int, func=''):
        status,id = self.API.buy(amount, par, action, time_frame)
        func(status, action) if func!='' else ...

        if status:
            status2,lucro=self.API.check_win_v4(id)
            if status2:
                return round(lucro, 2)
        else: return False

    def bet_digital(self, par:str, amount:float, action:str, time_frame:int, func=''):
        #action = CALL/PUT

        _, id = self.API.buy_digital_spot_v2(par, amount, action, time_frame)
        status = True if id != "error" else False

        func(status, action) if func!='' else ...

        if id != "error":
            while True:
                time.sleep(0.1)
                check,win=self.API.check_win_digital_v2(id)
                if check==True: return  round(win,2)
        else: return False

    def close(self):
        self.API.api.close()


def calculate_pavio(vela):
    if vela[-1]==1 or vela[-1]==0:
        pavio_top = vela[2] - vela[4]
        pavio_bot = vela[1] - vela[3]
    elif vela[-1]==-1:
        pavio_top = vela[2] - vela[1]
        pavio_bot = vela[4] - vela[3]
    
    return pavio_top, pavio_bot

t=IqOption()
t.conect('edno28@hotmail.com', '99730755ed')
tp = t.get_velas('EURUSD-OTC', 20, 5)
#pari = t.get_assets_open()


def catalogacao(asset:str, time:int, clock_init:str, level:int, taxa:float=0.15):
    RESULT = {c:0 for c in range(level+1)}
    RESULT[-1] = 0
    RESULT['ENTRADAS'], RESULT['DIR'] = [], []
    ve = t.get_velas(asset, 200, time)

    day = '-'+'06'

    for c in ve:
        if day in c[0] and clock_init in c[0]:
            print(c)
            break
    velas = ve[ve.index(c):]

    '''PERCORRENDO AS VELAS'''
    G=0
    for c in range(len(velas)):

        '''VERIFICANDO SE AS VELAS JA ACABARAM'''
        if c+G+1+level > len(velas):
            return RESULT

        vela = velas[c+G]
        pavio_top, pavio_bot = calculate_pavio(vela)
        direc = 1 if pavio_top>pavio_bot else -1
        
        '''PAVIOS TECNICAMENTE EMPATADOS'''
        if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa:
            direc  = vela[-1]#tratar tamanho da vela

        '''VERIFICAR RESULTADO DA ENTRADA'''
        if direc!=0:
            RESULT['ENTRADAS'].append(vela)
            RESULT['DIR'].append(direc)
            velas_ope = velas[c+G+1:c+G+1+level]
            velas_ope = [f[-1] for f in velas_ope]
            win = -1 if direc not in velas_ope else velas_ope.index(direc)
            if win==-1:
                G+=level+1
            elif win>0:
                G+=win+1

            RESULT[win] +=1

cat = catalogacao('EURUSD-OTC', 5, '10:00:00', 4)
cat

            


    
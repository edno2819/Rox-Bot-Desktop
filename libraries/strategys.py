from libraries.utils import calculate_pavio, time_now
from datetime import datetime, timedelta
from time import sleep
import logging

class CandlestickAnality:
    SEGMENTO = 0
    TIMES = {
        1:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        5:[4, 9],
        15:[4, 9]}

    def set_delay(self, delay:int):
        if delay>=0:
            delay = -1

        delay_seconds = ((60 + delay)/100)
        for key in self.TIMES.keys():
            self.TIMES[key] = [round(value + delay_seconds,2) for value in self.TIMES[key]]
        return self.TIMES

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
    
    def get_vela_for_time(velas, minute):
        for vela in velas:
            if vela[0][15]==minute:
                return vela
        return velas[-1]
            
    def RSI(nivel):...



class Trigger:
    def __init__(self, iq) -> None:
        self.log = logging.getLogger(__name__)    
        self.analy = CandlestickAnality()
        self.analy.set_delay(-1)
        self.iq = iq
    
    def catalogacao(self, asset:str, time:int, level:int, taxa:float=0.15, clock_init='03:00:00'):
        RESULT = {str(c):0 for c in range(level+1)}
        RESULT['-1'] = 0
        RESULT['ENTRADAS'], RESULT['DIR'], RESULT['GALE'] = [], [], []
        ve = self.iq.get_velas(asset, 15, time)

        day = '-'+time_now('%d')+' '

        axo = False
        for c in ve:
            if day in c[0] and clock_init in c[0]:
                axo = True
                break
        velas = ve[ve.index(c):] if axo else ve

        '''PERCORRENDO AS VELAS'''
        G=0
        for c in range(len(velas)):

            '''VERIFICANDO SE AS VELAS JA ACABARAM'''
            if c+G+1+level > len(velas):
                
                '''TRATANDO O RESULTADO PARA ENVIO'''
                RESULT['Derrota'] = RESULT['-1']
                RESULT['RESULTS'] = [RESULT[str(c)] for c in range(level+1)]
                RESULT['RESULTS'].append(RESULT['-1'])
                RESULT['COLS'] = [str(c) for c in range(level+1)]
                RESULT['COLS'].append('Loss')
                RESULT['ENTRADAS'] = [str(datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3, minutes=0)) for date in RESULT['ENTRADAS']]
                return RESULT

            vela = velas[c+G]
            pavio_top, pavio_bot = calculate_pavio(vela)
            direc = 1 if pavio_top>pavio_bot else -1
            
            '''PAVIOS TECNICAMENTE EMPATADOS'''
            if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa:
                direc  = vela[-1]#tratar tamanho da vela

            '''VERIFICAR RESULTADO DA ENTRADA'''
            if direc!=0:
                RESULT['ENTRADAS'].append(vela[0])
                RESULT['DIR'].append(direc)
                velas_ope = velas[c+G+1:c+G+1+level+1]
                velas_ope = [f[-1] for f in velas_ope]
                win = -1 if direc not in velas_ope else velas_ope.index(direc)
                if win==-1:
                    G+=level+1
                elif win>0:
                    G+=win+1

                RESULT[str(win)] +=1
                RESULT['GALE'].append('Loss' if win==-1 else win)

    def rox_trigger(self, asset, time, level, loss_to_trigger):
        while True:
            sleep(0.2)
            if CandlestickAnality.wait_time(self.analy.TIMES[time]):
                result = self.catalogacao(asset, time, level)
                if result['GALE'][len(result['GALE']) - loss_to_trigger:].count('Loss')==loss_to_trigger:
                    self.log.info(f'Result to Trigger ROX {result["ENTRADAS"][len(result["ENTRADAS"]) - loss_to_trigger:]}')
                    return



class Strategy:
    SEGMENTO = 0
    TIMES = {
        1:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        5:[4, 9],
        15:[4, 9],
    }

    def __init__(self, iq) -> None:
        self.log = logging.getLogger(__name__)    
        self.iq=iq   
        self.time = 1 
    

    def set_delay(self, delay:int):
        if delay>=0:
            delay = -1

        self.TIMES = {
                    1:[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                    5:[4, 9],
                    15:[4, 9],
                    }

        delay_seconds = ((60 + delay)/100)
        for key in self.TIMES.keys():
            self.TIMES[key] = [round(value + delay_seconds,2) for value in self.TIMES[key]]
        self.log.info(f"Set delay: {self.TIMES[self.time]}")

    
    def rox(self, par, taxa_dif_vela=0.1, wait=True) -> str:
        def rox_():
            minute = ((datetime.now()).strftime('%M'))
            velas_=self.iq.get_velas(par, 2, self.time)
            vela = CandlestickAnality.get_vela_for_time(velas_, minute[1:])

            pavio_top, pavio_bot = calculate_pavio(vela)
            direc = 1 if pavio_top>pavio_bot else -1

            self.log.info(f"Vela de operação {vela}; Maior pavio {direc}")

            if int(time_now("%S"))>4 and int(time_now("%S"))<=55 and wait==True:
                self.log.info(f"Sinal cancelado por delay; Entrada ROX {minute}")
                return 'INDE'

            
            '''PAVIOS TECNICAMENTE EMPATADOS'''
            if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa_dif_vela:
                direc = vela[-1]

            if direc==1:
                return 'CALL'
            elif direc==-1:
                return 'PUT'
            else: 
                return 'INDE'

        while True:
            direc = 'INDE'
            if wait:
                sleep(0.2)
                if CandlestickAnality.wait_time(self.TIMES[self.time]):
                    direc = rox_()
            else:
                direc = rox_()

            if direc in ['PUT', 'CALL']:
                return direc

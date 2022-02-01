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


class Catalog:

    def __init__(self, iq, asset, time, level, clock_init='03:00:00') -> None:
        self.log = logging.getLogger(__name__) 
        self.clock_init = clock_init
        self.asset = asset
        self.time = time
        self.iq = iq
        self.level = level
    
    def setResult(self):
        self.RESULT = {str(c):0 for c in range(-1,self.level+1)}
        self.RESULT['ENTRADAS'], self.RESULT['DIR'], self.RESULT['GALE'] = [], [], []

    def get_direct(self, vela, taxa):
        pavio_top, pavio_bot = calculate_pavio(vela)
        direc = 1 if pavio_top>pavio_bot else -1
        if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa:
            direc  = vela[-1]
        return direc
    
    def exclue_velas(self, velas):
        axo = False
        day = '-'+time_now('%d')+' '
        for c in velas:
            if day in c[0] and self.clock_init in c[0]:
                axo = True
                break
        return velas[velas.index(c):] if axo else velas

    def get_velas(self):
        qtd_velas = int(((60* int(time_now('%H'))/self.time)+1)+60)
        ve = self.iq.get_velas(self.asset, qtd_velas, self.time)
        return self.exclue_velas(ve)

    def standartOperation(self, velas, direc, jump, c):
        exit, resu = False, False
        velas_ope = velas[c+jump+1:c+jump+1+self.level+1] 
        direc_velas = [f[-1] for f in velas_ope]
        win = -1 if direc not in direc_velas else direc_velas.index(direc)

        if win==-1:
            jump+=self.level+1
            if velas_ope[-1]==velas[-1]:
                self.log.info(f'Saida da catalogação por Standart loss: velas_ope[-1]==velas[-1]')
                exit = True
                resu =  (self.level+1) - len(direc_velas) 

        elif win>0:
            jump+=win+1
            if velas_ope[-1]==velas[-1] and win+1==len(direc_velas):
                self.log.info(f'Saida da catalogação por Standrt Win: velas_ope[-1]==velas[-1] and win+1==len(direc_velas)')
                exit = True

        return exit, resu, win, jump

    def lastOperation(self, velas, direc, jump, c):
        exit, resu = False, False
        velas_ope = velas[c+jump+1:]
        direc_velas = [f[-1] for f in velas_ope]
        win = -1 if direc not in direc_velas else direc_velas.index(direc)

        if win==-1:
            self.log.info(f'Saida da catalogação por Last loss')
            exit = True
            resu =  (self.level+1) - len(direc_velas) # Perdeu em todos os gales == 0
        elif win>0:
            jump+=win+1
            #Se for a unica vela ele sai
            if len(direc_velas)==1:
                self.log.info(f'Saida da catalogação por Last win: len(direc_velas)==1')
                exit = True
                resu = 'run'
            elif win+1==len(direc_velas):
                self.log.info(f'Saida da catalogação por Last win: win+1==len(direc_velas)')
                exit = True
                resu = 'wait'
        return exit, resu, win, jump

    def formatReturnResult(self):
        self.RESULT['Derrota'] = self.RESULT['-1']

        self.RESULT['RESULTS'] = [self.RESULT[str(c)] for c in range(self.level+1)]
        self.RESULT['RESULTS'].append(self.RESULT['-1'])

        self.RESULT['COLS'] = [str(c) for c in range(self.level+1)]
        self.RESULT['COLS'].append('Loss')

        self.RESULT['GALE'].reverse()
        self.RESULT['DIR'].reverse()
        self.RESULT['ENTRADAS'].reverse()

        self.RESULT['ENTRADAS'] = [str(datetime.strptime(date, '%Y-%m-%d %H:%M:%S') - timedelta(hours=3, minutes=0)) for date in self.RESULT['ENTRADAS']]
        return self.RESULT

    def catalogacao(self, taxa:float=0.15):
        exit, resu = False, False
        self.setResult()
        velas = self.get_velas()

        jump = 0
        for c in range(len(velas)):
            if exit:  
                return resu, self.formatReturnResult(), direc 

            vela = velas[c+jump]
            direc = self.get_direct(vela, taxa)

            if direc!=0:
                self.RESULT['ENTRADAS'].append(vela[0])
                self.RESULT['DIR'].append(direc)

                if len(velas)>c+jump+1+self.level:
                    exit, resu, win, jump = self.standartOperation(velas, direc, jump, c)
                else:
                    exit, resu, win, jump = self.lastOperation(velas, direc, jump, c)

                self.RESULT[str(win)] +=1
                self.RESULT['GALE'].append('Loss' if win==-1 else win)        

    def catalogacao2(self, taxa:float=0.15):
        exit, resu = False, False
        self.setResult()
        velas = self.get_velas()

        jump = 0
        for c in range(len(velas)):
            if exit:  
                return resu, self.formatReturnResult()

            vela = velas[c+jump]
            direc = self.get_direct(vela, taxa)

            if direc!=0:
                self.RESULT['ENTRADAS'].append(vela[0])
                self.RESULT['DIR'].append(direc)

                if len(velas)>=c+jump+1+self.level+1:
                    exit, resu, win, jump = self.standartOperation(velas, direc, jump, c)
                else:
                    exit, resu, win, jump = self.lastOperation(velas, direc, jump, c)

                self.RESULT[str(win)] +=1
                self.RESULT['GALE'].append('Loss' if win==-1 else win)

              
            if c+jump+1>=len(velas):
                exit = True
                resu = False


class Strategy:
    SEGMENTO = 0
    TIMES = CandlestickAnality.TIMES

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

        sleep(5) if wait else '' 
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

        qtd_velas = int(((60* int(time_now('%H'))/time)+1)+60)
        ve = self.iq.get_velas(asset, qtd_velas, time)

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


    def catalogacao_next_vela(self, asset:str, time:int, level:int, taxa:float=0.15, clock_init='03:00:00'):
        last, exit, resu = False, False, False

        qtd_velas = int(((60* int(time_now('%H'))/time)+1)+60)

        ve = self.iq.get_velas(asset, qtd_velas, time)

        day = '-'+time_now('%d')+' '

        axo = False
        for c in ve:
            if day in c[0] and clock_init in c[0]:
                axo = True
                break
        velas = ve[ve.index(c):] if axo else ve

        G=0
        for c in range(len(velas)):

            if exit:    
                return resu

            vela = velas[c+G]
            pavio_top, pavio_bot = calculate_pavio(vela)
            direc = 1 if pavio_top>pavio_bot else -1

            if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa:
                direc  = vela[-1]
                
            if direc!=0:
                if len(velas)>=c+G+1+level+1:
                    velas_ope = velas[c+G+1:c+G+1+level+1] 

                else:
                    velas_ope = velas[c+G+1:]
                    last = True

                velas_ope = [f[-1] for f in velas_ope]

                win = -1 if direc not in velas_ope else velas_ope.index(direc)
                if win==-1:
                    if last:
                        exit = True
                        resu = 1 if len(velas_ope)==level+1 else False
                    else:
                        G+=level+1
                elif win>0:
                    last=False
                    G+=win+1
                    if len(velas_ope)==1 or len(velas)<=c+1+G:
                        exit = True
                        resu = win

            else:
                if len(velas[c+G+1:])==1:
                    exit = True
                    resu = win


    def rox_trigger(self, asset, time, level, loss_to_trigger):
        self.log.info(f'Trigger ROX Init')
        stratgy = Catalog(self.iq, asset, time, level)

        while True:
            sleep(0.2)
            if CandlestickAnality.wait_time(self.analy.TIMES[time]):
                res, result, _ = stratgy.catalogacao()
                #if 'Loss' in result['GALE'][:1]:    teste
                if res==0 and 'Loss'== result['GALE'][0] or 'Loss'== result['GALE'][1]:
                    self.log.info(f'Start operation - Result to Trigger ROX {result["ENTRADAS"][0]} aqui ------------')
                    return


    def rox_trigger_next_vela(self, asset, time, level, loss_to_trigger):
        '''
        Casos:
            1 - 
        '''
        self.log.info(f'Trigger ROX Init')
        stratgy = Catalog(self.iq, asset, time, level)

        while True:
            sleep(0.2)
            if CandlestickAnality.wait_time(self.analy.TIMES[time]):
                trigger, result, dir = stratgy.catalogacao()
                if result!=False:
                    break

        count = 0
        while True:
            sleep(0.2)

            if trigger=='run':
                self.log.info(f'Start operation - Result to Trigger ROX Next Vela 1: {result["ENTRADAS"][0]}, Triger: {trigger},  Dir: {dir}')
                return True

            elif trigger=='wait' or trigger==0:
                sleep(30)
                self.log.info(f'Start operation - Result to Trigger ROX Next Vela 2: {result["ENTRADAS"][0]}, Triger: {trigger},  Dir: {dir}')
                return False

            elif type(trigger)==int:
                if CandlestickAnality.wait_time(self.analy.TIMES[time]):
                    velas = self.iq.get_velas(asset, 1, time)
                    if velas[-1][-1]==dir or count==trigger:
                        wait = trigger!=level+1 and count!=0
                        self.log.info(f'Start operation - Result to Trigger ROX Next Vela 3: {result["ENTRADAS"][0]} wair: {wait}, Triger: {trigger},  Dir: {dir}')
                        sleep(30) if wait else ''#caso seja win de primeira
                        return wait
                    count+=1#verificar quando for win de primeira fora da catalogação
                    sleep(3)


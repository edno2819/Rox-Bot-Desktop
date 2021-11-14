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
    


class Strategy:
    SEGMENTO=0

    def __init__(self, iq) -> None:
        self.iq=iq
        self.STRATEGYS={
                        'MODO SEGMENTO': self.modo_segmento
                        }


    def mhi_minoria(self, par, time_out=1) -> tuple:
        while True:
            time.sleep(0.2)           
            if  wait_time([4.58, 4.59, 9.58, 9.59]):

                velas=self.iq.get_velas(par, 9, time_out)
                velas=filter_doji([vela[-1] for vela in velas])
                velas=[velas[0], velas[1], velas[2]]

                if sum(velas)>=1:
                    return 'PUT', 'GREEN'
                elif sum(velas)<=-1:
                    return 'CALL','RED'


    def mhi_maioria(self, par, time_out=1) -> tuple:
        while True:
            time.sleep(0.2)           
            if  wait_time([4.58, 4.59, 9.58, 9.59]):

                velas=self.iq.get_velas(par, 9, time_out)
                velas=filter_doji([vela[-1] for vela in velas])
                velas=[velas[0], velas[1], velas[2]]

                if sum(velas)>=1:
                    return 'CALL', 'GREEN'
                elif sum(velas)<=-1:
                    return 'PUT','RED'
                

    def torres_gemeas(self, par) -> tuple:
        while True:
            time.sleep(0.2)        
            if  wait_time([3.58, 3.59, 8.58, 8.59]):

                velas=self.iq.get_velas(par, 7, 1)
                velas=filter_doji([vela[-1] for vela in velas[:5]])
                velas=[velas[0]]

                if sum(velas)==1:
                    return 'CALL','GREEN'
                elif sum(velas)==-1:
                    return 'PUT', 'RED'


    def tres_mosqueteiros(self, par) -> tuple:
        while True:
            time.sleep(0.2)
            if wait_time([2.58, 2.59, 7.58, 7.59]):

                velas=self.iq.get_velas(par, 6, 1)
                velas=filter_doji([vela[-1] for vela in velas])
                velas=[velas[0]]

                if sum(velas)==1:
                    return 'CALL','GREEN'
                elif sum(velas)==-1:
                    return 'PUT', 'RED'


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

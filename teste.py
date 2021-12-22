from libraries.utils import calculate_pavio, time_now
from libraries.iq_api import IqOption



MAIN = IqOption()
MAIN.conect("edno28@hotmail.com","99730755ed")
par = "EURGBP"
time = 1
level = 3

class ets:

    def __init__(self, iq, asset, time, clock_init) -> None:
        self.clock_init = clock_init
        self.asset = asset
        self.time = time
        self.iq = iq
    
    def setResult(self):
        self.RESULT = {str(c):0 for c in range(-1,level+1)}
        self.RESULT['ENTRADAS'], self.RESULT['DIR'], self.RESULT['GALE'] = [], [], []

    def get_direct(self, vela, taxa):
        pavio_top, pavio_bot = calculate_pavio(vela)
        direc = 1 if pavio_top>pavio_bot else -1
        if abs(pavio_top - pavio_bot)<=min(pavio_top, pavio_bot)*taxa:
            direc  = vela[-1]#tratar tamanho da vela
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
        qtd_velas = int(((60* int(time_now('%H'))/time)+1)+60)
        ve = self.iq.get_velas(self.asset, qtd_velas, time)
        return self.exclue_velas(ve)

    def standartOperation(self, velas, direc, G, c):
        velas_ope = velas[c+G+1:c+G+1+level+1] 
        direc_velas = [f[-1] for f in velas_ope]
        win = -1 if direc not in direc_velas else direc_velas.index(direc)
        if win==-1:
                G+=level+1
        elif win>0:
            G+=win+1

        return win, G

    def lastOperation(self, velas, direc, G, c):
        velas_ope = velas[c+G+1:]
        direc_velas = [f[-1] for f in velas_ope]
        win = -1 if direc not in direc_velas else direc_velas.index(direc)

        if win==-1:
            exit = True
            resu = 1 if len(direc_velas)==level+1 else False
        elif win>0:
            G+=win+1
            if len(direc_velas)==1 or len(velas)<=c+1+G:
                exit = True
                resu = win
        return exit, resu, win, G

    def catalogacao(self, level:int, taxa:float=0.15):
        exit, resu = False, False
        self.setResult()
        velas = self.get_velas()

        G=0
        for c in range(len(velas)):
            if exit:    
                return resu

            vela = velas[c+G]
            direc = self.get_direct(vela, taxa)

            if direc!=0:
                self.RESULT['ENTRADAS'].append(vela[0])
                self.RESULT['DIR'].append(direc)

                if len(velas)>=c+G+1+level+1:
                    win, G = self.standartOperation(velas, direc, G, c)
                else:
                    exit, resu, win, G = self.lastOperation(velas, direc, G, c)

                self.RESULT[str(win)] +=1
                self.RESULT['GALE'].append('Loss' if win==-1 else win)


def asd():
    stratgy = ets(MAIN, par, time, '03:00:00')
    result = stratgy.catalogacao(2)


asd()
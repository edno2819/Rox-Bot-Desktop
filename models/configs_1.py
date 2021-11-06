from libraries.run import MAIN
from libraries.utils import calculate_pavio

 

 
def get_assets_py():
    result = MAIN.payout_all()
    asssets = list(set(list(result[1].keys()) + list(result[0].keys())))
    return asssets


def catalogar(asset, time):
    time = int(time)
    asset
    return 


def catalogacao(asset:str, time:int, clock_init:str, level:int, taxa:float=0.15):
    RESULT = {c:0 for c in range(level+1)}
    RESULT[-1] = 0
    RESULT['ENTRADAS'], RESULT['DIR'] = [], []
    ve = MAIN.get_velas(asset, int(1000/time), time)

    day = '-'+'06'#pegar data

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
            RESULT['ENTRADAS'].append(vela[0])
            RESULT['DIR'].append(direc)
            velas_ope = velas[c+G+1:c+G+1+level]
            velas_ope = [f[-1] for f in velas_ope]
            win = -1 if direc not in velas_ope else velas_ope.index(direc)
            if win==-1:
                G+=level+1
            elif win>0:
                G+=win+1

            RESULT[win] +=1
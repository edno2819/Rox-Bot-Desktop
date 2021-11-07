from libraries.run import MAIN
from libraries.utils import calculate_pavio, time_now
from datetime import datetime


 

 
def get_assets_py():
    result = MAIN.payout_all()
    asssets = list(set(list(result[1].keys()) + list(result[0].keys())))
    return asssets


def catalogar(asset, time):
    time = int(time)
    asset
    return 


def catalogacao(asset:str, time:int, clock_init:str, level:int, taxa:float=0.15):
    RESULT = {str(c):0 for c in range(level+1)}
    RESULT['-1'] = 0
    RESULT['ENTRADAS'], RESULT['DIR'], RESULT['GALE'] = [], [], []
    ve = MAIN.get_velas(asset, int(1000/time), time)

    day = '-'+time_now('%d')+' '

    for c in ve:
        if day in c[0] and clock_init in c[0]:
            break
    velas = ve[ve.index(c):]

    '''PERCORRENDO AS VELAS'''
    G=0
    for c in range(len(velas)):

        '''VERIFICANDO SE AS VELAS JA ACABARAM'''
        if c+G+1+level > len(velas):
            RESULT['Derrota'] = RESULT['-1']
            RESULT['RESULTS'] = [RESULT[str(c)] for c in range(level+1)]
            RESULT['RESULTS'].append(RESULT['-1'])
            RESULT['COLS'] = [str(c) for c in range(level+1)]
            RESULT['COLS'].append('Loss')
            #'0'+str(int(RESULT['ENTRADAS'][0][11:13])-3) if len(str(int(RESULT['ENTRADAS'][0][11:13])-3))==1 else str(int(RESULT['ENTRADAS'][0][11:13])-3)
            RESULT['ENTRADAS'] = [str(datetime.strptime(date[11:], '%H:%M:%S') - datetime.strptime('03:00:00', '%H:%M:%S')) for date in RESULT['ENTRADAS']]
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

            RESULT[str(win)] +=1
            RESULT['GALE'].append('Loss' if win==-1 else win)
        
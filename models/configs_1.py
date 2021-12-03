from libraries.utils import calculate_pavio, time_now
from datetime import datetime, timedelta
from libraries.iq_global import *


 
def get_assets_py():
    result = MAIN.payout_all()
    asssets = [f'BINARIA: {key} PY: {result[0][key]}' for key in result[0].keys()]
    asssets += [f'DIGITAL: {key} PY: {result[1][key]}' for key in result[1].keys()]
    return asssets


def catalogacao(asset:str, time:int, level:int, taxa:float=0.15, clock_init='03:00:00'):
    RESULT = {str(c):0 for c in range(level+1)}
    RESULT['-1'] = 0
    RESULT['ENTRADAS'], RESULT['DIR'], RESULT['GALE'] = [], [], []
    ve = MAIN.get_velas(asset, int(1000/time), time)

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
            RESULT['Derrota'] = RESULT['-1']

            RESULT['RESULTS'] = [RESULT[str(c)] for c in range(level+1)]
            RESULT['RESULTS'].append(RESULT['-1'])

            RESULT['COLS'] = [str(c) for c in range(level+1)]
            RESULT['COLS'].append('Loss')

            RESULT['GALE'].reverse()
            RESULT['DIR'].reverse()
            RESULT['ENTRADAS'].reverse()

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
    
    
def set_variables_configs1(asset, time, nivel, bina_dina):
    LOG.debug(f"Set configs 1: {asset}, {time}, {bina_dina}, {nivel}")
    MAIN_RUN.set_configs({'ASSET':asset, 'TIME_OPERATION':int(time), 'BINA_DINA':bina_dina, 'LEVEL':int(nivel)})

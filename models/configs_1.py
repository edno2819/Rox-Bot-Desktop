from libraries.iq_global import *
from libraries.strategys import *

 
def get_assets_py():
    result = MAIN.payout_all()
    asssets = [f'BINARIA: {key} PY: {result[0][key]}' for key in result[0].keys()]
    asssets += [f'DIGITAL: {key} PY: {result[1][key]}' for key in result[1].keys()]
    return asssets


def catalogacao(asset:str, time:int, level:int, taxa:float=0.15, clock_init='03:00:00'):
    stratgy = Catalog(MAIN, asset, time, level, clock_init)
    _, result, _ = stratgy.catalogacao(taxa)
    return result
    
def set_variables_configs1(asset, time, nivel, bina_dina):
    LOG.debug(f"Set configs 1: {asset}, {time}, {bina_dina}, {nivel}")
    dic = {'ASSET':asset, 'TIME_OPERATION':int(time), 'BINA_DINA':bina_dina, 'LEVEL':int(nivel)}
    MAIN_RUN.set_configs(dic)
    LOG.info(f"set configs2 : {dic.__str__()}")

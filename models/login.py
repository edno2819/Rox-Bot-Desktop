from libraries.google_sheets import get_data_sheet
from libraries.iq_global import MAIN
from libraries.utils import time_now
from dateutil.parser import parse


USERS = get_data_sheet()

def get_msg_sheet():
    msg = '\n'.join(USERS['mensagem'])
    return {'mensagem': msg[1:]}

def login_user(user_name, password):
    activ_bot , activ_iq = False, False
    if user_name in USERS['clientes'].keys():
        if USERS['clientes'][user_name]=='':
            activ_bot = True
        elif parse(USERS['clientes'][user_name])>=parse(time_now('%d/%m/%y')):
            activ_bot = True

    if MAIN.conect(user_name,password):
        activ_iq = True
    return activ_bot , activ_iq

def login_session():
    return ''

    
    
    
    

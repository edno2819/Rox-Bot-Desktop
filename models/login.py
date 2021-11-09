from libraries.google_sheets import get_data_sheet
from libraries.iq_global import MAIN

USERS = get_data_sheet()
 

def login_user(user_name, password):
    activ_bot , activ_iq = False, False
    if user_name in USERS['clientes']:
        activ_bot = True
    if MAIN.conect(user_name,password):
        activ_iq = True
    return activ_bot , activ_iq

def login_session():
    return ''

    
    
    
    

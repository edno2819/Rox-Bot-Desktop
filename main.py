from __future__ import print_function	
import eel
from models.login import *
from models.configs import *


eel.init('views')
teste = 0

@eel.expose # USADO PARA FUNCAO SER VISTA NO JS
def btn_save(name,phone,date,login,passw,email):
    msg = 'save_register(name,phone,date,login,passw,email)'
    eel.save_return(str(msg))


@eel.expose
def btn_recovery(email):
    msg = ''
    eel.reco_return(str(msg))


@eel.expose
def btn_login(user_name, password):
    result = login_user(user_name, password)
    result = '{'+f'"status_bot": "{result[0]}", "status_iq": "{result[1]}"' + '}'
    eel.login_return(str(result))

@eel.expose
def start_configs_1():
    infos = get_infos()
    return str(infos)

@eel.expose
def bnt_config_confirmar(stop_loss):
    global teste
    teste = stop_loss


@eel.expose
def bnt_sair():
    logout()




eel.start("index.html", size=(730,700))
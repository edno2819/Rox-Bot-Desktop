from __future__ import print_function	
import eel
from models.login import *
from models.configs_1 import *
from models.configs_2 import *
from libraries.utils import to_json_js


eel.init('views')


@eel.expose
def btn_login(user_name, password):
    result = login_user(user_name, password)
    result = '{'+f'"status_bot": "{result[0]}", "status_iq": "{result[1]}"' + '}'
    eel.login_return(str(result))

@eel.expose
def get_assets():
    result = get_assets_py()
    eel.create_list_assets(to_json_js(result))

@eel.expose
def bnt_catalogar(asset, time, nivel):
    result = catalogacao(asset, int(time), '03:00:00', int(nivel))
    eel.creat_table_catalog(to_json_js(result))

@eel.expose
def start_configs_2():
    infos = get_infos()
    eel.get_infos_init(to_json_js(infos))

@eel.expose
def bnt_config_confirmar(stop_loss):
    global teste
    teste = stop_loss


@eel.expose
def bnt_sair():
    logout()


# exibir erro no backtest

eel.start("index.html", size=(730,700))
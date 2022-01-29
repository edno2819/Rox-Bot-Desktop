from libraries.utils import to_json_js, time_now, check_port
from models.configs_1 import *
from models.configs_2 import *
from models.login import *
from models.run import *
import eel, sys
import logging


class GerePages:
    current_html = 'index.html'

    def ChangeCurrentPage(self, name):
        self.current_html = name


@eel.expose
def get_mensagem():
    eel.get_mensagem_init(to_json_js(get_msg_sheet())) 


@eel.expose
def change_current_page(name):
    gerepages.ChangeCurrentPage(name)


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
    bina_dina, asset, _, _ = asset.split(' ')
    result = catalogacao(asset, int(time), int(nivel))
    eel.creat_table_catalog(to_json_js(result))


@eel.expose
def start_configs_2():
    infos = get_infos()
    eel.get_infos_init(to_json_js(infos))


@eel.expose
def bnt_config_confirmar(asset, time, gale):
    bina_dina, asset, _, _ = asset.split(' ')
    set_variables_configs1(asset, time, gale, bina_dina.replace(":", ''))
    return 


@eel.expose
def bnt_sair():
    logout()


@eel.expose
def bnt_config_confirmar2(entrada, delay, stop_win, stop_loss, type_operation, type_stop, trigger, multiplier):
    set_variables_configs2(entrada, delay, stop_win, stop_loss, type_operation, type_stop, trigger, multiplier)


@eel.expose
def set_run_infos():
    infos = run_gere.get_infos_run()
    eel.get_infos_run(to_json_js(infos))


@eel.expose
def bnt_iniciar():
    run_gere.start_operation()


@eel.expose
def bnt_parar(): 
    run_gere.stop_operation()


def close_callback(route, websockets):
    global log

    if route=='run.html' and gerepages.current_html=='run.html':
        try:
            run_gere.NOT_HIBERNATE.kill()
            run_gere.stop_operation()
            logout()
        except Exception as e:
            log.info(f'Erro in exit run.html: {e}')
        sys.exit(0)

    elif route=='index.html'  and gerepages.current_html=='index.html':
        sys.exit(0)

    elif route=='configs_1.html'  and gerepages.current_html=='configs_1.html':
        try:
            logout()
            sys.exit(0)
        except Exception as e:
            log.info(f'Erro in exit configs_2.html: {e}')
            sys.exit(0)

    elif route=='configs_2.html'  and gerepages.current_html=='configs_2.html':
        try:
            logout()
            sys.exit(0)
        except Exception as e:
            log.info(f'Erro in exit configs_2.html: {e}')
            sys.exit(0)


def start_eel():
    ports = [8000, 8001, 27000, 8080]

    for port in ports:
        if not check_port(port):
            eel.start("index.html", size=(730,700), port=port, close_callback=close_callback)
            return



if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(name)s %(levelname)s %(message)s',
        filename=f'./logs/log_{time_now("%Y-%m-%d %H-%M-%S")}.log',
        filemode='w')

    log = logging.getLogger(__name__)

    gerepages = GerePages()
    run_gere = MeneRun()

    eel.init('views')
    start_eel()

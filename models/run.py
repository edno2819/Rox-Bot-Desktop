from libraries.iq_global import *
from libraries.thread_class import Thread
from libraries.utils import not_hibernate
import eel
import json


class MeneRun:
    NOT_HIBERNATE = Thread(target=not_hibernate)
    
    def get_infos_run(self):
        result = MAIN.API.get_profile_ansyc()
        name = result['name']
        return {"name":name, "balance":MAIN.saldo(), 'asset':MAIN_RUN.asset, 'bina_dina':MAIN_RUN.configs['BINA_DINA'],'nivel':MAIN_RUN.level, 'time':MAIN_RUN.time_operation}
    
    def reset_thread(self):
        self.THREAD_RUN = Thread(target=MAIN_RUN.run)

    def start_operation(self):
        MAIN.reconnect()
        self.reset_thread()
        LOG.info('Start operation button!')
        #MAIN_RUN.run()
        self.THREAD_RUN.start()

    def stop_operation(self):
        self.THREAD_RUN.kill()
        eel.alert_stop_goal(json.dumps({'msg':'Operação Parada!'}))
    


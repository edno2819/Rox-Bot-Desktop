from libraries.iq_global import *
from libraries.thread_class import Thread

THREAD_RUN = Thread(target=MAIN_RUN.run)


def get_infos_run():
    result = MAIN.API.get_profile_ansyc()
    name = result['name']
    return {"name":name, "balance":MAIN.saldo()}


def start_operation():
    MAIN_RUN.run()
    #THREAD_RUN.start()


def stop_operation():
    THREAD_RUN.kill()

def checks():...
    # entrada n pode ser maior q saldo



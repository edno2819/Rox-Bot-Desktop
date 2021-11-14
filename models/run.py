from libraries.iq_global import *
from libraries.thread_class import Thread
import threading

THREAD_RUN = Thread(target=MAIN_RUN.run)


def start_operation():
    THREAD_RUN.start()


def stop_operation():
    THREAD_RUN.kill()



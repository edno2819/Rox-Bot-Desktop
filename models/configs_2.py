from libraries.iq_global import *
 
def logout():
    MAIN.close()

def get_infos():
    result = MAIN.API.get_profile_ansyc()
    currency_char = result['currency']
    name = result['name']
    balance = round(float(result['balance']),2)
    LOG.debug(f"Get infos 2  : {currency_char}, {name}, {balance}")
    
    return {"currency_char":currency_char , "name":name, "balance":balance}

def set_variables_configs2(entrada, delay, stop_win, stop_loss, type_operation, type_stop, trigger, multiplier):
    stop_win = 0 if stop_win=='' else stop_win
    stop_loss = 0 if stop_loss=='' else stop_loss
    LOG.info(f"set configs2 : {entrada}, {delay}, {stop_win}, {stop_loss}, {type_operation}, {type_stop}")
    type_operation = 'PRACTICE'#TIRAR
    MAIN_RUN.set_configs({
    'ENTRADA':abs(float(entrada)), 'DELAY':int(round(float(delay),0)), 
    'TRIGGER':int(trigger.replace(',', '.')),'stop_win':float(stop_win), 
    'stop_loss':float(stop_loss), 'type_operation':type_operation, 
    'type_stop':type_stop, 'MUTIPLIER':float(multiplier)
    })

    MAIN_RUN.set_init()
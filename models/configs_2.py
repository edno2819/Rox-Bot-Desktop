from libraries.iq_global import *
 
def logout():
    MAIN.close()

def get_infos():
    result = MAIN.API.get_profile_ansyc()
    currency_char = result['currency']
    name = result['name']
    balance = round(float(result['balance']),2)
    return {"currency_char":currency_char , "name":name, "balance":balance}

def set_variables_configs2():
    MAIN_RUN.set_configs({})

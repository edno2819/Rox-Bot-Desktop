from libraries.run import MAIN
 

 
def get_assets_py():
    result = MAIN.payout_all()
    asssets = list(set(list(result[1].keys()) + list(result[0].keys())))
    return asssets


def catalogar(asset, time):
    time = int(time)
    asset
    return 


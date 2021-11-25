from datetime import datetime
import time

class Management:

    def __init__(self) -> None:
        self.types= {1: self.martingale, 2: self.recuperacao, 3:self.mao_fixa}

    def operation(self, op, bet, py):
        self.types[op](bet, py)
        return self.levels

    def martingale(self, bet:float, py:int):
        fator=py/100
        leveis=[bet*py/100,bet]

        for level in range(14):
            valor = ((bet*(level+2)*fator)+sum(leveis[1:]))/fator
            leveis.append(round(valor, 1))

        self.levels=leveis[1:]

    def martingale_fixo(self, bet:float, level, mult=2.3):
        leveis = [bet]
        for c in range(1,level+1):
            value = leveis[c-1]*mult
            leveis.append(value)
        
        return leveis

    def recuperacao(self, bet:float, py:int):
        fator=(py/100)
        leveis=[bet]

        for _ in range(9):
            total=sum(leveis)
            leveis.append(round(total/fator,2))

        self.levels=leveis

    def mao_fixa(self, bet:float, py:int):
        self.levels=[bet for c in range(10)]

    def quatro_por_um(self, status, level):
        if status and level>=5:
            time.sleep(5)
            wait=59-int(datetime.now().strftime('%S'))
            time.sleep(wait)
            return True
        return False

# a=Management()
# a.martingale_fixo(10, 4)
# print(a.levels)
            